import unittest
from abc import ABC

import nose2

from qgis.testing import start_app

start_app()  # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.config.keys.ili2db_keys import *
from asistente_ladm_col.lib.db.db_connector import DBConnector
from asistente_ladm_col.tests.base_test_for_models import BaseTestForModels
from asistente_ladm_col.tests.utils import (get_pg_conn,
                                            get_gpkg_conn,
                                            get_mssql_conn,
                                            restore_schema_mssql,
                                            reset_db_mssql,
                                            restore_schema)


class BaseTestValuationModel(BaseTestForModels, ABC):

    def get_name_of_models(self):
        return 'Valuation model'

    def check_required_models(self):
        self.assertTrue(self.db.supplies_model_exists())
        self.assertTrue(self.db.snr_data_model_exists())
        self.assertTrue(self.db.supplies_integration_model_exists())
        self.assertTrue(self.db.survey_model_exists())
        self.assertTrue(self.db.valuation_model_exists())
        self.assertFalse(self.db.cadastral_cartography_model_exists())

    def get_required_field_list(self):
        return ['EXT_ARCHIVE_S_DATA_F',
                'FRACTION_S_NUMERATOR_F',
                'MORE_BFS_T_LC_BOUNDARY_F',
                'MORE_BFS_T_LC_BUILDING_F',
                'MORE_BFS_T_LC_RIGHT_OF_WAY_F',
                'MORE_BFS_T_LC_PLOT_F',
                'MORE_BFS_T_LC_BUILDING_UNIT_F',
                'LESS_BFS_T_LC_BOUNDARY_F',
                'LESS_BFS_T_LC_BUILDING_F',
                'LESS_BFS_T_LC_RIGHT_OF_WAY_F',
                'LESS_BFS_T_LC_PLOT_F',
                'LESS_BFS_T_LC_BUILDING_UNIT_F',
                'FRACTION_S_MEMBER_F',
                'MEMBERS_T_GROUP_PARTY_F',
                'MEMBERS_T_PARTY_F',
                'POINT_BFS_T_LC_BOUNDARY_F',
                'POINT_BFS_T_LC_CONTROL_POINT_F',
                'POINT_BFS_T_LC_SURVEY_POINT_F',
                'POINT_BFS_T_LC_BOUNDARY_POINT_F',
                'COL_POINT_SOURCE_T_SOURCE_F',
                'COL_POINT_SOURCE_T_LC_CONTROL_POINT_F',
                'COL_UE_BAUNIT_T_LC_BUILDING_F',
                'COL_UE_BAUNIT_T_LC_BUILDING_UNIT_F',
                'COL_UE_BAUNIT_T_LC_RIGHT_OF_WAY_F',
                'COL_UE_SOURCE_T_SOURCE_F',
                'COL_UE_SOURCE_T_LC_BUILDING_F',
                'COL_UE_SOURCE_T_LC_RIGHT_OF_WAY_F',
                'COL_UE_SOURCE_T_LC_PLOT_F',
                'COL_UE_SOURCE_T_LC_BUILDING_UNIT_F',
                'BAUNIT_SOURCE_T_SOURCE_F',
                'BAUNIT_SOURCE_T_UNIT_F',
                'COL_CCL_SOURCE_T_SOURCE_F',
                'COL_CCL_SOURCE_T_BOUNDARY_F',
                'COL_GROUP_PARTY_T_TYPE_F',
                'COL_PARTY_T_NAME_F']

    def get_required_table_names_list(self):
        return ['MORE_BFS_T',
                'LESS_BFS_T',
                'POINT_BFS_T',
                'COL_POINT_SOURCE_T',
                'COL_RRR_SOURCE_T',
                'COL_UE_BAUNIT_T',
                'COL_UE_SOURCE_T',
                'COL_BAUNIT_SOURCE_T',
                'COL_CCL_SOURCE_T',
                'LC_BUILDING_TYPE_D',
                'LC_DOMAIN_BUILDING_TYPE_D',
                'LC_BUILDING_UNIT_TYPE_D',
                'LC_GROUP_PARTY_T',
                'LC_BUILDING_UNIT_T',
                'LC_BUILDING_T',
                'LC_RIGHT_T',
                'LC_ADMINISTRATIVE_SOURCE_T',
                'LC_SPATIAL_SOURCE_T',
                'LC_PARTY_T',
                'LC_BOUNDARY_T',
                'LC_PARCEL_T',
                'LC_BOUNDARY_POINT_T',
                'LC_RESTRICTION_T',
                'LC_RIGHT_OF_WAY_T',
                'LC_PLOT_T',
                'COL_ADMINISTRATIVE_SOURCE_TYPE_D',
                'LC_PARTY_TYPE_D',
                'COL_BAUNIT_TYPE_D',
                'LC_CONTROL_POINT_TYPE_D',
                'LC_SURVEY_POINT_TYPE_D',
                'COL_POINT_TYPE_D']

    def get_expected_dict(self):
        return {T_ID_KEY: 'T_Id',
                T_ILI_TID_KEY: "T_Ili_Tid",
                ILICODE_KEY: 'iliCode',
                DESCRIPTION_KEY: 'description',
                DISPLAY_NAME_KEY: 'dispName',
                "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Terreno": {
                 "table_name": "gc_terreno",
                 "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Terreno.Area_Terreno_Alfanumerica": "area_terreno_alfanumerica",
                 "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Terreno.Area_Terreno_Digital": "area_terreno_digital",
                 "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Terreno.Geometria": "geometria",
                 "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Terreno.Manzana_Vereda_Codigo": "manzana_vereda_codigo",
                 "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Terreno.Numero_Subterraneos": "numero_subterraneos",
                 "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.gc_terreno_predio.gc_predio..Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_PredioCatastro": "gc_predio"
                },
                "Submodelo_Avaluos.Avaluos.AV_TablaCalificacionConstruccion": {
                 "table_name": "av_tablacalificacionconstruccion",
                 "Submodelo_Avaluos.Avaluos.AV_TablaCalificacionConstruccion.Puntuacion": "puntuacion",
                 "Submodelo_Avaluos.Avaluos.AV_TablaCalificacionConstruccion.Uso": "uso",
                 "Submodelo_Avaluos.Avaluos.AV_TablaCalificacionConstruccion.Valor_M2_Construccion": "valor_m2_construccion"
                }}

    def get_expected_table_and_fields_length(self):
        return self.get_ili2db_names_count() + 180


