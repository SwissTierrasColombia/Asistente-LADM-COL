import datetime

import nose2
import psycopg2
from qgis.testing import (unittest,
                          start_app)

from qgis.core import edit

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

SCHEMA_LADM_COL_EMPTY = 'test_ladm_col_empty'


class TestCopy(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        print("\nINFO: Setting up copy CSV points to DB validation...")
        self.qgis_utils = QGISUtils()
        restore_schema(SCHEMA_LADM_COL_EMPTY)
        self.db_connection = get_dbconn(SCHEMA_LADM_COL_EMPTY)

        result = self.db_connection.test_connection()
        print('test_connection', result)
        if not result[1]:
            print('The test connection is not working (test_connection)')
            return

        clean_table(SCHEMA_LADM_COL_EMPTY, BOUNDARY_POINT_TABLE)

    def test_copy_csv_to_db(self):
        print("\nINFO: Validating copy CSV points to DB...")
        clean_table(SCHEMA_LADM_COL_EMPTY, BOUNDARY_POINT_TABLE)
        self.qgis_utils.disable_automatic_fields(self.db_connection, BOUNDARY_POINT_TABLE)
        self.upload_points_from_csv(SCHEMA_LADM_COL_EMPTY)
        self.validate_points_in_db(SCHEMA_LADM_COL_EMPTY)

        test_layer = self.qgis_utils.get_layer(self.db_connection, BOUNDARY_POINT_TABLE, load=True)
        self.delete_features(test_layer)
        self.assertEqual(test_layer.featureCount(), 0)

    def upload_points_from_csv(self, schema):
        print("Copying CSV data with no elevation...")
        csv_path = get_test_path('csv/puntos_fixed_v296.csv')
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
        self.qgis_utils.disable_automatic_fields(self.db_connection, BOUNDARY_POINT_TABLE)
        self.upload_points_from_csv_crs_wgs84(SCHEMA_LADM_COL_EMPTY)
        self.validate_points_in_db_from_wgs84(SCHEMA_LADM_COL_EMPTY)

        test_layer = self.qgis_utils.get_layer(self.db_connection, BOUNDARY_POINT_TABLE, load=True)
        self.delete_features(test_layer)
        self.assertEqual(test_layer.featureCount(), 0)

    def upload_points_from_csv_crs_wgs84(self, schema):
        print("Copying CSV data in WGS84...")
        csv_path = get_test_path('csv/puntos_crs_4326_wgs84_v296.csv')
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
        query = cur.execute("""SELECT st_x(localizacion_original), st_y(localizacion_original) FROM {}.{};""".format(schema, BOUNDARY_POINT_TABLE))
        results = cur.fetchall()
        self.assertEqual(len(results), 3)
        self.assertEqual([round(result, 3) for result in results[0]], [round(item_test, 3) for item_test in [963254.898999999, 1077285.69999999]])
        self.assertEqual([round(result, 3) for result in results[1]], [round(item_test, 3) for item_test in [963203.763999999, 1077262.172]])
        self.assertEqual([round(result, 3) for result in results[2]], [round(item_test, 3) for item_test in [963198.334999999, 1077258.884]])

    def test_copy_csv_with_z_to_db(self):
        print("\nINFO: Validating copy CSV points with Z to DB...")
        clean_table(SCHEMA_LADM_COL_EMPTY, BOUNDARY_POINT_TABLE)
        self.qgis_utils.disable_automatic_fields(self.db_connection, BOUNDARY_POINT_TABLE)
        self.upload_points_from_csv_with_elevation(SCHEMA_LADM_COL_EMPTY)
        self.validate_points_in_db(SCHEMA_LADM_COL_EMPTY, with_z=True)

        test_layer = self.qgis_utils.get_layer(self.db_connection, BOUNDARY_POINT_TABLE, load=True)
        self.delete_features(test_layer)
        self.assertEqual(test_layer.featureCount(), 0)

    def upload_points_from_csv_with_elevation(self, schema):
        print("\nINFO: Copying CSV data with elevation...")
        csv_path = get_test_path('csv/puntos_fixed_v296.csv')
        txt_delimiter = ';'
        cbo_longitude = 'x'
        cbo_latitude = 'y'
        elevation = 'z'

        self.qgis_utils.copy_csv_to_db(csv_path,
                                       txt_delimiter,
                                       cbo_longitude,
                                       cbo_latitude,
                                       self.db_connection,
                                       DEFAULT_EPSG,
                                       BOUNDARY_POINT_TABLE,
                                       elevation)

        self.validate_number_of_boundary_points_in_db(schema, 51)

    def validate_points_in_db(self, schema, with_z=False):
        cur = self.db_connection.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        print('\nValidating points {}(both spatial and alphanumeric attributes)'.format('with Z ' if with_z else ''))
        query = cur.execute("""SELECT * FROM {}.{};""".format(schema, BOUNDARY_POINT_TABLE))
        results = cur.fetchall()
        colnames = {desc[0]: cur.description.index(desc) for desc in cur.description}

        self.assertEqual(len(results), 51)

        row = results[50]
        self.assertEqual(row[colnames['id_punto_lindero']], None)
        self.assertEqual(row[colnames['puntotipo']], 77)
        self.assertEqual(row[colnames['acuerdo']], 346)
        self.assertEqual(row[colnames['fotoidentificacion']], None)
        self.assertEqual(row[colnames['ubicacion_punto']], None)
        self.assertEqual(row[colnames['exactitud_horizontal']], 1)
        self.assertEqual(row[colnames['exactitud_vertical']], None)
        self.assertEqual(row[colnames['posicion_interpolacion']], None)
        self.assertEqual(row[colnames['monumentacion']], None)
        self.assertEqual(row[colnames['metodoproduccion']], None)
        self.assertEqual(row[colnames['espacio_de_nombres']], 'OP_PUNTOLINDERO')
        self.assertEqual(row[colnames['local_id']], '51')
        self.assertEqual(row[colnames['ue_op_servidumbrepaso']], None)
        self.assertEqual(row[colnames['ue_op_construccion']], None)
        self.assertEqual(row[colnames['ue_op_terreno']], None)
        self.assertEqual(row[colnames['ue_op_unidadconstruccion']], None)
        self.assertEqual(row[colnames['comienzo_vida_util_version']], datetime.datetime(2019, 10, 16, 10, 25, 9))
        self.assertEqual(row[colnames['fin_vida_util_version']], None)

        geom = '01010000A02C0C0000B01E85ABFC642D41F2D24DE20A7030410000000000000000'
        if with_z:
            geom = '01010000A02C0C0000B01E85ABFC642D41F2D24DE20A7030418B6CE7FB29529740'

        self.assertEqual(row[colnames['localizacion_original']], geom)

    def test_copy_csv_overlapping_to_db(self):
        print('\nINFO: Validating copy csv overlapping to db')
        clean_table(SCHEMA_LADM_COL_EMPTY, BOUNDARY_POINT_TABLE)
        self.upload_points_from_csv_overlapping(SCHEMA_LADM_COL_EMPTY)
        self.validate_number_of_boundary_points_in_db(SCHEMA_LADM_COL_EMPTY, 0)

        test_layer = self.qgis_utils.get_layer(self.db_connection, BOUNDARY_POINT_TABLE, load=True)
        self.delete_features(test_layer)
        self.assertEqual(test_layer.featureCount(), 0)

    def upload_points_from_csv_overlapping(self, schema):
        print('Uploading points from csv overlapping...')
        csv_path = get_test_path('csv/puntos_overlapping_v269.csv')
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
        query = cur.execute("""SELECT count(t_id) FROM {}.{};""".format(schema, BOUNDARY_POINT_TABLE))
        result = cur.fetchone()
        self.assertEqual(result[0], num)

    @staticmethod
    def delete_features(layer):
        with edit(layer):
            list_ids = [feat.id() for feat in layer.getFeatures()]
            layer.deleteFeatures(list_ids)

    @classmethod
    def tearDownClass(self):
        self.db_connection.conn.close()


if __name__ == '__main__':
    nose2.main()
