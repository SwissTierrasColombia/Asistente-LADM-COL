import nose2

from qgis.testing import (start_app,
                          unittest)

from asistente_ladm_col.config.table_mapping_config import (ILICODE,
                                                            T_ID,
                                                            DESCRIPTION,
                                                            DISPLAY_NAME)

start_app() # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.tests.utils import (get_dbconn,
                                            restore_schema)


class TestTableAndFieldNames(unittest.TestCase):
    @classmethod
    def setUpClass(self):
       pass

    def test_snr_data_model(self):
        print("\nINFO: Validate names for SNR data model (small DB case)...")

        db_name = 'test_ladm_snr_data'
        restore_schema(db_name)
        db = get_dbconn(db_name)
        result = db.test_connection()
        self.assertTrue(result[0], 'The test connection is not working')

        self.assertTrue(db.snr_data_model_exists())

        dict_names = db.get_table_and_field_names()
        self.assertEqual(len(dict_names), 15)

        expected_dict = {T_ID: 't_id',
                         ILICODE: 'ilicode',
                         DESCRIPTION: 'description',
                         DISPLAY_NAME: 'dispname',
                         'Datos_SNR.Datos_SNR.snr_titular_derecho': {'table_name': 'snr_titular_derecho',
                                                                     'Datos_SNR.Datos_SNR.snr_titular_derecho.Porcentaje_Participacion': 'porcentaje_participacion',
                                                                     'Datos_SNR.Datos_SNR.snr_titular_derecho.snr_derecho..Datos_SNR.Datos_SNR.SNR_Derecho': 'snr_derecho',
                                                                     'Datos_SNR.Datos_SNR.snr_titular_derecho.snr_titular..Datos_SNR.Datos_SNR.SNR_Titular': 'snr_titular'}}

        for k,v in expected_dict.items():
            self.assertIn(k, dict_names)
            self.assertEqual(v, dict_names[k])

        db.conn.close()

    def test_operation_model(self):
        print("\nINFO: Validate names for Operation data model (the expected common DB case)...")

        db_name = 'test_ladm_operation_model'
        restore_schema(db_name)
        db = get_dbconn(db_name)
        result = db.test_connection()
        self.assertTrue(result[0], 'The test connection is not working')

        self.assertTrue(db.operation_model_exists())
        self.assertFalse(db.reference_cartography_model_exists())

        dict_names = db.get_table_and_field_names()
        self.assertEqual(len(dict_names), 144)

        expected_dict = {T_ID: 't_id',
                         ILICODE: 'ilicode',
                         DESCRIPTION: 'description',
                         DISPLAY_NAME: 'dispname',
                         'LADM_COL.LADM_Nucleo.col_masCcl': {'table_name': 'col_masccl',
                             'LADM_COL.LADM_Nucleo.col_masCcl.ccl_mas..Operacion.Operacion.OP_Lindero': 'ccl_mas',
                             'LADM_COL.LADM_Nucleo.col_masCcl.ue_mas..Operacion.Operacion.OP_Construccion': 'ue_mas_op_construccion',
                             'LADM_COL.LADM_Nucleo.col_masCcl.ue_mas..Operacion.Operacion.OP_ServidumbrePaso': 'ue_mas_op_servidumbrepaso',
                             'LADM_COL.LADM_Nucleo.col_masCcl.ue_mas..Operacion.Operacion.OP_Terreno': 'ue_mas_op_terreno',
                             'LADM_COL.LADM_Nucleo.col_masCcl.ue_mas..Operacion.Operacion.OP_UnidadConstruccion': 'ue_mas_op_unidadconstruccion'}}


        for k,v in expected_dict.items():
            self.assertIn(k, dict_names)
            self.assertEqual(v, dict_names[k])

        db.conn.close()

    def test_reference_cartography_model(self):
        print("\nINFO: Validate names for Reference Cartography data model (edge case for field keys)...")

        db_name = 'test_ladm_reference_cartography'
        restore_schema(db_name)
        db = get_dbconn(db_name)
        result = db.test_connection()
        self.assertTrue(result[0], 'The test connection is not working')

        self.assertTrue(db.operation_model_exists())
        self.assertTrue(db.reference_cartography_model_exists())

        dict_names = db.get_table_and_field_names()
        self.assertEqual(len(dict_names), 161)

        expected_dict = {T_ID: 't_id',
                         ILICODE: 'ilicode',
                         DESCRIPTION: 'description',
                         DISPLAY_NAME: 'dispname',
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

        db.conn.close()

    def tearDownClass():
        print('tearDown test_table_and_field_names')

if __name__ == '__main__':
    nose2.main()

