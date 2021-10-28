import unittest
from abc import ABC

import nose2

from asistente_ladm_col.lib.db.db_connector import DBConnector
from asistente_ladm_col.tests.base_test_for_models import BaseTestForModels
from asistente_ladm_col.tests.utils import (get_pg_conn,
                                            drop_pg_schema,
                                            get_test_path,
                                            get_gpkg_conn,
                                            get_mssql_conn,
                                            get_test_copy_path,
                                            get_gpkg_conn_from_path,
                                            reset_db_mssql)

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
        drop_pg_schema(cls.schema)
        db = get_pg_conn(cls.schema)
        cls.ili2db.import_schema(db, cls.models)
        cls.ili2db.import_data(db, cls.xtf_path)

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
        gpkg_path = get_test_copy_path('db/static/gpkg/ili2db.gpkg')
        db = get_gpkg_conn_from_path(gpkg_path)
        cls.ili2db.import_schema(db, cls.models)
        cls.ili2db.import_data(db, cls.xtf_path)
        return db


class TestAllModelsMSSQL(BaseTestForAllModels, unittest.TestCase):
    schema = 'test_ladm_all_models'

    def get_db_name(self):
        return 'SQL Server'

    @classmethod
    def restore_db(cls):
        reset_db_mssql(cls.schema)
        db = get_mssql_conn(cls.schema)
        cls.ili2db.import_schema(db, cls.models)
        cls.ili2db.import_data(db, cls.xtf_path)

    @classmethod
    def get_connector(cls) -> DBConnector:
        return get_mssql_conn(cls.schema)


if __name__ == '__main__':
    nose2.main()
