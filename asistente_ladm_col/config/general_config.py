import os.path

from qgis.PyQt.QtCore import (QSettings,
                              QObject,
                              Qt,
                              QCoreApplication)

from asistente_ladm_col.config.translator import PLUGIN_DIR
from asistente_ladm_col.config.table_mapping_config import Names
from asistente_ladm_col.config.enums import LogModeEnum
from asistente_ladm_col.utils.qt_utils import get_plugin_metadata

DEFAULT_LOG_MODE = LogModeEnum.USER
DEFAULT_LOG_FILE = ''

SUPPLIES_DB_PREFIX = None
SUPPLIES_DB_SUFFIX = " (Insumos)"
PREFIX_LAYER_MODIFIERS = 'prefix'
SUFFIX_LAYER_MODIFIERS = 'suffix'
STYLE_GROUP_LAYER_MODIFIERS = 'style_group'
VISIBLE_LAYER_MODIFIERS = 'visible'

TOOLBAR_BUILD_BOUNDARY = QCoreApplication.translate("TranslatableConfigStrings", "Build boundaries...")
TOOLBAR_MOVE_NODES = QCoreApplication.translate("TranslatableConfigStrings", "Move nodes...")
TOOLBAR_FILL_POINT_BFS = QCoreApplication.translate("TranslatableConfigStrings", "Fill Point BFS")
TOOLBAR_FILL_MORE_BFS_LESS = QCoreApplication.translate("TranslatableConfigStrings", "Fill More BFS and Less")
TOOLBAR_FILL_RIGHT_OF_WAY_RELATIONS = QCoreApplication.translate("TranslatableConfigStrings", "Fill Right of Way Relations")
TOOLBAR_IMPORT_FROM_INTERMEDIATE_STRUCTURE = QCoreApplication.translate("TranslatableConfigStrings", "Import from intermediate structure")
TOOLBAR_FINALIZE_GEOMETRY_CREATION = QCoreApplication.translate("TranslatableConfigStrings", "Finalize geometry creation")
ACTION_FINALIZE_GEOMETRY_CREATION_OBJECT_NAME = "finalize_geometry_creation"

# Constants for reports
NATIONAL_LAND_AGENCY = "ANT"
ANNEX_17_REPORT = "Anexo_17"
ANT_MAP_REPORT = "Plano_ANT"

# From this version on the plugin will work, a message will block prior versions
LATEST_OPERATION_MODEL_VERSION_SUPPORTED = "2.9.6"

DEFAULT_MODEL_NAMES_CHECKED = {
    'ANT_V2_9_6': Qt.Unchecked,
    'Avaluos_V2_9_6': Qt.Unchecked,
    'Cartografia_Referencia_V2_9_6': Qt.Unchecked,
    'Datos_Gestor_Catastral_V2_9_6': Qt.Unchecked,
    'Datos_Integracion_Insumos_V2_9_6': Qt.Unchecked,
    'Datos_SNR_V2_9_6': Qt.Unchecked,
    'Formulario_Catastro_V2_9_6': Qt.Unchecked,
    'Operacion_V2_9_6': Qt.Checked
}

DEFAULT_HIDDEN_MODELS = ['LADM_COL_V1_2', 'ISO19107_V1_MAGNABOG', 'ISO19107_PLANAS_V1']

DEFAULT_INHERITANCE ='smart2'
DEFAULT_EPSG =  "3116"
DEFAULT_TOO_LONG_BOUNDARY_SEGMENTS_TOLERANCE = 200 # meters
DEFAULT_USE_ROADS_VALUE = False
HELP_URL = "https://agenciaimplementacion.github.io/Asistente-LADM_COL"
FIELD_MAPPING_PATH = os.path.join(os.path.expanduser('~'), 'Asistente-LADM_COL', 'field_mappings')
MAXIMUM_FIELD_MAPPING_FILES_PER_TABLE = 10
PLUGIN_VERSION = get_plugin_metadata('asistente_ladm_col', 'version')
PLUGIN_NAME = get_plugin_metadata('asistente_ladm_col', 'name')
# PLUGIN_DIR (set in translator.py)
HELP_DIR_NAME = 'help'
STYLES_DIR = os.path.join(PLUGIN_DIR, 'resources', 'styles')
TOML_FILE_DIR = os.path.join(PLUGIN_DIR, 'resources', 'toml', 'hide_fields_LADM.toml')

# SISTEMA DE TRANSICIÓN
ST_LOGIN_SERVICE_URL = "http://apist.proadmintierra.info/api/security/oauth/token"
ST_LOGIN_SERVICE_PAYLOAD = "username={}&password={}&grant_type=password"
encoded = b'c3Qtd2ViLXNkVmExTlh3OmhLYmNlTjg5'
ST_LOGIN_AUTHORIZATION_CLIENT = "Basic {}".format(encoded.decode('utf-8'))

