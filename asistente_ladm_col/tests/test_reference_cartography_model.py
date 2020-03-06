import nose2

from qgis.testing import (start_app,
                          unittest)

start_app() # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.tests.utils import (get_required_fields,
                                            get_required_tables)
from asistente_ladm_col.config.mapping_config import (ILICODE_KEY,
                                                      T_ID_KEY,
                                                      DESCRIPTION_KEY,
                                                      DISPLAY_NAME_KEY)
from asistente_ladm_col.tests.utils import (get_pg_conn,
                                            get_gpkg_conn,
                                            restore_schema)


class TestReferenceCartographyModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("INFO: Restoring databases to be used")
        restore_schema('test_ladm_reference_cartography')
        cls.db_pg = get_pg_conn('test_ladm_reference_cartography')
        cls.db_gpkg = get_gpkg_conn('test_ladm_reference_cartography_gpkg')

    def test_required_models_pg(self):
        print("\nINFO: Validate if the schema for reference cartography model in PG...")
        result = self.db_pg.test_connection()
        self.assertTrue(result[0], 'The test connection is not working')
        self.check_required_models(self.db_pg)

    def test_required_models_gpkg(self):
        print("\nINFO: Validate if the schema for reference cartography model in GPKG...")
        result = self.db_gpkg.test_connection()
        self.assertTrue(result[0], 'The test connection is not working')
        self.check_required_models(self.db_gpkg)

    def check_required_models(self, db_connection):
        self.assertTrue(db_connection.supplies_model_exists())
        self.assertTrue(db_connection.snr_data_model_exists())
        self.assertTrue(db_connection.supplies_integration_model_exists())
        self.assertTrue(db_connection.operation_model_exists())
        self.assertFalse(db_connection.valuation_model_exists())
        self.assertFalse(db_connection.cadastral_form_model_exists())
        self.assertFalse(db_connection.ant_model_exists())
        self.assertTrue(db_connection.reference_cartography_model_exists())

    def test_names_from_model_pg(self):
        print("\nINFO: Validate names for Reference Cartography data model (edge case for field keys)...")
        result = self.db_pg.test_connection()
        self.assertTrue(result[0], 'The test connection is not working')

        dict_names = self.db_pg.get_table_and_field_names()
        self.assertEqual(len(dict_names), 161)

        expected_dict = {T_ID_KEY: 't_id',
                         ILICODE_KEY: 'ilicode',
                         DESCRIPTION_KEY: 'description',
                         DISPLAY_NAME_KEY: 'dispname',
                         'LADM_COL.LADM_Nucleo.col_masCcl': {'table_name': 'col_masccl',
                             'LADM_COL.LADM_Nucleo.col_masCcl.ccl_mas..Operacion.Operacion.OP_Lindero': 'ccl_mas_op_lindero',
                             'LADM_COL.LADM_Nucleo.col_masCcl.ccl_mas..Cartografia_Referencia.Auxiliares.CRF_EstructuraLineal': 'ccl_mas_crf_estructuralineal',
                             'LADM_COL.LADM_Nucleo.col_masCcl.ue_mas..Operacion.Operacion.OP_Construccion': 'ue_mas_op_construccion',
                             'LADM_COL.LADM_Nucleo.col_masCcl.ue_mas..Operacion.Operacion.OP_ServidumbrePaso': 'ue_mas_op_servidumbrepaso',
                             'LADM_COL.LADM_Nucleo.col_masCcl.ue_mas..Operacion.Operacion.OP_Terreno': 'ue_mas_op_terreno',
                             'LADM_COL.LADM_Nucleo.col_masCcl.ue_mas..Operacion.Operacion.OP_UnidadConstruccion': 'ue_mas_op_unidadconstruccion'}}

        for k,v in expected_dict.items():
            self.assertIn(k, dict_names)
            self.assertEqual(v, dict_names[k])

    def test_names_from_model_gpkg(self):
        print("\nINFO: Validate names for Reference Cartography data model (edge case for field keys) in GPKG...")
        result = self.db_gpkg.test_connection()
        self.assertTrue(result[0], 'The test connection is not working')

        dict_names = self.db_gpkg.get_table_and_field_names()
        self.assertEqual(len(dict_names), 161)

        expected_dict = {T_ID_KEY: 'T_Id',
                         ILICODE_KEY: 'iliCode',
                         DESCRIPTION_KEY: 'description',
                         DISPLAY_NAME_KEY: 'dispName',
                         'LADM_COL.LADM_Nucleo.col_masCcl': {'table_name': 'col_masccl',
                             'LADM_COL.LADM_Nucleo.col_masCcl.ccl_mas..Operacion.Operacion.OP_Lindero': 'ccl_mas_op_lindero',
                             'LADM_COL.LADM_Nucleo.col_masCcl.ccl_mas..Cartografia_Referencia.Auxiliares.CRF_EstructuraLineal': 'ccl_mas_crf_estructuralineal',
                             'LADM_COL.LADM_Nucleo.col_masCcl.ue_mas..Operacion.Operacion.OP_Construccion': 'ue_mas_op_construccion',
                             'LADM_COL.LADM_Nucleo.col_masCcl.ue_mas..Operacion.Operacion.OP_ServidumbrePaso': 'ue_mas_op_servidumbrepaso',
                             'LADM_COL.LADM_Nucleo.col_masCcl.ue_mas..Operacion.Operacion.OP_Terreno': 'ue_mas_op_terreno',
                             'LADM_COL.LADM_Nucleo.col_masCcl.ue_mas..Operacion.Operacion.OP_UnidadConstruccion': 'ue_mas_op_unidadconstruccion'}}

        for k,v in expected_dict.items():
            self.assertIn(k, dict_names)
            self.assertEqual(v, dict_names[k])

    def test_required_table_names_pg(self):
        print("\nINFO: Validate minimum required tables from names in PG...")
        result = self.db_pg.test_connection()
        self.assertTrue(result[0], 'The test connection is not working')
        self.check_required_table_names(self.db_pg)

    def test_required_table_names_gpkg(self):
        print("\nINFO: Validate minimum required tables from names in GPKG...")
        result = self.db_gpkg.test_connection()
        self.assertTrue(result[0], 'The test connection is not working')
        self.check_required_table_names(self.db_gpkg)

    def check_required_table_names(self, db_connection):
        test_required_tables = ['MORE_BFS_T', 'LESS_BFS_T', 'POINT_BFS_T', 'COL_POINT_SOURCE_T', 'COL_RRR_SOURCE_T', 'COL_UE_BAUNIT_T', 'COL_UE_SOURCE_T', 'COL_BAUNIT_SOURCE_T', 'COL_CCL_SOURCE_T', 'OP_BUILDING_TYPE_D', 'OP_DOMAIN_BUILDING_TYPE_D', 'OP_BUILDING_UNIT_TYPE_D', 'OP_GROUP_PARTY_T', 'OP_BUILDING_UNIT_T', 'OP_BUILDING_T', 'OP_RIGHT_T', 'OP_ADMINISTRATIVE_SOURCE_T', 'OP_SPATIAL_SOURCE_T', 'OP_PARTY_T', 'OP_BOUNDARY_T', 'OP_PARCEL_T', 'OP_BOUNDARY_POINT_T', 'OP_RESTRICTION_T', 'OP_RIGHT_OF_WAY_T', 'OP_PLOT_T', 'OP_ADMINISTRATIVE_SOURCE_TYPE_D', 'OP_PARTY_TYPE_D', 'OP_PARCEL_TYPE_D', 'OP_CONTROL_POINT_TYPE_D', 'OP_SURVEY_POINT_TYPE_D', 'OP_POINT_TYPE_D']
        required_tables = get_required_tables(db_connection)

        for test_required_table in test_required_tables:
            self.assertIn(test_required_table, required_tables)

    def test_required_field_names_pg(self):
        print("\nINFO: Validate minimum required fields from names in PG...")
        result = self.db_pg.test_connection()
        self.assertTrue(result[0], 'The test connection is not working')
        self.check_required_field_names(self.db_pg)

    def test_required_field_names_gpkg(self):
        print("\nINFO: Validate minimum required fields from names in GPKG...")
        result = self.db_gpkg.test_connection()
        self.assertTrue(result[0], 'The test connection is not working')
        self.check_required_field_names(self.db_gpkg)

    def check_required_field_names(self, db_connection):
        test_required_fields = ['MORE_BFS_T_CRF_LINEAR_STRUCTURE_F', 'LESS_BFS_T_CRF_LINEAR_STRUCTURE_F', 'POINT_BFS_T_CRF_LINEAR_STRUCTURE_F']
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

