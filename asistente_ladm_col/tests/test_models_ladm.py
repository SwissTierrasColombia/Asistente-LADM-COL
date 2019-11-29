import nose2

from qgis.testing import (start_app,
                          unittest)

start_app() # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.tests.utils import (get_dbconn,
                                            restore_schema)


class TestModelsLADM(unittest.TestCase):
    @classmethod
    def setUpClass(self):
       pass

    def test_snr_data_model(self):
        print("\nINFO: Validate if the schema for snr data model...")

        db_name = 'test_ladm_snr_data'
        restore_schema(db_name)
        self.db_connection = get_dbconn(db_name)
        result = self.db_connection.test_connection()
        self.assertTrue(result[0], 'The test connection is not working')

        self.assertFalse(self.db_connection.supplies_model_exists())
        self.assertTrue(self.db_connection.snr_data_model_exists())
        self.assertFalse(self.db_connection.supplies_integration_model_exists())
        self.assertFalse(self.db_connection.operation_model_exists())
        self.assertFalse(self.db_connection.valuation_model_exists())
        self.assertFalse(self.db_connection.cadastral_form_model_exists())
        self.assertFalse(self.db_connection.ant_model_exists())
        self.assertFalse(self.db_connection.reference_cartography_model_exists())

        self.db_connection.conn.close()

    def test_cadastral_manager_data_model(self):
        print("\nINFO: Validate if the schema cadastral manager data model...")

        db_name = 'test_ladm_cadastral_manager_data'
        restore_schema(db_name)
        self.db_connection = get_dbconn(db_name)
        result = self.db_connection.test_connection()
        self.assertTrue(result[0], 'The test connection is not working')

        self.assertTrue(self.db_connection.supplies_model_exists())
        self.assertFalse(self.db_connection.snr_data_model_exists())
        self.assertFalse(self.db_connection.supplies_integration_model_exists())
        self.assertFalse(self.db_connection.operation_model_exists())
        self.assertFalse(self.db_connection.valuation_model_exists())
        self.assertFalse(self.db_connection.cadastral_form_model_exists())
        self.assertFalse(self.db_connection.ant_model_exists())
        self.assertFalse(self.db_connection.reference_cartography_model_exists())

        self.db_connection.conn.close()

    def test_integration_models(self):
        print("\nINFO: Validate if the schema all models...")

        db_name = 'test_ladm_integration'
        restore_schema(db_name)
        self.db_connection = get_dbconn(db_name)
        result = self.db_connection.test_connection()
        self.assertTrue(result[0], 'The test connection is not working')

        self.assertTrue(self.db_connection.supplies_model_exists())
        self.assertTrue(self.db_connection.snr_data_model_exists())
        self.assertTrue(self.db_connection.supplies_integration_model_exists())
        self.assertFalse(self.db_connection.operation_model_exists())
        self.assertFalse(self.db_connection.valuation_model_exists())
        self.assertFalse(self.db_connection.cadastral_form_model_exists())
        self.assertFalse(self.db_connection.ant_model_exists())
        self.assertFalse(self.db_connection.reference_cartography_model_exists())

        self.db_connection.conn.close()

    def test_operation_model(self):
        print("\nINFO: Validate if the schema has the operating model...")

        db_name = 'test_ladm_operation_model'
        restore_schema(db_name)
        self.db_connection = get_dbconn(db_name)
        result = self.db_connection.test_connection()
        self.assertTrue(result[0], 'The test connection is not working')

        self.assertTrue(self.db_connection.supplies_model_exists())
        self.assertTrue(self.db_connection.snr_data_model_exists())
        self.assertTrue(self.db_connection.supplies_integration_model_exists())
        self.assertTrue(self.db_connection.operation_model_exists())
        self.assertFalse(self.db_connection.valuation_model_exists())
        self.assertFalse(self.db_connection.cadastral_form_model_exists())
        self.assertFalse(self.db_connection.ant_model_exists())
        self.assertFalse(self.db_connection.reference_cartography_model_exists())

        self.db_connection.conn.close()

    def test_valuation_model(self):
        print("\nINFO: Validate if the schema has the valuation model...")

        db_name = 'test_ladm_valuation_model'
        restore_schema(db_name)
        self.db_connection = get_dbconn(db_name)
        result = self.db_connection.test_connection()
        self.assertTrue(result[0], 'The test connection is not working')

        self.assertTrue(self.db_connection.supplies_model_exists())
        self.assertTrue(self.db_connection.snr_data_model_exists())
        self.assertTrue(self.db_connection.supplies_integration_model_exists())
        self.assertTrue(self.db_connection.operation_model_exists())
        self.assertTrue(self.db_connection.valuation_model_exists())
        self.assertFalse(self.db_connection.cadastral_form_model_exists())
        self.assertFalse(self.db_connection.ant_model_exists())
        self.assertFalse(self.db_connection.reference_cartography_model_exists())

        self.db_connection.conn.close()

    def test_cadastral_form_model(self):
        print("\nINFO: Validate if the schema has the cadastral form model...")

        db_name = 'test_ladm_cadastral_form_model'
        restore_schema(db_name)
        self.db_connection = get_dbconn(db_name)
        result = self.db_connection.test_connection()
        self.assertTrue(result[0], 'The test connection is not working')

        self.assertTrue(self.db_connection.supplies_model_exists())
        self.assertTrue(self.db_connection.snr_data_model_exists())
        self.assertTrue(self.db_connection.supplies_integration_model_exists())
        self.assertTrue(self.db_connection.operation_model_exists())
        self.assertTrue(self.db_connection.valuation_model_exists())
        self.assertTrue(self.db_connection.cadastral_form_model_exists())
        self.assertFalse(self.db_connection.ant_model_exists())
        self.assertFalse(self.db_connection.reference_cartography_model_exists())

        self.db_connection.conn.close()

    def test_reference_cartography_model(self):
        print("\nINFO: Validate if the schema all models...")

        db_name = 'test_ladm_reference_cartography'
        restore_schema(db_name)
        self.db_connection = get_dbconn(db_name)
        result = self.db_connection.test_connection()
        self.assertTrue(result[0], 'The test connection is not working')

        self.assertTrue(self.db_connection.supplies_model_exists())
        self.assertTrue(self.db_connection.snr_data_model_exists())
        self.assertTrue(self.db_connection.supplies_integration_model_exists())
        self.assertTrue(self.db_connection.operation_model_exists())
        self.assertFalse(self.db_connection.valuation_model_exists())
        self.assertFalse(self.db_connection.cadastral_form_model_exists())
        self.assertFalse(self.db_connection.ant_model_exists())
        self.assertTrue(self.db_connection.reference_cartography_model_exists())

        self.db_connection.conn.close()

    def test_ant_model(self):
        print("\nINFO: Validate if the schema all models...")

        db_name = 'test_ladm_ant'
        restore_schema(db_name)
        self.db_connection = get_dbconn(db_name)
        result = self.db_connection.test_connection()
        self.assertTrue(result[0], 'The test connection is not working')

        self.assertTrue(self.db_connection.supplies_model_exists())
        self.assertTrue(self.db_connection.snr_data_model_exists())
        self.assertTrue(self.db_connection.supplies_integration_model_exists())
        self.assertTrue(self.db_connection.operation_model_exists())
        self.assertFalse(self.db_connection.valuation_model_exists())
        self.assertFalse(self.db_connection.cadastral_form_model_exists())
        self.assertTrue(self.db_connection.ant_model_exists())
        self.assertFalse(self.db_connection.reference_cartography_model_exists())

        self.db_connection.conn.close()

    def test_all_models(self):
        print("\nINFO: Validate if the schema all models...")

        db_name = 'test_ladm_all_models'
        restore_schema(db_name)
        self.db_connection = get_dbconn(db_name)
        result = self.db_connection.test_connection()
        self.assertTrue(result[0], 'The test connection is not working')

        self.assertTrue(self.db_connection.supplies_model_exists())
        self.assertTrue(self.db_connection.snr_data_model_exists())
        self.assertTrue(self.db_connection.supplies_integration_model_exists())
        self.assertTrue(self.db_connection.operation_model_exists())
        self.assertTrue(self.db_connection.valuation_model_exists())
        self.assertTrue(self.db_connection.cadastral_form_model_exists())
        self.assertTrue(self.db_connection.ant_model_exists())
        self.assertTrue(self.db_connection.reference_cartography_model_exists())

        self.db_connection.conn.close()

    def tearDownClass():
        print('tearDown test_models_ladm')


if __name__ == '__main__':
    nose2.main()

