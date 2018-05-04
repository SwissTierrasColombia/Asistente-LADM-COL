DEFAULT_EPSG =  "3116"
DEFAULT_TOO_LONG_BOUNDARY_SEGMENTS_TOLERANCE = 200 # meters
ERROR_LAYER_GROUP = "Validation errors"
HELP_URL = "https://agenciaimplementacion.github.io/Asistente-LADM_COL"
PLUGIN_NAME = "Asistente LADM_COL"

MODULE_HELP_MAPPING = {
    '' : 'index.html', # default module is '', just go to index.html
    'controlled_measurement': 'cadastre/Preprocessing.html#controlled-measurement',
    'create_admin_source': 'cadastre/Source.html#administrative-source',
    'create_parcel': 'cadastre/Basic_Administrative_Unit.html#parcel',
    'create_points': 'cadastre/Surveying_and_Representation.html#create-point',
    'create_boundaries': 'cadastre/Surveying_and_Representation.html#create-boundary',
    'create_plot': 'cadastre/Spatial_Unit.html#create-plot',
    'create_building': 'cadastre/Spatial_Unit.html#create-building',
    'create_spatial_source': 'cadastre/Source.html#spatial-source',
    'legal_party': 'cadastre/Party.html#legal-party',
    'load_layers': 'load_layers.html#load-layers',
    'natural_party': 'cadastre/Party.html#natural-party',
    'settings': 'help.html#settings'
}
# Configure Project Generator Dependency
PROJECT_GENERATOR_MIN_REQUIRED_VERSION = "3.0.7"

# If Asistente LADM_COL depends on a specific version of Project Generator
#  (and only on that one), set to True
PROJECT_GENERATOR_EXACT_REQUIRED_VERSION = False

# If Asistente LADM_COL depends on a specific version of Project Generator
#  (and only on that one), and it is not the latest release, then you can
#  specify a download URL. If that's not the case, pass an empty string below
PROJECT_GENERATOR_REQUIRED_VERSION_URL = ''

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

TEST_SERVER = "www.google.com"
