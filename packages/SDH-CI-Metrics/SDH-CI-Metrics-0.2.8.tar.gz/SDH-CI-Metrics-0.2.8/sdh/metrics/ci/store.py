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

from sdh.metrics.store.fragment import FragmentStore
from sdh.metrics.store.metrics import flat_sum
import calendar
from datetime import datetime
import uuid


class CIStore(FragmentStore):
    def __init__(self, **kwargs):
        super(CIStore, self).__init__(**kwargs)

    def get_repositories(self):
        repo_keys = self.db.keys('frag:repos:-*-:')
        return filter(lambda x: x is not None, [self.db.hget(rk, 'id') for rk in repo_keys])

    def get_products(self):
        repo_keys = self.db.keys('frag:products:-*-:')
        return filter(lambda x: x is not None, [self.db.hget(rk, 'name') for rk in repo_keys])

    def get_builds(self):
        return self.db.smembers('frag:builds')

    def get_repo_builds(self, rid, children=True):
        r_uri = self.db.get('frag:repos:{}:'.format(rid))
        repo_name = self.db.hget('frag:repos:-{}-:'.format(r_uri), 'name')
        try:
            jobs = self.db.smembers('frag:repos:-{}-:jobs'.format(repo_name))
            builds = set([])
            for j_uri in jobs:
                builds.add(self.db.get('frag:jobs:-{}-:'.format(j_uri)))
            if children:
                builds.update(set.union(*[self.db.smembers('frag:builds:-{}-:sub'.format(b)) for b in builds]))
            return builds
        except TypeError:
            return []

    def get_jobs(self, begin=0, end=None, rid=None, bid=None, withstamps=False, limit=None, start=None, state=None):
        if end is None:
            end = calendar.timegm(datetime.utcnow().timetuple())
        jobs = self.db.zrangebyscore('frag:sorted-jobs', begin, end, withscores=withstamps,
                                     num=limit, start=start)
        if len(jobs):
            temp_key = str(uuid.uuid4())
            if rid is not None:
                self.db.sadd(temp_key, *jobs)
                repo_builds = self.get_repo_builds(rid)
                filtered_jobs = set([])
                for build in repo_builds:
                    filtered_jobs.update(self.db.sinter(temp_key, 'frag:builds:-{}-:jobs'.format(build)))
                jobs = filtered_jobs
                self.db.delete(temp_key)
            elif bid is not None:
                if withstamps:
                    self.db.zadd(temp_key, **dict(jobs))
                    ztemp_key = str(uuid.uuid4())
                    self.db.zinterstore(ztemp_key, keys=[temp_key, 'frag:builds:-{}-:jobs'.format(bid)],
                                        aggregate='MAX')
                    filtered_jobs = self.db.zrange(ztemp_key, 0, -1)
                    self.db.delete(ztemp_key)
                else:
                    self.db.sadd(temp_key, *jobs)
                    filtered_jobs = self.db.sinter(temp_key, 'frag:builds:-{}-:jobs'.format(bid))
                jobs = filtered_jobs
                self.db.delete(temp_key)

        if state is not None:
            results = [(j, self.db.get('frag:jobs:-{}-:result'.format(j))) for j in jobs]
            jobs = [j for (j, r) in results if state in self.db.get('frag:results:-{}-:'.format(r))]

        return jobs

    def get_last_passed_execution(self, bid, begin='-inf', end='+inf'):
        if begin is None:
            begin = '-inf'
        if end is None:
            end = '+inf'
        jobs = self.db.smembers('frag:builds:-{}-:jobs'.format(bid))
        try:
            results = [(j, self.db.get('frag:jobs:-{}-:result'.format(j))) for j in jobs]
            jobs = [j for (j, r) in results if 'pass' in self.db.get('frag:results:-{}-:'.format(r))]
        except TypeError:
            return

        if jobs:
            temp_key = str(uuid.uuid4())
            ztemp_key = str(uuid.uuid4())
            stemp_key = str(uuid.uuid4())
            sorted_key = 'frag:sorted-jobs'
            if begin != '-inf' or end != '+inf':
                filtered_jobs = self.db.zrangebyscore(sorted_key, begin, end, withscores=True)
                if filtered_jobs:
                    self.db.zadd(stemp_key, **dict(filtered_jobs))
                sorted_key = stemp_key
            self.db.sadd(temp_key, *jobs)
            self.db.zinterstore(ztemp_key, keys=[temp_key, sorted_key], aggregate='MAX')
            self.db.delete(temp_key)
            self.db.delete(stemp_key)
            result = self.db.zrevrangebyscore(ztemp_key, '+inf', '-inf', start=0, num=1)
            self.db.delete(ztemp_key)

            try:
                return result.pop()
            except IndexError:
                return

    def get_job_build_time(self, e_uri):
        finished = self.db.get('frag:jobs:-{}-:finished'.format(e_uri))
        created = self.db.get('frag:jobs:-{}-:created'.format(e_uri))
        try:
            return int(finished) - int(created)
        except TypeError:
            return float('NaN')

    def get_repo_build_time(self, rid, begin='-inf', end='+inf'):
        repo_builds = self.get_repo_builds(rid, children=False)
        build_time = 0
        for b_uri in repo_builds:
            last_exec = self.get_last_passed_execution(b_uri, begin, end)
            if last_exec is not None:
                build_time += self.get_job_build_time(last_exec)
        return build_time

    def get_broken_time(self, rid, begin=0, end=None):
        if end is None:
            end = calendar.timegm(datetime.utcnow().timetuple())
        builds = self.get_repo_builds(rid, children=False)
        repo_broken_time = 0
        for b in builds:
            jobs = self.get_jobs(begin, end, bid=b, withstamps=True)
            last_verdict = 'passed'
            build_broken_since = 0
            interval_broken_time = 0
            build_broken_time = 0
            for job in jobs:
                result = self.db.get('frag:jobs:-{}-:result'.format(job))
                verdict = self.db.get('frag:results:-{}-:'.format(result))
                if verdict is not None:
                    if last_verdict == 'passed' and last_verdict not in verdict:
                        build_broken_since = int(self.db.get('frag:jobs:-{}-:finished'.format(job)))
                    elif last_verdict == 'failed' and last_verdict in verdict:
                        next_broken_timestamp = int(self.db.get('frag:jobs:-{}-:finished'.format(job)))
                        interval_broken_time = next_broken_timestamp - build_broken_since
                    elif last_verdict == 'failed' and last_verdict not in verdict:
                        next_pass_timestamp = int(self.db.get('frag:jobs:-{}-:finished'.format(job)))
                        build_broken_time += (next_pass_timestamp - build_broken_since)
                        interval_broken_time = 0
                    last_verdict = verdict.split('#')[1]
            if last_verdict == 'failed':
                build_broken_time += interval_broken_time
            repo_broken_time += build_broken_time
        return repo_broken_time

    def get_time_to_fix(self, rid, begin=0, end=None):
        if end is None:
            end = calendar.timegm(datetime.utcnow().timetuple())
        builds = self.get_repo_builds(rid, children=False)
        repo_time_to_fix = 0
        intervals = 0
        for b in builds:
            jobs = self.get_jobs(begin, end, bid=b, withstamps=True)
            last_verdict = 'passed'
            build_broken_since = 0
            for job in jobs:
                result = self.db.get('frag:jobs:-{}-:result'.format(job))
                verdict = self.db.get('frag:results:-{}-:'.format(result))
                if verdict is not None:
                    if last_verdict == 'passed' and last_verdict not in verdict:
                        build_broken_since = int(self.db.get('frag:jobs:-{}-:finished'.format(job)))
                    elif last_verdict == 'failed' and last_verdict not in verdict:
                        intervals += 1
                        next_pass_timestamp = int(self.db.get('frag:jobs:-{}-:finished'.format(job)))
                        repo_time_to_fix += (next_pass_timestamp - build_broken_since)
                    last_verdict = verdict.split('#')[1]
        if intervals:
            repo_time_to_fix /= float(intervals)
        return repo_time_to_fix

    def get_product_projects(self, prid):
        product_uri = self.db.get('frag:products:{}:'.format(prid))
        project_uris = self.db.smembers('frag:products:-{}-:projects'.format(product_uri))
        return map(lambda x: self.db.hget('frag:projects:-{}-:'.format(x), 'name'), project_uris)

    def get_project_repositories(self, prid):
        project_uri = self.db.get('frag:projects:{}:'.format(prid))
        repo_names = self.db.smembers('frag:projects:-{}-:repos'.format(project_uri))
        repo_uris = map(lambda x: self.db.get('frag:reponames:{}:'.format(x)), repo_names)
        return map(lambda x: self.db.hget('frag:repos:-{}-:'.format(x), 'id'), repo_uris)

    def get_product_repositories(self, prid):
        return list(set(flat_sum(map(lambda x: self.get_project_repositories(x), self.get_product_projects(prid)))))
