import nose2

from qgis import utils
from qgis.core import QgsExpression
from qgis.testing import (unittest,
                          start_app)

start_app() # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.tests.utils import (get_field_values_by_key_values,
                                            restore_gpkg_db,
                                            get_test_path,
                                            standardize_query_results,
                                            import_asistente_ladm_col,
                                            import_qgis_model_baker,
                                            unload_qgis_model_baker,
                                            import_processing)
from asistente_ladm_col.logic.ladm_col.qgis_ladm_query import QGISLADMQuery
from asistente_ladm_col.lib.model_registry import LADMColModelRegistry
from asistente_ladm_col.config.ladm_names import LADMNames

from asistente_ladm_col.tests.resources.expected_results.queries.ladm_basic_query_test_results import expected_result_ladm_basic_query
from asistente_ladm_col.tests.resources.expected_results.queries.ladm_legal_query_test_results import expected_result_ladm_legal_query
from asistente_ladm_col.tests.resources.expected_results.queries.ladm_physical_query_test_results import expected_result_ladm_physical_query
from asistente_ladm_col.tests.resources.expected_results.queries.ladm_economic_query_test_results import expected_result_ladm_economic_query
from asistente_ladm_col.tests.resources.expected_results.queries.ladm_property_record_card_query_test_results import expected_result_ladm_property_record_card_query
from asistente_ladm_col.config.expression_functions import (get_domain_code_from_value,
                                                            get_domain_value_from_code)


class TestGPKGLADMQueries(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        import_processing()
        import_asistente_ladm_col() # Import plugin
        import_qgis_model_baker()
        models = [LADMColModelRegistry().model(LADMNames.LADM_COL_MODEL_KEY).full_name(),
                  LADMColModelRegistry().model(LADMNames.SNR_DATA_SUPPLIES_MODEL_KEY).full_name(),
                  LADMColModelRegistry().model(LADMNames.SUPPLIES_MODEL_KEY).full_name(),
                  LADMColModelRegistry().model(LADMNames.SUPPLIES_INTEGRATION_MODEL_KEY).full_name(),
                  LADMColModelRegistry().model(LADMNames.SURVEY_MODEL_KEY).full_name()]
        cls.db_gpkg = restore_gpkg_db(models, get_test_path("db/ladm/test_ladm_col_queries_v1_1.xtf"), True)

        # We can't use the restored database connection because the expression functions use the one in the plugin;
        # that's why we have to get the database connection and assign it to the plugin
        cls.plugin = utils.plugins["asistente_ladm_col"]  # Dict of active plugins
        cls.conn_manager = cls.plugin.conn_manager
        cls.conn_manager.set_db_connector_for_source(cls.db_gpkg)

        res, code, msg = cls.db_gpkg.test_connection()
        cls.assertTrue(res, msg)
        cls.assertIsNotNone(cls.db_gpkg.names.T_ID_F, 'Names is None')
        cls.ladm_queries = QGISLADMQuery()

        # Maybe custom expression functions are not register in processing module
        QgsExpression.registerFunction(get_domain_code_from_value)
        QgsExpression.registerFunction(get_domain_value_from_code)

        # Plots to be consulted are defined
        layers = {
            cls.db_gpkg.names.LC_PLOT_T: None
        }
        cls.plugin.app.core.get_layers(cls.db_gpkg, layers, load=True)
        cls.test_plot_t_ids = get_field_values_by_key_values(layers[cls.db_gpkg.names.LC_PLOT_T],
                                                             cls.db_gpkg.names.T_ILI_TID_F,
                                                             ['fc68c492-fad5-4a7b-98a3-6104e84a4ec4'],
                                                             cls.db_gpkg.names.T_ID_F)

    def test_ladm_queries_igac_basic_query(self):
        print("\nINFO: Validating basic info query from IGAC...")

        # Empty result
        kwargs = {'plot_t_ids': [-1]}
        self.assertEqual(self.ladm_queries.get_igac_basic_info(self.db_gpkg, **kwargs), {'lc_terreno': []})

        kwargs = {'plot_t_ids': self.test_plot_t_ids}
        result = standardize_query_results(self.ladm_queries.get_igac_basic_info(self.db_gpkg, **kwargs))
        self.assertTrue(expected_result_ladm_basic_query == result, 'The result obtained is not as expected: {} {}'.format(expected_result_ladm_basic_query, result))

    def test_ladm_queries_igac_legal_query(self):
        print("\nINFO: Validating legal info query from IGAC...")

        # Empty result
        kwargs = {'plot_t_ids': [-1]}
        self.assertEqual(self.ladm_queries.get_igac_legal_info(self.db_gpkg, **kwargs), {'lc_terreno': []})

        kwargs = {'plot_t_ids': self.test_plot_t_ids}
        result = standardize_query_results(self.ladm_queries.get_igac_legal_info(self.db_gpkg, **kwargs))
        self.assertTrue(expected_result_ladm_legal_query == result, 'The result obtained is not as expected: {} {}'.format(expected_result_ladm_legal_query, result))

    def test_ladm_queries_igac_property_record_card_query(self):
        print("\nINFO: Validating property record card info query from IGAC...")

        # Empty result
        kwargs = {'plot_t_ids': [-1]}
        self.assertEqual(self.ladm_queries.get_igac_property_record_card_info(self.db_gpkg, **kwargs), {'lc_terreno': []})

        kwargs = {'plot_t_ids': self.test_plot_t_ids}
        result = standardize_query_results(self.ladm_queries.get_igac_property_record_card_info(self.db_gpkg, **kwargs))
        self.assertTrue(expected_result_ladm_property_record_card_query == result, 'The result obtained is not as expected: {} {}'.format(expected_result_ladm_property_record_card_query, result))

    def test_ladm_queries_igac_physical_query(self):
        print("\nINFO: Validating physical info query from IGAC...")

        # Empty result
        kwargs = {'plot_t_ids': [-1]}
        self.assertEqual(self.ladm_queries.get_igac_physical_info(self.db_gpkg, **kwargs), {'lc_terreno': []})

        kwargs = {'plot_t_ids': self.test_plot_t_ids}
        result = standardize_query_results(self.ladm_queries.get_igac_physical_info(self.db_gpkg, **kwargs))
        self.assertTrue(expected_result_ladm_physical_query == result, 'The result obtained is not as expected: {} {}'.format(expected_result_ladm_physical_query, result))

    def test_ladm_queries_ladm_economic_query(self):
        print("\nINFO: Validating economic info query from IGAC...")

        # Empty result
        kwargs = {'plot_t_ids': [-1]}
        self.assertEqual(self.ladm_queries.get_igac_economic_info(self.db_gpkg, **kwargs), {'lc_terreno': []})

        kwargs = {'plot_t_ids': self.test_plot_t_ids}
        result = standardize_query_results(self.ladm_queries.get_igac_economic_info(self.db_gpkg, **kwargs))
        self.assertTrue(expected_result_ladm_economic_query == result, 'The result obtained is not as expected: {} {}'.format(expected_result_ladm_economic_query, result))

    @classmethod
    def tearDownClass(cls):
        print('Closing connection and unloading Model Baker...')
        cls.db_gpkg.conn.close()
        unload_qgis_model_baker()


if __name__ == '__main__':
    nose2.main()