BLO_LIS_FILE_PATH = os.path.join(PLUGIN_DIR, 'resources', 'etl', 'blo.lis')  # Default Cobol BLO.lis file

# Settings to create schema according to LADM-COL
CREATE_BASKET_COL = False
CREATE_IMPORT_TID = False
STROKE_ARCS = True


LAYER = 'layer'  # Used as key that holds a QgsVectorLayer in dictionaries
TABLE_ILINAME = 'table_iliname'
TABLE_NAME = 'tablename'
FIELD_ILINAME = 'field_iliname'
FIELD_NAME = 'fieldname'

# SETTINGS DIALOG TAB INDEXES
SETTINGS_CONNECTION_TAB_INDEX = 0
SETTINGS_MODELS_TAB_INDEX = 1


# Version to be installed when creating reports (annex 17 - ANT Map)
# (Other versions, if found, will be dropped in favor of this one)
REPORTS_REQUIRED_VERSION = '0.6dev'
URL_REPORTS_LIBRARIES = 'https://github.com/AgenciaImplementacion/LADM_COL_Reports/releases/download/{}/impresion.zip'.format(REPORTS_REQUIRED_VERSION)

MODULE_HELP_MAPPING = {
    '' : 'index.html', # default module is '', just go to index.html
    'create_admin_source': 'operation/Source.html#administrative-source',
    'create_parcel': 'operation/Basic_Administrative_Unit.html#parcel',
    'create_points': 'operation/Surveying_and_Representation.html#create-point',
    'create_boundaries': 'operation/Surveying_and_Representation.html#create-boundary',
    'create_plot': 'operation/Spatial_Unit.html#create-plot',
    'create_building': 'operation/Spatial_Unit.html#create-building',
    'create_building_unit': 'operation/Spatial_Unit.html#create-building-unit',
    'create_right_of_way':'operation/Spatial_Unit.html#create-right-of-way',
    'associate_ext_address': 'operation/Spatial_Unit.html#associate-extaddress',
    'create_right': 'operation/RRR.html#right',
    'create_restriction': 'operation/RRR.html#restriction',
    'create_spatial_source': 'operation/Source.html#spatial-source',
    'load_layers': 'load_layers.html#load-layers',
    'col_party': 'operation/Party.html#col-party',
    'group_party': 'operation/Party.html#group-party',
    'quality_rules': 'operation/Quality.html',
    'settings': 'settings.html',
    'create_building_unit_valuation': 'valuation/Create_building_unit.html',
    'create_building_unit_qualification_valuation_unconventional': 'valuation/Create_building_unit_qualification_unconventional.html',
    'create_building_unit_qualification_valuation_conventional': 'valuation/Create_building_unit_qualification_conventional.html',
    'create_geoeconomic_zone_valuation': 'valuation/Create_geoeconomic_zone.html',
    'create_physical_zone_valuation': 'valuation/Create_physical_zone.html',
    'import_from_excel': 'toolbar.html#import-from-intermediate-structure',
    'import_schema' : 'data_management.html#create-ladm-col-structure',
    'import_data' : 'data_management.html#import-data',
    'export_data' : 'data_management.html#export-data'
}

QGIS_REQUIRED_VERSION = '3.4.6-Madeira'
QGIS_REQUIRED_VERSION_INT = 30406
JAVA_REQUIRED_VERSION = 1.8

# Configure QGIS Model Baker Dependency
QGIS_MODEL_BAKER_PLUGIN_NAME = "QgisModelBaker"
QGIS_MODEL_BAKER_MIN_REQUIRED_VERSION = "4.3.1.2"

# If Asistente LADM_COL depends on a specific version of QGIS Model Baker
#  (and only on that one), set to True
QGIS_MODEL_BAKER_EXACT_REQUIRED_VERSION = True

# If Asistente LADM_COL depends on a specific version of QGIS Model Baker
#  (and only on that one), and it is not the latest release, then you can
#  specify a download URL. If that's not the case, pass an empty string below
QGIS_MODEL_BAKER_REQUIRED_VERSION_URL = 'https://github.com/AgenciaImplementacion/QgisModelBaker/releases/download/v4.3.1.2/QgisModelBaker.zip' # 'https://github.com/opengisch/QgisModelBaker/releases/download/4.3.1/QgisModelBaker.4.3.1.zip'

# Configure Map Swipe Tool Dependency
MAP_SWIPE_TOOL_PLUGIN_NAME = "mapswipetool_plugin"
MAP_SWIPE_TOOL_MIN_REQUIRED_VERSION = "1.2"
MAP_SWIPE_TOOL_EXACT_REQUIRED_VERSION = True
MAP_SWIPE_TOOL_REQUIRED_VERSION_URL = 'https://plugins.qgis.org/plugins/mapswipetool_plugin/version/1.2/download/' # ''https://github.com/AgenciaImplementacion/QgisModelBaker/releases/download/v4.1.0.1/QgisModelBaker.zip'

