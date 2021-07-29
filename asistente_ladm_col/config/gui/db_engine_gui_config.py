from qgis.PyQt.QtCore import (QCoreApplication,
                              QObject)

from asistente_ladm_col.config.gui.common_keys import *
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.utils.singleton import SingletonQObject


class DBEngineGUIConfig(QObject, metaclass=SingletonQObject):
    """
    Action configuration for each DB engine.

    These lists might be modified by add-ons. We expect add-ons to add action
    keys to the lists and don't expect them to remove elements from the lists.
    Action keys might live in these lists even if an add-on is uninstalled.
    The add-on should unregister all its actions in gui_builder and that's enough.
    """
    __COMMON_ACTIONS = [ACTION_SETTINGS,
                      ACTION_HELP,
                      ACTION_ABOUT,
                      ACTION_DOWNLOAD_GUIDE,
                      ACTION_FINALIZE_GEOMETRY_CREATION,
                      ACTION_BUILD_BOUNDARY,
                      ACTION_MOVE_NODES,
                      ACTION_FILL_BFS,
                      ACTION_FILL_MORE_BFS_AND_LESS,
                      ACTION_FILL_RIGHT_OF_WAY_RELATIONS,
                      ACTION_IMPORT_FROM_INTERMEDIATE_STRUCTURE,
                      ACTION_ST_LOGIN,
                      ACTION_ST_LOGOUT,
                      ACTION_ST_UPLOAD_XTF,
                      ACTION_CREATE_BOUNDARY,
                      ACTION_CREATE_POINT,
                      ACTION_CREATE_PLOT,
                      ACTION_CREATE_BUILDING,
                      ACTION_CREATE_BUILDING_UNIT,
                      ACTION_CREATE_RIGHT_OF_WAY,
                      ACTION_CREATE_EXT_ADDRESS,
                      ACTION_CREATE_PARCEL,
                      ACTION_CREATE_PARTY,
                      ACTION_CREATE_GROUP_PARTY,
                      ACTION_CREATE_RIGHT,
                      ACTION_CREATE_RESTRICTION,
                      ACTION_CREATE_ADMINISTRATIVE_SOURCE,
                      ACTION_CREATE_SPATIAL_SOURCE,
                      ACTION_UPLOAD_PENDING_SOURCE,
                      ACTION_SCHEMA_IMPORT,
                      ACTION_IMPORT_DATA,
                      ACTION_EXPORT_DATA,
                      ACTION_LOAD_LAYERS,
                      ACTION_FIX_LADM_COL_RELATIONS,
                      ACTION_CHANGE_DETECTION_PER_PARCEL,
                      ACTION_CHANGE_DETECTION_ALL_PARCELS,
                      ACTION_PARCEL_QUERY,
                      # ACTION_REPORT_ANNEX_17,
                      # ACTION_REPORT_ANT,
                      ACTION_CHANGE_DETECTION_SETTINGS,
                      ACTION_CHECK_QUALITY_RULES,
                      ACTION_ALLOCATE_PARCELS_FIELD_DATA_CAPTURE,
                      ACTION_SYNCHRONIZE_FIELD_DATA]

    __GPKG_ACTIONS = __COMMON_ACTIONS + [ACTION_RUN_ETL_SUPPLIES,
                                         ACTION_FIND_MISSING_COBOL_SUPPLIES,
                                         ACTION_FIND_MISSING_SNC_SUPPLIES,
                                         ACTION_INTEGRATE_SUPPLIES]

    __PG_ACTIONS = [ALL_ACTIONS]

    __MSSQL_ACTIONS = __COMMON_ACTIONS

    def __init__(self):
        QObject.__init__(self)
        self.logger = Logger()

    def add_actions_to_db_engines(self, action_key_list, db_engine_key_list):
        """
        For add-ons that want to modify actions of supported DB engines.
        If a supported DB engine is missing in the list, the actions will
        be disabled for DB connections that correspond to such engine.

        Note: All actions should support at least PostgreSQL.

        :param action_key_list: List of action keys to add.
        :param db_engine_key_list: List of DB engines in which the action should work. Possible values: 'pg', 'gpkg',
                                   'myssql'.
        """
        for engine in db_engine_key_list:
            engine_actions = getattr(self, "_DBEngineGUIConfig__{}_ACTIONS".format(engine.upper()), None)
            if engine_actions:
                setattr(self, "_DBEngineGUIConfig__{}_ACTIONS".format(engine.upper()), list(set(engine_actions + action_key_list)))
                self.logger.debug(__name__, "{} actions added to DB engine '{}'!".format(len(action_key_list), engine))

    def get_db_engine_actions(self, engine):
        """
        Gets a GUI config dict for both Toolbars and Menus.

        :param name: Either TEMPLATE_GUI or DEFAULT_GUI (or more if GUI_Congif() has more dict keys)
        :return: A deep copy (i.e., it's safe to alter it) of the GUI config dictionary
        """
        return getattr(self, "_DBEngineGUIConfig__{}_ACTIONS".format(engine.upper()), self.__COMMON_ACTIONS)
