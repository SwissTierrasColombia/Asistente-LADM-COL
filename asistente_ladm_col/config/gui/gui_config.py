from copy import deepcopy

from qgis.PyQt.QtCore import (QCoreApplication,
                              QObject)

from asistente_ladm_col.config.gui.common_keys import *


class GUI_Config(QObject):
    """
    Holds common GUI dict definitions. These are independent of roles.

    Each dict found here can be used as a GUI (both toolbar and menus) configuration. The GUI Builder takes such
    configuration is taken as the basis to start showing or hiding actions depending on the active role, actions
    supported  by the active DB engine,
    """
    DEFAULT_GUI_CONFIG_DICT = {
        MAIN_MENU: [{  # List of main menus
            WIDGET_TYPE: MENU,
            WIDGET_NAME: "LAD&M-COL",
            OBJECT_NAME: MENU_LADM_COL_OBJECTNAME,
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
                {
                    WIDGET_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Transitional System"),
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
            ACTIONS: []  # This toolbar shouldn't be shown because of the empty actions
        }]
    }

    TEMPLATE_GUI_CONFIG_DICT = {
        MAIN_MENU: [{  # List of main menus
            WIDGET_TYPE: MENU,
            WIDGET_NAME: "LAD&M-COL",
            OBJECT_NAME: MENU_LADM_COL_OBJECTNAME,
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
                        ACTION_EXPORT_DATA,
                        ACTION_XTF_MODEL_CONVERSION
                    ]
                }, {
                    WIDGET_TYPE: MENU,
                    WIDGET_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Data capture and structuring"),
                    OBJECT_NAME: "ladm_col_data_capture_and_structuring_menu",
                    ICON: DATA_CREATION_ICON,
                    ACTIONS: [
                        {
                            WIDGET_TYPE: MENU,
                            WIDGET_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Survey"),
                            OBJECT_NAME: MENU_SURVEY_OBJECTNAME,
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
                                        ACTION_CREATE_SPATIAL_SOURCE
                                    ]
                                }
                            ]
                        },
                        SEPARATOR,
                        ACTION_UPLOAD_PENDING_SOURCE,
                        ACTION_IMPORT_FROM_INTERMEDIATE_STRUCTURE,
                        SEPARATOR,
                        ACTION_FIX_LADM_COL_RELATIONS
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
                        ACTION_RUN_ETL_SUPPLIES,
                        ACTION_INTEGRATE_SUPPLIES,
                        ACTION_FIND_MISSING_COBOL_SUPPLIES,
                        ACTION_FIND_MISSING_SNC_SUPPLIES
                    ]
                },
                SEPARATOR,
                {
                    WIDGET_TYPE: MENU,
                    WIDGET_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Field data capture"),
                    OBJECT_NAME: "field_data_capture_menu",
                    ICON: FIELD_DATA_CAPTURE_ICON,
                    ACTIONS: [
                        ACTION_ALLOCATE_PARCELS_FIELD_DATA_CAPTURE,
                        ACTION_SYNCHRONIZE_FIELD_DATA
                    ]
                },
                SEPARATOR,
                ACTION_CHECK_QUALITY_RULES,
                ACTION_PARCEL_QUERY,
                {
                    WIDGET_TYPE: MENU,
                    WIDGET_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Reports"),
                    OBJECT_NAME: MENU_REPORTS_OBJECTNAME,
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
                    WIDGET_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Transitional System"),
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
                ACTION_FILL_MORE_BFS_AND_LESS
            ]
        }]
    }

    def __init__(self):
        QObject.__init__(self)

    def get_gui_dict(self, name):
        """
        Gets a GUI config dict for both Toolbars and Menus.

        :param name: Either TEMPLATE_GUI or DEFAULT_GUI (or more if GUI_Congif() has more dict keys)
        :return: A deep copy (i.e., it's safe to alter it) of the GUI config dictionary
        """
        return deepcopy(getattr(self, "{}_CONFIG_DICT".format(name), self.DEFAULT_GUI_CONFIG_DICT))
