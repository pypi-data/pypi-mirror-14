# copyright 2015 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.


from cubicweb.devtools import testlib
from cubes.cwcelerytest import tasks
from cubicweb_celery import app, init_repo


class DefaultTC(testlib.CubicWebTC):
    def setUp(self):
        super(DefaultTC, self).setUp()
        app.cwrepo = init_repo(app.cwconfig)

    def test_cwtask(self):
        eid = tasks.newgroup(u'test')
        with self.admin_access.repo_cnx() as cnx:
            self.assertEqual(cnx.entity_from_eid(eid).name, u'test')

    def test_default_config(self):
        self.assertTrue(app.conf.CELERY_ENABLE_UTC)
        self.assertEqual('Indian/Maldives',
                         app.conf.CELERY_TIMEZONE)


if __name__ == '__main__':
    from logilab.common.testlib import unittest_main
    unittest_main()
