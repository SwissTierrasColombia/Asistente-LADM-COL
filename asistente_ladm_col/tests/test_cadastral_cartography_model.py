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


class BaseTestForCadastralCartographyModel(BaseTestForModels, ABC):
    def get_name_of_models(self):
        return 'Reference cadastral cartography model'
    
    def check_required_models(self):
        self.assertTrue(self.db.supplies_model_exists())
        self.assertTrue(self.db.snr_data_model_exists())
        self.assertTrue(self.db.supplies_integration_model_exists())
        self.assertTrue(self.db.survey_model_exists())
        self.assertFalse(self.db.valuation_model_exists())
        self.assertTrue(self.db.cadastral_cartography_model_exists())

    def get_required_field_list(self):
        return []  # TODO: Update list with correct values

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
                "LADM_COL.LADM_Nucleo.col_masCcl": {
                     "table_name": "col_masccl",
                     "LADM_COL.LADM_Nucleo.col_masCcl.ccl_mas..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Lindero": "ccl_mas",
                     "LADM_COL.LADM_Nucleo.col_masCcl.ue_mas..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_UnidadConstruccion": "ue_mas_lc_unidadconstruccion",
                     "LADM_COL.LADM_Nucleo.col_masCcl.ue_mas..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Construccion": "ue_mas_lc_construccion",
                     "LADM_COL.LADM_Nucleo.col_masCcl.ue_mas..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_ServidumbreTransito": "ue_mas_lc_servidumbretransito",
                     "LADM_COL.LADM_Nucleo.col_masCcl.ue_mas..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Terreno": "ue_mas_lc_terreno"
                }}

    def get_expected_table_and_fields_length(self):
        return self.get_ili2db_names_count() + 174


class TestCadastralCartographyPG(BaseTestForCadastralCartographyModel, unittest.TestCase):
    schema = 'test_ladm_cadastral_cartography'

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
                "LADM_COL.LADM_Nucleo.col_masCcl": {
                 "table_name": "col_masccl",
                 "LADM_COL.LADM_Nucleo.col_masCcl.ccl_mas..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Lindero": "ccl_mas",
                 "LADM_COL.LADM_Nucleo.col_masCcl.ue_mas..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_UnidadConstruccion": "ue_mas_lc_unidadconstruccion",
                 "LADM_COL.LADM_Nucleo.col_masCcl.ue_mas..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Construccion": "ue_mas_lc_construccion",
                 "LADM_COL.LADM_Nucleo.col_masCcl.ue_mas..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_ServidumbreTransito": "ue_mas_lc_servidumbretransito",
                 "LADM_COL.LADM_Nucleo.col_masCcl.ue_mas..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Terreno": "ue_mas_lc_terreno"
                }}


class TestCadastralCartographyGPKG(BaseTestForCadastralCartographyModel, unittest.TestCase):

    def get_db_name(self):
        return 'GPKG'

    @classmethod
    def restore_db(cls):
        pass

    @classmethod
    def get_connector(cls) -> DBConnector:
        return get_gpkg_conn('test_ladm_cadastral_cartography_gpkg')


class TestCadastralCartographyModelMSSQL(BaseTestForCadastralCartographyModel, unittest.TestCase):
    schema = 'test_ladm_cadastral_cartography'

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
