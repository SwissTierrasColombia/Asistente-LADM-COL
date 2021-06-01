import nose2

from qgis.testing import (start_app,
                          unittest)

from asistente_ladm_col.app_interface import AppInterface

start_app()  # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.logic.ladm_col.ladm_data import LADMData
from asistente_ladm_col.tests.resources.expected_results.change_detections.supplies.parcel_data_to_compare_changes_all_data import parcel_data_to_compare_changes_all_data
from asistente_ladm_col.tests.resources.expected_results.change_detections.supplies.parcel_data_to_compare_changes_parcel_number_253940000000000230099335131315 import parcel_data_to_compare_changes_parcel_number_253940000000000230099335131315
from asistente_ladm_col.tests.resources.expected_results.change_detections.supplies.parcel_data_to_compare_changes_fmi_760ab38 import parcel_data_to_compare_changes_fmi_760ab38
from asistente_ladm_col.tests.utils import (get_pg_conn,
                                            normalize_response,
                                            standardize_query_results,
                                            get_field_values_by_key_values,
                                            restore_schema,
                                            import_qgis_model_baker,
                                            unload_qgis_model_baker)


class TestChangeDetectionSupplies(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("INFO: Restoring databases to be used")
        import_qgis_model_baker()
        restore_schema('test_change_detections')
        cls.db_pg = get_pg_conn('test_change_detections')
        res, code, msg = cls.db_pg.test_connection()
        cls.assertTrue(res, msg)

        cls.app = AppInterface()
        cls.ladm_data = LADMData()

    def get_test_plots_and_parcels(self):
        layers = {
            self.db_pg.names.GC_PLOT_T: None,
            self.db_pg.names.GC_PARCEL_T: None
        }
        self.app.core.get_layers(self.db_pg, layers, load=True)
        self.assertIsNotNone(layers, 'An error occurred while trying to get the layers of interest')

        # The t_ili_tid field is used instead of t_id which does not change every time a backup is generated
        parcel_ids_tests = [list(),
                            get_field_values_by_key_values(layers[self.db_pg.names.GC_PARCEL_T], self.db_pg.names.T_ILI_TID_F,
                                                           ['93acf8d8-b486-45d3-a4a9-0b811328b360'],
                                                           self.db_pg.names.T_ID_F),
                            get_field_values_by_key_values(layers[self.db_pg.names.GC_PARCEL_T], self.db_pg.names.T_ILI_TID_F,
                                                           ['93acf8d8-b486-45d3-a4a9-0b811328b360',
                                                               '65cde01b-c4b5-456f-b4b5-40ab12012969',
                                                               '25dcb65f-6a22-4866-86ee-394ff24a15a6'],
                                                           self.db_pg.names.T_ID_F)]

        plot_ids_tests = [list(),
                          get_field_values_by_key_values(layers[self.db_pg.names.GC_PLOT_T], self.db_pg.names.T_ILI_TID_F,
                                                         ['445e7c92-028e-4e81-8956-686146f5d51a'],
                                                         self.db_pg.names.T_ID_F),
                          get_field_values_by_key_values(layers[self.db_pg.names.GC_PLOT_T], self.db_pg.names.T_ILI_TID_F,
                                                         ['445e7c92-028e-4e81-8956-686146f5d51a',
                                                             '275aa114-122f-4a90-8be8-4b895703c9e7',
                                                             'd4e1b500-9d59-4d51-96a5-d612a563fd99'],
                                                         self.db_pg.names.T_ID_F)]
        return plot_ids_tests, parcel_ids_tests

    def test_get_plots_related_to_parcels_supplies(self):
        print("\nINFO: Validating get plots related to parcels in supplies model (Case: t_id)...")

        res, code, msg = self.db_pg.test_connection()
        self.assertTrue(res, msg)
        self.assertIsNotNone(self.db_pg.names.LC_BOUNDARY_POINT_T, 'Names is None')

        plot_ids_tests, parcel_ids_tests = self.get_test_plots_and_parcels()

        count = 0
        for parcel_ids_test in parcel_ids_tests:
            plot_ids = self.ladm_data.get_plots_related_to_parcels_supplies(self.db_pg, parcel_ids_test, self.db_pg.names.T_ID_F)
            self.assertEqual(sorted(plot_ids), sorted(plot_ids_tests[count]), "Failure with data set {}".format(count + 1))
            count += 1

        print("\nINFO: Validating get plots related to parcels in supplies model (Case: custom field)...")
        plot_custom_field_ids_tests = [list(), [967.13], [967.13, 4200.03, 25178.2]]

        count = 0
        for parcel_ids_test in parcel_ids_tests:
            plot_custom_field_ids = self.ladm_data.get_plots_related_to_parcels_supplies(self.db_pg, parcel_ids_test, self.db_pg.names.GC_PLOT_T_DIGITAL_PLOT_AREA_F)
            self.assertEqual(sorted(plot_custom_field_ids), sorted(plot_custom_field_ids_tests[count]), "Failure with data set {}".format(count + 1))
            count += 1

        print("\nINFO: Validating get plots related to parcels in supplies model (Case: t_id) with preloaded tables...")

        layers = {self.db_pg.names.GC_PLOT_T: None}
        self.app.core.get_layers(self.db_pg, layers, load=True)
        self.assertIsNotNone(layers, 'An error occurred while trying to get the layers of interest')

        count = 0
        for parcel_ids_test in parcel_ids_tests:
            plot_ids = self.ladm_data.get_plots_related_to_parcels_supplies(self.db_pg,
                                                                            parcel_ids_test,
                                                                            self.db_pg.names.T_ID_F,
                                                                            gc_plot_layer=layers[self.db_pg.names.GC_PLOT_T])
            self.assertEqual(sorted(plot_ids), sorted(plot_ids_tests[count]), "Failure with data set {}".format(count + 1))
            count += 1

    def test_get_parcels_related_to_plots_supplies(self):
        print("\nINFO: Validating get parcels related to plots in supplies model (Case: t_id)...")

        plot_ids_tests, parcel_ids_tests = self.get_test_plots_and_parcels()

        count = 0
        for plot_ids_test in plot_ids_tests:
            parcel_ids = self.ladm_data.get_parcels_related_to_plots_supplies(self.db_pg, plot_ids_test, self.db_pg.names.T_ID_F)
            self.assertEqual(sorted(parcel_ids), sorted(parcel_ids_tests[count]), "Failure with data set {}".format(count + 1))
            count += 1

        print("\nINFO: Validating get parcels related to plots in supplies model (Case: custom field)...")
        parcel_custom_field_ids_tests = [list(),
                                         ['253940000000000230241000000000'],
                                         ['253940000000000230241000000000', '253940000000000230241000000994', '253940000000000230241000000995']]

        count = 0
        for plot_ids_test in plot_ids_tests:
            parcel_custom_field_ids = self.ladm_data.get_parcels_related_to_plots_supplies(self.db_pg,
                                                                                           plot_ids_test,
                                                                                           self.db_pg.names.GC_PARCEL_T_PARCEL_NUMBER_F)
            self.assertEqual(sorted(parcel_custom_field_ids), sorted(parcel_custom_field_ids_tests[count]), "Failure with data set {}".format(count + 1))
            count += 1

        print("\nINFO: Validating get parcels related to plots in supplies model (Case: t_id) with preloaded tables...")

        layers = {self.db_pg.names.GC_PARCEL_T: None}
        self.app.core.get_layers(self.db_pg, layers, load=True)
        self.assertIsNotNone(layers, 'An error occurred while trying to get the layers of interest')

        count = 0
        for plot_ids_test in plot_ids_tests:
            parcel_ids = self.ladm_data.get_parcels_related_to_plots_supplies(self.db_pg,
                                                                              plot_ids_test,
                                                                              self.db_pg.names.T_ID_F,
                                                                              gc_parcel_table=layers[self.db_pg.names.GC_PARCEL_T])
            self.assertEqual(sorted(parcel_ids), sorted(parcel_ids_tests[count]), "Failure with data set {}".format(count + 1))
            count += 1

    def test_get_parcel_data_to_compare_changes_supplies(self):
        print("\nINFO: Validating get parcels data ...")

        features_test = parcel_data_to_compare_changes_all_data
        features = self.ladm_data.get_parcel_data_to_compare_changes_supplies(self.db_pg)
        normalize_response(features)
        standardize_query_results(features, key_to_remove="t_id")
        self.assertEqual(features, features_test)

        print("\nINFO: Validating get parcels data using search criterion...")

        features_test = parcel_data_to_compare_changes_parcel_number_253940000000000230099335131315
        search_criterion = {self.db_pg.names.GC_PARCEL_T_PARCEL_NUMBER_F: '253940000000000230099335131315'}
        features = self.ladm_data.get_parcel_data_to_compare_changes_supplies(self.db_pg, search_criterion=search_criterion)
        normalize_response(features)
        standardize_query_results(features, key_to_remove="t_id")
        self.assertEqual(features, features_test)

        features_test = parcel_data_to_compare_changes_fmi_760ab38
        search_criterion = {self.db_pg.names.GC_PARCEL_T_FMI_F: '760ab38'}
        features = self.ladm_data.get_parcel_data_to_compare_changes_supplies(self.db_pg, search_criterion=search_criterion)
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
