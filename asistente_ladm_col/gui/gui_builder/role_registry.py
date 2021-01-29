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

from qgis.PyQt.QtCore import (QObject,
                              pyqtSignal)

from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.config.gui.common_keys import *
from asistente_ladm_col.utils.singleton import SingletonQObject
from asistente_ladm_col.lib.logger import Logger


class RoleRegistry(QObject, metaclass=SingletonQObject):
    """
    Manage all role information. Current role can also be got/set from this class.

    Roles can set their own GUI configuration, their own LADM-COL supported models,
    their own quality rules, etc.
    """
    active_role_changed = pyqtSignal(str)  # New active role key

    COMMON_ACTIONS = [  # Common actions for all roles
        ACTION_LOAD_LAYERS,
        ACTION_SCHEMA_IMPORT,
        ACTION_IMPORT_DATA,
        ACTION_EXPORT_DATA,
        ACTION_XTF_MODEL_CONVERSION,
        ACTION_SETTINGS,
        ACTION_HELP,
        ACTION_ABOUT
    ]

    def __init__(self):
        QObject.__init__(self)
        self.logger = Logger()
        self.app = AppInterface()
        self._registered_roles = dict()
        self._default_role = BASIC_ROLE

    def register_role(self, role_key, role_dict):
        """
        Register roles for the LADM-COL assistant. Roles have access only to certain GUI controls, to
        certain LADM-COL models and to certain quality rules.

        :param role_key: Role unique identifier
        :param role_dict: Dictionary with the following information:
                ROLE_NAME: Name of the role
                ROLE_DESCRIPTION: Explains what this role is about
                ROLE_ACTIONS: List of actions a role has access to
                ROLE_MODELS: List of models and their configuration for the current role
        :return: Whether the role was successfully registered or not.
        """
        valid = False
        if ROLE_NAME in role_dict and ROLE_DESCRIPTION in role_dict and ROLE_ACTIONS in role_dict and \
                ROLE_GUI_CONFIG in role_dict and ROLE_MODELS in role_dict:
            self._registered_roles[role_key] = deepcopy(role_dict)
            valid = True
        else:
            self.logger.error(__name__, "Role '{}' is not defined correctly and could not be registered! Check the role_dict parameter.".format(role_key))

        return valid

    def get_active_role(self):
        return self.app.settings.active_role or self._default_role

    def get_active_role_name(self):
        return self.get_role_name(self.get_active_role())

    def active_role_already_set(self):
        """
        Whether we have set an active role already or not.

        :return: True if the current_role_key variable is stored in QSettings. False otherwise.
        """
        return self.app.settings.active_role is not None

    def set_active_role(self, role_key, emit_signal=True):
        """
        Set the active role for the plugin.

        :param role_key: Key to identify the role.
        :param emit_signal: Whether the active_role_changed should be emitted or not. A False argument should be passed
                            if the plugin config refresh will be called manually, for instance, because it is safer to
                            call a GUI refresh after closing some plugin dialogs.
        :return: Whether the role was successfully changed or not in the role registry.
        """
        res = False
        if role_key in self._registered_roles:
            res = True
        else:
            self.logger.warning(__name__, "Role '{}' was not found, the default role is now active.".format(role_key))
            role_key = self._default_role

        self.app.settings.active_role = role_key
        self.logger.info(__name__, "Role '{}' is now active!".format(role_key))

        if emit_signal:
            self.active_role_changed.emit(role_key)

        return res

    def set_active_default_role(self, emit_signal=True):
        return self.set_active_role(self._default_role, emit_signal)

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

    def get_role_models(self, role_key):
        """
        Normally you wouldn't need this but LADMColModelRegistry, which is anyway updated when the role changes
        """
        if role_key not in self._registered_roles:
            self.logger.error(__name__, "Role '{}' was not found, returning default role's models.".format(role_key))
            role_key = self._default_role

        return self._registered_roles[role_key][ROLE_MODELS]

    def get_active_role_supported_models(self):
        role_key = self.get_active_role()
        role_models = self.get_role_models(role_key)
        return role_models[ROLE_SUPPORTED_MODELS]

    def get_role_quality_rules(self, role_key):
        if role_key not in self._registered_roles:
            self.logger.error(__name__, "Role '{}' was not found, returning default role's quality rules.".format(role_key))
            role_key = self._default_role

        return self._registered_roles[role_key][ROLE_QUALITY_RULES]

    def get_role_db_source(self, role_key):
        if role_key not in self._registered_roles:
            self.logger.error(__name__, "Role '{}' was not found, returning default role's db source.".format(role_key))
            role_key = self._default_role

        return self._registered_roles[role_key][ROLE_DB_SOURCE] if ROLE_DB_SOURCE in self._registered_roles[role_key] else None