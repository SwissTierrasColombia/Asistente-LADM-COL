ADMINISTRATIVE_SOURCE_TABLE = "col_fuenteadministrativa"
ADMINISTRATIVE_SOURCE_TYPE_TABLE = "col_fuenteadministrativatipo"
AVAILABILITY_STATE_TABLE = "col_estadodisponibilidadtipo"
BFS_TABLE_BOUNDARY_FIELD = "ccl_lindero"
BFS_TABLE_BOUNDARY_POINT_FIELD = "punto_puntolindero"
BOUNDARY_POINT_TABLE = "puntolindero"
BOUNDARY_TABLE = "lindero"
BUILDING_TABLE = "construccion"
BUILDING_UNIT_TABLE = "unidadconstruccion"
CONTROL_POINT_TABLE = "puntocontrol"
GENDER_TYPE_TABLE = "col_generotipo"
LA_GROUP_PARTY_TABLE = "la_agrupacion_interesados"
ID_FIELD = "t_id"
PARCEL_TABLE = "predio"
PLOT_TABLE = "terreno"
LA_BAUNIT_TABLE = "la_baunit"
LA_BAUNIT_TYPE_TABLE = "la_baunittipo"
LA_DIMENSION_TYPE_TABLE = "la_dimensiontipo"
LA_BUILDING_UNIT_TYPE_TABLE = "la_unidadedificaciontipo"
LA_INTERPOLATION_TYPE_TABLE = "la_interpolaciontipo"
LA_MONUMENTATION_TYPE_TABLE = "la_monumentaciontipo"
LA_POINT_TABLE = "la_punto"
LA_POINT_TYPE_TABLE = "la_puntotipo"
LA_SURFACE_RELATION_TYPE_TABLE = "la_relacionsuperficietipo"
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
POINT_AGREEMENT_TYPE_TABLE = "col_acuerdotipo"
POINT_BOUNDARY_FACE_STRING_TABLE = "puntoccl"
PROJECT_GENERATOR_MIN_REQUIRED_VERSION = "3.0.0"
POINT_DESCRIPTION_TYPE_TABLE = "col_descripcionpuntotipo"
POINT_DEFINITION_TYPE_TABLE = "col_defpuntotipo"
POINT_INTERPOLATION_TYPE_TABLE = "col_interpolaciontipo"
POINT_MONUMENTATION_TYPE_TABLE = "col_monumentaciontipo"
RESPONSIBILITY_TABLE = "col_responsabilidad"
RESPONSIBILITY_TYPE_TABLE = "col_responsabilidadtipo"
RESTRICTION_TABLE = "col_restriccion"
RESTRICTION_TYPE_TABLE = "col_restricciontipo"
RIGHT_TABLE = "col_derecho"
RIGHT_TYPE_TABLE = "col_derechotipo"
REFERENCE_POINT_FIELD = "punto_referencia"
SPATIAL_SOURCE_TABLE = "col_fuenteespacial"
SPATIAL_SOURCE_TYPE_TABLE = "col_fuenteespacialtipo"
SURVEY_POINT_TABLE = "puntolevantamiento"
SURVEY_POINT_TYPE_TABLE = "col_puntolevtipo"
TABLE_PROP_ASSOCIATION = "ASSOCIATION"
TABLE_PROP_DOMAIN = "ENUM"
TABLE_PROP_STRUCTURE = "STRUCTURE"
TYPE_BUILDING_TYPE_TABLE = "col_tipoconstrucciontipo"
UEBAUNIT_TABLE = "uebaunit"
UEBAUNIT_TABLE_PARCEL_FIELD = "baunit_predio"
UEBAUNIT_TABLE_PLOT_FIELD = "ue_terreno"
VIDA_UTIL_FIELD = "comienzo_vida_util_version"

NAMESPACE_PREFIX = {
    BOUNDARY_POINT_TABLE: 'p',
    SURVEY_POINT_TABLE: 'p',
    BOUNDARY_TABLE: 'ccl',
    PLOT_TABLE: 'su',
    BUILDING_TABLE: 'su',
    BUILDING_UNIT_TABLE: 'su',
    PARCEL_TABLE: 'u',
    NATURAL_PARTY_TABLE: 'p',
    LEGAL_PARTY_TABLE: 'p',
    ADMINISTRATIVE_SOURCE_TABLE: 's',
    SPATIAL_SOURCE_TABLE: 's',
    RIGHT_TABLE: 'r'
}
