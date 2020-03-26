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

        result_empty = cls.db_gpkg_empty.test_connection()
        result_test = cls.db_gpkg_test.test_connection()
        cls.assertTrue(result_empty[0], 'The test connection is not working for empty db')
        cls.assertTrue(result_test[0], 'The test connection is not working for test data db')

    def test_refactor_field(self):
        print('\nINFO: Validating refactor field for boundary layer ...')

        dict_layers_to_check = {
            self.db_gpkg_test.names.OP_BOUNDARY_T: self.db_gpkg_empty.names.OP_BOUNDARY_T,
            self.db_gpkg_test.names.OP_PLOT_T: self.db_gpkg_empty.names.OP_PLOT_T,
            self.db_gpkg_test.names.OP_PARCEL_T: self.db_gpkg_empty.names.OP_PARCEL_T,
            self.db_gpkg_test.names.OP_BOUNDARY_POINT_T: self.db_gpkg_empty.names.OP_BOUNDARY_POINT_T,
            self.db_gpkg_test.names.OP_CONTROL_POINT_T: self.db_gpkg_empty.names.OP_CONTROL_POINT_T,
            self.db_gpkg_test.names.OP_SURVEY_POINT_T: self.db_gpkg_empty.names.OP_SURVEY_POINT_T,
            self.db_gpkg_test.names.OP_PARTY_T: self.db_gpkg_empty.names.OP_PARTY_T,
            self.db_gpkg_test.names.OP_ADMINISTRATIVE_SOURCE_T: self.db_gpkg_empty.names.OP_ADMINISTRATIVE_SOURCE_T,
            self.db_gpkg_test.names.OP_BUILDING_T: self.db_gpkg_empty.names.OP_BUILDING_T,
            self.db_gpkg_test.names.OP_BUILDING_UNIT_T: self.db_gpkg_empty.names.OP_BUILDING_UNIT_T
        }

        feature_count_test = {
            self.db_gpkg_test.names.OP_BOUNDARY_T: 154,
            self.db_gpkg_test.names.OP_PLOT_T: 52,
            self.db_gpkg_test.names.OP_PARCEL_T: 51,
            self.db_gpkg_test.names.OP_BOUNDARY_POINT_T: 390,
            self.db_gpkg_test.names.OP_CONTROL_POINT_T: 0,
            self.db_gpkg_test.names.OP_SURVEY_POINT_T: 53,
            self.db_gpkg_test.names.OP_PARTY_T: 36,
            self.db_gpkg_test.names.OP_ADMINISTRATIVE_SOURCE_T: 50,
            self.db_gpkg_test.names.OP_BUILDING_T: 17,
            self.db_gpkg_test.names.OP_BUILDING_UNIT_T: 29
        }

        for layer_name_test, layer_name_empty in dict_layers_to_check.items():
            layer = self.qgis_utils.get_layer(self.db_gpkg_test, layer_name_test, load=True)
            test_layer = self.qgis_utils.get_layer(self.db_gpkg_empty, layer_name_empty, load=True)
            self.assertEqual(layer.featureCount(), feature_count_test[layer_name_test], 'Error in {}'.format(layer_name_test))
            self.assertEqual(test_layer.featureCount(), 0, 'Error in {}'.format(layer_name_test))

            print("Import data from test db to empty db for {} using refactor fields".format(layer_name_test))
            run_etl_model(self.db_gpkg_empty.names, layer, test_layer, layer_name_empty)
            self.assertEqual(test_layer.featureCount(), feature_count_test[layer_name_test], 'Error in {}'.format(layer_name_test))

    @classmethod
    def tearDownClass(cls):
        print("INFO: Closing open connections to databases")
        cls.db_gpkg_empty.conn.close()
        cls.db_gpkg_test.conn.close()
        unload_qgis_model_baker()


if __name__ == '__main__':
    nose2.main()
