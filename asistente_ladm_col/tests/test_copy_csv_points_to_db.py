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
                                            clean_table,
                                            reproject_to_ctm12)
from asistente_ladm_col.lib.geometry import GeometryUtils

from asistente_ladm_col.logic.ladm_col.ladm_data import LADMData

import_processing()

SCHEMA_LADM_COL_EMPTY = 'test_ladm_col_empty'


class TestCopy(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\nINFO: Setting up copy CSV points to DB validation...")
        print("INFO: Restoring databases to be used")
        import_qgis_model_baker()
        import_asistente_ladm_col()
        cls.app = AppInterface()

    def setUp(self):
        restore_schema(SCHEMA_LADM_COL_EMPTY, True)
        self.db_pg = get_pg_conn(SCHEMA_LADM_COL_EMPTY)

        self.names = self.db_pg.names
        self.ladm_data = LADMData()
        self.geometry = GeometryUtils()

        res, code, msg = self.db_pg.test_connection()
        self.assertTrue(res, msg)
        self.assertIsNotNone(self.names.LC_BOUNDARY_POINT_T, 'Names is None')

    def test_copy_csv_to_db(self):
        print("\nINFO: Validating copy CSV points to DB...")
        clean_table(SCHEMA_LADM_COL_EMPTY, self.names.LC_BOUNDARY_POINT_T)
        layer = self.app.core.get_layer(self.db_pg, self.names.LC_BOUNDARY_POINT_T, True)
        self.app.core.disable_automatic_fields(layer)

        csv_path = get_test_path('csv/puntos_fixed_ladm_v1_1.csv')
        txt_delimiter = ';'
        cbo_longitude = 'x'
        cbo_latitude = 'y'
        csv_layer = self.app.core.csv_to_layer(csv_path, txt_delimiter, cbo_longitude, cbo_latitude, "EPSG:9377", reproject=False)

        self.upload_points_from_csv(csv_layer, SCHEMA_LADM_COL_EMPTY)

        self.validate_points_in_db(SCHEMA_LADM_COL_EMPTY)
        test_layer = self.app.core.get_layer(self.db_pg, self.names.LC_BOUNDARY_POINT_T, load=True)
        delete_features(test_layer)
        self.assertEqual(test_layer.featureCount(), 0)

    def boundary_point_layer_resolve_domains_for_test(self, csv_layer):
        data_provider = csv_layer.dataProvider()
        data_provider.addAttributes([QgsField('acuerdo', QVariant.Int),
                                     QgsField('puntotipo', QVariant.Int),
                                     QgsField('metodoproduccion', QVariant.Int)])
        csv_layer.updateFields()

        idx_agreement_field = data_provider.fieldNameIndex('acuerdo')
        idx_point_type_field = data_provider.fieldNameIndex('puntotipo')
        idx_production_method_field = data_provider.fieldNameIndex('metodoproduccion')

        with edit(csv_layer):
            for feature in csv_layer.getFeatures():
                feature.setAttribute(idx_agreement_field, self.ladm_data.get_domain_code_from_value(self.db_pg, self.names.LC_AGREEMENT_TYPE_D, feature['_acuerdo']))
                feature.setAttribute(idx_point_type_field, self.ladm_data.get_domain_code_from_value(self.db_pg, self.names.COL_POINT_TYPE_D, feature['_puntotipo']))
                feature.setAttribute(idx_production_method_field, self.ladm_data.get_domain_code_from_value(self.db_pg, self.names.COL_PRODUCTION_METHOD_TYPE_D, feature['_metodoproduccion']))
                csv_layer.updateFeature(feature)

    def upload_points_from_csv(self, csv_layer, schema):
        print("Copying CSV data with no elevation...")
        self.boundary_point_layer_resolve_domains_for_test(csv_layer)
        test_layer = self.app.core.get_layer(self.db_pg, self.names.LC_BOUNDARY_POINT_T, load=True)
        run_etl_model(self.names, csv_layer, test_layer, self.names.LC_BOUNDARY_POINT_T)
        self.assertEqual(test_layer.featureCount(), 51)
        self.validate_number_of_boundary_points_in_db(schema, 51)

    def test_upload_points_from_csv_crs_wgs84(self):
        print("\nINFO: Copying CSV data with EPSG:4326...")
        layer = self.app.core.get_layer(self.db_pg, self.names.LC_BOUNDARY_POINT_T, True)
        self.app.core.disable_automatic_fields(layer)

        csv_path = get_test_path('csv/puntos_crs_4326_wgs84_ladm_v1_1.csv')
        txt_delimiter = ';'
        cbo_longitude = 'x'
        cbo_latitude = 'y'
        crs = 'EPSG:4326'
        csv_layer = self.app.core.csv_to_layer(csv_path, txt_delimiter, cbo_longitude, cbo_latitude, crs, reproject=False)
        csv_layer = reproject_to_ctm12(csv_layer)

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
        cur.execute("""SELECT st_x(geometria), st_y(geometria) FROM {}.{};""".format(schema, self.names.LC_BOUNDARY_POINT_T))
        results = cur.fetchall()
        self.assertEqual(len(results), 3)
        self.assertEqual([round(result, 3) for result in results[0]], [round(item_test, 3) for item_test in [4843984.711, 2143385.632]])
        self.assertEqual([round(result, 3) for result in results[1]], [round(item_test, 3) for item_test in [4843918.478, 2143442.584]])
        self.assertEqual([round(result, 3) for result in results[2]], [round(item_test, 3) for item_test in [4843979.173, 2143379.773]])

    def test_copy_csv_with_z_to_db(self):
        print("\nINFO: Validating copy CSV points with Z to DB...")
        clean_table(SCHEMA_LADM_COL_EMPTY, self.names.LC_BOUNDARY_POINT_T)
        layer = self.app.core.get_layer(self.db_pg, self.names.LC_BOUNDARY_POINT_T, True)
        self.app.core.disable_automatic_fields(layer)

        csv_path = get_test_path('csv/puntos_fixed_ladm_v1_1.csv')
        txt_delimiter = ';'
        cbo_longitude = 'x'
        cbo_latitude = 'y'
        elevation = 'z'
        csv_layer = self.app.core.csv_to_layer(csv_path, txt_delimiter, cbo_longitude, cbo_latitude, "EPSG:9377", elevation, reproject=False)

        self.upload_points_from_csv_with_elevation(csv_layer, SCHEMA_LADM_COL_EMPTY)
        self.validate_points_in_db(SCHEMA_LADM_COL_EMPTY, with_z=True)

        test_layer = self.app.core.get_layer(self.db_pg, self.names.LC_BOUNDARY_POINT_T, load=True)
        delete_features(test_layer)
        self.assertEqual(test_layer.featureCount(), 0)

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
        cur.execute("""SELECT * FROM {}.{};""".format(schema, self.names.LC_BOUNDARY_POINT_T))
        results = cur.fetchall()
        colnames = {desc[0]: cur.description.index(desc) for desc in cur.description}

        self.assertEqual(len(results), 51)

        for row in results:
            if row[colnames['id_punto_lindero']] == '50':
                break

        self.assertEqual(row[colnames['id_punto_lindero']], '50')
        self.assertEqual(row[colnames['puntotipo']], 17)
        self.assertEqual(row[colnames['acuerdo']], 596)
        self.assertEqual(row[colnames['fotoidentificacion']], None)
        self.assertEqual(row[colnames['exactitud_horizontal']], 1.000)
        self.assertEqual(row[colnames['exactitud_vertical']], None)
        self.assertEqual(row[colnames['posicion_interpolacion']], None)
        self.assertEqual(row[colnames['metodoproduccion']], 1)
        self.assertEqual(row[colnames['espacio_de_nombres']], 'LC_PUNTOLINDERO')
        self.assertIsNotNone(row[colnames['local_id']])
        self.assertIsNone(row[colnames['ue_lc_servidumbretransito']])
        self.assertIsNone(row[colnames['ue_lc_construccion']])
        self.assertIsNone(row[colnames['ue_lc_terreno']])
        self.assertIsNone(row[colnames['ue_lc_unidadconstruccion']])
        self.assertIsNone(row[colnames['fin_vida_util_version']])

        geom = '01010000A0A1240000EC51B836A57A5241CDCCCC7C8D5A40410000000000000000'
        if with_z:
            geom = '01010000A0A1240000EC51B836A57A5241CDCCCC7C8D5A404123DBF97EEA2E9640'

        self.assertEqual(row[colnames['geometria']], geom)

    def test_copy_csv_overlapping_to_db(self):
        print('\nINFO: Validating copy csv overlapping to db')
        clean_table(SCHEMA_LADM_COL_EMPTY, self.names.LC_BOUNDARY_POINT_T)
        csv_path = get_test_path('csv/puntos_overlapping_ladm_v1_1.csv')
        txt_delimiter = ';'
        cbo_longitude = 'x'
        cbo_latitude = 'y'
        csv_layer = self.app.core.csv_to_layer(csv_path, txt_delimiter, cbo_longitude, cbo_latitude, "EPSG:9377", reproject=False)

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
        cur.execute("""SELECT count(t_id) FROM {}.{};""".format(schema, self.names.LC_BOUNDARY_POINT_T))
        result = cur.fetchone()
        self.assertEqual(result[0], num)

    def tearDown(self):
        print("INFO: Closing open connections to databases")
        self.db_pg.conn.close()

    @classmethod
    def tearDownClass(cls):
        unload_qgis_model_baker()


if __name__ == '__main__':
    nose2.main()
