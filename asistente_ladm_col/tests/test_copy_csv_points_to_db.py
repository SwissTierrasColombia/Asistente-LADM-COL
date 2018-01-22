import qgis
import nose2
import psycopg2
import os
import datetime

from sys import platform
from qgis.testing import unittest, start_app

start_app() # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.gui.point_spa_uni_cadaster_wizard import PointsSpatialUnitCadasterWizard
from asistente_ladm_col.tests.utils import get_dbconn, get_test_path, restore_schema
from asistente_ladm_col.utils.qgis_utils import QGISUtils

class TestCopy(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.qgis_utils = QGISUtils()
        self.db_connection = get_dbconn()
        result = self.db_connection.test_connection()
        print('test_connection', result)
        if not result[1]:
            print('The test connection is not working')
            return
        restore_schema(self.db_connection)

    def test_copy_csv_to_db(self):
        self.clean_table()
        self.upload_points_from_csv()
        self.validate_points_in_db()
        self.clean_table()

    def test_copy_csv_overlaping_to_db(self):
        self.clean_table()
        self.upload_points_from_csv_overlaping()
        self.clean_table()

    def upload_points_from_csv(self):
        csv_path = get_test_path('csv/puntos_fixed.csv')
        txt_delimiter = ';'
        cbo_longitude = 'x'
        cbo_latitude = 'y'
        res = self.qgis_utils.copy_csv_to_db(csv_path,
                                    txt_delimiter,
                                    cbo_longitude,
                                    cbo_latitude,
                                    self.db_connection)

        self.assertEqual(res, True)

    def upload_points_from_csv_overlaping(self):
        csv_path = get_test_path('csv/puntos_overlaping.csv')
        txt_delimiter = ';'
        cbo_longitude = 'x'
        cbo_latitude = 'y'
        res = self.qgis_utils.copy_csv_to_db(csv_path,
                                    txt_delimiter,
                                    cbo_longitude,
                                    cbo_latitude,
                                    self.db_connection)

        self.assertEqual(res, True)

    def validate_points_in_db(self):
        cur = self.db_connection.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        print('Validating points')
        query = cur.execute("""SELECT * FROM test_ladm_col.puntolindero;""")
        results = cur.fetchall()
        colnames = {desc[0]: cur.description.index(desc) for desc in cur.description}
        # for result in results:
        #     print(result[colnames['t_id']])
        self.assertEqual(len(results), 51)

        row = results[50]
        #self.assertEqual(row[colnames['t_id']], 52)
        self.assertEqual(row[colnames['acuerdo']], 'Acuerdo')
        self.assertEqual(row[colnames['definicion_punto']], 'No_Bien_Definido')
        self.assertEqual(row[colnames['descripcion_punto']], 'Otros')
        self.assertEqual(row[colnames['exactitud_vertical']], 1)
        self.assertEqual(row[colnames['exactitud_horizontal']], 1)
        self.assertEqual(row[colnames['confiabilidad']], None)
        self.assertEqual(row[colnames['nombre_punto']], None)
        self.assertEqual(row[colnames['posicion_interpolacion']], 'Centro_Arco')
        self.assertEqual(row[colnames['monumentacion']], None)
        self.assertEqual(row[colnames['puntotipo']], 'Catastro')
        self.assertEqual(row[colnames['p_espacio_de_nombres']], '-1')
        self.assertEqual(row[colnames['p_local_id']], '-1')
        self.assertEqual(row[colnames['ue_la_unidadespacial']], None)
        self.assertEqual(row[colnames['ue_terreno']], None)
        self.assertEqual(row[colnames['ue_la_espaciojuridicoredservicios']], None)
        self.assertEqual(row[colnames['ue_la_espaciojuridicounidadedificacion']], None)
        self.assertEqual(row[colnames['ue_servidumbrepaso']], None)
        self.assertEqual(row[colnames['ue_unidadconstruccion']], None)
        self.assertEqual(row[colnames['ue_construccion']], None)
        self.assertEqual(row[colnames['comienzo_vida_util_version']], datetime.datetime(2017, 4, 19, 14, 16, 41, 221713))
        self.assertEqual(row[colnames['fin_vida_util_version']], None)
        self.assertEqual(row[colnames['localizacion_original']], '01010000202C0C0000B01E85ABFC642D41F2D24DE20A703041')

    def clean_table(self):
        print('Clean test_ladm_col.puntolindero table...')
        cur = self.db_connection.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = cur.execute("""DELETE FROM test_ladm_col.puntolindero WHERE true;""")
        self.db_connection.conn.commit()
        cur.close()
        if query is not None:
            print('The clean test_ladm_col.puntolindero is not working')

    @classmethod
    def tearDownClass(self):
        self.db_connection.conn.close()
        #pass
        #print('In this section the DB will be clear?')
        # self.drop_schema()


if __name__ == '__main__':
    nose2.main()
