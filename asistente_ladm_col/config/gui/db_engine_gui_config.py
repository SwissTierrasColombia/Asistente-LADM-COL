from qgis.PyQt.QtCore import (QCoreApplication,
                              QObject)

from asistente_ladm_col.config.gui.common_keys import *


class DBEngineGUIConfig(QObject):
    """
    Action configuration for each DB engine.
    """
    COMMON_ACTIONS = [ACTION_SETTINGS,
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
                      ACTION_XTF_MODEL_CONVERSION,
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

    GPKG_ACTIONS = COMMON_ACTIONS + [ACTION_RUN_ETL_SUPPLIES,
                                     ACTION_FIND_MISSING_COBOL_SUPPLIES,
                                     ACTION_FIND_MISSING_SNC_SUPPLIES,
                                     ACTION_INTEGRATE_SUPPLIES]

    PG_ACTIONS = [ALL_ACTIONS]

    MSSQL_ACTIONS = COMMON_ACTIONS

    def __init__(self):
        QObject.__init__(self)

    def get_db_engine_actions(self, engine):
        """
        Gets a GUI config dict for both Toolbars and Menus.

        :param name: Either TEMPLATE_GUI or DEFAULT_GUI (or more if GUI_Congif() has more dict keys)
        :return: A deep copy (i.e., it's safe to alter it) of the GUI config dictionary
        """
        return getattr(self, "{}_ACTIONS".format(engine.upper()), self.COMMON_ACTIONS)
