# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import absolute_import

import collections
import re
import time

import flask_login
import structlog
import taskcluster
from flask import Blueprint
from flask import current_app
from flask import g
from flask import request
from flask import url_for
from flask.ext.login import current_user
from sqlalchemy import and_
from sqlalchemy import desc
from sqlalchemy import func
from sqlalchemy import not_
from sqlalchemy import or_

from relengapi.blueprints.clobberer import rest
from relengapi.blueprints.clobberer.models import DB_DECLARATIVE_BASE
from relengapi.blueprints.clobberer.models import Build
from relengapi.blueprints.clobberer.models import ClobberTime
from relengapi.lib import angular
from relengapi.lib import api
from relengapi.lib.api import apimethod
from relengapi.lib.permissions import p

logger = structlog.get_logger()

bp = Blueprint(
    'clobberer',
    __name__,
    template_folder='templates',
    static_folder='static'
)

p.clobberer.post.clobber.doc('Submit clobber requests')

bp.root_widget_template('clobberer_root_widget.html', priority=100)

# prefix which denotes release builddirs
BUILDDIR_REL_PREFIX = 'rel-'
BUILDER_REL_PREFIX = 'release-'


@bp.route('/')
@bp.route('/<string:branch>')
@flask_login.login_required
def root(branch=None):
    return angular.template(
        'clobberer.html',
        url_for('.static', filename='clobberer.js'),
        url_for('.static', filename='clobberer.css'),
        branches=api.get_data(branches),
        selected_branch=branch
    )


def _add_clobber(session, branch, builddir, slave=None):
    """
    A common method for adding clobber times to a session. The session passed
    in is returned; but is only committed if the commit option is True.
    """
    if re.search('^' + BUILDDIR_REL_PREFIX + '.*', builddir) is None:
        try:
            who = current_user.authenticated_email
        except AttributeError:
            if current_user.anonymous:
                who = 'anonymous'
            else:
                # TokenUser doesn't show up as anonymous; but also has no
                # authenticated_email
                who = 'automation'

        clobber_time = ClobberTime.as_unique(
            session,
            branch=branch,
            builddir=builddir,
            slave=slave,
        )
        clobber_time.lastclobber = int(time.time())
        clobber_time.who = who
        session.add(clobber_time)
        return None
    logger.debug('Rejecting clobber of builddir with release prefix: {}'.format(
        builddir))
    return None


@bp.route('/clobber', methods=['POST'])
@apimethod(None, body=[rest.ClobberRequest])
@p.clobberer.post.clobber.require()
def clobber(body):
    "Request clobbers for particular branches and builddirs."
    session = g.db.session(DB_DECLARATIVE_BASE)
    for clobber in body:
        _add_clobber(
            session,
            branch=clobber.branch,
            builddir=clobber.builddir,
            slave=clobber.slave
        )
    session.commit()
    return None


@bp.route('/clobber/by-builder', methods=['POST'])
@apimethod(None, body=[rest.ClobberRequestByBuilder])
@p.clobberer.post.clobber.require()
def clobber_by_builder(body):
    """
    Request clobbers for app builddirs associated with a particular buildername.
    """
    session = g.db.session(DB_DECLARATIVE_BASE)
    for clobber in body:
        builddirs_query = session.query(Build.builddir, Build.branch).filter(
            Build.buildername == clobber.buildername
        )
        if clobber.branch is not None:
            builddirs_query = builddirs_query.filter(Build.branch == clobber.branch)

        for result in builddirs_query.distinct():
            _add_clobber(
                session,
                builddir=result[0],
                branch=result[1],
                slave=clobber.slave
            )
    session.commit()
    return None


@bp.route('/branches')
@apimethod([unicode])
def branches():
    "Return a list of all the branches clobberer knows about."
    session = g.db.session(DB_DECLARATIVE_BASE)
    branches = session.query(Build.branch).distinct()
    # Users shouldn't see any branch associated with a release builddir
    branches = branches.filter(not_(Build.builddir.startswith(BUILDDIR_REL_PREFIX)))
    branches = branches.order_by(Build.branch)
    return [branch[0] for branch in branches]


@bp.route('/lastclobber/all', methods=['GET'])
@apimethod([rest.ClobberTime])
def lastclobber_all():
    "Return a sorted list of all clobbers"
    session = g.db.session(DB_DECLARATIVE_BASE)
    return session.query(ClobberTime).order_by(ClobberTime.lastclobber)


@bp.route('/lastclobber/branch/by-builder/<string:branch>', methods=['GET'])
@apimethod({unicode: [rest.ClobberTime]}, unicode)
def lastclobber_by_builder(branch):
    "Return a dictionary of most recent ClobberTimes grouped by buildername."
    session = g.db.session(DB_DECLARATIVE_BASE)

    # Isolates the maximum lastclobber for each builddir on a branch
    max_ct_sub_query = session.query(
        func.max(ClobberTime.lastclobber).label('lastclobber'),
        ClobberTime.builddir,
        ClobberTime.branch
    ).group_by(
        ClobberTime.builddir,
        ClobberTime.branch
    ).filter(ClobberTime.branch == branch).subquery()

    # Finds the "greatest n per group" by joining with the max_ct_sub_query
    # This is necessary to get the correct "who" values
    sub_query = session.query(ClobberTime).join(max_ct_sub_query, and_(
        ClobberTime.builddir == max_ct_sub_query.c.builddir,
        ClobberTime.lastclobber == max_ct_sub_query.c.lastclobber,
        ClobberTime.branch == max_ct_sub_query.c.branch)).subquery()

    # Attaches builddirs, along with their max lastclobber to a buildername
    full_query = session.query(
        Build.buildername,
        Build.builddir,
        sub_query.c.lastclobber,
        sub_query.c.who
    ).outerjoin(
        sub_query,
        Build.builddir == sub_query.c.builddir,
    ).filter(
        Build.branch == branch,
        not_(Build.buildername.startswith(BUILDER_REL_PREFIX))
    ).distinct().order_by(Build.buildername)

    summary = collections.defaultdict(list)
    for result in full_query:
        buildername, builddir, lastclobber, who = result
        summary[buildername].append(
            rest.ClobberTime(
                branch=branch,
                builddir=builddir,
                lastclobber=lastclobber,
                who=who
            )
        )
    return summary


