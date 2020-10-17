import os.path
import platform

from qgis.PyQt.QtGui import QColor
from qgis.core import Qgis

from asistente_ladm_col.config.translator import PLUGIN_DIR
from asistente_ladm_col.config.enums import EnumLogMode
from asistente_ladm_col.utils.qt_utils import get_plugin_metadata

DEPENDENCIES_BASE_PATH = os.path.join(os.path.expanduser('~'), 'Asistente-LADM-COL')

DEFAULT_LOG_MODE = EnumLogMode.DEV
DEFAULT_LOG_FILE = ''

# Constants for reports
NATIONAL_LAND_AGENCY = "ANT"
ANNEX_17_REPORT = "Anexo_17"
ANT_MAP_REPORT = "Plano_ANT"

PREFIX_ERROR_CODE = 'E'

# CTM 12
DEFAULT_SRS_AUTH = "EPSG"
DEFAULT_SRS_CODE = "9377"
DEFAULT_SRS_AUTHID = "EPSG:9377"

PLUGIN_VERSION = get_plugin_metadata('asistente_ladm_col', 'version')
PLUGIN_NAME = get_plugin_metadata('asistente_ladm_col', 'name')
PLUGINS_DIR = os.path.dirname(PLUGIN_DIR)

DEFAULT_USE_ROADS_VALUE = False
DEFAULT_AUTOMATIC_VALUES_IN_BATCH_MODE = True
HELP_URL = "https://swisstierrascolombia.github.io/Asistente-LADM-COL"
ETL_MODEL_NAME = "model:ETL-model"
ETL_MODEL_WITH_REPROJECTION_NAME = "model:ETL-model-with-reprojection"
FIELD_MAPPING_PATH = os.path.join(DEPENDENCIES_BASE_PATH, 'field_mappings')
FIELD_MAPPING_PARAMETER = 'mapping' if Qgis.QGIS_VERSION_INT < 31400 else 'fieldsmapper'
MAXIMUM_FIELD_MAPPING_FILES_PER_TABLE = 10
HELP_DIR_NAME = 'help'
DEFAULT_USE_CUSTOM_MODELS = True
DEFAULT_MODELS_DIR = os.path.join(PLUGIN_DIR, 'resources', 'models')
STYLES_DIR = os.path.join(PLUGIN_DIR, 'resources', 'styles')
CTM12_PG_SCRIPT_PATH = os.path.join(PLUGIN_DIR, 'resources', 'sql', 'insert_ctm12_pg.sql')
CTM12_GPKG_SCRIPT_PATH = os.path.join(PLUGIN_DIR, 'resources', 'sql', 'insert_ctm12_gpkg.sql')
TOML_FILE_DIR = os.path.join(PLUGIN_DIR, 'resources', 'toml', 'hide_fields_LADM.toml')

BLO_LIS_FILE_PATH = os.path.join(PLUGIN_DIR, 'resources', 'etl', 'blo.lis')  # Default Cobol BLO.lis file
PREDIO_BLOQUEO_FILE_PATH = os.path.join(PLUGIN_DIR, 'resources', 'etl', 'predio_bloqueo.csv')  # Default SNC predio_bloqueo.csv file
FICHA_MATRIZ_FILE_PATH = os.path.join(PLUGIN_DIR, 'resources', 'etl', 'ficha_matriz.csv')  # Default SNC ficha_matriz.csv file
FICHA_MATRIZ_PREDIO_FILE_PATH = os.path.join(PLUGIN_DIR, 'resources', 'etl', 'ficha_matriz_predio.csv')  # Default SNC ficha_matriz_predio.csv file
FICHA_MATRIZ_TORRE_FILE_PATH = os.path.join(PLUGIN_DIR, 'resources', 'etl', 'ficha_matriz_torre.csv')  # Default SNC ficha_matriz_torre.csv file
BUILDING_UNIT_CSVT_FILE_PATH = os.path.join(PLUGIN_DIR, 'resources', 'etl', 'unidad_construccion.csvt')  # Default SNC unidad_construccion.csvt file

# SETTINGS DIALOG TAB INDEXES
SETTINGS_CONNECTION_TAB_INDEX = 0
SETTINGS_MODELS_TAB_INDEX = 1
SETTINGS_QUALITY_TAB_INDEX = 2
SETTINGS_AUTOMATIC_VALUES_TAB_INDEX = 3
SETTINGS_SOURCES_TAB_INDEX = 4
SETTINGS_ADVANCED_TAB_INDEX = 5

