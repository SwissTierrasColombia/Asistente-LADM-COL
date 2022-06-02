from copy import deepcopy

from qgis.PyQt.QtCore import *

from asistente_ladm_col.config.general_config import (FDC_DATASET_NAME,
                                                      SUPPLIES_DB_SOURCE)
from asistente_ladm_col.config.keys.common import *
from asistente_ladm_col.config.gui.gui_config import GUI_Config
from asistente_ladm_col.config.keys.ili2db_keys import *
from asistente_ladm_col.config.quality_rule_config import *


basic_role_gui = GUI_Config().get_gui_dict(TEMPLATE_GUI)
basic_role_gui[TOOLBAR] = [{  # Overwrite list of toolbars
    WIDGET_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "LADM-COL tools"),
    OBJECT_NAME: 'ladm_col_toolbar',
    ACTIONS: [
        {  # List of toolbars
            WIDGET_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Data management"),
            OBJECT_NAME: 'ladm_col_data_management_toolbar',
            ICON: DATA_MANAGEMENT_ICON,
            ACTIONS: [ACTION_SCHEMA_IMPORT,
                      ACTION_IMPORT_DATA,
                      ACTION_EXPORT_DATA]
        },
        SEPARATOR,
        {
            WIDGET_TYPE: MENU,
            WIDGET_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Survey objects"),
            OBJECT_NAME: "ladm_col_survey_toolbar",
            ICON: OPERATION_ICON,
            ACTIONS: [
                ACTION_CREATE_POINT,
                ACTION_CREATE_BOUNDARY,
                SEPARATOR,
                ACTION_CREATE_PLOT,
                ACTION_CREATE_BUILDING,
                ACTION_CREATE_BUILDING_UNIT,
                ACTION_CREATE_RIGHT_OF_WAY,
                ACTION_FILL_RIGHT_OF_WAY_RELATIONS,
                SEPARATOR,
                ACTION_CREATE_EXT_ADDRESS,
                SEPARATOR,
                ACTION_CREATE_PARCEL,
                SEPARATOR,
                ACTION_CREATE_PARTY,
                ACTION_CREATE_GROUP_PARTY,
                SEPARATOR,
                ACTION_CREATE_RIGHT,
                ACTION_CREATE_RESTRICTION,
                SEPARATOR,
                ACTION_CREATE_ADMINISTRATIVE_SOURCE,
                ACTION_CREATE_SPATIAL_SOURCE,
                ACTION_UPLOAD_PENDING_SOURCE
            ]
        },
        SEPARATOR,
        ACTION_FINALIZE_GEOMETRY_CREATION,
        {
            WIDGET_TYPE: MENU,
            WIDGET_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Structuring tools"),
            OBJECT_NAME: "ladm_col_structuring_tools_toolbar",
            ICON: STRUCTURING_TOOLS_ICON,
            ACTIONS: [
                ACTION_BUILD_BOUNDARY,
                ACTION_MOVE_NODES,
                ACTION_FILL_BFS,
                ACTION_FILL_MORE_BFS_AND_LESS
            ]
        },
        SEPARATOR,
        ACTION_LOAD_LAYERS,
        ACTION_PARCEL_QUERY
    ]
}]

supplies_provider_role_gui = GUI_Config().get_gui_dict(TEMPLATE_GUI)
supplies_provider_role_gui[TOOLBAR] = [{  # Overwrite list of toolbars
    WIDGET_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "LADM-COL tools"),
    OBJECT_NAME: 'ladm_col_toolbar',
    ACTIONS: [
        {  # List of toolbars
            WIDGET_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Transitional System"),
            OBJECT_NAME: 'ladm_col_toolbar_st',
            ICON: ST_ICON,
            ACTIONS: [ACTION_ST_LOGIN,
                      ACTION_ST_LOGOUT]
        },
        SEPARATOR,
        ACTION_SCHEMA_IMPORT,
        ACTION_RUN_ETL_SUPPLIES,
        ACTION_FIND_MISSING_COBOL_SUPPLIES,
        ACTION_FIND_MISSING_SNC_SUPPLIES,
        ACTION_LOAD_LAYERS,
        ACTION_EXPORT_DATA
    ]
}]

