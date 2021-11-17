import unittest
from abc import ABC

import nose2

from asistente_ladm_col.lib.db.db_connector import DBConnector
from asistente_ladm_col.tests.base_test_for_models import BaseTestForModels
from asistente_ladm_col.tests.utils import (get_pg_conn,
                                            get_test_path,
                                            get_mssql_conn,
                                            restore_pg_db,
                                            restore_mssql_db,
                                            restore_gpkg_db)

from asistente_ladm_col.config.ladm_names import LADMNames
from asistente_ladm_col.lib.model_registry import LADMColModelRegistry


class BaseTestForAllModels(BaseTestForModels, ABC):
    xtf_path = get_test_path("db/ladm/test_ladm_all_models_v1_1.xtf")
    models = [LADMColModelRegistry().model(LADMNames.SURVEY_MODEL_KEY).full_name(),
              LADMColModelRegistry().model(LADMNames.VALUATION_MODEL_KEY).full_name(),
              LADMColModelRegistry().model(LADMNames.CADASTRAL_CARTOGRAPHY_MODEL_KEY).full_name()]

    def get_name_of_models(self):
        return 'All models'

    def check_required_models(self):
        self.assertTrue(self.db.supplies_model_exists())
        self.assertTrue(self.db.snr_data_model_exists())
        self.assertTrue(self.db.supplies_integration_model_exists())
        self.assertTrue(self.db.survey_model_exists())
        self.assertTrue(self.db.valuation_model_exists())
        self.assertTrue(self.db.cadastral_cartography_model_exists())


class TestAllModelsPG(BaseTestForAllModels, unittest.TestCase):
    schema = 'test_ladm_all_models'

    @classmethod
    def restore_db(cls):
        restore_pg_db(cls.schema, cls.models, cls.xtf_path)

    @classmethod
    def get_connector(cls) -> DBConnector:
        return get_pg_conn(cls.schema)

    def get_db_name(self):
        return 'PG'


class TestAllModelsGPKG(BaseTestForAllModels, unittest.TestCase):
    file_name = 'test_ladm_all_models'

    def get_db_name(self):
        return 'GPKG'

    @classmethod
    def restore_db(cls):
        pass

    @classmethod
    def get_connector(cls) -> DBConnector:
        return restore_gpkg_db(cls.file_name, cls.models, cls.xtf_path)


class TestAllModelsMSSQL(BaseTestForAllModels, unittest.TestCase):
    schema = 'test_ladm_all_models'

    def get_db_name(self):
        return 'SQL Server'

    @classmethod
    def restore_db(cls):
        restore_mssql_db(cls.schema, cls.models, cls.xtf_path)

    @classmethod
    def get_connector(cls) -> DBConnector:
        return get_mssql_conn(cls.schema)


if __name__ == '__main__':
    nose2.main()
