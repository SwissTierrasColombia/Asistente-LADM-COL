import unittest
from abc import ABC

import nose2

from qgis.testing import start_app

start_app() # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.config.mapping_config import (ILICODE_KEY,
                                                      T_ID_KEY,
                                                      T_ILI_TID_KEY,
                                                      DESCRIPTION_KEY,
                                                      DISPLAY_NAME_KEY)
from asistente_ladm_col.lib.db.db_connector import DBConnector
from asistente_ladm_col.tests.base_test_for_models import BaseTestForModels
from asistente_ladm_col.tests.utils import (get_pg_conn,
                                            get_gpkg_conn,
                                            get_mssql_conn,
                                            restore_schema_mssql,
                                            reset_db_mssql,
                                            restore_schema)

class BaseTestCadastralManagerDataModel(BaseTestForModels, ABC):
    def get_name_of_models(self):
        return 'Cadastral manager data model'

    def check_required_models(self):
        self.assertTrue(self.db.supplies_model_exists())
        self.assertFalse(self.db.snr_data_model_exists())
        self.assertFalse(self.db.supplies_integration_model_exists())
        self.assertFalse(self.db.survey_model_exists())
        self.assertFalse(self.db.valuation_model_exists())
        self.assertFalse(self.db.cadastral_cartography_model_exists())

    def get_required_field_list(self):
        return []

    def get_required_table_names_list(self):
        return ['GC_PARCEL_T',
                'GC_OWNER_T',
                'GC_PLOT_T',
                'GC_BUILDING_UNIT_T',
                'GC_PARCEL_TYPE_D',
                'GC_BUILDING_UNIT_TYPE_T']

    def get_expected_dict(self):
        return {T_ID_KEY: 'T_Id',
                         T_ILI_TID_KEY: "T_Ili_Tid",
                         ILICODE_KEY: 'iliCode',
                         DESCRIPTION_KEY: 'description',
                         DISPLAY_NAME_KEY: 'dispName',
                         "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_PredioCatastro": {
                             "table_name": "gc_prediocatastro",
                             "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_PredioCatastro.Circulo_Registral": "circulo_registral",
                             "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_PredioCatastro.Condicion_Predio": "condicion_predio",
                             "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_PredioCatastro.Destinacion_Economica": "destinacion_economica",
                             "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_PredioCatastro.Fecha_Datos": "fecha_datos",
                             "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_PredioCatastro.Matricula_Inmobiliaria_Catastro": "matricula_inmobiliaria_catastro",
                             "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_PredioCatastro.Numero_Predial": "numero_predial",
                             "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_PredioCatastro.Numero_Predial_Anterior": "numero_predial_anterior",
                             "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_PredioCatastro.NUPRE": "nupre",
                             "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_PredioCatastro.Sistema_Procedencia_Datos": "sistema_procedencia_datos",
                             "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_PredioCatastro.Tipo_Catastro": "tipo_catastro",
                             "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_PredioCatastro.Tipo_Predio": "tipo_predio",
                             "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_PredioCatastro.Direcciones..Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_PredioCatastro": "gc_prediocatastro_direcciones",
                             "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_PredioCatastro.Estado_Predio..Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_PredioCatastro": "gc_prediocatastro_estado_predio"
                         }}

    def get_expected_table_and_fields_length(self):
        return 32


class TestCadastralManagerDataModelPG(BaseTestCadastralManagerDataModel, unittest.TestCase):
    schema = 'test_ladm_cadastral_manager_data'

    @classmethod
    def restore_db(cls):
        restore_schema(cls.schema)

    @classmethod
    def get_connector(cls) -> DBConnector:
        return get_pg_conn(cls.schema)

    def get_db_name(self):
        return 'PG'

    def get_expected_dict(self):
        return {T_ID_KEY: 't_id',
                T_ILI_TID_KEY: "t_ili_tid",
                ILICODE_KEY: 'ilicode',
                DESCRIPTION_KEY: 'description',
                DISPLAY_NAME_KEY: 'dispname',
                "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_PredioCatastro": {
                 "table_name": "gc_prediocatastro",
                 "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_PredioCatastro.Circulo_Registral": "circulo_registral",
                 "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_PredioCatastro.Condicion_Predio": "condicion_predio",
                 "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_PredioCatastro.Destinacion_Economica": "destinacion_economica",
                 "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_PredioCatastro.Fecha_Datos": "fecha_datos",
                 "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_PredioCatastro.Matricula_Inmobiliaria_Catastro": "matricula_inmobiliaria_catastro",
                 "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_PredioCatastro.Numero_Predial": "numero_predial",
                 "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_PredioCatastro.Numero_Predial_Anterior": "numero_predial_anterior",
                 "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_PredioCatastro.NUPRE": "nupre",
                 "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_PredioCatastro.Sistema_Procedencia_Datos": "sistema_procedencia_datos",
                 "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_PredioCatastro.Tipo_Catastro": "tipo_catastro",
                 "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_PredioCatastro.Tipo_Predio": "tipo_predio",
                 "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_PredioCatastro.Direcciones..Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_PredioCatastro": "gc_prediocatastro_direcciones",
                 "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_PredioCatastro.Estado_Predio..Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_PredioCatastro": "gc_prediocatastro_estado_predio"
                }}


class TestCadastralManagerDataModelGPKG(BaseTestCadastralManagerDataModel, unittest.TestCase):

    def get_db_name(self):
        return 'GPKG'

    @classmethod
    def restore_db(cls):
        pass

    @classmethod
    def get_connector(cls) -> DBConnector:
        return get_gpkg_conn('test_ladm_cadastral_manager_data_gpkg')


class TestCadastralManagerDataModelMSSQL(BaseTestCadastralManagerDataModel, unittest.TestCase):
    schema = 'test_ladm_cadastral_manager_data'

    def get_db_name(self):
        return 'SQL Server'

    @classmethod
    def restore_db(cls):
        reset_db_mssql(cls.schema)
        restore_schema_mssql(cls.schema)

    @classmethod
    def get_connector(cls) -> DBConnector:
        return get_mssql_conn(cls.schema)


if __name__ == '__main__':
    nose2.main()
