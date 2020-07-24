import nose2

from qgis.core import (QgsVectorLayer,
                       QgsWkbTypes)
from qgis.testing import (unittest,
                          start_app)

from asistente_ladm_col.app_interface import AppInterface

start_app() # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.tests.utils import (import_qgis_model_baker,
                                            unload_qgis_model_baker,
                                            get_pg_conn,
                                            delete_features,
                                            restore_schema,
                                            run_etl_model)
from asistente_ladm_col.tests.utils import get_test_copy_path

GPKG_PATH_DISTINCT_GEOMS = 'geopackage/test_distinct_geoms_v1_0.gpkg'
SCHEMA_DISTINCT_GEOMS = 'test_distinct_geoms'
SCHEMA_LADM_COL_EMPTY = 'test_ladm_col_empty'


class TestGeomsLoad(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\nINFO: Setting up copy layer With different Geometries to DB validation...")

        cls.app = AppInterface()
        import_qgis_model_baker()

        # restore schemas
        print("INFO: Restoring databases to be used")
        restore_schema(SCHEMA_DISTINCT_GEOMS)
        restore_schema(SCHEMA_LADM_COL_EMPTY)
        cls.gpkg_path = get_test_copy_path(GPKG_PATH_DISTINCT_GEOMS)

        cls.db_distinct_geoms = get_pg_conn(SCHEMA_DISTINCT_GEOMS)
        cls.db_pg = get_pg_conn(SCHEMA_LADM_COL_EMPTY)

    def test_valid_import_geom_3d_to_db_gpkg(self):
        print('\nINFO: Validating ETL-Model from [ Point, PointZ, PointM, PointZM ] to Point geometries...')
        res, code, msg = self.db_pg.test_connection()
        self.assertTrue(res, msg)

        res, code, msg = self.db_distinct_geoms.test_connection()
        self.assertTrue(res, msg)
        self.assertIsNotNone(self.db_pg.names.LC_BOUNDARY_POINT_T, 'Names is None')

        test_layer = self.app.core.get_layer(self.db_pg, self.db_pg.names.LC_BOUNDARY_POINT_T, load=True)

        print("Validating Point to Point")
        uri = self.gpkg_path + '|layername={layername}'.format(layername='points')
        point_layer = QgsVectorLayer(uri, 'points', 'ogr')
        self.assertTrue(point_layer.isValid())
        self.assertEqual(point_layer.wkbType(), QgsWkbTypes.Point)
        run_etl_model(self.db_pg.names, point_layer, test_layer, self.db_pg.names.LC_BOUNDARY_POINT_T)
        print("Info: Validating geometry Point...")
        self.assertEqual(test_layer.wkbType(), QgsWkbTypes.PointZ)
        self.assertEqual(test_layer.featureCount(), 51)

        delete_features(test_layer)
        self.assertEqual(test_layer.featureCount(), 0)

        print("Validating PointZ to Point")
        uri = self.gpkg_path + '|layername={layername}'.format(layername='points_Z')
        point_layer = QgsVectorLayer(uri, 'points_Z', 'ogr')
        self.assertTrue(point_layer.isValid())
        self.assertIn(point_layer.wkbType(), [QgsWkbTypes.PointZ, QgsWkbTypes.Point25D])
        output = run_etl_model(self.db_pg.names, point_layer, test_layer, self.db_pg.names.LC_BOUNDARY_POINT_T)
        print("Info: Validating geometry PointZ...", test_layer.wkbType())
        self.assertEqual(test_layer.wkbType(), QgsWkbTypes.PointZ)
        self.assertEqual(test_layer.featureCount(), 51)

        delete_features(test_layer)
        self.assertEqual(test_layer.featureCount(), 0)

        print("Validating PointM To Point")
        uri = self.gpkg_path + '|layername={layername}'.format(layername='points_M')
        point_layer = QgsVectorLayer(uri, 'points', 'ogr')
        self.assertTrue(point_layer.isValid())
        self.assertEqual(point_layer.wkbType(), QgsWkbTypes.PointM)
        run_etl_model(self.db_pg.names, point_layer, test_layer, self.db_pg.names.LC_BOUNDARY_POINT_T)
        print("Info: Validating geometry PointM...", test_layer.wkbType())
        self.assertEqual(test_layer.wkbType(), QgsWkbTypes.PointZ)
        self.assertEqual(test_layer.featureCount(), 51)

        delete_features(test_layer)
        self.assertEqual(test_layer.featureCount(), 0)

        # PointZM To Point
        print("Validating PointZM To Point")
        uri = self.gpkg_path + '|layername={layername}'.format(layername='points_ZM')
        point_layer = QgsVectorLayer(uri, 'points', 'ogr')
        self.assertTrue(point_layer.isValid())
        self.assertEqual(point_layer.wkbType(), QgsWkbTypes.PointZM)
        run_etl_model(self.db_pg.names, point_layer, test_layer, self.db_pg.names.LC_BOUNDARY_POINT_T)
        print("Info: Validating geometry PointZM...", test_layer.wkbType())
        self.assertEqual(test_layer.wkbType(), QgsWkbTypes.PointZ)
        self.assertEqual(test_layer.featureCount(), 51)

        delete_features(test_layer)
        self.assertEqual(test_layer.featureCount(), 0)

    def test_valid_import_geom_3d_to_db_postgres(self):
        print('\nINFO: Validating ETL-Model from [ Point, PointZ, PointM, PointZM ] to PointZ (Postgres) geometries...')

        res, code, msg = self.db_pg.test_connection()
        self.assertTrue(res, msg)

        res, code, msg = self.db_distinct_geoms.test_connection()
        self.assertTrue(res, msg)
        self.assertIsNotNone(self.db_pg.names.LC_BOUNDARY_POINT_T, 'Names is None')

        test_layer = self.app.core.get_layer(self.db_pg, self.db_pg.names.LC_BOUNDARY_POINT_T, load=True)

        print("Validating Point to PointZ")
        point_layer = self.app.core.get_layer(self.db_distinct_geoms, 'points', load=True)
        self.assertTrue(point_layer.isValid())
        self.assertEqual(point_layer.wkbType(), QgsWkbTypes.Point)
        run_etl_model(self.db_pg.names, point_layer, test_layer, self.db_pg.names.LC_BOUNDARY_POINT_T)
        print("Info: Validating geometry Point...")
        self.assertEqual(test_layer.wkbType(), QgsWkbTypes.PointZ)
        self.assertEqual(test_layer.featureCount(), 51)

        delete_features(test_layer)
        self.assertEqual(test_layer.featureCount(), 0)

        print("Validating PointZ to PointZ")
        point_layer = self.app.core.get_layer(self.db_distinct_geoms, 'points_z', load=True)
        self.assertTrue(point_layer.isValid())
        self.assertIn(point_layer.wkbType(), [QgsWkbTypes.PointZ, QgsWkbTypes.Point25D])
        run_etl_model(self.db_pg.names, point_layer, test_layer, self.db_pg.names.LC_BOUNDARY_POINT_T)
        print("Info: Validating geometry PointZ...", test_layer.wkbType())
        self.assertEqual(test_layer.wkbType(), QgsWkbTypes.PointZ)
        self.assertEqual(test_layer.featureCount(), 51)

        delete_features(test_layer)
        self.assertEqual(test_layer.featureCount(), 0)

        print("Validating PointM To PointZ")
        point_layer = self.app.core.get_layer(self.db_distinct_geoms, 'points_m', load=True)
        self.assertTrue(point_layer.isValid())
        self.assertEqual(point_layer.wkbType(), QgsWkbTypes.PointM)
        run_etl_model(self.db_pg.names, point_layer, test_layer, self.db_pg.names.LC_BOUNDARY_POINT_T)
        print("Info: Validating geometry PointZ...", test_layer.wkbType())
        self.assertEqual(test_layer.wkbType(), QgsWkbTypes.PointZ)
        self.assertEqual(test_layer.featureCount(), 51)

        delete_features(test_layer)
        self.assertEqual(test_layer.featureCount(), 0)

        print("Validating PointZM To PointZ")
        point_layer = self.app.core.get_layer(self.db_distinct_geoms, 'points_zm', load=True)
        self.assertTrue(point_layer.isValid())
        self.assertEqual(point_layer.wkbType(), QgsWkbTypes.PointZM)
        run_etl_model(self.db_pg.names, point_layer, test_layer, self.db_pg.names.LC_BOUNDARY_POINT_T)
        print("Info: Validating geometry PointZ...", test_layer.wkbType())
        self.assertEqual(test_layer.wkbType(), QgsWkbTypes.PointZ)
        self.assertEqual(test_layer.featureCount(), 51)

        delete_features(test_layer)
        self.assertEqual(test_layer.featureCount(), 0)

    @classmethod
    def tearDownClass(cls):
        print("INFO: Closing open connections to databases")
        cls.db_distinct_geoms.conn.close()
        cls.db_pg.conn.close()
        unload_qgis_model_baker()


if __name__ == '__main__':
    nose2.main()
