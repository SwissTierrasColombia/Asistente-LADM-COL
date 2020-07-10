from qgis.PyQt.QtCore import *

from asistente_ladm_col.config.gui.common_keys import *
from asistente_ladm_col.config.gui.gui_config import GUI_Config


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
        ACTION_LOAD_LAYERS,
        ACTION_EXPORT_DATA
    ]
}]

operator_role_gui = {}  # Let the gui builder use the template GUI config.

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


ROLE_CONFIG = {
    BASIC_ROLE: {
        ROLE_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Basic"),
        ROLE_DESCRIPTION: QCoreApplication.translate("AsistenteLADMCOLPlugin",
                                                     "The basic role helps you to explore the LADM-COL assistant main functionalities."),
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
            ACTION_CHECK_QUALITY_RULES
        ],
        ROLE_GUI_CONFIG: basic_role_gui
    },
    SUPPLIES_PROVIDER_ROLE: {
        ROLE_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Supplies Provider"),
        ROLE_DESCRIPTION: QCoreApplication.translate("AsistenteLADMCOLPlugin",
                                                     "The Supplies Provider role generates a XTF file with supplies data for the Manager role."),
        ROLE_ACTIONS: [
            ACTION_RUN_ETL_SUPPLIES,
            ACTION_FIND_MISSING_COBOL_SUPPLIES,
            ACTION_ST_LOGIN,
            ACTION_ST_LOGOUT
        ],
        ROLE_GUI_CONFIG: supplies_provider_role_gui
    },
    OPERATOR_ROLE: {
        ROLE_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Operator"),
        ROLE_DESCRIPTION: QCoreApplication.translate("AsistenteLADMCOLPlugin",
                                                     "The operator is in charge of capturing current cadastral data."),
        ROLE_ACTIONS: [
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
            ACTION_CHECK_QUALITY_RULES
        ],
        ROLE_GUI_CONFIG: operator_role_gui
    },
    MANAGER_ROLE: {
        ROLE_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Manager"),
        ROLE_DESCRIPTION: QCoreApplication.translate("AsistenteLADMCOLPlugin",
                                                     "The manager is in charge of preparing supplies for operators as well as validating and managing the data provided by operators."),
        ROLE_ACTIONS: [
            ACTION_CHANGE_DETECTION_SETTINGS,
            ACTION_CHANGE_DETECTION_ALL_PARCELS,
            ACTION_CHANGE_DETECTION_PER_PARCEL,
            ACTION_ST_LOGIN,
            ACTION_ST_LOGOUT,
            ACTION_REPORT_ANNEX_17,
            ACTION_REPORT_ANT,
            ACTION_INTEGRATE_SUPPLIES,
            ACTION_PARCEL_QUERY,
            ACTION_CHECK_QUALITY_RULES
        ],
        ROLE_GUI_CONFIG: manager_role_gui
    },
    ADVANCED_ROLE: {
        ROLE_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Advanced"),
        ROLE_DESCRIPTION: QCoreApplication.translate("AsistenteLADMCOLPlugin",
                                                     "The advanced role has access to all the functionality."),
        ROLE_ACTIONS: [ALL_ACTIONS],
        ROLE_GUI_CONFIG: advanced_role_gui
    }
}