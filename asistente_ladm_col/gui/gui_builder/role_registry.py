"""
/***************************************************************************
                              Asistente LADM-COL
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
from asistente_ladm_col.config.keys.common import *
from asistente_ladm_col.config.role_config import get_role_config
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

        # Register default roles
        for role_key, role_config in get_role_config().items():
            if ROLE_ENABLED in role_config and role_config[ROLE_ENABLED]:
                self.register_role(role_key, role_config)

    def register_role(self, role_key, role_dict, activate_role=False):
        """
        Register roles for the LADM-COL assistant. Roles have access only to certain GUI controls, to
        certain LADM-COL models and to certain quality rules.

        Warning: this class will modify the role_dict, so better pass a deepcopy of the configuration dict.

        :param role_key: Role unique identifier
        :param role_dict: Dictionary with the following information:
                ROLE_NAME: Name of the role
                ROLE_DESCRIPTION: Explains what this role is about
                ROLE_ENABLED: Whether this role is enabled or not
                ROLE_ACTIONS: List of actions a role has access to
                ROLE_MODELS: List of models and their configuration for the current role
                ROLE_QUALITY_RULES: List of quality rule keys this role has access to
                ROLE_GUI_CONFIG: Dict with the GUI config (menus and toolbars)
        :return: Whether the role was successfully registered or not.
        """
        valid = False
        if ROLE_NAME in role_dict and ROLE_DESCRIPTION in role_dict and ROLE_ACTIONS in role_dict and \
                ROLE_GUI_CONFIG in role_dict and TEMPLATE_GUI in role_dict[ROLE_GUI_CONFIG] \
                and ROLE_MODELS in role_dict:
            if role_dict[ROLE_GUI_CONFIG]:  # It's mandatory to provide a GUI config for the role
                self._registered_roles[role_key] = role_dict
                valid = True
            else:
                self.logger.error(__name__,
                                  "Role '{}' has no GUI config and could not be registered!".format(role_key))
        else:
            self.logger.error(__name__, "Role '{}' is not defined correctly and could not be registered! Check the role_dict parameter.".format(role_key))

        if activate_role:
            self.set_active_role(role_key)

        return valid

    def unregister_role(self, role_key):
        res = False
        if role_key in self._registered_roles:
            # You cannot unregister the default role
            if role_key != self._default_role:
                # First change active role to default if role_key is active
                if role_key == self.get_active_role():
                    self.set_active_role(self._default_role)

                # Then unregister the role
                self._registered_roles[role_key] = None
                del self._registered_roles[role_key]
                res = False
            else:
                self.logger.warning(__name__, "You cannot unregister the default role!")
        else:
            self.logger.warning(__name__,
                                "The role ('{}') you're trying to unregister is not registered!".format(role_key))

        return res

    def get_active_role(self):
        # We make sure the active role we return is in fact registered.
        # Otherwise, we set the default role as active.
        active_role = self.app.settings.active_role
        if not active_role in self._registered_roles:
            self.set_active_role(self._default_role)

        return self.app.settings.active_role

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

    def get_role_gui_config(self, role_key, gui_type=TEMPLATE_GUI):
        """
        Return the role GUI config.

        :param role_key: Role id.
        :param gui_type: Either TEMPLATE_GUI or DEFAULT_GUI (the one for wrong db connections).
        :return: Dict with the GUI config for the role.
        """
        if role_key not in self._registered_roles:
            self.logger.error(__name__, "Role '{}' was not found, returning default role's GUI configuration.".format(role_key))
            role_key = self._default_role

        # Return a deepcopy, since we don't want external classes to modify a role's GUI config
        gui_conf = self._registered_roles[role_key][ROLE_GUI_CONFIG].get(gui_type, dict())
        return deepcopy(gui_conf)  # The plugin knows what to do if the role has no DEFAULT_GUI

    def get_role_models(self, role_key):
        """
        Normally you wouldn't need this but LADMColModelRegistry, which is anyway updated when the role changes.
        """
        if role_key not in self._registered_roles:
            self.logger.error(__name__, "Role '{}' was not found, returning default role's models.".format(role_key))
            role_key = self._default_role

        return self._registered_roles[role_key][ROLE_MODELS]

    def get_active_role_supported_models(self):
        return self.get_role_supported_models(self.get_active_role())

    def get_role_supported_models(self, role_key):
        return self.get_role_models(role_key)[ROLE_SUPPORTED_MODELS]

    def active_role_needs_automatic_expression_for_baskets(self):
        return self._registered_roles[self.get_active_role()].get(ROLE_NEEDS_AUTOMATIC_VALUE_FOR_BASKETS, False)

    def get_role_quality_rules(self, role_key):
        if role_key not in self._registered_roles:
            self.logger.error(__name__, "Role '{}' was not found, returning default role's quality rules.".format(role_key))
            role_key = self._default_role

        return self._registered_roles[role_key][ROLE_QUALITY_RULES]

    def get_role_db_source(self, role_key):
        if role_key not in self._registered_roles:
            self.logger.error(__name__, "Role '{}' was not found, returning default role's db source.".format(role_key))
            role_key = self._default_role

        return self._registered_roles[role_key].get(ROLE_DB_SOURCE, None)

    def add_actions_to_roles(self, action_keys, role_keys=None):
        """
        For add-ons that want to modify actions of already registered roles.

        This first adds each action_key to allowed role actions, and then it
        adds each action key to the menu Add-ons that is empty by default in
        the template GUI Config.

        After calling this method, it is necessary to call gui_builder.build_gui()
        to refresh the GUI with these changes. Otherwise, the user won't see
        changes until build_gui() is called from the Asistente LADM-COL.

        :param action_keys: List of action keys.
        :param role_keys: List of role keys. This param is optional. If it's not passed, we'll use all registered roles.
        """
        if not role_keys:
            role_keys = list(self._registered_roles.keys())

        for role_key in role_keys:
            if role_key in self._registered_roles:
                self.__add_actions_to_allowed_role_actions(action_keys, role_key)
                self.__add_actions_to_role_add_on_menu(action_keys, role_key)
                self.logger.debug(__name__, "{} actions added to role '{}'!".format(len(action_keys), role_key))

    def __add_actions_to_allowed_role_actions(self, action_keys, role_key):
        # Add action keys to the list of allowed actions for a given role
        role_actions = self._registered_roles[role_key][ROLE_ACTIONS]
        self._registered_roles[role_key][ROLE_ACTIONS] = list(set(role_actions + action_keys))
        del role_actions

    def __add_actions_to_role_add_on_menu(self, action_keys, role_key):
        # Go for the Menu with object_name LADM_COL_ADD_ON_MENU and add the action keys
        gui_config = self._registered_roles[role_key][ROLE_GUI_CONFIG]
        for main_menu in gui_config.get(MAIN_MENU, dict()):  # Since MAIN_MENU is a list of menus
            for action in main_menu.get(ACTIONS, list()):
                if isinstance(action, dict):  # We know this is a menu
                    if action.get(OBJECT_NAME, "") == LADM_COL_ADD_ON_MENU:  # This is the Add-ons menu
                        action[ACTIONS] = list(set(action[ACTIONS] + action_keys))  # Add actions and avoid dup.
                        break  # Go to other menus, because in this one we are done!
