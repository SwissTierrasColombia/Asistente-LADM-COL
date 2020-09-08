import nose2

from qgis.testing import (start_app,
                          unittest)

start_app() # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.tests.utils import (get_required_fields,
                                            get_required_tables,
                                            import_qgis_model_baker,
                                            unload_qgis_model_baker)
from asistente_ladm_col.config.ili2db_names import *
from asistente_ladm_col.tests.utils import (get_pg_conn,
                                            get_gpkg_conn,
                                            restore_schema)


class TestAllModels(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("INFO: Restoring databases to be used")
        import_qgis_model_baker()
        restore_schema('test_ladm_all_models')
        cls.db_pg = get_pg_conn('test_ladm_all_models')
        cls.db_gpkg = get_gpkg_conn('test_ladm_all_models_gpkg')

    def test_required_models_pg(self):
        print("\nINFO: Validate if the schema for all models in PG...")
        res, code, msg = self.db_pg.test_connection()
        self.assertTrue(res, msg)
        self.check_required_models(self.db_pg)

    def test_required_models_gpkg(self):
        print("\nINFO: Validate if the schema for all models in GPKG...")
        res, code, msg = self.db_gpkg.test_connection()
        self.assertTrue(res, msg)
        self.check_required_models(self.db_gpkg)

    def check_required_models(self, db_connection):
        self.assertTrue(db_connection.supplies_model_exists())
        self.assertTrue(db_connection.snr_data_model_exists())
        self.assertTrue(db_connection.supplies_integration_model_exists())
        self.assertTrue(db_connection.survey_model_exists())
        self.assertTrue(db_connection.valuation_model_exists())
        self.assertTrue(db_connection.cadastral_cartography_model_exists())

    def test_names_from_model_pg(self):
        print("\nINFO: Validate names for all model in PG...")
        res, code, msg = self.db_pg.test_connection()
        self.assertTrue(res, msg)

        dict_names = self.db_pg.get_db_mapping()
        self.assertEqual(len(dict_names), 195)

        expected_dict = {T_ID_KEY: 't_id',
                         T_ILI_TID_KEY: "t_ili_tid",
                         ILICODE_KEY: 'ilicode',
                         DESCRIPTION_KEY: 'description',
                         DISPLAY_NAME_KEY: 'dispname',
                         "LADM_COL.LADM_Nucleo.col_masCcl": {
                             "table_name": "col_masccl",
                             "LADM_COL.LADM_Nucleo.col_masCcl.ccl_mas..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Lindero": "ccl_mas",
                             "LADM_COL.LADM_Nucleo.col_masCcl.ue_mas..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_UnidadConstruccion": "ue_mas_lc_unidadconstruccion",
                             "LADM_COL.LADM_Nucleo.col_masCcl.ue_mas..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Construccion": "ue_mas_lc_construccion",
                             "LADM_COL.LADM_Nucleo.col_masCcl.ue_mas..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_ServidumbreTransito": "ue_mas_lc_servidumbretransito",
                             "LADM_COL.LADM_Nucleo.col_masCcl.ue_mas..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Terreno": "ue_mas_lc_terreno"
                         },
                         "Submodelo_Integracion_Insumos.Datos_Integracion_Insumos.INI_PredioInsumos": {
                             "table_name": "ini_predioinsumos",
                             "Submodelo_Integracion_Insumos.Datos_Integracion_Insumos.INI_PredioInsumos.Observaciones": "observaciones",
                             "Submodelo_Integracion_Insumos.Datos_Integracion_Insumos.INI_PredioInsumos.Tipo_Emparejamiento": "tipo_emparejamiento",
                             "Submodelo_Integracion_Insumos.Datos_Integracion_Insumos.ini_predio_integracion_gc.gc_predio_catastro..Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_PredioCatastro": "gc_predio_catastro",
                             "Submodelo_Integracion_Insumos.Datos_Integracion_Insumos.ini_predio_integracion_snr.snr_predio_juridico..Submodelo_Insumos_SNR.Datos_SNR.SNR_PredioRegistro": "snr_predio_juridico"
                         },
                         "Submodelo_Avaluos.Avaluos.AV_TablaCalificacionConstruccion": {
                             "table_name": "av_tablacalificacionconstruccion",
                             "Submodelo_Avaluos.Avaluos.AV_TablaCalificacionConstruccion.Puntuacion": "puntuacion",
                             "Submodelo_Avaluos.Avaluos.AV_TablaCalificacionConstruccion.Uso": "uso",
                             "Submodelo_Avaluos.Avaluos.AV_TablaCalificacionConstruccion.Valor_M2_Construccion": "valor_m2_construccion"
                         }}

        for k,v in expected_dict.items():
            self.assertIn(k, dict_names)
            self.assertEqual(v, dict_names[k])

    def test_names_from_model_gpkg(self):
        print("\nINFO: Validate names for all model in GPKG...")
        res, code, msg = self.db_gpkg.test_connection()
        self.assertTrue(res, msg)

        dict_names = self.db_gpkg.get_db_mapping()
        self.assertEqual(len(dict_names), 195)

        expected_dict = {T_ID_KEY: 'T_Id',
                         T_ILI_TID_KEY: "T_Ili_Tid",
                         ILICODE_KEY: 'iliCode',
                         DESCRIPTION_KEY: 'description',
                         DISPLAY_NAME_KEY: 'dispName',
                         "LADM_COL.LADM_Nucleo.col_masCcl": {
                             "table_name": "col_masccl",
                             "LADM_COL.LADM_Nucleo.col_masCcl.ccl_mas..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Lindero": "ccl_mas",
                             "LADM_COL.LADM_Nucleo.col_masCcl.ue_mas..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_UnidadConstruccion": "ue_mas_lc_unidadconstruccion",
                             "LADM_COL.LADM_Nucleo.col_masCcl.ue_mas..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Construccion": "ue_mas_lc_construccion",
                             "LADM_COL.LADM_Nucleo.col_masCcl.ue_mas..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_ServidumbreTransito": "ue_mas_lc_servidumbretransito",
                             "LADM_COL.LADM_Nucleo.col_masCcl.ue_mas..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Terreno": "ue_mas_lc_terreno"
                         },
                         "Submodelo_Integracion_Insumos.Datos_Integracion_Insumos.INI_PredioInsumos": {
                             "table_name": "ini_predioinsumos",
                             "Submodelo_Integracion_Insumos.Datos_Integracion_Insumos.INI_PredioInsumos.Observaciones": "observaciones",
                             "Submodelo_Integracion_Insumos.Datos_Integracion_Insumos.INI_PredioInsumos.Tipo_Emparejamiento": "tipo_emparejamiento",
                             "Submodelo_Integracion_Insumos.Datos_Integracion_Insumos.ini_predio_integracion_gc.gc_predio_catastro..Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_PredioCatastro": "gc_predio_catastro",
                             "Submodelo_Integracion_Insumos.Datos_Integracion_Insumos.ini_predio_integracion_snr.snr_predio_juridico..Submodelo_Insumos_SNR.Datos_SNR.SNR_PredioRegistro": "snr_predio_juridico"
                         },
                         "Submodelo_Avaluos.Avaluos.AV_TablaCalificacionConstruccion": {
                             "table_name": "av_tablacalificacionconstruccion",
                             "Submodelo_Avaluos.Avaluos.AV_TablaCalificacionConstruccion.Puntuacion": "puntuacion",
                             "Submodelo_Avaluos.Avaluos.AV_TablaCalificacionConstruccion.Uso": "uso",
                             "Submodelo_Avaluos.Avaluos.AV_TablaCalificacionConstruccion.Valor_M2_Construccion": "valor_m2_construccion"
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
        test_required_tables = ['MORE_BFS_T', 'LESS_BFS_T', 'POINT_BFS_T', 'COL_POINT_SOURCE_T', 'COL_RRR_SOURCE_T', 'COL_UE_BAUNIT_T', 'COL_UE_SOURCE_T', 'COL_BAUNIT_SOURCE_T', 'COL_CCL_SOURCE_T', 'LC_BUILDING_TYPE_D', 'LC_DOMAIN_BUILDING_TYPE_D', 'LC_BUILDING_UNIT_TYPE_D', 'LC_GROUP_PARTY_T', 'LC_BUILDING_UNIT_T', 'LC_BUILDING_T', 'LC_RIGHT_T', 'LC_ADMINISTRATIVE_SOURCE_T', 'LC_SPATIAL_SOURCE_T', 'LC_PARTY_T', 'LC_BOUNDARY_T', 'LC_PARCEL_T', 'LC_BOUNDARY_POINT_T', 'LC_RESTRICTION_T', 'LC_RIGHT_OF_WAY_T', 'LC_PLOT_T', 'LC_ADMINISTRATIVE_SOURCE_TYPE_D', 'LC_PARTY_TYPE_D', 'LC_PARCEL_TYPE_D', 'LC_CONTROL_POINT_TYPE_D', 'LC_SURVEY_POINT_TYPE_D', 'LC_POINT_TYPE_D', 'GC_PARCEL_T', 'GC_OWNER_T', 'GC_PLOT_T', 'GC_BUILDING_UNIT_T', 'INI_PARCEL_SUPPLIES_T', 'SNR_RIGHT_T', 'SNR_SOURCE_RIGHT_T', 'SNR_PARCEL_REGISTRY_T', 'SNR_TITLE_HOLDER_T', 'EXT_ARCHIVE_S']
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
        test_required_fields = ['EXT_ARCHIVE_S_DATA_F', 'FRACTION_S_NUMERATOR_F', 'MORE_BFS_T_LC_BOUNDARY_F','MORE_BFS_T_LC_PLOT_F', 'MORE_BFS_T_LC_BUILDING_UNIT_F', 'LESS_BFS_T_LC_BOUNDARY_F', 'FRACTION_S_MEMBER_F', 'MEMBERS_T_GROUP_PARTY_F', 'MEMBERS_T_PARTY_F', 'POINT_BFS_T_LC_BOUNDARY_F', 'POINT_BFS_T_LC_CONTROL_POINT_F', 'POINT_BFS_T_LC_SURVEY_POINT_F', 'POINT_BFS_T_LC_BOUNDARY_POINT_F', 'COL_POINT_SOURCE_T_SOURCE_F', 'COL_POINT_SOURCE_T_LC_CONTROL_POINT_F', 'COL_UE_BAUNIT_T_LC_BUILDING_F', 'COL_UE_BAUNIT_T_LC_BUILDING_UNIT_F', 'COL_UE_BAUNIT_T_LC_RIGHT_OF_WAY_F', 'COL_UE_SOURCE_T_SOURCE_F', 'COL_UE_SOURCE_T_LC_BUILDING_F', 'COL_UE_SOURCE_T_LC_RIGHT_OF_WAY_F', 'COL_UE_SOURCE_T_LC_PLOT_F']
        required_fields = get_required_fields(db_connection)

        for test_required_field in test_required_fields:
            self.assertIn(test_required_field, required_fields)

    @classmethod
    def tearDownClass(cls):
        print("INFO: Closing open connections to databases")
        cls.db_pg.conn.close()
        cls.db_gpkg.conn.close()
        unload_qgis_model_baker()


if __name__ == '__main__':
    nose2.main()

