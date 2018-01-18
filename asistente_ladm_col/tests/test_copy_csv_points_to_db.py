import qgis
import nose2
import psycopg2
import os

from sys import platform
from qgis.testing import unittest, start_app

start_app() # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.gui.point_spa_uni_cadaster_wizard import PointsSpatialUnitCadasterWizard
from asistente_ladm_col.tests.utils import get_dbconn, get_iface, get_test_path
from asistente_ladm_col.utils.qgis_utils import QGISUtils

class TestExport(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.iface = get_iface()
        self.qgis_utils = QGISUtils()
        self.db_connection = get_dbconn()
        print('test_connection', self.db_connection.test_connection())
        print('Restoring ladm_col database...')
        script_dir = 'restore_db.sh'
        if platform == "linux" or platform == "linux2" or platform == "darwin":
            script_dir = get_test_path('restore_db.sh')
        elif platform == "win32":
            script_dir = get_test_path('restore_db.bat')
        else:
            print('Please add the test script')

        process = os.popen(script_dir)
        output = process.readlines()
        process.close()
        print('Done restoring ladm_col database.')
        print(output)

    def test_show_wiz_point_sp_un_cad(self):
        wiz = PointsSpatialUnitCadasterWizard(self.iface, self.db_connection, self.qgis_utils)
        a = wiz.copy_csv_points_to_db()
        self.assertEqual(a, None) # Isn't ok yet

        # cur = self.db_connection.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        # print('Restoring ladm_col database')
        # query = cur.execute("""SELECT 1""")
        # query.next()
        # print('query', query.value(0))

        #probarlo por fuera!!!

        # target_point_layer = self.qgis_utils.get_layer(self._db, BOUNDARY_POINT_TABLE, load=True)
        # if target_point_layer is None:
        #     self.iface.messageBar().pushMessage("Asistente LADM_COL",
        #         QCoreApplication.translate("PointsSpatialUnitCadasterWizard",
        #                                    "Boundary point layer couldn't be found in the DB..."),
        #         QgsMessageBar.WARNING)
        #     return
        #
        # self.iface.copySelectionToClipboard(csv_layer)
        # target_point_layer.startEditing()
        # self.iface.pasteFromClipboard(target_point_layer)
        # target_point_layer.commitChanges()
        # QgsProject.instance().addMapLayer(target_point_layer)
        # self.iface.zoomFull()

    def tearDownClass():
        print('in this section the DB will be clear')

if __name__ == '__main__':
    nose2.main()