field_admin_role_gui = GUI_Config().get_gui_dict(TEMPLATE_GUI)
field_admin_role_gui[TOOLBAR] = [{  # Overwrite list of toolbars
    WIDGET_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "LADM-COL tools"),
    OBJECT_NAME: 'ladm_col_toolbar',
    ACTIONS: [
        ACTION_LOAD_LAYERS,
        ACTION_INTEGRATE_SUPPLIES,
        SEPARATOR,
        ACTION_CHECK_QUALITY_RULES,
        ACTION_PARCEL_QUERY,
        SEPARATOR,
        {  # List of toolbars
            WIDGET_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Reports"),
            OBJECT_NAME: 'ladm_col_reports_toolbar',
            ICON: REPORTS_ICON,
            ACTIONS: [
                ACTION_REPORT_ANNEX_17,
                ACTION_REPORT_ANT
            ]
        },
        SEPARATOR,
        ACTION_SETTINGS
    ]
}]

field_coordinator_role_gui = GUI_Config().get_gui_dict(TEMPLATE_GUI)
field_coordinator_role_gui[TOOLBAR] = [{  # Overwrite list of toolbars
    WIDGET_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "LADM-COL tools"),
    OBJECT_NAME: 'ladm_col_toolbar',
    ACTIONS: [
        ACTION_LOAD_LAYERS,
        ACTION_INTEGRATE_SUPPLIES,
        SEPARATOR,
        ACTION_SETTINGS
    ]
}]

operator_role_gui = GUI_Config().get_gui_dict(TEMPLATE_GUI)  # Just use the template GUI config.

manager_role_gui = GUI_Config().get_gui_dict(TEMPLATE_GUI)
manager_role_gui[TOOLBAR] = [{  # Overwrite list of toolbars
    WIDGET_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "LADM-COL tools"),
    OBJECT_NAME: 'ladm_col_toolbar',
    ACTIONS: [
        {  # List of toolbars
            WIDGET_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Transitional System"),
            OBJECT_NAME: 'ladm_col_toolbar_st',
            ICON: ST_ICON,
            ACTIONS: [ACTION_ST_LOGIN,
                      ACTION_ST_LOGOUT]
        },
        SEPARATOR,
        ACTION_LOAD_LAYERS,
        ACTION_INTEGRATE_SUPPLIES,
        SEPARATOR,
        ACTION_CHECK_QUALITY_RULES,
        ACTION_PARCEL_QUERY,
        SEPARATOR,
        {  # List of toolbars
            WIDGET_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Change Detection"),
            OBJECT_NAME: 'ladm_col_change_detection_toolbar',
            ICON: CHANGE_DETECTION_ICON,
            ACTIONS: [
                ACTION_CHANGE_DETECTION_SETTINGS,
                SEPARATOR,
                ACTION_CHANGE_DETECTION_PER_PARCEL,
                ACTION_CHANGE_DETECTION_ALL_PARCELS
            ]
        },
        SEPARATOR,
        {  # List of toolbars
            WIDGET_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Reports"),
            OBJECT_NAME: 'ladm_col_reports_toolbar',
            ICON: REPORTS_ICON,
            ACTIONS: [
                ACTION_REPORT_ANNEX_17,
                ACTION_REPORT_ANT
            ]
        }
    ]
}]

advanced_role_gui = GUI_Config().get_gui_dict(TEMPLATE_GUI)
advanced_role_gui[TOOLBAR] = [{  # List of toolbars
    WIDGET_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "LADM-COL tools"),
    OBJECT_NAME: 'ladm_col_toolbar',
    ACTIONS: [
        {  # List of toolbars
            WIDGET_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Transitional System"),
            OBJECT_NAME: 'ladm_col_st_toolbar',
            ICON: ST_ICON,
            ACTIONS: [ACTION_ST_LOGIN,
                      ACTION_ST_LOGOUT]
        },
        SEPARATOR,
        {
            WIDGET_TYPE: MENU,
            WIDGET_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Survey objects"),
            OBJECT_NAME: "ladm_col_survey_toolbar",
            ICON: OPERATION_ICON,
            ACTIONS: [
                ACTION_CREATE_POINT,
                ACTION_CREATE_BOUNDARY,
                SEPARATOR,
                ACTION_CREATE_PLOT,
                ACTION_CREATE_BUILDING,
                ACTION_CREATE_BUILDING_UNIT,
                ACTION_CREATE_RIGHT_OF_WAY,
                ACTION_FILL_RIGHT_OF_WAY_RELATIONS,
                SEPARATOR,
                ACTION_CREATE_EXT_ADDRESS,
                SEPARATOR,
                ACTION_CREATE_PARCEL,
                SEPARATOR,
                ACTION_CREATE_PARTY,
                ACTION_CREATE_GROUP_PARTY,
                SEPARATOR,
                ACTION_CREATE_RIGHT,
                ACTION_CREATE_RESTRICTION,
                SEPARATOR,
                ACTION_CREATE_ADMINISTRATIVE_SOURCE,
                ACTION_CREATE_SPATIAL_SOURCE,
                ACTION_UPLOAD_PENDING_SOURCE
            ]
        },
        SEPARATOR,
        ACTION_LOAD_LAYERS,
        SEPARATOR,
        ACTION_FINALIZE_GEOMETRY_CREATION,
        ACTION_BUILD_BOUNDARY,
        ACTION_MOVE_NODES,
        SEPARATOR,
        ACTION_FILL_BFS,
        ACTION_FILL_MORE_BFS_AND_LESS,
        SEPARATOR,
        ACTION_SETTINGS
    ]
}]


