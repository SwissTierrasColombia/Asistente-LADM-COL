import nose2

from qgis.core import (QgsVectorLayer,
                       QgsWkbTypes)
from qgis.testing import (unittest,
                          start_app)

start_app() # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.tests.utils import (import_projectgenerator,
                                            get_dbconn,
                                            restore_schema,
                                            run_etl_model,
                                            clean_table)
from asistente_ladm_col.utils.qgis_utils import QGISUtils
from asistente_ladm_col.tests.utils import get_test_copy_path
from asistente_ladm_col.config.table_mapping_config import BOUNDARY_POINT_TABLE

import_projectgenerator()


class TestGeomsLoad(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        print("\nINFO: Setting up copy Layer With different Geometries to DB validation...")
        self.qgis_utils = QGISUtils()
        self.gpkg_path = get_test_copy_path('geopackage/points_z_m_zm.gpkg')
        self.test_connection = get_dbconn('test_distinct_geoms')
        self.db_connection = get_dbconn('test_ladm_col')
        self.db_connection_3d = get_dbconn('test_ladm_col_3d')
        result = self.test_connection.test_connection()
        print('test_connection', result)
        if not result[1]:
            print('The test connection is not working')
            return
        result = self.db_connection.test_connection()
        restore_schema('test_distinct_geoms')
        restore_schema('test_ladm_col')
        restore_schema('test_ladm_col_3d')

    def test_valid_import_geom_2d_to_db_gpkg(self):
        print('\nINFO: Validating ETL-Model from [ Point, PointZ, PointM, PointZM ] to Point geometries...')

        # Layer in LADM for test
        test_layer = self.qgis_utils.get_layer(self.db_connection, BOUNDARY_POINT_TABLE, load=True)

        # Point To Point
        print("Validating Point to Point")
        uri = self.gpkg_path + '|layername={layername}'.format(layername='points')
        point_layer = QgsVectorLayer(uri, 'points', 'ogr')
        print("Is Valid layer :", point_layer.isValid())
        run_etl_model(point_layer, out_layer=test_layer)
        test_layer.startEditing()
        print("Info: Validating geometry Point...")
        self.assertEqual(QgsWkbTypes.PointGeometry, test_layer.type())
        self.assertEqual(QgsWkbTypes.Point, point_layer.wkbType())
        self.assertEqual(QgsWkbTypes.Point, test_layer.wkbType())
        self.assertEqual(test_layer.featureCount(), 51)
        clean_table('test_ladm_col', BOUNDARY_POINT_TABLE)
        test_layer.dataProvider().truncate()

        # PointZ To Point
        print("Validating PointZ to Point")
        uri = self.gpkg_path + '|layername={layername}'.format(layername='points_Z')
        point_layer = QgsVectorLayer(uri, 'points_Z', 'ogr')
        print("Is Valid layer :", point_layer.isValid())
        self.assertIn(point_layer.wkbType(), [QgsWkbTypes.PointZ, QgsWkbTypes.Point25D])
        output = run_etl_model(point_layer, out_layer=test_layer)
        print("Info: Validating geometry PointZ...", test_layer.wkbType())
        self.assertEqual(QgsWkbTypes.PointGeometry, test_layer.type())
        self.assertEqual(QgsWkbTypes.Point, test_layer.wkbType())
        self.assertEqual(test_layer.featureCount(), 51)
        clean_table('test_ladm_col', BOUNDARY_POINT_TABLE)
        test_layer.dataProvider().truncate()

        # PointM To Point
        print("Validating PointM To Point")
        uri = self.gpkg_path + '|layername={layername}'.format(layername='points_M')
        point_layer = QgsVectorLayer(uri, 'points', 'ogr')
        print("Is Valid layer :", point_layer.isValid())
        run_etl_model(point_layer, out_layer=test_layer)
        print("Info: Validating geometry PointZ...", test_layer.wkbType())
        self.assertEqual(QgsWkbTypes.PointGeometry, test_layer.type())
        self.assertEqual(QgsWkbTypes.PointM, point_layer.wkbType())
        self.assertEqual(QgsWkbTypes.Point, test_layer.wkbType())
        self.assertEqual(test_layer.featureCount(), 51)
        clean_table('test_ladm_col', BOUNDARY_POINT_TABLE)
        test_layer.dataProvider().truncate()

        # PointZM To Point
        print("Validating PointZM To Point")
        uri = self.gpkg_path + '|layername={layername}'.format(layername='points_ZM')
        point_layer = QgsVectorLayer(uri, 'points', 'ogr')
        print("Is Valid layer :", point_layer.isValid())
        run_etl_model(point_layer, out_layer=test_layer)
        print("Info: Validating geometry PointZ...", test_layer.wkbType())
        self.assertEqual(QgsWkbTypes.PointGeometry, test_layer.type())
        self.assertEqual(QgsWkbTypes.PointZM, point_layer.wkbType())
        self.assertEqual(QgsWkbTypes.Point, test_layer.wkbType())
        self.assertEqual(test_layer.featureCount(), 51)
        clean_table('test_ladm_col', BOUNDARY_POINT_TABLE)
        test_layer.dataProvider().truncate()


    def test_valid_import_geom_3d_to_db_gpkg(self):
        print('\nINFO: Validating ETL-Model from [ Point, PointZ, PointM, PointZM ] to PointZ geometries...')

        test_layer_3d = self.qgis_utils.get_layer(self.db_connection_3d, BOUNDARY_POINT_TABLE, load=True)

        # Point To PointZ
        print("Validating Point to PointZ")
        uri = self.gpkg_path + '|layername={layername}'.format(layername='points')
        point_layer = QgsVectorLayer(uri, 'points', 'ogr')
        print("Is Valid layer :", point_layer.isValid())
        run_etl_model(point_layer, out_layer=test_layer_3d)
        print("Info: Validating geometry Point...")
        self.assertEqual(QgsWkbTypes.PointGeometry, test_layer_3d.type())
        self.assertEqual(QgsWkbTypes.Point, point_layer.wkbType())
        self.assertEqual(QgsWkbTypes.PointZ, test_layer_3d.wkbType())
        self.assertEqual(test_layer_3d.featureCount(), 51)
        test_layer_3d.startEditing()
        clean_table('test_ladm_col_3d', BOUNDARY_POINT_TABLE)
        test_layer_3d.dataProvider().truncate()

        # PointZ To PointZ
        print("Validating PointZ to PointZ")
        uri = self.gpkg_path + '|layername={layername}'.format(layername='points_Z')
        point_layer = QgsVectorLayer(uri, 'points', 'ogr')
        run_etl_model(point_layer, out_layer=test_layer_3d)
        print("Info: Validating geometry PointZ...", test_layer_3d.wkbType())
        self.assertEqual(QgsWkbTypes.PointGeometry, test_layer_3d.type())
        self.assertIn(point_layer.wkbType(), [QgsWkbTypes.PointZ, QgsWkbTypes.Point25D])
        self.assertEqual(QgsWkbTypes.PointZ, test_layer_3d.wkbType())
        self.assertEqual(test_layer_3d.featureCount(), 51)
        clean_table('test_ladm_col_3d', BOUNDARY_POINT_TABLE)
        test_layer_3d.dataProvider().truncate()

        # PointM To PointZ
        print("Validating PointM To PointZ")
        uri = self.gpkg_path + '|layername={layername}'.format(layername='points_M')
        point_layer = QgsVectorLayer(uri, 'points', 'ogr')
        run_etl_model(point_layer, out_layer=test_layer_3d)
        print("Info: Validating geometry PointZ...", test_layer_3d.wkbType())
        self.assertEqual(QgsWkbTypes.PointGeometry, test_layer_3d.type())
        self.assertEqual(QgsWkbTypes.PointM, point_layer.wkbType())
        self.assertEqual(QgsWkbTypes.PointZ, test_layer_3d.wkbType())
        self.assertEqual(test_layer_3d.featureCount(), 51)
        clean_table('test_ladm_col_3d', BOUNDARY_POINT_TABLE)
        test_layer_3d.dataProvider().truncate()

        # PointZM To PointZ
        print("Validating PointZM To PointZ")
        uri = self.gpkg_path + '|layername={layername}'.format(layername='points_ZM')
        point_layer = QgsVectorLayer(uri, 'points', 'ogr')
        run_etl_model(point_layer, out_layer=test_layer_3d)
        print("Info: Validating geometry PointZ...", test_layer_3d.wkbType())
        self.assertEqual(QgsWkbTypes.PointGeometry, test_layer_3d.type())
        self.assertEqual(QgsWkbTypes.PointZM, point_layer.wkbType())
        self.assertEqual(QgsWkbTypes.PointZ, test_layer_3d.wkbType())
        self.assertEqual(test_layer_3d.featureCount(), 51)
        clean_table('test_ladm_col_3d', BOUNDARY_POINT_TABLE)
        test_layer_3d.dataProvider().truncate()

    def test_valid_import_geom_2d_to_db_postgres(self):
        print('\nINFO: Validating ETL-Model from [ Point, PointZ, PointM, PointZM ] to Point (Postgres) geometries...')
        print('\nUSING POSTGRESQL SCHEMA')

        test_layer = self.qgis_utils.get_layer(self.db_connection, BOUNDARY_POINT_TABLE, load=True)

        # Point To Point
        print("Validating Point to Point")
        point_layer = self.qgis_utils.get_layer(self.test_connection, 'points', load=True)
        print("Is Valid layer :", point_layer.isValid())
        run_etl_model(point_layer, out_layer=test_layer)
        test_layer.startEditing()
        print("Info: Validating geometry Point...")
        self.assertEqual(QgsWkbTypes.PointGeometry, test_layer.type())
        self.assertEqual(QgsWkbTypes.Point, test_layer.wkbType())
        self.assertEqual(test_layer.featureCount(), 51)

        # PointZ To Point
        print("Validating PointZ to Point")
        point_layer = self.qgis_utils.get_layer(self.test_connection, 'points_z', load=True)
        print("Is Valid layer :", point_layer.isValid())
        self.assertIn(point_layer.wkbType(), [QgsWkbTypes.PointZ, QgsWkbTypes.Point25D])
        run_etl_model(point_layer, out_layer=test_layer)
        print("Info: Validating geometry PointZ...", test_layer.wkbType())
        self.assertEqual(QgsWkbTypes.PointGeometry, test_layer.type())
        self.assertEqual(QgsWkbTypes.Point, test_layer.wkbType())
        self.assertEqual(test_layer.featureCount(), 51)

        # PointM To Point
        print("Validating PointM To Point")
        point_layer = self.qgis_utils.get_layer(self.test_connection, 'points_m', load=True)
        print("Is Valid layer :", point_layer.isValid())
        run_etl_model(point_layer, out_layer=test_layer)
        print("Info: Validating geometry PointZ...", test_layer.wkbType())
        self.assertEqual(QgsWkbTypes.PointGeometry, test_layer.type())
        self.assertEqual(QgsWkbTypes.PointM, point_layer.wkbType())
        self.assertEqual(QgsWkbTypes.Point, test_layer.wkbType())
        self.assertEqual(test_layer.featureCount(), 51)

        # PointZM To Point
        print("Validating PointZM To Point")
        point_layer = self.qgis_utils.get_layer(self.test_connection, 'points_zm', load=True)
        print("Is Valid layer :", point_layer.isValid())
        run_etl_model(point_layer, out_layer=test_layer)
        print("Info: Validating geometry PointZ...", test_layer.wkbType())
        self.assertEqual(QgsWkbTypes.PointGeometry, test_layer.type())
        self.assertEqual(QgsWkbTypes.PointZM, point_layer.wkbType())
        self.assertEqual(QgsWkbTypes.Point, test_layer.wkbType())
        self.assertEqual(test_layer.featureCount(), 51)

    def test_valid_import_geom_3d_to_db_postgres(self):
        print('\nINFO: Validating ETL-Model from [ Point, PointZ, PointM, PointZM ] to PointZ (Postgres) geometries...')

        test_layer_3d = self.qgis_utils.get_layer(self.db_connection_3d, BOUNDARY_POINT_TABLE, load=True)
        test_layer_3d.startEditing()

        # Point To PointZ
        print("Validating Point to PointZ")
        point_layer = self.qgis_utils.get_layer(self.test_connection, 'points', load=True)
        run_etl_model(point_layer, out_layer=test_layer_3d)
        print("Info: Validating geometry Point...")
        self.assertEqual(QgsWkbTypes.PointGeometry, test_layer_3d.type())
        self.assertEqual(QgsWkbTypes.Point, point_layer.wkbType())
        self.assertEqual(QgsWkbTypes.PointZ, test_layer_3d.wkbType())
        self.assertEqual(test_layer_3d.featureCount(), 51)

        # PointZ To PointZ
        print("Validating PointZ to PointZ")
        point_layer = self.qgis_utils.get_layer(self.test_connection, 'points_z', load=True)
        run_etl_model(point_layer, out_layer=test_layer_3d)
        print("Info: Validating geometry PointZ...", test_layer_3d.wkbType())
        self.assertEqual(QgsWkbTypes.PointGeometry, test_layer_3d.type())
        self.assertIn(point_layer.wkbType(), [QgsWkbTypes.PointZ, QgsWkbTypes.Point25D])
        self.assertEqual(QgsWkbTypes.PointZ, test_layer_3d.wkbType())
        self.assertEqual(test_layer_3d.featureCount(), 51)

        # PointM To PointZ
        print("Validating PointM To PointZ")
        point_layer = self.qgis_utils.get_layer(self.test_connection, 'points_m', load=True)
        run_etl_model(point_layer, out_layer=test_layer_3d)
        print("Info: Validating geometry PointZ...", test_layer_3d.wkbType())
        self.assertEqual(QgsWkbTypes.PointGeometry, test_layer_3d.type())
        self.assertEqual(QgsWkbTypes.PointM, point_layer.wkbType())
        self.assertEqual(QgsWkbTypes.PointZ, test_layer_3d.wkbType())
        self.assertEqual(test_layer_3d.featureCount(), 51)

        # PointZM To PointZ
        print("Validating PointZM To PointZ")
        point_layer = self.qgis_utils.get_layer(self.test_connection, 'points_zm', load=True)
        run_etl_model(point_layer, out_layer=test_layer_3d)
        print("Info: Validating geometry PointZ...", test_layer_3d.wkbType())
        self.assertEqual(QgsWkbTypes.PointGeometry, test_layer_3d.type())
        self.assertEqual(QgsWkbTypes.PointZM, point_layer.wkbType())
        self.assertEqual(QgsWkbTypes.PointZ, test_layer_3d.wkbType())
        self.assertEqual(test_layer_3d.featureCount(), 51)

    @classmethod
    def tearDownClass(self):
        print('tearDown test_change_geometries_in_load')

if __name__ == '__main__':
    nose2.main()