# Change detection
PARCEL_STATUS = '_PARCEL_STATUS_'
PARCEL_STATUS_DISPLAY = ''
CHANGE_DETECTION_NEW_PARCEL = QCoreApplication.translate("", "New parcel") # alta
CHANGE_DETECTION_MISSING_PARCEL = QCoreApplication.translate("", "Missing parcel") # Baja
CHANGE_DETECTION_PARCEL_CHANGED = QCoreApplication.translate("", "Parcel changed")
CHANGE_DETECTION_PARCEL_ONLY_GEOMETRY_CHANGED = QCoreApplication.translate("", "Only geometry changed")
CHANGE_DETECTION_PARCEL_REMAINS = QCoreApplication.translate("", "OK")
CHANGE_DETECTION_SEVERAL_PARCELS = QCoreApplication.translate("", "Several")
CHANGE_DETECTION_NULL_PARCEL = QCoreApplication.translate("", "null")
STATUS_COLORS = {CHANGE_DETECTION_NEW_PARCEL: Qt.red,
                 CHANGE_DETECTION_MISSING_PARCEL: Qt.red,
                 CHANGE_DETECTION_PARCEL_CHANGED: Qt.red,
                 CHANGE_DETECTION_PARCEL_ONLY_GEOMETRY_CHANGED: Qt.red,
                 CHANGE_DETECTION_PARCEL_REMAINS: Qt.green,
                 CHANGE_DETECTION_SEVERAL_PARCELS: Qt.yellow,
                 CHANGE_DETECTION_NULL_PARCEL: Qt.yellow}
SOURCE_DB = '_SOURCE_'
SUPPLIES_DB_SOURCE = '_SUPPLIES_'
COLLECTED_DB_SOURCE = '_COLLECTED_'
PLOT_GEOMETRY_KEY = 'GEOMETRY_PLOT'

# QGIS Model Baker definitions
SCHEMA_NAME = 'schemaname'
TABLE_NAME = 'tablename'
PRIMARY_KEY = 'primary_key'
GEOMETRY_COLUMN = 'geometry_column'
SRID = 'srid'
GEOMETRY_TYPE = 'type'
KIND_SETTINGS = 'kind_settings'
TABLE_ALIAS = 'table_alias'
MODEL = 'model'
REFERENCING_LAYER = 'referencing_table'
REFERENCING_FIELD = 'referencing_column'
RELATION_NAME = 'constraint_name'
REFERENCED_LAYER = 'referenced_table'
REFERENCED_FIELD = 'referenced_column'
DOMAIN_CLASS_RELATION = 'domain_class'
CLASS_CLASS_RELATION = 'class_class'

TEST_SERVER = "www.google.com"

# Colors for labels in wizards and dialogs
CSS_COLOR_ERROR_LABEL = "color:#FF0000"
CSS_COLOR_OKAY_LABEL = "color:#478046"
CSS_COLOR_INACTIVE_LABEL = "color:#646464"

# DOWNLOAD PAGE URL IN QGIS PLUGIN REPO
PLUGIN_DOWNLOAD_URL_IN_QGIS_REPO = "https://plugins.qgis.org/plugins/asistente_ladm_col/"

# About dialog
RELEASE_URL = "https://github.com/AgenciaImplementacion/Asistente-LADM_COL/releases/tag/"

# For testing if an schema comes from ili2db
INTERLIS_TEST_METADATA_TABLE_PG = 't_ili2db_table_prop'

# Endpoint for testing the Source Service (avoid last slash)
DEFAULT_ENDPOINT_SOURCE_SERVICE = 'http://portal.proadmintierra.info:18888/filemanager'
SOURCE_SERVICE_UPLOAD_SUFFIX = 'v1/file'
SOURCE_SERVICE_EXPECTED_ID = 'IDEATFileManager'
SUFFIX_GET_THUMBNAIL = "&thumbnail=true&size=large"

# UI OBJECTNAMES
OPERATION_MENU_OBJECTNAME = "ladm_col_operation"
LADM_COL_MENU_OBJECTNAME = "ladm_col"
PROPERTY_RECORD_CARD_MENU_OBJECTNAME = "ladm_col_property_record_card"
QUERIES_ACTION_OBJECTNAME = "ladm_col_queries"
REPORTS_MENU_OBJECTNAME = "ladm_col_reports"
VALUATION_MENU_OBJECTNAME = "ladm_col_valuation"

# Documentation
HELP_DOWNLOAD = 'https://github.com/AgenciaImplementacion/Asistente-LADM_COL-docs/releases/download'


