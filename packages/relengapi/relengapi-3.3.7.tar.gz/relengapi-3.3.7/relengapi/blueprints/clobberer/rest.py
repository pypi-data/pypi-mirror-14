# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import absolute_import

import wsme.types


class ClobberRequest(wsme.types.Base):
    "Represents a clobber request for a branch and build directory."

    #: The branch for this clobber request.
    branch = wsme.types.wsattr(unicode, mandatory=False, default=None)
    #: The build directory to be clobbered.
    builddir = wsme.types.wsattr(unicode, mandatory=True, default=None)
    #: A specific slave to clobber (defaults to all slaves).
    slave = wsme.types.wsattr(unicode, mandatory=False, default=None)


class ClobberRequestByBuilder(wsme.types.Base):
    "Represents a clobber request for a branch and buildername."

    #: The branch for this clobber request (defaults to all branches).
    branch = wsme.types.wsattr(unicode, mandatory=False, default=None)
    #: A buildername whose associated builddirs will be clobbered.
    buildername = wsme.types.wsattr(unicode, mandatory=True, default=None)
    #: A specific slave to clobber (defaults to all slaves).
    slave = wsme.types.wsattr(unicode, mandatory=False, default=None)


class ClobberTime(wsme.types.Base):
    "Represents the most recent data pertaining to a particular clobber."

    branch = unicode  #: The branch associated with this clobber.
    builddir = unicode  #: The clobbered directory.
    slave = unicode  #: A particular slave (null means all slaves).
    lastclobber = int  #: Timestamp associated with the last clobber request.
    who = unicode  #: User who initiated the last clobber.


class TCWorkerType(wsme.types.Base):
    """Represents worker type of taskcluster
    """

    name = wsme.types.wsattr(unicode, mandatory=True)
    caches = wsme.types.wsattr([str], mandatory=False, default=[])


class TCBranch(wsme.types.Base):
    """Represents branches of taskcluster
    """

    name = wsme.types.wsattr(unicode, mandatory=True)
    provisionerId = wsme.types.wsattr(unicode, mandatory=False, default=None)
    workerTypes = wsme.types.wsattr(
        {str: TCWorkerType}, mandatory=False, default=dict())


class TCPurgeCacheRequest(wsme.types.Base):
    """A clobber request for purging cache on taskcluster.
         http://docs.taskcluster.net/services/purge-cache
    """

    provisionerId = wsme.types.wsattr(unicode, mandatory=False, default=None)
    workerType = wsme.types.wsattr(unicode, mandatory=False, default=None)
    cacheName = wsme.types.wsattr(unicode, mandatory=False, default=None)
