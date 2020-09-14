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


class BaseTestSNRDataModel(BaseTestForModels, ABC):
    def get_name_of_models(self):
        return 'SNR data model'

    def check_required_models(self):
        self.assertFalse(self.db.supplies_model_exists())
        self.assertTrue(self.db.snr_data_model_exists())
        self.assertFalse(self.db.supplies_integration_model_exists())
        self.assertFalse(self.db.survey_model_exists())
        self.assertFalse(self.db.valuation_model_exists())
        self.assertFalse(self.db.cadastral_cartography_model_exists())

    def get_required_field_list(self):
        return ['EXT_ARCHIVE_S_DATA_F', 'EXT_ARCHIVE_S_EXTRACTION_F']

    def get_required_table_names_list(self):
        return ['SNR_RIGHT_T',
                'SNR_SOURCE_RIGHT_T',
                'SNR_PARCEL_REGISTRY_T',
                'SNR_TITLE_HOLDER_T',
                'SNR_RIGHT_TYPE_D',
                'SNR_TITLE_HOLDER_DOCUMENT_T',
                'SNR_SOURCE_TYPE_D',
                'SNR_TITLE_HOLDER_TYPE_D',
                'EXT_ARCHIVE_S']

    def get_expected_dict(self):
        return {T_ID_KEY: 'T_Id',
                T_ILI_TID_KEY: "T_Ili_Tid",
                ILICODE_KEY: 'iliCode',
                DESCRIPTION_KEY: 'description',
                DISPLAY_NAME_KEY: 'dispName',
                'Submodelo_Insumos_SNR.Datos_SNR.snr_titular_derecho':
                    {'table_name': 'snr_titular_derecho',
                     'Submodelo_Insumos_SNR.Datos_SNR.snr_titular_derecho.Porcentaje_Participacion': 'porcentaje_participacion',
                     'Submodelo_Insumos_SNR.Datos_SNR.snr_titular_derecho.snr_derecho..Submodelo_Insumos_SNR.Datos_SNR.SNR_Derecho': 'snr_derecho',
                     'Submodelo_Insumos_SNR.Datos_SNR.snr_titular_derecho.snr_titular..Submodelo_Insumos_SNR.Datos_SNR.SNR_Titular': 'snr_titular'}}

    def get_expected_table_and_fields_length(self):
        return self.get_ili2db_names_count() + 13


class TestSNRDataModelPG(BaseTestSNRDataModel, unittest.TestCase):
    schema = 'test_ladm_snr_data'

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
                'Submodelo_Insumos_SNR.Datos_SNR.snr_titular_derecho':
                    {'table_name': 'snr_titular_derecho',
                     'Submodelo_Insumos_SNR.Datos_SNR.snr_titular_derecho.Porcentaje_Participacion': 'porcentaje_participacion',
                     'Submodelo_Insumos_SNR.Datos_SNR.snr_titular_derecho.snr_derecho..Submodelo_Insumos_SNR.Datos_SNR.SNR_Derecho': 'snr_derecho',
                     'Submodelo_Insumos_SNR.Datos_SNR.snr_titular_derecho.snr_titular..Submodelo_Insumos_SNR.Datos_SNR.SNR_Titular': 'snr_titular'}}


class TestSNRDataModelGPKG(BaseTestSNRDataModel, unittest.TestCase):

    def get_db_name(self):
        return 'GPKG'

    @classmethod
    def restore_db(cls):
        pass

    @classmethod
    def get_connector(cls) -> DBConnector:
        return get_gpkg_conn('test_ladm_snr_gpkg')


class TestSNRDataModelMSSQL(BaseTestSNRDataModel, unittest.TestCase):
    schema = 'test_ladm_snr_data'

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
