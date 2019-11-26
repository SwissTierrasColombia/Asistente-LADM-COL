# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-11-07
        copyright            : (C) 2019 by Germán Carrillo (BSF Swissphoto)
        email                : gcarrillo@linuxmail.org
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""

from copy import deepcopy

from qgis.PyQt.QtCore import (QCoreApplication,
                              QSettings)

from asistente_ladm_col.config.gui.common_keys import *
from asistente_ladm_col.utils.singleton import Singleton
from asistente_ladm_col.lib.logger import Logger

class Role_Registry(metaclass=Singleton):
    """
    Manage all role information. Current role can also be got/set from this class.
    """
    COMMON_ACTIONS = [  # Common actions for all roles
        ACTION_LOAD_LAYERS,
        ACTION_SCHEMA_IMPORT,
        ACTION_IMPORT_DATA,
        ACTION_EXPORT_DATA,
        ACTION_SETTINGS,
        ACTION_HELP,
        ACTION_ABOUT
    ]

    def __init__(self):
        self.logger = Logger()
        self._registered_roles = dict()
        self._default_role = BASIC_ROLE

        role = BASIC_ROLE
        role_dict = {
            ROLE_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Basic"),
            ROLE_DESCRIPTION: QCoreApplication.translate("AsistenteLADMCOLPlugin",
                                                         "The basic role helps you to explore the LADM_COL assistant main functionalities."),
            ROLE_ACTIONS: [],
            ROLE_GUI_CONFIG: {}  # Empty to let other modules decide on a default gui_config dict
        }
        self.register_role(role, role_dict)

        role = OPERATOR_ROLE
        role_dict = {
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
                ACTION_MOVE_NODES,
                ACTION_FINALIZE_GEOMETRY_CREATION
            ],
            ROLE_GUI_CONFIG: {}
        }
        self.register_role(role, role_dict)

        role = MANAGER_ROLE
        role_dict = {
            ROLE_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Manager"),
            ROLE_DESCRIPTION: QCoreApplication.translate("AsistenteLADMCOLPlugin",
                                                         "The manager is in charge of preparing supplies for operators as well as validatinsg and managing the data provided by operators."),
            ROLE_ACTIONS: [
                ACTION_PARCEL_QUERY,
                ACTION_REPORT_ANNEX_17,
                ACTION_REPORT_ANT,
                ACTION_OFFICIAL_SETTINGS,
                ACTION_CHANGE_DETECTION_PER_PARCEL,
                ACTION_CHANGE_DETECTION_ALL_PARCELS,
                ACTION_RUN_ETL_SNC,
                ACTION_RUN_ETL_COBOL,
                ACTION_INTEGRATE_SUPPLIES,
                ACTION_ST_LOGIN,
                ACTION_ST_LOGOUT
            ],
            ROLE_GUI_CONFIG: {}
        }
        self.register_role(role, role_dict)

        role = ADVANCED_ROLE
        role_dict = {
            ROLE_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Advanced"),
            ROLE_DESCRIPTION: QCoreApplication.translate("AsistenteLADMCOLPlugin",
                                                         "The advanced role has access to all the functionality."),
            ROLE_ACTIONS: [ALL_ACTIONS],
                ROLE_GUI_CONFIG: {
                    MAIN_MENU: [{ # List of main menus
                        WIDGET_TYPE: MENU,
                        WIDGET_NAME: "LAD&M_COL DATA",
                        OBJECT_NAME: 'main_menu_2',
                        ACTIONS: [{
                                WIDGET_TYPE: MENU,
                                WIDGET_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Data Management"),
                                OBJECT_NAME: "ladm_col_data_management_menu2",
                                ICON: DATA_MANAGEMENT_ICON,
                                ACTIONS: [
                                    ACTION_SCHEMA_IMPORT,
                                    ACTION_IMPORT_DATA,
                                    ACTION_EXPORT_DATA
                                ]
                            },
                            ACTION_ABOUT
                        ]
                        },{
                            WIDGET_TYPE: MENU,
                            WIDGET_NAME: "LAD&M_COL",
                            OBJECT_NAME: 'main_menu',
                            ACTIONS: [
                                ACTION_LOAD_LAYERS,
                                SEPARATOR,
                                {
                                    WIDGET_TYPE: MENU,
                                    WIDGET_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Supplies"),
                                    OBJECT_NAME: "ladm_col_supplies_menu",
                                    ICON: SUPPLIES_ICON,
                                    ACTIONS: [
                                        ACTION_RUN_ETL_COBOL,
                                        ACTION_RUN_ETL_SNC,
                                        ACTION_INTEGRATE_SUPPLIES
                                    ]
                                }, {
                                    WIDGET_TYPE: MENU,
                                    WIDGET_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Operation"),
                                    OBJECT_NAME: "ladm_col_operation_menu",
                                    ICON: OPERATION_ICON,
                                    ACTIONS: [
                                        {
                                            WIDGET_TYPE: MENU,
                                            WIDGET_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Surveying and Representation"),
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
                                            WIDGET_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Basic Administrative Unit"),
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
                                ACTION_CHECK_QUALITY_RULES,
                                SEPARATOR,
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
                                }, {
                                    WIDGET_TYPE: MENU,
                                    WIDGET_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Change Detection"),
                                    OBJECT_NAME: "ladm_col_change_detection_menu",
                                    ICON: CHANGE_DETECTION_ICON,
                                    ACTIONS: [
                                        ACTION_CHANGE_DETECTION_PER_PARCEL,
                                        ACTION_CHANGE_DETECTION_ALL_PARCELS,
                                        SEPARATOR,
                                        ACTION_OFFICIAL_SETTINGS
                                    ]
                                },
                                SEPARATOR,
                                ACTION_SETTINGS,
                                SEPARATOR,
                                ACTION_HELP,
                                ACTION_ABOUT
                            ]
                    }], TOOLBAR: [{  # List of toolbars
                        WIDGET_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "LADM-COL tools 2"),
                        OBJECT_NAME: 'ladm_col_toolbar2',
                        ACTIONS: [
                            ACTION_OFFICIAL_SETTINGS,
                            SEPARATOR,
                            {  # List of toolbars
                                WIDGET_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "LADM-COL tools3"),
                                OBJECT_NAME: 'ladm_col_toolbar3',
                                ACTIONS: [ACTION_REPORT_ANNEX_17,
                                          ACTION_ABOUT]
                            }
                        ]
                    }, {
                        WIDGET_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "LADM-COL tools"),
                        OBJECT_NAME: 'ladm_col_toolbar',
                        ACTIONS: [
                            ACTION_FINALIZE_GEOMETRY_CREATION,
                            ACTION_BUILD_BOUNDARY,
                            ACTION_MOVE_NODES,
                            ACTION_FILL_BFS,
                            ACTION_FILL_MORE_BFS_AND_LESS,
                            ACTION_IMPORT_FROM_INTERMEDIATE_STRUCTURE
                        ]
                    }]
                }
        }
        self.register_role(role, role_dict)

    def register_role(self, role_key, role_dict):
        """
        Register roles for the LADM_COL assistant. Roles have access only to certain GUI controls.

        :param role_key: Role unique identifier
        :param role_dict: Dictionary with the following information:
                ROLE_NAME: Name of the role
                ROLE_DESCRIPTION: Explains what this role is about
                ROLE_ACTIONS: List of actions a role has access to
        :return: Whether the role was successfully registered or not.
        """
        valid = False
        if ROLE_NAME in role_dict and ROLE_DESCRIPTION in role_dict and ROLE_ACTIONS in role_dict and ROLE_GUI_CONFIG in role_dict:
            self._registered_roles[role_key] = deepcopy(role_dict)
            valid = True
        else:
            self.logger.error(__name__, "Role '{}' is not defined correctly and could not be registered! Check the role_dict parameter.".format(role_key))

        return valid

    def get_active_role(self):
        return QSettings().value("Asistente-LADM_COL/roles/current_role_key", self._default_role)

    def active_role_already_set(self):
        """
        Whether we have set an active role already or not.

        :return: True if the current_role_key variable is stored in QSettings. False otherwise.
        """
        return QSettings().value("Asistente-LADM_COL/roles/current_role_key", False) is not False

    def set_active_role(self, role_key):
        res = False
        if role_key in self._registered_roles:
            res = True
        else:
            self.logger.warning(__name__, "Role '{}' was not found, the default role is now active.".format(role_key))
            role_key = self._default_role

        QSettings().setValue("Asistente-LADM_COL/roles/current_role_key", role_key)
        self.logger.info(__name__, "Role '{}' is now active!".format(role_key))

        return res

    def set_active_default_role(self):
        QSettings().setValue("Asistente-LADM_COL/roles/current_role_key", self._default_role)
        self.logger.info(__name__, "Default role '{}' is now active!".format(self._default_role))
        return True

    def get_roles_info(self):
        return {k: v[ROLE_NAME] for k,v in self._registered_roles.items()}

    def get_role_description(self, role_key):
        if role_key not in self._registered_roles:
            self.logger.error(__name__, "Role '{}' was not found, returning default role's decription".format(role_key))
            role_key = self._default_role

        return self._registered_roles[role_key][ROLE_DESCRIPTION]

    def get_role_actions(self, role_key):
        if role_key not in self._registered_roles:
            self.logger.error(__name__, "Role '{}' was not found, returning default role's actions.".format(role_key))
            role_key = self._default_role

        return list(set(self._registered_roles[role_key][ROLE_ACTIONS] + self.COMMON_ACTIONS))

    def get_role_gui_config(self, role_key):
        if role_key not in self._registered_roles:
            self.logger.error(__name__, "Role '{}' was not found, returning default role's GUI configuration.".format(role_key))
            role_key = self._default_role

        return self._registered_roles[role_key][ROLE_GUI_CONFIG]
