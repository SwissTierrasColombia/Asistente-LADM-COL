DEFAULT_EPSG =  "3116"
DEFAULT_TOO_LONG_BOUNDARY_SEGMENTS_TOLERANCE = 200 # meters
ERROR_LAYER_GROUP = "Validation errors"
HELP_URL = "https://agenciaimplementacion.github.io/Asistente-LADM_COL"
MODULE_HELP_MAPPING = {
    '' : 'index.html', # default module is '', just go to index.html
    'add_points':'cadas/Spatial_Unit.html#add-points',
    'define_boundaries':'cadas/Spatial_Unit.html#define-boundaries',
    'create_plot':'cadas/Spatial_Unit.html#create-plot',
    'legal_party' : 'cadas/Party.html#legal-party',
    'natural_party' : 'cadas/Party.html#natural-party'
}
PLUGIN_NAME = "Asistente LADM_COL"

# Configure Project Generator Dependency
PROJECT_GENERATOR_MIN_REQUIRED_VERSION = "3.0.5"

# If Asistente LADM_COL depends on a specific version of Project Generator
#  (and only on that one), set to True
PROJECT_GENERATOR_EXACT_REQUIRED_VERSION = True

# If Asistente LADM_COL depends on a specific version of Project Generator
#  (and only on that one), and it is not the latest release, then you can
#  specify a download URL. If that's not the case, pass an empty string below
PROJECT_GENERATOR_REQUIRED_VERSION_URL = 'https://plugins.qgis.org/plugins/projectgenerator/version/3.0.5/download/'

TEST_SERVER = "www.google.com"
