import unittest
from abc import ABC

import nose2

from qgis.testing import start_app

start_app()  # need to start before asistente_ladm_col.tests.utils

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

class BaseTestForCadastralCartographyModel(BaseTestForModels, ABC):
    schema = 'test_ladm_cadastral_cartography'
    xtf_path = get_test_path("db/ladm/test_ladm_cartography_model_v1_2.xtf")
    models = [LADMColModelRegistry().model(LADMNames.CADASTRAL_CARTOGRAPHY_MODEL_KEY).full_name()]
    def get_name_of_models(self):
        return 'Reference cadastral cartography model'
    
    def check_required_models(self):
        self.assertFalse(self.db.supplies_model_exists())
        self.assertFalse(self.db.snr_data_model_exists())
        self.assertFalse(self.db.supplies_integration_model_exists())
        self.assertFalse(self.db.survey_model_exists())
        self.assertFalse(self.db.valuation_model_exists())
        self.assertTrue(self.db.cadastral_cartography_model_exists())


class TestCadastralCartographyPG(BaseTestForCadastralCartographyModel, unittest.TestCase):

    @classmethod
    def restore_db(cls):
        restore_pg_db(cls.schema, cls.models, cls.xtf_path)

    @classmethod
    def get_connector(cls) -> DBConnector:
        return get_pg_conn(cls.schema)

    def get_db_name(self):
        return 'PG'


class TestCadastralCartographyGPKG(BaseTestForCadastralCartographyModel, unittest.TestCase):

    def get_db_name(self):
        return 'GPKG'

    @classmethod
    def restore_db(cls):
        pass

    @classmethod
    def get_connector(cls) -> DBConnector:
        return restore_gpkg_db(cls.schema, cls.models, cls.xtf_path)


class TestCadastralCartographyModelMSSQL(BaseTestForCadastralCartographyModel, unittest.TestCase):

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
