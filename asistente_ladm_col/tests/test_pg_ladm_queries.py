import nose2

from qgis.testing import (start_app,
                          unittest)

start_app() # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.tests.utils import (get_pg_conn,
                                            standardize_query_results,
                                            restore_schema)
from asistente_ladm_col.tests.resources.expected_results.queries.ladm_basic_query_test_results import expected_result_ladm_basic_query
from asistente_ladm_col.tests.resources.expected_results.queries.ladm_economic_query_test_results import expected_result_ladm_economic_query
from asistente_ladm_col.tests.resources.expected_results.queries.ladm_legal_query_test_results import expected_result_ladm_legal_query
from asistente_ladm_col.tests.resources.expected_results.queries.ladm_physical_query_test_results import expected_result_ladm_physical_query
from asistente_ladm_col.tests.resources.expected_results.queries.ladm_property_record_card_query_test_results import expected_result_ladm_property_record_card_query
from asistente_ladm_col.logic.ladm_col.pg_ladm_query import PGLADMQuery


class TestPGLADMQueries(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("INFO: Restoring databases to be used")
        restore_schema('test_ladm_col_queries')
        cls.db_pg = get_pg_conn('test_ladm_col_queries')

        cls.ladm_queries = PGLADMQuery()

        # Standardize query results: id's are removed because it depends on the database test data
        standardize_query_results(expected_result_ladm_basic_query.copy())
        standardize_query_results(expected_result_ladm_economic_query.copy())
        standardize_query_results(expected_result_ladm_legal_query.copy())
        standardize_query_results(expected_result_ladm_physical_query.copy())
        standardize_query_results(expected_result_ladm_property_record_card_query.copy())

    def test_igac_basic_info_query(self):
        print("\nINFO: Validating basic info query from IGAC...")

        res, code, msg = self.db_pg.test_connection()
        self.assertTrue(res, msg)

        kwargs = {'plot_t_ids': [1430]}
        result = standardize_query_results(self.ladm_queries.get_igac_basic_info(self.db_pg, **kwargs))
        self.assertTrue(expected_result_ladm_basic_query == result, 'The result obtained is not as expected: {} {}'.format(expected_result_ladm_basic_query, result))

    def test_igac_legal_info_query(self):
        print("\nINFO: Validating legal info query from IGAC...")

        kwargs = {'plot_t_ids': [1430]}
        result = standardize_query_results(self.ladm_queries.get_igac_legal_info(self.db_pg, **kwargs))
        self.assertTrue(expected_result_ladm_legal_query == result, 'The result obtained is not as expected: {} {}'.format(expected_result_ladm_legal_query, result))

    def test_igac_property_record_card_info_query(self):
        print("\nINFO: Validating property record card info query from IGAC...")

        kwargs = {'plot_t_ids': [1430]}
        result = standardize_query_results(self.ladm_queries.get_igac_property_record_card_info(self.db_pg, **kwargs))
        self.assertTrue(expected_result_ladm_property_record_card_query == result, 'The result obtained is not as expected: {} {}'.format(expected_result_ladm_property_record_card_query, result))

    def test_igac_physical_info_query(self):
        print("\nINFO: Validating physical info query from IGAC...")

        kwargs = {'plot_t_ids': [1430]}
        result = standardize_query_results(self.ladm_queries.get_igac_physical_info(self.db_pg, **kwargs))
        self.assertTrue(expected_result_ladm_physical_query == result, 'The result obtained is not as expected: {} {}'.format(expected_result_ladm_physical_query, result))

    def test_igac_economic_info_query(self):
        print("\nINFO: Validating economic info query from IGAC...")

        kwargs = {'plot_t_ids': [1430]}
        result = standardize_query_results(self.ladm_queries.get_igac_economic_info(self.db_pg, **kwargs))
        self.assertTrue(expected_result_ladm_economic_query == result, 'The result obtained is not as expected: {} {}'.format(expected_result_ladm_economic_query, result))

    @classmethod
    def tearDownClass(cls):
        print("INFO: Closing open connections to databases")
        cls.db_pg.conn.close()


if __name__ == '__main__':
    nose2.main()

