"""
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
  This file is part of the Smart Developer Hub Project:
    http://www.smartdeveloperhub.org

  Center for Open Middleware
        http://www.centeropenmiddleware.com/
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
  Copyright (C) 2015 Center for Open Middleware.
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at 

            http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
"""

__author__ = 'Fernando Serena'

import calendar
from sdh.metrics.server import MetricsApp
from sdh.metrics.ci.store import CIStore
from sdh.metrics.store.metrics import store_calc
import os
import urlparse

config = os.environ.get('CONFIG', 'sdh.metrics.ci.config.DevelopmentConfig')

app = MetricsApp(__name__, config)
st = CIStore(**app.config['REDIS'])
app.store = st


@st.query(['?_oh org:hasProduct ?prod', '?prod org:id ?prid'])
def query_products(arg):
    product_uri = arg.get('prod')
    product_name = arg.get('prid')
    st.execute('sadd', 'frag:products', product_uri)
    st.execute('set', 'frag:products:{}:'.format(product_name), product_uri)
    st.execute('hset', 'frag:products:-{}-:'.format(product_uri), 'name', product_name)


@st.query(['?_oh org:hasProject ?proj', '?proj org:id ?pjid', '?proj doap:repository ?repo'])
def query_projects(arg):
    project_uri = arg.get('proj')
    project_name = arg.get('pjid')
    st.execute('sadd', 'frag:projects', project_uri)
    st.execute('set', 'frag:projects:{}:'.format(project_name), project_uri)
    st.execute('hset', 'frag:projects:-{}-:'.format(project_uri), 'name', project_name)
    repo_name = urlparse.urlparse(arg.get('repo')).path.split('/').pop(-1)
    st.execute('sadd', 'frag:projects:-{}-:repos'.format(project_uri),
               repo_name)


@st.query(['?prod org:relatesToProject ?proj'])
def add_project(arg):
    st.execute('sadd', 'frag:products:-{}-:projects'.format(arg.get('prod')), arg.get('proj'))
    st.execute('sadd', 'frag:projects:-{}-:products'.format(arg.get('proj')), arg.get('prod'))


@st.collect('?h ci:hasBuild ?b')
def add_build((h, _, b_uri)):
    st.execute('sadd', 'frag:builds', b_uri)


@st.collect('?b ci:includesBuild ?sb')
def add_sub_build((p_uri, _, b_uri)):
    st.execute('sadd', 'frag:builds', b_uri)
    st.execute('sadd', 'frag:builds:-{}-:sub'.format(p_uri), b_uri)


@st.collect('?sh scm:hasRepository ?r')
def search_repository(_):
    pass


@st.collect('?r scm:repositoryId ?rid')
def add_repository_id((r_uri, _, rid)):
    st.execute('hset', 'frag:repos:-{}-:'.format(r_uri), 'id', rid.toPython())
    st.execute('set', 'frag:repos:{}:'.format(rid.toPython()), r_uri)


@st.collect('?r scm:location ?rl')
def add_repository_location((r_uri, _, location)):
    st.execute('hset', 'frag:repos:-{}-:'.format(r_uri), 'location', location.toPython())


@st.collect('?r doap:name ?rn')
def add_repository((r_uri, _, name)):
    st.execute('hset', 'frag:repos:-{}-:'.format(r_uri), 'name', name.toPython())
    st.execute('set', 'frag:reponames:{}:'.format(name), r_uri)


@st.collect('?e scm:location ?loc')
def link_location((e_uri, _, location)):
    location = location.toPython()
    if location:
        repo_name = urlparse.urlparse(location).path.split('/').pop(-1)
        repo_name = repo_name.replace('.git', '')
        st.execute('set', 'frag:jobs:-{}-:repo'.format(e_uri), repo_name)
        st.execute('sadd', 'frag:repos:-{}-:jobs'.format(repo_name), e_uri)


@st.collect('?ab ci:hasExecution ?e')
def add_execution((b_uri, _, e_uri)):
    st.execute('sadd', 'frag:builds:-{}-:jobs'.format(b_uri), e_uri)
    st.execute('set', 'frag:jobs:-{}-:'.format(e_uri), b_uri)


