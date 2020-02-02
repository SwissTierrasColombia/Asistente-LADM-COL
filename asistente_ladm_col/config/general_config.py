import os.path
import platform

from qgis.PyQt.QtGui import QColor

from asistente_ladm_col.config.translator import PLUGIN_DIR
from asistente_ladm_col.config.enums import LogModeEnum
from asistente_ladm_col.utils.qt_utils import get_plugin_metadata

DEPENDENCIES_BASE_PATH = os.path.join(os.path.expanduser('~'), 'Asistente-LADM_COL')
DEPENDENCY_REPORTS_DIR_NAME = 'impresion'

DEFAULT_LOG_MODE = LogModeEnum.DEV
DEFAULT_LOG_FILE = ''

# Constants for reports
NATIONAL_LAND_AGENCY = "ANT"
ANNEX_17_REPORT = "Anexo_17"
ANT_MAP_REPORT = "Plano_ANT"


DEFAULT_EPSG =  "3116"
DEFAULT_USE_ROADS_VALUE = False
HELP_URL = "https://agenciaimplementacion.github.io/Asistente-LADM_COL"
FIELD_MAPPING_PATH = os.path.join(DEPENDENCIES_BASE_PATH, 'field_mappings')
MAXIMUM_FIELD_MAPPING_FILES_PER_TABLE = 10
PLUGIN_VERSION = get_plugin_metadata('asistente_ladm_col', 'version')
PLUGIN_NAME = get_plugin_metadata('asistente_ladm_col', 'name')
# PLUGIN_DIR (set in translator.py)
HELP_DIR_NAME = 'help'
STYLES_DIR = os.path.join(PLUGIN_DIR, 'resources', 'styles')
TOML_FILE_DIR = os.path.join(PLUGIN_DIR, 'resources', 'toml', 'hide_fields_LADM.toml')

# SISTEMA DE TRANSICIÓN
ST_DOMAIN = "http://apist.proadmintierra.info"
ST_LOGIN_SERVICE_URL = "{}/api/security/oauth/token".format(ST_DOMAIN)
ST_LOGIN_SERVICE_PAYLOAD = "username={}&password={}&grant_type=password"
encoded = b'c3Qtd2ViLXNkVmExTlh3OmhLYmNlTjg5'
ST_LOGIN_AUTHORIZATION_CLIENT = "Basic {}".format(encoded.decode('utf-8'))
ST_GET_TASKS_SERVICE_URL = "{}/api/workspaces/v1/tasks/pending".format(ST_DOMAIN)
TRANSITION_SYSTEM_EXPECTED_RESPONSE = "unauthorized"

BLO_LIS_FILE_PATH = os.path.join(PLUGIN_DIR, 'resources', 'etl', 'blo.lis')  # Default Cobol BLO.lis file

LAYER = 'layer'  # Used as key that holds a QgsVectorLayer in dictionaries

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

QGIS_REQUIRED_VERSION = '3.10.0-A Coruña'
QGIS_REQUIRED_VERSION_INT = 31000
JAVA_REQUIRED_VERSION = 1.8

KEY_JAVA_OS_VERSION = platform.system() + '_' + platform.architecture()[0]

DICT_JAVA_DOWNLOAD_URL = {
    'Linux_32bit': 'https://javadl.oracle.com/webapps/download/AutoDL?BundleId=241524_1f5b5a70bf22433b84d0e960903adac8',  # jre-8u241-linux-i586.tar.gz
    'Linux_64bit': 'https://javadl.oracle.com/webapps/download/AutoDL?BundleId=241526_1f5b5a70bf22433b84d0e960903adac8',  # jre-8u241-linux-x64.tar.gz
    'Darwin_64bit': 'https://github.com/frekele/oracle-java/releases/download/8u212-b10/jre-8u212-macosx-x64.tar.gz',  # jre-8u212-macosx-x64.tar.gz
    'Windows_32bit': 'https://javadl.oracle.com/webapps/download/AutoDL?BundleId=240727_5b13a193868b4bf28bcb45c792fce896',  # jre-8u231-windows-i586.tar.gz
    'Windows_64bit': 'https://javadl.oracle.com/webapps/download/AutoDL?BundleId=240729_5b13a193868b4bf28bcb45c792fce896'  # jre-8u231-windows-x64.tar.gz
}

