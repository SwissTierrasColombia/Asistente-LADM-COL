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
from asistente_ladm_col.tests.utils import (get_pg_conn,
                                            restore_schema)


class TestValuationModel(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        restore_schema('test_ladm_valuation_model')
        self.db_pg = get_pg_conn('test_ladm_valuation_model')

    def test_required_models_pg(self):
        print("\nINFO: Validate if the schema for valuation model...")
        result = self.db_pg.test_connection()
        self.assertTrue(result[0], 'The test connection is not working')
        self.check_required_models(self.db_pg)

    def check_required_models(self, db_connection):
        self.assertTrue(db_connection.supplies_model_exists())
        self.assertTrue(db_connection.snr_data_model_exists())
        self.assertTrue(db_connection.supplies_integration_model_exists())
        self.assertTrue(db_connection.operation_model_exists())
        self.assertTrue(db_connection.valuation_model_exists())
        self.assertFalse(db_connection.cadastral_form_model_exists())
        self.assertFalse(db_connection.ant_model_exists())
        self.assertFalse(db_connection.reference_cartography_model_exists())

    def test_names_from_model_pg(self):
        print("\nINFO: Validate names for Valuation model from db...")
        result = self.db_pg.test_connection()
        self.assertTrue(result[0], 'The test connection is not working')

        dict_names = self.db_pg.get_table_and_field_names()
        self.assertEqual(len(dict_names), 158)

        expected_dict = {T_ID: 't_id',
                         ILICODE: 'ilicode',
                         DESCRIPTION: 'description',
                         DISPLAY_NAME: 'dispname',
                         'Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Terreno': {
                             'table_name': 'gc_terreno',
                             'Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Terreno.Area_Terreno_Alfanumerica': 'area_terreno_alfanumerica',
                             'Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Terreno.Area_Terreno_Digital': 'area_terreno_digital',
                             'Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Terreno.Geometria': 'geometria',
                             'Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Terreno.Manzana_Vereda_Codigo': 'manzana_vereda_codigo',
                             'Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Terreno.Numero_Subterraneos': 'numero_subterraneos',
                             'Datos_Gestor_Catastral.Datos_Gestor_Catastral.gc_terreno_predio.gc_predio..Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Predio_Catastro': 'gc_predio'
                         }}

        for k,v in expected_dict.items():
            self.assertIn(k, dict_names)
            self.assertEqual(v, dict_names[k])

    def test_required_table_names_pg(self):
        print("\nINFO: Validate minimum required tables from names...")
        result = self.db_pg.test_connection()
        self.assertTrue(result[0], 'The test connection is not working')
        self.check_required_table_names(self.db_pg)

    def check_required_table_names(self, db_connection):
        test_required_tables = ['MORE_BFS_T', 'LESS_BFS_T', 'POINT_BFS_T', 'COL_POINT_SOURCE_T', 'COL_RRR_SOURCE_T', 'COL_UE_BAUNIT_T', 'COL_UE_SOURCE_T', 'COL_BAUNIT_SOURCE_T', 'COL_CCL_SOURCE_T', 'OP_BUILDING_TYPE_D', 'OP_DOMAIN_BUILDING_TYPE_D', 'OP_BUILDING_UNIT_TYPE_D', 'OP_GROUP_PARTY_T', 'OP_BUILDING_UNIT_T', 'OP_BUILDING_T', 'OP_RIGHT_T', 'OP_ADMINISTRATIVE_SOURCE_T', 'OP_SPATIAL_SOURCE_T', 'OP_PARTY_T', 'OP_BOUNDARY_T', 'OP_PARCEL_T', 'OP_BOUNDARY_POINT_T', 'OP_RESTRICTION_T', 'OP_RIGHT_OF_WAY_T', 'OP_PLOT_T', 'OP_ADMINISTRATIVE_SOURCE_TYPE_D', 'OP_PARTY_TYPE_D', 'OP_PARCEL_TYPE_D', 'OP_CONTROL_POINT_TYPE_D', 'OP_SURVEY_POINT_TYPE_D', 'OP_POINT_TYPE_D']
        required_tables = get_required_tables(db_connection)
        for test_required_table in test_required_tables:
            self.assertIn(test_required_table, required_tables)

    def test_required_field_names_pg(self):
        print("\nINFO: Validate minimum required fields from names...")
        result = self.db_pg.test_connection()
        self.assertTrue(result[0], 'The test connection is not working')
        self.check_required_field_names(self.db_pg)

    def check_required_field_names(self, db_connection):
        test_required_fields = ['EXT_ARCHIVE_S_DATA_F', 'FRACTION_S_NUMERATOR_F', 'FRACTION_S_OP_RIGHT_F', 'FRACTION_S_OP_RESTRICTION_F', 'MORE_BFS_T_OP_BOUNDARY_F', 'MORE_BFS_T_OP_BUILDING_F', 'MORE_BFS_T_OP_RIGHT_OF_WAY_F', 'MORE_BFS_T_OP_PLOT_F', 'MORE_BFS_T_OP_BUILDING_UNIT_F', 'LESS_BFS_T_OP_BOUNDARY_F', 'LESS_BFS_T_OP_BUILDING_F', 'LESS_BFS_T_OP_RIGHT_OF_WAY_F', 'LESS_BFS_T_OP_PLOT_F', 'LESS_BFS_T_OP_BUILDING_UNIT_F', 'FRACTION_S_MEMBER_F', 'MEMBERS_T_GROUP_PARTY_F', 'MEMBERS_T_PARTY_F', 'POINT_BFS_T_OP_BOUNDARY_F', 'POINT_BFS_T_OP_CONTROL_POINT_F', 'POINT_BFS_T_OP_SURVEY_POINT_F', 'POINT_BFS_T_OP_BOUNDARY_POINT_F', 'COL_POINT_SOURCE_T_SOURCE_F', 'COL_POINT_SOURCE_T_OP_CONTROL_POINT_F', 'COL_UE_BAUNIT_T_OP_BUILDING_F', 'COL_UE_BAUNIT_T_OP_BUILDING_UNIT_F', 'COL_UE_BAUNIT_T_OP_RIGHT_OF_WAY_F', 'COL_UE_SOURCE_T_SOURCE_F', 'COL_UE_SOURCE_T_OP_BUILDING_F', 'COL_UE_SOURCE_T_OP_RIGHT_OF_WAY_F', 'COL_UE_SOURCE_T_OP_PLOT_F', 'COL_UE_SOURCE_T_OP_BUILDING_UNIT_F', 'BAUNIT_SOURCE_T_SOURCE_F', 'BAUNIT_SOURCE_T_UNIT_F', 'COL_CCL_SOURCE_T_SOURCE_F', 'COL_CCL_SOURCE_T_BOUNDARY_F', 'COL_GROUP_PARTY_T_TYPE_F', 'COL_PARTY_T_NAME_F']
        required_fields = get_required_fields(db_connection)
        for test_required_field in test_required_fields:
            self.assertIn(test_required_field, required_fields)

    @classmethod
    def tearDownClass(self):
        self.db_pg.conn.close()


if __name__ == '__main__':
    nose2.main()