# Wizards
WIZARD_NAME = "wizard_name"
WIZARD_CLASS = "wizard_class"
WIZARD_FEATURE_NAME = "wizard_tool_name"
WIZARD_UI = "wizard_ui"
WIZARD_HELP = "wizard_help"
WIZARD_HELP_PAGES = "wizard_help_page"
WIZARD_QSETTINGS = "wizard_qsettings"
WIZARD_QSETTINGS_LOAD_DATA_TYPE = "wizard_qsettings_load_data_type"
WIZARD_QSETTINGS_LOAD_CONVENTION_TYPE = "wizard_qsettings_load_convention_type"
WIZARD_QSETTINGS_TYPE_PARCEL_SELECTED = "wizard_qsetting_type_parcel_selected"
WIZARD_TOOL_NAME = "wizard_tool_name"

WIZARD_HELP1 = "wizard_help1"
WIZARD_HELP2 = "wizard_help2"
WIZARD_HELP3 = "wizard_help3"
WIZARD_HELP4 = "wizard_help4"
WIZARD_HELP5 = "wizard_help5"

WIZARD_TYPE = "wizard_type"

WIZARD_LAYERS = "wizard_layers"
WIZARD_EDITING_LAYER_NAME = "wizard_editing_layer_name"
WIZARD_MAP_LAYER_PROXY_MODEL = "wizard_map_layer_proxy_model"
WIZARD_READ_ONLY_FIELDS = "wizard_read_only_fields"

# Cadastral model
WIZARD_CREATE_COL_PARTY_CADASTRAL = "wizard_create_col_party_cadastral"
WIZARD_CREATE_ADMINISTRATIVE_SOURCE_OPERATION = "wizard_create_administrative_source_operation"
WIZARD_CREATE_BOUNDARY_OPERATION = "wizard_create_boundary_operation"
WIZARD_CREATE_BUILDING_OPERATION = "wizard_create_building_operation"
WIZARD_CREATE_BUILDING_UNIT_OPERATION = "wizard_create_building_unit_operation"
WIZARD_CREATE_RIGHT_OPERATION = "wizard_create_right_operation"
WIZARD_CREATE_RESTRICTION_OPERATION = "wizard_create_restriction_operation"
WIZARD_CREATE_SPATIAL_SOURCE_OPERATION = "wizard_create_spatial_source_operation"
WIZARD_CREATE_PARCEL_OPERATION = "wizard_create_parcel_operation"
WIZARD_CREATE_PLOT_OPERATION = "wizard_create_plot_operation"
WIZARD_CREATE_EXT_ADDRESS_OPERATION = "wizard_create_ext_address_operation"
WIZARD_CREATE_RIGHT_OF_WAY_OPERATION = "wizard_create_right_of_way_operation"

# Valuation model
WIZARD_CREATE_GEOECONOMIC_ZONE_VALUATION = "wizard_create_geoeconomic_zone_valuation"
WIZARD_CREATE_PHYSICAL_ZONE_VALUATION = "wizard_create_physical_zone_valuation"
WIZARD_CREATE_BUILDING_UNIT_VALUATION = "wizard_create_building_unit_valuation"
WIZARD_CREATE_BUILDING_UNIT_QUALIFICATION_VALUATION = "wizard_create_building_unit_qualification_valuation"

# Log topology rules
LOG_QUALITY_PREFIX_TOPOLOGICAL_RULE_TITLE = "<h4>"
LOG_QUALITY_SUFFIX_TOPOLOGICAL_RULE_TITLE = "</h4>"
LOG_QUALITY_LIST_CONTAINER_OPEN = "<ul>"
LOG_QUALITY_LIST_CONTAINER_CLOSE = "</ul>"
LOG_QUALITY_CONTENT_SEPARATOR = "<HR>"
LOG_QUALITY_LIST_ITEM_ERROR_OPEN = "<li style='color:red;'>"
LOG_QUALITY_LIST_ITEM_ERROR_CLOSE = "</li>"
LOG_QUALITY_LIST_ITEM_CORRECT_OPEN = "<li style='color:green;'>"
LOG_QUALITY_LIST_ITEM_CORRECT_CLOSE = "</li>"
LOG_QUALITY_LIST_ITEM_OPEN = "<li style='color:#ffd356;'>"
LOG_QUALITY_LIST_ITEM_CLOSE = "</li>"

