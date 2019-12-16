from asistente_ladm_col.config.table_mapping_config import (OPERATION_MODEL_PREFIX,
                                                            CADASTRAL_FORM_MODEL_PREFIX,
                                                            VALUATION_MODEL_PREFIX,
                                                            SUPPLIES_MODEL_PREFIX)



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
BASIC_ROLE = 'basic_role'
SUPPLIES_PROVIDER_ROLE = 'supplies_provider_role'
OPERATOR_ROLE = 'operator_role'
MANAGER_ROLE = 'manager_role'
ADVANCED_ROLE = 'advanced_role'
ADMINISTRATOR_ROLE = 'administrator_role'
ALL_ROLES = 'all_roles'
ACTION_SETTINGS = 'action_settings'
ACTION_HELP = 'action_help'
ACTION_ABOUT = 'action_about'

ACTION_DOWNLOAD_GUIDE = 'action_download_guide'
ACTION_FINALIZE_GEOMETRY_CREATION = 'action_finalize_geometry_creation'
ACTION_BUILD_BOUNDARY = 'action_build_boundary'
ACTION_MOVE_NODES = 'action_move_nodes'
ACTION_FILL_BFS = 'action_fill_bfs'
ACTION_FILL_MORE_BFS_AND_LESS = 'action_fill_more_bfs_and_less'
ACTION_FILL_RIGHT_OF_WAY_RELATIONS = 'action_fill_right_of_way_relations'
ACTION_IMPORT_FROM_INTERMEDIATE_STRUCTURE = 'action_import_from_intermediate_structure'

ACTION_RUN_ETL_COBOL = 'action_run_etl_cobol'
ACTION_RUN_ETL_SNC = 'action_run_etl_snc'
ACTION_FIND_MISSING_COBOL_SUPPLIES = 'action_find_missing_cobol_supplies'
ACTION_INTEGRATE_SUPPLIES = 'action_integrate_supplies'

ACTION_ST_LOGIN = 'action_st_login'
ACTION_ST_LOGOUT = 'action_st_logout'
ACTION_ST_UPLOAD_XTF = 'action_st_upload_xtf'

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
ACTION_SCHEMA_IMPORT_SUPPLIES = 'action_schema_import_supplies'
ACTION_IMPORT_DATA = 'action_import_data'
ACTION_IMPORT_DATA_SUPPLIES = 'action_import_data_supplies'
ACTION_EXPORT_DATA = 'action_export_data'
ACTION_EXPORT_DATA_SUPPLIES = 'action_export_data_supplies'
ACTION_LOAD_LAYERS = 'action_load_layers'
ACTION_REPORT_ANNEX_17 = 'action_report_annex_17'
ACTION_REPORT_ANT = 'action_report_ant'
ACTION_CHANGE_DETECTION_PER_PARCEL = 'action_change_detection_per_parcel'
ACTION_CHANGE_DETECTION_ALL_PARCELS = 'action_change_detection_all_parcels'
ACTION_SUPPLIES_SETTINGS = 'action_supplies_settings'

ALL_ACTIONS = 'all_actions'

SURVEYING_ICON = ":/Asistente-LADM_COL/resources/images/surveying.png"
DATA_MANAGEMENT_ICON = ":/Asistente-LADM_COL/resources/images/create_db.png"
DATA_CREATION_ICON = ":/Asistente-LADM_COL/resources/images/data_creation.svg"
ST_ICON = ":/Asistente-LADM_COL/resources/images/st.svg"
OPERATION_ICON = ":/Asistente-LADM_COL/resources/images/icon.png"
STRUCTURING_TOOLS_ICON = ":/Asistente-LADM_COL/resources/images/structuring_tools.svg"
SUPPLIES_ICON = ""
SPATIAL_UNIT_ICON = ":/Asistente-LADM_COL/resources/images/spatial_unit.png"
BA_UNIT_ICON = ":/Asistente-LADM_COL/resources/images/ba_unit.png"
RRR_ICON = ":/Asistente-LADM_COL/resources/images/rrr.png"
PARTY_ICON = ":/Asistente-LADM_COL/resources/images/party.png"
SOURCE_ICON = ":/Asistente-LADM_COL/resources/images/source.png"
REPORTS_ICON = ":/Asistente-LADM_COL/resources/images/reports.svg"
CHANGE_DETECTION_ICON = ":/Asistente-LADM_COL/resources/images/change_detection.svg"

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
        ACTION_RUN_ETL_SNC,
        ACTION_FIND_MISSING_COBOL_SUPPLIES
    ]
}