def get_field_admin_role_models():
    """
    Function to delay configuration for admin role models, since it
    needs to overwrite ili2db params from the main model config
    """
    from asistente_ladm_col.lib.model_registry import LADMColModelRegistry

    field_admin_role_models = COMMON_ROLE_MODELS.copy()
    field_admin_role_models[ROLE_SUPPORTED_MODELS] = COMMON_SUPPORTED_MODELS + [LADMNames.FIELD_DATA_CAPTURE_MODEL_KEY]
    field_admin_role_models[ROLE_CHECKED_MODELS] = [LADMNames.FIELD_DATA_CAPTURE_MODEL_KEY]
    fdc_model = LADMColModelRegistry().model(LADMNames.FIELD_DATA_CAPTURE_MODEL_KEY)
    params = fdc_model.get_ili2db_params()
    if ILI2DB_UPDATE in params:
        params[ILI2DB_UPDATE].append((ILI2DB_DATASET_KEY, FDC_DATASET_NAME))
    else:
        params[ILI2DB_UPDATE] = [(ILI2DB_DATASET_KEY, FDC_DATASET_NAME)]
    field_admin_role_models[ROLE_MODEL_ILI2DB_PARAMETERS] = {LADMNames.FIELD_DATA_CAPTURE_MODEL_KEY: params}
    return field_admin_role_models

field_coordinator_role_models = COMMON_ROLE_MODELS.copy()
field_coordinator_role_models[ROLE_SUPPORTED_MODELS] = COMMON_SUPPORTED_MODELS + [LADMNames.FIELD_DATA_CAPTURE_MODEL_KEY]
field_coordinator_role_models[ROLE_CHECKED_MODELS] = [LADMNames.FIELD_DATA_CAPTURE_MODEL_KEY]

advanced_role_models = COMMON_ROLE_MODELS.copy()
advanced_role_models[ROLE_SUPPORTED_MODELS] = COMMON_SUPPORTED_MODELS + [LADMNames.FIELD_DATA_CAPTURE_MODEL_KEY]
advanced_role_models[ROLE_CHECKED_MODELS] = COMMON_CHECKED_MODELS


