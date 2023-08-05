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

from sdh.metrics.ci import app, st as store
from sdh.metrics.store.metrics import aggregate, avg, flat_sum
from sdh.metrics.server import SCM, ORG, CI
import calendar
from datetime import datetime
import math


@app.metric('/total-builds', id='builds', title='Builds')
def get_total_builds(**kwargs):
    return [len(store.get_builds())]


@app.metric('/total-repo-builds', id='repository-builds', title='Builds', parameters=[SCM.Repository])
def get_repo_builds(rid, **kwargs):
    return [len(store.get_repo_builds(rid))]


@app.metric('/avg-builds', aggr='avg', id='builds', title='Builds')
def get_avg_builds(**kwargs):
    return avg([len(store.get_repo_builds(rid)) for rid in store.get_repositories()])


@app.metric('/total-executions', id='executions', title='Executions')
def get_total_executions(**kwargs):
    return aggregate(store, 'metrics:total-jobs', kwargs['begin'], kwargs['end'], kwargs['max'])


@app.metric('/total-passed-builds', id='passed-builds', title='Passed builds')
def get_total_passed_builds(**kwargs):
    success_builds = 0
    for build in store.get_builds():
        last_passed = store.get_last_passed_execution(build, kwargs['begin'], kwargs['end'])
        if last_passed:
            success_builds += 1
    return {}, [success_builds]


@app.metric('/total-failed-builds', id='failed-builds', title='Failed builds')
def get_total_failed_builds(**kwargs):
    failed_builds = 0
    for build in store.get_builds():
        last_passed = store.get_last_passed_execution(build, kwargs['begin'], kwargs['end'])
        if not last_passed or last_passed is None:
            failed_builds += 1
    return {}, [failed_builds]


@app.metric('/total-passed-executions', id='passed-executions', title='Passed executions')
def get_total_passed_executions(**kwargs):
    return aggregate(store, 'metrics:total-passed-jobs', kwargs['begin'], kwargs['end'], kwargs['max'])


@app.metric('/total-failed-executions', id='failed-executions', title='Failed executions')
def get_total_failed_executions(**kwargs):
    return aggregate(store, 'metrics:total-failed-jobs', kwargs['begin'], kwargs['end'], kwargs['max'])


@app.metric('/total-repo-executions', id='repository-executions', title='Executions', parameters=[SCM.Repository])
def get_total_repo_executions(rid, **kwargs):
    return aggregate(store, 'metrics:total-repo-jobs:{}'.format(rid), kwargs['begin'], kwargs['end'], kwargs['max'])


@app.metric('/avg-repo-executions', aggr='avg', id='repository-executions', title='Executions',
            parameters=[SCM.Repository])
def get_avg_repo_executions(rid, **kwargs):
    return aggregate(store, 'metrics:total-repo-jobs:{}'.format(rid), kwargs['begin'], kwargs['end'], kwargs['max'],
                     aggr=avg)


@app.metric('/total-passed-repo-executions', id='passed-repository-executions', title='Passed executions',
            parameters=[SCM.Repository])
def get_total_passed_repo_executions(rid, **kwargs):
    return aggregate(store, 'metrics:total-passed-repo-jobs:{}'.format(rid), kwargs['begin'], kwargs['end'],
                     kwargs['max'])


@app.metric('/total-failed-repo-executions', id='failed-repository-executions', title='Failed executions',
            parameters=[SCM.Repository])
def get_total_failed_repo_executions(rid, **kwargs):
    return aggregate(store, 'metrics:total-failed-repo-jobs:{}'.format(rid), kwargs['begin'], kwargs['end'],
                     kwargs['max'])


@app.metric('/repository-success-rate', id='repository-success-rate', title='Success rate',
            parameters=[SCM.Repository])
def get_repository_success_rate(rid, **kwargs):
    passed_ctx, passed = aggregate(store, 'metrics:total-passed-repo-jobs:{}'.format(rid), kwargs['begin'],
                                   kwargs['end'],
                                   kwargs['max'])

    total_ctx, total = aggregate(store, 'metrics:total-repo-jobs:{}'.format(rid), kwargs['begin'], kwargs['end'],
                                 kwargs['max'])

    # When there are no executions (t == 0), rate should be equal to 1??
    rate = [float(r) / float(t) if t else 0 for r, t in zip(passed, total)]
    return total_ctx, rate


@app.metric('/project-success-rate', id='project-success-rate', title='Success rate',
            parameters=[ORG.Project])
