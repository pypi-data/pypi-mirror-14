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

from sdh.metrics.qualitative import app, st as store
from sdh.metrics.store.metrics import aggregate, flat_sum
from sdh.metrics.server import SCM, ORG, CI, APIError
from itertools import dropwhile


def __calc_quality(s, rm):
    if not s:
        return 1.0 - rm
    else:
        return (s + rm) / 2.0


def calculate_member_quality(uid, **kwargs):
    def __process_row():
        return [__calc_quality(s, rm) for s, rm in zip(sr, rm_activity)]

    try:
        repo_ctx, repositories = app.request_view('member-repositories', uid=uid, **kwargs)
        repositories = map(lambda x: x['id'], repositories)
        repo_success_rate = map(lambda x: app.request_metric('sum-repository-success-rate', rid=x, **kwargs),
                                repositories)

        context = repo_success_rate[0][0]
        repo_success_rate = map(lambda x: x[1], repo_success_rate)
        repo_member_activity = map(
            lambda x: app.request_metric('sum-member-activity-in-repository', uid=uid, rid=x, **kwargs)[1],
            repositories)

        res = [__process_row() for sr, rm_activity in zip(repo_success_rate, repo_member_activity)]
        res = [sum(t) / len(t) for t in zip(*res)]
        return context, res
    except (EnvironmentError, AttributeError) as e:
        raise APIError(e.message)


@app.metric('/member-quality', id='member-quality', title='Quality', parameters=[ORG.Person])
def get_member_quality(uid, **kwargs):
    return calculate_member_quality(uid, **kwargs)


@app.metric('/repository-quality', id='repository-quality', title='Quality', parameters=[SCM.Repository])
def get_repository_quality(rid, **kwargs):
    try:
        repo_ctx, devs = app.request_view('repository-developers', rid=rid, **kwargs)
        devs = map(lambda x: x['id'], devs)
        devs_quality = map(lambda x: calculate_member_quality(x, **kwargs), devs)

        context = repo_ctx
        if devs_quality:
            context = devs_quality[0][0]
        res = [sum(_)/len(_) for _ in zip(*map(lambda x: x[1], devs_quality))]
        return context, res
    except (EnvironmentError, AttributeError) as e:
        raise APIError(e.message)


@app.metric('/project-quality', id='project-quality', title='Quality', parameters=[ORG.Project])
def get_project_quality(pjid, **kwargs):
    try:
        project_ctx, devs = app.request_view('project-developers', pjid=pjid, **kwargs)
        devs = map(lambda x: x['id'], devs)
        devs_quality = map(lambda x: calculate_member_quality(x, **kwargs), devs)

        context = project_ctx
        if devs_quality:
            context = devs_quality[0][0]
            res = [sum(_) / len(_) for _ in zip(*map(lambda x: x[1], devs_quality))]
        else:
            res = [0]
        return context, res
    except (EnvironmentError, AttributeError) as e:
        raise APIError(e.message)


@app.metric('/product-quality', id='product-quality', title='Quality', parameters=[ORG.Product])
def get_product_quality(prid, **kwargs):
    try:
        product_ctx, devs = app.request_view('product-developers', prid=prid, **kwargs)
        devs = map(lambda x: x['id'], devs)
        devs_quality = map(lambda x: calculate_member_quality(x, **kwargs), devs)

        context = product_ctx
        if devs_quality:
            context = devs_quality[0][0]
            res = [sum(_) / len(_) for _ in zip(*map(lambda x: x[1], devs_quality))]
        else:
            res = [0]
        return context, res
    except (EnvironmentError, AttributeError) as e:
        raise APIError(e.message)


def cost(nd, nc):
    commits_ratio = 1.0 if nc >= 10 else nc / 10.0
    return commits_ratio * 200 * nd     # 25 * 8 = 200


