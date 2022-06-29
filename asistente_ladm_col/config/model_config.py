from copy import deepcopy

from qgis.PyQt.QtCore import QCoreApplication

from asistente_ladm_col.config.db_mapping_config import DBMappingConfig
from asistente_ladm_col.config.general_config import (ILIVALIDATOR_ERRORS_CATALOG_PATH,
                                                      IGAC_ERRORS_CATALOG_PATH)
from asistente_ladm_col.config.keys.common import (MODEL_ALIAS,
                                                   MODEL_IS_SUPPORTED,
                                                   MODEL_SUPPORTED_VERSION,
                                                   MODEL_HIDDEN_BY_DEFAULT,
                                                   MODEL_CHECKED_BY_DEFAULT,
                                                   MODEL_MAPPING,
                                                   MODEL_ILI2DB_PARAMETERS,
                                                   MODEL_CATALOGS)
from asistente_ladm_col.config.keys.ili2db_keys import *
from asistente_ladm_col.config.ladm_names import LADMNames


class ModelConfig:
    """
    Store default configuration for supported models.

    Note that MODEL_ILI2DB_PARAMETERS is only used to specify changes in default parameters,
    like enabling createBasketCol on specific models.
    """
    def __init__(self):
        db_mapping_config = DBMappingConfig()

        self.__MODEL_CONFIG = {
            LADMNames.LADM_COL_MODEL_KEY: {
                MODEL_ALIAS: QCoreApplication.translate("TranslatableConfigStrings", "LADM-COL"),
                MODEL_IS_SUPPORTED: True,
                MODEL_SUPPORTED_VERSION: "3.1",
                MODEL_HIDDEN_BY_DEFAULT: True,
                MODEL_CHECKED_BY_DEFAULT: False,
                MODEL_MAPPING: db_mapping_config.get_model_mapping(LADMNames.LADM_COL_MODEL_KEY)
            },
            LADMNames.SURVEY_MODEL_KEY: {
                MODEL_ALIAS: QCoreApplication.translate("TranslatableConfigStrings", "Survey"),
                MODEL_IS_SUPPORTED: True,
                MODEL_SUPPORTED_VERSION: "1.2",
                MODEL_HIDDEN_BY_DEFAULT: False,
                MODEL_CHECKED_BY_DEFAULT: True,
                MODEL_MAPPING: db_mapping_config.get_model_mapping(LADMNames.SURVEY_MODEL_KEY)
            },
            LADMNames.SURVEY_1_0_MODEL_KEY: {
                MODEL_ALIAS: QCoreApplication.translate("TranslatableConfigStrings", "Survey"),
                MODEL_IS_SUPPORTED: True,
                MODEL_SUPPORTED_VERSION: "1.0",
                MODEL_HIDDEN_BY_DEFAULT: True,
                MODEL_CHECKED_BY_DEFAULT: True,
                MODEL_MAPPING: db_mapping_config.get_model_mapping(LADMNames.SURVEY_1_0_MODEL_KEY)
            },
            LADMNames.SUPPLIES_MODEL_KEY: {
                MODEL_ALIAS: QCoreApplication.translate("TranslatableConfigStrings", "Supplies"),
                MODEL_IS_SUPPORTED: True,
                MODEL_SUPPORTED_VERSION: "1.0",
                MODEL_HIDDEN_BY_DEFAULT: False,
                MODEL_CHECKED_BY_DEFAULT: False,
                MODEL_MAPPING: db_mapping_config.get_model_mapping(LADMNames.SUPPLIES_MODEL_KEY)
            },
            LADMNames.SNR_DATA_SUPPLIES_MODEL_KEY: {
                MODEL_ALIAS: QCoreApplication.translate("TranslatableConfigStrings", "SNR data"),
                MODEL_IS_SUPPORTED: True,
                MODEL_SUPPORTED_VERSION: "2.0",
                MODEL_HIDDEN_BY_DEFAULT: False,
                MODEL_CHECKED_BY_DEFAULT: False,
                MODEL_MAPPING: db_mapping_config.get_model_mapping(LADMNames.SNR_DATA_SUPPLIES_MODEL_KEY)
            },
            LADMNames.SUPPLIES_INTEGRATION_MODEL_KEY: {
                MODEL_ALIAS: QCoreApplication.translate("TranslatableConfigStrings", "Supplies integration data"),
                MODEL_IS_SUPPORTED: True,
                MODEL_SUPPORTED_VERSION: "1.0",
                MODEL_HIDDEN_BY_DEFAULT: False,
                MODEL_CHECKED_BY_DEFAULT: False,
                MODEL_MAPPING: db_mapping_config.get_model_mapping(LADMNames.SUPPLIES_INTEGRATION_MODEL_KEY)
            },
            LADMNames.CADASTRAL_CARTOGRAPHY_MODEL_KEY: {
                MODEL_ALIAS: QCoreApplication.translate("TranslatableConfigStrings", "Reference cadastral cartography"),
                MODEL_IS_SUPPORTED: True,
                MODEL_SUPPORTED_VERSION: "1.2",
                MODEL_HIDDEN_BY_DEFAULT: False,
                MODEL_CHECKED_BY_DEFAULT: False,
                MODEL_MAPPING: db_mapping_config.get_model_mapping(LADMNames.CADASTRAL_CARTOGRAPHY_MODEL_KEY)
            },
            LADMNames.VALUATION_MODEL_KEY: {
                MODEL_ALIAS: QCoreApplication.translate("TranslatableConfigStrings", "Valuation"),
                MODEL_IS_SUPPORTED: True,
                MODEL_SUPPORTED_VERSION: "1.2",
                MODEL_HIDDEN_BY_DEFAULT: False,
                MODEL_CHECKED_BY_DEFAULT: False,
                MODEL_MAPPING: db_mapping_config.get_model_mapping(LADMNames.VALUATION_MODEL_KEY)
            },
            LADMNames.ISO19107_MODEL_KEY: {
                MODEL_ALIAS: QCoreApplication.translate("TranslatableConfigStrings", "ISO19107"),
                MODEL_IS_SUPPORTED: True,
                MODEL_SUPPORTED_VERSION: "3.0",
                MODEL_HIDDEN_BY_DEFAULT: True,
                MODEL_CHECKED_BY_DEFAULT: False,
                MODEL_MAPPING: db_mapping_config.get_model_mapping(LADMNames.ISO19107_MODEL_KEY)
            },
            LADMNames.CATALOG_OBJECTS_MODEL_KEY: {
                MODEL_ALIAS: QCoreApplication.translate("TranslatableConfigStrings", "Catalog objects"),
                MODEL_IS_SUPPORTED: True,
                MODEL_SUPPORTED_VERSION: "1",
                MODEL_HIDDEN_BY_DEFAULT: True,
                MODEL_CHECKED_BY_DEFAULT: False,
                MODEL_MAPPING: dict()
            },
            LADMNames.QUALITY_ERROR_MODEL_KEY: {
                MODEL_ALIAS: QCoreApplication.translate("TranslatableConfigStrings", "Quality errors"),
                MODEL_IS_SUPPORTED: True,
                MODEL_SUPPORTED_VERSION: "0.1",
                MODEL_HIDDEN_BY_DEFAULT: False,
                MODEL_CHECKED_BY_DEFAULT: False,
                MODEL_MAPPING: db_mapping_config.get_model_mapping(LADMNames.QUALITY_ERROR_MODEL_KEY),
                MODEL_CATALOGS: {'iliValidator': ILIVALIDATOR_ERRORS_CATALOG_PATH,
                                 'IGAC': IGAC_ERRORS_CATALOG_PATH}
            },
            LADMNames.FIELD_DATA_CAPTURE_MODEL_KEY: {
                MODEL_ALIAS: QCoreApplication.translate("TranslatableConfigStrings", "Field data capture"),
                MODEL_IS_SUPPORTED: False,
                MODEL_SUPPORTED_VERSION: "0.1",
                MODEL_HIDDEN_BY_DEFAULT: True,
                MODEL_CHECKED_BY_DEFAULT: False,
                MODEL_ILI2DB_PARAMETERS: {
                    ILI2DB_SCHEMAIMPORT: [(ILI2DB_CREATE_BASKET_COL_KEY, None)]
                },
                MODEL_MAPPING: db_mapping_config.get_model_mapping(LADMNames.FIELD_DATA_CAPTURE_MODEL_KEY)
            }
        }

    def get_model_config(self, model_key):
        # Return a copy to avoid external changes to original config
        return deepcopy(self.__MODEL_CONFIG.get(model_key, dict()))

    def get_models_config(self):
        # Return a copy to avoid external changes to original config
        return deepcopy(self.__MODEL_CONFIG)
