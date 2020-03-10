import nose2

from qgis.core import (QgsVectorLayer,
                       QgsWkbTypes)
from qgis.testing import (unittest,
                          start_app)

start_app() # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.tests.utils import (import_qgis_model_baker,
                                            unload_qgis_model_baker,
                                            get_copy_gpkg_conn,
                                            get_gpkg_conn,
                                            delete_features,
                                            run_etl_model)
from asistente_ladm_col.utils.qgis_utils import QGISUtils


class TestRefactorFieldsMapping(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        import_qgis_model_baker()
        cls.db_gpkg_empty = get_copy_gpkg_conn('test_empty_ladm_gpkg')
        cls.db_gpkg_test = get_copy_gpkg_conn('test_export_data_qpkg')
        cls.qgis_utils = QGISUtils()

    def test_refactor_field_for_boundary(self):
        print('\nINFO: Validating refactor field for boundary layer ...')
        result_empty = self.db_gpkg_empty.test_connection()
        result_test = self.db_gpkg_test.test_connection()
        self.assertTrue(result_empty[0], 'The test connection is not working for empty db')
        self.assertTrue(result_test[0], 'The test connection is not working for test data db')
        self.assertIsNotNone(self.db_gpkg_empty.names.OP_BOUNDARY_T, 'Names is None')

        boundary_layer = self.qgis_utils.get_layer(self.db_gpkg_test, self.db_gpkg_test.names.OP_BOUNDARY_T, load=True)
        test_layer = self.qgis_utils.get_layer(self.db_gpkg_empty, self.db_gpkg_empty.names.OP_BOUNDARY_T, load=True)
        self.assertEqual(boundary_layer.featureCount(), 154)
        self.assertEqual(test_layer.featureCount(), 0)

        print("Import data from test db to empty db for boundary using refactor fields")
        run_etl_model(self.db_gpkg_empty.names, boundary_layer, test_layer, self.db_gpkg_empty.names.OP_BOUNDARY_POINT_T)
        self.assertEqual(test_layer.featureCount(), 154)

        delete_features(test_layer)
        self.assertEqual(test_layer.featureCount(), 0)

    @classmethod
    def tearDownClass(cls):
        print("INFO: Closing open connections to databases")
        cls.db_gpkg_empty.conn.close()
        cls.db_gpkg_test.conn.close()
        unload_qgis_model_baker()


if __name__ == '__main__':
    nose2.main()
