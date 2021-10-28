import nose2
import tempfile

from qgis.testing import (start_app,
                          unittest)

from asistente_ladm_col.tests.utils import (get_test_copy_path,
                                            get_test_path,
                                            get_gpkg_conn_from_path,
                                            get_pg_conn,
                                            drop_pg_schema,
                                            get_mssql_conn,
                                            reset_db_mssql,
                                            import_qgis_model_baker,
                                            unload_qgis_model_baker)

from asistente_ladm_col.lib.qgis_model_baker.ili2db import Ili2DB
from asistente_ladm_col.lib.model_registry import LADMColModelRegistry
from asistente_ladm_col.config.ladm_names import LADMNames

start_app()


class TestIli2db(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        import_qgis_model_baker()
        cls.ili2db = Ili2DB()

        schema_name = 'ili2db'

        gpkg_path = get_test_copy_path('db/static/gpkg/ili2db.gpkg')
        gpkg_db = get_gpkg_conn_from_path(gpkg_path)

        drop_pg_schema(schema_name)
        pg_db = get_pg_conn(schema_name)

        reset_db_mssql(schema_name)
        mssql_db = get_mssql_conn(schema_name)

        cls.db_connections = {
            'gpkg': gpkg_db,
            'pg': pg_db,
            'mssql': mssql_db
        }

    def test_ili2db(self):
        for db_engine, db in self.db_connections.items():
            print("\nINFO: Validating import schema, import data and export method in {}...".format(db_engine))

            model = LADMColModelRegistry().model(LADMNames.SURVEY_MODEL_KEY)
            res_schema_import, msg_schema_import = self.ili2db.import_schema(db, [model.full_name()])
            self.assertTrue(res_schema_import, msg_schema_import)

            # Run import data
            xtf_path = get_test_path("xtf/test_ladm_col_queries_v1_1.xtf")
            res_import_data, msg_import_data = self.ili2db.import_data(db, xtf_path)
            self.assertTrue(res_import_data, msg_import_data)

            # Export data
            xtf_export_path = tempfile.mktemp() + '.xtf'
            res_export, msg_export = self.ili2db.export(db, xtf_export_path)
            self.assertTrue(res_export, msg_export)

    @classmethod
    def tearDownClass(cls):
        print("INFO: Unloading Model Baker...")
        unload_qgis_model_baker()


if __name__ == '__main__':
    nose2.main()