DICT_JAVA_MD5SUM = {
    'Linux_32bit': '349cf9d4ce26c3ea413be17f59d8b4fe',
    'Linux_64bit': '98f53c5894eeb2e8ffcff84092e0d2f2',
    'Darwin_64bit': '0927df5891c5adf324707da73c6890fa',
    'Windows_32bit': 'e76d2497116cf285c9750bef639cde0b',
    'Windows_64bit': 'e8e21d73ea1c2f0b21bb22fc9e54b8fc'
}

DICT_JAVA_DIR_NAME = {
    'Linux_32bit': 'jre1.8.0_241',
    'Linux_64bit': 'jre1.8.0_241',
    'Darwin_64bit': 'jre1.8.0_212.jre/Contents/Home',
    'Windows_32bit': 'jre1.8.0_231',
    'Windows_64bit': 'jre1.8.0_231'
}

# Configure QGIS Model Baker Dependency
QGIS_MODEL_BAKER_PLUGIN_NAME = "QgisModelBaker"
QGIS_MODEL_BAKER_MIN_REQUIRED_VERSION = "4.3.1.2"

# If Asistente LADM_COL depends on a specific version of QGIS Model Baker
#  (and only on that one), set to True
QGIS_MODEL_BAKER_EXACT_REQUIRED_VERSION = True

# If Asistente LADM_COL depends on a specific version of QGIS Model Baker
#  (and only on that one), and it is not the latest release, then you can
#  specify a download URL. If that's not the case, pass an empty string below
QGIS_MODEL_BAKER_REQUIRED_VERSION_URL = 'https://github.com/AgenciaImplementacion/QgisModelBaker/releases/download/v4.3.1.2/QgisModelBaker.zip'  # 'https://github.com/opengisch/QgisModelBaker/releases/download/4.3.1/QgisModelBaker.4.3.1.zip'

# Configure Map Swipe Tool Dependency
MAP_SWIPE_TOOL_PLUGIN_NAME = "mapswipetool_plugin"
MAP_SWIPE_TOOL_MIN_REQUIRED_VERSION = "1.2"
MAP_SWIPE_TOOL_EXACT_REQUIRED_VERSION = True
MAP_SWIPE_TOOL_REQUIRED_VERSION_URL = ''  # 'https://plugins.qgis.org/plugins/mapswipetool_plugin/version/1.2/download/'

SOURCE_DB = '_SOURCE_'
SUPPLIES_DB_SOURCE = '_SUPPLIES_'
COLLECTED_DB_SOURCE = '_COLLECTED_'

TEST_SERVER = "www.google.com"

# Colors for labels in wizards and dialogs
CSS_COLOR_ERROR_LABEL = "color:#FF0000"
CSS_COLOR_OKAY_LABEL = "color:#478046"
CSS_COLOR_INACTIVE_LABEL = "color:#646464"

# Colors for Transition System task steps
CHECKED_COLOR = QColor(166, 255, 152, 255)
UNCHECKED_COLOR = QColor(255, 245, 152, 255)
GRAY_COLOR = QColor(219, 219, 219, 255)

# DOWNLOAD PAGE URL IN QGIS PLUGIN REPO
PLUGIN_DOWNLOAD_URL_IN_QGIS_REPO = "https://plugins.qgis.org/plugins/asistente_ladm_col/"

# About dialog
RELEASE_URL = "https://github.com/AgenciaImplementacion/Asistente-LADM_COL/releases/tag/"

# Endpoint for testing the Source Service (avoid last slash)
DEFAULT_ENDPOINT_SOURCE_SERVICE = 'http://portal.proadmintierra.info:18888/filemanager'
SOURCE_SERVICE_UPLOAD_SUFFIX = 'v1/file'
SOURCE_SERVICE_EXPECTED_ID = 'IDEATFileManager'
SUFFIX_GET_THUMBNAIL = "&thumbnail=true&size=large"

# Documentation
HELP_DOWNLOAD = 'https://github.com/AgenciaImplementacion/Asistente-LADM_COL-docs/releases/download'

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

# Wizards
WIZARD_CLASS = "wizard_class"
WIZARD_FEATURE_NAME = "wizard_feature_name"
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