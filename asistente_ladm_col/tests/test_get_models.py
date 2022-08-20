import nose2

from qgis.testing import (start_app,
                          unittest)

start_app() # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.config.ladm_names import LADMNames
from asistente_ladm_col.core.ili2db import Ili2DB
from asistente_ladm_col.lib.model_registry import LADMColModelRegistry
from asistente_ladm_col.tests.utils import (restore_pg_db,
                                            restore_mssql_db,
                                            restore_gpkg_db)


class TestGetModels(unittest.TestCase):
    expected_models = {
        'ladm_all_models': [LADMColModelRegistry().model(LADMNames.VALUATION_MODEL_KEY).full_name(),
                            LADMColModelRegistry().model(LADMNames.CADASTRAL_CARTOGRAPHY_MODEL_KEY).full_name(),
                            LADMColModelRegistry().model(LADMNames.SUPPLIES_MODEL_KEY).full_name(),
                            LADMColModelRegistry().model(LADMNames.SUPPLIES_INTEGRATION_MODEL_KEY).full_name(),
                            LADMColModelRegistry().model(LADMNames.SNR_DATA_SUPPLIES_MODEL_KEY).full_name(),
                            LADMColModelRegistry().model(LADMNames.SURVEY_MODEL_KEY).full_name(),
                            LADMColModelRegistry().model(LADMNames.ISO19107_MODEL_KEY).full_name(),
                            LADMColModelRegistry().model(LADMNames.LADM_COL_MODEL_KEY).full_name()],
        'ladm_integration': [LADMColModelRegistry().model(LADMNames.SNR_DATA_SUPPLIES_MODEL_KEY).full_name(),
                             LADMColModelRegistry().model(LADMNames.SUPPLIES_INTEGRATION_MODEL_KEY).full_name(),
                             LADMColModelRegistry().model(LADMNames.SUPPLIES_MODEL_KEY).full_name(),
                             LADMColModelRegistry().model(LADMNames.ISO19107_MODEL_KEY).full_name(),
                             LADMColModelRegistry().model(LADMNames.LADM_COL_MODEL_KEY).full_name()],
        'ladm_survey_model': [LADMColModelRegistry().model(LADMNames.SURVEY_MODEL_KEY).full_name(),
                              LADMColModelRegistry().model(LADMNames.SNR_DATA_SUPPLIES_MODEL_KEY).full_name(),
                              LADMColModelRegistry().model(LADMNames.SUPPLIES_INTEGRATION_MODEL_KEY).full_name(),
                              LADMColModelRegistry().model(LADMNames.SUPPLIES_MODEL_KEY).full_name(),
                              LADMColModelRegistry().model(LADMNames.ISO19107_MODEL_KEY).full_name(),
                              LADMColModelRegistry().model(LADMNames.LADM_COL_MODEL_KEY).full_name()],
        'ladm_cadastral_manager_data': [LADMColModelRegistry().model(LADMNames.SUPPLIES_MODEL_KEY).full_name(),
                                        LADMColModelRegistry().model(LADMNames.ISO19107_MODEL_KEY).full_name(),
                                        LADMColModelRegistry().model(LADMNames.LADM_COL_MODEL_KEY).full_name()]}

    @classmethod
    def setUpClass(cls):
        cls.ili2db = Ili2DB()

    def test_pg_get_models(self):
        print("\nINFO: Validate get models method() in postgres...")

        for schema_name in self.expected_models:
            self.db_pg = restore_pg_db(schema_name, self.expected_models[schema_name])
            res, code, msg = self.db_pg.test_connection()
            self.assertTrue(res, msg)

            model_names = self.db_pg.get_models()
            print(model_names, self.expected_models[schema_name])
            self.assertEqual(set(self.expected_models[schema_name]), set(model_names))
            self.db_pg.conn.close()

    def test_gpkg_get_models(self):
        print("\nINFO: Validate get models method() in geopackage...")

        for schema_name in self.expected_models:
            self.db_gpkg = restore_gpkg_db(schema_name, self.expected_models[schema_name])
            res, code, msg = self.db_gpkg.test_connection()
            self.assertTrue(res, msg)

            model_names = self.db_gpkg.get_models()
            self.assertEqual(set(self.expected_models[schema_name]), set(model_names))

    def test_mssql_get_models(self):
        print("\nINFO: Validate get models method() in mssql...")

        for schema_name in self.expected_models:
            self.db_mssql = restore_mssql_db(schema_name, self.expected_models[schema_name])
            res, code, msg = self.db_mssql.test_connection()
            self.assertTrue(res, msg)

            model_names = self.db_mssql.get_models()
            print(model_names, self.expected_models[schema_name])
            self.assertEqual(set(self.expected_models[schema_name]), set(model_names))
            self.db_mssql.conn.close()

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == '__main__':
    nose2.main()