@bp.route('/lastclobber', methods=['GET'])
def lastclobber():
    "Get the max/last clobber time for a particular builddir and branch."

    session = g.db.session(DB_DECLARATIVE_BASE)
    now = int(time.time())
    branch = request.args.get('branch')
    slave = request.args.get('slave')
    builddir = request.args.get('builddir')
    buildername = request.args.get('buildername')
    # TODO: Move the builds update to a separate endpoint (requires client changes)
    build = Build.as_unique(
        session,
        branch=branch,
        builddir=builddir,
        buildername=buildername,
    )
    # Always force the time to update
    build.last_build_time = now
    session.add(build)
    session.commit()

    max_ct = session.query(ClobberTime).filter(
        ClobberTime.builddir == builddir,
        ClobberTime.branch == branch,
        # a NULL slave value signifies all slaves
        or_(ClobberTime.slave == slave, ClobberTime.slave == None)  # noqa
    ).order_by(desc(ClobberTime.lastclobber)).first()

    if max_ct:
        # The client parses this result by colon as:
        # builddir, lastclobber, who = urlib2.open.split(':')
        # as such it's important for this to be plain text and have
        # no extra colons within the field values themselves
        return "{}:{}:{}\n".format(max_ct.builddir, max_ct.lastclobber, max_ct.who)
    return ""


@bp.route('/forceclobber', methods=['GET'])
def forceclobber():
    """
    Coerce the client to clobber by always returning a future clobber time.
    This works because the client decides to clobber based on a timestamp
    comparison.
    """
    future_time = int(time.time()) + 3600
    builddir = request.args.get('builddir')
    return "{}:{}:forceclobber".format(builddir, future_time)


def tc_branches():
    decision_namespace = 'gecko.v2.%s.latest.firefox.decision'

    index = taskcluster.Index()
    queue = taskcluster.Queue()

    result = index.listNamespaces('gecko.v2', dict(limit=1000))

    branches = {
        i['name']: dict(name=i['name'], workerTypes=dict())
        for i in result.get('namespaces', [])
    }

    for branchName, branch in branches.items():

        # decision task might not exist
        try:
            decision_task = index.findTask(decision_namespace % branchName)
            decision_graph = queue.getLatestArtifact(
                decision_task['taskId'], 'public/graph.json')
        except taskcluster.exceptions.TaskclusterRestFailure:
            continue

        for task in decision_graph.get('tasks', []):
            task = task['task']
            task_cache = task.get('payload', dict()).get('cache', dict())

            provisionerId = task.get('provisionerId')
            if provisionerId:
                branch['provisionerId'] = provisionerId

            workerType = task.get('workerType')
            if workerType:
                branch['workerTypes'].setdefault(
                    workerType, dict(name=workerType, caches=[]))

                if len(task_cache) > 0:
                    branch['workerTypes'][workerType]['caches'] = list(set(
                        branch['workerTypes'][workerType]['caches'] +
                        task_cache.keys()
                    ))

    caches_to_skip = current_app.config.get('TASKCLUSTER_CACHES_TO_SKIP', [])

    return [
        rest.TCBranch(
            name=branchName,
            provisionerId=branch.get('provisionerId'),
            workerTypes={
                workerType: rest.TCWorkerType(
                        name=workerType,
                        caches=[
                            cache
                            for cache in branch['workerTypes'][workerType]['caches']
                            if cache not in caches_to_skip
                        ],
                    )
                for workerType in branch['workerTypes']
            })
        for branchName, branch in branches.items()]


@bp.route('/tc/branches', methods=['GET'])
@apimethod([rest.TCBranch])
def tc_branches_cached():
    """List of all the gecko branches with their worker types
    """

    def cache_key():
        return time.time() // current_app.config.get(
            'TASKCLUSTER_CACHE_DURATION', 60 * 5)

    def cache(fun):
        def wrap(*args, **kwargs):
            key = cache_key()
            if getattr(fun, '__cache_key', None) != key:
                fun.__cache_value = fun(*args, **kwargs)
                fun.__cache_key = key
            return getattr(fun, '__cache_value', None)
        return wrap

    return cache(tc_branches)()


@bp.route('/tc/purgecache', methods=['POST'])
@apimethod(None, body=[rest.TCPurgeCacheRequest])
@p.clobberer.post.clobber.require()
def tc_purgecache(body):
    """Purge cache on taskcluster
    """

    credentials = []

    client_id = current_app.config.get('TASKCLUSTER_CLIENTID')
    access_token = current_app.config.get('TASKCLUSTER_ACCESSTOKEN')

    if client_id and access_token:
        credentials = [dict(
            credentials=dict(
                clientId=client_id,
                accessToken=access_token,
            ))]

    purge_cache = taskcluster.PurgeCache(*credentials)

    for item in body:
        purge_cache.purgeCache(item.provisionerId,
                               item.workerType,
                               dict(cacheName=item.cacheName))

    return None


_ROR = "https://github.com/mozilla/build-relengapi-clobberer"
_ISSUE_URL = "%s/issues" % _ROR

# See <relengapi>/docs/development/@relengapi/blueprints/#project-metadata
metadata = {
    "repository_of_record": _ROR,
    "bug_report_url": _ISSUE_URL,
}