@app.metric('/repository-cost', id='repository-cost', title='Cost', parameters=[SCM.Repository])
def get_repository_cost(rid, **kwargs):
    try:
        kwargs['max'] = 0
        context, devs = app.request_metric('sum-repository-developers', rid=rid, **kwargs)
        kwargs['max'] = context['size']
        kwargs['begin'] = context['begin']
        kwargs['end'] = context['end']
        context, commits = app.request_metric('sum-repository-commits', rid=rid, **kwargs)
        pairs = list(dropwhile(lambda x: x[1] == 0, zip(devs, commits)))
        pairs = list(dropwhile(lambda x: x[1] == 0, reversed(pairs)))
        res = [cost(nd, nc) for nd, nc in pairs]
        return context, [sum(res)]
    except (EnvironmentError, AttributeError) as e:
        raise APIError(e.message)


@app.metric('/project-cost', id='project-cost', title='Cost', parameters=[ORG.Project])
def get_project_cost(pjid, **kwargs):
    try:
        kwargs['max'] = 0
        context, devs = app.request_metric('sum-project-developers', pjid=pjid, **kwargs)
        kwargs['max'] = context['size']
        kwargs['begin'] = context['begin']
        kwargs['end'] = context['end']
        context, commits = app.request_metric('sum-project-commits', pjid=pjid, **kwargs)
        pairs = list(dropwhile(lambda x: x[1] == 0, zip(devs, commits)))
        pairs = list(dropwhile(lambda x: x[1] == 0, reversed(pairs)))
        res = [cost(nd, nc) for nd, nc in pairs]
        return context, [sum(res)]
    except (EnvironmentError, AttributeError) as e:
        raise APIError(e.message)


@app.metric('/product-cost', id='product-cost', title='Cost', parameters=[ORG.Product])
def get_product_cost(prid, **kwargs):
    try:
        kwargs['max'] = 0
        context, devs = app.request_metric('sum-product-developers', prid=prid, **kwargs)
        kwargs['max'] = context['size']
        kwargs['begin'] = context['begin']
        kwargs['end'] = context['end']
        context, commits = app.request_metric('sum-product-commits', prid=prid, **kwargs)
        pairs = list(dropwhile(lambda x: x[1] == 0, zip(devs, commits)))
        pairs = list(dropwhile(lambda x: x[1] == 0, reversed(pairs)))
        res = [cost(nd, nc) for nd, nc in pairs]
        return context, [sum(res)]
    except (EnvironmentError, AttributeError) as e:
        raise APIError(e.message)


@app.metric('/product-ttm', id='product-timetomarket', title='Time-to-market', parameters=[ORG.Product])
def get_product_ttm(prid, **kwargs):
    try:
        context, passed = app.request_metric('sum-passed-product-executions', prid=prid, **kwargs)
        _, activity = app.request_metric('sum-product-activity', prid=prid, **kwargs)
        kwargs['max'] = context['size']
        kwargs['begin'] = context['begin']
        kwargs['end'] = context['end']
        _, total = app.request_metric('sum-passed-executions', **kwargs)
        res = [(a + (p / float(t))) / 2.0 if t else 0 for p, a, t in zip(passed, activity, total)]
        return context, res
    except (EnvironmentError, AttributeError) as e:
        raise APIError(e.message)


@app.metric('/product-health', id='product-health', title='Health', parameters=[ORG.Product])
def get_product_health(prid, **kwargs):
    try:
        context, buildtime = app.request_metric('sum-product-buildtime', prid=prid, **kwargs)
        _, brokentime = app.request_metric('sum-product-brokentime', prid=prid, **kwargs)
        _, timetofix = app.request_metric('avg-product-timetofix', prid=prid, **kwargs)

        health = 0
        if buildtime and brokentime and timetofix:
            base_health = (timetofix[0] + brokentime[0]) / buildtime[0] if buildtime[0] else 10000.0
            base_health = min(10000.0, base_health)
            base_health = max(0.0, base_health / 10000.0)
            health = 1.0 - base_health

        return context, [health]
    except (EnvironmentError, AttributeError) as e:
        raise APIError(e.message)
