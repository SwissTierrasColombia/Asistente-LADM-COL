import nose2

from qgis import utils
from qgis.core import QgsExpression
from qgis.testing import (start_app,
                          unittest)

start_app() # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.app_interface import AppInterface

from asistente_ladm_col.tests.utils import (get_pg_conn,
                                            get_field_values_by_key_values,
                                            standardize_query_results,
                                            import_asistente_ladm_col,
                                            import_processing,
                                            restore_schema)
from asistente_ladm_col.tests.resources.expected_results.queries.ladm_basic_query_test_results import expected_result_ladm_basic_query
from asistente_ladm_col.tests.resources.expected_results.queries.ladm_economic_query_test_results import expected_result_ladm_economic_query
from asistente_ladm_col.tests.resources.expected_results.queries.ladm_legal_query_test_results import expected_result_ladm_legal_query
from asistente_ladm_col.tests.resources.expected_results.queries.ladm_physical_query_test_results import expected_result_ladm_physical_query
from asistente_ladm_col.tests.resources.expected_results.queries.ladm_property_record_card_query_test_results import expected_result_ladm_property_record_card_query
from asistente_ladm_col.logic.ladm_col.pg_ladm_query import PGLADMQuery
from asistente_ladm_col.config.expression_functions import (get_domain_code_from_value,
                                                            get_domain_value_from_code)

class TestPGLADMQueries(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        import_processing()
        import_asistente_ladm_col()  # Import plugin

        print("INFO: Restoring databases to be used")
        restore_schema('test_ladm_col_queries')
        cls.db_pg = get_pg_conn('test_ladm_col_queries')

        # We can't use the restored database connection because the expression functions use the one in the plugin;
        # that's why we have to get the database connection and assign it to the plugin
        cls.plugin = utils.plugins["asistente_ladm_col"]  # Dict of active plugins
        cls.conn_manager = cls.plugin.conn_manager
        cls.conn_manager.set_db_connector_for_source(cls.db_pg)

        res, code, msg = cls.db_pg.test_connection()
        cls.assertTrue(res, msg)
        cls.assertIsNotNone(cls.db_pg.names.T_ID_F, 'Names is None')
        cls.ladm_queries = PGLADMQuery()

        # Maybe custom expression functions are not register in processing module
        QgsExpression.registerFunction(get_domain_code_from_value)
        QgsExpression.registerFunction(get_domain_value_from_code)

        # Plots to be consulted are defined
        layers = {
            cls.db_pg.names.LC_PLOT_T: None
        }
        cls.plugin.app.core.get_layers(cls.db_pg, layers, load=True)
        cls.test_plot_t_ids = get_field_values_by_key_values(layers[cls.db_pg.names.LC_PLOT_T],
                                                             cls.db_pg.names.T_ILI_TID_F,
                                                             ['fc68c492-fad5-4a7b-98a3-6104e84a4ec4'],
                                                             cls.db_pg.names.T_ID_F)

    def test_igac_basic_info_query(self):
        print("\nINFO: Validating basic info query from IGAC...")

        # Empty result
        kwargs = {'plot_t_ids': [-1]}
        self.assertEqual(self.ladm_queries.get_igac_basic_info(self.db_pg, **kwargs), {'lc_terreno': []})

        kwargs = {'plot_t_ids': self.test_plot_t_ids}
        result = standardize_query_results(self.ladm_queries.get_igac_basic_info(self.db_pg, **kwargs))
        self.assertTrue(expected_result_ladm_basic_query == result, 'The result obtained is not as expected: {} {}'.format(expected_result_ladm_basic_query, result))

    def test_igac_legal_info_query(self):
        print("\nINFO: Validating legal info query from IGAC...")

        # Empty result
        kwargs = {'plot_t_ids': [-1]}
        self.assertEqual(self.ladm_queries.get_igac_legal_info(self.db_pg, **kwargs), {'lc_terreno': []})

        kwargs = {'plot_t_ids': self.test_plot_t_ids}
        result = standardize_query_results(self.ladm_queries.get_igac_legal_info(self.db_pg, **kwargs))
        self.assertTrue(expected_result_ladm_legal_query == result, 'The result obtained is not as expected: {} {}'.format(expected_result_ladm_legal_query, result))

    def test_igac_physical_info_query(self):
        print("\nINFO: Validating physical info query from IGAC...")

        # Empty result
        kwargs = {'plot_t_ids': [-1]}
        self.assertEqual(self.ladm_queries.get_igac_physical_info(self.db_pg, **kwargs), {'lc_terreno': []})

        kwargs = {'plot_t_ids': self.test_plot_t_ids}
        result = standardize_query_results(self.ladm_queries.get_igac_physical_info(self.db_pg, **kwargs))
        self.assertTrue(expected_result_ladm_physical_query == result, 'The result obtained is not as expected: {} {}'.format(expected_result_ladm_physical_query, result))

    def test_igac_economic_info_query(self):
        print("\nINFO: Validating economic info query from IGAC...")

        # Empty result
        kwargs = {'plot_t_ids': [-1]}
        self.assertEqual(self.ladm_queries.get_igac_economic_info(self.db_pg, **kwargs), {'lc_terreno': []})

        kwargs = {'plot_t_ids': self.test_plot_t_ids}
        result = standardize_query_results(self.ladm_queries.get_igac_economic_info(self.db_pg, **kwargs))
        self.assertTrue(expected_result_ladm_economic_query == result, 'The result obtained is not as expected: {} {}'.format(expected_result_ladm_economic_query, result))

    @classmethod
    def tearDownClass(cls):
        print("INFO: Closing open connections to databases")
        cls.db_pg.conn.close()


if __name__ == '__main__':
    nose2.main()

