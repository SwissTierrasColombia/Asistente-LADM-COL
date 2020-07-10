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

from qgis.PyQt.QtCore import QSettings

from asistente_ladm_col.config.gui.common_keys import *
from asistente_ladm_col.utils.singleton import Singleton
from asistente_ladm_col.lib.logger import Logger


class RoleRegistry(metaclass=Singleton):
    """
    Manage all role information. Current role can also be got/set from this class.

    Roles can set their own GUI configuration even using and overwriting the template gui config.
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

    def register_role(self, role_key, role_dict):
        """
        Register roles for the LADM-COL assistant. Roles have access only to certain GUI controls.

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
        return QSettings().value("Asistente-LADM-COL/roles/current_role_key", self._default_role)

    def active_role_already_set(self):
        """
        Whether we have set an active role already or not.

        :return: True if the current_role_key variable is stored in QSettings. False otherwise.
        """
        return QSettings().value("Asistente-LADM-COL/roles/current_role_key", False) is not False

    def set_active_role(self, role_key):
        res = False
        if role_key in self._registered_roles:
            res = True
        else:
            self.logger.warning(__name__, "Role '{}' was not found, the default role is now active.".format(role_key))
            role_key = self._default_role

        QSettings().setValue("Asistente-LADM-COL/roles/current_role_key", role_key)
        self.logger.info(__name__, "Role '{}' is now active!".format(role_key))

        return res

    def set_active_default_role(self):
        QSettings().setValue("Asistente-LADM-COL/roles/current_role_key", self._default_role)
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
