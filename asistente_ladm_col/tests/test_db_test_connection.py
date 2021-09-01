import nose2

from qgis.testing import (start_app,
                          unittest)

from asistente_ladm_col.config.ladm_names import LADMNames

start_app() # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.config.enums import (EnumTestConnectionMsg,
                                             EnumTestLevel)
from asistente_ladm_col.config.keys.common import REQUIRED_MODELS
from asistente_ladm_col.tests.utils import (get_gpkg_conn,
                                            get_pg_conn,
                                            restore_schema,
                                            get_gpkg_conn_from_path,
                                            import_qgis_model_baker,
                                            unload_qgis_model_baker,
                                            reset_db_mssql,
                                            restore_schema_mssql,
                                            get_mssql_conn)


class TestDBTestConnection(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\nINFO: Importing Model Baker...")
        import_qgis_model_baker()

    def test_pg_test_connection_interlis_ladm_col_models(self):
        print("\nINFO: Validate test_connection() for PostgreSQL (Interlis, no LADM-COL models)...")

        restore_schema('test_ladm_all_models')
        db_pg = get_pg_conn('test_ladm_all_models')
        res, code, msg = db_pg.test_connection()
        self.assertTrue(res, msg)
        self.assertEqual(code, EnumTestConnectionMsg.SCHEMA_WITH_VALID_LADM_COL_STRUCTURE)
        db_pg.conn.close()

    def test_pg_test_connection_interlis_no_ladm_col_models(self):
        print("\nINFO: Validate test_connection() for PostgreSQL (Interlis, no LADM-COL models)...")

        restore_schema('interlis_no_ladm')
        db_pg = get_pg_conn('interlis_no_ladm')
        res, code, msg = db_pg.test_connection()
        self.assertFalse(res, msg)
        self.assertEqual(code, EnumTestConnectionMsg.NO_LADM_MODELS_FOUND_IN_SUPPORTED_VERSION)
        db_pg.conn.close()

    def test_pg_test_connection_no_interlis_no_ladm_col_models(self):
        print("\nINFO: Validate test_connection() for PostgreSQL (no Interlis, no LADM-COL models)...")

        restore_schema('empty_no_interlis_no_ladm')
        db_pg = get_pg_conn('empty_no_interlis_no_ladm')
        res, code, msg = db_pg.test_connection()
        self.assertFalse(res, msg)
        self.assertEqual(code, EnumTestConnectionMsg.INTERLIS_META_ATTRIBUTES_NOT_FOUND)
        db_pg.conn.close()

    def test_pg_test_connection_interlis_with_ili2pg3_ladm_col_221_models(self):
        print("\nINFO: Validate test_connection() for PostgreSQL (Interlis with ili2pg 3, LADM-COL 2.2.1 models)...")

        restore_schema('interlis_ili2db3_ladm')
        db_pg = get_pg_conn('interlis_ili2db3_ladm')
        res, code, msg = db_pg.test_connection()
        self.assertFalse(res, msg)
        self.assertEqual(EnumTestConnectionMsg.INVALID_ILI2DB_VERSION, code)
        db_pg.conn.close()

    def test_pg_test_connection_interlis_ladm_col_models_higher_version(self):
        print("\nINFO: Validate test_connection() for PostgreSQL (Interlis, LADM-COL with higher models version)...")

        restore_schema('ladm_col_210')
        db_pg = get_pg_conn('ladm_col_210')
        res, code, msg = db_pg.test_connection()
        self.assertFalse(res, msg)
        self.assertEqual(code, EnumTestConnectionMsg.NO_LADM_MODELS_FOUND_IN_SUPPORTED_VERSION)
        db_pg.conn.close()

    def test_gpkg_test_connection(self):
        print("\nINFO: Validate test_connection() for GeoPackage (survey model: OK!)...")
        db = get_gpkg_conn('test_ladm_survey_model_gpkg')
        res, code, msg = db.test_connection()
        self.assertTrue(res, msg)
        self.assertEqual(code, EnumTestConnectionMsg.DB_WITH_VALID_LADM_COL_STRUCTURE)

    def test_gpkg_test_connection_wrong_extension(self):
        print("\nINFO: Validate test_connection() for GeoPackage (wrong extension)...")

        db = get_gpkg_conn_from_path('/tmp/a.gpkgs')
        res, code, msg = db.test_connection()
        self.assertFalse(res, msg)
        self.assertEqual(code, EnumTestConnectionMsg.WRONG_FILE_EXTENSION)

    def test_gpkg_test_connection_dir_not_found(self):
        print("\nINFO: Validate test_connection() for GeoPackage (dir not found)...")

        db = get_gpkg_conn_from_path('/tmpa/a.gpkg')
        res, code, msg = db.test_connection(EnumTestLevel.SCHEMA_IMPORT)
        self.assertFalse(res, msg)
        self.assertEqual(code, EnumTestConnectionMsg.DIR_NOT_FOUND)

    def test_gpkg_test_connection_file_not_found(self):
        print("\nINFO: Validate test_connection() for GeoPackage (file not found)...")

        db = get_gpkg_conn_from_path('/tmp/a.gpkg')
        res, code, msg = db.test_connection()
        self.assertFalse(res, msg)
        self.assertEqual(code, EnumTestConnectionMsg.GPKG_FILE_NOT_FOUND)

    def test_gpkg_test_connection_existing_file_no_interlis(self):
        print("\nINFO: Validate test_connection() for GeoPackage (existing file, no Interlis)...")

        db = get_gpkg_conn('no_interlis_gpkg')
        res, code, msg = db.test_connection()
        self.assertFalse(res, msg)
        self.assertEqual(code, EnumTestConnectionMsg.INTERLIS_META_ATTRIBUTES_NOT_FOUND)

    def test_gpkg_test_connection_existing_file_schema_import(self):
        print("\nINFO: Validate test_connection() for GeoPackage (existing file, Schema Import)...")

        db = get_gpkg_conn('no_interlis_gpkg')
        res, code, msg = db.test_connection(EnumTestLevel.SCHEMA_IMPORT)
        self.assertTrue(res, msg)
        self.assertEqual(code, EnumTestConnectionMsg.CONNECTION_TO_SERVER_SUCCESSFUL)

    def test_gpkg_test_connection_interlis_no_ladm_col_models(self):
        print("\nINFO: Validate test_connection() for GeoPackage (Interlis, no LADM-COL models)...")

        db = get_gpkg_conn('interlis_no_ladm_col_models_gpkg')
        res, code, msg = db.test_connection()
        self.assertFalse(res, msg)
        self.assertEqual(code, EnumTestConnectionMsg.NO_LADM_MODELS_FOUND_IN_SUPPORTED_VERSION)

    def test_gpkg_test_connection_required_models_success(self):
        print("\nINFO: Validate test_connection() for GeoPackage (required models (success): survey and snr)...")
        db = get_gpkg_conn('test_ladm_survey_model_gpkg')
        res, code, msg = db.test_connection(models={REQUIRED_MODELS: [LADMNames.SURVEY_MODEL_KEY,
                                                                      LADMNames.SNR_DATA_SUPPLIES_MODEL_KEY]})
        self.assertTrue(res, msg)
        self.assertEqual(code, EnumTestConnectionMsg.DB_WITH_VALID_LADM_COL_STRUCTURE)

    def test_gpkg_test_connection_required_models_error(self):
        print("\nINFO: Validate test_connection() for GeoPackage (required models (error): ant)...")
        db = get_gpkg_conn('test_ladm_survey_model_gpkg')
        res, code, msg = db.test_connection(models={REQUIRED_MODELS: [LADMNames.VALUATION_MODEL_KEY]})
        self.assertFalse(res, msg)
        self.assertEqual(code, EnumTestConnectionMsg.REQUIRED_LADM_MODELS_NOT_FOUND)

    def test_mssql_test_connection_no_interlis_no_ladm_col_models(self):
        print("\nINFO: Validate test_connection() for SQL Server (no Interlis, no LADM-COL models)...")
        schema = 'empty_no_interlis_no_ladm'
        reset_db_mssql(schema)
        restore_schema_mssql(schema)
        db_conn = get_mssql_conn('empty_no_interlis_no_ladm')
        res, code, msg = db_conn.test_connection()
        self.assertFalse(res, msg)
        self.assertEqual(code, EnumTestConnectionMsg.INTERLIS_META_ATTRIBUTES_NOT_FOUND)
        db_conn.conn.close()

    def test_mssql_test_connection_interlis_no_ladm_col_models(self):
        print("\nINFO: Validate test_connection() for SQL Server (Interlis, no LADM-COL models)...")

        schema = 'interlis_no_ladm'
        reset_db_mssql(schema)
        restore_schema_mssql(schema)
        db_conn = get_mssql_conn(schema)
        res, code, msg = db_conn.test_connection()
        self.assertFalse(res, msg)
        self.assertEqual(code, EnumTestConnectionMsg.NO_LADM_MODELS_FOUND_IN_SUPPORTED_VERSION)
        db_conn.conn.close()

    def test_mssql_test_connection_interlis_ladm_col_models_higher_version(self):
        print("\nINFO: Validate test_connection() for SQL Server (Interlis, LADM-COL with higher models version)...")
        schema = 'ladm_col_211'
        reset_db_mssql(schema)
        restore_schema_mssql(schema)
        db_conn = get_mssql_conn(schema)
        res, code, msg = db_conn.test_connection()
        self.assertFalse(res, msg)
        self.assertEqual(code, EnumTestConnectionMsg.NO_LADM_MODELS_FOUND_IN_SUPPORTED_VERSION)
        db_conn.conn.close()

    def test_mssql_test_connection_interlis_ladm_col_models(self):
        print("\nINFO: Validate test_connection() for SQL Server (Interlis, no LADM-COL models)...")
        schema = 'test_ladm_all_models'
        reset_db_mssql(schema)
        restore_schema_mssql(schema)
        db_conn = get_mssql_conn(schema)
        res, code, msg = db_conn.test_connection()
        self.assertTrue(res, msg)
        self.assertEqual(code, EnumTestConnectionMsg.SCHEMA_WITH_VALID_LADM_COL_STRUCTURE)
        db_conn.conn.close()

    def test_mssql_test_connection_interlis_with_ili2mssql3_ladm_col_221_models(self):
        print("\nINFO: Validate test_connection() for SQL Server (Interlis with ili2mssql 3, LADM-COL 2.2.1 models)...")
        schema = 'interlis_ili2db3_ladm'
        reset_db_mssql(schema)
        restore_schema_mssql(schema)
        db_conn = get_mssql_conn(schema)
        res, code, msg = db_conn.test_connection()
        self.assertFalse(res, msg)
        self.assertEqual(EnumTestConnectionMsg.INVALID_ILI2DB_VERSION, code)
        db_conn.conn.close()

    @classmethod
    def tearDownClass(cls):
        print("INFO: Unloading Model Baker...")
        unload_qgis_model_baker()

if __name__ == '__main__':
    nose2.main()
