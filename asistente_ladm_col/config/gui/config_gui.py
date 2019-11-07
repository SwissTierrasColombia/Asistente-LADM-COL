from copy import deepcopy

from qgis.PyQt.QtCore import (QCoreApplication,
                              QObject)
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import (QMenu,
                                 QPushButton,
                                 QToolBar)

from asistente_ladm_col.config.general_config import *

DEFAULT_GUI = 'DEFAULT_GUI'
TEMPLATE_GUI = 'TEMPLATE_GUI'

OBJECT_NAME = 'object_name'
ICON = 'icon'
ACTIONS = 'actions'
MAIN_MENU = 'main_menu'
WIDGET_NAME = 'widget_name'
MENU = 'menu'
TOOLBAR = 'toolbar'
WIDGET_TYPE = 'widget_type'
SEPARATOR = 'separator'
NO_MENU = 'no_menu'
OPERATION_MENU = 'operation_menu'
SUPPLIES_MENU = 'supplies_menu'

ROLE_ACTIONS = 'role_actions'
ROLE_NAME = 'role_name'
ROLE_DESCRIPTION = 'role_description'
ROLE_GUI_CONFIG = 'role_gui_config'
BASIC_ROLE = 'BASIC_role'
OPERATOR_ROLE = 'operator_role'
MANAGER_ROLE = 'manager_role'
ADVANCED_ROLE = 'advanced_role'
ADMINISTRATOR_ROLE = 'administrator_role'
ALL_ROLES = 'all_roles'
ACTION_SETTINGS = 'action_settings'
ACTION_HELP = 'action_help'
ACTION_ABOUT = 'action_about'

ACTION_FINALIZE_GEOMETRY_CREATION = 'action_finalize_geometry_creation'
ACTION_BUILD_BOUNDARY = 'action_build_boundary'
ACTION_MOVE_NODES = 'action_move_nodes'
ACTION_FILL_BFS = 'action_fill_bfs'
ACTION_FILL_MORE_BFS_AND_LESS = 'action_fill_more_bfs_and_less'
ACTION_FILL_RIGHT_OF_WAY_RELATIONS = 'action_fill_right_of_way_relations'
ACTION_IMPORT_FROM_INTERMEDIATE_STRUCTURE = 'action_import_from_intermediate_structure'

ACTION_RUN_ETL_COBOL = 'action_run_etl_cobol'
ACTION_RUN_ETL_SNC = 'action_run_etl_snc'
ACTION_INTEGRATE_SUPPLIES = 'action_integrate_supplies'

ACTION_CHECK_QUALITY_RULES = 'action_check_quality_rules'
ACTION_PARCEL_QUERY = 'action_parcel_query'
ACTION_CREATE_BOUNDARY = 'action_create_boundary'
ACTION_CREATE_POINT = 'action_create_point'
ACTION_CREATE_PLOT = 'action_create_plot'
ACTION_CREATE_BUILDING = 'action_create_building'
ACTION_CREATE_BUILDING_UNIT = 'action_create_building_unit'
ACTION_CREATE_RIGHT_OF_WAY = 'action_create_right_of_way'
ACTION_CREATE_EXT_ADDRESS = 'action_create_ext_address'
ACTION_CREATE_PARCEL = 'action_create_parcel'
ACTION_CREATE_PARTY = 'action_create_party'
ACTION_CREATE_GROUP_PARTY = 'action_create_group_party'
ACTION_CREATE_RIGHT = 'action_create_right'
ACTION_CREATE_RESTRICTION = 'action_create_restriction'
ACTION_CREATE_ADMINISTRATIVE_SOURCE = 'action_create_administrative_source'
ACTION_CREATE_SPATIAL_SOURCE = 'action_create_spatial_source'
ACTION_UPLOAD_PENDING_SOURCE = 'action_upload_pending_source'
ACTION_SCHEMA_IMPORT = 'action_schema_import'
ACTION_IMPORT_DATA = 'action_import_data'
ACTION_EXPORT_DATA = 'action_export_data'
ACTION_LOAD_LAYERS = 'action_load_layers'
ACTION_REPORT_ANNEX_17 = 'action_report_annex_17'
ACTION_REPORT_ANT = 'action_report_ant'
ACTION_CHANGE_DETECTION_PER_PARCEL = 'action_change_detection_per_parcel'
ACTION_CHANGE_DETECTION_ALL_PARCELS = 'action_change_detection_all_parcels'
ACTION_OFFICIAL_SETTINGS = 'action_official_settings'

