import nose2
import os
import tempfile

from asistente_ladm_col.config.ili2db_names import ILI2DBNames
from asistente_ladm_col.lib.model_registry import LADMColModelRegistry
from xml.dom.minidom import parse

from qgis.testing import unittest, start_app

from asistente_ladm_col.app_interface import AppInterface

start_app()
from QgisModelBaker.libqgsprojectgen.db_factory.gpkg_command_config_manager import GpkgCommandConfigManager
from QgisModelBaker.libqgsprojectgen.generator.generator import Generator
from QgisModelBaker.libili2db.ili2dbconfig import (SchemaImportConfiguration,
                                                   ImportDataConfiguration,
                                                   ExportConfiguration,
                                                   BaseConfiguration)
from QgisModelBaker.libili2db import (iliimporter,
                                      iliexporter)
from QgisModelBaker.libili2db.globals import DbIliMode

from asistente_ladm_col.config.general_config import (TOML_FILE_DIR,
                                                      DEFAULT_SRS_AUTH,
                                                      DEFAULT_SRS_CODE)
from asistente_ladm_col.config.ladm_names import LADMNames
from asistente_ladm_col.tests.utils import (testdata_path,
                                            get_test_copy_path,
                                            get_gpkg_conn_from_path,
                                            get_pg_conn,
                                            restore_schema,
                                            import_qgis_model_baker,
                                            unload_qgis_model_baker,
                                            MODELS_PATH,
                                            reset_db_mssql,
                                            get_mssql_conn, restore_schema_mssql)


