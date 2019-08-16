import datetime

import nose2
import psycopg2
from qgis.testing import (unittest,
                          start_app)

start_app() # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.tests.utils import (import_qgis_model_baker,
                                            import_processing,
                                            get_dbconn,
                                            get_test_path,
                                            restore_schema,
                                            clean_table)
from asistente_ladm_col.utils.qgis_utils import QGISUtils
from asistente_ladm_col.config.table_mapping_config import BOUNDARY_POINT_TABLE
from asistente_ladm_col.config.general_config import DEFAULT_EPSG

import_qgis_model_baker()
import_processing()


class TestCopy(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        print("\nINFO: Setting up copy CSV points to DB validation...")
        self.qgis_utils = QGISUtils()
        restore_schema('test_ladm_col')
        self.db_connection = get_dbconn('test_ladm_col')

        restore_schema('test_ladm_col_3d')
        self.db_connection_3d = get_dbconn('test_ladm_col_3d')

        result = self.db_connection.test_connection()
        print('test_connection', result)
        if not result[1]:
            print('The test connection is not working (test_connection)')
            return

        result = self.db_connection_3d.test_connection()
        print('test_ladm_col_3d', result)
        if not result[1]:
            print('The test connection is not working (test_ladm_col_3d)')
            return


    def test_copy_csv_to_db(self):
        print("\nINFO: Validating copy CSV points to DB...")
        schema = 'test_ladm_col'
        clean_table('test_ladm_col', BOUNDARY_POINT_TABLE)
        self.qgis_utils.disable_automatic_fields(self.db_connection, BOUNDARY_POINT_TABLE)
        self.upload_points_from_csv(schema)
        self.validate_points_in_db(schema)
        clean_table(schema, BOUNDARY_POINT_TABLE)

    def upload_points_from_csv(self, schema):
        print("Copying CSV data with no elevation...")
        csv_path = get_test_path('csv/puntos_fixed.csv')
        txt_delimiter = ';'
        cbo_longitude = 'x'
        cbo_latitude = 'y'
        self.qgis_utils.copy_csv_to_db(csv_path,
                                    txt_delimiter,
                                    cbo_longitude,
                                    cbo_latitude,
                                    self.db_connection,
                                    DEFAULT_EPSG,
                                    BOUNDARY_POINT_TABLE)

        self.validate_number_of_boundary_points_in_db(schema, 51)

    def test_upload_points_from_csv_crs_wgs84(self):
        print("\nINFO: Copying CSV data with EPSG:4326...")
        schema = 'test_ladm_col'
        clean_table(schema, BOUNDARY_POINT_TABLE)
        self.qgis_utils.disable_automatic_fields(self.db_connection, BOUNDARY_POINT_TABLE)
        self.upload_points_from_csv_crs_wgs84(schema)
        self.validate_points_in_db_from_wgs84(schema)
        clean_table(schema, BOUNDARY_POINT_TABLE)

    def upload_points_from_csv_crs_wgs84(self, schema):
        print("Copying CSV data in WGS84...")
        csv_path = get_test_path('csv/puntos_crs_4326_wgs84.csv')
        txt_delimiter = ';'
        cbo_longitude = 'x'
        cbo_latitude = 'y'
        epsg = '4326'

        res = self.qgis_utils.copy_csv_to_db(csv_path,
                                    txt_delimiter,
                                    cbo_longitude,
                                    cbo_latitude,
                                    self.db_connection,
                                    epsg,
                                    BOUNDARY_POINT_TABLE)

        self.validate_number_of_boundary_points_in_db(schema, 3)

    def validate_points_in_db_from_wgs84(self, schema):
        print('\nINFO: Validating points in db from wgs84')
        cur = self.db_connection.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = cur.execute("""SELECT st_x(localizacion_original), st_y(localizacion_original) FROM {}.puntolindero;""".format(schema))
        results = cur.fetchall()
        self.assertEqual(len(results), 3)
        self.assertEqual(results, [[963052.433292674, 1077370.54548811], [963056.711416816, 1077286.71929338], [963056.670399835, 1077210.30465577]])

    def test_copy_csv_with_z_to_db(self):
        print("\nINFO: Validating copy CSV points with Z to DB...")
        schema = 'test_ladm_col_3d'
        clean_table(schema, BOUNDARY_POINT_TABLE)
        self.qgis_utils.disable_automatic_fields(self.db_connection_3d, BOUNDARY_POINT_TABLE)
        self.upload_points_from_csv_with_elevation(schema)
        self.validate_points_in_db(schema, with_z=True)
        clean_table(schema, BOUNDARY_POINT_TABLE)

    def upload_points_from_csv_with_elevation(self, schema):
        print("\nINFO: Copying CSV data with elevation...")
        csv_path = get_test_path('csv/puntos_fixed.csv')
        txt_delimiter = ';'
        cbo_longitude = 'x'
        cbo_latitude = 'y'
        elevation = 'z'

        self.qgis_utils.copy_csv_to_db(csv_path,
                                       txt_delimiter,
                                       cbo_longitude,
                                       cbo_latitude,
                                       self.db_connection_3d,
                                       DEFAULT_EPSG,
                                       BOUNDARY_POINT_TABLE,
                                       elevation)

        self.validate_number_of_boundary_points_in_db(schema, 51)

    def validate_points_in_db(self, schema, with_z=False):
        cur = self.db_connection.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        print('\nValidating points {}(both spatial and alphanumeric attributes)'.format('with Z ' if with_z else ''))
        query = cur.execute("""SELECT * FROM {}.puntolindero;""".format(schema))
        results = cur.fetchall()
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

        geom = '01010000202C0C0000B01E85ABFC642D41F2D24DE20A703041'
        if with_z:
            geom = '01010000A02C0C0000B01E85ABFC642D41F2D24DE20A7030418B6CE7FB29529740'

        self.assertEqual(row[colnames['localizacion_original']], geom)

    def test_copy_csv_overlapping_to_db(self):
        print('\nINFO: Validating copy csv overlapping to db')
        schema = 'test_ladm_col'
        clean_table(schema, 'puntolindero')
        self.upload_points_from_csv_overlapping(schema)
        self.validate_number_of_boundary_points_in_db(schema, 0)
        clean_table(schema, 'puntolindero')

    def upload_points_from_csv_overlapping(self, schema):
        print('Uploading points from csv overlapping...')
        csv_path = get_test_path('csv/puntos_overlapping.csv')
        txt_delimiter = ';'
        cbo_longitude = 'x'
        cbo_latitude = 'y'
        self.qgis_utils.copy_csv_to_db(csv_path,
                                    txt_delimiter,
                                    cbo_longitude,
                                    cbo_latitude,
                                    self.db_connection,
                                    DEFAULT_EPSG,
                                    BOUNDARY_POINT_TABLE)

        self.validate_number_of_boundary_points_in_db(schema, 0)

    def validate_number_of_boundary_points_in_db(self, schema, num=0):
        print('\nINFO: Validating number of boundary points in schema {}'.format(schema))
        cur = self.db_connection.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = cur.execute("""SELECT count(t_id) FROM {}.puntolindero;""".format(schema))
        result = cur.fetchone()
        self.assertEqual(result[0], num)

    @classmethod
    def tearDownClass(self):
        self.db_connection.conn.close()


if __name__ == '__main__':
    nose2.main()
