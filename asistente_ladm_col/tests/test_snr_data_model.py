import nose2

from qgis.testing import (start_app,
                          unittest)

start_app() # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.config.table_mapping_config import (VARIABLE_NAME,
                                                            FIELDS_DICT)
from asistente_ladm_col.config.table_mapping_config import Names
from asistente_ladm_col.tests.utils import (get_dbconn,
                                            restore_schema)


class TestSNRDataModel(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        restore_schema('test_ladm_snr_data')
        self.db_connection = get_dbconn('test_ladm_snr_data')
        self.names = Names()

    def test_snr_data_model(self):
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

    def test_required_tables_names(self):
        print("\nINFO: Validate minimum required tables...")

        test_required_tables = ['SNR_RIGHT_T', 'SNR_SOURCE_BOUNDARIES_T', 'SNR_SOURCE_RIGHT_T', 'SNR_PARCEL_REGISTRY_T', 'SNR_TITLE_HOLDER_T', 'SNR_RIGHT_TYPE_D', 'SNR_TITLE_HOLDER_DOCUMENT_T', 'SNR_SOURCE_TYPE_D', 'SNR_TITLE_HOLDER_TYPE_D', 'EXT_ARCHIVE_S']
        required_tables = list()
        for key, value in self.names.TABLE_DICT.items():
            if getattr(self.names, value[VARIABLE_NAME]):
                required_tables.append(value[VARIABLE_NAME])

        self.assertListEqual(list(set(test_required_tables)), list(set(required_tables)))

    def test_required_fields_names(self):
        print("\nINFO: Validate minimum required fields...")

        test_required_fields = ['EXT_ARCHIVE_S_DATA_F', 'EXT_ARCHIVE_S_EXTRACTION_F', 'EXT_ARCHIVE_S_ACCEPTANCE_DATE_F', 'EXT_ARCHIVE_S_DELIVERY_DATE_F', 'EXT_ARCHIVE_S_STORAGE_DATE_F', 'EXT_ARCHIVE_S_NAMESPACE_F', 'EXT_ARCHIVE_S_LOCAL_ID_F']
        required_fields = list()
        for key, value in self.names.TABLE_DICT.items():
            for key_field, value_field in value[FIELDS_DICT].items():
                if getattr(self.names, value_field):
                    required_fields.append(value_field)

        self.assertListEqual(list(set(test_required_fields)), list(set(required_fields)))

    @classmethod
    def tearDownClass(self):
        self.db_connection.conn.close()


if __name__ == '__main__':
    nose2.main()

