import nose2

from qgis.testing import (start_app,
                          unittest)

start_app() # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.config.table_mapping_config import (Names,
                                                            ILICODE,
                                                            T_ID,
                                                            DESCRIPTION,
                                                            DISPLAY_NAME)
from asistente_ladm_col.tests.utils import (get_dbconn,
                                            restore_schema)


class TestValuationModel(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        restore_schema('test_ladm_valuation_model')
        self.db_connection = get_dbconn('test_ladm_valuation_model')
        self.names = Names()

    def test_required_models(self):
        print("\nINFO: Validate if the schema for valuation model...")
        result = self.db_connection.test_connection()
        self.assertTrue(result[0], 'The test connection is not working')

        self.assertTrue(self.db_connection.supplies_model_exists())
        self.assertTrue(self.db_connection.snr_data_model_exists())
        self.assertTrue(self.db_connection.supplies_integration_model_exists())
        self.assertTrue(self.db_connection.operation_model_exists())
        self.assertTrue(self.db_connection.valuation_model_exists())
        self.assertFalse(self.db_connection.cadastral_form_model_exists())
        self.assertFalse(self.db_connection.ant_model_exists())
        self.assertFalse(self.db_connection.reference_cartography_model_exists())

    def test_names_from_model(self):
        print("\nINFO: Validate names for Valuation model...")
        result = self.db_connection.test_connection()
        self.assertTrue(result[0], 'The test connection is not working')

        dict_names = self.db_connection.get_table_and_field_names()
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

    @classmethod
    def tearDownClass(self):
        self.db_connection.conn.close()


if __name__ == '__main__':
    nose2.main()