SURVEYING_ICON = ":/Asistente-LADM_COL/resources/images/surveying.png"
DATA_MANAGEMENT_ICON = ":/Asistente-LADM_COL/resources/images/create_db.png"
OPERATION_ICON = ""
SUPPLIES_ICON = ""
SPATIAL_UNIT_ICON = ":/Asistente-LADM_COL/resources/images/spatial_unit.png"
BA_UNIT_ICON = ":/Asistente-LADM_COL/resources/images/ba_unit.png"
RRR_ICON = ":/Asistente-LADM_COL/resources/images/rrr.png"
PARTY_ICON = ":/Asistente-LADM_COL/resources/images/party.png"
SOURCE_ICON = ":/Asistente-LADM_COL/resources/images/source.png"
REPORTS_ICON = ":/Asistente-LADM_COL/resources/images/domains.png"
CHANGE_DETECTION_ICON = ":/Asistente-LADM_COL/resources/images/surveying.png"

MODELS_GUI_DICT = {
    OPERATION_MODEL_PREFIX: [
        ACTION_CHECK_QUALITY_RULES
    ],
    CADASTRAL_FORM_MODEL_PREFIX: [
    ],
    VALUATION_MODEL_PREFIX: [
    ],
    SUPPLIES_MODEL_PREFIX: [
        ACTION_RUN_ETL_COBOL,
        ACTION_RUN_ETL_SNC
    ]
}


from ...resources import *

__ALL_ACTIONS__ = 'all_actions'

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
                    ACTIONS: []
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
                ACTION_LOAD_LAYERS,
                {
                    WIDGET_TYPE: MENU,
                    WIDGET_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Data Management"),
                    OBJECT_NAME: "ladm_col_data_management_menu",
                    ICON: DATA_MANAGEMENT_ICON,
                    ACTIONS: [
                        ACTION_SCHEMA_IMPORT,
                        ACTION_IMPORT_DATA,
                        ACTION_EXPORT_DATA
                    ]
                },
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
                ACTION_FILL_RIGHT_OF_WAY_RELATIONS,
                {
                    WIDGET_TYPE: MENU,
                    WIDGET_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create LADM objects"),
                    OBJECT_NAME: "edit_tools",
                    ACTIONS: [
                        ACTION_CREATE_POINT,
                        ACTION_CREATE_BOUNDARY,
                        SEPARATOR,
                        ACTION_CREATE_PLOT,
                        ACTION_CREATE_BUILDING,
                        ACTION_CREATE_BUILDING_UNIT,
                        ACTION_CREATE_RIGHT_OF_WAY,
                        ACTION_CREATE_EXT_ADDRESS,
                        SEPARATOR,
                        ACTION_CREATE_PARCEL,
                        SEPARATOR,
                        ACTION_CREATE_RIGHT,
                        ACTION_CREATE_RESTRICTION,
                        SEPARATOR,
                        ACTION_CREATE_PARTY,
                        ACTION_CREATE_GROUP_PARTY,
                        SEPARATOR,
                        ACTION_CREATE_ADMINISTRATIVE_SOURCE,
                        ACTION_CREATE_SPATIAL_SOURCE,
                        ACTION_UPLOAD_PENDING_SOURCE
                    ]
                },
                ACTION_IMPORT_FROM_INTERMEDIATE_STRUCTURE
            ]
        }]
    }

    def __init__(self):
        QObject.__init__(self)

    def get_gui_dict(self, name):
        return deepcopy(getattr(self, "{}_CONFIG_DICT".format(name), self.DEFAULT_GUI_CONFIG_DICT))


