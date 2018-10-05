import os.path

from ..utils.qt_utils import get_plugin_metadata
from qgis.PyQt.QtCore import QLocale, QSettings, QObject, QCoreApplication

CADASTRE_MODEL_PREFIX = "Catastro_Registro_Nucleo_"
CADASTRE_MODEL_PREFIX_LEGACY = "Catastro_COL_"
PROPERTY_RECORD_CARD_MODEL_PREFIX = "Ficha_Predial_"
# From this version on the plugin will work, a message will block prior versions
LATEST_UPDATE_FOR_SUPPORTED_MODEL_VERSION = "17.07.2018"

DEFAULT_EPSG =  "3116"
DEFAULT_TOO_LONG_BOUNDARY_SEGMENTS_TOLERANCE = 200 # meters
DEFAULT_USE_ROADS_VALUE = False
DEFAULT_POLYGON_AREA_TOLERANCE = 0.1 # square meters
HELP_URL = "https://agenciaimplementacion.github.io/Asistente-LADM_COL"
PLUGIN_DIR = os.path.dirname(os.path.dirname(__file__))
PLUGIN_VERSION = get_plugin_metadata('asistente_ladm_col', 'version')
PLUGIN_NAME = get_plugin_metadata('asistente_ladm_col', 'name')
HELP_DIR_NAME = 'help'
QGIS_LANG = QLocale(QSettings().value('locale/userLocale')).name()[:2]
STYLES_DIR = os.path.join(PLUGIN_DIR, 'styles')

MODULE_HELP_MAPPING = {
    '' : 'index.html', # default module is '', just go to index.html
    'controlled_measurement': 'cadastre/Preprocessing.html#controlled-measurement',
    'create_admin_source': 'cadastre/Source.html#administrative-source',
    'create_parcel': 'cadastre/Basic_Administrative_Unit.html#parcel',
    'create_points': 'cadastre/Surveying_and_Representation.html#create-point',
    'create_boundaries': 'cadastre/Surveying_and_Representation.html#create-boundary',
    'create_plot': 'cadastre/Spatial_Unit.html#create-plot',
    'create_building': 'cadastre/Spatial_Unit.html#create-building',
    'create_building_unit': 'cadastre/Spatial_Unit.html#create-building-unit',
    'create_right': 'cadastre/RRR.html#right',
    'create_responsibility': 'cadastre/RRR.html#responsibility',
    'create_restriction': 'cadastre/RRR.html#restriction',
    'create_spatial_source': 'cadastre/Source.html#spatial-source',
    'load_layers': 'load_layers.html#load-layers',
    'col_party': 'cadastre/Party.html#col-party',
    'quality_rules': 'index.html', # TODO: Add this to help sections
    'settings': 'help.html#settings',
    'create_property_record_card': 'property_record_card/Property_record_card.html',
    'create_nuclear_family': 'property_record_card/Nuclear_family.html',
    'create_natural_party': 'property_record_card/Natural_party.html',
    'create_legal_party': 'property_record_card/Legal_party.html',
    'create_market_research': 'property_record_card/Market_research.html'
}
# Configure Project Generator Dependency
PROJECT_GENERATOR_MIN_REQUIRED_VERSION = "3.3.0"

# If Asistente LADM_COL depends on a specific version of Project Generator
#  (and only on that one), set to True
PROJECT_GENERATOR_EXACT_REQUIRED_VERSION = False

# If Asistente LADM_COL depends on a specific version of Project Generator
#  (and only on that one), and it is not the latest release, then you can
#  specify a download URL. If that's not the case, pass an empty string below
PROJECT_GENERATOR_REQUIRED_VERSION_URL = '' # 'https://github.com/AgenciaImplementacion/projectgenerator/releases/download/3.2.7.2/projectgenerator.zip'

# Project Generator definitions
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
RELATION_TYPE = 'relation_type'
DOMAIN_CLASS_RELATION = 'domain_class'
CLASS_CLASS_RELATION = 'class_class'

TEST_SERVER = "www.google.com"

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

# UI OBJECTNAMES
CADASTRE_MENU_OBJECTNAME = "ladm_col_cadastre"
LADM_COL_MENU_OBJECTNAME = "ladm_col"
PROPERTY_RECORD_CARD_MENU_OBJECTNAME = "ladm_col_property_record_card"

# Documentation
HELP_DOWNLOAD = 'https://github.com/AgenciaImplementacion/Asistente-LADM_COL-docs/releases/download'

class TranslatableConfigStrings(QObject):
    def __init__(self):
        self.ERROR_LAYER_GROUP = QCoreApplication.translate("TranslatableConfigStrings", "Validation errors")
