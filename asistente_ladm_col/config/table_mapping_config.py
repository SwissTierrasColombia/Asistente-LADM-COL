from qgis.core import NULL

"""
CADASTRE MAPPING
"""
ADMINISTRATIVE_SOURCE_TABLE = "col_fuenteadministrativa"
ADMINISTRATIVE_SOURCE_TYPE_TABLE = "col_fuenteadministrativatipo"
AVAILABILITY_STATE_TABLE = "col_estadodisponibilidadtipo"
POINT_BFS_TABLE_BOUNDARY_FIELD = "ccl_lindero"
BFS_TABLE_BOUNDARY_POINT_FIELD = "punto_puntolindero"
BOUNDARY_POINT_TABLE = "puntolindero"
BOUNDARY_TABLE = "lindero"
BUILDING_TABLE = "construccion"
BUILDING_UNIT_TABLE = "unidadconstruccion"
BUSINESS_NAME_FIELD = "razon_social"
CCLSOURCE_TABLE = "cclfuente"
CCLSOURCE_TABLE_BOUNDARY_FIELD = "ccl_lindero"
CCLSOURCE_TABLE_SOURCE_FIELD = "lfuente"
COL_PARTY_NAME_FIELD = "nombre"
COL_PARTY_TABLE = "col_interesado"
CONTROL_POINT_TABLE = "puntocontrol"
DEPARTMENT_FIELD = "departamento"
DOCUMENT_ID_FIELD = "documento_identidad"
DOMAIN_KEY_FIELD = {
    "pg": "ilicode",
    "gpkg": "iliCode"
}
EXTFILE_TABLE = "extarchivo"
EXTFILE_DATA_FIELD = "datos"
FIRST_NAME_FIELD = "primer_nombre"
FIRST_SURNAME_FIELD = "primer_apellido"
FMI_FIELD = "fmi"
FRACTION_TABLE = "fraccion"
FRACTION_DENOMINATOR_FIELD = "denominador"
FRACTION_MEMBER_FIELD = "miembros_participacion"
FRACTION_NUMERATOR_FIELD = "numerador"
GENDER_TYPE_TABLE = "col_generotipo"
ID_FIELD = "t_id"
LA_GROUP_PARTY_TABLE = "la_agrupacion_interesados"
LA_GROUP_PARTY_NAME_FIELD = "nombre"
LA_GROUP_PARTY_GPTYPE_FIELD = "ai_tipo"
LA_GROUP_PARTY_TYPE_FIELD = "tipo"
LA_GROUP_PARTY_TYPE_TABLE = "col_grupointeresadotipo"
LA_GROUP_PARTY_TYPE_VALUE = "Otro"
LA_BAUNIT_NAME_FIELD = "nombre"
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
LESS_TABLE = "menos"
LESS_TABLE_BOUNDARY_FIELD = "ccl_lindero"
LESS_TABLE_PLOT_FIELD = "eu_terreno"
LOCAL_ID_FIELD = "_local_id"
MEMBERS_GROUP_PARTY_FIELD = "agrupacion"
MEMBERS_PARTY_FIELD = "interesados_col_interesado"
MEMBERS_TABLE = "miembros"
MORE_BOUNDARY_FACE_STRING_TABLE = "masccl"
MOREBFS_TABLE_BOUNDARY_FIELD = "cclp_lindero"
MOREBFS_TABLE_PLOT_FIELD = "uep_terreno"
MUNICIPALITY_FIELD = "municipio"
NAMESPACE_FIELD = "_espacio_de_nombres"
NIT_NUMBER_FIELD = "numero_nit"
NUMBER_OF_FLOORS = "numero_pisos"
NUPRE_FIELD = "nupre"
PARCEL_NAME_FIELD = "nombre"
PARCEL_TABLE = "predio"
PARTY_DOCUMENT_TYPE_TABLE = "col_interesadodocumentotipo"
PARTY_TYPE_TABLE = "la_interesadotipo"
PLOT_TABLE = "terreno"
POINT_AGREEMENT_TYPE_TABLE = "col_acuerdotipo"
POINT_BOUNDARY_FACE_STRING_TABLE = "puntoccl"
POINT_DESCRIPTION_TYPE_TABLE = "col_descripcionpuntotipo"
POINT_DEFINITION_TYPE_TABLE = "col_defpuntotipo"
POINT_INTERPOLATION_TYPE_TABLE = "col_interpolaciontipo"
POINT_MONUMENTATION_TYPE_TABLE = "col_monumentaciontipo"
POINTSOURCE_TABLE = "puntofuente"
POINTSOURCE_TABLE_BOUNDARYPOINT_FIELD = "punto_puntolindero"
POINTSOURCE_TABLE_SURVEYPOINT_FIELD = "punto_puntolevantamiento"
POINTSOURCE_TABLE_CONTROLPOINT_FIELD = "punto_puntocontrol"
POINTSOURCE_TABLE_SOURCE_FIELD = "pfuente"
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
RIGHT_OF_WAY_TABLE="servidumbrepaso"
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
UEBAUNIT_TABLE_BUILDING_FIELD = "ue_construccion"
UEBAUNIT_TABLE_BUILDING_UNIT_FIELD = "ue_unidadconstruccion"
UEBAUNIT_TABLE_PARCEL_FIELD = "baunit_predio"
UEBAUNIT_TABLE_PLOT_FIELD = "ue_terreno"
UEBAUNIT_TABLE_RIGHT_OF_WAY_FIELD = "ue_servidumbrepaso"
UESOURCE_TABLE = "uefuente"
UESOURCE_TABLE_PLOT_FIELD = "ue_terreno"
UESOURCE_TABLE_SOURCE_FIELD = "pfuente"
VIDA_UTIL_FIELD = "comienzo_vida_util_version"
ZONE_FIELD = "zona"

