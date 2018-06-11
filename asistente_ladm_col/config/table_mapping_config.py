from qgis.core import NULL

ADMINISTRATIVE_SOURCE_TABLE = "col_fuenteadministrativa"
ADMINISTRATIVE_SOURCE_TYPE_TABLE = "col_fuenteadministrativatipo"
AVAILABILITY_STATE_TABLE = "col_estadodisponibilidadtipo"
BFS_TABLE_BOUNDARY_FIELD = "ccl_lindero"
BFS_TABLE_BOUNDARY_POINT_FIELD = "punto_puntolindero"
BOUNDARY_POINT_TABLE = "puntolindero"
BOUNDARY_TABLE = "lindero"
BUILDING_TABLE = "construccion"
BUILDING_UNIT_TABLE = "unidadconstruccion"
BUSINESS_NAME_FIELD = "razon_social"
CONTROL_POINT_TABLE = "puntocontrol"
DOCUMENT_ID_FIELD = "documento_identidad"
EXTFILE_TABLE = "extarchivo"
EXTFILE_DATA_FIELD = "datos"
FIRST_NAME_FIELD = "primer_nombre"
FIRST_SURNAME_FIELD = "primer_apellido"
FMI_FIELD = "fmi"
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
NAME_FIELD = "nombre"
NAMESPACE_FIELD = "_espacio_de_nombres"
NATURAL_PARTY_TABLE = "interesado_natural"
NIT_NUMBER_FIELD = "numero_nit"
NUMBER_OF_FLOORS = "numero_pisos"
NUPRE_FIELD = "nupre"
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
RRR_SOURCE_RELATION_TABLE = "rrrfuente"
RRR_SOURCE_RESPONSIBILITY_FIELD = "rrr_col_responsabilidad"
RRR_SOURCE_RESTRICTION_FIELD = "rrr_col_restriccion"
RRR_SOURCE_RIGHT_FIELD = "rrr_col_derecho"
RRR_SOURCE_SOURCE_FIELD = "rfuente"
RIGHT_TABLE = "col_derecho"
RIGHT_TYPE_TABLE = "col_derechotipo"
REFERENCE_POINT_FIELD = "punto_referencia"
SECOND_NAME_FIELD = "segundo_nombre"
SECOND_SURNAME_FIELD = "segundo_apellido"
SPATIAL_SOURCE_TABLE = "col_fuenteespacial"
SPATIAL_SOURCE_TYPE_TABLE = "col_fuenteespacialtipo"
SURVEY_POINT_TABLE = "puntolevantamiento"
SURVEY_POINT_TYPE_TABLE = "col_puntolevtipo"
TABLE_PROP_ASSOCIATION = "ASSOCIATION"
TABLE_PROP_DOMAIN = "ENUM"
TABLE_PROP_STRUCTURE = "STRUCTURE"
TYPE_BUILDING_TYPE_TABLE = "col_tipoconstrucciontipo"
TYPE_FIELD = "tipo"
UEBAUNIT_TABLE = "uebaunit"
UEBAUNIT_TABLE_PARCEL_FIELD = "baunit_predio"
UEBAUNIT_TABLE_PLOT_FIELD = "ue_terreno"
VIDA_UTIL_FIELD = "comienzo_vida_util_version"

NAMESPACE_PREFIX = {
    ADMINISTRATIVE_SOURCE_TABLE: 's',
    BOUNDARY_POINT_TABLE: 'p',
    BOUNDARY_TABLE: 'ccl',
    BUILDING_TABLE: 'su',
    BUILDING_UNIT_TABLE: 'su',
    CONTROL_POINT_TABLE: 'p',
    EXTFILE_TABLE: 's',
    LEGAL_PARTY_TABLE: 'p',
    SPATIAL_SOURCE_TABLE: 's',
    NATURAL_PARTY_TABLE: 'p',
    PARCEL_TABLE: 'u',
    PLOT_TABLE: 'su',
    RESPONSIBILITY_TABLE: 'r',
    RESTRICTION_TABLE: 'r',
    RIGHT_TABLE: 'r',
    SPATIAL_SOURCE_TABLE: 's',
    SURVEY_POINT_TABLE: 'p'
}

DICT_DISPLAY_EXPRESSIONS = {
    NATURAL_PARTY_TABLE: '{}+\' \'+{}+\' \'+{}+\' \'+{}+\' \'+{}'.format(DOCUMENT_ID_FIELD,
                                                                    FIRST_SURNAME_FIELD,
                                                                    SECOND_SURNAME_FIELD,
                                                                    FIRST_NAME_FIELD,
                                                                    SECOND_NAME_FIELD),
    LEGAL_PARTY_TABLE: '{}+\' \'+{}'.format(NIT_NUMBER_FIELD, BUSINESS_NAME_FIELD),
    PARCEL_TABLE: '{}+\' \'+{}+\' \'+{}'.format(NUPRE_FIELD, FMI_FIELD, NAME_FIELD),
    LA_BAUNIT_TABLE: '{}+\' \'+{}+\' \'+{}'.format(ID_FIELD, NAME_FIELD, TYPE_FIELD),
    LA_GROUP_PARTY_TABLE: '{}+\' \'+{}'.format(ID_FIELD, NAME_FIELD),
    BUILDING_TABLE: '"{}{}" + \' \' + "{}{}"'.format(NAMESPACE_PREFIX[BUILDING_UNIT_TABLE],
                                                                    NAMESPACE_FIELD,
                                                                    NAMESPACE_PREFIX[BUILDING_UNIT_TABLE],
                                                                    LOCAL_ID_FIELD)
}

LAYER_VARIABLES = {
    BUILDING_TABLE: {
        "qgis_25d_angle": 90,
        "qgis_25d_height": 1
    },
    BUILDING_UNIT_TABLE: {
        "qgis_25d_angle": 90,
        "qgis_25d_height": '"{}" * 2.5'.format(NUMBER_OF_FLOORS)
    }
}

CUSTOM_WIDGET_CONFIGURATION = {
    EXTFILE_TABLE: {
        'type': 'ExternalResource',
        'config': {
            'PropertyCollection': {
                'properties': {},
                'name': NULL,
                'type': 'collection'
            },
            'UseLink': True,
            'FullUrl': True,
            'FileWidget': True,
            'DocumentViewer': 0,
            'RelativeStorage': 0,
            'StorageMode': 0,
            'FileWidgetButton': True,
            'DocumentViewerHeight': 0,
            'DocumentViewerWidth': 0,
            'FileWidgetFilter': ''
        }
    }
}
