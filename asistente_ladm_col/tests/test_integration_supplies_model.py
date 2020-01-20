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


class TestIntegrationSuppliesModel(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        restore_schema('test_ladm_integration')
        self.db_connection = get_dbconn('test_ladm_integration')
        self.names = Names()

    def test_required_models(self):
        print("\nINFO: Validate if the schema for integration supplies model model...")
        result = self.db_connection.test_connection()
        self.assertTrue(result[0], 'The test connection is not working')

        self.assertTrue(self.db_connection.supplies_model_exists())
        self.assertTrue(self.db_connection.snr_data_model_exists())
        self.assertTrue(self.db_connection.supplies_integration_model_exists())
        self.assertFalse(self.db_connection.operation_model_exists())
        self.assertFalse(self.db_connection.valuation_model_exists())
        self.assertFalse(self.db_connection.cadastral_form_model_exists())
        self.assertFalse(self.db_connection.ant_model_exists())
        self.assertFalse(self.db_connection.reference_cartography_model_exists())

    def test_names_from_model(self):
        print("\nINFO: Validate names for Integration Supplies model...")
        result = self.db_connection.test_connection()
        self.assertTrue(result[0], 'The test connection is not working')

        dict_names = self.db_connection.get_table_and_field_names()
        self.assertEqual(len(dict_names), 40)
        expected_dict = {T_ID: 't_id',
                         ILICODE: 'ilicode',
                         DESCRIPTION: 'description',
                         DISPLAY_NAME: 'dispname',
                         'Datos_Integracion_Insumos.Datos_Integracion_Insumos.INI_Predio_Insumos': {
                             'table_name': 'ini_predio_insumos',
                             'Datos_Integracion_Insumos.Datos_Integracion_Insumos.ini_predio_integracion_gc.gc_predio_catastro..Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Predio_Catastro': 'gc_predio_catastro',
                             'Datos_Integracion_Insumos.Datos_Integracion_Insumos.ini_predio_integracion_snr.snr_predio_juridico..Datos_SNR.Datos_SNR.SNR_Predio_Registro': 'snr_predio_juridico'
                         },
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

        for k,v in expected_dict.items():
            self.assertIn(k, dict_names)
            self.assertEqual(v, dict_names[k])

    @classmethod
    def tearDownClass(self):
        self.db_connection.conn.close()


if __name__ == '__main__':
    nose2.main()

