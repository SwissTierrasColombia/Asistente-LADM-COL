import nose2

from qgis.testing import (start_app,
                          unittest)

start_app() # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.config.table_mapping_config import (Names,
                                                            ILICODE,
                                                            T_ID,
                                                            DESCRIPTION,
                                                            DISPLAY_NAME)
from asistente_ladm_col.tests.utils import (get_gpkg_conn,
                                            get_pg_conn,
                                            restore_schema,
                                            get_test_path)

class TestGetModels(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        print('setUp test_get_models')

    def test_pg_get_models(self):
        print("\nINFO: Validate get models method() in postgres...")
        expected_dict = {'test_ladm_all_models': ['ANT_V2_9_6', 'Avaluos_V2_9_6', 'Cartografia_Referencia_V2_9_6', 
                                                        'Datos_Gestor_Catastral_V2_9_6', 'Datos_Integracion_Insumos_V2_9_6', 
                                                        'Datos_SNR_V2_9_6', 'Formulario_Catastro_V2_9_6', 'Operacion_V2_9_6', 
                                                        'ISO19107_PLANAS_V1', 'LADM_COL_V1_3'],
                         'test_ladm_integration': ['Datos_SNR_V2_9_6', 'Datos_Integracion_Insumos_V2_9_6', 
                                                            'Datos_Gestor_Catastral_V2_9_6', 'ISO19107_PLANAS_V1', 'LADM_COL_V1_3'],
                         'test_ladm_operation_model': ['Operacion_V2_9_6', 'Datos_SNR_V2_9_6', 'Datos_Integracion_Insumos_V2_9_6', 
                                                            'Datos_Gestor_Catastral_V2_9_6', 'ISO19107_PLANAS_V1', 'LADM_COL_V1_3'],
                         'test_ladm_cadastral_manager_data': ['Datos_Gestor_Catastral_V2_9_6', 'ISO19107_PLANAS_V1']} 

        for schema_name in expected_dict:
            restore_schema(schema_name)
            self.db_pg = get_pg_conn(schema_name)

            model_names = self.db_pg.get_models()
            self.assertEqual(set(expected_dict[schema_name]), set(model_names))
            self.db_pg.conn.close()

    def test_gpkg_get_models(self):
        print("\nINFO: Validate get models method() in geopackage...")
        expected_dict = {'test_ladm_all_models_v2_9_6': ['ANT_V2_9_6', 'Avaluos_V2_9_6', 'Cartografia_Referencia_V2_9_6', 
                                                        'Datos_Gestor_Catastral_V2_9_6', 'Datos_Integracion_Insumos_V2_9_6', 
                                                        'Datos_SNR_V2_9_6', 'Formulario_Catastro_V2_9_6', 'Operacion_V2_9_6', 
                                                        'ISO19107_PLANAS_V1', 'LADM_COL_V1_3'],
                         'test_ladm_integration_model_v2_9_6': ['Datos_SNR_V2_9_6', 'Datos_Integracion_Insumos_V2_9_6', 
                                                            'Datos_Gestor_Catastral_V2_9_6', 'ISO19107_PLANAS_V1', 'LADM_COL_V1_3'],
                         'test_ladm_operation_model_v2_9_6': ['Operacion_V2_9_6', 'Datos_SNR_V2_9_6', 'Datos_Integracion_Insumos_V2_9_6', 
                                                            'Datos_Gestor_Catastral_V2_9_6', 'ISO19107_PLANAS_V1', 'LADM_COL_V1_3'],
                         'test_ladm_cadastral_manager_model_v2_9_6': ['Datos_Gestor_Catastral_V2_9_6', 'ISO19107_PLANAS_V1']} 

        for gpkg in expected_dict:
            gpkg_path = get_test_path('geopackage/{}.gpkg'.format(gpkg))
            self.db_gpkg = get_gpkg_conn(gpkg_path)

            model_names = self.db_gpkg.get_models()
            self.assertEqual(set(expected_dict[gpkg]), set(model_names))

    def tearDownClass():
        print('tearDown test_get_models')


if __name__ == '__main__':
    nose2.main()