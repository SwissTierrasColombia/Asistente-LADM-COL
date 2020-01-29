import nose2
import os
import tempfile

from qgis.testing import unittest, start_app
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

from asistente_ladm_col.utils.utils import md5sum
from asistente_ladm_col.utils.qgis_utils import QGISUtils
from asistente_ladm_col.config.general_config import (TOML_FILE_DIR,
                                                      DEFAULT_EPSG)
from asistente_ladm_col.config.mapping_config import LADMNames
from asistente_ladm_col.tests.utils import (testdata_path,
                                            get_test_copy_path,
                                            get_gpkg_conn_from_path,
                                            get_pg_conn,
                                            restore_schema)


class TestQgisModelBaker(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        print("\nINFO: Setting up copy layer With different Geometries to DB validation...")
        self.qgis_utils = QGISUtils()

    def test_export_data_in_pg(self):
        print("\nINFO: Validate Export Data in PG...")
        restore_schema('test_export_data')
        db_pg = get_pg_conn('test_export_data')

        base_config = BaseConfiguration()
        base_config.custom_model_directories = testdata_path('models/LADM_COL')
        base_config.custom_model_directories_enabled = True

        configuration = ExportConfiguration()
        configuration.base_configuration = base_config
        configuration.dbhost = 'postgres'
        configuration.dbusr = 'usuario_ladm_col'
        configuration.dbpwd = 'clave_ladm_col'
        configuration.database = 'ladm_col'
        configuration.dbschema = 'test_export_data'
        configuration.delete_data = True
        configuration.ilimodels = ';'.join([LADMNames.SUPPORTED_LADM_MODEL,
                                            LADMNames.SUPPORTED_SNR_DATA_MODEL,
                                            LADMNames.SUPPORTED_SUPPLIES_MODEL,
                                            LADMNames.SUPPORTED_SUPPLIES_INTEGRATION_MODEL,
                                            LADMNames.SUPPORTED_OPERATION_MODEL,
                                            LADMNames.SUPPORTED_ANT_MODEL,
                                            LADMNames.SUPPORTED_CADASTRAL_FORM_MODEL,
                                            LADMNames.SUPPORTED_VALUATION_MODEL])

        exporter = iliexporter.Exporter()
        exporter.tool = DbIliMode.ili2pg
        exporter.configuration = configuration
        exporter.configuration.xtffile = os.path.join(tempfile.mkdtemp(), 'test_export_data.xtf')
        self.assertEqual(exporter.run(), iliexporter.Exporter.SUCCESS)
        self.assertEqual(md5sum(testdata_path('xtf/test_ladm_col_queries_v2.9.6.xtf')), md5sum(exporter.configuration.xtffile))
        db_pg.conn.close()

    def test_import_data_in_pg(self):
        print("\nINFO: Validate Import Data in PG...")

        restore_schema('test_import_data')
        db_pg = get_pg_conn('test_import_data')

        base_config = BaseConfiguration()
        base_config.custom_model_directories = testdata_path('models/LADM_COL')
        base_config.custom_model_directories_enabled = True

        configuration = ImportDataConfiguration()
        configuration.base_configuration = base_config
        configuration.dbhost = 'postgres'
        configuration.dbusr = 'usuario_ladm_col'
        configuration.dbpwd = 'clave_ladm_col'
        configuration.database = 'ladm_col'
        configuration.epsg = DEFAULT_EPSG
        configuration.inheritance = LADMNames.DEFAULT_INHERITANCE
        configuration.create_basket_col = LADMNames.CREATE_BASKET_COL
        configuration.create_import_tid = LADMNames.CREATE_IMPORT_TID
        configuration.stroke_arcs = LADMNames.STROKE_ARCS
        configuration.dbschema = 'test_import_data'
        configuration.delete_data = True
        configuration.ilimodels = ';'.join([LADMNames.SUPPORTED_LADM_MODEL,
                                            LADMNames.SUPPORTED_SNR_DATA_MODEL,
                                            LADMNames.SUPPORTED_SUPPLIES_MODEL,
                                            LADMNames.SUPPORTED_SUPPLIES_INTEGRATION_MODEL,
                                            LADMNames.SUPPORTED_OPERATION_MODEL,
                                            LADMNames.SUPPORTED_ANT_MODEL,
                                            LADMNames.SUPPORTED_CADASTRAL_FORM_MODEL,
                                            LADMNames.SUPPORTED_VALUATION_MODEL])

        importer = iliimporter.Importer(dataImport=True)
        importer.tool = DbIliMode.ili2pg
        importer.configuration = configuration
        importer.configuration.xtffile = testdata_path('xtf/test_ladm_col_queries_v2.9.6.xtf')
        self.assertEqual(importer.run(), iliimporter.Importer.SUCCESS)

        generator = Generator(
            DbIliMode.ili2pg,
            'dbname={} user={} password={} host={}'.format(configuration.database, configuration.dbusr,
                                                           configuration.dbpwd, configuration.dbhost),
            configuration.inheritance,
            importer.configuration.dbschema)

        available_layers = generator.layers()
        self.assertEqual(len(available_layers), 193)

        result = db_pg.test_connection()
        self.assertTrue(result[0], 'The test connection is not working')
        test_layer = self.qgis_utils.get_layer(db_pg, db_pg.names.OP_BOUNDARY_POINT_T, load=True)

        self.assertEqual(test_layer.featureCount(), 390)
        db_pg.conn.close()

    def test_import_data_in_gpkg(self):
        print("\nINFO: Validate Import Data in GPKG...")

        gpkg_path = get_test_copy_path('geopackage/test_import_data.gpkg')

        base_config = BaseConfiguration()
        base_config.custom_model_directories = testdata_path('models/LADM_COL')
        base_config.custom_model_directories_enabled = True

        configuration = ImportDataConfiguration()
        configuration.base_configuration = base_config

        configuration.tool = DbIliMode.ili2gpkg
        configuration.dbfile = gpkg_path
        configuration.epsg = DEFAULT_EPSG
        configuration.inheritance = LADMNames.DEFAULT_INHERITANCE
        configuration.create_basket_col = LADMNames.CREATE_BASKET_COL
        configuration.create_import_tid = LADMNames.CREATE_IMPORT_TID
        configuration.stroke_arcs = LADMNames.STROKE_ARCS
        configuration.delete_data = True
        configuration.ilimodels = ';'.join([LADMNames.SUPPORTED_LADM_MODEL,
                                            LADMNames.SUPPORTED_SNR_DATA_MODEL,
                                            LADMNames.SUPPORTED_SUPPLIES_MODEL,
                                            LADMNames.SUPPORTED_SUPPLIES_INTEGRATION_MODEL,
                                            LADMNames.SUPPORTED_OPERATION_MODEL,
                                            LADMNames.SUPPORTED_ANT_MODEL,
                                            LADMNames.SUPPORTED_CADASTRAL_FORM_MODEL,
                                            LADMNames.SUPPORTED_VALUATION_MODEL])
        importer = iliimporter.Importer(dataImport=True)
        importer.tool = DbIliMode.ili2gpkg
        importer.configuration = configuration
        importer.configuration.xtffile = testdata_path('xtf/test_ladm_col_queries_v2.9.6.xtf')
        self.assertEqual(importer.run(), iliimporter.Importer.SUCCESS)

        config_manager = GpkgCommandConfigManager(importer.configuration)
        generator = Generator(DbIliMode.ili2gpkg, config_manager.get_uri(), configuration.inheritance)

        available_layers = generator.layers()
        self.assertEqual(len(available_layers), 193)

        db_gpkg = get_gpkg_conn_from_path(config_manager.get_uri())
        result = db_gpkg.test_connection()
        self.assertTrue(result[0], 'The test connection is not working')
        test_layer = self.qgis_utils.get_layer(db_gpkg, db_gpkg.names.OP_BOUNDARY_POINT_T, load=True)
        self.assertEqual(test_layer.featureCount(), 390)
        db_gpkg.conn.close()

    def test_import_schema_in_pg(self):
        print("\nINFO: Validate Import Schema in PG...")
        base_config = BaseConfiguration()
        base_config.custom_model_directories = testdata_path('xtf') +';' +testdata_path('models/LADM_COL')
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
        configuration.epsg = DEFAULT_EPSG
        configuration.inheritance = LADMNames.DEFAULT_INHERITANCE
        configuration.create_basket_col = LADMNames.CREATE_BASKET_COL
        configuration.create_import_tid = LADMNames.CREATE_IMPORT_TID
        configuration.stroke_arcs = LADMNames.STROKE_ARCS
        configuration.ilimodels = ';'.join([LADMNames.SUPPORTED_LADM_MODEL,
                                            LADMNames.SUPPORTED_SNR_DATA_MODEL,
                                            LADMNames.SUPPORTED_SUPPLIES_MODEL,
                                            LADMNames.SUPPORTED_SUPPLIES_INTEGRATION_MODEL,
                                            LADMNames.SUPPORTED_OPERATION_MODEL,
                                            LADMNames.SUPPORTED_ANT_MODEL,
                                            LADMNames.SUPPORTED_CADASTRAL_FORM_MODEL,
                                            LADMNames.SUPPORTED_REFERENCE_CARTOGRAPHY,
                                            LADMNames.SUPPORTED_VALUATION_MODEL])

        importer = iliimporter.Importer()
        importer.tool = DbIliMode.ili2pg
        importer.configuration = configuration

        self.assertEqual(importer.run(), iliimporter.Importer.SUCCESS)

        generator = Generator(
            DbIliMode.ili2pg,
            'dbname={} user={} password={} host={}'.format(configuration.database, configuration.dbusr, configuration.dbpwd, configuration.dbhost),
            configuration.inheritance,
            importer.configuration.dbschema)

        available_layers = generator.layers()
        self.assertEqual(len(available_layers), 211)

    def test_import_schema_in_gpkg(self):
        print("\nINFO: Validate Import Schema in GPKG...")
        base_config = BaseConfiguration()
        base_config.custom_model_directories = testdata_path('models/LADM_COL')
        base_config.custom_model_directories_enabled = True

        configuration = SchemaImportConfiguration()
        configuration.base_configuration = base_config
        configuration.tool = DbIliMode.ili2gpkg
        configuration.dbfile = os.path.join(tempfile.mkdtemp(), 'tmp_import_schema.gpkg')
        configuration.tomlfile = TOML_FILE_DIR
        configuration.epsg = DEFAULT_EPSG
        configuration.inheritance = LADMNames.DEFAULT_INHERITANCE
        configuration.create_basket_col = LADMNames.CREATE_BASKET_COL
        configuration.create_import_tid = LADMNames.CREATE_IMPORT_TID
        configuration.stroke_arcs = LADMNames.STROKE_ARCS
        configuration.ilimodels = ';'.join([LADMNames.SUPPORTED_LADM_MODEL,
                                            LADMNames.SUPPORTED_SNR_DATA_MODEL,
                                            LADMNames.SUPPORTED_SUPPLIES_MODEL,
                                            LADMNames.SUPPORTED_SUPPLIES_INTEGRATION_MODEL,
                                            LADMNames.SUPPORTED_OPERATION_MODEL,
                                            LADMNames.SUPPORTED_ANT_MODEL,
                                            LADMNames.SUPPORTED_CADASTRAL_FORM_MODEL,
                                            LADMNames.SUPPORTED_REFERENCE_CARTOGRAPHY,
                                            LADMNames.SUPPORTED_VALUATION_MODEL])

        importer = iliimporter.Importer()
        importer.tool = DbIliMode.ili2gpkg
        importer.configuration = configuration

        self.assertEqual(importer.run(), iliimporter.Importer.SUCCESS)

        config_manager = GpkgCommandConfigManager(importer.configuration)
        generator = Generator(DbIliMode.ili2gpkg, config_manager.get_uri(), configuration.inheritance)

        available_layers = generator.layers()
        self.assertEqual(len(available_layers), 211)

if __name__ == '__main__':
    nose2.main()