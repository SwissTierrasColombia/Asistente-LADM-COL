ADMINISTRATIVE_SOURCE_TABLE = "col_fuenteadministrativa"
ADMINISTRATIVE_SOURCE_TYPE_TABLE = "col_fuenteadministrativatipo"
AVAILABILITY_STATE_TABLE = "col_estadodisponibilidadtipo"
BFS_TABLE_BOUNDARY_FIELD = "ccl_lindero"
BFS_TABLE_BOUNDARY_POINT_FIELD = "punto_puntolindero"
BOUNDARY_POINT_TABLE = "puntolindero"
BOUNDARY_TABLE = "lindero"
CONSTRUCTION_TABLE = "construccion"
CONTROL_POINT_TABLE = "puntocontrol"
DEFAULT_EPSG = "3116"
DEFAULT_TOO_LONG_BOUNDARY_SEGMENTS_TOLERANCE = 200 # meters
ERROR_LAYER_GROUP = "Validation errors"
GENDER_TYPE_TABLE = "col_generotipo"
ID_FIELD = "t_id"
PARCEL_TABLE = "predio"
PLOT_TABLE = "terreno"
LA_BAUNIT_TYPE_TABLE = "la_baunittipo"
LENGTH_FIELD_BOUNDARY_TABLE = "longitud"
LEGAL_PARTY_TABLE = "interesado_juridico"
LEGAL_PARTY_TYPE_TABLE = "col_interesadojuridicotipo"
LESS_TABLE = "menos"
LESS_TABLE_BOUNDARY_FIELD = "ccl_lindero"
LESS_TABLE_PLOT_FIELD = "eu_terreno"
LOCAL_ID_FIELD = "_local_id"
MORE_BOUNDARY_FACE_STRING_TABLE = "masccl"
MOREBFS_TABLE_BOUNDARY_FIELD = "cclp_lindero"
MOREBFS_TABLE_PLOT_FIELD = "uep_terreno"
NAMESPACE_FIELD = "_espacio_de_nombres"
NATURAL_PARTY_TABLE = "interesado_natural"
PARTY_DOCUMENT_TYPE_TABLE = "col_interesadodocumentotipo"
PARTY_TYPE_TABLE = "la_interesadotipo"
POINT_BOUNDARY_FACE_STRING_TABLE = "puntoccl"
PROJECT_GENERATOR_MIN_REQUIRED_VERSION = "3.0.5"
SPATIAL_SOURCE_TABLE = "col_fuenteespacial"
SPATIAL_SOURCE_TYPE_TABLE = "col_fuenteespacialtipo"
SURVEY_POINT_TABLE = "puntolevantamiento"
TABLE_PROP_ASSOCIATION = "ASSOCIATION"
TABLE_PROP_DOMAIN = "ENUM"
TABLE_PROP_STRUCTURE = "STRUCTURE"
UEBAUNIT_TABLE = "uebaunit"
UEBAUNIT_TABLE_PARCEL_FIELD = "baunit_predio"
UEBAUNIT_TABLE_PLOT_FIELD = "ue_terreno"
VIDA_UTIL_FIELD = "comienzo_vida_util_version"
BUILDING_TABLE = "construccion"

NAMESPACE_PREFIX = {
    BOUNDARY_POINT_TABLE: 'p',
    SURVEY_POINT_TABLE: 'p',
    BOUNDARY_TABLE: 'ccl',
    PLOT_TABLE: 'su',
    CONSTRUCTION_TABLE: 'su',
    PARCEL_TABLE: 'u',
    NATURAL_PARTY_TABLE: 'p',
    LEGAL_PARTY_TABLE: 'p',
    ADMINISTRATIVE_SOURCE_TABLE: 's',
    SPATIAL_SOURCE_TABLE: 's'
}