class TestValuationModelPG(BaseTestValuationModel, unittest.TestCase):
    schema = 'test_ladm_valuation_model'

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
                "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Terreno": {
                 "table_name": "gc_terreno",
                 "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Terreno.Area_Terreno_Alfanumerica": "area_terreno_alfanumerica",
                 "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Terreno.Area_Terreno_Digital": "area_terreno_digital",
                 "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Terreno.Geometria": "geometria",
                 "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Terreno.Manzana_Vereda_Codigo": "manzana_vereda_codigo",
                 "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Terreno.Numero_Subterraneos": "numero_subterraneos",
                 "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.gc_terreno_predio.gc_predio..Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_PredioCatastro": "gc_predio"
                },
                "Submodelo_Avaluos.Avaluos.AV_TablaCalificacionConstruccion": {
                 "table_name": "av_tablacalificacionconstruccion",
                 "Submodelo_Avaluos.Avaluos.AV_TablaCalificacionConstruccion.Puntuacion": "puntuacion",
                 "Submodelo_Avaluos.Avaluos.AV_TablaCalificacionConstruccion.Uso": "uso",
                 "Submodelo_Avaluos.Avaluos.AV_TablaCalificacionConstruccion.Valor_M2_Construccion": "valor_m2_construccion"
                }}


class TestValuationModelGPKG(BaseTestValuationModel, unittest.TestCase):

    def get_db_name(self):
        return 'GPKG'

    @classmethod
    def restore_db(cls):
        pass

    @classmethod
    def get_connector(cls) -> DBConnector:
        return get_gpkg_conn('test_ladm_valuation_model_gpkg')


class TestValuationModelMSSQL(BaseTestValuationModel, unittest.TestCase):
    schema = 'test_ladm_valuation_model'

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
