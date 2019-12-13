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
from asistente_ladm_col.config.gui.gui_config import GUI_Config
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
        template_gui = GUI_Config().get_gui_dict(TEMPLATE_GUI)
        template_gui[TOOLBAR] = [{  # Overwrite list of toolbars
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
        role_dict = {
            ROLE_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Basic"),
            ROLE_DESCRIPTION: QCoreApplication.translate("AsistenteLADMCOLPlugin",
                                                         "The basic role helps you to explore the LADM_COL assistant main functionalities."),
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
                ACTION_BUILD_BOUNDARY,
                ACTION_MOVE_NODES,
                ACTION_FINALIZE_GEOMETRY_CREATION,
                ACTION_FILL_BFS,
                ACTION_FILL_MORE_BFS_AND_LESS,
                ACTION_FILL_RIGHT_OF_WAY_RELATIONS,
                ACTION_PARCEL_QUERY,
                ACTION_CHECK_QUALITY_RULES
            ],
            ROLE_GUI_CONFIG: template_gui  # Empty to let other modules decide on a default gui_config dict
        }
        self.register_role(role, role_dict)

        role = SUPPLIES_PROVIDER_ROLE
        template_gui = GUI_Config().get_gui_dict(TEMPLATE_GUI)
        template_gui[TOOLBAR] = [{  # Overwrite list of toolbars
            WIDGET_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "LADM-COL tools"),
            OBJECT_NAME: 'ladm_col_toolbar',
            ACTIONS: [
                {  # List of toolbars
                    WIDGET_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Transition System"),
                    OBJECT_NAME: 'ladm_col_toolbar_st',
                    ICON: ST_ICON,
                    ACTIONS: [ACTION_ST_LOGIN,
                              ACTION_ST_LOGOUT]
                },
                SEPARATOR,
                ACTION_SCHEMA_IMPORT,
                ACTION_RUN_ETL_COBOL,
                ACTION_RUN_ETL_SNC,
                ACTION_FIND_MISSING_COBOL_SUPPLIES,
                ACTION_LOAD_LAYERS,
                ACTION_EXPORT_DATA
            ]
        }]
        role_dict = {
            ROLE_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Supplies Provider"),
            ROLE_DESCRIPTION: QCoreApplication.translate("AsistenteLADMCOLPlugin",
                "The Supplies Provider role generates a XTF file with supplies data for the Manager role."),
            ROLE_ACTIONS: [
                ACTION_RUN_ETL_COBOL,
                ACTION_RUN_ETL_SNC,
                ACTION_FIND_MISSING_COBOL_SUPPLIES,
                ACTION_ST_LOGIN,
                ACTION_ST_LOGOUT
            ],
            ROLE_GUI_CONFIG: template_gui  # Empty to let other modules decide on a default gui_config dict
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
                ACTION_BUILD_BOUNDARY,
                ACTION_MOVE_NODES,
                ACTION_FINALIZE_GEOMETRY_CREATION,
                ACTION_FILL_BFS,
                ACTION_FILL_MORE_BFS_AND_LESS,
                ACTION_FILL_RIGHT_OF_WAY_RELATIONS,
                ACTION_CHANGE_DETECTION_ALL_PARCELS,
                ACTION_CHANGE_DETECTION_PER_PARCEL,
                ACTION_CHANGE_DETECTION_SETTINGS,
                ACTION_ST_LOGIN,
                ACTION_ST_LOGOUT,
                ACTION_PARCEL_QUERY,
                ACTION_CHECK_QUALITY_RULES
            ],
            ROLE_GUI_CONFIG: {}
        }
        self.register_role(role, role_dict)

        role = MANAGER_ROLE
        template_gui = GUI_Config().get_gui_dict(TEMPLATE_GUI)
        template_gui[TOOLBAR] = [{  # Overwrite list of toolbars
            WIDGET_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "LADM-COL tools"),
            OBJECT_NAME: 'ladm_col_toolbar',
            ACTIONS: [
                {  # List of toolbars
                    WIDGET_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Transition System"),
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
                        ACTION_CHANGE_DETECTION_PER_PARCEL,
                        ACTION_CHANGE_DETECTION_ALL_PARCELS,
                        SEPARATOR,
                        ACTION_CHANGE_DETECTION_SETTINGS
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
        role_dict = {
            ROLE_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Manager"),
            ROLE_DESCRIPTION: QCoreApplication.translate("AsistenteLADMCOLPlugin",
                                                         "The manager is in charge of preparing supplies for operators as well as validating and managing the data provided by operators."),
            ROLE_ACTIONS: [
                ACTION_CHANGE_DETECTION_ALL_PARCELS,
                ACTION_CHANGE_DETECTION_PER_PARCEL,
                ACTION_CHANGE_DETECTION_SETTINGS,
                ACTION_ST_LOGIN,
                ACTION_ST_LOGOUT,
                ACTION_REPORT_ANNEX_17,
                ACTION_REPORT_ANT,
                ACTION_INTEGRATE_SUPPLIES,
                ACTION_PARCEL_QUERY,
                ACTION_CHECK_QUALITY_RULES
            ],
            ROLE_GUI_CONFIG: template_gui
        }
        self.register_role(role, role_dict)

        role = ADVANCED_ROLE
        template_gui = GUI_Config().get_gui_dict(TEMPLATE_GUI)
        template_gui[TOOLBAR] = [{  # List of toolbars
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
                ACTION_FILL_MORE_BFS_AND_LESS,
                SEPARATOR,
                ACTION_SETTINGS
            ]
        }]
        role_dict = {
            ROLE_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Advanced"),
            ROLE_DESCRIPTION: QCoreApplication.translate("AsistenteLADMCOLPlugin",
                                                         "The advanced role has access to all the functionality."),
            ROLE_ACTIONS: [ALL_ACTIONS],
            ROLE_GUI_CONFIG: template_gui
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

    def get_role_name(self, role_key):
        if role_key not in self._registered_roles:
            self.logger.error(__name__, "Role '{}' was not found, returning default role's name".format(role_key))
            role_key = self._default_role

        return self._registered_roles[role_key][ROLE_NAME]

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
