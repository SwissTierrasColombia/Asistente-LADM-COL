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


class TestCadastralFormModel(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        restore_schema('test_ladm_cadastral_form_model')
        self.db_connection = get_dbconn('test_ladm_cadastral_form_model')
        self.names = Names()

    def test_required_models(self):
        print("\nINFO: Validate if the schema for cadastral form model...")
        result = self.db_connection.test_connection()
        self.assertTrue(result[0], 'The test connection is not working')

        self.assertTrue(self.db_connection.supplies_model_exists())
        self.assertTrue(self.db_connection.snr_data_model_exists())
        self.assertTrue(self.db_connection.supplies_integration_model_exists())
        self.assertTrue(self.db_connection.operation_model_exists())
        self.assertTrue(self.db_connection.valuation_model_exists())
        self.assertTrue(self.db_connection.cadastral_form_model_exists())
        self.assertFalse(self.db_connection.ant_model_exists())
        self.assertFalse(self.db_connection.reference_cartography_model_exists())

    def test_names_from_model(self):
        print("\nINFO: Validate names for cadastral form model...")
        result = self.db_connection.test_connection()
        self.assertTrue(result[0], 'The test connection is not working')

        dict_names = self.db_connection.get_table_and_field_names()
        self.assertEqual(len(dict_names), 177)

        expected_dict = {T_ID: 't_id',
                         ILICODE: 'ilicode',
                         DESCRIPTION: 'description',
                         DISPLAY_NAME: 'dispname',
                         'Formulario_Catastro.Formulario_Catastro.FCM_Formulario_Unico_CM': {
                             'table_name': 'fcm_formulario_unico_cm',
                             'Formulario_Catastro.Formulario_Catastro.FCM_Formulario_Unico_CM.Barrio_Vereda': 'barrio_vereda',
                             'Formulario_Catastro.Formulario_Catastro.FCM_Formulario_Unico_CM.Categoria_Suelo': 'categoria_suelo',
                             'Formulario_Catastro.Formulario_Catastro.FCM_Formulario_Unico_CM.Clase_Suelo': 'clase_suelo',
                             'Formulario_Catastro.Formulario_Catastro.FCM_Formulario_Unico_CM.Corregimiento': 'corregimiento',
                             'Formulario_Catastro.Formulario_Catastro.FCM_Formulario_Unico_CM.Destinacion_Economica': 'destinacion_economica',
                             'Formulario_Catastro.Formulario_Catastro.FCM_Formulario_Unico_CM.Fecha_Inicio_Tenencia': 'fecha_inicio_tenencia',
                             'Formulario_Catastro.Formulario_Catastro.FCM_Formulario_Unico_CM.Fecha_Visita_predial': 'fecha_visita_predial',
                             'Formulario_Catastro.Formulario_Catastro.FCM_Formulario_Unico_CM.Formalidad': 'formalidad',
                             'Formulario_Catastro.Formulario_Catastro.FCM_Formulario_Unico_CM.Localidad_Comuna': 'localidad_comuna',
                             'Formulario_Catastro.Formulario_Catastro.FCM_Formulario_Unico_CM.Nombre_Reconocedor': 'nombre_reconocedor',
                             'Formulario_Catastro.Formulario_Catastro.FCM_Formulario_Unico_CM.Numero_Predial_Predio_Matriz': 'numero_predial_predio_matriz',
                             'Formulario_Catastro.Formulario_Catastro.FCM_Formulario_Unico_CM.Observaciones': 'observaciones',
                             'Formulario_Catastro.Formulario_Catastro.FCM_Formulario_Unico_CM.Tiene_FMI': 'tiene_fmi',
                             'Formulario_Catastro.Formulario_Catastro.FCM_Formulario_Unico_CM.Numeros_Prediales_Englobe..Formulario_Catastro.Formulario_Catastro.FCM_Formulario_Unico_CM': 'fcm_formulario_unic_cm_numeros_prediales_englobe',
                             'Formulario_Catastro.Formulario_Catastro.fcm_formulario_predio.op_predio..Operacion.Operacion.OP_Predio': 'op_predio'
                         }}

        for k,v in expected_dict.items():
            self.assertIn(k, dict_names)
            self.assertEqual(v, dict_names[k])


    @classmethod
    def tearDownClass(self):
        self.db_connection.conn.close()


if __name__ == '__main__':
    nose2.main()

