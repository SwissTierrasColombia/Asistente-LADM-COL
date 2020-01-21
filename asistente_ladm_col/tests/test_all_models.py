import nose2

from qgis.testing import (start_app,
                          unittest)

start_app() # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.tests.utils import (get_required_fields,
                                            get_required_tables)
from asistente_ladm_col.config.table_mapping_config import (ILICODE,
                                                            T_ID,
                                                            DESCRIPTION,
                                                            DISPLAY_NAME)
from asistente_ladm_col.tests.utils import (get_dbconn,
                                            restore_schema)


class TestAllModels(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        restore_schema('test_ladm_all_models')
        self.db_connection_pg = get_dbconn('test_ladm_all_models')

    def test_required_models_pg(self):
        print("\nINFO: Validate if the schema for all models...")
        result = self.db_connection_pg.test_connection()
        self.assertTrue(result[0], 'The test connection is not working')
        self.check_required_models(self.db_connection_pg)

    def check_required_models(self, db_connection):
        self.assertTrue(db_connection.supplies_model_exists())
        self.assertTrue(db_connection.snr_data_model_exists())
        self.assertTrue(db_connection.supplies_integration_model_exists())
        self.assertTrue(db_connection.operation_model_exists())
        self.assertTrue(db_connection.valuation_model_exists())
        self.assertTrue(db_connection.cadastral_form_model_exists())
        self.assertTrue(db_connection.ant_model_exists())
        self.assertTrue(db_connection.reference_cartography_model_exists())

    def test_names_from_model_pg(self):
        print("\nINFO: Validate names for all model...")
        result = self.db_connection_pg.test_connection()
        self.assertTrue(result[0], 'The test connection is not working')

        dict_names = self.db_connection_pg.get_table_and_field_names()
        self.assertEqual(len(dict_names), 215)

        expected_dict = {T_ID: 't_id',
                         ILICODE: 'ilicode',
                         DESCRIPTION: 'description',
                         DISPLAY_NAME: 'dispname',
                         'LADM_COL.LADM_Nucleo.col_masCcl': {
                             'table_name': 'col_masccl',
                             'LADM_COL.LADM_Nucleo.col_masCcl.ccl_mas..Operacion.Operacion.OP_Lindero': 'ccl_mas_op_lindero',
                             'LADM_COL.LADM_Nucleo.col_masCcl.ccl_mas..Cartografia_Referencia.Auxiliares.CRF_EstructuraLineal': 'ccl_mas_crf_estructuralineal',
                             'LADM_COL.LADM_Nucleo.col_masCcl.ue_mas..Operacion.Operacion.OP_UnidadConstruccion': 'ue_mas_op_unidadconstruccion',
                             'LADM_COL.LADM_Nucleo.col_masCcl.ue_mas..Operacion.Operacion.OP_Construccion': 'ue_mas_op_construccion',
                             'LADM_COL.LADM_Nucleo.col_masCcl.ue_mas..Operacion.Operacion.OP_Terreno': 'ue_mas_op_terreno',
                             'LADM_COL.LADM_Nucleo.col_masCcl.ue_mas..Operacion.Operacion.OP_ServidumbrePaso': 'ue_mas_op_servidumbrepaso'
                         },
                         'Datos_Integracion_Insumos.Datos_Integracion_Insumos.INI_Predio_Insumos': {
                             'table_name': 'ini_predio_insumos',
                             'Datos_Integracion_Insumos.Datos_Integracion_Insumos.ini_predio_integracion_gc.gc_predio_catastro..Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Predio_Catastro': 'gc_predio_catastro',
                             'Datos_Integracion_Insumos.Datos_Integracion_Insumos.ini_predio_integracion_snr.snr_predio_juridico..Datos_SNR.Datos_SNR.SNR_Predio_Registro': 'snr_predio_juridico'
                         },
                         'ANT.Fiso.ANT_Conflictos': {
                             'table_name': 'ant_conflictos',
                             'ANT.Fiso.ANT_Conflictos.Conflicto': 'conflicto',
                             'ANT.Fiso.ANT_Conflictos.Descripcion': 'descripcion',
                             'ANT.Fiso.ant_conflictos_predio.op_predio..Operacion.Operacion.OP_Predio': 'op_predio'
                         }}

        for k,v in expected_dict.items():
            self.assertIn(k, dict_names)
            self.assertEqual(v, dict_names[k])

    def test_required_table_names_pg(self):
        print("\nINFO: Validate minimum required tables from names...")
        result = self.db_connection_pg.test_connection()
        self.assertTrue(result[0], 'The test connection is not working')
        self.check_required_table_names(self.db_connection_pg)

    def check_required_table_names(self, db_connection):
        test_required_tables = ['MORE_BFS_T', 'LESS_BFS_T', 'POINT_BFS_T', 'COL_POINT_SOURCE_T', 'COL_RRR_SOURCE_T', 'COL_UE_BAUNIT_T', 'COL_UE_SOURCE_T', 'COL_BAUNIT_SOURCE_T', 'COL_CCL_SOURCE_T', 'OP_BUILDING_TYPE_D', 'OP_DOMAIN_BUILDING_TYPE_D', 'OP_BUILDING_UNIT_TYPE_D', 'OP_GROUP_PARTY_T', 'OP_BUILDING_UNIT_T', 'OP_BUILDING_T', 'OP_RIGHT_T', 'OP_ADMINISTRATIVE_SOURCE_T', 'OP_SPATIAL_SOURCE_T', 'OP_PARTY_T', 'OP_BOUNDARY_T', 'OP_PARCEL_T', 'OP_BOUNDARY_POINT_T', 'OP_RESTRICTION_T', 'OP_RIGHT_OF_WAY_T', 'OP_PLOT_T', 'OP_ADMINISTRATIVE_SOURCE_TYPE_D', 'OP_PARTY_TYPE_D', 'OP_PARCEL_TYPE_D', 'OP_CONTROL_POINT_TYPE_D', 'OP_SURVEY_POINT_TYPE_D', 'OP_POINT_TYPE_D', 'GC_PARCEL_T', 'GC_OWNER_T', 'GC_PLOT_T', 'GC_BUILDING_UNIT_T', 'INI_PARCEL_SUPPLIES_T', 'SNR_RIGHT_T', 'SNR_SOURCE_RIGHT_T', 'SNR_PARCEL_REGISTRY_T', 'SNR_TITLE_HOLDER_T', 'EXT_ARCHIVE_S']
        required_tables = get_required_tables(db_connection)

        for test_required_table in test_required_tables:
            self.assertIn(test_required_table, required_tables)

    def test_required_field_names_pg(self):
        print("\nINFO: Validate minimum required fields from names...")
        result = self.db_connection_pg.test_connection()
        self.assertTrue(result[0], 'The test connection is not working')
        self.check_required_field_names(self.db_connection_pg)

    def check_required_field_names(self, db_connection):
        test_required_fields = ['EXT_ARCHIVE_S_DATA_F', 'FRACTION_S_NUMERATOR_F', 'MORE_BFS_T_OP_BOUNDARY_F','MORE_BFS_T_OP_PLOT_F', 'MORE_BFS_T_OP_BUILDING_UNIT_F', 'LESS_BFS_T_OP_BOUNDARY_F', 'MORE_BFS_T_CRF_LINEAR_STRUCTURE_F', 'LESS_BFS_T_CRF_LINEAR_STRUCTURE_F', 'POINT_BFS_T_CRF_LINEAR_STRUCTURE_F', 'FRACTION_S_MEMBER_F', 'MEMBERS_T_GROUP_PARTY_F', 'MEMBERS_T_PARTY_F', 'POINT_BFS_T_OP_BOUNDARY_F', 'POINT_BFS_T_OP_CONTROL_POINT_F', 'POINT_BFS_T_OP_SURVEY_POINT_F', 'POINT_BFS_T_OP_BOUNDARY_POINT_F', 'COL_POINT_SOURCE_T_SOURCE_F', 'COL_POINT_SOURCE_T_OP_CONTROL_POINT_F', 'COL_UE_BAUNIT_T_OP_BUILDING_F', 'COL_UE_BAUNIT_T_OP_BUILDING_UNIT_F', 'COL_UE_BAUNIT_T_OP_RIGHT_OF_WAY_F', 'COL_UE_SOURCE_T_SOURCE_F', 'COL_UE_SOURCE_T_OP_BUILDING_F', 'COL_UE_SOURCE_T_OP_RIGHT_OF_WAY_F', 'COL_UE_SOURCE_T_OP_PLOT_F']
        required_fields = get_required_fields(db_connection)

        for test_required_field in test_required_fields:
            self.assertIn(test_required_field, required_fields)

    @classmethod
    def tearDownClass(self):
        self.db_connection_pg.conn.close()


if __name__ == '__main__':
    nose2.main()

