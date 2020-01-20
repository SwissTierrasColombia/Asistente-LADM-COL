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


class TestANTModel(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        restore_schema('test_ladm_ant')
        self.db_connection = get_dbconn('test_ladm_ant')
        self.names = Names()

    def test_required_models(self):
        print("\nINFO: Validate if the schema for ANT model...")
        result = self.db_connection.test_connection()
        self.assertTrue(result[0], 'The test connection is not working')

        self.assertTrue(self.db_connection.supplies_model_exists())
        self.assertTrue(self.db_connection.snr_data_model_exists())
        self.assertTrue(self.db_connection.supplies_integration_model_exists())
        self.assertTrue(self.db_connection.operation_model_exists())
        self.assertFalse(self.db_connection.valuation_model_exists())
        self.assertFalse(self.db_connection.cadastral_form_model_exists())
        self.assertTrue(self.db_connection.ant_model_exists())
        self.assertFalse(self.db_connection.reference_cartography_model_exists())

    def test_names_from_model(self):
        print("\nINFO: Validate names for ANT model...")
        result = self.db_connection.test_connection()
        self.assertTrue(result[0], 'The test connection is not working')

        dict_names = self.db_connection.get_table_and_field_names()
        self.assertEqual(len(dict_names), 162)
        expected_dict = {T_ID: 't_id',
                         ILICODE: 'ilicode',
                         DESCRIPTION: 'description',
                         DISPLAY_NAME: 'dispname',
                         'ANT.Fiso.ANT_Interesado_Caracterizacion': {
                             'table_name': 'ant_interesado_caracterizacion',
                             'ANT.Fiso.ANT_Interesado_Caracterizacion.A_Que_Titulo': 'a_que_titulo',
                             'ANT.Fiso.ANT_Interesado_Caracterizacion.Alguna_Vez_Casado': 'alguna_vez_casado',
                             'ANT.Fiso.ANT_Interesado_Caracterizacion.Autoriza_Ant': 'autoriza_ant',
                             'ANT.Fiso.ANT_Interesado_Caracterizacion.Beneficiario_Incora_Incoder_ANT_URT': 'beneficiario_incora_incoder_ant_urt',
                             'ANT.Fiso.ANT_Interesado_Caracterizacion.Cabeza_hogar': 'cabeza_hogar',
                             'ANT.Fiso.ANT_Interesado_Caracterizacion.Conflicto_Vigente_Descripcion': 'conflicto_vigente_descripcion',
                             'ANT.Fiso.ANT_Interesado_Caracterizacion.Conserva_Registro': 'conserva_registro',
                             'ANT.Fiso.ANT_Interesado_Caracterizacion.Considera_Propietario': 'considera_propietario',
                             'ANT.Fiso.ANT_Interesado_Caracterizacion.Corregimiento': 'corregimiento',
                             'ANT.Fiso.ANT_Interesado_Caracterizacion.Correo_Electronico': 'correo_electronico',
                             'ANT.Fiso.ANT_Interesado_Caracterizacion.Cuenta_Con_Predio_Rural': 'cuenta_con_predio_rural',
                             'ANT.Fiso.ANT_Interesado_Caracterizacion.Cuenta_Con_Sociedad_Patrimonial_Anterior_Sin_Liquidar': 'cuenta_con_sociedad_patrimonial_anterior_sin_liquidar',
                             'ANT.Fiso.ANT_Interesado_Caracterizacion.Datos_Alternos_Contacto': 'datos_alternos_contacto',
                             'ANT.Fiso.ANT_Interesado_Caracterizacion.Declara_Renta': 'declara_renta',
                             'ANT.Fiso.ANT_Interesado_Caracterizacion.Departamento': 'departamento',
                             'ANT.Fiso.ANT_Interesado_Caracterizacion.Direccion_Residencia': 'direccion_residencia',
                             'ANT.Fiso.ANT_Interesado_Caracterizacion.Esta_Viva_Persona_Caso': 'esta_viva_persona_caso',
                             'ANT.Fiso.ANT_Interesado_Caracterizacion.Estado_Civil_Actual': 'estado_civil_actual',
                             'ANT.Fiso.ANT_Interesado_Caracterizacion.Explota_Predio': 'explota_predio',
                             'ANT.Fiso.ANT_Interesado_Caracterizacion.Explotan_Otros_Predios_Rurales': 'explotan_otros_predios_rurales',
                             'ANT.Fiso.ANT_Interesado_Caracterizacion.Fecha_Constitucion_Marital': 'fecha_constitucion_marital',
                             'ANT.Fiso.ANT_Interesado_Caracterizacion.Fecha_Ejerce_Relacion_Tenencia': 'fecha_ejerce_relacion_tenencia',
                             'ANT.Fiso.ANT_Interesado_Caracterizacion.Fecha_Habita_Predio': 'fecha_habita_predio',
                             'ANT.Fiso.ANT_Interesado_Caracterizacion.Fecha_Resolucion': 'fecha_resolucion',
                             'ANT.Fiso.ANT_Interesado_Caracterizacion.Genero': 'genero',
                             'ANT.Fiso.ANT_Interesado_Caracterizacion.Habita_Predio': 'habita_predio',
                             'ANT.Fiso.ANT_Interesado_Caracterizacion.Hace_Parte_Asociacion_Economia_Campesina': 'hace_parte_asociacion_economia_campesina',
                             'ANT.Fiso.ANT_Interesado_Caracterizacion.Mensaje_Correo_Electronico': 'mensaje_correo_electronico',
                             'ANT.Fiso.ANT_Interesado_Caracterizacion.Mensaje_Texto_Telefono_Movil': 'mensaje_texto_telefono_movil',
                             'ANT.Fiso.ANT_Interesado_Caracterizacion.Mensaje_Voz_Telefono_Movil': 'mensaje_voz_telefono_movil',
                             'ANT.Fiso.ANT_Interesado_Caracterizacion.Municipio': 'municipio',
                             'ANT.Fiso.ANT_Interesado_Caracterizacion.Numero_Resolucion': 'numero_resolucion',
                             'ANT.Fiso.ANT_Interesado_Caracterizacion.Patrimonio_Neto_SMMLV': 'patrimonio_neto_smmlv',
                             'ANT.Fiso.ANT_Interesado_Caracterizacion.Porque_Considera_Derecho_Predio': 'porque_considera_derecho_predio',
                             'ANT.Fiso.ANT_Interesado_Caracterizacion.Propietario_Predio_Rural_Urbano_Vivienda': 'propietario_predio_rural_urbano_vivienda',
                             'ANT.Fiso.ANT_Interesado_Caracterizacion.Registro_SNR': 'registro_snr',
                             'ANT.Fiso.ANT_Interesado_Caracterizacion.Reside_Residio_Municipio_Ubicacion_Predio_Solicitud': 'reside_residio_municipio_ubicacion_predio_solicitud',
                             'ANT.Fiso.ANT_Interesado_Caracterizacion.Se_Separo_Legalmente': 'se_separo_legalmente',
                             'ANT.Fiso.ANT_Interesado_Caracterizacion.Tiene_Conflicto_Linderos_Servidumbre_Area': 'tiene_conflicto_linderos_servidumbre_area',
                             'ANT.Fiso.ANT_Interesado_Caracterizacion.Tipo_Beneficio': 'tipo_beneficio',
                             'ANT.Fiso.ANT_Interesado_Caracterizacion.Ubicacion_Predio': 'ubicacion_predio',
                             'ANT.Fiso.ANT_Interesado_Caracterizacion.Vereda': 'vereda',
                             'ANT.Fiso.ANT_Interesado_Caracterizacion.Vive_Actualmente_Persona_Con_Que_Caso': 'vive_actualmente_persona_con_que_caso',
                             'ANT.Fiso.ant_interesado_caracterizacion.op_interesado..Operacion.Operacion.OP_Interesado': 'op_interesado'
                         }}

        for k,v in expected_dict.items():
            self.assertIn(k, dict_names)
            self.assertEqual(v, dict_names[k])

    @classmethod
    def tearDownClass(self):
        self.db_connection.conn.close()


if __name__ == '__main__':
    nose2.main()

