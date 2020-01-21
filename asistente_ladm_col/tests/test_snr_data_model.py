import nose2

from qgis.testing import (start_app,
                          unittest)

start_app() # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.config.table_mapping_config import (Names,
                                                            ILICODE,
                                                            T_ID,
                                                            DESCRIPTION,
                                                            DISPLAY_NAME)
from asistente_ladm_col.tests.utils import (get_pg_conn,
                                            restore_schema)


class TestSNRDataModel(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        restore_schema('test_ladm_snr_data')
        self.db_connection = get_pg_conn('test_ladm_snr_data')
        self.names = Names()

    def test_required_models(self):
        print("\nINFO: Validate if the schema for snr data model...")
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

    def test_names_from_model(self):
        print("\nINFO: Validate names for SNR data model (small DB case)...")
        result = self.db_connection.test_connection()
        self.assertTrue(result[0], 'The test connection is not working')

        dict_names = self.db_connection.get_table_and_field_names()
        self.assertEqual(len(dict_names), 15)

        expected_dict = {T_ID: 't_id',
                         ILICODE: 'ilicode',
                         DESCRIPTION: 'description',
                         DISPLAY_NAME: 'dispname',
                         'Datos_SNR.Datos_SNR.snr_titular_derecho': {'table_name': 'snr_titular_derecho',
                                                                     'Datos_SNR.Datos_SNR.snr_titular_derecho.Porcentaje_Participacion': 'porcentaje_participacion',
                                                                     'Datos_SNR.Datos_SNR.snr_titular_derecho.snr_derecho..Datos_SNR.Datos_SNR.SNR_Derecho': 'snr_derecho',
                                                                     'Datos_SNR.Datos_SNR.snr_titular_derecho.snr_titular..Datos_SNR.Datos_SNR.SNR_Titular': 'snr_titular'}}

        for k,v in expected_dict.items():
            self.assertIn(k, dict_names)
            self.assertEqual(v, dict_names[k])

    @classmethod
    def tearDownClass(self):
        self.db_connection.conn.close()


if __name__ == '__main__':
    nose2.main()

