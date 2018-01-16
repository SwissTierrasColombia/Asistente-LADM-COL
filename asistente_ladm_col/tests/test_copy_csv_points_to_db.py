import qgis
import nose2

from qgis.testing import unittest, start_app
from asistente_ladm_col.gui.point_spa_uni_cadaster_wizard import PointsSpatialUnitCadasterWizard

start_app()

from asistente_ladm_col.tests.utils import dbconn

class TestExport(unittest.TestCase):

    def test_show_wiz_point_sp_un_cad(self):
        print('hello')
        print(dbconn())
        #wiz = PointsSpatialUnitCadasterWizard(self.iface, self.get_db_connection(), self.qgis_utils)
        #wiz.copy_csv_points_to_db()
        self.assertEqual(1, 1)

if __name__ == '__main__':
    nose2.main()