# Excel titles
EXCEL_SHEET_NAME_PLOT = 'predio'
EXCEL_SHEET_NAME_PARTY = 'interesado'
EXCEL_SHEET_NAME_GROUP = 'agrupacion'
EXCEL_SHEET_NAME_RIGHT = 'derecho'
EXCEL_SHEET_TITLE_DEPARTMENT = 'departamento'
EXCEL_SHEET_TITLE_MUNICIPALITY = 'municipio'
EXCEL_SHEET_TITLE_ZONE = 'zona'
EXCEL_SHEET_TITLE_REGISTRATION_PLOT = 'matricula predio'
EXCEL_SHEET_TITLE_NPN = 'numero predial nuevo'
EXCEL_SHEET_TITLE_NPV = 'numero predial viejo'
EXCEL_SHEET_TITLE_PLOT_NAME = 'nombre predio'
EXCEL_SHEET_TITLE_VALUATION = 'avaluo'
EXCEL_SHEET_TITLE_PLOT_TYPE = 'tipo predio'
EXCEL_SHEET_TITLE_FIRST_NAME = 'nombre1'
EXCEL_SHEET_TITLE_MIDDLE = 'nombre2'
EXCEL_SHEET_TITLE_FIRST_SURNAME = 'apellido1'
EXCEL_SHEET_TITLE_SECOND_SURNAME = 'apellido2'
EXCEL_SHEET_TITLE_BUSINESS_NAME = 'razon social'
EXCEL_SHEET_TITLE_SEX = 'sexo persona'
EXCEL_SHEET_TITLE_DOCUMENT_TYPE = 'tipo documento'
EXCEL_SHEET_TITLE_DOCUMENT_NUMBER = 'numero de documento'
EXCEL_SHEET_TITLE_KIND_PERSON = 'tipo persona'
EXCEL_SHEET_TITLE_ISSUING_ENTITY = 'organo emisor del documento'
EXCEL_SHEET_TITLE_DATE_ISSUE = 'fecha emision del documento'
EXCEL_SHEET_TITLE_ID_GROUP = 'id agrupación'
EXCEL_SHEET_TITLE_TYPE = 'tipo'
EXCEL_SHEET_TITLE_PARTY_DOCUMENT_NUMBER = 'número documento Interesado'
EXCEL_SHEET_TITLE_GROUP = 'agrupación'
EXCEL_SHEET_TITLE_SOURCE_TYPE = 'tipo de fuente'
EXCEL_SHEET_TITLE_DESCRIPTION_SOURCE = 'Descripción de la fuente'
EXCEL_SHEET_TITLE_STATE_SOURCE = 'estado_disponibilidad de la fuente'
EXCEL_SHEET_TITLE_OFFICIALITY_SOURCE = 'Es oficial la fuente'
EXCEL_SHEET_TITLE_STORAGE_PATH = 'Ruta de Almacenamiento de la fuente'

ERROR_LAYER_GROUP = "ERROR_LAYER_GROUP"
CHECK_OVERLAPS_IN_BOUNDARY_POINTS = "CHECK_OVERLAPS_IN_BOUNDARY_POINTS"
CHECK_OVERLAPS_IN_CONTROL_POINTS = "CHECK_OVERLAPS_IN_CONTROL_POINTS"
CHECK_BOUNDARY_POINTS_COVERED_BY_BOUNDARY_NODES = "CHECK_BOUNDARY_POINTS_COVERED_BY_BOUNDARY_NODES"
RIGHT_OF_WAY_LINE_LAYER = "RIGHT_OF_WAY_LINE_LAYER"
CHECK_BOUNDARY_POINTS_COVERED_BY_PLOT_NODES = "CHECK_BOUNDARY_POINTS_COVERED_BY_PLOT_NODES"
CHECK_TOO_LONG_BOUNDARY_SEGMENTS = "CHECK_TOO_LONG_BOUNDARY_SEGMENTS"
CHECK_OVERLAPS_IN_BOUNDARIES = "CHECK_OVERLAPS_IN_BOUNDARIES"
CHECK_BOUNDARIES_ARE_NOT_SPLIT = "CHECK_BOUNDARIES_ARE_NOT_SPLIT"
CHECK_BOUNDARIES_COVERED_BY_PLOTS = "CHECK_BOUNDARIES_COVERED_BY_PLOTS"
CHECK_BOUNDARY_NODES_COVERED_BY_BOUNDARY_POINTS = "CHECK_BOUNDARY_NODES_COVERED_BY_BOUNDARY_POINTS"
CHECK_DANGLES_IN_BOUNDARIES = "CHECK_DANGLES_IN_BOUNDARIES"
CHECK_OVERLAPS_IN_PLOTS = "CHECK_OVERLAPS_IN_PLOTS"
CHECK_OVERLAPS_IN_BUILDINGS = "CHECK_OVERLAPS_IN_BUILDINGS"
CHECK_OVERLAPS_IN_RIGHTS_OF_WAY = "CHECK_OVERLAPS_IN_RIGHTS_OF_WAY"
CHECK_PLOTS_COVERED_BY_BOUNDARIES = "CHECK_PLOTS_COVERED_BY_BOUNDARIES"
CHECK_RIGHT_OF_WAY_OVERLAPS_BUILDINGS = "CHECK_RIGHT_OF_WAY_OVERLAPS_BUILDINGS"
CHECK_GAPS_IN_PLOTS = "CHECK_GAPS_IN_PLOTS"
CHECK_MULTIPART_IN_RIGHT_OF_WAY = "CHECK_MULTIPART_IN_RIGHT_OF_WAY"
CHECK_BUILDING_WITHIN_PLOTS = "CHECK_BUILDING_WITHIN_PLOTS"
CHECK_BUILDING_UNIT_WITHIN_PLOTS = "CHECK_BUILDING_UNIT_WITHIN_PLOTS"

