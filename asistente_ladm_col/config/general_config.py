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

# CTM 12
DEFAULT_SRS_AUTH = "EPSG"
DEFAULT_SRS_CODE = "9377"
DEFAULT_SRS_AUTHID = "EPSG:9377"

PLUGIN_VERSION = get_plugin_metadata('asistente_ladm_col', 'version')
PLUGIN_NAME = get_plugin_metadata('asistente_ladm_col', 'name')
PLUGINS_DIR = os.path.dirname(PLUGIN_DIR)

DEFAULT_ILI2DB_DEBUG_MODE = False
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
ILIVALIDATOR_ERRORS_CATALOG_PATH = os.path.join(PLUGIN_DIR, 'resources', 'models', 'catalogo_errores_ilivalidator.xtf')
IGAC_ERRORS_CATALOG_PATH = os.path.join(PLUGIN_DIR, 'resources', 'models', 'catalogo_errores.xtf')
PROCESSING_MODELS_DIR = os.path.join(PLUGIN_DIR, 'lib', 'processing', 'models')
PROCESSING_SCRIPTS_DIR = os.path.join(PLUGIN_DIR, 'lib', 'processing', 'scripts')
STYLES_DIR = os.path.join(PLUGIN_DIR, 'resources', 'styles')
CTM12_PG_SCRIPT_PATH = os.path.join(PLUGIN_DIR, 'resources', 'sql', 'insert_ctm12_pg.sql')
CTM12_GPKG_SCRIPT_PATH = os.path.join(PLUGIN_DIR, 'resources', 'sql', 'insert_ctm12_gpkg.sql')
TOML_FILE_DIR = os.path.join(PLUGIN_DIR, 'resources', 'toml', 'LADM_COL_configuration.toml')

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
REPORTS_REQUIRED_VERSION = '1.0'
URL_REPORTS_LIBRARIES = 'https://github.com/SwissTierrasColombia/LADM-COL_Reports/releases/download/{}/impresion.zip'.format(REPORTS_REQUIRED_VERSION)
REPORTS_LIBRARIES_MD5SUM = '1298ecaa7a56d639ab0e83897f8d7dbd'

MODULE_HELP_MAPPING = {
    '' : 'index.html', # default module is '', just go to index.html
    'associate_ext_address': 'captura_y_estructura_de_datos.html#relacionar-direccion',
    'create_admin_source': 'captura_y_estructura_de_datos.html#crear-fuente-administrativa',
    'create_parcel': 'captura_y_estructura_de_datos.html#crear-predio',
    'create_points': 'captura_y_estructura_de_datos.html#crear-punto',
    'create_boundary_point': 'captura_y_estructura_de_datos.html#punto-lindero',
    'create_survey_point': 'captura_y_estructura_de_datos.html#punto-levantamiento',
    'create_control_point': 'captura_y_estructura_de_datos.html#punto-de-control',
    'create_boundaries': 'captura_y_estructura_de_datos.html#crear-lindero',
    'create_plot': 'captura_y_estructura_de_datos.html#crear-terreno',
    'create_building': 'captura_y_estructura_de_datos.html#crear-construccion',
    'create_building_unit': 'captura_y_estructura_de_datos.html#crear-unidad-de-construccion',
    'create_right_of_way':'captura_y_estructura_de_datos.html#crear-servidumbre-de-transito',
    'create_right': 'captura_y_estructura_de_datos.html#crear-derecho',
    'create_restriction': 'captura_y_estructura_de_datos.html#crear-restriccion',
    'create_spatial_source': 'captura_y_estructura_de_datos.html#crear-fuente-espacial',
    'enable_ctm12': 'introduccion.html#habilitar-proyeccion-origen-nacional',
    'export_data': 'administracion_de_datos.html#exportar-datos',
    'group_party': 'captura_y_estructura_de_datos.html#crear-agrupacion-de-interesados',
    'import_from_excel': 'captura_y_estructura_de_datos/importar_desde_estructura_intermedia.html',
    'import_schema' : 'administracion_de_datos.html#crear-estructura-ladm-col',
    'import_data' : 'administracion_de_datos.html#importar-datos',
    'load_layers': 'cargar_capas.html',
    'omission_commission_cobol': 'gestion_de_insumos.html#reporte-omisiones-y-comisiones-cobol',
    'omission_commission_snc': 'gestion_de_insumos.html#reporte-omisiones-y-comisiones-snc',
    'party': 'captura_y_estructura_de_datos.html#crear-interesado',
    'quality_rules': 'reglas_de_calidad.html',
    'settings': 'configuracion.html',
    'supplies': 'gestion_de_insumos.html',
    'transitional_system': 'sistema_de_transicion.html',
    'transitional_system_cancel_task': 'sistema_de_transicion.html#cancelar-tarea',
    'transitional_system_login': 'sistema_de_transicion.html#autenticacion',
    'transitional_system_upload_file': 'sistema_de_transicion.html#subir-archivo',
    'welcome_screen': 'introduccion.html#dialogo-de-bienvenida'
}

QGIS_REQUIRED_VERSION = '3.16.0 Hannover'
QGIS_REQUIRED_VERSION_INT = 31600

QR_METADATA_TOOL_NAME = "{} v{}; QGIS v{}.".format(
    PLUGIN_NAME,
    PLUGIN_VERSION,
    Qgis.QGIS_VERSION)

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

# Configure Map Swipe Tool Dependency
MAP_SWIPE_TOOL_PLUGIN_NAME = "mapswipetool_plugin"
MAP_SWIPE_TOOL_MIN_REQUIRED_VERSION = "1.2"
MAP_SWIPE_TOOL_EXACT_REQUIRED_VERSION = True
MAP_SWIPE_TOOL_REQUIRED_VERSION_URL = ''  # 'https://plugins.qgis.org/plugins/mapswipetool_plugin/version/1.2/download/'

