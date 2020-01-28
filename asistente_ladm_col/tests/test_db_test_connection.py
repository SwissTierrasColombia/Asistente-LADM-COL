import nose2

from qgis.testing import (start_app,
                          unittest)

start_app() # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.tests.utils import (get_gpkg_conn,
                                            get_pg_conn,
                                            restore_schema,
                                            get_gpkg_conn_from_path)


class TestDBTestConnection(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        print('setUp test_db_test_connection')

    def test_pg_test_connection_interlis_ladm_col_models(self):
        print("\nINFO: Validate test_connection() for PostgreSQL (Interlis, no LADM-COL models)...")

        restore_schema('test_ladm_all_models')
        db_pg = get_pg_conn('test_ladm_all_models')
        res, msg = db_pg.test_connection()
        self.assertTrue(res, msg)
        self.assertIn("has a valid LADM_COL structure!", msg)
        db_pg.conn.close()


    def test_pg_test_connection_interlis_no_ladm_col_models(self):
        print("\nINFO: Validate test_connection() for PostgreSQL (Interlis, no LADM-COL models)...")

        restore_schema('interlis_no_ladm')
        db_pg = get_pg_conn('interlis_no_ladm')
        res, msg = db_pg.test_connection()
        self.assertFalse(res, msg)
        self.assertIn('At least one LADM_COL model should exist!', msg)
        db_pg.conn.close()

    def test_pg_test_connection_no_interlis_no_ladm_col_models(self):
        print("\nINFO: Validate test_connection() for PostgreSQL (no Interlis, no LADM-COL models)...")

        restore_schema('empty_no_interlis_no_ladm')
        db_pg = get_pg_conn('empty_no_interlis_no_ladm')
        res, msg = db_pg.test_connection()
        self.assertFalse(res, msg)
        self.assertIn("The schema 'empty_no_interlis_no_ladm' is not a valid LADM_COL schema.", msg)
        self.assertIn("the schema doesn't have the structure of the LADM_COL model.", msg)
        db_pg.conn.close()

    def test_pg_test_connection_interlis_with_ili2pg3_ladm_col_221_models(self):
        print("\nINFO: Validate test_connection() for PostgreSQL (Interlis with ili2pg 3, LADM-COL 2.2.1 models)...")

        restore_schema('interlis_ili2db3_ladm')
        db_pg = get_pg_conn('interlis_ili2db3_ladm')
        res, msg = db_pg.test_connection()
        self.assertFalse(res, msg)
        self.assertIn("The DB schema 'interlis_ili2db3_ladm' was created with an old version of ili2db (v3), which is no longer supported. You need to migrate it to ili2db4.", msg)
        db_pg.conn.close()

    def test_pg_test_connection_bad_interlis_ladm_col_models(self):
        print("\nINFO: Validate test_connection() for PostgreSQL (Bad Interlis, LADM-COL models)...")
        print("\nINFO:All records for t_ili2db_attrname table where removed...")

        restore_schema('bad_interlis_ladm')
        db_pg = get_pg_conn('bad_interlis_ladm')
        res, msg = db_pg.test_connection()
        self.assertFalse(res, msg)
        self.assertIn('Table/field names from the DB are not correct.', msg)
        db_pg.conn.close()

    def test_pg_test_connection_interlis_ladm_col_models_upper_version(self):
        print("\nINFO: Validate test_connection() for PostgreSQL (Interlis, LADM-COL with higher models version)...")

        restore_schema('ladm_col_210')
        db_pg = get_pg_conn('ladm_col_210')
        res, msg = db_pg.test_connection()
        self.assertFalse(res, msg)
        self.assertIn("At least one LADM_COL model should exist! Supported models are 'LADM_COL_V1_3, Datos_SNR_V2_9_6, Datos_Gestor_Catastral_V2_9_6, Datos_Integracion_Insumos_V2_9_6, Operacion_V2_9_6, ANT_V2_9_6, Formulario_Catastro_V2_9_6, Cartografia_Referencia_V2_9_6, Avaluos_V2_9_6'", msg)
        db_pg.conn.close()

    def test_gpkg_test_connection(self):
        print("\nINFO: Validate test_connection() for GeoPackage (model operation: OK!)...")
        db = get_gpkg_conn('test_ladm_operation_model_gpkg')
        res, msg = db.test_connection()
        print(msg)
        self.assertTrue(res, msg)

    def test_gpkg_test_connection_file_not_found(self):
        print("\nINFO: Validate test_connection() for GeoPackage (file not found)...")

        db = get_gpkg_conn_from_path('/tmp/a.gpkg')
        res, msg = db.test_connection()
        print(msg)
        self.assertFalse(res, msg)

    def test_gpkg_test_connection_existing_file_no_interlis(self):
        print("\nINFO: Validate test_connection() for GeoPackage (existing file, no Interlis)...")

        db = get_gpkg_conn('no_interlis_gpkg')
        res, msg = db.test_connection()
        print(msg)
        self.assertFalse(res, msg)

    def test_gpkg_test_connection_interlis_no_ladm_col_models(self):
        print("\nINFO: Validate test_connection() for GeoPackage (Interlis, no LADM-COL models)...")

        db = get_gpkg_conn('interlis_no_ladm_col_models_gpkg')
        res, msg = db.test_connection()
        print(msg)
        self.assertFalse(res, msg)

if __name__ == '__main__':
    nose2.main()