@st.collect('?e dcterms:created ?et')
def add_execution((e_uri, _, created)):
    timestamp = calendar.timegm(created.toPython().timetuple())
    st.execute('zadd', 'frag:sorted-jobs', timestamp, e_uri)
    st.execute('set', 'frag:jobs:-{}-:created'.format(e_uri), timestamp)


@st.collect('?e ci:finished ?tf')
def add_finished_execution((e_uri, _, t)):
    timestamp = calendar.timegm(t.toPython().timetuple())
    st.execute('zadd', 'frag:jobs:finished'.format(e_uri), timestamp, e_uri)
    st.execute('set', 'frag:jobs:-{}-:finished'.format(e_uri), timestamp)


@st.collect('?e oslc_auto:state ?st')
def add_execution_result((e_uri, _, state)):
    st.execute('set', 'frag:jobs:-{}-:state'.format(e_uri), state.toPython())


@st.collect('?e ci:hasResult ?jr')
def add_execution_result((e_uri, _, r_uri)):
    st.execute('set', 'frag:jobs:-{}-:result'.format(e_uri), r_uri)


@st.collect('?jr oslc_auto:verdict ?v')
def add_execution_result((jr_uri, _, verdict)):
    st.execute('set', 'frag:results:-{}-:'.format(jr_uri), verdict.toPython())


@app.calculus(triggers=['add_execution'])
def update_interval_jobs(begin, end):
    jobs = st.get_jobs(begin, end)
    store_calc(st, 'metrics:total-jobs', begin, len(jobs))

    results = [(j, st.db.get('frag:jobs:-{}-:result'.format(j))) for j in jobs]
    verdicts = filter(lambda (_, v): v is not None,
                      [(j, st.db.get('frag:results:-{}-:'.format(r))) for (j, r) in results])
    passed_jobs = [j for (j, v) in verdicts if 'passed' in v]
    failed_jobs = [j for (j, v) in verdicts if 'failed' in v]
    store_calc(st, 'metrics:total-passed-jobs', begin, len(passed_jobs))
    store_calc(st, 'metrics:total-failed-jobs', begin, len(failed_jobs))


@app.calculus(triggers=['add_execution'])
def update_interval_repo_metrics(begin, end):
    totals = {}
    passed = {}
    failed = {}
    for rid in st.get_repositories():
        jobs = st.get_jobs(begin, end, rid=rid)
        totals[rid] = len(jobs)
        store_calc(st, 'metrics:total-repo-jobs:{}'.format(rid), begin, totals[rid])

        results = [(j, st.db.get('frag:jobs:-{}-:result'.format(j))) for j in jobs]
        verdicts = filter(lambda (_, v): v is not None,
                          [(j, st.db.get('frag:results:-{}-:'.format(r))) for (j, r) in results])
        passed_jobs = [j for (j, v) in verdicts if 'passed' in v]
        passed[rid] = len(passed_jobs)
        failed_jobs = [j for (j, v) in verdicts if 'failed' in v]
        failed[rid] = len(failed_jobs)
        store_calc(st, 'metrics:total-passed-repo-jobs:{}'.format(rid), begin, passed[rid])
        store_calc(st, 'metrics:total-failed-repo-jobs:{}'.format(rid), begin, failed[rid])

    for product in st.get_products():
        product_total = 0
        product_passed = 0
        product_failed = 0
        projects = st.get_product_projects(product)
        for project in projects:
            project_total = 0
            project_passed = 0
            project_failed = 0
            for rid in set.intersection(set(totals.keys()), st.get_project_repositories(project)):
                project_total += totals[rid]
                project_passed += passed[rid]
                project_failed += failed[rid]
            store_calc(st, 'metrics:total-project-jobs:{}'.format(project), begin, project_total)
            store_calc(st, 'metrics:total-passed-project-jobs:{}'.format(project), begin, project_passed)
            store_calc(st, 'metrics:total-failed-project-jobs:{}'.format(project), begin, project_failed)
            product_total += project_total
            product_passed += project_passed
            product_failed += project_failed

        store_calc(st, 'metrics:total-product-jobs:{}'.format(product), begin, product_total)
        store_calc(st, 'metrics:total-passed-product-jobs:{}'.format(product), begin, product_passed)
        store_calc(st, 'metrics:total-failed-product-jobs:{}'.format(product), begin, product_failed)
