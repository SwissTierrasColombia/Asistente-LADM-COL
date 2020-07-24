import nose2

from qgis.testing import (start_app,
                          unittest)

start_app() # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.tests.utils import (get_required_fields,
                                            get_required_tables)
from asistente_ladm_col.config.mapping_config import (ILICODE_KEY,
                                                      T_ID_KEY,
                                                      T_ILI_TID_KEY,
                                                      DESCRIPTION_KEY,
                                                      DISPLAY_NAME_KEY)
from asistente_ladm_col.tests.utils import (get_pg_conn,
                                            get_gpkg_conn,
                                            restore_schema)


class TestIntegrationSuppliesModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("INFO: Restoring databases to be used")
        restore_schema('test_ladm_integration')
        cls.db_pg = get_pg_conn('test_ladm_integration')
        cls.db_gpkg = get_gpkg_conn('test_ladm_integration_gpkg')

    def test_required_models_pg(self):
        print("\nINFO: Validate if the schema for integration supplies model model in PG...")
        res, code, msg = self.db_pg.test_connection()
        self.assertTrue(res, msg)
        self.check_required_models(self.db_pg)

    def test_required_models_gpkg(self):
        print("\nINFO: Validate if the schema for integration supplies model model in GPKG...")
        res, code, msg = self.db_gpkg.test_connection()
        self.assertTrue(res, msg)
        self.check_required_models(self.db_gpkg)

    def check_required_models(self, db_connection):
        self.assertTrue(db_connection.supplies_model_exists())
        self.assertTrue(db_connection.snr_data_model_exists())
        self.assertTrue(db_connection.supplies_integration_model_exists())
        self.assertFalse(db_connection.survey_model_exists())
        self.assertFalse(db_connection.valuation_model_exists())
        self.assertFalse(db_connection.cadastral_cartography_model_exists())

    def test_names_from_model_pg(self):
        print("\nINFO: Validate names for Integration Supplies model in PG...")
        res, code, msg = self.db_pg.test_connection()
        self.assertTrue(res, msg)

        dict_names = self.db_pg.get_table_and_field_names()
        self.assertEqual(len(dict_names), 47)
        expected_dict = {T_ID_KEY: 't_id',
                         T_ILI_TID_KEY: "t_ili_tid",
                         ILICODE_KEY: 'ilicode',
                         DESCRIPTION_KEY: 'description',
                         DISPLAY_NAME_KEY: 'dispname',
                         "Submodelo_Integracion_Insumos.Datos_Integracion_Insumos.INI_PredioInsumos": {
                             "table_name": "ini_predioinsumos",
                             "Submodelo_Integracion_Insumos.Datos_Integracion_Insumos.INI_PredioInsumos.Observaciones": "observaciones",
                             "Submodelo_Integracion_Insumos.Datos_Integracion_Insumos.INI_PredioInsumos.Tipo_Emparejamiento": "tipo_emparejamiento",
                             "Submodelo_Integracion_Insumos.Datos_Integracion_Insumos.ini_predio_integracion_gc.gc_predio_catastro..Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_PredioCatastro": "gc_predio_catastro",
                             "Submodelo_Integracion_Insumos.Datos_Integracion_Insumos.ini_predio_integracion_snr.snr_predio_juridico..Submodelo_Insumos_SNR.Datos_SNR.SNR_PredioRegistro": "snr_predio_juridico"
                         }}

        for k,v in expected_dict.items():
            self.assertIn(k, dict_names)
            self.assertEqual(v, dict_names[k])

    def test_names_from_model_gpkg(self):
        print("\nINFO: Validate names for Integration Supplies model in GPKG...")
        res, code, msg = self.db_gpkg.test_connection()
        self.assertTrue(res, msg)

        dict_names = self.db_gpkg.get_table_and_field_names()
        self.assertEqual(len(dict_names), 47)
        expected_dict = {T_ID_KEY: 'T_Id',
                         T_ILI_TID_KEY: "T_Ili_Tid",
                         ILICODE_KEY: 'iliCode',
                         DESCRIPTION_KEY: 'description',
                         DISPLAY_NAME_KEY: 'dispName',
                         "Submodelo_Integracion_Insumos.Datos_Integracion_Insumos.INI_PredioInsumos": {
                             "table_name": "ini_predioinsumos",
                             "Submodelo_Integracion_Insumos.Datos_Integracion_Insumos.INI_PredioInsumos.Observaciones": "observaciones",
                             "Submodelo_Integracion_Insumos.Datos_Integracion_Insumos.INI_PredioInsumos.Tipo_Emparejamiento": "tipo_emparejamiento",
                             "Submodelo_Integracion_Insumos.Datos_Integracion_Insumos.ini_predio_integracion_gc.gc_predio_catastro..Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_PredioCatastro": "gc_predio_catastro",
                             "Submodelo_Integracion_Insumos.Datos_Integracion_Insumos.ini_predio_integracion_snr.snr_predio_juridico..Submodelo_Insumos_SNR.Datos_SNR.SNR_PredioRegistro": "snr_predio_juridico"
                         }}

        for k,v in expected_dict.items():
            self.assertIn(k, dict_names)
            self.assertEqual(v, dict_names[k])

    def test_required_table_names_pg(self):
        print("\nINFO: Validate minimum required tables from names in PG...")
        res, code, msg = self.db_pg.test_connection()
        self.assertTrue(res, msg)
        self.check_required_table_names(self.db_pg)

    def test_required_table_names_gpkg(self):
        print("\nINFO: Validate minimum required tables from names in GPKG...")
        res, code, msg = self.db_gpkg.test_connection()
        self.assertTrue(res, msg)
        self.check_required_table_names(self.db_gpkg)

    def check_required_table_names(self, db_connection):
        test_required_tables = ['GC_PARCEL_T', 'GC_OWNER_T', 'GC_PLOT_T', 'GC_BUILDING_UNIT_T', 'INI_PARCEL_SUPPLIES_T', 'SNR_RIGHT_T', 'SNR_SOURCE_RIGHT_T', 'SNR_PARCEL_REGISTRY_T', 'SNR_TITLE_HOLDER_T', 'EXT_ARCHIVE_S']
        required_tables = get_required_tables(db_connection)

        for test_required_table in test_required_tables:
            self.assertIn(test_required_table, required_tables)

    def test_required_field_names_pg(self):
        print("\nINFO: Validate minimum required fields from names in PG...")
        res, code, msg = self.db_pg.test_connection()
        self.assertTrue(res, msg)
        self.check_required_field_names(self.db_pg)

    def test_required_field_names_gpkg(self):
        print("\nINFO: Validate minimum required fields from names in GPKG...")
        res, code, msg = self.db_gpkg.test_connection()
        self.assertTrue(res, msg)
        self.check_required_field_names(self.db_gpkg)

    def check_required_field_names(self, db_connection):
        test_required_fields = ['EXT_ARCHIVE_S_DATA_F', 'EXT_ARCHIVE_S_EXTRACTION_F']
        required_fields = get_required_fields(db_connection)

        for test_required_field in test_required_fields:
            self.assertIn(test_required_field, required_fields)

    @classmethod
    def tearDownClass(cls):
        print("INFO: Closing open connections to databases")
        cls.db_pg.conn.close()
        cls.db_gpkg.conn.close()


if __name__ == '__main__':
    nose2.main()