"""
PROPERTY RECORD CARD MAPPING
"""
PROPERTY_RECORD_CARD_TABLE = "predio_ficha"
PRC_PUBLIC_PARCEL_TYPE_FIELD = "tipo_predio_publico"
PRC_PARCEL_TYPE_FIELD = "predio_tipo"
MARKET_RESEARCH_TABLE = "investigacionmercado"
NUCLEAR_FAMILY_TABLE = "nucleofamiliar"
NATURAL_PARTY_TABLE = "interesado_natural"
LEGAL_PARTY_TABLE = "interesado_juridico"

"""
PROPERTY PARCEL TABLE
"""
PARCEL_TYPE_FIELD = "tipo"
PARCEL_TYPE_PH_OPTION = "PropiedadHorizontal.UnidadPredial"


NAMESPACE_PREFIX = {
    ADMINISTRATIVE_SOURCE_TABLE: 's',
    BOUNDARY_POINT_TABLE: 'p',
    BOUNDARY_TABLE: 'ccl',
    BUILDING_TABLE: 'su',
    BUILDING_UNIT_TABLE: 'su',
    COL_PARTY_TABLE: 'p',
    CONTROL_POINT_TABLE: 'p',
    EXTFILE_TABLE: 's',
    LA_GROUP_PARTY_TABLE: 'p',
    PARCEL_TABLE: 'u',
    PLOT_TABLE: 'su',
    RESPONSIBILITY_TABLE: 'r',
    RESTRICTION_TABLE: 'r',
    RIGHT_OF_WAY_TABLE: 'su',
    RIGHT_TABLE: 'r',
    SPATIAL_SOURCE_TABLE: 's',
    SURVEY_POINT_TABLE: 'p'
}

DICT_AUTOMATIC_VALUES = {
    BOUNDARY_TABLE: [{LENGTH_FIELD_BOUNDARY_TABLE: "$length"}],
    COL_PARTY_TABLE: [{COL_PARTY_NAME_FIELD: "regexp_replace(regexp_replace(regexp_replace(concat({}, ' ', {}, ' ', {}, ' ', {}, ' ', {}, ' ', {}), '\\\\s+', ' '), '^\\\\s+', ''), '\\\\s+$', '')".format(
        DOCUMENT_ID_FIELD,
        FIRST_SURNAME_FIELD,
        SECOND_SURNAME_FIELD,
        FIRST_NAME_FIELD,
        SECOND_NAME_FIELD,
        BUSINESS_NAME_FIELD)}],
    PARCEL_TABLE: [{DEPARTMENT_FIELD: 'substr("numero_predial", 0, 2)'},
                   {MUNICIPALITY_FIELD: 'substr("numero_predial", 3, 3)'},
                   {ZONE_FIELD: 'substr("numero_predial", 6, 2)'}]
}

