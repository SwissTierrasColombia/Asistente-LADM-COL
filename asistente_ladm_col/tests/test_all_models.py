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


class BaseTestForAllModels(BaseTestForModels, ABC):
    def get_name_of_models(self):
        return 'All models'

    def check_required_models(self):
        self.assertTrue(self.db.supplies_model_exists())
        # self.assertTrue(self.db.snr_data_model_exists())  # TODO: Migrate to Lev Cat 1.2
        # self.assertTrue(self.db.supplies_integration_model_exists())  # TODO: Migrate to Lev Cat 1.2
        # self.assertTrue(self.db.survey_model_exists())  # TODO: Migrate to Lev Cat 1.2
        self.assertTrue(self.db.valuation_model_exists())
        # self.assertTrue(self.db.cadastral_cartography_model_exists())  # TODO: Migrate to Lev Cat 1.2


class TestAllModelsPG(BaseTestForAllModels, unittest.TestCase):
    schema = 'test_ladm_all_models'

    @classmethod
    def restore_db(cls):
        restore_schema(cls.schema)

    @classmethod
    def get_connector(cls) -> DBConnector:
        return get_pg_conn(cls.schema)

    def get_db_name(self):
        return 'PG'


class TestAllModelsGPKG(BaseTestForAllModels, unittest.TestCase):

    def get_db_name(self):
        return 'GPKG'

    @classmethod
    def restore_db(cls):
        pass

    @classmethod
    def get_connector(cls) -> DBConnector:
        return get_gpkg_conn('test_ladm_all_models_gpkg')


class TestAllModelsMSSQL(BaseTestForAllModels, unittest.TestCase):
    schema = 'test_ladm_all_models'

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
