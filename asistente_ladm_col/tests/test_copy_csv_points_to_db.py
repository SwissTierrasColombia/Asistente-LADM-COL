import nose2
import psycopg2
from qgis.testing import (unittest,
                          start_app)
from qgis.PyQt.QtCore import QVariant

from qgis.core import (edit,
                       QgsField)

from asistente_ladm_col.app_interface import AppInterface

start_app() # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.tests.utils import (import_qgis_model_baker,
                                            run_etl_model,
                                            import_asistente_ladm_col,
                                            unload_qgis_model_baker,
                                            import_processing,
                                            get_pg_conn,
                                            delete_features,
                                            get_test_path,
                                            restore_schema,
                                            clean_table)
from asistente_ladm_col.lib.geometry import GeometryUtils
from asistente_ladm_col.config.general_config import DEFAULT_EPSG

from asistente_ladm_col.logic.ladm_col.ladm_data import LADMDATA

import_processing()

SCHEMA_LADM_COL_EMPTY = 'test_ladm_col_empty'


class TestCopy(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\nINFO: Setting up copy CSV points to DB validation...")
        print("INFO: Restoring databases to be used")
        import_qgis_model_baker()
        restore_schema(SCHEMA_LADM_COL_EMPTY)
        cls.db_pg = get_pg_conn(SCHEMA_LADM_COL_EMPTY)

        cls.app = AppInterface()
        cls.names = cls.db_pg.names
        import_asistente_ladm_col()
        cls.ladm_data = LADMDATA()
        cls.geometry = GeometryUtils()

        result = cls.db_pg.test_connection()
        cls.assertTrue(result[0], 'The test connection is not working for empty db')
        cls.assertIsNotNone(cls.names.LC_BOUNDARY_POINT_T, 'Names is None')

    def _test_copy_csv_to_db(self):
        print("\nINFO: Validating copy CSV points to DB...")
        clean_table(SCHEMA_LADM_COL_EMPTY, self.names.LC_BOUNDARY_POINT_T)
        layer = self.app.core.get_layer(self.db_pg, self.names.LC_BOUNDARY_POINT_T, True)
        self.app.core.disable_automatic_fields(layer)

        csv_path = get_test_path('csv/puntos_fixed_v296.csv')
        txt_delimiter = ';'
        cbo_longitude = 'x'
        cbo_latitude = 'y'
        csv_layer = self.app.core.csv_to_layer(csv_path, txt_delimiter, cbo_longitude, cbo_latitude, DEFAULT_EPSG)
        self.upload_points_from_csv(csv_layer, SCHEMA_LADM_COL_EMPTY)

        self.validate_points_in_db(SCHEMA_LADM_COL_EMPTY)
        test_layer = self.app.core.get_layer(self.db_pg, self.names.LC_BOUNDARY_POINT_T, load=True)
        delete_features(test_layer)
        self.assertEqual(test_layer.featureCount(), 0)

        # TODO: Rewrite test using t_ili_tids instead of depending on a list order...

    def boundary_point_layer_resolve_domains_for_test(self, csv_layer):
        data_provider = csv_layer.dataProvider()
        data_provider.addAttributes([QgsField('acuerdo', QVariant.Int),
                                     QgsField('puntotipo', QVariant.Int)])
        csv_layer.updateFields()

        idx_agreement_field = data_provider.fieldNameIndex('acuerdo')
        idx_point_type_field = data_provider.fieldNameIndex('puntotipo')

        with edit(csv_layer):
            for feature in csv_layer.getFeatures():
                feature.setAttribute(idx_agreement_field, self.ladm_data.get_domain_code_from_value(self.db_pg, self.names.LC_AGREEMENT_TYPE_D, feature['_acuerdo']))
                feature.setAttribute(idx_point_type_field, self.ladm_data.get_domain_code_from_value(self.db_pg, self.names.LC_POINT_TYPE_D, feature['_puntotipo']))
                csv_layer.updateFeature(feature)

    def upload_points_from_csv(self, csv_layer, schema):
        print("Copying CSV data with no elevation...")
        self.boundary_point_layer_resolve_domains_for_test(csv_layer)
        test_layer = self.app.core.get_layer(self.db_pg, self.names.LC_BOUNDARY_POINT_T, load=True)
        run_etl_model(self.names, csv_layer, test_layer, self.names.LC_BOUNDARY_POINT_T)
        self.assertEqual(test_layer.featureCount(), 51)
        self.validate_number_of_boundary_points_in_db(schema, 51)

    def _test_upload_points_from_csv_crs_wgs84(self):
        print("\nINFO: Copying CSV data with EPSG:4326...")
        layer = self.app.core.get_layer(self.db_pg, self.names.LC_BOUNDARY_POINT_T, True)
        self.app.core.disable_automatic_fields(layer)

        csv_path = get_test_path('csv/puntos_crs_4326_wgs84_v296.csv')
        txt_delimiter = ';'
        cbo_longitude = 'x'
        cbo_latitude = 'y'
        epsg = '4326'
        csv_layer = self.app.core.csv_to_layer(csv_path, txt_delimiter, cbo_longitude, cbo_latitude, epsg)


        self.upload_points_from_csv_crs_wgs84(csv_layer, SCHEMA_LADM_COL_EMPTY)
        self.validate_points_in_db_from_wgs84(SCHEMA_LADM_COL_EMPTY)

        test_layer = self.app.core.get_layer(self.db_pg, self.names.LC_BOUNDARY_POINT_T, load=True)
        delete_features(test_layer)
        self.assertEqual(test_layer.featureCount(), 0)

    def upload_points_from_csv_crs_wgs84(self, csv_layer, schema):
        print("Copying CSV data in WGS84...")
        self.boundary_point_layer_resolve_domains_for_test(csv_layer)
        test_layer = self.app.core.get_layer(self.db_pg, self.names.LC_BOUNDARY_POINT_T, load=True)
        run_etl_model(self.names, csv_layer, test_layer, self.names.LC_BOUNDARY_POINT_T)
        self.validate_number_of_boundary_points_in_db(schema, 3)

    def validate_points_in_db_from_wgs84(self, schema):
        print('\nINFO: Validating points in db from wgs84')
        cur = self.db_pg.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = cur.execute("""SELECT st_x(geometria), st_y(geometria) FROM {}.{};""".format(schema, self.names.LC_BOUNDARY_POINT_T))
        results = cur.fetchall()
        self.assertEqual(len(results), 3)
        self.assertEqual([round(result, 3) for result in results[0]], [round(item_test, 3) for item_test in [963254.898999999, 1077285.69999999]])
        self.assertEqual([round(result, 3) for result in results[1]], [round(item_test, 3) for item_test in [963203.763999999, 1077262.172]])
        self.assertEqual([round(result, 3) for result in results[2]], [round(item_test, 3) for item_test in [963198.334999999, 1077258.884]])

    def _test_copy_csv_with_z_to_db(self):
        print("\nINFO: Validating copy CSV points with Z to DB...")
        clean_table(SCHEMA_LADM_COL_EMPTY, self.names.LC_BOUNDARY_POINT_T)
        layer = self.app.core.get_layer(self.db_pg, self.names.LC_BOUNDARY_POINT_T, True)
        self.app.core.disable_automatic_fields(layer)

        csv_path = get_test_path('csv/puntos_fixed_v296.csv')
        txt_delimiter = ';'
        cbo_longitude = 'x'
        cbo_latitude = 'y'
        elevation = 'z'
        csv_layer = self.app.core.csv_to_layer(csv_path, txt_delimiter, cbo_longitude, cbo_latitude, DEFAULT_EPSG, elevation)

        self.upload_points_from_csv_with_elevation(csv_layer, SCHEMA_LADM_COL_EMPTY)
        self.validate_points_in_db(SCHEMA_LADM_COL_EMPTY, with_z=True)

        test_layer = self.app.core.get_layer(self.db_pg, self.names.LC_BOUNDARY_POINT_T, load=True)
        delete_features(test_layer)
        self.assertEqual(test_layer.featureCount(), 0)

        # TODO: Rewrite test using t_ili_tids instead of depending on a list order...

    def upload_points_from_csv_with_elevation(self, csv_layer, schema):
        print("\nINFO: Copying CSV data with elevation...")
        self.boundary_point_layer_resolve_domains_for_test(csv_layer)
        test_layer = self.app.core.get_layer(self.db_pg, self.names.LC_BOUNDARY_POINT_T, load=True)
        run_etl_model(self.names, csv_layer, test_layer, self.names.LC_BOUNDARY_POINT_T)
        self.assertEqual(test_layer.featureCount(), 51)
        self.validate_number_of_boundary_points_in_db(schema, 51)

    def validate_points_in_db(self, schema, with_z=False):
        cur = self.db_pg.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        print('\nValidating points {}(both spatial and alphanumeric attributes)'.format('with Z ' if with_z else ''))
        query = cur.execute("""SELECT * FROM {}.{};""".format(schema, self.names.LC_BOUNDARY_POINT_T))
        results = cur.fetchall()
        colnames = {desc[0]: cur.description.index(desc) for desc in cur.description}

        self.assertEqual(len(results), 51)

        row = results[50]
        self.assertEqual(row[colnames['id_punto_lindero']], None)
        self.assertEqual(row[colnames['puntotipo']], 208)
        self.assertEqual(row[colnames['acuerdo']], 485)
        self.assertEqual(row[colnames['fotoidentificacion']], None)
        self.assertEqual(row[colnames['ubicacion_punto']], None)
        self.assertEqual(row[colnames['exactitud_horizontal']], 1)
        self.assertEqual(row[colnames['exactitud_vertical']], None)
        self.assertEqual(row[colnames['posicion_interpolacion']], None)
        self.assertEqual(row[colnames['metodoproduccion']], None)
        self.assertEqual(row[colnames['espacio_de_nombres']], 'OP_PUNTOLINDERO')
        self.assertEqual(row[colnames['local_id']], '51')
        self.assertEqual(row[colnames['ue_op_servidumbrepaso']], None)
        self.assertEqual(row[colnames['ue_op_construccion']], None)
        self.assertEqual(row[colnames['ue_op_terreno']], None)
        self.assertEqual(row[colnames['ue_op_unidadconstruccion']], None)
        self.assertEqual(row[colnames['fin_vida_util_version']], None)

        geom = '01010000A02C0C0000B01E85ABFC642D41F2D24DE20A7030410000000000000000'
        if with_z:
            geom = '01010000A02C0C0000B01E85ABFC642D41F2D24DE20A7030418B6CE7FB29529740'

        self.assertEqual(row[colnames['geometria']], geom)

    def _test_copy_csv_overlapping_to_db(self):
        # TODO: Fix this test!
        # Message:
        # AttributeError: 'bool' object has no attribute 'featureCount'

        print('\nINFO: Validating copy csv overlapping to db')
        clean_table(SCHEMA_LADM_COL_EMPTY, self.names.LC_BOUNDARY_POINT_T)
        csv_path = get_test_path('csv/puntos_overlapping_v269.csv')
        txt_delimiter = ';'
        cbo_longitude = 'x'
        cbo_latitude = 'y'
        csv_layer = self.app.core.csv_to_layer(csv_path, txt_delimiter, cbo_longitude, cbo_latitude, DEFAULT_EPSG)
        self.upload_points_from_csv_overlapping(csv_layer, SCHEMA_LADM_COL_EMPTY)
        self.validate_number_of_boundary_points_in_db(SCHEMA_LADM_COL_EMPTY, 0)

        test_layer = self.app.core.get_layer(self.db_pg, self.names.LC_BOUNDARY_POINT_T, load=True)
        delete_features(test_layer)
        self.assertEqual(test_layer.featureCount(), 0)

    def upload_points_from_csv_overlapping(self, csv_layer, schema):
        print('Uploading points from csv overlapping...')
        overlapping = self.geometry.get_overlapping_points(csv_layer)

        if not overlapping:
            self.boundary_point_layer_resolve_domains_for_test(csv_layer)
            test_layer = self.app.core.get_layer(self.db_pg, self.names.LC_BOUNDARY_POINT_T, load=True)
            run_etl_model(self.names, csv_layer, test_layer, self.names.LC_BOUNDARY_POINT_T)

        self.validate_number_of_boundary_points_in_db(schema, 0)

    def validate_number_of_boundary_points_in_db(self, schema, num=0):
        print('\nINFO: Validating number of boundary points in schema {}'.format(schema))
        cur = self.db_pg.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = cur.execute("""SELECT count(t_id) FROM {}.{};""".format(schema, self.names.LC_BOUNDARY_POINT_T))
        result = cur.fetchone()
        self.assertEqual(result[0], num)

    @classmethod
    def tearDownClass(cls):
        print("INFO: Closing open connections to databases")
        cls.db_pg.conn.close()
        unload_qgis_model_baker()


if __name__ == '__main__':
    nose2.main()