# Crypto
CRYPTO_LIBRARY_NAME = "CryptoUtils.jar"
DEPENDENCY_CRYPTO_DIR = os.path.join(DEPENDENCIES_BASE_PATH, "CRYPTO")
CRYPTO_LIBRARY_PATH = os.path.join(DEPENDENCY_CRYPTO_DIR, CRYPTO_LIBRARY_NAME)
URL_CRYPTO_LIBRARY = 'https://github.com/SwissTierrasColombia/Crypto_Utils/releases/download/v1.0.0/Crypto_Utils-0.0.1-SNAPSHOT.jar'
CYPTO_MD5SUM = 'a42e671dcc78f519020a16f4c47da588'

# Version to be installed when creating reports (annex 17 - ANT Map)
# (Other versions, if found, will be dropped in favor of this one)
DEPENDENCY_REPORTS_DIR_NAME = os.path.join(DEPENDENCIES_BASE_PATH, 'impresion')
REPORTS_REQUIRED_VERSION = '0.8'
URL_REPORTS_LIBRARIES = 'https://github.com/SwissTierrasColombia/LADM-COL_Reports/releases/download/{}/impresion.zip'.format(REPORTS_REQUIRED_VERSION)
REPORTS_LIBRARIES_MD5SUM = 'ebccc3bd2e4a9ccaf1da7b94dd222347'

