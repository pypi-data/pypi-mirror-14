# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import absolute_import

from nose.tools import eq_

from relengapi.lib import introspection


def test_get_distributions():
    distributions = introspection.get_distributions()
    eq_(distributions['relengapi'].project_name, 'relengapi')