def get_project_success_rate(pjid, **kwargs):
    passed_ctx, passed = aggregate(store, 'metrics:total-passed-project-jobs:{}'.format(pjid), kwargs['begin'],
                                   kwargs['end'],
                                   kwargs['max'])

    total_ctx, total = aggregate(store, 'metrics:total-project-jobs:{}'.format(pjid), kwargs['begin'], kwargs['end'],
                                 kwargs['max'])

    # When there are no executions (t == 0), rate should be equal to 1??
    rate = [float(r) / float(t) if t else 0 for r, t in zip(passed, total)]
    return total_ctx, rate


@app.metric('/product-success-rate', id='product-success-rate', title='Success rate',
            parameters=[ORG.Product])
def get_product_success_rate(pjid, **kwargs):
    passed_ctx, passed = aggregate(store, 'metrics:total-passed-product-jobs:{}'.format(pjid), kwargs['begin'],
                                   kwargs['end'],
                                   kwargs['max'])

    total_ctx, total = aggregate(store, 'metrics:total-product-jobs:{}'.format(pjid), kwargs['begin'], kwargs['end'],
                                 kwargs['max'])

    # When there are no executions (t == 0), rate should be equal to 1??
    rate = [float(r) / float(t) if t else 0 for r, t in zip(passed, total)]
    return total_ctx, rate

@app.metric('/repo-build-time', id='repository-buildtime', parameters=[SCM.Repository], title='Build time')
def get_repo_build_time(rid, **kwargs):
    total = store.get_repo_build_time(rid, begin=kwargs['begin'], end=kwargs['end'])
    if math.isnan(total):
        return []
    return [total]


@app.metric('/project-build-time', id='project-buildtime', title='Build time', parameters=[ORG.Project])
def get_project_build_time(pjid, **kwargs):
    begin = kwargs['begin']
    if begin is None:
        begin = 0
    end = kwargs['end']
    if end is None:
        end = calendar.timegm(datetime.now().timetuple())

    return {}, [
        sum([store.get_repo_build_time(rid, begin=begin, end=end) for rid in store.get_project_repositories(pjid)])]


@app.metric('/product-build-time', id='product-buildtime', title='Build time', parameters=[ORG.Product])
def get_product_build_time(prid, **kwargs):
    begin = kwargs['begin']
    if begin is None:
        begin = 0
    end = kwargs['end']
    if end is None:
        end = calendar.timegm(datetime.now().timetuple())

    return {}, [
        sum([store.get_repo_build_time(rid, begin=begin, end=end) for rid in store.get_product_repositories(prid)])]

@app.metric('/avg-build-time', aggr='avg', id='buildtime', title='Build time')
def get_avg_build_time(**kwargs):
    average = avg(
        [store.get_repo_build_time(rid, begin=kwargs['begin'], end=kwargs['end']) for rid in store.get_repositories()])
    if math.isnan(average):
        return []
    return [average]


@app.metric('/total-build-time', id='buildtime', title='Build time')
def get_total_build_time(**kwargs):
    total = sum(
        [store.get_repo_build_time(rid, begin=kwargs['begin'], end=kwargs['end']) for rid in store.get_repositories()])
    if math.isnan(total):
        return []

    return [total]


@app.metric('/total-broken-time', id='brokentime', title='Broken time')
def get_total_broken_time(**kwargs):
    return [sum([store.get_broken_time(rid) for rid in store.get_repositories()])]


@app.metric('/repo-broken-time', id='repository-brokentime', title='Broken time', parameters=[SCM.Repository])
def get_repo_broken_time(rid, **kwargs):
    begin = kwargs['begin']
    if begin is None:
        begin = 0
    end = kwargs['end']
    if end is None:
        end = calendar.timegm(datetime.now().timetuple())

    return {'begin': begin, 'end': end}, [store.get_broken_time(rid, begin=begin, end=end)]


@app.metric('/project-broken-time', id='project-brokentime', title='Broken time', parameters=[ORG.Project])
def get_project_broken_time(pjid, **kwargs):
    begin = kwargs['begin']
    if begin is None:
        begin = 0
    end = kwargs['end']
    if end is None:
        end = calendar.timegm(datetime.now().timetuple())

    return {}, [sum([store.get_broken_time(rid, begin=begin, end=end) for rid in store.get_project_repositories(pjid)])]


@app.metric('/product-broken-time', id='product-brokentime', title='Broken time', parameters=[ORG.Product])
def get_product_broken_time(prid, **kwargs):
    begin = kwargs['begin']
    if begin is None:
        begin = 0
    end = kwargs['end']
    if end is None:
        end = calendar.timegm(datetime.now().timetuple())

    return {}, [sum([store.get_broken_time(rid, begin=begin, end=end) for rid in store.get_product_repositories(prid)])]