MODULE_HELP_MAPPING = {
    '' : 'index.html', # default module is '', just go to index.html
    'supplies': 'gestion_de_insumos.html',
    'transitional_system': 'sistema_de_transicion.html',
    'create_admin_source': 'captura_y_estructura_de_datos/fuentes.html#fuente-administrativa',
    'create_parcel': 'captura_y_estructura_de_datos/unidad_basica_administrativa.html#predio',
    'create_points': 'captura_y_estructura_de_datos/topografia_y_representacion.html#crear-punto',
    'create_boundaries': 'captura_y_estructura_de_datos/topografia_y_representacion.html#crear-lindero',
    'create_plot': 'captura_y_estructura_de_datos/unidad_espacial.html#crear-terreno',
    'create_building': 'captura_y_estructura_de_datos/unidad_espacial.html#crear-construccion',
    'create_building_unit': 'captura_y_estructura_de_datos/unidad_espacial.html#crear-unidad-de-construccion',
    'create_right_of_way':'captura_y_estructura_de_datos/unidad_espacial.html#crear-servidumbre-de-paso',
    'associate_ext_address': 'captura_y_estructura_de_datos/unidad_espacial.html#relacionar-extdireccion',
    'create_right': 'captura_y_estructura_de_datos/rrr.html#derecho',
    'create_restriction': 'captura_y_estructura_de_datos/rrr.html#restriccion',
    'create_spatial_source': 'captura_y_estructura_de_datos/fuentes.html#fuente-espacial',
    'load_layers': 'cargar_capas.html',
    'party': 'captura_y_estructura_de_datos/interesado.html#crear-interesado',
    'group_party': 'captura_y_estructura_de_datos/interesado.html#agrupacion-de-interesados',
    'quality_rules': 'reglas_de_calidad.html',
    'settings': 'configuracion.html',
    'import_from_excel': 'captura_y_estructura_de_datos/importar_desde_estructura_intermedia.html',
    'import_schema' : 'administracion_de_datos/crear_estructura_ladm_col.html',
    'import_data' : 'administracion_de_datos/importar_datos.html',
    'export_data' : 'administracion_de_datos/exportar_datos.html'
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
QGIS_MODEL_BAKER_MIN_REQUIRED_VERSION = "6.1.1.5"

# If Asistente LADM-COL depends on a specific version of QGIS Model Baker
#  (and only on that one), set to True
QGIS_MODEL_BAKER_EXACT_REQUIRED_VERSION = True

# If Asistente LADM-COL depends on a specific version of QGIS Model Baker
#  (and only on that one), and it is not the latest release, then you can
#  specify a download URL. If that's not the case, pass an empty string below
QGIS_MODEL_BAKER_REQUIRED_VERSION_URL = 'https://github.com/SwissTierrasColombia/QgisModelBaker/releases/download/v6.1.1.5/QgisModelBaker_6115.zip'  # ''

# Configure Map Swipe Tool Dependency
MAP_SWIPE_TOOL_PLUGIN_NAME = "mapswipetool_plugin"
MAP_SWIPE_TOOL_MIN_REQUIRED_VERSION = "1.2"
MAP_SWIPE_TOOL_EXACT_REQUIRED_VERSION = True
MAP_SWIPE_TOOL_REQUIRED_VERSION_URL = ''  # 'https://plugins.qgis.org/plugins/mapswipetool_plugin/version/1.2/download/'

# Configure QField Sync Dependency
QFIELD_SYNC_PLUGIN_NAME = "qfieldsync"
QFIELD_SYNC_MIN_REQUIRED_VERSION = "3.2.0.1"
QFIELD_SYNC_EXACT_REQUIRED_VERSION = True
QFIELD_SYNC_REQUIRED_VERSION_URL = 'https://github.com/SwissTierrasColombia/qfieldsync/releases/download/v3.2.0.1/qfieldsync_3201.zip'  # ''

SOURCE_DB = '_SOURCE_'
SUPPLIES_DB_SOURCE = 'SUPPLIES'
COLLECTED_DB_SOURCE = 'COLLECTED'

TEST_SERVER = "www.google.com"

# Colors for labels in wizards and dialogs
CSS_COLOR_ERROR_LABEL = "color:#FF0000"
CSS_COLOR_OKAY_LABEL = "color:#478046"
CSS_COLOR_INACTIVE_LABEL = "color:#646464"

# Colors for Transitional System task steps
CHECKED_COLOR = QColor(166, 255, 152, 255)
UNCHECKED_COLOR = QColor(255, 245, 152, 255)
GRAY_COLOR = QColor(219, 219, 219, 255)

# Colors for non allocatet parcels in field data capture
NOT_ALLOCATED_PARCEL_COLOR = QColor(255, 165, 0, 255)  # Orange

# DOWNLOAD PAGE URL IN QGIS PLUGIN REPO
PLUGIN_DOWNLOAD_URL_IN_QGIS_REPO = "https://plugins.qgis.org/plugins/asistente_ladm_col/"

# About dialog
RELEASE_URL = "https://github.com/SwissTierrasColombia/Asistente-LADM-COL/releases/tag/"

# Endpoint for testing the Source Service (avoid last slash)
DEFAULT_USE_SOURCE_SERVICE_SETTING = False
DEFAULT_ENDPOINT_SOURCE_SERVICE = 'http://portal.proadmintierra.info:18888/filemanager'
SOURCE_SERVICE_UPLOAD_SUFFIX = 'v1/file'
SOURCE_SERVICE_EXPECTED_ID = 'IDEATFileManager'
SUFFIX_GET_THUMBNAIL = "&thumbnail=true&size=large"

# Documentation
HELP_DOWNLOAD = 'https://github.com/SwissTierrasColombia/Asistente-LADM-COL-docs/releases/download'

DEFAULT_DATASET_NAME = "Default dataset"
FDC_ADMIN_DATASET_NAME = "Captura en campo (Coordinador General)"
FDC_COORDINATOR_DATASET_NAME = "Captura en campo (Coordinador de Campo)"

TOLERANCE_MAX_VALUE = 5000  # In milimeters

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
WIZARD_CREATE_ADMINISTRATIVE_SOURCE_SURVEY = "wizard_create_administrative_source_survey"
WIZARD_CREATE_BOUNDARY_SURVEY = "wizard_create_boundary_survey"
WIZARD_CREATE_BUILDING_SURVEY = "wizard_create_building_survey"
WIZARD_CREATE_BUILDING_UNIT_SURVEY = "wizard_create_building_unit_survey"
WIZARD_CREATE_RIGHT_SURVEY = "wizard_create_right_survey"
WIZARD_CREATE_RESTRICTION_SURVEY = "wizard_create_restriction_survey"
WIZARD_CREATE_SPATIAL_SOURCE_SURVEY = "wizard_create_spatial_source_survey"
WIZARD_CREATE_PARCEL_SURVEY = "wizard_create_parcel_survey"
WIZARD_CREATE_PLOT_SURVEY = "wizard_create_plot_survey"
WIZARD_CREATE_EXT_ADDRESS_SURVEY = "wizard_create_ext_address_survey"
WIZARD_CREATE_RIGHT_OF_WAY_SURVEY = "wizard_create_right_of_way_survey"

# Valuation model
WIZARD_CREATE_GEOECONOMIC_ZONE_VALUATION = "wizard_create_geoeconomic_zone_valuation"
WIZARD_CREATE_PHYSICAL_ZONE_VALUATION = "wizard_create_physical_zone_valuation"
WIZARD_CREATE_BUILDING_UNIT_VALUATION = "wizard_create_building_unit_valuation"
WIZARD_CREATE_BUILDING_UNIT_QUALIFICATION_VALUATION = "wizard_create_building_unit_qualification_valuation"