# Logic consistency checks
CHECK_PARCEL_RIGHT_RELATIONSHIP = "CHECK_PARCEL_RIGHT_RELATIONSHIP"
CHECK_FRACTION_SUM_FOR_PARTY_GROUPS = "CHECK_FRACTION_SUM_FOR_PARTY_GROUPS"
FIND_DUPLICATE_RECORDS_IN_A_TABLE = "FIND_DUPLICATE_RECORDS_IN_A_TABLE"
CHECK_DEPARMENT_CODE_HAS_TWO_NUMERICAL_CHARACTERS = "CHECK_DEPARMENT_CODE_HAS_TWO_NUMERICAL_CHARACTERS"
CHECK_MUNICIPALITY_CODE_HAS_THREE_NUMERICAL_CHARACTERS = "CHECK_MUNICIPALITY_CODE_HAS_THREE_NUMERICAL_CHARACTERS"
CHECK_PARCEL_NUMBER_HAS_30_NUMERICAL_CHARACTERS = "CHECK_PARCEL_NUMBER_HAS_30_NUMERICAL_CHARACTERS"
CHECK_PARCEL_NUMBER_BEFORE_HAS_20_NUMERICAL_CHARACTERS = "CHECK_PARCEL_NUMBER_BEFORE_HAS_20_NUMERICAL_CHARACTERS"
CHECK_COL_PARTY_NATURAL_TYPE = "CHECK_COL_PARTY_NATURAL_TYPE"
CHECK_COL_PARTY_LEGAL_TYPE = "CHECK_COL_PARTY_LEGAL_TYPE"
CHECK_PARCEL_TYPE_AND_22_POSITON_OF_PARCEL_NUMBER = "CHECK_PARCEL_TYPE_AND_22_POSITON_OF_PARCEL_NUMBER"
CHECK_UEBAUNIT_PARCEL = "CHECK_UEBAUNIT_PARCEL"

# Logic consistency errors
ERROR_PARCEL_WITH_NO_RIGHT = "ERROR_PARCEL_WITH_NO_RIGHT"
ERROR_PARCEL_WITH_REPEATED_DOMAIN_RIGHT = "ERROR_PARCEL_WITH_REPEATED_DOMAIN_RIGHT"

# Specific topology errors
CHECK_PLOT_NODES_COVERED_BY_BOUNDARY_POINTS = "CHECK_PLOT_NODES_COVERED_BY_BOUNDARY_POINTS"
ERROR_PLOT_IS_NOT_COVERED_BY_BOUNDARY = "ERROR_PLOT_IS_NOT_COVERED_BY_BOUNDARY"
ERROR_BOUNDARY_IS_NOT_COVERED_BY_PLOT = "ERROR_BOUNDARY_IS_NOT_COVERED_BY_PLOT"
ERROR_NO_MORE_BOUNDARY_FACE_STRING_TABLE = "ERROR_NO_MORE_BOUNDARY_FACE_STRING_TABLE"
ERROR_DUPLICATE_MORE_BOUNDARY_FACE_STRING_TABLE = "ERROR_DUPLICATE_MORE_BOUNDARY_FACE_STRING_TABLE"
ERROR_NO_LESS_TABLE = "ERROR_NO_LESS_TABLE"
ERROR_DUPLICATE_LESS_TABLE = "ERROR_DUPLICATE_LESS_TABLE"
ERROR_NO_FOUND_POINT_BFS = "ERROR_NO_FOUND_POINT_BFS"
ERROR_DUPLICATE_POINT_BFS = "ERROR_DUPLICATE_POINT_BFS"
ERROR_BOUNDARY_POINT_IS_NOT_COVERED_BY_BOUNDARY_NODE = "ERROR_BOUNDARY_POINT_IS_NOT_COVERED_BY_BOUNDARY_NODE"
ERROR_BOUNDARY_NODE_IS_NOT_COVERED_BY_BOUNDARY_POINT = "ERROR_BOUNDARY_NODE_IS_NOT_COVERED_BY_BOUNDARY_POINT"
ERROR_BUILDING_IS_NOT_OVER_A_PLOT = "ERROR_BUILDING_IS_NOT_OVER_A_PLOT"
ERROR_BUILDING_CROSSES_A_PLOT_LIMIT = "ERROR_BUILDING_CROSSES_A_PLOT_LIMIT"
ERROR_BUILDING_UNIT_IS_NOT_OVER_A_PLOT = "ERROR_BUILDING_UNIT_IS_NOT_OVER_A_PLOT"
ERROR_BUILDING_UNIT_CROSSES_A_PLOT_LIMIT = "ERROR_BUILDING_UNIT_CROSSES_A_PLOT_LIMIT"

