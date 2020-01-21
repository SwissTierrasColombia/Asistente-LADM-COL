import nose2

from qgis.testing import (start_app,
                          unittest)

start_app() # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.config.table_mapping_config import (Names,
                                                            ILICODE,
                                                            T_ID,
                                                            DESCRIPTION,
                                                            DISPLAY_NAME)
from asistente_ladm_col.tests.utils import (get_pg_conn,
                                            restore_schema)


class TestAllModels(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        restore_schema('test_ladm_all_models')
        self.db_connection = get_pg_conn('test_ladm_all_models')
        self.names = Names()

    def test_required_models(self):
        print("\nINFO: Validate if the schema for all models...")
        result = self.db_connection.test_connection()
        self.assertTrue(result[0], 'The test connection is not working')

        self.assertTrue(self.db_connection.supplies_model_exists())
        self.assertTrue(self.db_connection.snr_data_model_exists())
        self.assertTrue(self.db_connection.supplies_integration_model_exists())
        self.assertTrue(self.db_connection.operation_model_exists())
        self.assertTrue(self.db_connection.valuation_model_exists())
        self.assertTrue(self.db_connection.cadastral_form_model_exists())
        self.assertTrue(self.db_connection.ant_model_exists())
        self.assertTrue(self.db_connection.reference_cartography_model_exists())

    def test_names_from_model(self):
        print("\nINFO: Validate names for all model...")
        result = self.db_connection.test_connection()
        self.assertTrue(result[0], 'The test connection is not working')

        dict_names = self.db_connection.get_table_and_field_names()
        self.assertEqual(len(dict_names), 215)

        expected_dict = {T_ID: 't_id',
                         ILICODE: 'ilicode',
                         DESCRIPTION: 'description',
                         DISPLAY_NAME: 'dispname',
                         'Datos_SNR.Datos_SNR.SNR_Predio_Registro': {
                             'table_name': 'snr_predio_registro',
                             'Datos_SNR.Datos_SNR.SNR_Predio_Registro.Cabida_Linderos': 'cabida_linderos',
                             'Datos_SNR.Datos_SNR.SNR_Predio_Registro.Codigo_ORIP': 'codigo_orip',
                             'Datos_SNR.Datos_SNR.SNR_Predio_Registro.Fecha_Datos': 'fecha_datos',
                             'Datos_SNR.Datos_SNR.SNR_Predio_Registro.Matricula_Inmobiliaria': 'matricula_inmobiliaria',
                             'Datos_SNR.Datos_SNR.SNR_Predio_Registro.Matricula_Inmobiliaria_Matriz': 'matricula_inmobiliaria_matriz',
                             'Datos_SNR.Datos_SNR.SNR_Predio_Registro.Numero_Predial_Anterior_en_FMI': 'numero_predial_anterior_en_fmi',
                             'Datos_SNR.Datos_SNR.SNR_Predio_Registro.Numero_Predial_Nuevo_en_FMI': 'numero_predial_nuevo_en_fmi',
                             'Datos_SNR.Datos_SNR.SNR_Predio_Registro.NUPRE_en_FMI': 'nupre_en_fmi',
                             'Datos_SNR.Datos_SNR.snr_fuente_cabidalinderos.snr_fuente_cabidalinderos..Datos_SNR.Datos_SNR.SNR_Fuente_CabidaLinderos': 'snr_fuente_cabidalinderos'
                         },
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
                         },
                         'Operacion.Operacion.op_predio_insumos_operacion': {
                             'table_name': 'op_predio_insumos_operacion',
                             'Operacion.Operacion.op_predio_insumos_operacion.ini_predio_insumos..Datos_Integracion_Insumos.Datos_Integracion_Insumos.INI_Predio_Insumos': 'ini_predio_insumos',
                             'Operacion.Operacion.op_predio_insumos_operacion.op_predio..Operacion.Operacion.OP_Predio': 'op_predio'
                         },
                         'ANT.Fiso.ANT_Solicitud': {
                             'table_name': 'ant_solicitud',
                             'ANT.Fiso.ANT_Solicitud.Acepta_Notificacion_Correo_Electronico': 'acepta_notificacion_correo_electronico',
                             'ANT.Fiso.ANT_Solicitud.Anio_Fallecimiento_Persona_Herencia': 'anio_fallecimiento_persona_herencia',
                             'ANT.Fiso.ANT_Solicitud.Area_Aprox_Predio_Solicitud': 'area_aprox_predio_solicitud',
                             'ANT.Fiso.ANT_Solicitud.Area_Explotacion_Aprox': 'area_explotacion_aprox',
                             'ANT.Fiso.ANT_Solicitud.Cantidad_Presonas_Recibieron_Predio': 'cantidad_presonas_recibieron_predio',
                             'ANT.Fiso.ANT_Solicitud.Centro_Poblado': 'centro_poblado',
                             'ANT.Fiso.ANT_Solicitud.Clase_Explotacion': 'clase_explotacion',
                             'ANT.Fiso.ANT_Solicitud.Corregimiento': 'corregimiento',
                             'ANT.Fiso.ANT_Solicitud.Correo_Electronico': 'correo_electronico',
                             'ANT.Fiso.ANT_Solicitud.Deja_herencia_Verdadero_Duenio': 'deja_herencia_verdadero_duenio',
                             'ANT.Fiso.ANT_Solicitud.Direccion_Predio': 'direccion_predio',
                             'ANT.Fiso.ANT_Solicitud.Documento_Respaldo_Negocio': 'documento_respaldo_negocio',
                             'ANT.Fiso.ANT_Solicitud.Documento_Tiene_Nombre_Dejo_Herencia': 'documento_tiene_nombre_dejo_herencia',
                             'ANT.Fiso.ANT_Solicitud.Documento_Tiene_Nombre_Tercero': 'documento_tiene_nombre_tercero',
                             'ANT.Fiso.ANT_Solicitud.Documentos_Respaldo_Donacion': 'documentos_respaldo_donacion',
                             'ANT.Fiso.ANT_Solicitud.Entidad_Adjudicacion_Ocupante': 'entidad_adjudicacion_ocupante',
                             'ANT.Fiso.ANT_Solicitud.Entidad_Adjudicacion_Poseedor': 'entidad_adjudicacion_poseedor',
                             'ANT.Fiso.ANT_Solicitud.Especifique_Titulo': 'especifique_titulo',
                             'ANT.Fiso.ANT_Solicitud.Estado_Tramite_Ocupante': 'estado_tramite_ocupante',
                             'ANT.Fiso.ANT_Solicitud.Estado_Tramite_Poseedor': 'estado_tramite_poseedor',
                             'ANT.Fiso.ANT_Solicitud.Existe_Herederos': 'existe_herederos',
                             'ANT.Fiso.ANT_Solicitud.Fecha_Explota_Predio': 'fecha_explota_predio',
                             'ANT.Fiso.ANT_Solicitud.Fecha_Solicitud': 'fecha_solicitud',
                             'ANT.Fiso.ANT_Solicitud.Fecha_Solicitud_Tramite_Ocupante': 'fecha_solicitud_tramite_ocupante',
                             'ANT.Fiso.ANT_Solicitud.Fecha_Solicitud_Tramite_Poseedor': 'fecha_solicitud_tramite_poseedor',
                             'ANT.Fiso.ANT_Solicitud.Herederos_Acuerdo_Adelantar_sucesion': 'herederos_acuerdo_adelantar_sucesion',
                             'ANT.Fiso.ANT_Solicitud.Interesado_Programas_Formalizacion_Acceso_Tierras_ANT': 'interesado_programas_formalizacion_acceso_tierras_ant',
                             'ANT.Fiso.ANT_Solicitud.Lista_Otros_Herederos': 'lista_otros_herederos',
                             'ANT.Fiso.ANT_Solicitud.Modulo_Debe_Ingresar': 'modulo_debe_ingresar',
                             'ANT.Fiso.ANT_Solicitud.Nombre_Duenio_predio': 'nombre_duenio_predio',
                             'ANT.Fiso.ANT_Solicitud.Nombre_Predio': 'nombre_predio',
                             'ANT.Fiso.ANT_Solicitud.Nombre_Predio_Mayor_Extension': 'nombre_predio_mayor_extension',
                             'ANT.Fiso.ANT_Solicitud.Numero_Formulario': 'numero_formulario',
                             'ANT.Fiso.ANT_Solicitud.Ocupante_Inicio_Adjudicacion_Predio': 'ocupante_inicio_adjudicacion_predio',
                             'ANT.Fiso.ANT_Solicitud.Otro': 'otro',
                             'ANT.Fiso.ANT_Solicitud.Parentesco_Persona_Donante': 'parentesco_persona_donante',
                             'ANT.Fiso.ANT_Solicitud.Parentesco_Persona_Herencia': 'parentesco_persona_herencia',
                             'ANT.Fiso.ANT_Solicitud.Persona_Vendio_Vive': 'persona_vendio_vive',
                             'ANT.Fiso.ANT_Solicitud.Porque_No_Realizo_Escritura': 'porque_no_realizo_escritura',
                             'ANT.Fiso.ANT_Solicitud.Poseedor_Inicio_Adjudicacion_Predio': 'poseedor_inicio_adjudicacion_predio',
                             'ANT.Fiso.ANT_Solicitud.Predio_Parte_Predio_Mayor': 'predio_parte_predio_mayor',
                             'ANT.Fiso.ANT_Solicitud.Quien_Vendio_Predio': 'quien_vendio_predio',
                             'ANT.Fiso.ANT_Solicitud.Quienes_Habitan_Predio': 'quienes_habitan_predio',
                             'ANT.Fiso.ANT_Solicitud.Regimen_Escogencia': 'regimen_escogencia',
                             'ANT.Fiso.ANT_Solicitud.Registro_Titulo_Predio_SNR': 'registro_titulo_predio_snr',
                             'ANT.Fiso.ANT_Solicitud.Tiene_Como_Contactar_Vendedor': 'tiene_como_contactar_vendedor',
                             'ANT.Fiso.ANT_Solicitud.Vendedor_Dispuesto_Firmar_Escritura': 'vendedor_dispuesto_firmar_escritura',
                             'ANT.Fiso.ANT_Solicitud.Vereda': 'vereda',
                             'ANT.Fiso.ant_interesado_solicitud.op_interesado..Operacion.Operacion.OP_Interesado': 'op_interesado',
                             'ANT.Fiso.ant_predio_solicitud.op_predio..Operacion.Operacion.OP_Predio': 'op_predio'
                         },
                         'Operacion.Operacion.OP_Predio': {
                             'table_name': 'op_predio',
                             'Operacion.Operacion.OP_Predio.Avaluo_Predio': 'avaluo_predio',
                             'Operacion.Operacion.OP_Predio.Codigo_ORIP': 'codigo_orip',
                             'LADM_COL.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version': 'comienzo_vida_util_version',
                             'Operacion.Operacion.OP_Predio.Condicion_Predio': 'condicion_predio',
                             'Operacion.Operacion.OP_Predio.Departamento': 'departamento',
                             'Operacion.Operacion.OP_Predio.Direccion': 'direccion',
                             'LADM_COL.LADM_Nucleo.Oid.Espacio_De_Nombres': 'espacio_de_nombres',
                             'LADM_COL.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version': 'fin_vida_util_version',
                             'LADM_COL.LADM_Nucleo.Oid.Local_Id': 'local_id',
                             'Operacion.Operacion.OP_Predio.Matricula_Inmobiliaria': 'matricula_inmobiliaria',
                             'Operacion.Operacion.OP_Predio.Municipio': 'municipio',
                             'LADM_COL.LADM_Nucleo.COL_BAUnit.Nombre': 'nombre',
                             'Operacion.Operacion.OP_Predio.Numero_Predial': 'numero_predial',
                             'Operacion.Operacion.OP_Predio.Numero_Predial_Anterior': 'numero_predial_anterior',
                             'Operacion.Operacion.OP_Predio.NUPRE': 'nupre',
                             'Operacion.Operacion.OP_Predio.Tipo': 'tipo'
                         },
                         'LADM_COL.LADM_Nucleo.col_masCcl': {
                             'table_name': 'col_masccl',
                             'LADM_COL.LADM_Nucleo.col_masCcl.ccl_mas..Operacion.Operacion.OP_Lindero': 'ccl_mas_op_lindero',
                             'LADM_COL.LADM_Nucleo.col_masCcl.ccl_mas..Cartografia_Referencia.Auxiliares.CRF_EstructuraLineal': 'ccl_mas_crf_estructuralineal',
                             'LADM_COL.LADM_Nucleo.col_masCcl.ue_mas..Operacion.Operacion.OP_UnidadConstruccion': 'ue_mas_op_unidadconstruccion',
                             'LADM_COL.LADM_Nucleo.col_masCcl.ue_mas..Operacion.Operacion.OP_Construccion': 'ue_mas_op_construccion',
                             'LADM_COL.LADM_Nucleo.col_masCcl.ue_mas..Operacion.Operacion.OP_Terreno': 'ue_mas_op_terreno',
                             'LADM_COL.LADM_Nucleo.col_masCcl.ue_mas..Operacion.Operacion.OP_ServidumbrePaso': 'ue_mas_op_servidumbrepaso'
                         }}

        for k,v in expected_dict.items():
            self.assertIn(k, dict_names)
            self.assertEqual(v, dict_names[k])

    @classmethod
    def tearDownClass(self):
        self.db_connection.conn.close()


if __name__ == '__main__':
    nose2.main()

