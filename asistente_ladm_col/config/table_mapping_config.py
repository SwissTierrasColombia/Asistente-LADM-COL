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
BUILDING_AREA_FIELD = "area_construccion"
BUILDING_VALUATION_FIELD = "avaluo_construccion"
BUILDING_UNIT_AREA_FIELD = "area_construida"
BUILDING_UNIT_PRIVATE_AREA_FIELD = "area_privada_construida"
BUILDING_UNIT_VALUATION_FIELD = "avaluo_unidad_construccion"
BUILDING_UNIT_TABLE = "unidadconstruccion"
BUSINESS_NAME_FIELD = "razon_social"
CCLSOURCE_TABLE = "cclfuente"
CCLSOURCE_TABLE_BOUNDARY_FIELD = "ccl_lindero"
CCLSOURCE_TABLE_SOURCE_FIELD = "lfuente"
COL_PARTY_DOCUMENT_ID_FIELD = "documento_identidad"
COL_PARTY_TABLE = "col_interesado"
COL_PARTY_TYPE_FIELD = "tipo"
COL_PARTY_DOC_TYPE_FIELD = "tipo_documento"
COL_PARTY_FIRST_NAME_FIELD = "primer_nombre"
COL_PARTY_SURNAME_FIELD = "primer_apellido"
COL_PARTY_BUSINESS_NAME_FIELD = "razon_social"
COL_PARTY_LEGAL_PARTY_FIELD = "tipo_interesado_juridico"
COL_PARTY_NAME_FIELD = "nombre"
COL_RESTRICTION_TYPE_RIGHT_OF_WAY_VALUE = "Servidumbre"
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
PARCEL_NUMBER_FIELD = "numero_predial"
PARCEL_NUMBER_BEFORE_FIELD = "numero_predial_anterior"
PARCEL_TABLE = "predio"
PARCEL_TYPE_FIELD = "tipo"
PARCEL_TYPE_PH_OPTION = "PropiedadHorizontal.UnidadPredial"
PARCEL_VALUATION_FIELD = "avaluo_predio"
PARTY_DOCUMENT_TYPE_TABLE = "col_interesadodocumentotipo"
PARTY_TYPE_TABLE = "la_interesadotipo"
PLOT_TABLE = "terreno"
PLOT_CALCULATED_AREA_FIELD = "area_calculada"
PLOT_VALUATION_FIELD = "avaluo_terreno"
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
RESTRICTION_TABLE_DESCRIPTION_FIELD = "descripcion"
RESTRICTION_TABLE = "col_restriccion"
RESTRICTION_TABLE_PARCEL_FIELD = "unidad_predio"
RESTRICTION_TYPE_TABLE = "col_restricciontipo"
RRR_SOURCE_RELATION_TABLE = "rrrfuente"
RRR_SOURCE_RESPONSIBILITY_FIELD = "rrr_col_responsabilidad"
RRR_SOURCE_RESTRICTION_FIELD = "rrr_col_restriccion"
RRR_SOURCE_RIGHT_FIELD = "rrr_col_derecho"
RRR_SOURCE_SOURCE_FIELD = "rfuente"
RIGHT_TABLE = "col_derecho"
RIGHT_TYPE_TABLE = "col_derechotipo"
RIGHT_OF_WAY_TABLE="servidumbrepaso"
RIGHT_OF_WAY_TABLE_IDENTIFICATOR_FIELD = "identificador"
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
VALUATION MAPPING
"""
AVALUOUNIDADCONSTRUCCION_TABLE = "avaluounidadconstruccion"
AVALUOUNIDADCONSTRUCCION_TABLE_BUILDING_UNIT_VALUATION_FIELD = "aucons"
AVALUOUNIDADCONSTRUCCION_TABLE_BUILDING_UNIT_FIELD = "ucons"
VALUATION_PARCEL_TABLE = "avaluos_v2_2_1avaluos_predio"
VALUATION_HORIZONTAL_PROPERTY_TABLE = "predio_matriz_ph"
VALUATION_COMMON_EQUIPMENT_TABLE = "equipamiento_comunal"
VALUATION_BUILDING_TABLE = "avaluos_v2_2_1avaluos_construccion"
VALUATION_BUILDING_UNIT_TABLE = "unidad_construccion"
VALUATION_BUILDING_UNIT_QUALIFICATION_NO_CONVENTIONAL_TABLE = "calificacion_no_convencional"
VALUATION_BUILDING_UNIT_QUALIFICATION_CONVENTIONAL_TABLE = "calificacion_convencional"
VALUATION_GEOECONOMIC_ZONE_TABLE = "zona_homogenea_geoeconomica"
VALUATION_PHYSICAL_ZONE_TABLE = "zona_homogenea_fisica"

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
    LA_GROUP_PARTY_TABLE: "concat({}, ' ', {})".format(ID_FIELD, LA_GROUP_PARTY_NAME_FIELD),
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
            'expression': """
                            CASE 
                                WHEN  "{parcel_type}" =  'NPH' THEN
                                    num_selected('{plot_layer}') = 1 AND num_selected('{building_unit_layer}') = 0
                                WHEN  "{parcel_type}" IN  ('PropiedadHorizontal.Matriz', 'Condominio.Matriz', 'ParqueCementerio.Matriz', 'BienUsoPublico', 'Condominio.UnidadPredial') THEN
                                    num_selected('{plot_layer}') = 1 AND num_selected('{building_unit_layer}') = 0
                                WHEN  "{parcel_type}" IN  ('Via', 'ParqueCementerio.UnidadPrivada') THEN
                                    num_selected('{plot_layer}') = 1 AND num_selected('{building_unit_layer}') = 0 AND num_selected('{building_layer}') = 0
                                WHEN  "{parcel_type}" =   'PropiedadHorizontal.UnidadPredial' THEN
                                    num_selected('{plot_layer}') = 0 AND num_selected('{building_unit_layer}') != 0 AND num_selected('{building_layer}') = 0
                                WHEN  "{parcel_type}" =  'Mejora' THEN
                                    num_selected('{plot_layer}') = 0 AND num_selected('{building_unit_layer}') = 0 AND num_selected('{building_layer}') = 1
                                ELSE
                                    TRUE
                            END""".format(parcel_type=PARCEL_TYPE_FIELD, plot_layer=PLOT_TABLE, building_layer=BUILDING_TABLE, building_unit_layer=BUILDING_UNIT_TABLE),
            'description': 'La parcela debe tener una o varias unidades espaciales asociadas. Verifique las reglas ' #''Parcel must have one or more spatial units associated with it. Check the rules.'
        },
        PARCEL_NUMBER_FIELD: {
            'expression': """CASE
                                WHEN  "{parcel_number}" IS NOT NULL THEN
                                    CASE
                                        WHEN length("{parcel_number}") != 30 OR regexp_match(to_string("{parcel_number}"), '^[0-9]*$') = 0  THEN
                                            FALSE
                                        WHEN "{parcel_type}" = 'NPH' THEN
                                            substr("{parcel_number}", 22,1) = 0 
                                        WHEN strpos( "{parcel_type}", 'PropiedadHorizontal.') != 0 THEN
                                            substr("{parcel_number}", 22,1) = 9
                                        WHEN strpos( "{parcel_type}", 'Condominio.') != 0 THEN
                                            substr("{parcel_number}", 22,1) = 8
                                        WHEN strpos("{parcel_type}", 'ParqueCementerio.') != 0 THEN
                                            substr("{parcel_number}", 22,1) = 7
                                        WHEN "{parcel_type}" = 'Mejora' THEN
                                            substr("{parcel_number}", 22,1) = 5
                                        WHEN "{parcel_type}" = 'Via' THEN
                                            substr("{parcel_number}", 22,1) = 4
                                        WHEN "{parcel_type}" = 'BienUsoPublico' THEN
                                            substr("{parcel_number}", 22,1) = 3
                                        ELSE
                                            TRUE
                                    END
                                ELSE
                                    TRUE
                            END""".format(parcel_type=PARCEL_TYPE_FIELD, parcel_number=PARCEL_NUMBER_FIELD),
            'description': 'El campo debe tener 30 caracteres numéricos y la posición 22 debe coincidir con el tipo de predio.'
        }, PARCEL_NUMBER_BEFORE_FIELD: {
            'expression': """CASE
                                WHEN  "{parcel_number_before}" IS NULL THEN
                                    TRUE
                                WHEN length("{parcel_number_before}") != 20 OR regexp_match(to_string("{parcel_number_before}"), '^[0-9]*$') = 0 THEN
                                    FALSE
                                ELSE
                                    TRUE
                            END""".format(parcel_number_before=PARCEL_NUMBER_BEFORE_FIELD),
            'description': 'El campo debe tener 20 caracteres numéricos.'
        }, PARCEL_VALUATION_FIELD:{
            'expression': """
                            CASE
                                WHEN  "{parcel_valuation}" IS NULL THEN
                                    TRUE
                                WHEN  "{parcel_valuation}" = 0 THEN
                                    FALSE
                                ELSE
                                    TRUE
                            END""".format(parcel_valuation=PARCEL_VALUATION_FIELD),
            'description': 'El valor debe ser mayor a cero (0).'
        }
    },
    COL_PARTY_TABLE: {
        COL_PARTY_DOC_TYPE_FIELD: {
            'expression': """
                            CASE
                                WHEN  "{col_party_type}" = 'Persona_Natural' THEN
                                     "{col_party_doc_type}" !=  'NIT'
                                WHEN  "{col_party_type}" = 'Persona_No_Natural' THEN
                                     "{col_party_doc_type}" = 'NIT' OR "{col_party_doc_type}" = 'Secuencial_IGAC' OR "{col_party_doc_type}" = 'Secuencial_SNR' 
                                ELSE
                                    TRUE
                            END""".format(col_party_type=COL_PARTY_TYPE_FIELD, col_party_doc_type=COL_PARTY_DOC_TYPE_FIELD),
            'description': 'Si el tipo de interesado es "Persona Natural" entonces el tipo de documento debe ser diferente de \'NIT\'. Pero si el tipo de interesado es "Persona No Natural" entonces el tipo de documento debe ser \'NIT\' o \'Secuencial IGAC\' o \'Secuencial SNR\'. '
        }, COL_PARTY_FIRST_NAME_FIELD:{
            'expression': """
                        CASE
                            WHEN  "{col_party_type}" = 'Persona_Natural'  THEN
                                 "{col_party_first_name}" IS NOT NULL AND length(trim("{col_party_first_name}")) != 0
                            WHEN  "{col_party_type}" = 'Persona_No_Natural'  THEN
                                 "{col_party_first_name}" IS NULL
                            ELSE
                                TRUE
                        END""".format(col_party_type=COL_PARTY_TYPE_FIELD, col_party_first_name=COL_PARTY_FIRST_NAME_FIELD),
            'description': 'Si el tipo de interesado es "Persona Natural" este campo se debe diligenciar, si el tipo de interesado es "Persona No Natural" este campo debe ser NULL.'
        }, COL_PARTY_SURNAME_FIELD: {
            'expression': """
                CASE
                    WHEN  "{col_party_type}" = 'Persona_Natural' THEN
                         "{col_party_surname}" IS NOT NULL AND length(trim("{col_party_surname}")) != 0
                    WHEN  "{col_party_type}" = 'Persona_No_Natural' THEN
                         "{col_party_surname}" IS NULL
                    ELSE
                        TRUE
                END""".format(col_party_type=COL_PARTY_TYPE_FIELD, col_party_surname=COL_PARTY_SURNAME_FIELD),
            'description': 'Si el tipo de interesado es "Persona Natural" este campo se debe diligenciar, si el tipo de interesado es "Persona No Natural" este campo debe ser NULL.'
        }, COL_PARTY_BUSINESS_NAME_FIELD:{
            'expression': """
                            CASE
                                WHEN  "{col_party_type}" =  'Persona_No_Natural' THEN
                                     "{col_party_business_name}" IS NOT NULL AND  length(trim( "{col_party_business_name}")) != 0
                                WHEN  "{col_party_type}" =  'Persona_Natural' THEN
                                     "{col_party_business_name}" IS NULL
                                ELSE
                                    TRUE
                            END""".format(col_party_type=COL_PARTY_TYPE_FIELD, col_party_business_name=COL_PARTY_BUSINESS_NAME_FIELD),
            'description': 'Si el tipo de interesado es "Persona No Natural" este campo se debe diligenciar, si el tipo de interesado es "Persona Natural" este campo debe ser NULL.'

        }, COL_PARTY_LEGAL_PARTY_FIELD:{
            'expression': """
                            CASE
                                WHEN  "{col_party_type}" =  'Persona_No_Natural' THEN
                                     "{col_party_legal_party}" IS NOT NULL
                                WHEN  "{col_party_type}" =  'Persona_Natural' THEN
                                     "{col_party_legal_party}" IS NULL                                     
                                ELSE
                                    TRUE
                            END""".format(col_party_type=COL_PARTY_TYPE_FIELD, col_party_legal_party=COL_PARTY_LEGAL_PARTY_FIELD),
            'description': 'Si el tipo de interesado es "Persona No Natural" este campo se debe diligenciar, si el tipo de interesado es "Persona Natural" este campo debe ser NULL.'

        }, COL_PARTY_DOCUMENT_ID_FIELD:{
            'expression': """
                            CASE
                                WHEN  "{col_party_document_id}"  IS NULL THEN
                                    FALSE
                                WHEN length(trim("{col_party_document_id}")) = 0 THEN
                                    FALSE
                                ELSE
                                    TRUE
                            END""".format(col_party_document_id=COL_PARTY_DOCUMENT_ID_FIELD),
            'description': 'El campo es obligatorio.'

        }
    },
    PLOT_TABLE: {
        PLOT_CALCULATED_AREA_FIELD: {
            'expression': """
                            CASE
                                WHEN  "{plot_calculated_area}" IS NULL THEN
                                    FALSE
                                WHEN  "{plot_calculated_area}" = 0 THEN
                                    FALSE
                                ELSE
                                    TRUE
                            END""".format(plot_calculated_area = PLOT_CALCULATED_AREA_FIELD),
            'description': 'El valor debe ser mayor a cero (0).'
        }, PLOT_VALUATION_FIELD: {
            'expression': """
                            CASE
                                WHEN  "{plot_valuation_field}" IS NULL THEN
                                    FALSE
                                WHEN  "{plot_valuation_field}" = 0 THEN
                                    FALSE
                                ELSE
                                    TRUE
                            END""".format(plot_valuation_field = PLOT_VALUATION_FIELD),
            'description': 'El valor debe ser mayor a cero (0).'
        }
    },
    BUILDING_TABLE: {
        BUILDING_AREA_FIELD: {
            'expression': """
                    CASE
                        WHEN  "{building_area}" IS NULL THEN
                            TRUE
                        WHEN  "{building_area}" = 0 THEN
                            FALSE
                        ELSE
                            TRUE
                    END""".format(building_area=BUILDING_AREA_FIELD),
            'description': 'El valor debe ser mayor a cero (0).'
        }, BUILDING_VALUATION_FIELD: {
            'expression': """
                    CASE
                        WHEN  "{building_valuation_field}" IS NULL THEN
                            FALSE
                        WHEN  "{building_valuation_field}" = 0 THEN
                            FALSE
                        ELSE
                            TRUE
                    END""".format(building_valuation_field=BUILDING_VALUATION_FIELD),
            'description': 'El valor debe ser mayor a cero (0).'
        }
    },
    BUILDING_UNIT_TABLE: {
        BUILDING_UNIT_AREA_FIELD: {
            'expression': """
                    CASE
                        WHEN  "{building_unit_area}" IS NULL THEN
                            TRUE
                        WHEN  "{building_unit_area}" = 0 THEN
                            FALSE
                        ELSE
                            TRUE
                    END""".format(building_unit_area=BUILDING_UNIT_AREA_FIELD),
            'description': 'El valor debe ser mayor a cero (0).'
        }, BUILDING_UNIT_PRIVATE_AREA_FIELD: {
            'expression': """
                    CASE
                        WHEN  "{building_unit_private_area}" IS NULL THEN
                            TRUE
                        WHEN  "{building_unit_private_area}" = 0 THEN
                            FALSE
                        ELSE
                            TRUE
                    END""".format(building_unit_private_area=BUILDING_UNIT_PRIVATE_AREA_FIELD),
            'description': 'El valor debe ser mayor a cero (0).'
        }, BUILDING_UNIT_VALUATION_FIELD: {
            'expression': """
                    CASE
                        WHEN  "{building_unit_valuation_field}" IS NULL THEN
                            TRUE
                        WHEN  "{building_unit_valuation_field}" = 0 THEN
                            FALSE
                        ELSE
                            TRUE
                    END""".format(building_unit_valuation_field=BUILDING_UNIT_VALUATION_FIELD),
            'description': 'El valor debe ser mayor a cero (0).'
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
    },
    VALUATION_PARCEL_TABLE: {
        ' ': {
            'show_label': True,
            'column_count':  1,
            'attr_list':  ['num_balcones', 'num_terrazas', 'num_mezanines'],
            'visibility_expression': None,
            'before_attr': None,
            'after_attr': None
        },
        '  ': {
            'show_label': True,
            'column_count':  1,
            'attr_list':  ['frente', 'fondo'],
            'visibility_expression': None,
            'before_attr': None,
            'after_attr': 'comun_uso_exclusivo'
        }
        },
    VALUATION_HORIZONTAL_PROPERTY_TABLE: {
        '': {
            'show_label': True,
            'column_count': 1,
            'attr_list': ['tipologia_constructiva_copropiedad', 'anio_construccion_etapa',
                          'estado_conservacion_copropiedad', 'materiales_construccion_areas_comunes',
                          'disenio_funcionalidad_copropiedad'],
            'visibility_expression': None,
            'before_attr': None,
            'after_attr': None
        },
        ' ': {
            'show_label': True,
            'column_count': 1,
            'attr_list': ['num_etapas', 'num_interiores', 'num_torres', 'num_pisos_por_torre', 'num_unidades_privadas',
                          'num_sotanos'],
            'visibility_expression': None,
            'before_attr': None,
            'after_attr': None
        }
    },
    VALUATION_BUILDING_UNIT_TABLE: {
        '': {
            'show_label': True,
            'column_count': 1,
            'attr_list': ['num_habitaciones', 'num_banios', 'num_cocinas', 'num_oficinas', 'num_estudios',
                          'num_bodegas', 'num_locales', 'num_salas', 'num_comedores'],
            'visibility_expression': None,
            'before_attr': None,
            'after_attr': None
        },
        ' ': {
            'show_label': True,
            'column_count': 1,
            'attr_list': ['anio_construction', 'uso', 'destino_econo', 'puntuacion', 'tipologia',
                          'estado_conservacion', 'construccion_tipo'],
            'visibility_expression': None,
            'before_attr': None,
            'after_attr': None
        },
    },
    VALUATION_BUILDING_UNIT_QUALIFICATION_CONVENTIONAL_TABLE: {
        ' ': {
            'show_label': True,
            'column_count': 1,
            'attr_list': ['sub_total_estructura', 'sub_total_acabados', 'sub_total_banio', 'sub_total_cocina',
                          'total_residencial_y_comercial', 'total_industrial'],
            'visibility_expression': None,
            'before_attr': None,
            'after_attr': None
        },
        '  ': {
            'show_label': True,
            'column_count': 1,
            'attr_list': ['armazon', 'muros', 'cubierta', 'conservacion_estructura', 'fachada', 'cubrimiento_muros',
                          'piso', 'conservacion_acabados', 'tamanio_banio', 'enchape_banio', 'mobiliario_banio',
                          'conservacion_banio', 'tamanio_cocina', 'enchape_cocina', 'mobiliario_cocina',
                          'conservacion_cocina', 'cerchas'],
            'visibility_expression': None,
            'before_attr': ' ',
            'after_attr': None
        },
        '   ': {
            'show_label': True,
            'column_count': 1,
            'attr_list': ['puntos_armazon', 'puntos_muro', 'puntos_cubierta', 'puntos_estructura_conservacion',
                          'puntos_fachada', 'puntos_cubrimiento_muros', 'puntos_piso', 'puntos_conservacion_acabados',
                          'puntos_tamanio_banio', 'puntos_enchape_banio', 'puntos_mobiliario_banio',
                          'puntos_conservacion_banio', 'puntos_tamanio_cocina', 'puntos_enchape_cocina',
                          'puntos_mobiliario_cocina', 'puntos_conservacion_cocina', 'puntos_cerchas'],
            'visibility_expression': None,
            'before_attr': '  ',
            'after_attr': None
        }
    }
}


"""
we define the minimum structure of a table to validate that there are no repeated records
"""
LOGIC_CONSISTENCY_TABLES = {
    # Geometric tables
    BOUNDARY_POINT_TABLE: ['acuerdo',
                           'definicion_punto',
                           'descripcion_punto',
                           'exactitud_vertical',
                           'exactitud_horizontal',
                           'confiabilidad',
                           'nombre_punto',
                           'posicion_interpolacion',
                           'monumentacion',
                           'puntotipo',
                           'localizacion_original'],
    SURVEY_POINT_TABLE: ['tipo_punto_levantamiento',
                         'definicion_punto',
                         'exactitud_vertical',
                         'exactitud_horizontal',
                         'nombre_punto',
                         'posicion_interpolacion',
                         'monumentacion',
                         'puntotipo',
                         'localizacion_original'],
    CONTROL_POINT_TABLE: ['nombre_punto',
                          'exactitud_vertical',
                          'exactitud_horizontal',
                          'tipo_punto_control',
                          'confiabilidad',
                          'posicion_interpolacion',
                          'monumentacion',
                          'puntotipo',
                          'localizacion_original'],
    BOUNDARY_TABLE: [LENGTH_FIELD_BOUNDARY_TABLE,
                     'localizacion_textual',
                     'geometria'],
    PLOT_TABLE: ['area_registral',
                 'area_calculada',
                 'avaluo_terreno',
                 'dimension',
                 'etiqueta',
                 'relacion_superficie',
                 'nivel',
                 'punto_referencia',
                 'poligono_creado'],
    BUILDING_TABLE: ['avaluo_construccion',
                     'area_construccion',
                     'tipo',
                     'dimension',
                     'etiqueta',
                     'relacion_superficie',
                     'nivel',
                     'punto_referencia',
                     'poligono_creado'],
    BUILDING_UNIT_TABLE: ['avaluo_unidad_construccion',
                          'numero_pisos',
                          'area_construida',
                          'area_privada_construida',
                          'construccion',
                          'tipo',
                          'dimension',
                          'etiqueta',
                          'relacion_superficie',
                          'nivel',
                          'punto_referencia',
                          'poligono_creado'],
    # Alphanumeric tables
    COL_PARTY_TABLE: ['documento_identidad',
                      'tipo_documento'],
    PARCEL_TABLE: ['departamento',
                   'municipio',
                   'zona',
                   'nupre',
                   'fmi',
                   'numero_predial',
                   'numero_predial_anterior',
                   'avaluo_predio',
                   'copropiedad',
                   'nombre',
                   'tipo'],
    RIGHT_TABLE: ['tipo',
                  'codigo_registral_derecho',
                  'descripcion',
                  'comprobacion_comparte',
                  'uso_efectivo',
                  'r_espacio_de_nombres',
                  'interesado_la_agrupacion_interesados',
                  'interesado_col_interesado',
                  'unidad_la_baunit',
                  'unidad_predio'],
    RESTRICTION_TABLE: ['interesado_requerido',
                        'tipo',
                        'codigo_registral_restriccion',
                        'descripcion',
                        'comprobacion_comparte',
                        'uso_efectivo',
                        'interesado_la_agrupacion_interesados',
                        'interesado_col_interesado',
                        'unidad_la_baunit',
                        'unidad_predio'],
    RESPONSIBILITY_TABLE: ['tipo',
                           'codigo_registral_responsabilidad',
                           'descripcion',
                           'comprobacion_comparte',
                           'uso_efectivo',
                           'interesado_la_agrupacion_interesados',
                           'interesado_col_interesado',
                           'unidad_la_baunit',
                           'unidad_predio'],
    ADMINISTRATIVE_SOURCE_TABLE: ['texto',
                                  'tipo',
                                  'codigo_registral_transaccion',
                                  'nombre',
                                  'fecha_aceptacion',
                                  'estado_disponibilidad',
                                  'sello_inicio_validez',
                                  'tipo_principal',
                                  'fecha_grabacion',
                                  'fecha_entrega',
                                  'oficialidad']
}
