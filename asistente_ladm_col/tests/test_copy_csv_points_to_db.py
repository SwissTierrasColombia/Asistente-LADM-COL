import qgis
import nose2
import psycopg2
import datetime

from qgis.testing import unittest, start_app
from processing.core.Processing import Processing
start_app() # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.tests.utils import import_projectgenerator, get_dbconn, get_test_path, restore_schema, clean_table
from asistente_ladm_col.utils.qgis_utils import QGISUtils
from asistente_ladm_col.config.table_mapping_config import BOUNDARY_POINT_TABLE

import_projectgenerator()

class TestCopy(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        print("\nINFO: Setting up copy CSV points to DB validation...")
        self.qgis_utils = QGISUtils()
        self.db_connection = get_dbconn('test_ladm_col')
        self.db_connection_3d = get_dbconn('test_ladm_col_3d')
        result = self.db_connection.test_connection()
        print('test_connection', result)
        if not result[1]:
            print('The test connection is not working')
            return
        restore_schema('test_ladm_col')
        restore_schema('test_ladm_col_3d')

    def test_copy_csv_to_db(self):
        print("\nINFO: Validating copy CSV points to DB...")
        clean_table('test_ladm_col', 'puntolindero')
        self.qgis_utils.disable_automatic_fields(self.db_connection, BOUNDARY_POINT_TABLE)
        self.upload_points_from_csv()
        self.validate_points_in_db()
        clean_table('test_ladm_col', 'puntolindero')

    def upload_points_from_csv(self):
        print("Copying CSV data with no elevation...")
        csv_path = get_test_path('csv/puntos_fixed.csv')
        txt_delimiter = ';'
        cbo_longitude = 'x'
        cbo_latitude = 'y'
        res = self.qgis_utils.copy_csv_to_db(csv_path,
                                    txt_delimiter,
                                    cbo_longitude,
                                    cbo_latitude,
                                    self.db_connection,
                                    self.qgis_utils.get_layer(self.db_connection, BOUNDARY_POINT_TABLE, load=True))
        self.assertEqual(res, True)

    def test_copy_csv_with_z_to_db(self):
        print("\nINFO: Validating copy CSV points with Z to DB...")
        clean_table('test_ladm_col_3d', 'puntolindero')
        self.qgis_utils.disable_automatic_fields(self.db_connection_3d, BOUNDARY_POINT_TABLE)
        self.upload_points_from_csv_with_elevation()
        self.validate_points_z_in_db()
        clean_table('test_ladm_col_3d', 'puntolindero')

    def upload_points_from_csv_with_elevation(self):
        print("\nINFO: Copying CSV data with elevation...")
        csv_path = get_test_path('csv/puntos_fixed.csv')
        txt_delimiter = ';'
        cbo_longitude = 'x'
        cbo_latitude = 'y'
        elevation = 'z'
        Processing.initialize()

        res = self.qgis_utils.copy_csv_to_db(csv_path,
                                             txt_delimiter,
                                             cbo_longitude,
                                             cbo_latitude,
                                             self.db_connection_3d,
                                     self.qgis_utils.get_layer(self.db_connection_3d, BOUNDARY_POINT_TABLE, load=True),
                                             elevation)
        self.assertEqual(res, True)

    def validate_points_in_db(self):
        cur = self.db_connection.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        print('\nINFO: Validating points')
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

    def validate_points_z_in_db(self):
        cur = self.db_connection.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        print('\nINFO: Validating points Z')
        query = cur.execute("""SELECT * FROM test_ladm_col_3d.puntolindero;""")
        results = cur.fetchall()
        print("Registers !!!!", results)
        colnames = {desc[0]: cur.description.index(desc) for desc in cur.description}
        self.assertEqual(len(results), 51)

        row = results[50]

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
        self.assertEqual(row[colnames['localizacion_original']], '01010000A02C0C0000B01E85ABFC642D41F2D24DE20A7030418B6CE7FB29529740')

    def test_copy_csv_overlapping_to_db(self):
        clean_table('test_ladm_col', 'puntolindero')
        self.upload_points_from_csv_overlapping()
        self.validate_points_overlapping_in_db()
        clean_table('test_ladm_col', 'puntolindero')

    def upload_points_from_csv_overlapping(self):
        csv_path = get_test_path('csv/puntos_overlapping.csv')
        txt_delimiter = ';'
        cbo_longitude = 'x'
        cbo_latitude = 'y'
        res = self.qgis_utils.copy_csv_to_db(csv_path,
                                    txt_delimiter,
                                    cbo_longitude,
                                    cbo_latitude,
                                    self.db_connection,
                                    self.qgis_utils.get_layer(self.db_connection, BOUNDARY_POINT_TABLE, load=True))

        self.assertEqual(res, False)

    def validate_points_overlapping_in_db(self):
        cur = self.db_connection.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        print('\nINFO: Validating points')
        query = cur.execute("""SELECT * FROM test_ladm_col.puntolindero;""")
        results = cur.fetchall()
        colnames = {desc[0]: cur.description.index(desc) for desc in cur.description}
        self.assertEqual(len(results), 0)

    @classmethod
    def tearDownClass(self):
        self.db_connection.conn.close()
        #pass
        #print('In this section the DB will be clear?')
        # self.drop_schema()


if __name__ == '__main__':
    nose2.main()
