import nose2

from qgis.testing import (start_app,
                          unittest)

start_app() # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.tests.utils import (get_pg_conn,
                                            restore_schema)
from asistente_ladm_col.tests.resources.expected_results.queries.basic_query_test_results import basic_query_test_results
from asistente_ladm_col.tests.resources.expected_results.queries.economic_query_test_results import economic_query_test_results
from asistente_ladm_col.tests.resources.expected_results.queries.legal_query_test_results import legal_query_test_results
from asistente_ladm_col.tests.resources.expected_results.queries.physical_query_test_results import physical_query_test_results
from asistente_ladm_col.tests.resources.expected_results.queries.property_record_card_query_test_results import property_record_card_query_test_results


class TestQueries(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("INFO: Restoring databases to be used")
        restore_schema('test_ladm_col_queries')
        cls.db_pg = get_pg_conn('test_ladm_col_queries')

    def test_igac_basic_info_query(self):
        print("\nINFO: Validating basic info query from IGAC...")

        result = self.db_pg.test_connection()
        self.assertTrue(result[0], 'The test connection is not working')

        plot_t_id = 1416
        records = self.db_pg.get_igac_basic_info(plot_t_id=plot_t_id)
        self.assertTrue(1 == len(records), 'The number of records obtained is not as expected')
        self.assertTrue(basic_query_test_results['query_by_plot_id'] == records[0]['op_terreno'], 'The result obtained is not as expected: {} {}'.format(basic_query_test_results['query_by_plot_id'], records[0]['op_terreno']))

    def test_igac_legal_info_query(self):
        print("\nINFO: Validating legal info query from IGAC...")

        plot_t_id = 1416
        records = self.db_pg.get_igac_legal_info(plot_t_id=plot_t_id)
        self.assertTrue(1 == len(records), 'The number of records obtained is not as expected')
        self.assertTrue(legal_query_test_results['query_by_plot_id'] == records[0]['op_terreno'], 'The result obtained is not as expected: {} {}'.format(legal_query_test_results['query_by_plot_id'], records[0]['op_terreno']))

    def test_igac_property_record_card_info_query(self):
        print("\nINFO: Validating property record card info query from IGAC...")

        plot_t_id = 1416
        records = self.db_pg.get_igac_property_record_card_info(plot_t_id=plot_t_id)
        self.assertTrue(1 == len(records), 'The number of records obtained is not as expected')
        self.assertTrue(property_record_card_query_test_results['query_by_plot_id'] == records[0]['op_terreno'], 'The result obtained is not as expected: {} {}'.format(property_record_card_query_test_results['query_by_plot_id'], records[0]['op_terreno']))

    def test_igac_physical_info_query(self):
        print("\nINFO: Validating physical info query from IGAC...")

        plot_t_id = 1416
        records = self.db_pg.get_igac_physical_info(plot_t_id=plot_t_id)
        self.assertTrue(1 == len(records), 'The number of records obtained is not as expected')
        self.assertTrue(physical_query_test_results['query_by_plot_id'] == records[0]['op_terreno'], 'The result obtained is not as expected: {} {}'.format(physical_query_test_results['query_by_plot_id'], records[0]['op_terreno']))

    def test_igac_economic_info_query(self):
        print("\nINFO: Validating economic info query from IGAC...")

        plot_t_id = 1416
        records = self.db_pg.get_igac_economic_info(plot_t_id=plot_t_id)
        self.assertTrue(1 == len(records), 'The number of records obtained is not as expected')
        self.assertTrue(economic_query_test_results['query_by_plot_id'] == records[0]['op_terreno'], 'The result obtained is not as expected: {} {}'.format(economic_query_test_results['query_by_plot_id'], records[0]['op_terreno']))

    @classmethod
    def tearDownClass(cls):
        print("INFO: Closing open connections to databases")
        cls.db_pg.conn.close()


if __name__ == '__main__':
    nose2.main()

