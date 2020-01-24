import nose2

from qgis.testing import (start_app,
                          unittest)

start_app() # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.tests.utils import (get_gpkg_conn,
                                            get_gpkg_conn_from_path)

class TestDBTestConnection(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        print('setUp test_db_test_connection')

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

    def tearDownClass():
        print('tearDown test_db_test_connection')

if __name__ == '__main__':
    nose2.main()