@app.metric('/repo-time-to-fix', aggr='avg', id='repository-timetofix', title='Time to fix',
            parameters=[SCM.Repository])
def get_repo_time_to_fix(rid, **kwargs):
    begin = kwargs['begin']
    if begin is None:
        begin = 0
    end = kwargs['end']
    if end is None:
        end = calendar.timegm(datetime.now().timetuple())

    return {}, [store.get_time_to_fix(rid, begin=begin, end=end)]


@app.metric('/time-to-fix', aggr='avg', id='timetofix', title='Time to fix')
def get_time_to_fix(**kwargs):
    begin = kwargs['begin']
    if begin is None:
        begin = 0
    end = kwargs['end']
    if end is None:
        end = calendar.timegm(datetime.now().timetuple())

    return {}, [avg([store.get_time_to_fix(rid, begin=begin, end=end) for rid in store.get_repositories()])]


@app.metric('/project-time-to-fix', aggr='avg', id='project-timetofix', title='Time to fix', parameters=[ORG.Project])
def get_project_time_to_fix(pjid, **kwargs):
    begin = kwargs['begin']
    if begin is None:
        begin = 0
    end = kwargs['end']
    if end is None:
        end = calendar.timegm(datetime.now().timetuple())

    return {}, [avg([store.get_time_to_fix(rid, begin=begin, end=end) for rid in store.get_project_repositories(pjid)])]


@app.metric('/product-time-to-fix', aggr='avg', id='product-timetofix', title='Time to fix', parameters=[ORG.Product])
def get_product_time_to_fix(prid, **kwargs):
    begin = kwargs['begin']
    if begin is None:
        begin = 0
    end = kwargs['end']
    if end is None:
        end = calendar.timegm(datetime.now().timetuple())

    return {}, [
        avg([store.get_time_to_fix(rid, begin=begin, end=end) for rid in store.get_product_repositories(prid)])]


@app.metric('/total-product-builds', id='product-builds', title='Builds', parameters=[ORG.Product])
def get_product_builds(prid, **kwargs):
    projects = store.get_product_projects(prid)
    repo_ids = flat_sum(map(lambda x: store.get_project_repositories(x), projects))
    return {}, [sum(map(lambda x: len(store.get_repo_builds(x)), repo_ids))]


@app.metric('/total-project-builds', id='project-builds', title='Builds', parameters=[ORG.Project])
def get_project_builds(pjid, **kwargs):
    repo_ids = store.get_project_repositories(pjid)
    return {}, [sum(map(lambda x: len(store.get_repo_builds(x)), repo_ids))]


@app.metric('/total-product-executions', id='product-executions', title='Executions', parameters=[ORG.Product])
def get_product_executions(prid, **kwargs):
    return aggregate(store, 'metrics:total-product-jobs:{}'.format(prid), kwargs['begin'], kwargs['end'], kwargs['max'])


@app.metric('/total-project-executions', id='project-executions', title='Executions', parameters=[ORG.Project])
def get_project_executions(prid, **kwargs):
    return aggregate(store, 'metrics:total-project-jobs:{}'.format(prid), kwargs['begin'], kwargs['end'], kwargs['max'])


@app.metric('/total-passed-product-executions', id='passed-product-executions', title='Executions',
            parameters=[ORG.Product])
def get_product_passed_executions(prid, **kwargs):
    return aggregate(store, 'metrics:total-passed-product-jobs:{}'.format(prid), kwargs['begin'], kwargs['end'],
                     kwargs['max'])


@app.metric('/total-passed-project-executions', id='passed-project-executions', title='Executions',
            parameters=[ORG.Project])
def get_project_passed_executions(prid, **kwargs):
    return aggregate(store, 'metrics:total-passed-project-jobs:{}'.format(prid), kwargs['begin'], kwargs['end'],
                     kwargs['max'])


@app.metric('/total-failed-product-executions', id='failed-product-executions', title='Failed executions',
            parameters=[ORG.Product])
def get_product_failed_executions(prid, **kwargs):
    return aggregate(store, 'metrics:total-failed-product-jobs:{}'.format(prid), kwargs['begin'], kwargs['end'],
                     kwargs['max'])


@app.metric('/total-failed-project-executions', id='failed-project-executions', title='Failed executions',
            parameters=[ORG.Project])
def get_project_failed_executions(prid, **kwargs):
    return aggregate(store, 'metrics:total-failed-project-jobs:{}'.format(prid), kwargs['begin'], kwargs['end'],
                     kwargs['max'])
