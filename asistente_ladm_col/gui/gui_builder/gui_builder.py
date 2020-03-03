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

from asistente_ladm_col.config.mapping_config import LADMNames
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

    def register_action(self, key, action):
        self._registered_actions[key] = action

    def register_actions(self, dict_key_action):
        self._registered_actions.update(dict_key_action)

    def get_action(self, action_tag):
        return self._registered_actions[action_tag] if action_tag in self._registered_actions else None

    def build_gui(self, db, test_conn_result):
        """
        Build the plugin gui according to configurations.
        We first check if the DB is LADM, if not, we use a default gui configuration. Otherwise we ask the role_key for
        a gui configuration. If he/she has it, we use it, otherwise we use a template gui configuration.

        :param db: DBConnector object
        :param test_conn_result: Can be True or False if test_connection was called, or None if we should call it now.
        :return:
        """
        self.unload_gui(final_unload=False)  # First clear everything

        # Filter menus and actions and get a gui_config with the proper structure ready to build the GUI (e.g., with no
        # empty Menus)
        gui_config = self._get_filtered_gui_config(db, test_conn_result)

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

    def _get_filtered_gui_config(self, db, test_conn_result):
        """
        Rebuilds a gui_config dict removing not allowed actions.

        :param db: DB Connector
        :param test_conn_result: True if the DB is LADM; False if not; None if test_connection has not been called yet.
                                 This is mainly to avoid recalling test_connection if we already know its result.
        :return: Dictionary in the form of a gui_config dict, but only with allowed actions for the role_key passed.
        """
        role_key = Role_Registry().get_active_role()
        self.logger.info(__name__, "Active role: {}".format(Role_Registry().get_role_name(role_key)))

        if test_conn_result is None:
            test_conn_result = db.test_connection()[0]

        gui_config = self._get_gui_config(db, test_conn_result, role_key)
        # self.logger.debug(__name__, "Filtered gui_config: {}".format(gui_config))
        role_actions = self._get_role_actions(role_key)
        model_actions = self._get_model_actions(db) if test_conn_result else list()

        # Here we define how to deal with actions, role permissions and models present
        # We decided to prefer always the rol's actions. Like this:
        # R  M   Res
        # V  V    V
        # V  F    V
        # F  V    F
        # F  F    F
        allowed_actions = role_actions  # It's safe to make use of this list, no need to copy it, as it is a sum of lists
        self.logger.debug(__name__, "Allowed actions for role '{}': {}".format(role_key, allowed_actions))

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
                    # If the action is registeres, we check if the action is allowed, either by finding ALL_ACTIONS
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

    def _get_gui_config(self, db, test_conn_result, role_key):
        """
        Get a basic GUI config (still unfiltered).

        :param db: DB Connector
        :param test_conn_result: True if the DB is LADM; False if not; None if test_connection has not been called yet.
                                 This is mainly to avoid recalling test_connection if we already know its result.
        :param role_key: Active role key to whom we will ask for its GUI config. Normally, it should be the active one.
        :return: Dictionary in the form of a gui_config dict (still unfiltered).
        """
        gui_type = DEFAULT_GUI  # If test_connection is False, we use a default gui config

        if test_conn_result:
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

    def _get_model_actions(self, db):
        """
        Gets a list of actions that models in the DB enable. E.g., if we have valuation model, we add to this list
        valuation actions, otherwise we don't.

        :param db: DB Connector object
        :return: List of actions without duplicate elements.
        """
        actions = list()
        if db.operation_model_exists():
            actions.extend(MODELS_GUI_DICT[LADMNames.OPERATION_MODEL_PREFIX])
        if db.cadastral_form_model_exists():
            actions.extend(MODELS_GUI_DICT[LADMNames.CADASTRAL_FORM_MODEL_PREFIX])
        if db.valuation_model_exists():
            actions.extend(MODELS_GUI_DICT[LADMNames.VALUATION_MODEL_PREFIX])

        return list(set(actions))

    def unload_gui(self, final_unload=True):
        """
        Destroys the GUI (Menus and toolbars)

        :param final_unload: True if the plugin is closing. False if we just destroy the GUI to rebuild it once more.
        """
        if final_unload:
            self.logger.info(__name__, "Unloading completely the GUI (final_unload)")
            for action in self._registered_actions.values():
                del action
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
                    base_menu.addAction(self._registered_actions[item])

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
                    toolbar.addAction(self._registered_actions[item])

    def show_welcome_screen(self):
        return not Role_Registry().active_role_already_set()