DICT_DISPLAY_EXPRESSIONS = {
    COL_PARTY_TABLE: "regexp_replace(regexp_replace(regexp_replace(concat({}, ' ', {}, ' ', {}, ' ', {}, ' ', {}, ' ', {}), '\\\\s+', ' '), '^\\\\s+', ''), '\\\\s+$', '')".format(
        DOCUMENT_ID_FIELD,
        FIRST_SURNAME_FIELD,
        SECOND_SURNAME_FIELD,
        FIRST_NAME_FIELD,
        SECOND_NAME_FIELD,
        BUSINESS_NAME_FIELD),
    PARCEL_TABLE: "concat({}, ' ', {}, ' ', {})".format(NUPRE_FIELD, FMI_FIELD, PARCEL_NAME_FIELD),
    LA_BAUNIT_TABLE: "{} || ' ' || {} || ' ' || {}".format(ID_FIELD, LA_BAUNIT_NAME_FIELD, TYPE_FIELD),
    LA_GROUP_PARTY_TABLE: "{} || ' ' || {}".format(ID_FIELD, LA_GROUP_PARTY_NAME_FIELD),
    BUILDING_TABLE: '"{}{}"  || \' \' ||  "{}"'.format(NAMESPACE_PREFIX[BUILDING_UNIT_TABLE],
                                                                    NAMESPACE_FIELD,
                                                                    ID_FIELD)
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

LAYER_CONSTRAINTS = {
    PROPERTY_RECORD_CARD_TABLE: {
        PRC_PUBLIC_PARCEL_TYPE_FIELD: {
            'expression': 'CASE WHEN "{prc_ptf}" IS NOT NULL THEN\n(strpos("{prc_ptf}", \'Privado.\') != 0 AND "{prc_pptf}" IS NULL) OR (strpos("{prc_ptf}", \'Publico.\') != 0 AND "{prc_pptf}" IS NOT NULL)\nELSE True\nEND'.format(prc_ptf=PRC_PARCEL_TYPE_FIELD, prc_pptf=PRC_PUBLIC_PARCEL_TYPE_FIELD),
            'description': 'Si el tipo de predio es Público, debes elegir un valor de este listado; pero si el tipo de predio es Privado, no debes seleccionar ningún valor de este listado.'
        }
    },
    PARCEL_TABLE: {
        PARCEL_TYPE_FIELD: {
            'expression': 'CASE\n'
                          'WHEN "{parcel_type}" IS NOT NULL AND num_selected(\'{layer}\') > 0 THEN \n("{parcel_type}" = \'PropiedadHorizontal.UnidadPredial\')\n'
                          'WHEN "{parcel_type}" IS NOT NULL AND num_selected(\'{layer}\') = 0 THEN \n("{parcel_type}" != \'PropiedadHorizontal.UnidadPredial\')\n'
                          'ELSE True\n'
                          'END'.format(parcel_type=PARCEL_TYPE_FIELD, layer=BUILDING_UNIT_TABLE),
            'description': 'Si el tipo de predio es Propiedad Horizontal, debes elegir únicamente la opción {parcel_type_field}; en otro caso puedes seleccionar cualquier otra opción del listado.'.format(parcel_type_field=PARCEL_TYPE_PH_OPTION)
        }
    }
}

"""
Do not use the same before attribute for 2 differente groups. The same applies
to after attribute.

Leave before_attr/after_attr empty to add the group at the end of the form.
"""
FORM_GROUPS = {
    PROPERTY_RECORD_CARD_TABLE: {
        'Código Predial Nacional': {
            'show_label': True,
            'column_count': 1,
            'attr_list': ['sector', 'barrio', 'localidad_comuna', 'manzana_vereda', 'terreno', 'condicion_propiedad', 'edificio', 'piso', 'unidad'],
            'visibility_expression': None,
            'before_attr': 'estado_nupre',
            'after_attr': None
        },
        'Tipo predio público': {
            'show_label': False,
            'column_count':  1,
            'attr_list':  ['tipo_predio_publico'],
            'visibility_expression': '"predio_tipo" IS NOT NULL AND strpos("predio_tipo", \'Publico.\') != 0',
            'before_attr': None,
            'after_attr': 'predio_tipo'
        }
    }
}