class GUI_Builder():
    """
    Build plugin GUI according to actors and LADM_COL models present in the current db connection
    """
    def __init__(self, iface):
        self.iface = iface
        self._registered_actions = dict()

        self.menus = list()
        self.toolbar_menus = list()
        self.toolbars = list()

    def register_action(self, key, action):
        self._registered_actions[key] = action

    def register_actions(self, dict_key_action):
        self._registered_actions.update(dict_key_action)

    def build_gui(self, db, test_conn_result, role_key):
        """
        Build the plugin gui according to configurations.
        We first check if the DB is LADM, if not, we use a default gui configuration. Otherwise we ask the role_key for
        a gui configuration. If he/she has it, we use it, otherwise we use a template gui configuration.

        :param db: DBConnector object
        :param test_conn_result: Can be True or False if test_connection was called, or None if we should call it now.
        :param role_key: Role key for whom the GUI will be built.
        :return:
        """
        print("Before unload")
        self.unload_gui(final_unload=False)  # First clear everything
        print("After unload")

        # Filter menus and actions and get a gui_config with the proper structure ready to build the GUI (e.g., with no
        # empty Menus)
        gui_config = self._get_filtered_gui_config(db, test_conn_result, role_key)
        print("After get filtered gui config")

        for component, values in gui_config.items():
            if component == MAIN_MENU:
                for menu_def in values:
                    menu = self._build_menu(menu_def)
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

    def _get_filtered_gui_config(self, db, test_conn_result, role_key):
        """
        Rebuilds a gui_config dict removing not allowed actions.

        :param db: DB Connector
        :param test_conn_result: True if the DB is LADM; False if not; None if test_connection has not been called yet.
                                 This is mainly to avoid recalling test_connection if we already know its result.
        :param role_key: Role key for whom the GUI will be built. Normally, it should be the active role.
        :return: Dictionary in the form of a gui_config dict, but with only allowed actions for the role_key passed.
        """
        gui_config = self._get_gui_config(db, test_conn_result, role_key)
        print("gui config dict:", gui_config)
        role_actions = self._get_role_actions(role_key)
        model_actions = self._get_model_actions(db)

        # Here we define how to deal with actions, role permissions and models present
        # We decided to prefer always the rol's actions. Like this:
        # R  M   Res
        # V  V    V
        # V  F    V
        # F  V    F
        # F  F    F
        allowed_actions = role_actions  # It's safe to make use of this list, no need to copy it, as it is a sum of lists
        print("Allowed actions for role {}".format(role_key), allowed_actions)

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
                if (item in allowed_actions or __ALL_ACTIONS__ in allowed_actions) and item in self._registered_actions:
                    # The action must be registered, otherwise we don't continue
                    # If the action is registeres, we check if the action is allowed, either by finding __ALL_ACTIONS__
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
        :param role_key: Active role key to whome we will ask for its GUI config. Normally, it should be the active one.
        :return: Dictionary in the form of a gui_config dict (still unfiltered).
        """
        gui_type = DEFAULT_GUI  # If test_connection is False, we use a default gui config
        if test_conn_result is None:
            test_conn_result = db.test_connection()[0]

        if test_conn_result:
            gui_config = Role_Registry().get_role_gui_config(role_key)
            if gui_config:
                print("GUI CONFIG ROLE")
                return gui_config  # We'll use the dict specified for the role
            else:
                gui_type = TEMPLATE_GUI  # If the role has not a gui_dict, we use a template.

        print("GUI CONFIG: {}".format(gui_type))

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
            actions.extend(MODELS_GUI_DICT[OPERATION_MODEL_PREFIX])
        if db.cadastral_form_model_exists():
            actions.extend(MODELS_GUI_DICT[CADASTRAL_FORM_MODEL_PREFIX])
        if db.valuation_model_exists():
            actions.extend(MODELS_GUI_DICT[VALUATION_MODEL_PREFIX])

        return list(set(actions))

    def unload_gui(self, final_unload=True):
        """
        Destroys the GUI (Menus and toolbars)

        :param final_unload: True if the plugin is closing. False if we just destroy the GUI to rebuild it once more.
        """
        if final_unload:
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

    def _build_menu(self, menu_def):
        menu = self.iface.mainWindow().findChild(QMenu, menu_def[OBJECT_NAME])
        print("build_menu:",menu is None, menu_def[WIDGET_NAME])
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
                menu.setIcon(QIcon(menu_def[ICON]))
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


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


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
                ACTION_INTEGRATE_SUPPLIES
            ],
            ROLE_GUI_CONFIG: {}
        }
        self.register_role(role, role_dict)

        role = ADVANCED_ROLE
        role_dict = {
            ROLE_NAME: QCoreApplication.translate("AsistenteLADMCOLPlugin", "Avanzado"),
            ROLE_DESCRIPTION: QCoreApplication.translate("AsistenteLADMCOLPlugin",
                                                         "The advanced role has access to all the functionality."),
            ROLE_ACTIONS: [__ALL_ACTIONS__],
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
                            ACTION_FILL_RIGHT_OF_WAY_RELATIONS,
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
            print("Role '{}' is not defined correctly and could not be registered! Check the role_dict.".format(role_key))  # TODO: Al logger

        return valid

    def get_active_role(self):
        return QSettings().value("Asistente-LADM_COL/roles/current_role_key", self._default_role)

    def set_active_role(self, role_key):
        res = False
        if role_key in self._registered_roles[role_key]:
            res = True
        else:
            print("Role '{}' was not found, returning default role's decription.".format(role_key))  # TODO: Al logger
            role_key = self._default_role

        QSettings().setValue("Asistente-LADM_COL/roles/current_role_key", role_key)

        return res

    def get_roles_info(self):
        return {k: v[ROLE_NAME] for k,v in self._registered_roles.items()}

    def get_role_description(self, role_key):
        if role_key not in self._registered_roles:
            print("Role '{}' was not found, returning default role's decription".format(role_key))  # TODO: Al logger
            role_key = self._default_role

        return self._registered_roles[role_key][ROLE_DESCRIPTION]

    def get_role_actions(self, role_key):
        if role_key not in self._registered_roles:
            print("Role '{}' was not found, returning default role's actions.".format(role_key))  # TODO: Al logger
            role_key = self._default_role

        return list(set(self._registered_roles[role_key][ROLE_ACTIONS] + self.COMMON_ACTIONS))

    def get_role_gui_config(self, role_key):
        if role_key not in self._registered_roles:
            print("Role '{}' was not found, returning default role's GUI configuration.".format(role_key))  # TODO: Al logger
            role_key = self._default_role

        return self._registered_roles[role_key][ROLE_GUI_CONFIG]
