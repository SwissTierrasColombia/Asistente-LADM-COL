import unittest
from abc import ABC

import nose2

from qgis.testing import start_app

start_app() # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.lib.db.db_connector import DBConnector
from asistente_ladm_col.tests.base_test_for_models import BaseTestForModels
from asistente_ladm_col.tests.utils import (get_pg_conn,
                                            get_gpkg_conn,
                                            get_mssql_conn,
                                            restore_schema_mssql,
                                            reset_db_mssql,
                                            restore_schema)

class BaseTestCadastralManagerDataModel(BaseTestForModels, ABC):
    def get_name_of_models(self):
        return 'Cadastral manager data model'

    def check_required_models(self):
        self.assertTrue(self.db.supplies_model_exists())
        self.assertFalse(self.db.snr_data_model_exists())
        self.assertFalse(self.db.supplies_integration_model_exists())
        self.assertFalse(self.db.survey_model_exists())
        self.assertFalse(self.db.valuation_model_exists())
        self.assertFalse(self.db.cadastral_cartography_model_exists())


class TestCadastralManagerDataModelPG(BaseTestCadastralManagerDataModel, unittest.TestCase):
    schema = 'test_ladm_cadastral_manager_data'

    @classmethod
    def restore_db(cls):
        restore_schema(cls.schema)

    @classmethod
    def get_connector(cls) -> DBConnector:
        return get_pg_conn(cls.schema)

    def get_db_name(self):
        return 'PG'


class TestCadastralManagerDataModelGPKG(BaseTestCadastralManagerDataModel, unittest.TestCase):

    def get_db_name(self):
        return 'GPKG'

    @classmethod
    def restore_db(cls):
        pass

    @classmethod
    def get_connector(cls) -> DBConnector:
        return get_gpkg_conn('test_ladm_cadastral_manager_data_gpkg')


class TestCadastralManagerDataModelMSSQL(BaseTestCadastralManagerDataModel, unittest.TestCase):
    schema = 'test_ladm_cadastral_manager_data'

    def get_db_name(self):
        return 'SQL Server'

    @classmethod
    def restore_db(cls):
        reset_db_mssql(cls.schema)
        restore_schema_mssql(cls.schema)

    @classmethod
    def get_connector(cls) -> DBConnector:
        return get_mssql_conn(cls.schema)


if __name__ == '__main__':
    nose2.main()
