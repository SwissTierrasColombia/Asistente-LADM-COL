import nose2
import tempfile

from qgis.testing import (start_app,
                          unittest)

from asistente_ladm_col.tests.utils import (get_iface,
                                            get_test_copy_path,
                                            get_test_path,
                                            get_gpkg_conn_from_path,
                                            get_pg_conn,
                                            drop_pg_schema,
                                            get_mssql_conn,
                                            reset_db_mssql)
from asistente_ladm_col.asistente_ladm_col_plugin import AsistenteLADMCOLPlugin

from asistente_ladm_col.core.ili2db import Ili2DB
from asistente_ladm_col.lib.model_registry import LADMColModelRegistry
from asistente_ladm_col.config.ladm_names import LADMNames


asistente_ladm_col = AsistenteLADMCOLPlugin(get_iface(), False)

start_app()


class TestIli2db(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
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
            configuration = self.ili2db.get_import_schema_configuration(db, [model.full_name()])
            res_schema_import, msg_schema_import = self.ili2db.import_schema(db, configuration)
            self.assertTrue(res_schema_import, msg_schema_import)

            # Run import data
            xtf_path = get_test_path("xtf/test_ladm_col_queries_v1_2.xtf")
            configuration = self.ili2db.get_import_data_configuration(db, xtf_path)
            res_import_data, msg_import_data = self.ili2db.import_data(db, configuration)
            self.assertTrue(res_import_data, msg_import_data)

            # Export data
            xtf_export_path = tempfile.mktemp() + '.xtf'
            configuration = self.ili2db.get_export_configuration(db, xtf_export_path)
            res_export, msg_export = self.ili2db.export(db, configuration)
            self.assertTrue(res_export, msg_export)

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == '__main__':
    nose2.main()
