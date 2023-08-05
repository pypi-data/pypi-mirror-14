# copyright 2012 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
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

"""cubicweb-postgis tests
"""

from cubicweb.devtools import testlib
from cubicweb.devtools import (startpgcluster, stoppgcluster,
                               PostgresApptestConfiguration)

def setUpModule():
    startpgcluster(__file__)

def tearDownModule():
    stoppgcluster(__file__)


class PostgisTC(testlib.CubicWebTC):
    configcls = PostgresApptestConfiguration

    def test_geometry_srid(self):
        with self.admin_access.repo_cnx() as cnx:
            cnx.create_entity('City', name=u'Paris', center_4326=(u'POINT(2.34 48.4)', 4326))
            cnx.commit()
            self.assertEqual(cnx.execute('Any ST_SRID(C) WHERE X center_4326 C')[0][0], 4326)
            # wrong srid
            with self.assertRaises(Exception) as ctx:
                cnx.create_entity('City', name=u'Nantes', center_4326=(u'POINT(1.5 47.25)', -1))
            self.assertEqual(ctx.exception.__class__.__name__, 'DataError')

    def test_geometry_nosrid(self):
        with self.admin_access.repo_cnx() as cnx:
            cnx.create_entity('City', name=u'Paris', center_nosrid=(u'POINT(2.34 48.4)', 4326))
            cnx.commit()
            self.assertEqual(cnx.execute('Any ST_SRID(C) WHERE X center_nosrid C')[0][0], 4326)
            cnx.create_entity('City', name=u'Nantes', center_nosrid=(u'POINT(1.5 47.25)', -1))
            cnx.commit()


class PostgisSQLiteFakeTC(testlib.CubicWebTC):

    def test_schema(self):
        with self.admin_access.repo_cnx() as cnx:
            self.assertTrue(cnx.find('CWEType', name=u'Geometry'))
            city_schema = cnx.system_sql("select sql from sqlite_master where type = 'table' and name = 'cw_City'").fetchall()[0][0]
            self.assertIn('cw_center_4326 text', city_schema)


if __name__ == '__main__':
    import unittest
    unittest.main()