class TestQgisModelBaker(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\nINFO: Setting up copy layer With different Geometries to DB validation...")
        print("INFO: Restoring databases to be used")

        cls.app = AppInterface()
        cls.base_test_path = tempfile.mkdtemp()
        import_qgis_model_baker()

        cls.ladmcol_models = LADMColModelRegistry()

    def test_export_data_in_pg(self):
        print("\nINFO: Validate Export Data in PG...")
        restore_schema('test_export_data')
        db_pg = get_pg_conn('test_export_data')

        base_config = BaseConfiguration()
        base_config.custom_model_directories = testdata_path(MODELS_PATH)
        base_config.custom_model_directories_enabled = True

        configuration = ExportConfiguration()
        configuration.base_configuration = base_config
        configuration.dbhost = 'postgres'
        configuration.dbusr = 'usuario_ladm_col'
        configuration.dbpwd = 'clave_ladm_col'
        configuration.database = 'ladm_col'
        configuration.dbschema = 'test_export_data'
        configuration.delete_data = True
        configuration.ilimodels = ';'.join([self.ladmcol_models.model(LADMNames.LADM_COL_MODEL_KEY).full_name(),
                                            self.ladmcol_models.model(LADMNames.SNR_DATA_SUPPLIES_MODEL_KEY).full_name(),
                                            self.ladmcol_models.model(LADMNames.SUPPLIES_MODEL_KEY).full_name(),
                                            self.ladmcol_models.model(LADMNames.SUPPLIES_INTEGRATION_MODEL_KEY).full_name(),
                                            self.ladmcol_models.model(LADMNames.SURVEY_MODEL_KEY).full_name()])

        exporter = iliexporter.Exporter()
        exporter.tool = DbIliMode.ili2pg
        exporter.configuration = configuration
        exporter.configuration.xtffile = os.path.join(tempfile.mkdtemp(), 'test_export_data.xtf')
        # exporter.stderr.connect(self.on_stderr)
        self.assertEqual(exporter.run(), iliexporter.Exporter.SUCCESS)
        self.check_export_xtf(exporter.configuration.xtffile)
        db_pg.conn.close()

    def test_export_data_in_gpkg(self):
        print("\nINFO: Validate Export Data in GPKG...")
        gpkg_path = get_test_copy_path('db/ladm/gpkg/test_export_data_ladm_v1_1.gpkg')

        base_config = BaseConfiguration()
        base_config.custom_model_directories = testdata_path(MODELS_PATH)
        base_config.custom_model_directories_enabled = True

        configuration = ExportConfiguration()
        configuration.base_configuration = base_config
        configuration.ilimodels = ';'.join([self.ladmcol_models.model(LADMNames.LADM_COL_MODEL_KEY).full_name(),
                                            self.ladmcol_models.model(LADMNames.SNR_DATA_SUPPLIES_MODEL_KEY).full_name(),
                                            self.ladmcol_models.model(LADMNames.SUPPLIES_MODEL_KEY).full_name(),
                                            self.ladmcol_models.model(LADMNames.SUPPLIES_INTEGRATION_MODEL_KEY).full_name(),
                                            self.ladmcol_models.model(LADMNames.SURVEY_MODEL_KEY).full_name()])
        configuration.dbfile = gpkg_path

        exporter = iliexporter.Exporter()
        exporter.tool = DbIliMode.ili2gpkg
        exporter.configuration = configuration
        exporter.configuration.xtffile = os.path.join(self.base_test_path, 'test_export_data.xtf')
        # exporter.stderr.connect(self.on_stderr)
        self.assertEqual(exporter.run(), iliexporter.Exporter.SUCCESS)
        self.check_export_xtf(exporter.configuration.xtffile)

    def check_export_xtf(self, xtf_path):
        test_xtf_dom = parse(testdata_path('xtf/test_ladm_col_queries_v1_1.xtf'))
        test_xtf_lc_building_count = len(test_xtf_dom.getElementsByTagName('Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_1.Levantamiento_Catastral.LC_Construccion'))
        test_xtf_lc_admin_source_count = len(test_xtf_dom.getElementsByTagName('Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_1.Levantamiento_Catastral.LC_FuenteAdministrativa'))
        test_xtf_snr = test_xtf_dom.getElementsByTagName('Submodelo_Insumos_SNR_V1_0.Datos_SNR')[0]
        test_xtf_gc = test_xtf_dom.getElementsByTagName('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral')[0]
        test_xtf_integration = test_xtf_dom.getElementsByTagName('Submodelo_Integracion_Insumos_V1_0.Datos_Integracion_Insumos')[0]

        xtf_dom = parse(testdata_path(xtf_path))
        xtf_lc_building_count = len(xtf_dom.getElementsByTagName('Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_1.Levantamiento_Catastral.LC_Construccion'))
        xtf_lc_admin_source_count = len(xtf_dom.getElementsByTagName('Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_1.Levantamiento_Catastral.LC_FuenteAdministrativa'))
        xtf_snr = xtf_dom.getElementsByTagName('Submodelo_Insumos_SNR_V1_0.Datos_SNR')[0]
        xtf_gc = xtf_dom.getElementsByTagName('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral')[0]
        xtf_integration = xtf_dom.getElementsByTagName('Submodelo_Integracion_Insumos_V1_0.Datos_Integracion_Insumos')[0]

        self.assertEqual(xtf_lc_building_count, test_xtf_lc_building_count)
        self.assertEqual(xtf_lc_admin_source_count, test_xtf_lc_admin_source_count)
        self.assertEqual(xtf_snr.toxml(), test_xtf_snr.toxml())
        self.assertEqual(xtf_gc.toxml(), test_xtf_gc.toxml())
        self.assertEqual(xtf_integration.toxml(), test_xtf_integration.toxml())

    def test_import_data_in_pg(self):
        print("\nINFO: Validate Import Data in PG...")

        restore_schema('test_import_data')
        db_pg = get_pg_conn('test_import_data')

        base_config = BaseConfiguration()
        base_config.custom_model_directories = testdata_path(MODELS_PATH)
        base_config.custom_model_directories_enabled = True

        configuration = ImportDataConfiguration()
        configuration.base_configuration = base_config
        configuration.dbhost = 'postgres'
        configuration.dbusr = 'usuario_ladm_col'
        configuration.dbpwd = 'clave_ladm_col'
        configuration.database = 'ladm_col'
        configuration.srs_auth = DEFAULT_SRS_AUTH
        configuration.srs_code = DEFAULT_SRS_CODE
        configuration.inheritance = ILI2DBNames.DEFAULT_INHERITANCE
        configuration.create_basket_col = ILI2DBNames.CREATE_BASKET_COL
        configuration.create_import_tid = ILI2DBNames.CREATE_IMPORT_TID
        configuration.stroke_arcs = ILI2DBNames.STROKE_ARCS
        configuration.dbschema = 'test_import_data'
        configuration.delete_data = True
        configuration.ilimodels = ';'.join([self.ladmcol_models.model(LADMNames.LADM_COL_MODEL_KEY).full_name(),
                                            self.ladmcol_models.model(LADMNames.SNR_DATA_SUPPLIES_MODEL_KEY).full_name(),
                                            self.ladmcol_models.model(LADMNames.SUPPLIES_MODEL_KEY).full_name(),
                                            self.ladmcol_models.model(LADMNames.SUPPLIES_INTEGRATION_MODEL_KEY).full_name(),
                                            self.ladmcol_models.model(LADMNames.SURVEY_MODEL_KEY).full_name()])

        importer = iliimporter.Importer(dataImport=True)
        importer.tool = DbIliMode.ili2pg
        importer.configuration = configuration
        importer.configuration.xtffile = testdata_path('xtf/test_ladm_col_queries_v1_1.xtf')
        # importer.stderr.connect(self.on_stderr)
        self.assertEqual(importer.run(), iliimporter.Importer.SUCCESS)

        generator = Generator(
            DbIliMode.ili2pg,
            'dbname={} user={} password={} host={}'.format(configuration.database, configuration.dbusr,
                                                           configuration.dbpwd, configuration.dbhost),
            configuration.inheritance,
            importer.configuration.dbschema)

        available_layers = generator.layers()
        self.assertEqual(len(available_layers), 160)

        res, code, msg = db_pg.test_connection()
        self.assertTrue(res, msg)
        test_layer = self.app.core.get_layer(db_pg, db_pg.names.LC_BOUNDARY_POINT_T, load=True)

        self.assertEqual(test_layer.featureCount(), 390)
        db_pg.conn.close()

    def test_import_data_in_gpkg(self):
        print("\nINFO: Validate Import Data in GPKG...")

        gpkg_path = get_test_copy_path('db/ladm/gpkg/test_import_data_ladm_v1_1.gpkg')

        base_config = BaseConfiguration()
        base_config.custom_model_directories = testdata_path(MODELS_PATH)
        base_config.custom_model_directories_enabled = True

        configuration = ImportDataConfiguration()
        configuration.base_configuration = base_config

        configuration.tool = DbIliMode.ili2gpkg
        configuration.dbfile = gpkg_path
        configuration.srs_auth = DEFAULT_SRS_AUTH
        configuration.srs_code = DEFAULT_SRS_CODE
        configuration.inheritance = ILI2DBNames.DEFAULT_INHERITANCE
        configuration.create_basket_col = ILI2DBNames.CREATE_BASKET_COL
        configuration.create_import_tid = ILI2DBNames.CREATE_IMPORT_TID
        configuration.stroke_arcs = ILI2DBNames.STROKE_ARCS
        configuration.delete_data = True
        configuration.ilimodels = ';'.join([self.ladmcol_models.model(LADMNames.LADM_COL_MODEL_KEY).full_name(),
                                            self.ladmcol_models.model(LADMNames.SNR_DATA_SUPPLIES_MODEL_KEY).full_name(),
                                            self.ladmcol_models.model(LADMNames.SUPPLIES_MODEL_KEY).full_name(),
                                            self.ladmcol_models.model(LADMNames.SUPPLIES_INTEGRATION_MODEL_KEY).full_name(),
                                            self.ladmcol_models.model(LADMNames.SURVEY_MODEL_KEY).full_name()])
        importer = iliimporter.Importer(dataImport=True)
        importer.tool = DbIliMode.ili2gpkg
        importer.configuration = configuration
        importer.configuration.xtffile = testdata_path('xtf/test_ladm_col_queries_v1_1.xtf')
        # importer.stderr.connect(self.on_stderr)
        self.assertEqual(importer.run(), iliimporter.Importer.SUCCESS)

        config_manager = GpkgCommandConfigManager(importer.configuration)
        generator = Generator(DbIliMode.ili2gpkg, config_manager.get_uri(), configuration.inheritance)

        available_layers = generator.layers()
        self.assertEqual(len(available_layers), 160)

        db_gpkg = get_gpkg_conn_from_path(config_manager.get_uri())
        res, code, msg = db_gpkg.test_connection()
        self.assertTrue(res, msg)
        test_layer = self.app.core.get_layer(db_gpkg, db_gpkg.names.LC_BOUNDARY_POINT_T, load=True)
        self.assertEqual(test_layer.featureCount(), 390)
        db_gpkg.conn.close()

    def test_import_schema_in_pg(self):
        print("\nINFO: Validate Import Schema in PG...")
        base_config = BaseConfiguration()
        base_config.custom_model_directories = testdata_path('xtf') +';' +testdata_path(MODELS_PATH)
        base_config.custom_model_directories_enabled = True

        configuration = SchemaImportConfiguration()
        configuration.base_configuration = base_config
        configuration.tool = DbIliMode.ili2pg
        configuration.dbhost = 'postgres'
        configuration.dbusr = 'usuario_ladm_col'
        configuration.dbpwd = 'clave_ladm_col'
        configuration.database = 'ladm_col'
        configuration.dbschema = 'test_import_schema'
        configuration.tomlfile = TOML_FILE_DIR
        configuration.srs_code = 3116
        configuration.inheritance = ILI2DBNames.DEFAULT_INHERITANCE
        configuration.create_basket_col = ILI2DBNames.CREATE_BASKET_COL
        configuration.create_import_tid = ILI2DBNames.CREATE_IMPORT_TID
        configuration.stroke_arcs = ILI2DBNames.STROKE_ARCS
        configuration.ilimodels = ';'.join([self.ladmcol_models.model(LADMNames.LADM_COL_MODEL_KEY).full_name(),
                                            self.ladmcol_models.model(LADMNames.SNR_DATA_SUPPLIES_MODEL_KEY).full_name(),
                                            self.ladmcol_models.model(LADMNames.SUPPLIES_MODEL_KEY).full_name(),
                                            self.ladmcol_models.model(LADMNames.SUPPLIES_INTEGRATION_MODEL_KEY).full_name(),
                                            self.ladmcol_models.model(LADMNames.SURVEY_MODEL_KEY).full_name(),
                                            self.ladmcol_models.model(LADMNames.CADASTRAL_CARTOGRAPHY_MODEL_KEY).full_name(),
                                            self.ladmcol_models.model(LADMNames.VALUATION_MODEL_KEY).full_name()])

        importer = iliimporter.Importer()
        importer.tool = DbIliMode.ili2pg
        importer.configuration = configuration
        # importer.stderr.connect(self.on_stderr)
        self.assertEqual(importer.run(), iliimporter.Importer.SUCCESS)

        generator = Generator(
            DbIliMode.ili2pg,
            'dbname={} user={} password={} host={}'.format(configuration.database, configuration.dbusr, configuration.dbpwd, configuration.dbhost),
            configuration.inheritance,
            importer.configuration.dbschema)

        available_layers = generator.layers()
        self.assertEqual(len(available_layers), 188)

    def test_import_schema_in_gpkg(self):
        print("\nINFO: Validate Import Schema in GPKG...")
        base_config = BaseConfiguration()
        base_config.custom_model_directories = testdata_path(MODELS_PATH)
        base_config.custom_model_directories_enabled = True

        configuration = SchemaImportConfiguration()
        configuration.base_configuration = base_config
        configuration.tool = DbIliMode.ili2gpkg
        configuration.dbfile = os.path.join(self.base_test_path, 'tmp_import_schema.gpkg')
        configuration.tomlfile = TOML_FILE_DIR
        configuration.srs_code = 3116
        configuration.inheritance = ILI2DBNames.DEFAULT_INHERITANCE
        configuration.create_basket_col = ILI2DBNames.CREATE_BASKET_COL
        configuration.create_import_tid = ILI2DBNames.CREATE_IMPORT_TID
        configuration.stroke_arcs = ILI2DBNames.STROKE_ARCS
        configuration.ilimodels = ';'.join([self.ladmcol_models.model(LADMNames.LADM_COL_MODEL_KEY).full_name(),
                                            self.ladmcol_models.model(LADMNames.SNR_DATA_SUPPLIES_MODEL_KEY).full_name(),
                                            self.ladmcol_models.model(LADMNames.SUPPLIES_MODEL_KEY).full_name(),
                                            self.ladmcol_models.model(LADMNames.SUPPLIES_INTEGRATION_MODEL_KEY).full_name(),
                                            self.ladmcol_models.model(LADMNames.SURVEY_MODEL_KEY).full_name(),
                                            self.ladmcol_models.model(LADMNames.CADASTRAL_CARTOGRAPHY_MODEL_KEY).full_name(),
                                            self.ladmcol_models.model(LADMNames.VALUATION_MODEL_KEY).full_name()])

        importer = iliimporter.Importer()
        importer.tool = DbIliMode.ili2gpkg
        importer.configuration = configuration
        # importer.stderr.connect(self.on_stderr)
        self.assertEqual(importer.run(), iliimporter.Importer.SUCCESS)

        config_manager = GpkgCommandConfigManager(importer.configuration)
        generator = Generator(DbIliMode.ili2gpkg, config_manager.get_uri(), configuration.inheritance)

        available_layers = generator.layers()
        self.assertEqual(len(available_layers), 188)

    def test_import_schema_in_mssql(self):
        schema = 'test_import_schema'
        reset_db_mssql(schema)

        print("\nINFO: Validate Import Schema in MS SQL Server")
        base_config = BaseConfiguration()
        base_config.custom_model_directories = testdata_path('xtf') +';' +testdata_path(MODELS_PATH)
        base_config.custom_model_directories_enabled = True

        configuration = SchemaImportConfiguration()
        configuration.base_configuration = base_config
        configuration.tool = DbIliMode.ili2mssql
        configuration.dbhost = 'mssql'
        configuration.dbusr = 'sa'
        configuration.dbpwd = '<YourStrong!Passw0rd>'
        configuration.dbport = '1433'
        configuration.database = schema
        configuration.dbschema = schema
        configuration.db_odbc_driver = 'ODBC Driver 17 for SQL Server'

        configuration.tomlfile = TOML_FILE_DIR
        configuration.epsg = 9377
        configuration.inheritance = ILI2DBNames.DEFAULT_INHERITANCE
        configuration.create_basket_col = ILI2DBNames.CREATE_BASKET_COL
        configuration.create_import_tid = ILI2DBNames.CREATE_IMPORT_TID
        configuration.stroke_arcs = ILI2DBNames.STROKE_ARCS
        configuration.ilimodels = ';'.join([self.ladmcol_models.model(LADMNames.LADM_COL_MODEL_KEY).full_name(),
                                            self.ladmcol_models.model(LADMNames.SNR_DATA_SUPPLIES_MODEL_KEY).full_name(),
                                            self.ladmcol_models.model(LADMNames.SUPPLIES_MODEL_KEY).full_name(),
                                            self.ladmcol_models.model(LADMNames.SUPPLIES_INTEGRATION_MODEL_KEY).full_name(),
                                            self.ladmcol_models.model(LADMNames.SURVEY_MODEL_KEY).full_name()])

        importer = iliimporter.Importer()
        importer.tool = DbIliMode.ili2mssql
        importer.configuration = configuration
        # importer.stderr.connect(self.on_stderr)
        self.assertEqual(importer.run(), iliimporter.Importer.SUCCESS)

        generator = Generator(DbIliMode.ili2mssql,
                              'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={host},1433;DATABASE={db};UID={user};PWD={pwd}'
                              .format(db=configuration.database, user=configuration.dbusr, pwd=configuration.dbpwd,
                                      host=configuration.dbhost, port=configuration.dbport), configuration.inheritance,
                              importer.configuration.dbschema)

        available_layers = generator.layers()
        self.assertEqual(len(available_layers), 160)

    def test_import_data_in_mssql(self):
        print("\nINFO: Validate Import Data in MS SQL Server...")

        schema = 'test_ladm_col'
        reset_db_mssql(schema)
        restore_schema_mssql(schema)

        db_conn = get_mssql_conn(schema)

        base_config = BaseConfiguration()
        base_config.custom_model_directories = testdata_path(MODELS_PATH)
        base_config.custom_model_directories_enabled = True

        model_list = [self.ladmcol_models.model(LADMNames.LADM_COL_MODEL_KEY).full_name(),
                      self.ladmcol_models.model(LADMNames.SNR_DATA_SUPPLIES_MODEL_KEY).full_name(),
                      self.ladmcol_models.model(LADMNames.SUPPLIES_MODEL_KEY).full_name(),
                      self.ladmcol_models.model(LADMNames.SUPPLIES_INTEGRATION_MODEL_KEY).full_name(),
                      self.ladmcol_models.model(LADMNames.SURVEY_MODEL_KEY).full_name()]

        configuration = ImportDataConfiguration()
        configuration.base_configuration = base_config
        configuration.dbhost = 'mssql'
        configuration.dbusr = 'sa'
        configuration.dbpwd = '<YourStrong!Passw0rd>'
        configuration.dbport = '1433'
        configuration.database = schema  # use schema because delete schemas in mssql is difficult
        configuration.dbschema = schema
        configuration.db_odbc_driver = 'ODBC Driver 17 for SQL Server'
        configuration.delete_data = True
        configuration.ilimodels = ';'.join(model_list)

        configuration.inheritance = ILI2DBNames.DEFAULT_INHERITANCE

        configuration.create_basket_col = ILI2DBNames.CREATE_BASKET_COL
        configuration.create_import_tid = ILI2DBNames.CREATE_IMPORT_TID
        configuration.stroke_arcs = ILI2DBNames.STROKE_ARCS

        importer = iliimporter.Importer(dataImport=True)
        importer.tool = DbIliMode.ili2mssql
        importer.configuration = configuration
        importer.configuration.xtffile = testdata_path('xtf/test_ladm_col_queries_v1_1.xtf')
        # importer.stderr.connect(self.on_stderr)
        self.assertEqual(importer.run(), iliimporter.Importer.SUCCESS)

        generator = Generator(DbIliMode.ili2mssql,
                              'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={host},1433;DATABASE={db};UID={user};PWD={pwd}'
                              .format(db=configuration.database, user=configuration.dbusr, pwd=configuration.dbpwd,
                                      host=configuration.dbhost, port=configuration.dbport), configuration.inheritance,
                              importer.configuration.dbschema)

        available_layers = generator.layers()
        self.assertEqual(len(available_layers), 160)

        res, code, msg = db_conn.test_connection()
        self.assertTrue(res, msg)
        test_layer = self.app.core.get_layer(db_conn, db_conn.names.LC_BOUNDARY_POINT_T, load=True)

        self.assertEqual(test_layer.featureCount(), 390)
        db_conn.conn.close()

    def test_export_data_in_mssql(self):
        print("\nINFO: Validate Export Data in MS SQL Server...")

        schema = 'test_export_data'
        reset_db_mssql(schema)
        restore_schema_mssql(schema)

        db_conn = get_mssql_conn(schema)

        base_config = BaseConfiguration()
        base_config.custom_model_directories = testdata_path(MODELS_PATH)
        base_config.custom_model_directories_enabled = True

        model_list = [self.ladmcol_models.model(LADMNames.LADM_COL_MODEL_KEY).full_name(),
                      self.ladmcol_models.model(LADMNames.SNR_DATA_SUPPLIES_MODEL_KEY).full_name(),
                      self.ladmcol_models.model(LADMNames.SUPPLIES_MODEL_KEY).full_name(),
                      self.ladmcol_models.model(LADMNames.SUPPLIES_INTEGRATION_MODEL_KEY).full_name(),
                      self.ladmcol_models.model(LADMNames.SURVEY_MODEL_KEY).full_name()]

        configuration = ExportConfiguration()
        configuration.base_configuration = base_config
        configuration.dbhost = 'mssql'
        configuration.dbusr = 'sa'
        configuration.dbpwd = '<YourStrong!Passw0rd>'
        configuration.dbport = '1433'
        configuration.database = schema  # use schema because delete schemas in mssql is difficult
        configuration.dbschema = schema
        configuration.db_odbc_driver = 'ODBC Driver 17 for SQL Server'
        configuration.delete_data = True
        configuration.ilimodels = ';'.join(model_list)

        exporter = iliexporter.Exporter()
        exporter.tool = DbIliMode.ili2mssql
        exporter.configuration = configuration
        exporter.configuration.xtffile = os.path.join(tempfile.mkdtemp(), 'test_export_data.xtf')
        # exporter.stderr.connect(self.on_stderr)
        self.assertEqual(exporter.run(), iliexporter.Exporter.SUCCESS)
        self.check_export_xtf(exporter.configuration.xtffile)
        db_conn.conn.close()

    def on_stderr(self, text):
        if text:
            print("   ", text)

    @classmethod
    def tearDownClass(cls):
        unload_qgis_model_baker()

if __name__ == '__main__':
    nose2.main()
