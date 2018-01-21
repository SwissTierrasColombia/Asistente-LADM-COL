import qgis
import nose2
import psycopg2
import os

from sys import platform
from qgis.testing import unittest, start_app

start_app() # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.gui.point_spa_uni_cadaster_wizard import PointsSpatialUnitCadasterWizard
from asistente_ladm_col.tests.utils import get_dbconn, get_test_path
from asistente_ladm_col.utils.qgis_utils import QGISUtils

class TestExport(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.qgis_utils = QGISUtils()
        self.db_connection = get_dbconn()
        result = self.db_connection.test_connection()
        print('test_connection', result)
        if not result[1]:
            print('The test connection is not working')
            return

        cur = self.db_connection.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""SELECT schema_name FROM information_schema.schemata WHERE schema_name = 'test_ladm_col';""")
        result = cur.fetchone()
        if result is not None and len(result) > 0:
            print('The schema test_ladm_col already exists')
            return

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
        if len(output) > 0:
            print('Warning:', output)

    def drop_schema(self):
        print('Clean ladm_col database...')
        cur = self.db_connection.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = cur.execute("""DROP SCHEMA test_ladm_col CASCADE;""")
        self.db_connection.conn.commit()
        cur.close()
        self.db_connection.conn.close()
        if query is not None:
            print('The drop schema is not working')

    def test_show_wiz_point_sp_un_cad(self):
        csv_path = get_test_path('csv/puntos_fixed.csv')
        txt_delimiter = ';'
        cbo_longitude = 'x'
        cbo_latitude = 'y'
        res = self.qgis_utils.copy_csv_to_db(csv_path,
                                    txt_delimiter,
                                    cbo_longitude,
                                    cbo_latitude,
                                    self.db_connection)

        self.assertEqual(res, True) # Isn't ok yet

        # cur = self.db_connection.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        # print('Restoring ladm_col database')
        # query = cur.execute("""SELECT 1""")
        # query.next()
        # print('query', query.value(0))

    def tearDownClass():
        print('In this section the DB will be clear?')
        # self.drop_schema()


if __name__ == '__main__':
    nose2.main()
