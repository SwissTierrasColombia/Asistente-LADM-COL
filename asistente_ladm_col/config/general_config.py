import os.path

from qgis.PyQt.QtCore import (QSettings,
                              QObject,
                              QCoreApplication)

from .translator import PLUGIN_DIR
from .table_mapping_config import (MORE_BOUNDARY_FACE_STRING_TABLE,
                                   POINT_BOUNDARY_FACE_STRING_TABLE,
                                   LESS_TABLE)
from ..utils.qt_utils import get_plugin_metadata

CADASTRE_MODEL_PREFIX = "Catastro_Registro_Nucleo_"
CADASTRE_MODEL_PREFIX_LEGACY = "Catastro_COL_"
PROPERTY_RECORD_CARD_MODEL_PREFIX = "Ficha_Predial_"
VALUATION_MODEL_PREFIX = "Avaluos_"
# From this version on the plugin will work, a message will block prior versions
LATEST_UPDATE_FOR_SUPPORTED_MODEL_VERSION = "17.07.2018"

DEFAULT_EPSG =  "3116"
DEFAULT_TOO_LONG_BOUNDARY_SEGMENTS_TOLERANCE = 200 # meters
DEFAULT_USE_ROADS_VALUE = False
HELP_URL = "https://agenciaimplementacion.github.io/Asistente-LADM_COL"
FIELD_MAPPING_PATH = os.path.join(os.path.expanduser('~'), 'Asistente-LADM_COL', 'field_mappings')
MAXIMUM_FIELD_MAPPING_FILES_PER_TABLE = 10
PLUGIN_VERSION = get_plugin_metadata('asistente_ladm_col', 'version')
PLUGIN_NAME = get_plugin_metadata('asistente_ladm_col', 'name')
HELP_DIR_NAME = 'help'
STYLES_DIR = os.path.join(PLUGIN_DIR, 'styles')

# Version to be installed when creating reports (annex 17)
# (Other versions, if found, will be dropped in favor of this one)
REPORTS_REQUIRED_VERSION = '0.1'
URL_REPORTS_LIBRARIES = 'https://github.com/AgenciaImplementacion/annex_17/releases/download/{}/impresion.zip'.format(REPORTS_REQUIRED_VERSION)

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
    'create_market_research': 'property_record_card/Market_research.html',
    'create_parcel_valuation': 'valuation/Create_parcel.html',
    'create_horizontal_property_valuation': 'valuation/Create_Horizontal_property_main_parcel.html',
    'create_common_equipment_valuation': 'valuation.Create_common_equipment.html',
    'create_building_valuation': 'valuation/Create_building.html',
    'create_building_unit_valuation': 'valuation/Create_building_unit.html',
    'create_building_unit_qualification_valuation_unconventional': 'valuation/Create_building_unit_qualification_unconventional.html',
    'create_building_unit_qualification_valuation_conventional': 'valuation/Create_building_unit_qualification_conventional.html',
    'create_geoeconomic_zone_valuation': 'valuation/Create_geoeconomic_zone.html',
    'create_physical_zone_valuation': 'valuation/Create_physical_zone.html',
    'import_from_excel': 'toolbar.html#import-from-intermediate-structure'
}
# Configure Project Generator Dependency
PROJECT_GENERATOR_MIN_REQUIRED_VERSION = "3.3.7"

# If Asistente LADM_COL depends on a specific version of Project Generator
#  (and only on that one), set to True
PROJECT_GENERATOR_EXACT_REQUIRED_VERSION = False

# If Asistente LADM_COL depends on a specific version of Project Generator
#  (and only on that one), and it is not the latest release, then you can
#  specify a download URL. If that's not the case, pass an empty string below
PROJECT_GENERATOR_REQUIRED_VERSION_URL = '' #'https://github.com/AgenciaImplementacion/projectgenerator/releases/download/3.3.2.1/projectgenerator.zip'

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
VALUATION_MENU_OBJECTNAME = "ladm_col_valuation"

# Documentation
HELP_DOWNLOAD = 'https://github.com/AgenciaImplementacion/Asistente-LADM_COL-docs/releases/download'


