import nose2
from asistente_ladm_col.lib.model_registry import LADMColModelRegistry

from qgis.testing import (start_app,
                          unittest)

start_app() # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.config.ladm_names import LADMNames
from asistente_ladm_col.tests.utils import (get_gpkg_conn,
                                            get_pg_conn,
                                            restore_schema,
                                            import_qgis_model_baker, unload_qgis_model_baker)


class TestGetModels(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        import_qgis_model_baker()
        cls.ladmcol_models = LADMColModelRegistry()

    def test_pg_get_models(self):
        print("\nINFO: Validate get models method() in postgres...")
        expected_dict = {'test_ladm_all_models': [self.ladmcol_models.model(LADMNames.VALUATION_MODEL_KEY).full_name(),
                                                  self.ladmcol_models.model(LADMNames.CADASTRAL_CARTOGRAPHY_MODEL_KEY).full_name(),
                                                  self.ladmcol_models.model(LADMNames.SUPPLIES_MODEL_KEY).full_name(),
                                                  self.ladmcol_models.model(LADMNames.SUPPLIES_INTEGRATION_MODEL_KEY).full_name(),
                                                  self.ladmcol_models.model(LADMNames.SNR_DATA_SUPPLIES_MODEL_KEY).full_name(),
                                                  self.ladmcol_models.model(LADMNames.SURVEY_MODEL_KEY).full_name(),
                                                  self.ladmcol_models.model(LADMNames.ISO19107_MODEL_KEY).full_name(),
                                                  self.ladmcol_models.model(LADMNames.LADM_COL_MODEL_KEY).full_name()],
                         'test_ladm_integration': [self.ladmcol_models.model(LADMNames.SNR_DATA_SUPPLIES_MODEL_KEY).full_name(),
                                                   self.ladmcol_models.model(LADMNames.SUPPLIES_INTEGRATION_MODEL_KEY).full_name(),
                                                   self.ladmcol_models.model(LADMNames.SUPPLIES_MODEL_KEY).full_name(),
                                                   self.ladmcol_models.model(LADMNames.ISO19107_MODEL_KEY).full_name(),
                                                   self.ladmcol_models.model(LADMNames.LADM_COL_MODEL_KEY).full_name()],
                         'test_ladm_survey_model': [self.ladmcol_models.model(LADMNames.SURVEY_MODEL_KEY).full_name(),
                                                    self.ladmcol_models.model(LADMNames.SNR_DATA_SUPPLIES_MODEL_KEY).full_name(),
                                                    self.ladmcol_models.model(LADMNames.SUPPLIES_INTEGRATION_MODEL_KEY).full_name(),
                                                    self.ladmcol_models.model(LADMNames.SUPPLIES_MODEL_KEY).full_name(),
                                                    self.ladmcol_models.model(LADMNames.ISO19107_MODEL_KEY).full_name(),
                                                    self.ladmcol_models.model(LADMNames.LADM_COL_MODEL_KEY).full_name()],
                         'test_ladm_cadastral_manager_data': [self.ladmcol_models.model(LADMNames.SUPPLIES_MODEL_KEY).full_name(),
                                                              self.ladmcol_models.model(LADMNames.ISO19107_MODEL_KEY).full_name()]}

        for schema_name in expected_dict:
            restore_schema(schema_name)
            self.db_pg = get_pg_conn(schema_name)
            res, code, msg = self.db_pg.test_connection()
            self.assertTrue(res, msg)

            model_names = self.db_pg.get_models()
            print(model_names, expected_dict[schema_name])
            self.assertEqual(set(expected_dict[schema_name]), set(model_names))
            self.db_pg.conn.close()

    def test_gpkg_get_models(self):
        print("\nINFO: Validate get models method() in geopackage...")
        expected_dict = {
            'test_ladm_all_models_gpkg': [self.ladmcol_models.model(LADMNames.VALUATION_MODEL_KEY).full_name(),
                                          self.ladmcol_models.model(LADMNames.CADASTRAL_CARTOGRAPHY_MODEL_KEY).full_name(),
                                          self.ladmcol_models.model(LADMNames.SUPPLIES_MODEL_KEY).full_name(),
                                          self.ladmcol_models.model(LADMNames.SUPPLIES_INTEGRATION_MODEL_KEY).full_name(),
                                          self.ladmcol_models.model(LADMNames.SNR_DATA_SUPPLIES_MODEL_KEY).full_name(),
                                          self.ladmcol_models.model(LADMNames.SURVEY_MODEL_KEY).full_name(),
                                          self.ladmcol_models.model(LADMNames.ISO19107_MODEL_KEY).full_name(),
                                          self.ladmcol_models.model(LADMNames.LADM_COL_MODEL_KEY).full_name()],
            'test_ladm_integration_gpkg': [self.ladmcol_models.model(LADMNames.SNR_DATA_SUPPLIES_MODEL_KEY).full_name(),
                                           self.ladmcol_models.model(LADMNames.SUPPLIES_INTEGRATION_MODEL_KEY).full_name(),
                                           self.ladmcol_models.model(LADMNames.SUPPLIES_MODEL_KEY).full_name(),
                                           self.ladmcol_models.model(LADMNames.ISO19107_MODEL_KEY).full_name(),
                                           self.ladmcol_models.model(LADMNames.LADM_COL_MODEL_KEY).full_name()],
            'test_ladm_survey_model_gpkg': [self.ladmcol_models.model(LADMNames.SURVEY_MODEL_KEY).full_name(),
                                            self.ladmcol_models.model(LADMNames.SNR_DATA_SUPPLIES_MODEL_KEY).full_name(),
                                            self.ladmcol_models.model(LADMNames.SUPPLIES_INTEGRATION_MODEL_KEY).full_name(),
                                            self.ladmcol_models.model(LADMNames.SUPPLIES_MODEL_KEY).full_name(),
                                            self.ladmcol_models.model(LADMNames.ISO19107_MODEL_KEY).full_name(),
                                            self.ladmcol_models.model(LADMNames.LADM_COL_MODEL_KEY).full_name()],
            'test_ladm_cadastral_manager_data_gpkg': [self.ladmcol_models.model(LADMNames.SUPPLIES_MODEL_KEY).full_name(),
                                                      self.ladmcol_models.model(LADMNames.ISO19107_MODEL_KEY).full_name()]}

        for gpkg_schema_name in expected_dict:
            self.db_gpkg = get_gpkg_conn(gpkg_schema_name)
            res, code, msg = self.db_gpkg.test_connection()
            self.assertTrue(res, msg)

            model_names = self.db_gpkg.get_models()
            self.assertEqual(set(expected_dict[gpkg_schema_name]), set(model_names))

    @classmethod
    def tearDownClass(cls):
        unload_qgis_model_baker()

if __name__ == '__main__':
    nose2.main()