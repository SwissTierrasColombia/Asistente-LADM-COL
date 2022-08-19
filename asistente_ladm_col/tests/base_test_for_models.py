from abc import ABC

from qgis.testing import start_app

start_app() # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.config.enums import EnumTestLevel
from asistente_ladm_col.lib.db.db_connector import DBConnector


class BaseTestForModels(ABC):

    def check_required_models(self):
        raise NotImplementedError

    def get_db_name(self):
        raise NotImplementedError

    def get_name_of_models(self):
        raise NotImplementedError

    @classmethod
    def restore_db(cls):
        raise NotImplementedError

    @classmethod
    def get_connector(cls) -> DBConnector:
        raise NotImplementedError

    @classmethod
    def setUpClass(cls):
        print("INFO: Restoring databases to be used")
        cls.restore_db()
        cls.db = cls.get_connector()

    def test_required_models(self):
        print("\nINFO: Validate required models for {} in {}...".format(
            self.get_name_of_models(), self.get_db_name()))
        res, code, msg = self.db.test_connection()
        self.assertTrue(res, msg)
        self.check_required_models()

    def test_names(self):
        print("\nINFO: Validate mapped names for {} in {}...".format(
            self.get_name_of_models(), self.get_db_name()))
        res, code, msg = self.db.test_connection(EnumTestLevel.DB)
        self.assertTrue(res, msg)

        res, msg = self.db.names.test_names()
        self.assertFalse(res, "We expected this check to be False because names shouldn't be initialized yet!")

        self.db.names.initialize_table_and_field_names(self.db.get_db_mapping(), self.db.get_models())
        res, msg = self.db.names.test_names()
        self.assertTrue(res, "Error: {}".format(msg))

    @classmethod
    def tearDownClass(cls):
        print("INFO: Closing open connections to databases")
        cls.db.conn.close()
