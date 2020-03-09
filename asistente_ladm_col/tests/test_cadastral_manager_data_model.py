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


class TestCadastralManagerDataModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("INFO: Restoring databases to be used")
        restore_schema('test_ladm_cadastral_manager_data')
        cls.db_pg = get_pg_conn('test_ladm_cadastral_manager_data')
        cls.db_gpkg = get_gpkg_conn('test_ladm_cadastral_manager_data_gpkg')

    def test_required_models_pg(self):
        print("\nINFO: Validate if the schema for cadastral manager data model in PG...")
        result = self.db_pg.test_connection()
        self.assertTrue(result[0], 'The test connection is not working')
        self.check_required_models(self.db_pg)

    def test_required_models_gpkg(self):
        print("\nINFO: Validate if the schema for cadastral manager data model in GPKG...")
        result = self.db_gpkg.test_connection()
        self.assertTrue(result[0], 'The test connection is not working')
        self.check_required_models(self.db_gpkg)

    def check_required_models(self, db_connection):
        self.assertTrue(db_connection.supplies_model_exists())
        self.assertFalse(db_connection.snr_data_model_exists())
        self.assertFalse(db_connection.supplies_integration_model_exists())
        self.assertFalse(db_connection.operation_model_exists())
        self.assertFalse(db_connection.valuation_model_exists())
        self.assertFalse(db_connection.cadastral_form_model_exists())
        self.assertFalse(db_connection.ant_model_exists())
        self.assertFalse(db_connection.reference_cartography_model_exists())

    def test_names_from_db_pg(self):
        print("\nINFO: Validate names for Cadastral Manager Data model (the expected common DB case) in PG...")
        result = self.db_pg.test_connection()
        self.assertTrue(result[0], 'The test connection is not working')

        dict_names = self.db_pg.get_table_and_field_names()
        self.assertEqual(len(dict_names), 28)

        expected_dict = {T_ID_KEY: 't_id',
                         ILICODE_KEY: 'ilicode',
                         DESCRIPTION_KEY: 'description',
                         DISPLAY_NAME_KEY: 'dispname',
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

    def test_names_from_db_gpkg(self):
        print("\nINFO: Validate names for Cadastral Manager Data model (the expected common DB case) in GPKG...")
        result = self.db_gpkg.test_connection()
        self.assertTrue(result[0], 'The test connection is not working')

        dict_names = self.db_gpkg.get_table_and_field_names()
        self.assertEqual(len(dict_names), 28)

        expected_dict = {T_ID_KEY: 'T_Id',
                         ILICODE_KEY: 'iliCode',
                         DESCRIPTION_KEY: 'description',
                         DISPLAY_NAME_KEY: 'dispName',
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
        test_required_tables = ['GC_PARCEL_T', 'GC_OWNER_T', 'GC_PLOT_T', 'GC_BUILDING_UNIT_T', 'GC_PARCEL_TYPE_D', 'GC_BUILDING_UNIT_TYPE_T']
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
        test_required_fields = []
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

