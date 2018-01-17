import qgis
import nose2

from qgis.testing import unittest, start_app

start_app() # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.gui.point_spa_uni_cadaster_wizard import PointsSpatialUnitCadasterWizard
from asistente_ladm_col.tests.utils import get_dbconn, get_iface
from asistente_ladm_col.utils.qgis_utils import QGISUtils

class TestExport(unittest.TestCase):

    def setUpClass():
        print('in this section the DB will be filled')

    def test_show_wiz_point_sp_un_cad(self):
        self.iface = get_iface()
        self.qgis_utils = QGISUtils()
        self.db_connection = get_dbconn()
        wiz = PointsSpatialUnitCadasterWizard(self.iface, self.db_connection, self.qgis_utils)
        a = wiz.copy_csv_points_to_db()
        self.assertEqual(a, None) # Isn't ok yet

    def tearDownClass():
        print('in this section the DB will be clear')

if __name__ == '__main__':
    nose2.main()
