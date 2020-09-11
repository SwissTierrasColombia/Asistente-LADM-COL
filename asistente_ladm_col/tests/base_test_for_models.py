from abc import ABC

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

    def get_required_field_list(self):
        raise NotImplementedError

    def get_required_table_names_list(self):
        raise NotImplementedError

    def get_expected_table_and_fields_length(self):
        raise NotImplementedError

    def get_expected_dict(self):
        raise NotImplementedError

    @classmethod
    def setUpClass(cls):
        print("INFO: Restoring databases to be used")
        cls.restore_db()
        cls.db = cls.get_connector()

    def test_required_field_names(self):
        print("\nINFO: Validate minimum required fields (only variables) from names in {}...".format(self.get_db_name()))

        res, code, msg = self.db.test_connection()

        self.assertTrue(res, msg)
        self._check_required_field_names()

    def test_required_models(self):
        print("\nINFO: Validate required models for {} in {}...".format(
            self.get_name_of_models(), self.get_db_name()))
        res, code, msg = self.db.test_connection()
        self.assertTrue(res, msg)
        self.check_required_models()

    def test_required_table_names(self):
        print("\nINFO: Validate minimum required tables (only variables) from names {}...".format(self.get_db_name()))
        res, code, msg = self.db.test_connection()
        self.assertTrue(res, msg)
        self._check_required_table_names()

    def test_names_from_model(self):
        print("\nINFO: Validate names (both variables and values) for {} in {}...".format(
            self.get_name_of_models(), self.get_db_name()))
        res, code, msg = self.db.test_connection()
        self.assertTrue(res, msg)

        dict_names = self.db.get_table_and_field_names()

        self.assertEqual(len(dict_names), self.get_expected_table_and_fields_length())

        expected_dict = self.get_expected_dict()

        for k, v in expected_dict.items():
            self.assertIn(k, dict_names)
            self.assertEqual(v, dict_names[k])

    def _check_required_field_names(self):
        test_required_fields = self.get_required_field_list()
        required_fields = self.__get_all_mapped_field_names()

        for test_required_field in test_required_fields:
            self.assertIn(test_required_field, required_fields)

    def _check_required_table_names(self):
        test_required_tables = self.get_required_table_names_list()
        required_tables = self.__get_all_mapped_table_names()

        for test_required_table in test_required_tables:
            self.assertIn(test_required_table, required_tables)

    @classmethod
    def __get_all_mapped_field_names(cls):
        # Get all field variables mapped from the db table and fields
        required_fields = list()
        for key, value in cls.db.names.TABLE_DICT.items():
            for key_field, value_field in value[cls.db.names.FIELDS_DICT].items():
                if getattr(cls.db.names, value_field):
                    required_fields.append(value_field)
        return required_fields

    @classmethod
    def __get_all_mapped_table_names(cls):
        # Get all table variables mapped from the db table and fields
        required_tables = list()
        for key, value in cls.db.names.TABLE_DICT.items():
            if getattr(cls.db.names, value[cls.db.names.VARIABLE_NAME]):
                required_tables.append(value[cls.db.names.VARIABLE_NAME])
        return required_tables

    @classmethod
    def tearDownClass(cls):
        print("INFO: Closing open connections to databases")
        cls.db.conn.close()
