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


class TestCadastralManagerDataModel(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        restore_schema('test_ladm_cadastral_manager_data')
        self.db_connection = get_dbconn('test_ladm_cadastral_manager_data')
        self.names = Names()

    def test_required_models(self):
        print("\nINFO: Validate if the schema for cadastral manager data model...")
        result = self.db_connection.test_connection()
        self.assertTrue(result[0], 'The test connection is not working')

        self.assertTrue(self.db_connection.supplies_model_exists())
        self.assertFalse(self.db_connection.snr_data_model_exists())
        self.assertFalse(self.db_connection.supplies_integration_model_exists())
        self.assertFalse(self.db_connection.operation_model_exists())
        self.assertFalse(self.db_connection.valuation_model_exists())
        self.assertFalse(self.db_connection.cadastral_form_model_exists())
        self.assertFalse(self.db_connection.ant_model_exists())
        self.assertFalse(self.db_connection.reference_cartography_model_exists())

    def test_names_from_model(self):
        print("\nINFO: Validate names for Cadastral Manager Data model (the expected common DB case)...")
        result = self.db_connection.test_connection()
        self.assertTrue(result[0], 'The test connection is not working')

        dict_names = self.db_connection.get_table_and_field_names()
        self.assertEqual(len(dict_names), 28)

        expected_dict = {T_ID: 't_id',
                         ILICODE: 'ilicode',
                         DESCRIPTION: 'description',
                         DISPLAY_NAME: 'dispname',
                         'Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Predio_Catastro': {
                             'table_name': 'gc_predio_catastro',
                             'Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Predio_Catastro.Circulo_Registral': 'circulo_registral',
                             'Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Predio_Catastro.Condicion_Predio': 'condicion_predio',
                             'Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Predio_Catastro.Destinacion_Economica': 'destinacion_economica',
                             'Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Predio_Catastro.Entidad_Emisora_Alerta': 'entidad_emisora_alerta',
                             'Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Predio_Catastro.Estado_Alerta': 'estado_alerta',
                             'Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Predio_Catastro.Fecha_Alerta': 'fecha_alerta',
                             'Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Predio_Catastro.Fecha_Datos': 'fecha_datos',
                             'Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Predio_Catastro.Matricula_Inmobiliaria_Catastro': 'matricula_inmobiliaria_catastro',
                             'Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Predio_Catastro.Numero_Predial': 'numero_predial',
                             'Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Predio_Catastro.Numero_Predial_Anterior': 'numero_predial_anterior',
                             'Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Predio_Catastro.Sistema_Procedencia_Datos': 'sistema_procedencia_datos',
                             'Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Predio_Catastro.Tipo_Catastro': 'tipo_catastro',
                             'Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Predio_Catastro.Tipo_Predio': 'tipo_predio',
                             'Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Predio_Catastro.Direcciones..Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Predio_Catastro': 'gc_predio_catastro_direcciones'
                         }}

        for k, v in expected_dict.items():
            self.assertIn(k, dict_names)
            self.assertEqual(v, dict_names[k])

    @classmethod
    def tearDownClass(self):
        self.db_connection.conn.close()


if __name__ == '__main__':
    nose2.main()

