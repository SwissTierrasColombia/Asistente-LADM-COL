from copy import deepcopy

from qgis.PyQt.QtCore import (QCoreApplication,
                              QObject)

from .common_keys import *


class GUI_Config(QObject):
    """
    Holds common GUI dict definitions. These are independent of roles.
    """
    DEFAULT_GUI_CONFIG_DICT = {
        MAIN_MENU: [{  # List of main menus
            WIDGET_TYPE: MENU,
            WIDGET_NAME: "LAD&M_COL",
            OBJECT_NAME: 'main_menu',
            ACTIONS: [
                {
                    WIDGET_TYPE: MENU,
                    WIDGET_NAME: "Empty menu",
                    OBJECT_NAME: 'empty_menu',
                    ACTIONS: []  # This menu is removed because of the empty actions
                }, {
                    WIDGET_TYPE: MENU,
                    WIDGET_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Data management"),
                    OBJECT_NAME: "ladm_col_data_management_menu",
                    ICON: DATA_MANAGEMENT_ICON,
                    ACTIONS: [
                        ACTION_SCHEMA_IMPORT
                    ]
                },
                SEPARATOR,
                ACTION_SETTINGS,
                SEPARATOR,
                ACTION_HELP,
                ACTION_ABOUT
            ]
        }], TOOLBAR: [{  # List of toolbars
            WIDGET_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "LADM-COL tools"),
            OBJECT_NAME: 'ladm_col_toolbar',
            ACTIONS: [
                ACTION_FINALIZE_GEOMETRY_CREATION,
                ACTION_IMPORT_FROM_INTERMEDIATE_STRUCTURE
            ]
        }]
    }

    TEMPLATE_GUI_CONFIG_DICT = {
        MAIN_MENU: [{  # List of main menus
            WIDGET_TYPE: MENU,
            WIDGET_NAME: "LAD&M_COL",
            OBJECT_NAME: 'main_menu',
            ACTIONS: [
                ACTION_DOWNLOAD_GUIDE,
                SEPARATOR,
                {
                    WIDGET_TYPE: MENU,
                    WIDGET_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Data management"),
                    OBJECT_NAME: "ladm_col_data_management_menu",
                    ICON: DATA_MANAGEMENT_ICON,
                    ACTIONS: [
                        ACTION_SCHEMA_IMPORT,
                        ACTION_IMPORT_DATA,
                        ACTION_EXPORT_DATA
                    ]
                }, {
                    WIDGET_TYPE: MENU,
                    WIDGET_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Data capture and structuring"),
                    OBJECT_NAME: "ladm_col_data_capture_and_structuring_menu",
                    ICON: DATA_CREATION_ICON,
                    ACTIONS: [
                        {
                            WIDGET_TYPE: MENU,
                            WIDGET_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Operation"),
                            OBJECT_NAME: "ladm_col_operation_menu",
                            ICON: OPERATION_ICON,
                            ACTIONS: [
                                {
                                    WIDGET_TYPE: MENU,
                                    WIDGET_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin",
                                                                            "Surveying and Representation"),
                                    OBJECT_NAME: "surveying and representation_menu",
                                    ICON: SURVEYING_ICON,
                                    ACTIONS: [
                                        ACTION_CREATE_POINT,
                                        ACTION_CREATE_BOUNDARY
                                    ]
                                },
                                {
                                    WIDGET_TYPE: MENU,
                                    WIDGET_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Spatial Unit"),
                                    OBJECT_NAME: "spatial unit_menu",
                                    ICON: SPATIAL_UNIT_ICON,
                                    ACTIONS: [
                                        ACTION_CREATE_PLOT,
                                        ACTION_CREATE_BUILDING,
                                        ACTION_CREATE_BUILDING_UNIT,
                                        SEPARATOR,
                                        ACTION_CREATE_RIGHT_OF_WAY,
                                        ACTION_FILL_RIGHT_OF_WAY_RELATIONS,
                                        SEPARATOR,
                                        ACTION_CREATE_EXT_ADDRESS
                                    ]
                                }, {
                                    WIDGET_TYPE: MENU,
                                    WIDGET_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin",
                                                                            "Basic Administrative Unit"),
                                    OBJECT_NAME: "basic administrative unit_menu",
                                    ICON: BA_UNIT_ICON,
                                    ACTIONS: [ACTION_CREATE_PARCEL]
                                }, {
                                    WIDGET_TYPE: MENU,
                                    WIDGET_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "RRR"),
                                    OBJECT_NAME: "rrr_menu",
                                    ICON: RRR_ICON,
                                    ACTIONS: [
                                        ACTION_CREATE_RIGHT,
                                        ACTION_CREATE_RESTRICTION
                                    ]
                                }, {
                                    WIDGET_TYPE: MENU,
                                    WIDGET_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Party"),
                                    OBJECT_NAME: "party_menu",
                                    ICON: PARTY_ICON,
                                    ACTIONS: [
                                        ACTION_CREATE_PARTY,
                                        ACTION_CREATE_GROUP_PARTY
                                    ]
                                }, {
                                    WIDGET_TYPE: MENU,
                                    WIDGET_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Source"),
                                    OBJECT_NAME: "source_menu",
                                    ICON: SOURCE_ICON,
                                    ACTIONS: [
                                        ACTION_CREATE_ADMINISTRATIVE_SOURCE,
                                        ACTION_CREATE_SPATIAL_SOURCE,
                                        ACTION_UPLOAD_PENDING_SOURCE
                                    ]
                                }
                            ]
                        },
                        SEPARATOR,
                        ACTION_IMPORT_FROM_INTERMEDIATE_STRUCTURE
                    ]
                },
                ACTION_LOAD_LAYERS,
                SEPARATOR,
                {
                    WIDGET_TYPE: MENU,
                    WIDGET_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Supplies management"),
                    OBJECT_NAME: "ladm_col_supplies_menu",
                    ICON: SUPPLIES_ICON,
                    ACTIONS: [
                        ACTION_RUN_ETL_COBOL,
                        ACTION_RUN_ETL_SNC,
                        ACTION_INTEGRATE_SUPPLIES,
                        ACTION_FIND_MISSING_COBOL_SUPPLIES
                    ]
                },
                SEPARATOR,
                ACTION_CHECK_QUALITY_RULES,
                ACTION_PARCEL_QUERY,
                {
                    WIDGET_TYPE: MENU,
                    WIDGET_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Reports"),
                    OBJECT_NAME: "ladm_col_reports_menu",
                    ICON: REPORTS_ICON,
                    ACTIONS: [
                        ACTION_REPORT_ANNEX_17,
                        ACTION_REPORT_ANT
                    ]
                },
                SEPARATOR,
                {
                    WIDGET_TYPE: MENU,
                    WIDGET_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Change detection"),
                    OBJECT_NAME: "ladm_col_change_detection_menu",
                    ICON: CHANGE_DETECTION_ICON,
                    ACTIONS: [
                        ACTION_CHANGE_DETECTION_SETTINGS,
                        SEPARATOR,
                        ACTION_CHANGE_DETECTION_PER_PARCEL,
                        ACTION_CHANGE_DETECTION_ALL_PARCELS
                    ]
                },
                SEPARATOR,
                {
                    WIDGET_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Transition System"),
                    OBJECT_NAME: 'ladm_col_st_menu',
                    ICON: ST_ICON,
                    ACTIONS: [ACTION_ST_LOGIN,
                              ACTION_ST_LOGOUT]
                },
                SEPARATOR,
                ACTION_SETTINGS,
                SEPARATOR,
                ACTION_HELP,
                ACTION_ABOUT
            ]
        }], TOOLBAR: [{  # List of toolbars
            WIDGET_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "LADM-COL tools"),
            OBJECT_NAME: 'ladm_col_toolbar',
            ACTIONS: [
                {  # List of toolbars
                    WIDGET_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Transition System"),
                    OBJECT_NAME: 'ladm_col_st_toolbar',
                    ICON: ST_ICON,
                    ACTIONS: [ACTION_ST_LOGIN,
                              ACTION_ST_LOGOUT]
                },
                SEPARATOR,
                {
                    WIDGET_TYPE: MENU,
                    WIDGET_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Operation objects"),
                    OBJECT_NAME: "ladm_col_operation_toolbar",
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
                ACTION_FILL_MORE_BFS_AND_LESS
            ]
        }]
    }

    def __init__(self):
        QObject.__init__(self)

    def get_gui_dict(self, name):
        return deepcopy(getattr(self, "{}_CONFIG_DICT".format(name), self.DEFAULT_GUI_CONFIG_DICT))
