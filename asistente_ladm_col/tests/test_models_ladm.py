import nose2

from qgis.testing import (start_app,
                          unittest)

start_app() # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.tests.utils import (get_dbconn,
                                            restore_schema)
class TestQueries(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        self.schemas_db = {'test_ladm_operation_model': None,
                           'test_ladm_valuation_model': None,
                           'test_ladm_cadastral_form_model': None}

        for name_schema, value in self.schemas_db.items():
            restore_schema(name_schema)

            self.schemas_db[name_schema] = get_dbconn(name_schema)
            result = self.schemas_db[name_schema].test_connection()
            print('test_connection', result)

            if not result[1]:
                print('The test connection is not working')
                return

    def test_operation_model(self):
        print("\nINFO: Validate if the schema has the operating model...")
        self.assertFalse(self.schemas_db['test_ladm_operation_model'].valuation_model_exists())
        self.assertFalse(self.schemas_db['test_ladm_operation_model'].cadastral_form_model_exists())

    def test_valuation_model(self):
        print("\nINFO: Validate if the schema has the valuation model...")
        self.assertTrue(self.schemas_db['test_ladm_valuation_model'].valuation_model_exists())
        self.assertFalse(self.schemas_db['test_ladm_valuation_model'].cadastral_form_model_exists())

    def test_cadastral_form_model(self):
        print("\nINFO: Validate if the schema has the cadastral form model...")
        self.assertFalse(self.schemas_db['test_ladm_cadastral_form_model'].valuation_model_exists())
        self.assertTrue(self.schemas_db['test_ladm_cadastral_form_model'].cadastral_form_model_exists())

    def tearDownClass():
        print('tearDown test_queries')


if __name__ == '__main__':
    nose2.main()