# Configure Invisible Layers and Groups Dependency
INVISIBLE_LAYERS_AND_GROUPS_PLUGIN_NAME = "InvisibleLayersAndGroups"
INVISIBLE_LAYERS_AND_GROUPS_MIN_REQUIRED_VERSION = "2.1"
INVISIBLE_LAYERS_AND_GROUPS_EXACT_REQUIRED_VERSION = True
INVISIBLE_LAYERS_AND_GROUPS_REQUIRED_VERSION_URL = 'https://plugins.qgis.org/plugins/InvisibleLayersAndGroups/version/2.1/download/'

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
HELP_ASSET_NAME = "Asistente-LADM-COL-docs.zip"

DEFAULT_DATASET_NAME = "Default_dataset"
FDC_DATASET_NAME = "Captura_en_campo"
# Basket t_id to be used for all new features capured in the field, where we have no function expression
FDC_WILD_CARD_BASKET_ID = 9999

TOLERANCE_MAX_VALUE = 5000  # In millimeters
DEFAULT_TOLERANCE_VALUE = 0  # In millimeters

# Log topology rules
LOG_QUALITY_PREFIX_TOPOLOGICAL_RULE_TITLE = "<h4>"
LOG_QUALITY_SUFFIX_TOPOLOGICAL_RULE_TITLE = "</h4>"
LOG_QUALITY_LIST_CONTAINER_OPEN = "<ul>"
LOG_QUALITY_LIST_CONTAINER_CLOSE = "</ul>"
LOG_QUALITY_CONTENT_SEPARATOR = "<HR>"
LOG_QUALITY_LIST_ITEM_ERROR_OPEN = "<li style='color:red;'>"
LOG_QUALITY_LIST_ITEM_ERROR_CLOSE = "</li>"
LOG_QUALITY_LIST_ITEM_SUCCESS_OPEN = "<li style='color:green;'>"
LOG_QUALITY_LIST_ITEM_SUCCESS_CLOSE = "</li>"
LOG_QUALITY_LIST_ITEM_OPEN = "<li style='color:#f7b907;'>"
LOG_QUALITY_LIST_ITEM_CLOSE = "</li>"
LOG_QUALITY_LIST_ITEM_CRITICAL_OPEN = "<li style='color:#d611ac;'>"
LOG_QUALITY_LIST_ITEM_CRITICAL_CLOSE = "</li>"
LOG_QUALITY_OPTIONS_OPEN = "<span style='color:#949494;font-style: italic'>"
LOG_QUALITY_OPTIONS_CLOSE = "</span>"

WIDGET_STYLE_QUALITY_RULE_SUCCESS = """{color: black;
                                        border: 2px solid White;
                                        border-radius: 7px;
                                        border-style: outset;
                                        background: #AAE89E;
                                        padding: 5px;}"""
WIDGET_STYLE_QUALITY_RULE_ERRORS = """{color: #e1e1e1;
                                       border: 2px solid White;
                                       border-radius: 7px;
                                       border-style: outset;
                                       background: #F15156;
                                       padding: 5px;}"""
WIDGET_STYLE_QUALITY_RULE_UNDEFINED = """{color: #495867;
                                          border: 2px solid White;
                                          border-radius: 7px;
                                          border-style: outset;
                                          background: #F2AF29;
                                          padding: 5px;}"""
WIDGET_STYLE_QUALITY_RULE_CRITICAL = """{color: black;
                                         border: 2px solid White;
                                         border-radius: 7px;
                                         border-style: outset;
                                         background: #B8B8D1;
                                         padding: 5px;}"""
WIDGET_STYLE_QUALITY_RULE_INITIAL_STATE = """{color: #495867;
                                              border: 2px solid White;
                                              border-radius: 7px;
                                              border-style: outset;
                                              background: #fbf5bd;
                                              padding: 5px;}"""

TABLE_ITEM_COLOR_ERROR = "#ebafb5"
TABLE_ITEM_COLOR_EXCEPTION = "#f9d791"
TABLE_ITEM_COLOR_FIXED_ERROR = "#ccf5c4"

# Wizards
WIZARD_CLASS = "wizard_class"
WIZARD_FEATURE_NAME = "wizard_feature_name"
WIZARD_UI = "wizard_ui"
WIZARD_HELP = "wizard_help"
WIZARD_HELP_PAGES = "wizard_help_page"
WIZARD_QSETTINGS = "wizard_qsettings"
WIZARD_QSETTINGS_PATH = "wizard_qsettings_path"
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
WIZARD_STRINGS = "wizard_strings"
WIZARD_SEL_SOURCE_TITLE = "wizard_sel_source_title",
WIZARD_SEL_SOURCE_ENTERING_DATA_MANUALLY = "wizard_sel_source_entering_data_manually"
WIZARD_SEL_FEATURES_TITLE = "wizard_sel_features_title"

WIZARD_REFACTOR_FIELDS_RECENT_MAPPING_OPTIONS = "wizard_refactor_recent_mapping_options"
WIZARD_REFACTOR_FIELDS_LAYER_FILTERS = "wizard_refactor_layer_filters"
WIZARD_SELECT_SOURCE_HELP = "wizard_select_source_help"
WIZARD_FINISH_BUTTON_TEXT = "wizard_finish_button_text"

WIZARD_CREATION_MODE_KEY = "creation_mode"
WIZARD_SELECTED_TYPE_KEY = "selected_type"

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
