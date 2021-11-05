import nose2

from qgis.testing import (start_app,
                          unittest)

from asistente_ladm_col.app_interface import AppInterface

start_app()  # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.lib.model_registry import LADMColModelRegistry
from asistente_ladm_col.config.ladm_names import LADMNames
from asistente_ladm_col.logic.ladm_col.ladm_data import LADMData
from asistente_ladm_col.tests.utils import (normalize_response,
                                            restore_pg_db,
                                            get_test_path,
                                            standardize_query_results,
                                            get_field_values_by_key_values,
                                            import_qgis_model_baker,
                                            unload_qgis_model_baker)

from asistente_ladm_col.tests.resources.expected_results.change_detections.collected.parcel_data_to_compare_changes_all_data import parcel_data_to_compare_changes_all_data
from asistente_ladm_col.tests.resources.expected_results.change_detections.collected.parcel_data_to_compare_changes_parcel_number_253940000000000230055000000000 import parcel_data_to_compare_changes_parcel_number_253940000000000230055000000000
from asistente_ladm_col.tests.resources.expected_results.change_detections.collected.parcel_data_to_compare_changes_parcel_number_253940000000000230241000000000 import parcel_data_to_compare_changes_parcel_number_253940000000000230241000000000


class TestChangeDetectionsCollected(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("INFO: Restoring databases to be used")
        import_qgis_model_baker()

        schema = 'test_ladm_col_queries'
        models = [LADMColModelRegistry().model(LADMNames.LADM_COL_MODEL_KEY).full_name(),
                  LADMColModelRegistry().model(LADMNames.SNR_DATA_SUPPLIES_MODEL_KEY).full_name(),
                  LADMColModelRegistry().model(LADMNames.SUPPLIES_MODEL_KEY).full_name(),
                  LADMColModelRegistry().model(LADMNames.SUPPLIES_INTEGRATION_MODEL_KEY).full_name(),
                  LADMColModelRegistry().model(LADMNames.SURVEY_MODEL_KEY).full_name()]
        cls.db_pg = restore_pg_db(schema, models, get_test_path("db/ladm/test_ladm_col_queries_v1_1.xtf"), True)
        res, code, msg = cls.db_pg.test_connection()
        cls.assertTrue(res, msg)

        cls.app = AppInterface()
        cls.ladm_data = LADMData()
        cls.names = cls.db_pg.names

    def get_test_plots_and_parcels(self):
        layers = {
            self.names.LC_PLOT_T: None,
            self.names.LC_PARCEL_T: None
        }
        self.app.core.get_layers(self.db_pg, layers, load=True)
        self.assertIsNotNone(layers, 'An error occurred while trying to get the layers of interest')

        # The t_ili_tid field is used instead of t_id which does not change every time a backup is generated
        parcel_ids_tests = [list(),
                            get_field_values_by_key_values(layers[self.names.LC_PARCEL_T], self.names.T_ILI_TID_F,
                                                           ['4649c6d1-0882-45c8-a8a9-e278d26ac8dd'],
                                                           self.names.T_ID_F),
                            get_field_values_by_key_values(layers[self.names.LC_PARCEL_T], self.names.T_ILI_TID_F,
                                                           ['37dd793e-8e9f-4825-9592-d9a8aee80d24',
                                                               '4649c6d1-0882-45c8-a8a9-e278d26ac8dd',
                                                               'ac853cd5-88ec-481b-96b8-dda61b6bde3f'],
                                                           self.names.T_ID_F)]

        plot_ids_tests = [list(),
                          get_field_values_by_key_values(layers[self.names.LC_PLOT_T], self.names.T_ILI_TID_F,
                                                         ['45bf5b96-d34e-4f5f-827e-eb5469784772'],
                                                         self.names.T_ID_F),
                          get_field_values_by_key_values(layers[self.names.LC_PLOT_T], self.names.T_ILI_TID_F,
                                                         ['e21e18a4-7bce-4d0e-8c49-94b2d3321c8a',
                                                             '45bf5b96-d34e-4f5f-827e-eb5469784772',
                                                             '81c4e87a-99a0-4c6b-a44c-1b7795f93014'],
                                                         self.names.T_ID_F)]
        return plot_ids_tests, parcel_ids_tests

    def test_get_plots_related_to_parcels(self):
        print("\nINFO: Validating get plots related to parcels (Case: t_id)...")

        plot_ids_tests, parcel_ids_tests = self.get_test_plots_and_parcels()

        count = 0
        for parcel_ids_test in parcel_ids_tests:
            plot_ids = self.ladm_data.get_plots_related_to_parcels(self.db_pg, parcel_ids_test, self.names.T_ID_F)
            # We use assertCountEqual to compare if two lists are the same regardless of the order of their elements.
            # https://docs.python.org/3.2/library/unittest.html#unittest.TestCase.assertCountEqual
            self.assertCountEqual(plot_ids, plot_ids_tests[count], "Failure with data set {}".format(count + 1))
            count += 1

        print("\nINFO: Validating get plots related to parcels (Case: custom field)...")
        plot_custom_field_ids_tests = [list(), [49379], [2614.3, 49379, 59108.5]]

        count = 0
        for parcel_ids_test in parcel_ids_tests:
            plot_custom_field_ids = self.ladm_data.get_plots_related_to_parcels(self.db_pg, parcel_ids_test, self.names.LC_PLOT_T_PLOT_AREA_F)
            self.assertCountEqual(plot_custom_field_ids, plot_custom_field_ids_tests[count], "Failure with data set {}".format(count + 1))
            count += 1

        print("\nINFO: Validating get plots related to parcels (Case: t_id) with preloaded tables...")

        layers = {
            self.names.LC_PLOT_T: None,
            self.names.COL_UE_BAUNIT_T: None
        }
        self.app.core.get_layers(self.db_pg, layers, load=True)
        self.assertIsNotNone(layers, 'An error occurred while trying to get the layers of interest')

        count = 0
        for parcel_ids_test in parcel_ids_tests:
            plot_ids = self.ladm_data.get_plots_related_to_parcels(self.db_pg,
                                                                   parcel_ids_test,
                                                                   self.names.T_ID_F,
                                                                   plot_layer=layers[self.names.LC_PLOT_T],
                                                                   uebaunit_table=layers[self.names.COL_UE_BAUNIT_T])
            self.assertCountEqual(plot_ids, plot_ids_tests[count], "Failure with data set {}".format(count + 1))
            count += 1

    def test_get_parcels_related_to_plots(self):
        print("\nINFO: Validating get parcels related to plots (Case: t_id)...")

        plot_ids_tests, parcel_ids_tests = self.get_test_plots_and_parcels()

        count = 0
        for plot_ids_test in plot_ids_tests:
            parcel_ids = self.ladm_data.get_parcels_related_to_plots(self.db_pg, plot_ids_test, self.names.T_ID_F)
            # We use assertCountEqual to compare if two lists are the same regardless of the order of their elements.
            # https://docs.python.org/3.2/library/unittest.html#unittest.TestCase.assertCountEqual
            self.assertCountEqual(parcel_ids, parcel_ids_tests[count], "Failure with data set {}".format(count + 1))
            count += 1

        print("\nINFO: Validating get parcels related to plots (Case: custom field)...")
        parcel_custom_field_ids_tests = [list(),
                                         ['253940000000000230054000000000'],
                                         ['253940000000000230241000000000', '253940000000000230054000000000', '253940000000000230254000000000']]

        count = 0
        for plot_ids_test in plot_ids_tests:
            parcel_custom_field_ids = self.ladm_data.get_parcels_related_to_plots(self.db_pg,
                                                                                  plot_ids_test,
                                                                                  self.names.LC_PARCEL_T_PARCEL_NUMBER_F)
            self.assertCountEqual(parcel_custom_field_ids, parcel_custom_field_ids_tests[count],
                                  "Failure with data set {}".format(count + 1))
            count += 1

        print("\nINFO: Validating get parcels related to plots (Case: t_id) with preloaded tables...")

        layers = {
            self.names.LC_PARCEL_T: None,
            self.names.COL_UE_BAUNIT_T: None
        }
        self.app.core.get_layers(self.db_pg, layers, load=True)
        self.assertIsNotNone(layers, 'An error occurred while trying to get the layers of interest')

        count = 0
        for plot_ids_test in plot_ids_tests:
            parcel_ids = self.ladm_data.get_parcels_related_to_plots(self.db_pg,
                                                                     plot_ids_test,
                                                                     self.names.T_ID_F,
                                                                     parcel_table=layers[self.names.LC_PARCEL_T],
                                                                     uebaunit_table=layers[self.names.COL_UE_BAUNIT_T])
            self.assertCountEqual(parcel_ids, parcel_ids_tests[count], "Failure with data set {}".format(count + 1))
            count += 1

    def test_get_parcel_data_to_compare_changes(self):
        print("\nINFO: Validating get parcels data ...")
        features_test = parcel_data_to_compare_changes_all_data
        features = self.ladm_data.get_parcel_data_to_compare_changes(self.db_pg)
        normalize_response(features)
        standardize_query_results(features, key_to_remove="t_id")
        self.assertEqual(features, features_test)

        print("\nINFO: Validating get parcels data using search criterion...")
        features_test = parcel_data_to_compare_changes_parcel_number_253940000000000230055000000000
        search_criterion = {self.names.LC_PARCEL_T_PARCEL_NUMBER_F: '253940000000000230055000000000'}
        features = self.ladm_data.get_parcel_data_to_compare_changes(self.db_pg, search_criterion=search_criterion)
        normalize_response(features)
        standardize_query_results(features, key_to_remove="t_id")
        self.assertEqual(features, features_test)

        print("\nINFO: Validating get parcels data using search criterion...")
        features_test = parcel_data_to_compare_changes_parcel_number_253940000000000230241000000000
        search_criterion = {self.names.LC_PARCEL_T_PARCEL_NUMBER_F: '253940000000000230241000000000'}
        features = self.ladm_data.get_parcel_data_to_compare_changes(self.db_pg, search_criterion=search_criterion)
        normalize_response(features)
        standardize_query_results(features, key_to_remove="t_id")
        self.assertEqual(features, features_test)

    @classmethod
    def tearDownClass(cls):
        print("\nINFO: Closing open connections to databases")
        cls.db_pg.conn.close()
        unload_qgis_model_baker()


if __name__ == '__main__':
    nose2.main()
