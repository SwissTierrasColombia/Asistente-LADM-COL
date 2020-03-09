import nose2

from qgis.testing import (start_app,
                          unittest)

start_app() # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.config.mapping_config import LADMNames
from asistente_ladm_col.tests.utils import (get_gpkg_conn,
                                            get_pg_conn,
                                            restore_schema)


class TestGetModels(unittest.TestCase):

    def test_pg_get_models(self):
        print("\nINFO: Validate get models method() in postgres...")
        expected_dict = {'test_ladm_all_models': [LADMNames.SUPPORTED_ANT_MODEL, LADMNames.SUPPORTED_VALUATION_MODEL,
                                                  LADMNames.SUPPORTED_REFERENCE_CARTOGRAPHY,
                                                  LADMNames.SUPPORTED_SUPPLIES_MODEL,
                                                  LADMNames.SUPPORTED_SUPPLIES_INTEGRATION_MODEL,
                                                  LADMNames.SUPPORTED_SNR_DATA_MODEL,
                                                  LADMNames.SUPPORTED_CADASTRAL_FORM_MODEL,
                                                  LADMNames.SUPPORTED_OPERATION_MODEL,
                                                  LADMNames.SUPPORTED_ISO_CARTESIAN_COORDINATES,
                                                  LADMNames.SUPPORTED_LADM_MODEL],
                         'test_ladm_integration': [LADMNames.SUPPORTED_SNR_DATA_MODEL,
                                                   LADMNames.SUPPORTED_SUPPLIES_INTEGRATION_MODEL,
                                                   LADMNames.SUPPORTED_SUPPLIES_MODEL,
                                                   LADMNames.SUPPORTED_ISO_CARTESIAN_COORDINATES,
                                                   LADMNames.SUPPORTED_LADM_MODEL],
                         'test_ladm_operation_model': [LADMNames.SUPPORTED_OPERATION_MODEL,
                                                       LADMNames.SUPPORTED_SNR_DATA_MODEL,
                                                       LADMNames.SUPPORTED_SUPPLIES_INTEGRATION_MODEL,
                                                       LADMNames.SUPPORTED_SUPPLIES_MODEL,
                                                       LADMNames.SUPPORTED_ISO_CARTESIAN_COORDINATES,
                                                       LADMNames.SUPPORTED_LADM_MODEL],
                         'test_ladm_cadastral_manager_data': [LADMNames.SUPPORTED_SUPPLIES_MODEL,
                                                              LADMNames.SUPPORTED_ISO_CARTESIAN_COORDINATES]}

        for schema_name in expected_dict:
            restore_schema(schema_name)
            self.db_pg = get_pg_conn(schema_name)

            model_names = self.db_pg.get_models()
            self.assertEqual(set(expected_dict[schema_name]), set(model_names))
            self.db_pg.conn.close()

    def test_gpkg_get_models(self):
        print("\nINFO: Validate get models method() in geopackage...")
        expected_dict = {
            'test_ladm_all_models_gpkg': [LADMNames.SUPPORTED_ANT_MODEL, LADMNames.SUPPORTED_VALUATION_MODEL,
                                          LADMNames.SUPPORTED_REFERENCE_CARTOGRAPHY,
                                          LADMNames.SUPPORTED_SUPPLIES_MODEL,
                                          LADMNames.SUPPORTED_SUPPLIES_INTEGRATION_MODEL,
                                          LADMNames.SUPPORTED_SNR_DATA_MODEL, LADMNames.SUPPORTED_CADASTRAL_FORM_MODEL,
                                          LADMNames.SUPPORTED_OPERATION_MODEL,
                                          LADMNames.SUPPORTED_ISO_CARTESIAN_COORDINATES,
                                          LADMNames.SUPPORTED_LADM_MODEL],
            'test_ladm_integration_gpkg': [LADMNames.SUPPORTED_SNR_DATA_MODEL,
                                           LADMNames.SUPPORTED_SUPPLIES_INTEGRATION_MODEL,
                                           LADMNames.SUPPORTED_SUPPLIES_MODEL,
                                           LADMNames.SUPPORTED_ISO_CARTESIAN_COORDINATES,
                                           LADMNames.SUPPORTED_LADM_MODEL],
            'test_ladm_operation_model_gpkg': [LADMNames.SUPPORTED_OPERATION_MODEL, LADMNames.SUPPORTED_SNR_DATA_MODEL,
                                               LADMNames.SUPPORTED_SUPPLIES_INTEGRATION_MODEL,
                                               LADMNames.SUPPORTED_SUPPLIES_MODEL,
                                               LADMNames.SUPPORTED_ISO_CARTESIAN_COORDINATES,
                                               LADMNames.SUPPORTED_LADM_MODEL],
            'test_ladm_cadastral_manager_data_gpkg': [LADMNames.SUPPORTED_SUPPLIES_MODEL,
                                                      LADMNames.SUPPORTED_ISO_CARTESIAN_COORDINATES]}

        for gpkg_schema_name in expected_dict:
            self.db_gpkg = get_gpkg_conn(gpkg_schema_name)

            model_names = self.db_gpkg.get_models()
            self.assertEqual(set(expected_dict[gpkg_schema_name]), set(model_names))


if __name__ == '__main__':
    nose2.main()