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
from qgis.PyQt.QtCore import (QCoreApplication,
                              QObject)
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import (QMenu,
                                 QPushButton,
                                 QToolBar)

from asistente_ladm_col.config.config_db_supported import ConfigDbSupported
from asistente_ladm_col.config.gui.common_keys import *
from asistente_ladm_col.config.gui.gui_config import GUI_Config
from asistente_ladm_col.gui.gui_builder.role_registry import Role_Registry
from asistente_ladm_col.lib.logger import Logger


class GUI_Builder(QObject):
    """
    Build plugin GUI according to roles and LADM_COL models present in the current db connection
    """
    def __init__(self, iface):
        QObject.__init__(self)
        self.iface = iface
        self.logger = Logger()
        self._registered_actions = dict()

        self.menus = list()
        self.toolbar_menus = list()
        self.toolbars = list()

        # When building the GUI we rely on info from the DB connection
        self._db = None
        self._test_conn_result = None
        self._db_engine_actions = list()
        self._engine_name = ""

    def register_action(self, key, action):
        self._registered_actions[key] = {ACTION: action,
                                         DEFAULT_ACTION_TEXT: action.text(),
                                         DEFAULT_ACTION_STATUS: action.isEnabled()}

    def register_actions(self, dict_key_action):
        new_dict = dict()
        for k,v in dict_key_action.items():
            new_dict[k] = {ACTION: v,
                           DEFAULT_ACTION_TEXT: v.text(),
                           DEFAULT_ACTION_STATUS: v.isEnabled()}

        self._registered_actions.update(new_dict)

    def get_action(self, action_key):
        return self._get_and_configure_action(action_key)

    def set_db_connection(self, db, test_conn_result=None):
        """
        Set the DB connection info this class will use to build the GUI.

        :param db: DBConnector object
        :param test_conn_result: Can be True or False if test_connection was called, or None if we should call it.
        :return:
        """
        self._db = db
        self._test_conn_result = test_conn_result if test_conn_result is not None else db.test_connection()[0]
        db_factory = ConfigDbSupported().get_db_factory(db.engine)
        self._db_engine_actions = db_factory.get_db_engine_actions()
        self._engine_name = db_factory.get_name()

    def build_gui(self):
        """
        Build the plugin gui according to configurations.
        We first check if the DB is LADM, if not, we use a default gui configuration. Otherwise we ask the role_key for
        a gui configuration. If he/she has it, we use it, otherwise we use a template gui configuration.
        """
        if self._db is None or self._test_conn_result is None:
            self.logger.warning(__name__, QCoreApplication.translate("AsistenteLADMCOLPlugin",
                                                                     "You should first set the db connection in the GUI_Builder to build the GUI!"))
            return

        self.unload_gui(final_unload=False)  # First clear everything

        # Filter menus and actions and get a gui_config with the proper structure ready to build the GUI (e.g., with no
        # empty Menus)
        gui_config = self._get_filtered_gui_config()

        for component, values in gui_config.items():
            if component == MAIN_MENU:
                for menu_def in values:
                    menu = self._build_menu(menu_def)

                    # Try to add the menu in the second to last position of the QGIS menus
                    existent_actions = self.iface.mainWindow().menuBar().actions()
                    if len(existent_actions) > 0:
                        last_action = existent_actions[-1]
                        self.iface.mainWindow().menuBar().insertMenu(last_action, menu)
                    else:
                        self.iface.mainWindow().menuBar().addMenu(menu)
                    self.menus.append(menu)
            elif component == TOOLBAR:
                for toolbar_def in values:  # We expect a list of dicts here...
                    toolbar = self._build_toolbar(toolbar_def)

                    self.toolbars.append(toolbar)

    def _get_filtered_gui_config(self):
        """
        Rebuilds a gui_config dict removing not allowed actions.

        :return: Dictionary in the form of a gui_config dict, but only with allowed actions for the role_key passed.
        """
        role_key = Role_Registry().get_active_role()
        self.logger.info(__name__, "Active role: {}".format(Role_Registry().get_role_name(role_key)))

        gui_config = self._get_gui_config(role_key)
        # self.logger.debug(__name__, "Filtered gui_config: {}".format(gui_config))
        role_actions = self._get_role_actions(role_key)
        model_actions = self._get_model_actions() if self._test_conn_result else list()

        # If you want to take models into account, combine role_actions and model_actions as you like, and store the
        # result in allowed_actions.
        #
        # Here we define how to deal with actions, role permissions and models present
        # We decided to prefer always the rol's actions. Like this (R: Role, M: Model, Res: Result):
        # R  M   Res
        # V  V    V
        # V  F    V
        # F  V    F
        # F  F    F
        #
        # Therefore:
        allowed_actions = role_actions  # It's safe to make use of this list, no need to copy it, as it's a sum of lists
        self.logger.debug(__name__, "Allowed actions for role '{}': {}".format(role_key, allowed_actions))

        # Now, use only allowed actions and remove other actions from gui_config
        filtered_gui_config = dict()
        for k,v in gui_config.items():
            if k == MAIN_MENU or k == TOOLBAR:
                for menu_def in v:
                    actions = self._get_filtered_actions(menu_def[ACTIONS], allowed_actions)
                    if actions:
                        menu_def[ACTIONS] = actions
                        if not k in filtered_gui_config:
                            filtered_gui_config[k] = [menu_def]
                        else:
                            filtered_gui_config[k].append(menu_def)

        return filtered_gui_config

    def _get_filtered_actions(self, action_list, allowed_actions):
        """
        Filters out not allowed actions from an action list. It removes menus if no actions are allowed inside that
        menu, and it also removes separators if they are in a wrong position (e.e., two consecutive separators, a
        trailing separator, etc.)

        :param action_list: List of all actions defined in a gui_config dict.
        :param allowed_actions: List of allowed actions. Actions that are not here are not returned by this function.
        :return: List of actions with actions not allowed removed.
        """
        filtered_actions = list()
        for item in action_list:
            if type(item) is dict: # Menu
                menu_actions = self._get_filtered_actions(item[ACTIONS], allowed_actions)
                if [menu_action for menu_action in menu_actions if menu_action != SEPARATOR]:
                    item[ACTIONS] = menu_actions
                    filtered_actions.append(item)
            elif item == SEPARATOR:
                if filtered_actions and filtered_actions[-1] != SEPARATOR:
                    filtered_actions.append(SEPARATOR)
            else:  # Action
                if (item in allowed_actions or ALL_ACTIONS in allowed_actions) and item in self._registered_actions:
                    # The action must be registered, otherwise we don't continue
                    # If the action is registered, we check if the action is allowed, either by finding ALL_ACTIONS
                    # or by finding the action in the allowed actions list
                    filtered_actions.append(item)

        self._remove_trailing_separators(filtered_actions)

        return filtered_actions

    def _remove_trailing_separators(self, action_list):
        """
        Remove unnecessary trailing separators, both in menus and in the current action_list. Modifies the input list.

        :param action_list: list of actions, separators and other widgets
        """
        for item in action_list[:]:
            if type(item) is dict:
                # We don't expect empty ACTION lists, so it should be safe a [-1]
                if item[ACTIONS][-1] == SEPARATOR:
                    del item[ACTIONS][-1]

        if action_list and action_list[-1] == SEPARATOR:
            del action_list[-1]

    def _get_gui_config(self, role_key):
        """
        Get a basic GUI config (still unfiltered).

        :param role_key: Active role key to whom we will ask for its GUI config. Normally, it should be the active one.
        :return: Dictionary in the form of a gui_config dict (still unfiltered).
        """
        gui_type = DEFAULT_GUI  # If test_connection is False, we use a default gui config

        if self._test_conn_result:
            gui_config = Role_Registry().get_role_gui_config(role_key)
            if gui_config:
                self.logger.info(__name__, "Using gui_config from the role.")
                return gui_config
            else:
                self.logger.info(__name__, "Using gui_config from the template.")
                gui_type = TEMPLATE_GUI

        if gui_type == DEFAULT_GUI:
            self.logger.info(__name__, "Using gui_config from the default GUI (minimal).")

        return GUI_Config().get_gui_dict(gui_type)

    def _get_role_actions(self, role_key):
        """
        Get actions a given role has access to.

        :param role_key: Role key.
        :return: List of actions a role has access to.
        """
        return Role_Registry().get_role_actions(role_key)

    def _get_model_actions(self):
        """
        Gets a list of actions that models in the DB enable. E.g., if we have valuation model, we add to this list
        valuation actions, otherwise we don't.

        :return: List of actions without duplicate elements.
        """
        actions = list()
        if self._db.operation_model_exists():
            actions.extend(MODELS_GUI_DICT[LADMNames.OPERATION_MODEL_PREFIX])
        if self._db.cadastral_form_model_exists():
            actions.extend(MODELS_GUI_DICT[LADMNames.CADASTRAL_FORM_MODEL_PREFIX])
        if self._db.valuation_model_exists():
            actions.extend(MODELS_GUI_DICT[LADMNames.VALUATION_MODEL_PREFIX])

        return list(set(actions))

    def unload_gui(self, final_unload=True):
        """
        Destroys the GUI (Menus and toolbars)

        :param final_unload: True if the plugin is closing. False if we just destroy the GUI to rebuild it once more.
        """
        if final_unload:
            self.logger.info(__name__, "Unloading completely the GUI (final_unload)")
            for action_info in self._registered_actions.values():
                del action_info[ACTION]
            self._registered_actions = dict()

        for menu in self.menus:
            menu.clear()
            menu.deleteLater()

        for menu in self.toolbar_menus:  # Basically, a push button who has been received a menu
            menu.deleteLater()

        for toolbar in self.toolbars:
            self.iface.mainWindow().removeToolBar(toolbar)
            del toolbar

        self.menus = list()
        self.toolbar_menus = list()
        self.toolbars = list()

        self.logger.info(__name__, "GUI unloaded (not a final_unload)")

    def _build_menu(self, menu_def):
        menu = self.iface.mainWindow().findChild(QMenu, menu_def[OBJECT_NAME])
        if menu is None:
            menu = QMenu(menu_def[WIDGET_NAME], self.iface.mainWindow().menuBar())
            if ICON in menu_def:
                menu.setIcon(QIcon(menu_def[ICON]))
            menu.setObjectName(menu_def[OBJECT_NAME])

        self._build_actions(menu_def[ACTIONS], menu)

        return menu

    def _build_toolbar_menu(self, menu_def):
        # Menus for toolbars are created differently...
        widget = self.iface.mainWindow().findChild(QPushButton, menu_def[OBJECT_NAME])
        if widget is None:
            widget = QPushButton(menu_def[WIDGET_NAME])
            menu = QMenu()
            if ICON in menu_def:
                widget.setIcon(QIcon(menu_def[ICON]))
            widget.setMenu(menu)

        self._build_actions(menu_def[ACTIONS], menu)  # Now we have a normal menu, build actions on it

        return widget

    def _build_toolbar(self, toolbar_def):
        toolbar = self.iface.mainWindow().findChild(QToolBar, toolbar_def[OBJECT_NAME])
        if toolbar is None:
            toolbar = self.iface.addToolBar(QCoreApplication.translate("AsistenteLADMCOLPlugin", toolbar_def[WIDGET_NAME]))
            toolbar.setObjectName(toolbar_def[OBJECT_NAME])
            toolbar.setToolTip(toolbar_def[WIDGET_NAME])

        self._build_toolbar_actions(toolbar_def[ACTIONS], toolbar)

        return toolbar

    def _build_actions(self, actions_list, base_menu):
        for item in actions_list:
            if type(item) is dict:  # Menu
                menu = self._build_menu(item)
                base_menu.addMenu(menu)
                self.menus.append(menu)
            elif item == SEPARATOR:
                base_menu.addSeparator()
            else:  # Action
                if item in self._registered_actions:
                    base_menu.addAction(self._get_and_configure_action(item))

    def _build_toolbar_actions(self, actions_list, toolbar):
        for item in actions_list:
            if type(item) is dict:  # Menu
                widget = self._build_toolbar_menu(item)
                toolbar.addWidget(widget)
                self.toolbar_menus.append(widget)
            elif item == SEPARATOR:
                toolbar.addSeparator()
            else:  # Action
                if item in self._registered_actions:
                    toolbar.addAction(self._get_and_configure_action(item))

    def _get_and_configure_action(self, action_key):
        """
        Get and configure actions. Configuration means to enable/disable them, and set text and tooltip, among others.

        :param action_key:
        :return:
        """
        action = self._registered_actions[action_key][ACTION] if action_key in self._registered_actions else None
        if action is None:
            return action

        # Default properties
        action_text = self._registered_actions[action_key][DEFAULT_ACTION_TEXT]
        action.setEnabled(self._registered_actions[action_key][DEFAULT_ACTION_STATUS])
        action.setText(action_text)
        action.setToolTip(action_text)

        # If not supported by current DB engine...
        if not ALL_ACTIONS in self._db_engine_actions and not action_key in self._db_engine_actions:
            action.setEnabled(False)
            action.setText(QCoreApplication.translate("AsistenteLADMCOLPlugin", "{} (not for {})").format(action_text,
                                                                                                          self._engine_name))
            action.setToolTip(QCoreApplication.translate("AsistenteLADMCOLPlugin",
                                                         "Not supported by {}".format(self._engine_name)))

        return action

    def show_welcome_screen(self):
        return not Role_Registry().active_role_already_set()