class TranslatableConfigStrings(QObject):
    def __init__(self):
        self.ERROR_LAYER_GROUP = QCoreApplication.translate("TranslatableConfigStrings", "Validation errors")
        self.CHECK_OVERLAPS_IN_BOUNDARY_POINTS = QCoreApplication.translate("TranslatableConfigStrings", "Boundary Points should not overlap")
        self.CHECK_OVERLAPS_IN_CONTROL_POINTS = QCoreApplication.translate("TranslatableConfigStrings", "Control Points should not overlap")
        self.CHECK_BOUNDARY_POINTS_COVERED_BY_BOUNDARY_NODES = QCoreApplication.translate("TranslatableConfigStrings", "Boundary Points should be covered by Boundary nodes")
        self.CHECK_BOUNDARY_POINTS_COVERED_BY_PLOT_NODES = QCoreApplication.translate("TranslatableConfigStrings", "Boundary Points should be covered by plot nodes")

        too_long_tolerance = int(QSettings().value('Asistente-LADM_COL/quality/too_long_tolerance', DEFAULT_TOO_LONG_BOUNDARY_SEGMENTS_TOLERANCE)) # meters
        self.CHECK_TOO_LONG_BOUNDARY_SEGMENTS = QCoreApplication.translate("TranslatableConfigStrings", "Boundary segments should not be longer than {}m.").format(too_long_tolerance)
        self.CHECK_OVERLAPS_IN_BOUNDARIES = QCoreApplication.translate("TranslatableConfigStrings", "Boundaries should not overlap")
        self.CHECK_BOUNDARIES_ARE_NOT_SPLIT = QCoreApplication.translate("TranslatableConfigStrings", "Boundaries should not be split")
        self.CHECK_BOUNDARIES_COVERED_BY_PLOTS = QCoreApplication.translate("TranslatableConfigStrings", "Boundaries should be covered by Plots")
        self.CHECK_BOUNDARY_NODES_COVERED_BY_BOUNDARY_POINTS = QCoreApplication.translate("TranslatableConfigStrings", "Boundary nodes should be covered by Boundary Points")
        self.CHECK_DANGLES_IN_BOUNDARIES = QCoreApplication.translate("TranslatableConfigStrings", "Boundaries should not have dangles")
        self.CHECK_OVERLAPS_IN_PLOTS = QCoreApplication.translate("TranslatableConfigStrings", "Plots should not overlap")
        self.CHECK_OVERLAPS_IN_BUILDINGS = QCoreApplication.translate("TranslatableConfigStrings", "Buildings should not overlap")
        self.CHECK_OVERLAPS_IN_RIGHTS_OF_WAY = QCoreApplication.translate("TranslatableConfigStrings", "Rights of Way should not overlap")
        self.CHECK_PLOTS_COVERED_BY_BOUNDARIES = QCoreApplication.translate("TranslatableConfigStrings", "Plots should be covered by Boundaries")
        self.CHECK_RIGHT_OF_WAY_OVERLAPS_BUILDINGS = QCoreApplication.translate("TranslatableConfigStrings", "Right of Way should not overlap Buildings")
        self.CHECK_GAPS_IN_PLOTS = QCoreApplication.translate("TranslatableConfigStrings", "Plots should not have gaps")
        self.CHECK_MULTIPART_IN_RIGHT_OF_WAY = QCoreApplication.translate("TranslatableConfigStrings", "Right of Way should not have multipart geometries")

        # Specific topology errors
        self.CHECK_PLOT_NODES_COVERED_BY_BOUNDARY_POINTS = QCoreApplication.translate("TranslatableConfigStrings", "Plot nodes should be covered by boundary points")
        self.ERROR_PLOT_IS_NOT_COVERED_BY_BOUNDARY = QCoreApplication.translate("TranslatableConfigStrings", "Plot is not covered by boundary")
        self.ERROR_BOUNDARY_IS_NOT_COVERED_BY_PLOT = QCoreApplication.translate("TranslatableConfigStrings", "Boundary is not covered by plot")
        self.ERROR_NO_MORE_BOUNDARY_FACE_STRING_TABLE = QCoreApplication.translate("TranslatableConfigStrings", "Topological relationship between boundary and plot is not recorded in the {} table").format(MORE_BOUNDARY_FACE_STRING_TABLE)
        self.ERROR_DUPLICATE_MORE_BOUNDARY_FACE_STRING_TABLE = QCoreApplication.translate("TranslatableConfigStrings", "Topological relationship between boundary and plot is duplicated in the {} table").format(MORE_BOUNDARY_FACE_STRING_TABLE)
        self.ERROR_NO_LESS_TABLE = QCoreApplication.translate("TranslatableConfigStrings", "Topological relationship between boundary and plot is not recorded in the {} table").format(LESS_TABLE)
        self.ERROR_DUPLICATE_LESS_TABLE = QCoreApplication.translate("TranslatableConfigStrings", "Topological relationship between boundary and plot is duplicated in the {} table").format(LESS_TABLE)
        self.ERROR_NO_FOUND_POINT_BFS = QCoreApplication.translate("TranslatableConfigStrings", "Topological relationship between boundary point and boundary is not recorded in the {} table").format(POINT_BOUNDARY_FACE_STRING_TABLE)
        self.ERROR_DUPLICATE_POINT_BFS = QCoreApplication.translate("TranslatableConfigStrings", "Topological relationship between boundary point and boundary is duplicated in the {} table").format(POINT_BOUNDARY_FACE_STRING_TABLE)
        self.ERROR_BOUNDARY_POINT_IS_NOT_COVERED_BY_BOUNDARY_NODE = QCoreApplication.translate("TranslatableConfigStrings", "Boundary point is not covered by boundary node")
        self.ERROR_BOUNDARY_NODE_IS_NOT_COVERED_BY_BOUNDARY_POINT = QCoreApplication.translate("TranslatableConfigStrings", "Boundary node is not covered by boundary point")


translated_strings = TranslatableConfigStrings()