def get_role_config():
    return deepcopy({
        BASIC_ROLE: {
            ROLE_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Basic"),
            ROLE_DESCRIPTION: QCoreApplication.translate("AsistenteLADMCOLPlugin",
                                                         "The <b>Basic</b> role helps you to explore the LADM-COL assistant main functionalities.<br><br>This is the <b>recommended role</b> if you are just getting started with the LADM-COL assistant."),
            ROLE_ENABLED: True,
            ROLE_MODELS: COMMON_ROLE_MODELS,
            ROLE_ACTIONS: [
                ACTION_DOWNLOAD_GUIDE,
                ACTION_CREATE_POINT,
                ACTION_CREATE_BOUNDARY,
                ACTION_CREATE_PLOT,
                ACTION_CREATE_BUILDING,
                ACTION_CREATE_BUILDING_UNIT,
                ACTION_CREATE_RIGHT_OF_WAY,
                ACTION_CREATE_EXT_ADDRESS,
                ACTION_CREATE_PARCEL,
                ACTION_CREATE_RIGHT,
                ACTION_CREATE_RESTRICTION,
                ACTION_CREATE_PARTY,
                ACTION_CREATE_GROUP_PARTY,
                ACTION_CREATE_ADMINISTRATIVE_SOURCE,
                ACTION_CREATE_SPATIAL_SOURCE,
                ACTION_UPLOAD_PENDING_SOURCE,
                ACTION_IMPORT_FROM_INTERMEDIATE_STRUCTURE,
                ACTION_FIX_LADM_COL_RELATIONS,
                ACTION_BUILD_BOUNDARY,
                ACTION_MOVE_NODES,
                ACTION_FINALIZE_GEOMETRY_CREATION,
                ACTION_FILL_BFS,
                ACTION_FILL_MORE_BFS_AND_LESS,
                ACTION_FILL_RIGHT_OF_WAY_RELATIONS,
                ACTION_PARCEL_QUERY,
                ACTION_CHECK_QUALITY_RULES],
            ROLE_QUALITY_RULES: [
                QR_ILIVALIDATORR0001,
                QR_IGACR1001,
                #QR_IGACR2001,
                #QR_IGACR3006,
                QR_IGACR4001,
                QR_IGACR4005
            ],
            ROLE_GUI_CONFIG: {TEMPLATE_GUI: basic_role_gui}
        },
        SUPPLIES_PROVIDER_ROLE: {
            ROLE_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Supplies Provider"),
            ROLE_DESCRIPTION: QCoreApplication.translate("AsistenteLADMCOLPlugin",
                                                         "The <b>Supplies Provider</b> role generates a XTF file with supplies data for the operators."),
            ROLE_ENABLED: True,
            ROLE_DB_SOURCE: SUPPLIES_DB_SOURCE,
            ROLE_MODELS: {
                ROLE_SUPPORTED_MODELS: [LADMNames.LADM_COL_MODEL_KEY,
                                        LADMNames.SUPPLIES_MODEL_KEY,
                                        LADMNames.SNR_DATA_SUPPLIES_MODEL_KEY,
                                        LADMNames.SUPPLIES_INTEGRATION_MODEL_KEY,
                                        LADMNames.ISO19107_MODEL_KEY],
                ROLE_HIDDEN_MODELS: COMMON_HIDDEN_MODELS,
                ROLE_CHECKED_MODELS: [LADMNames.SUPPLIES_MODEL_KEY,
                                      LADMNames.SUPPLIES_INTEGRATION_MODEL_KEY]
            },
            ROLE_ACTIONS: [
                ACTION_RUN_ETL_SUPPLIES,
                ACTION_FIND_MISSING_COBOL_SUPPLIES,
                ACTION_FIND_MISSING_SNC_SUPPLIES,
                ACTION_ST_LOGIN,
                ACTION_ST_LOGOUT
            ],
            ROLE_QUALITY_RULES: list(),
            ROLE_GUI_CONFIG: {TEMPLATE_GUI: supplies_provider_role_gui}
        },
        FIELD_ADMIN_ROLE: {
            ROLE_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Field administrator"),
            ROLE_DESCRIPTION: QCoreApplication.translate("AsistenteLADMCOLPlugin",
                                                         "The <b>field administrator</b> assigns parcel sets to field coordinators and synchronizes back the data they have structured from field surveys."),
            ROLE_ENABLED: False,
            ROLE_MODELS: get_field_admin_role_models(),
            ROLE_ACTIONS: [
                ACTION_XTF_MODEL_CONVERTER,
                ACTION_ALLOCATE_PARCELS_FIELD_DATA_CAPTURE,
                #  ACTION_SYNCHRONIZE_FIELD_DATA,
                ACTION_INTEGRATE_SUPPLIES,
                ACTION_PARCEL_QUERY,
                ACTION_CHECK_QUALITY_RULES],
            ROLE_QUALITY_RULES: ALL_QUALITY_RULES,
            ROLE_GUI_CONFIG: {TEMPLATE_GUI: field_admin_role_gui}
        },
        FIELD_COORDINATOR_ROLE: {
            ROLE_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Field coordinator"),
            ROLE_DESCRIPTION: QCoreApplication.translate("AsistenteLADMCOLPlugin",
                                                         "The <b>field coordinator</b> assigns parcel sets to surveyors and synchronizes back the data they collected in the field."),
            ROLE_ENABLED: False,
            ROLE_MODELS: field_coordinator_role_models,
            ROLE_ACTIONS: [
                ACTION_XTF_MODEL_CONVERTER,
                ACTION_ALLOCATE_PARCELS_FIELD_DATA_CAPTURE
                #  ACTION_SYNCHRONIZE_FIELD_DATA],
            ],
            ROLE_QUALITY_RULES: list(),
            ROLE_GUI_CONFIG: {TEMPLATE_GUI: field_coordinator_role_gui}
        },
        OPERATOR_ROLE: {
            ROLE_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Operator"),
            ROLE_DESCRIPTION: QCoreApplication.translate("AsistenteLADMCOLPlugin",
                                                         "The <b>Operator</b> is in charge of capturing current cadastral data."),
            ROLE_ENABLED: True,
            ROLE_MODELS: COMMON_ROLE_MODELS,
            ROLE_ACTIONS: [
                ACTION_XTF_MODEL_CONVERTER,
                ACTION_CREATE_POINT,
                ACTION_CREATE_BOUNDARY,
                ACTION_CREATE_PLOT,
                ACTION_CREATE_BUILDING,
                ACTION_CREATE_BUILDING_UNIT,
                ACTION_CREATE_RIGHT_OF_WAY,
                ACTION_CREATE_EXT_ADDRESS,
                ACTION_CREATE_PARCEL,
                ACTION_CREATE_RIGHT,
                ACTION_CREATE_RESTRICTION,
                ACTION_CREATE_PARTY,
                ACTION_CREATE_GROUP_PARTY,
                ACTION_CREATE_ADMINISTRATIVE_SOURCE,
                ACTION_CREATE_SPATIAL_SOURCE,
                ACTION_UPLOAD_PENDING_SOURCE,
                ACTION_IMPORT_FROM_INTERMEDIATE_STRUCTURE,
                ACTION_FIX_LADM_COL_RELATIONS,
                ACTION_BUILD_BOUNDARY,
                ACTION_MOVE_NODES,
                ACTION_FINALIZE_GEOMETRY_CREATION,
                ACTION_FILL_BFS,
                ACTION_FILL_MORE_BFS_AND_LESS,
                ACTION_FILL_RIGHT_OF_WAY_RELATIONS,
                ACTION_CHANGE_DETECTION_SETTINGS,
                ACTION_CHANGE_DETECTION_ALL_PARCELS,
                ACTION_CHANGE_DETECTION_PER_PARCEL,
                ACTION_ST_LOGIN,
                ACTION_ST_LOGOUT,
                ACTION_PARCEL_QUERY,
                ACTION_CHECK_QUALITY_RULES],
            ROLE_QUALITY_RULES: ALL_QUALITY_RULES,
            ROLE_GUI_CONFIG: {TEMPLATE_GUI: operator_role_gui}
        },
        MANAGER_ROLE: {
            ROLE_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Manager"),
            ROLE_DESCRIPTION: QCoreApplication.translate("AsistenteLADMCOLPlugin",
                                                         "The <b>Manager</b> is in charge of preparing supplies for operators as well as validating and managing the data provided by operators."),
            ROLE_ENABLED: True,
            ROLE_MODELS: COMMON_ROLE_MODELS,
            ROLE_ACTIONS: [
                ACTION_XTF_MODEL_CONVERTER,
                ACTION_CHANGE_DETECTION_SETTINGS,
                ACTION_CHANGE_DETECTION_ALL_PARCELS,
                ACTION_CHANGE_DETECTION_PER_PARCEL,
                ACTION_ST_LOGIN,
                ACTION_ST_LOGOUT,
                ACTION_REPORT_ANNEX_17,
                ACTION_REPORT_ANT,
                ACTION_INTEGRATE_SUPPLIES,
                ACTION_PARCEL_QUERY,
                ACTION_CHECK_QUALITY_RULES],
            ROLE_QUALITY_RULES: ALL_QUALITY_RULES,
            ROLE_GUI_CONFIG: {TEMPLATE_GUI: manager_role_gui}
        },
        ADVANCED_ROLE: {
            ROLE_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Advanced"),
            ROLE_DESCRIPTION: QCoreApplication.translate("AsistenteLADMCOLPlugin",
                                                         "The <b>Advanced</b> role has access to all the functionality."),
            ROLE_ENABLED: True,
            ROLE_MODELS: COMMON_ROLE_MODELS,  # advanced_role_models,
            ROLE_ACTIONS: [ALL_ACTIONS],
            ROLE_QUALITY_RULES: ALL_QUALITY_RULES,
            ROLE_GUI_CONFIG: {TEMPLATE_GUI: advanced_role_gui}
        }
    })
