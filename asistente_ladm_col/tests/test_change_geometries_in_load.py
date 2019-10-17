import nose2

from qgis.core import (QgsVectorLayer,
                       QgsWkbTypes)
from qgis.testing import (unittest,
                          start_app)

start_app() # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.tests.utils import (import_qgis_model_baker,
                                            get_dbconn,
                                            restore_schema,
                                            run_etl_model,
                                            clean_table)
from asistente_ladm_col.utils.qgis_utils import QGISUtils
from asistente_ladm_col.tests.utils import get_test_copy_path
from asistente_ladm_col.config.table_mapping_config import BOUNDARY_POINT_TABLE

import_qgis_model_baker()

GPKG_PATH_DISTINCT_GEOMS = 'geopackage/test_distinct_geoms_v296.gpkg'
SCHEMA_DISTINCT_GEOMS = 'test_distinct_geoms'
SCHEMA_LADM_COL_EMPTY = 'test_ladm_col_empty'


class TestGeomsLoad(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        print("\nINFO: Setting up copy layer With different Geometries to DB validation...")
        self.qgis_utils = QGISUtils()

        # resore schemas
        restore_schema(SCHEMA_DISTINCT_GEOMS)
        restore_schema(SCHEMA_LADM_COL_EMPTY)
        self.gpkg_path = get_test_copy_path(GPKG_PATH_DISTINCT_GEOMS)

        self.db_distinct_geoms = get_dbconn(SCHEMA_DISTINCT_GEOMS)
        result = self.db_distinct_geoms.test_connection()
        print('Test_connection for: '.format(SCHEMA_DISTINCT_GEOMS), result)
        if not result[1]:
            print('The test connection with  {} db is not working'.format(SCHEMA_DISTINCT_GEOMS))
            return

        self.db_connection = get_dbconn(SCHEMA_LADM_COL_EMPTY)
        result = self.db_connection.test_connection()
        print('Test_connection for: '.format(SCHEMA_LADM_COL_EMPTY), result)
        if not result[1]:
            print('The test connection with  {} db is not working'.format(SCHEMA_LADM_COL_EMPTY))
            return

        clean_table(SCHEMA_LADM_COL_EMPTY, BOUNDARY_POINT_TABLE)

    def test_valid_import_geom_3d_to_db_gpkg(self):
        print('\nINFO: Validating ETL-Model from [ Point, PointZ, PointM, PointZM ] to Point geometries...')
        test_layer = self.qgis_utils.get_layer(self.db_connection, BOUNDARY_POINT_TABLE, load=True)

        print("Validating Point to Point")
        uri = self.gpkg_path + '|layername={layername}'.format(layername='points')
        point_layer = QgsVectorLayer(uri, 'points', 'ogr')
        self.assertTrue(point_layer.isValid())
        self.assertEqual(point_layer.wkbType(), QgsWkbTypes.Point)
        run_etl_model(point_layer, out_layer=test_layer)
        print("Info: Validating geometry Point...")
        self.assertEqual(test_layer.wkbType(), QgsWkbTypes.PointZ)
        self.assertEqual(test_layer.featureCount(), 51)

        self.delete_features(test_layer)
        self.assertEqual(test_layer.featureCount(), 0)

        print("Validating PointZ to Point")
        uri = self.gpkg_path + '|layername={layername}'.format(layername='points_Z')
        point_layer = QgsVectorLayer(uri, 'points_Z', 'ogr')
        self.assertTrue(point_layer.isValid())
        self.assertIn(point_layer.wkbType(), [QgsWkbTypes.PointZ, QgsWkbTypes.Point25D])
        output = run_etl_model(point_layer, out_layer=test_layer)
        print("Info: Validating geometry PointZ...", test_layer.wkbType())
        self.assertEqual(test_layer.wkbType(), QgsWkbTypes.PointZ)
        self.assertEqual(test_layer.featureCount(), 51)

        self.delete_features(test_layer)
        self.assertEqual(test_layer.featureCount(), 0)

        print("Validating PointM To Point")
        uri = self.gpkg_path + '|layername={layername}'.format(layername='points_M')
        point_layer = QgsVectorLayer(uri, 'points', 'ogr')
        self.assertTrue(point_layer.isValid())
        self.assertEqual(point_layer.wkbType(), QgsWkbTypes.PointM)
        run_etl_model(point_layer, out_layer=test_layer)
        print("Info: Validating geometry PointM...", test_layer.wkbType())
        self.assertEqual(test_layer.wkbType(), QgsWkbTypes.PointZ)
        self.assertEqual(test_layer.featureCount(), 51)

        self.delete_features(test_layer)
        self.assertEqual(test_layer.featureCount(), 0)

        # PointZM To Point
        print("Validating PointZM To Point")
        uri = self.gpkg_path + '|layername={layername}'.format(layername='points_ZM')
        point_layer = QgsVectorLayer(uri, 'points', 'ogr')
        self.assertTrue(point_layer.isValid())
        self.assertEqual(point_layer.wkbType(), QgsWkbTypes.PointZM)
        run_etl_model(point_layer, out_layer=test_layer)
        print("Info: Validating geometry PointZM...", test_layer.wkbType())
        self.assertEqual(test_layer.wkbType(), QgsWkbTypes.PointZ)
        self.assertEqual(test_layer.featureCount(), 51)

        self.delete_features(test_layer)
        self.assertEqual(test_layer.featureCount(), 0)

    def test_valid_import_geom_3d_to_db_postgres(self):
        print('\nINFO: Validating ETL-Model from [ Point, PointZ, PointM, PointZM ] to PointZ (Postgres) geometries...')

        test_layer = self.qgis_utils.get_layer(self.db_connection, BOUNDARY_POINT_TABLE, load=True)

        print("Validating Point to PointZ")
        point_layer = self.qgis_utils.get_layer(self.db_distinct_geoms, 'points', load=True)
        self.assertTrue(point_layer.isValid())
        self.assertEqual(point_layer.wkbType(), QgsWkbTypes.Point)
        run_etl_model(point_layer, out_layer=test_layer)
        print("Info: Validating geometry Point...")
        self.assertEqual(test_layer.wkbType(), QgsWkbTypes.PointZ)
        self.assertEqual(test_layer.featureCount(), 51)

        self.delete_features(test_layer)
        self.assertEqual(test_layer.featureCount(), 0)

        print("Validating PointZ to PointZ")
        point_layer = self.qgis_utils.get_layer(self.db_distinct_geoms, 'points_z', load=True)
        self.assertTrue(point_layer.isValid())
        self.assertIn(point_layer.wkbType(), [QgsWkbTypes.PointZ, QgsWkbTypes.Point25D])
        run_etl_model(point_layer, out_layer=test_layer)
        print("Info: Validating geometry PointZ...", test_layer.wkbType())
        self.assertEqual(test_layer.wkbType(), QgsWkbTypes.PointZ)
        self.assertEqual(test_layer.featureCount(), 51)

        self.delete_features(test_layer)
        self.assertEqual(test_layer.featureCount(), 0)

        print("Validating PointM To PointZ")
        point_layer = self.qgis_utils.get_layer(self.db_distinct_geoms, 'points_m', load=True)
        self.assertTrue(point_layer.isValid())
        self.assertEqual(point_layer.wkbType(), QgsWkbTypes.PointM)
        run_etl_model(point_layer, out_layer=test_layer)
        print("Info: Validating geometry PointZ...", test_layer.wkbType())
        self.assertEqual(test_layer.wkbType(), QgsWkbTypes.PointZ)
        self.assertEqual(test_layer.featureCount(), 51)

        self.delete_features(test_layer)
        self.assertEqual(test_layer.featureCount(), 0)

        print("Validating PointZM To PointZ")
        point_layer = self.qgis_utils.get_layer(self.db_distinct_geoms, 'points_zm', load=True)
        self.assertTrue(point_layer.isValid())
        self.assertEqual(point_layer.wkbType(), QgsWkbTypes.PointZM)
        run_etl_model(point_layer, out_layer=test_layer)
        print("Info: Validating geometry PointZ...", test_layer.wkbType())
        self.assertEqual(test_layer.wkbType(), QgsWkbTypes.PointZ)
        self.assertEqual(test_layer.featureCount(), 51)

        self.delete_features(test_layer)
        self.assertEqual(test_layer.featureCount(), 0)

    def delete_features(self, layer):
        fids = [f.id() for f in layer.getFeatures()]
        return layer.dataProvider().deleteFeatures(fids)

    @classmethod
    def tearDownClass(self):
        print('tearDown test_change_geometries_in_load')

if __name__ == '__main__':
    nose2.main()