class TranslatableConfigStrings(QObject):
    def __init__(self):
        self.names = Names()

    def get_translatable_config_strings(self):
        return {
            ERROR_LAYER_GROUP: QCoreApplication.translate("TranslatableConfigStrings", "Validation errors"),
            CHECK_OVERLAPS_IN_BOUNDARY_POINTS: QCoreApplication.translate("TranslatableConfigStrings", "Boundary Points should not overlap"),
            CHECK_OVERLAPS_IN_CONTROL_POINTS: QCoreApplication.translate("TranslatableConfigStrings", "Control Points should not overlap"),
            CHECK_BOUNDARY_POINTS_COVERED_BY_BOUNDARY_NODES: QCoreApplication.translate("TranslatableConfigStrings", "Boundary Points should be covered by Boundary nodes"),
            RIGHT_OF_WAY_LINE_LAYER: QCoreApplication.translate("TranslatableConfigStrings", "Right of way line"),
            CHECK_BOUNDARY_POINTS_COVERED_BY_PLOT_NODES: QCoreApplication.translate("TranslatableConfigStrings", "Boundary Points should be covered by plot nodes"),
            CHECK_TOO_LONG_BOUNDARY_SEGMENTS: QCoreApplication.translate("TranslatableConfigStrings", "Boundary segments should not be longer than {}m.").format(int(QSettings().value('Asistente-LADM_COL/quality/too_long_tolerance', DEFAULT_TOO_LONG_BOUNDARY_SEGMENTS_TOLERANCE))),
            CHECK_OVERLAPS_IN_BOUNDARIES: QCoreApplication.translate("TranslatableConfigStrings", "Boundaries should not overlap"),
            CHECK_BOUNDARIES_ARE_NOT_SPLIT: QCoreApplication.translate("TranslatableConfigStrings", "Boundaries should not be split"),
            CHECK_BOUNDARIES_COVERED_BY_PLOTS: QCoreApplication.translate("TranslatableConfigStrings", "Boundaries should be covered by Plots"),
            CHECK_BOUNDARY_NODES_COVERED_BY_BOUNDARY_POINTS: QCoreApplication.translate("TranslatableConfigStrings", "Boundary nodes should be covered by Boundary Points"),
            CHECK_DANGLES_IN_BOUNDARIES: QCoreApplication.translate("TranslatableConfigStrings", "Boundaries should not have dangles"),
            CHECK_OVERLAPS_IN_PLOTS: QCoreApplication.translate("TranslatableConfigStrings", "Plots should not overlap"),
            CHECK_OVERLAPS_IN_BUILDINGS: QCoreApplication.translate("TranslatableConfigStrings", "Buildings should not overlap"),
            CHECK_OVERLAPS_IN_RIGHTS_OF_WAY: QCoreApplication.translate("TranslatableConfigStrings", "Rights of Way should not overlap"),
            CHECK_PLOTS_COVERED_BY_BOUNDARIES: QCoreApplication.translate("TranslatableConfigStrings", "Plots should be covered by Boundaries"),
            CHECK_RIGHT_OF_WAY_OVERLAPS_BUILDINGS: QCoreApplication.translate("TranslatableConfigStrings", "Right of Way should not overlap Buildings"),
            CHECK_GAPS_IN_PLOTS: QCoreApplication.translate("TranslatableConfigStrings", "Plots should not have gaps"),
            CHECK_MULTIPART_IN_RIGHT_OF_WAY: QCoreApplication.translate("TranslatableConfigStrings", "Right of Way should not have multipart geometries"),
            CHECK_BUILDING_WITHIN_PLOTS: QCoreApplication.translate("TranslatableConfigStrings", "Buildings should be within Plots"),
            CHECK_BUILDING_UNIT_WITHIN_PLOTS: QCoreApplication.translate("TranslatableConfigStrings", "Building Units should be within Plots"),
            CHECK_PARCEL_RIGHT_RELATIONSHIP: QCoreApplication.translate("TranslatableConfigStrings", "Parcel should have one and only one Right"),
            CHECK_FRACTION_SUM_FOR_PARTY_GROUPS: QCoreApplication.translate("TranslatableConfigStrings", "Group Party Fractions should sum 1"),
            FIND_DUPLICATE_RECORDS_IN_A_TABLE: QCoreApplication.translate("TranslatableConfigStrings", "Table records should not be repeated"),
            CHECK_DEPARMENT_CODE_HAS_TWO_NUMERICAL_CHARACTERS: QCoreApplication.translate("TranslatableConfigStrings", "Check that the {department} field of the {parcel} table has two numerical characters").format(department=self.names.OP_PARCEL_T_DEPARTMENT_F, parcel=self.names.OP_PARCEL_T),
            CHECK_MUNICIPALITY_CODE_HAS_THREE_NUMERICAL_CHARACTERS: QCoreApplication.translate("TranslatableConfigStrings", "Check that the {municipality} field of the {parcel} table has three numerical characters").format(municipality=self.names.OP_PARCEL_T_MUNICIPALITY_F, parcel=self.names.OP_PARCEL_T),
            CHECK_PARCEL_NUMBER_HAS_30_NUMERICAL_CHARACTERS: QCoreApplication.translate("TranslatableConfigStrings", "Check that the {parcel_number} has 30 numerical characters").format(parcel_number=self.names.OP_PARCEL_T_PARCEL_NUMBER_F),
            CHECK_PARCEL_NUMBER_BEFORE_HAS_20_NUMERICAL_CHARACTERS: QCoreApplication.translate("TranslatableConfigStrings", "Check that the {parcel_number_before} has 20 numerical characters").format(parcel_number_before=self.names.OP_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F),
            CHECK_COL_PARTY_NATURAL_TYPE: QCoreApplication.translate("TranslatableConfigStrings", "Check that attributes are appropriate for parties of type natural"),
            CHECK_COL_PARTY_LEGAL_TYPE: QCoreApplication.translate("TranslatableConfigStrings", "Check that attributes are appropriate for parties of type legal"),
            CHECK_PARCEL_TYPE_AND_22_POSITON_OF_PARCEL_NUMBER: QCoreApplication.translate("TranslatableConfigStrings", "Check that the type of parcel corresponds to position 22 of the {parcel_number}").format(parcel_number=self.names.OP_PARCEL_T_PARCEL_NUMBER_F),
            CHECK_UEBAUNIT_PARCEL: QCoreApplication.translate("TranslatableConfigStrings", "Check that Spatial Units associated with Parcels correspond to the parcel type"),
            ERROR_PARCEL_WITH_NO_RIGHT: QCoreApplication.translate("TranslatableConfigStrings", "Parcel does not have any Right associated"),
            ERROR_PARCEL_WITH_REPEATED_DOMAIN_RIGHT: QCoreApplication.translate("TranslatableConfigStrings", "Parcel has more than one domain right associated"),
            CHECK_PLOT_NODES_COVERED_BY_BOUNDARY_POINTS: QCoreApplication.translate("TranslatableConfigStrings", "Plot nodes should be covered by boundary points"),
            ERROR_PLOT_IS_NOT_COVERED_BY_BOUNDARY: QCoreApplication.translate("TranslatableConfigStrings", "Plot is not covered by boundary"),
            ERROR_BOUNDARY_IS_NOT_COVERED_BY_PLOT: QCoreApplication.translate("TranslatableConfigStrings", "Boundary is not covered by plot"),
            ERROR_NO_MORE_BOUNDARY_FACE_STRING_TABLE: QCoreApplication.translate("TranslatableConfigStrings", "Topological relationship between boundary and plot is not recorded in the masccl table"),
            ERROR_DUPLICATE_MORE_BOUNDARY_FACE_STRING_TABLE: QCoreApplication.translate("TranslatableConfigStrings", "Topological relationship between boundary and plot is duplicated in the masccl table"),
            ERROR_NO_LESS_TABLE: QCoreApplication.translate("TranslatableConfigStrings", "Topological relationship between boundary and plot is not recorded in the menosccl table"),
            ERROR_DUPLICATE_LESS_TABLE: QCoreApplication.translate("TranslatableConfigStrings", "Topological relationship between boundary and plot is duplicated in the menosccl table"),
            ERROR_NO_FOUND_POINT_BFS: QCoreApplication.translate("TranslatableConfigStrings", "Topological relationship between boundary point and boundary is not recorded in the puntoccl table"),
            ERROR_DUPLICATE_POINT_BFS: QCoreApplication.translate("TranslatableConfigStrings", "Topological relationship between boundary point and boundary is duplicated in the puntoccl table"),
            ERROR_BOUNDARY_POINT_IS_NOT_COVERED_BY_BOUNDARY_NODE: QCoreApplication.translate("TranslatableConfigStrings", "Boundary point is not covered by boundary node"),
            ERROR_BOUNDARY_NODE_IS_NOT_COVERED_BY_BOUNDARY_POINT: QCoreApplication.translate("TranslatableConfigStrings", "Boundary node is not covered by boundary point"),
            ERROR_BUILDING_IS_NOT_OVER_A_PLOT: QCoreApplication.translate("TranslatableConfigStrings", "Building is not over a plot"),
            ERROR_BUILDING_CROSSES_A_PLOT_LIMIT: QCoreApplication.translate("TranslatableConfigStrings", "Building crosses a plot's limit"),
            ERROR_BUILDING_UNIT_IS_NOT_OVER_A_PLOT: QCoreApplication.translate("TranslatableConfigStrings", "Building Unit is not over a plot"),
            ERROR_BUILDING_UNIT_CROSSES_A_PLOT_LIMIT: QCoreApplication.translate("TranslatableConfigStrings", "Building Unit crosses a plot's limit")
        }
