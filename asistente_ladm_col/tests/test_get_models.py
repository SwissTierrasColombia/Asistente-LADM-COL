import nose2

from qgis.testing import (start_app,
                          unittest)

start_app() # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.config.ladm_names import LADMNames
from asistente_ladm_col.lib.qgis_model_baker.ili2db import Ili2DB
from asistente_ladm_col.lib.model_registry import LADMColModelRegistry
from asistente_ladm_col.tests.utils import (get_gpkg_conn,
                                            get_pg_conn,
                                            drop_pg_schema,
                                            get_mssql_conn,
                                            reset_db_mssql,
                                            restore_schema,
                                            get_test_copy_path,
                                            get_gpkg_conn_from_path,
                                            import_qgis_model_baker,
                                            unload_qgis_model_baker)


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
        import_qgis_model_baker()
        cls.ili2db = Ili2DB()

    def test_pg_get_models(self):
        print("\nINFO: Validate get models method() in postgres...")

        for schema_name in self.expected_models:
            drop_pg_schema(schema_name)
            self.db_pg = get_pg_conn(schema_name)
            self.ili2db.import_schema(self.db_pg, self.expected_models[schema_name])

            res, code, msg = self.db_pg.test_connection()
            self.assertTrue(res, msg)

            model_names = self.db_pg.get_models()
            print(model_names, self.expected_models[schema_name])
            self.assertEqual(set(self.expected_models[schema_name]), set(model_names))
            self.db_pg.conn.close()

    def test_gpkg_get_models(self):
        print("\nINFO: Validate get models method() in geopackage...")

        for schema_name in self.expected_models:
            self.db_gpkg = get_gpkg_conn_from_path(get_test_copy_path('db/static/gpkg/ili2db.gpkg'))
            self.ili2db.import_schema(self.db_gpkg, self.expected_models[schema_name])

            res, code, msg = self.db_gpkg.test_connection()
            self.assertTrue(res, msg)

            model_names = self.db_gpkg.get_models()
            self.assertEqual(set(self.expected_models[schema_name]), set(model_names))

    def test_mssql_get_models(self):
        print("\nINFO: Validate get models method() in mssql...")

        for schema_name in self.expected_models:
            reset_db_mssql(schema_name)
            self.db_mssql = get_mssql_conn(schema_name)
            self.ili2db.import_schema(self.db_mssql, self.expected_models[schema_name])

            res, code, msg = self.db_mssql.test_connection()
            self.assertTrue(res, msg)

            model_names = self.db_mssql.get_models()
            print(model_names, self.expected_models[schema_name])
            self.assertEqual(set(self.expected_models[schema_name]), set(model_names))
            self.db_mssql.conn.close()

    @classmethod
    def tearDownClass(cls):
        unload_qgis_model_baker()


if __name__ == '__main__':
    nose2.main()