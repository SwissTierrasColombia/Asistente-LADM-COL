from qgis.core import QgsExpression
from asistente_ladm_col.logic.ladm_col.data.ladm_query_objects import (OwnField,
                                                                       DomainOwnField,
                                                                       EvalExprOwnField,
                                                                       RelateOwnFieldObject,
                                                                       RelateOwnFieldValue,
                                                                       RelateRemoteFieldValue,
                                                                       SpatialFilterSubLevel,
                                                                       FilterSubLevel)

from asistente_ladm_col.config.enums import SpatialOperationType
from asistente_ladm_col.config.mapping_config import QueryNames


def get_structure_property_record_card_query(names):
    query = {
        QueryNames.LEVEL_TABLE: {
            QueryNames.LEVEL_TABLE_NAME: names.OP_PLOT_T,
            QueryNames.LEVEL_TABLE_ALIAS: names.OP_PLOT_T,
            QueryNames.FILTER_SUB_LEVEL: FilterSubLevel(names.T_ID_F, names.OP_PLOT_T, names.T_ID_F),
            QueryNames.TABLE_FIELDS: [OwnField(names.OP_PLOT_T_PLOT_AREA_F, "Área terreno [m2]")],
            QueryNames.LEVEL_TABLE: {
                QueryNames.LEVEL_TABLE_NAME: names.OP_PARCEL_T,
                QueryNames.LEVEL_TABLE_ALIAS: names.OP_PARCEL_T,
                QueryNames.FILTER_SUB_LEVEL: FilterSubLevel(names.COL_UE_BAUNIT_T_PARCEL_F,
                                                            names.COL_UE_BAUNIT_T,
                                                            names.COL_UE_BAUNIT_T_OP_PLOT_F),
                QueryNames.TABLE_FIELDS: [
                    OwnField(names.COL_BAUNIT_T_NAME_F, "Nombre"),
                    OwnField(names.OP_PARCEL_T_DEPARTMENT_F, "Departamento"),
                    OwnField(names.OP_PARCEL_T_MUNICIPALITY_F, "Municipio"),
                    OwnField(names.OP_PARCEL_T_NUPRE_F, "NUPRE"),
                    OwnField(names.OP_PARCEL_T_FMI_F, "FMI"),
                    OwnField(names.OP_PARCEL_T_PARCEL_NUMBER_F, "Número predial"),
                    OwnField(names.OP_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F, "Número predial anterior"),
                    DomainOwnField(names.OP_PARCEL_T_TYPE_F, "Tipo", names.OP_PARCEL_TYPE_D)
                ]
            }
        }
    }

    return query


def get_structure_economic_query(names):
    query = {
        QueryNames.LEVEL_TABLE: {
            QueryNames.LEVEL_TABLE_NAME: names.OP_PLOT_T,
            QueryNames.LEVEL_TABLE_ALIAS: names.OP_PLOT_T,
            QueryNames.FILTER_SUB_LEVEL: FilterSubLevel(names.T_ID_F, names.OP_PLOT_T, names.T_ID_F),
            QueryNames.TABLE_FIELDS: [OwnField(names.OP_PLOT_T_PLOT_VALUATION_F, "Avalúo terreno [COP]"),
                                      OwnField(names.OP_PLOT_T_PLOT_AREA_F, "Área terreno [m2]")],
            QueryNames.LEVEL_TABLE: {
                QueryNames.LEVEL_TABLE_NAME: names.OP_PARCEL_T,
                QueryNames.LEVEL_TABLE_ALIAS: names.OP_PARCEL_T,
                QueryNames.FILTER_SUB_LEVEL: FilterSubLevel(names.COL_UE_BAUNIT_T_PARCEL_F,
                                                            names.COL_UE_BAUNIT_T,
                                                            names.COL_UE_BAUNIT_T_OP_PLOT_F),
                QueryNames.TABLE_FIELDS: [
                    OwnField(names.COL_BAUNIT_T_NAME_F, "Nombre"),
                    OwnField(names.OP_PARCEL_T_DEPARTMENT_F, "Departamento"),
                    OwnField(names.OP_PARCEL_T_MUNICIPALITY_F, "Municipio"),
                    OwnField(names.OP_PARCEL_T_NUPRE_F, "NUPRE"),
                    OwnField(names.OP_PARCEL_T_FMI_F, "FMI"),
                    OwnField(names.OP_PARCEL_T_PARCEL_NUMBER_F, "Número predial"),
                    OwnField(names.OP_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F, "Número predial anterior"),
                    OwnField(names.OP_PARCEL_T_VALUATION_F, "Ávaluo predio"),
                    DomainOwnField(names.OP_PARCEL_T_TYPE_F, "Tipo", names.OP_PARCEL_TYPE_D)
                ],
                QueryNames.LEVEL_TABLE: {
                    QueryNames.LEVEL_TABLE_NAME: names.OP_BUILDING_T,
                    QueryNames.LEVEL_TABLE_ALIAS: names.OP_BUILDING_T,
                    QueryNames.FILTER_SUB_LEVEL: FilterSubLevel(names.COL_UE_BAUNIT_T_OP_BUILDING_F,
                                                                names.COL_UE_BAUNIT_T,
                                                                names.COL_UE_BAUNIT_T_PARCEL_F),
                    QueryNames.TABLE_FIELDS: [
                        OwnField(names.OP_BUILDING_T_BUILDING_VALUATION_F, "Avalúo [COP]"),
                        OwnField(names.OP_BUILDING_T_BUILDING_AREA_F, "Área construcción")
                    ],
                    QueryNames.LEVEL_TABLE: {
                        QueryNames.LEVEL_TABLE_NAME: names.OP_BUILDING_UNIT_T,
                        QueryNames.LEVEL_TABLE_ALIAS: names.OP_BUILDING_UNIT_T,
                        QueryNames.FILTER_SUB_LEVEL: FilterSubLevel(names.T_ID_F, names.OP_BUILDING_UNIT_T,
                                                                    names.OP_BUILDING_UNIT_T_BUILDING_F),
                        QueryNames.TABLE_FIELDS: [
                            OwnField(names.OP_BUILDING_UNIT_T_BUILDING_VALUATION_F, "Avalúo"),
                            OwnField(names.OP_BUILDING_UNIT_T_BUILT_AREA_F, "Área construida [m2]"),
                            OwnField(names.OP_BUILDING_UNIT_T_BUILT_PRIVATE_AREA_F,
                                     "Área privada construida [m2]"),
                            OwnField(names.OP_BUILDING_UNIT_T_TOTAL_FLOORS_F, "Número de pisos"),
                            OwnField(names.OP_BUILDING_UNIT_T_FLOOR_F, "Ubicación en el piso"),
                            DomainOwnField(names.OP_BUILDING_UNIT_T_USE_F, "Uso",
                                           names.OP_BUILDING_UNIT_USE_D),
                            OwnField(names.OP_BUILDING_UNIT_T_YEAR_OF_BUILDING_F, "Año construcción")
                        ]
                    }
                }
            }
        }
    }

    return query


def get_structure_physical_query(names):
    op_spatial_source_fields = [
        DomainOwnField(names.COL_SPATIAL_SOURCE_T_TYPE_F, "Tipo de fuente espacial",
                       names.COL_SPATIAL_SOURCE_TYPE_D),
        DomainOwnField(names.COL_SOURCE_T_AVAILABILITY_STATUS_F, "Estado disponibilidad",
                       names.COL_AVAILABILITY_TYPE_D),
        DomainOwnField(names.COL_SOURCE_T_MAIN_TYPE_F, "Tipo principal", names.CI_CODE_PRESENTATION_FORM_D),
        OwnField(names.COL_SOURCE_T_DATE_DOCUMENT_F, "Fecha documento"),
        RelateOwnFieldValue('Archivo fuente', names.EXT_ARCHIVE_S,
                            OwnField(names.EXT_ARCHIVE_S_DATA_F, 'Archivo fuente'),
                            names.EXT_ARCHIVE_S_OP_SPATIAL_SOURCE_F)
    ]

    query = {
        QueryNames.LEVEL_TABLE: {
            QueryNames.LEVEL_TABLE_NAME: names.OP_PLOT_T,
            QueryNames.LEVEL_TABLE_ALIAS: names.OP_PLOT_T,
            QueryNames.FILTER_SUB_LEVEL: FilterSubLevel(names.T_ID_F, names.OP_PLOT_T, names.T_ID_F),
            QueryNames.TABLE_FIELDS: [OwnField(names.OP_PLOT_T_PLOT_AREA_F, "Área terreno [m2]")],
            '1' + QueryNames.LEVEL_TABLE: {
                QueryNames.LEVEL_TABLE_NAME: names.OP_PARCEL_T,
                QueryNames.LEVEL_TABLE_ALIAS: names.OP_PARCEL_T,
                QueryNames.FILTER_SUB_LEVEL: FilterSubLevel(names.COL_UE_BAUNIT_T_PARCEL_F,
                                                            names.COL_UE_BAUNIT_T,
                                                            names.COL_UE_BAUNIT_T_OP_PLOT_F),
                QueryNames.TABLE_FIELDS: [
                    OwnField(names.COL_BAUNIT_T_NAME_F, "Nombre"),
                    OwnField(names.OP_PARCEL_T_NUPRE_F, "NUPRE"),
                    OwnField(names.OP_PARCEL_T_FMI_F, "FMI"),
                    OwnField(names.OP_PARCEL_T_PARCEL_NUMBER_F, "Número predial"),
                    OwnField(names.OP_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F, "Número predial anterior")
                ],
                QueryNames.LEVEL_TABLE: {
                    QueryNames.LEVEL_TABLE_NAME: names.OP_BUILDING_T,
                    QueryNames.LEVEL_TABLE_ALIAS: names.OP_BUILDING_T,
                    QueryNames.FILTER_SUB_LEVEL: FilterSubLevel(names.COL_UE_BAUNIT_T_OP_BUILDING_F,
                                                                names.COL_UE_BAUNIT_T,
                                                                names.COL_UE_BAUNIT_T_PARCEL_F),
                    QueryNames.TABLE_FIELDS: [
                        OwnField(names.OP_BUILDING_T_BUILDING_AREA_F, "Área construcción"),
                        OwnField(names.OP_BUILDING_T_NUMBER_OF_FLOORS_F, "Número de pisos")
                    ],
                    '1' + QueryNames.LEVEL_TABLE: {
                        QueryNames.LEVEL_TABLE_NAME: names.OP_BUILDING_UNIT_T,
                        QueryNames.LEVEL_TABLE_ALIAS: names.OP_BUILDING_UNIT_T,
                        QueryNames.FILTER_SUB_LEVEL: FilterSubLevel(names.T_ID_F, names.OP_BUILDING_UNIT_T,
                                                                    names.OP_BUILDING_UNIT_T_BUILDING_F),
                        QueryNames.TABLE_FIELDS: [
                            OwnField(names.OP_BUILDING_UNIT_T_TOTAL_FLOORS_F, "Número de pisos"),
                            DomainOwnField(names.OP_BUILDING_UNIT_T_USE_F, "Uso",
                                           names.OP_BUILDING_UNIT_USE_D),
                            DomainOwnField(names.OP_BUILDING_UNIT_T_BUILDING_TYPE_F, "Tipo construcción",
                                           names.OP_BUILDING_TYPE_D),
                            DomainOwnField(names.OP_BUILDING_UNIT_T_BUILDING_UNIT_TYPE_F,
                                           "Tipo unidad de construcción", names.OP_BUILDING_UNIT_TYPE_D),
                            OwnField(names.OP_BUILDING_UNIT_T_BUILT_PRIVATE_AREA_F,
                                     "Área privada construida [m2]"),
                            OwnField(names.OP_BUILDING_UNIT_T_BUILT_AREA_F, "Área construida [m2]")
                        ],
                        QueryNames.LEVEL_TABLE: {
                            QueryNames.LEVEL_TABLE_NAME: names.OP_SPATIAL_SOURCE_T,
                            QueryNames.LEVEL_TABLE_ALIAS: names.OP_SPATIAL_SOURCE_T,
                            QueryNames.FILTER_SUB_LEVEL: FilterSubLevel(names.COL_UE_SOURCE_T_SOURCE_F,
                                                                        names.COL_UE_SOURCE_T,
                                                                        names.COL_UE_SOURCE_T_OP_BUILDING_UNIT_F),
                            QueryNames.TABLE_FIELDS: op_spatial_source_fields
                        }
                    },
                    '2' + QueryNames.LEVEL_TABLE: {
                        QueryNames.LEVEL_TABLE_NAME: names.OP_SPATIAL_SOURCE_T,
                        QueryNames.LEVEL_TABLE_ALIAS: names.OP_SPATIAL_SOURCE_T,
                        QueryNames.FILTER_SUB_LEVEL: FilterSubLevel(names.COL_UE_SOURCE_T_SOURCE_F,
                                                                    names.COL_UE_SOURCE_T,
                                                                    names.COL_UE_SOURCE_T_OP_BUILDING_F),
                        QueryNames.TABLE_FIELDS: op_spatial_source_fields
                    }
                }
            },
            '2' + QueryNames.LEVEL_TABLE: {
                QueryNames.LEVEL_TABLE_NAME: names.OP_BOUNDARY_T,
                QueryNames.LEVEL_TABLE_ALIAS: names.OP_BOUNDARY_T + " externos",
                QueryNames.FILTER_SUB_LEVEL: FilterSubLevel(names.MORE_BFS_T_OP_BOUNDARY_F,
                                                            names.MORE_BFS_T,
                                                            names.MORE_BFS_T_OP_PLOT_F),
                QueryNames.TABLE_FIELDS: [OwnField(names.OP_BOUNDARY_T_LENGTH_F, "Longitud [m]")]
            },
            '3' + QueryNames.LEVEL_TABLE: {
                QueryNames.LEVEL_TABLE_NAME: names.OP_BOUNDARY_POINT_T,
                QueryNames.LEVEL_TABLE_ALIAS: names.OP_BOUNDARY_POINT_T + " externos",
                QueryNames.FILTER_SUB_LEVEL: FilterSubLevel(names.MORE_BFS_T_OP_BOUNDARY_F,
                                                            names.MORE_BFS_T,
                                                            names.MORE_BFS_T_OP_PLOT_F,
                                                            FilterSubLevel(names.POINT_BFS_T_OP_BOUNDARY_POINT_F,
                                                                           names.POINT_BFS_T,
                                                                           names.POINT_BFS_T_OP_BOUNDARY_F)
                                                            ),
                QueryNames.TABLE_FIELDS: [
                    EvalExprOwnField("Coordenadas", QgsExpression("$x || ' ' || $y || ' ' || z($geometry)"))]
            },
            '4' + QueryNames.LEVEL_TABLE: {
                QueryNames.LEVEL_TABLE_NAME: names.OP_BOUNDARY_T,
                QueryNames.LEVEL_TABLE_ALIAS: names.OP_BOUNDARY_T + " internos",
                QueryNames.FILTER_SUB_LEVEL: FilterSubLevel(names.LESS_BFS_T_OP_BOUNDARY_F,
                                                            names.LESS_BFS_T,
                                                            names.LESS_BFS_T_OP_PLOT_F),
                QueryNames.TABLE_FIELDS: [OwnField(names.OP_BOUNDARY_T_LENGTH_F, "Longitud [m]")]
            },
            '5' + QueryNames.LEVEL_TABLE: {
                QueryNames.LEVEL_TABLE_NAME: names.OP_BOUNDARY_POINT_T,
                QueryNames.LEVEL_TABLE_ALIAS: names.OP_BOUNDARY_POINT_T + " internos",
                QueryNames.FILTER_SUB_LEVEL: FilterSubLevel(names.LESS_BFS_T_OP_BOUNDARY_F,
                                                            names.LESS_BFS_T,
                                                            names.LESS_BFS_T_OP_PLOT_F,
                                                            FilterSubLevel(names.POINT_BFS_T_OP_BOUNDARY_POINT_F,
                                                                           names.POINT_BFS_T,
                                                                           names.POINT_BFS_T_OP_BOUNDARY_F)
                                                            ),
                QueryNames.TABLE_FIELDS: [
                    EvalExprOwnField("Coordenadas", QgsExpression("$x || ' ' || $y || ' ' || z($geometry)"))]
            },
            '6' + QueryNames.LEVEL_TABLE: {
                QueryNames.LEVEL_TABLE_NAME: names.OP_SURVEY_POINT_T,
                QueryNames.LEVEL_TABLE_ALIAS: names.OP_SURVEY_POINT_T,
                QueryNames.FILTER_SUB_LEVEL: SpatialFilterSubLevel(names.T_ID_F, names.OP_SURVEY_POINT_T,
                                                                   names.OP_PLOT_T,
                                                                   SpatialOperationType.INTERSECTS_SPATIAL_OPERATION),
                QueryNames.TABLE_FIELDS: [
                    EvalExprOwnField("Coordenadas", QgsExpression("$x || ' ' || $y || ' ' || z($geometry)"))]
            },
            '7' + QueryNames.LEVEL_TABLE: {
                QueryNames.LEVEL_TABLE_NAME: names.OP_SPATIAL_SOURCE_T,
                QueryNames.LEVEL_TABLE_ALIAS: names.OP_SPATIAL_SOURCE_T,
                QueryNames.FILTER_SUB_LEVEL: FilterSubLevel(names.COL_UE_SOURCE_T_SOURCE_F,
                                                            names.COL_UE_SOURCE_T,
                                                            names.COL_UE_SOURCE_T_OP_PLOT_F),
                QueryNames.TABLE_FIELDS: op_spatial_source_fields
            }
        }
    }

    return query


def get_structure_legal_query(names):
    op_party_contact_fields = [
        OwnField(names.OP_PARTY_CONTACT_T_TELEPHONE_NUMBER_1_F, 'Teléfono 1'),
        OwnField(names.OP_PARTY_CONTACT_T_TELEPHONE_NUMBER_2_F, 'Teléfono 2'),
        OwnField(names.OP_PARTY_CONTACT_T_NOTIFICATION_ADDRESS_F, 'Domicilio notificación'),
        OwnField(names.OP_PARTY_CONTACT_T_EMAIL_F, 'Correo electrónico'),
        DomainOwnField(names.OP_PARTY_CONTACT_T_DATA_SOURCE_F, 'Origen de datos', names.OP_INSTITUTION_TYPE_D)
    ]

    op_administrative_source_fields = [
        DomainOwnField(names.OP_ADMINISTRATIVE_SOURCE_T_TYPE_F, "Tipo de fuente administrativa",
                       names.OP_ADMINISTRATIVE_SOURCE_TYPE_D),
        OwnField(names.OP_ADMINISTRATIVE_SOURCE_T_EMITTING_ENTITY_F, "Ente emisor"),
        DomainOwnField(names.COL_SOURCE_T_AVAILABILITY_STATUS_F, "Estado disponibilidad",
                       names.COL_AVAILABILITY_TYPE_D),
        RelateOwnFieldValue('Archivo fuente', names.EXT_ARCHIVE_S,
                            OwnField(names.EXT_ARCHIVE_S_DATA_F, 'Archivo fuente'),
                            names.EXT_ARCHIVE_S_OP_ADMINISTRATIVE_SOURCE_F)
    ]

    op_party_fields = [
        DomainOwnField(names.OP_PARTY_T_TYPE_F, "Tipo", names.OP_PARTY_TYPE_D),
        OwnField(names.OP_PARTY_T_DOCUMENT_ID_F, 'Cédula de ciudadanía'),
        OwnField(names.COL_PARTY_T_NAME_F, 'Nombre'),
        OwnField(names.OP_PARTY_T_GENRE_F, 'Género'),
        RelateOwnFieldObject(names.OP_PARTY_CONTACT_T, names.OP_PARTY_CONTACT_T, op_party_contact_fields,
                             names.OP_PARTY_CONTACT_T_OP_PARTY_F)
    ]

    op_group_party_party_fields = [
        DomainOwnField(names.OP_PARTY_T_TYPE_F, "Tipo", names.OP_PARTY_TYPE_D),
        OwnField(names.OP_PARTY_T_DOCUMENT_ID_F, 'Cédula de ciudadanía'),
        OwnField(names.COL_PARTY_T_NAME_F, 'Nombre'),
        OwnField(names.OP_PARTY_T_GENRE_F, 'Género'),
        RelateOwnFieldObject(names.OP_PARTY_CONTACT_T, names.OP_PARTY_CONTACT_T, op_party_contact_fields,
                             names.OP_PARTY_CONTACT_T_OP_PARTY_F),
        RelateRemoteFieldValue(names.FRACTION_S,
                               names.FRACTION_S,
                               EvalExprOwnField("fracción",
                                                QgsExpression(
                                                    "round({numerador}/{denominador} * 100, 3)".format(
                                                        denominador=names.FRACTION_S_DENOMINATOR_F,
                                                        numerador=names.FRACTION_S_NUMERATOR_F
                                                    ))),
                               names.FRACTION_S_MEMBER_F,
                               FilterSubLevel(names.T_ID_F, names.MEMBERS_T, names.MEMBERS_T_PARTY_F))
    ]

    op_group_party_fields = [
        DomainOwnField(names.COL_GROUP_PARTY_T_TYPE_F, "Tipo de agrupación de interesados",
                       names.COL_GROUP_PARTY_TYPE_D),
        OwnField(names.COL_PARTY_T_NAME_F, "Nombre")
    ]

    query = {
        QueryNames.LEVEL_TABLE: {
            QueryNames.LEVEL_TABLE_NAME: names.OP_PLOT_T,
            QueryNames.LEVEL_TABLE_ALIAS: names.OP_PLOT_T,
            QueryNames.FILTER_SUB_LEVEL: FilterSubLevel(names.T_ID_F, names.OP_PLOT_T, names.T_ID_F),
            QueryNames.TABLE_FIELDS: [OwnField(names.OP_PLOT_T_PLOT_AREA_F, "Área terreno [m2]")],
            QueryNames.LEVEL_TABLE: {
                QueryNames.LEVEL_TABLE_NAME: names.OP_PARCEL_T,
                QueryNames.LEVEL_TABLE_ALIAS: names.OP_PARCEL_T,
                QueryNames.FILTER_SUB_LEVEL: FilterSubLevel(names.COL_UE_BAUNIT_T_PARCEL_F,
                                                            names.COL_UE_BAUNIT_T,
                                                            names.COL_UE_BAUNIT_T_OP_PLOT_F),
                QueryNames.TABLE_FIELDS: [
                    OwnField(names.COL_BAUNIT_T_NAME_F, "Nombre"),
                    OwnField(names.OP_PARCEL_T_NUPRE_F, "NUPRE"),
                    OwnField(names.OP_PARCEL_T_FMI_F, "FMI"),
                    OwnField(names.OP_PARCEL_T_PARCEL_NUMBER_F, "Número predial"),
                    OwnField(names.OP_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F, "Número predial anterior")
                ],
                '1' + QueryNames.LEVEL_TABLE: {
                    QueryNames.LEVEL_TABLE_NAME: names.OP_RIGHT_T,
                    QueryNames.LEVEL_TABLE_ALIAS: names.OP_RIGHT_T,
                    QueryNames.FILTER_SUB_LEVEL: FilterSubLevel(names.T_ID_F, names.OP_RIGHT_T,
                                                                names.COL_BAUNIT_RRR_T_UNIT_F),
                    QueryNames.TABLE_FIELDS: [
                        DomainOwnField(names.OP_RIGHT_T_TYPE_F, "Tipo de derecho", names.OP_RIGHT_TYPE_D),
                        OwnField(names.COL_RRR_T_DESCRIPTION_F, "Descripción")
                    ],
                    '1' + QueryNames.LEVEL_TABLE: {
                        QueryNames.LEVEL_TABLE_NAME: names.OP_ADMINISTRATIVE_SOURCE_T,
                        QueryNames.LEVEL_TABLE_ALIAS: names.OP_ADMINISTRATIVE_SOURCE_T,
                        QueryNames.FILTER_SUB_LEVEL: FilterSubLevel(names.COL_RRR_SOURCE_T_SOURCE_F,
                                                                    names.COL_RRR_SOURCE_T,
                                                                    names.COL_RRR_SOURCE_T_OP_RIGHT_F),
                        QueryNames.TABLE_FIELDS: op_administrative_source_fields
                    },
                    '2' + QueryNames.LEVEL_TABLE: {
                        QueryNames.LEVEL_TABLE_NAME: names.OP_PARTY_T,
                        QueryNames.LEVEL_TABLE_ALIAS: names.OP_PARTY_T,
                        QueryNames.FILTER_SUB_LEVEL: FilterSubLevel(names.COL_RRR_PARTY_T_OP_PARTY_F,
                                                                    names.OP_RIGHT_T,
                                                                    names.T_ID_F),
                        QueryNames.TABLE_FIELDS: op_party_fields
                    },
                    '3' + QueryNames.LEVEL_TABLE: {
                        QueryNames.LEVEL_TABLE_NAME: names.OP_GROUP_PARTY_T,
                        QueryNames.LEVEL_TABLE_ALIAS: names.OP_GROUP_PARTY_T,
                        QueryNames.FILTER_SUB_LEVEL: FilterSubLevel(names.COL_RRR_PARTY_T_OP_GROUP_PARTY_F,
                                                                    names.OP_RIGHT_T,
                                                                    names.T_ID_F),
                        QueryNames.TABLE_FIELDS: op_group_party_fields,
                        QueryNames.LEVEL_TABLE: {
                            QueryNames.LEVEL_TABLE_NAME: names.OP_PARTY_T,
                            QueryNames.LEVEL_TABLE_ALIAS: names.OP_PARTY_T,
                            QueryNames.FILTER_SUB_LEVEL: FilterSubLevel(names.MEMBERS_T_PARTY_F,
                                                                        names.MEMBERS_T,
                                                                        names.MEMBERS_T_GROUP_PARTY_F),
                            QueryNames.TABLE_FIELDS: op_group_party_party_fields
                        },
                    }
                },
                '2' + QueryNames.LEVEL_TABLE: {
                    QueryNames.LEVEL_TABLE_NAME: names.OP_RESTRICTION_T,
                    QueryNames.LEVEL_TABLE_ALIAS: names.OP_RESTRICTION_T,
                    QueryNames.FILTER_SUB_LEVEL: FilterSubLevel(names.T_ID_F, names.OP_RESTRICTION_T,
                                                                names.COL_BAUNIT_RRR_T_UNIT_F),
                    QueryNames.TABLE_FIELDS: [
                        DomainOwnField(names.OP_RESTRICTION_T_TYPE_F, "Tipo de restricción",
                                       names.OP_RESTRICTION_TYPE_D),
                        OwnField(names.COL_RRR_T_DESCRIPTION_F, "Descripción")
                    ],
                    '1' + QueryNames.LEVEL_TABLE: {
                        QueryNames.LEVEL_TABLE_NAME: names.OP_ADMINISTRATIVE_SOURCE_T,
                        QueryNames.LEVEL_TABLE_ALIAS: names.OP_ADMINISTRATIVE_SOURCE_T,
                        QueryNames.FILTER_SUB_LEVEL: FilterSubLevel(names.COL_RRR_SOURCE_T_SOURCE_F,
                                                                    names.COL_RRR_SOURCE_T,
                                                                    names.COL_RRR_SOURCE_T_OP_RESTRICTION_F),
                        QueryNames.TABLE_FIELDS: op_administrative_source_fields
                    },
                    '2' + QueryNames.LEVEL_TABLE: {
                        QueryNames.LEVEL_TABLE_NAME: names.OP_PARTY_T,
                        QueryNames.LEVEL_TABLE_ALIAS: names.OP_PARTY_T,
                        QueryNames.FILTER_SUB_LEVEL: FilterSubLevel(names.COL_RRR_PARTY_T_OP_PARTY_F,
                                                                    names.OP_RESTRICTION_T,
                                                                    names.T_ID_F),
                        QueryNames.TABLE_FIELDS: op_party_fields
                    },
                    '3' + QueryNames.LEVEL_TABLE: {
                        QueryNames.LEVEL_TABLE_NAME: names.OP_GROUP_PARTY_T,
                        QueryNames.LEVEL_TABLE_ALIAS: names.OP_GROUP_PARTY_T,
                        QueryNames.FILTER_SUB_LEVEL: FilterSubLevel(names.COL_RRR_PARTY_T_OP_GROUP_PARTY_F,
                                                                    names.OP_RESTRICTION_T,
                                                                    names.T_ID_F),
                        QueryNames.TABLE_FIELDS: op_group_party_fields,
                        QueryNames.LEVEL_TABLE: {
                            QueryNames.LEVEL_TABLE_NAME: names.OP_PARTY_T,
                            QueryNames.LEVEL_TABLE_ALIAS: names.OP_PARTY_T,
                            QueryNames.FILTER_SUB_LEVEL: FilterSubLevel(names.MEMBERS_T_PARTY_F,
                                                                        names.MEMBERS_T,
                                                                        names.MEMBERS_T_GROUP_PARTY_F),
                            QueryNames.TABLE_FIELDS: op_group_party_party_fields
                        }
                    }
                }
            }
        }
    }

    return query


def get_structure_basic_query(names):
    required_address_fields = [
        DomainOwnField(names.EXT_ADDRESS_S_ADDRESS_TYPE_F, "Tipo dirección", names.EXT_ADDRESS_TYPE_D),
        OwnField(names.EXT_ADDRESS_S_POSTAL_CODE_F, 'Código postal'),
        EvalExprOwnField("Dirección",
                         QgsExpression("""trim(
                                coalesce(get_domain_value_from_code( '{dominio_clase_via_principal}',  "{clase_via_principal}" , False, False)||' ', '') ||
                                coalesce({valor_via_principal} || ' ', '') ||
                                coalesce({letra_via_principal} || ' ', '') ||
                                coalesce(get_domain_value_from_code( '{dominio_sector_ciudad}',  "{sector_ciudad}", False, False)||' ', '') ||
                                coalesce({valor_via_generadora} || ' ', '') ||
                                coalesce({letra_via_generadora} || ' ', '') ||
                                coalesce({numero_predio} || ' ', '') ||
                                coalesce(get_domain_value_from_code( '{dominio_sector_predio}',  "{sector_predio}", False, False)||' ', '') ||
                                coalesce({complemento} || ' ', '') ||
                                coalesce({nombre_predio}, '')
                            )""".format(
                             dominio_clase_via_principal=names.EXT_ADDRESS_TYPE_MAIN_ROAD_CLASS_D,
                             clase_via_principal=names.EXT_ADDRESS_S_MAIN_ROAD_CLASS_F,
                             valor_via_principal=names.EXT_ADDRESS_S_VALUE_MAIN_ROAD_F,
                             letra_via_principal=names.EXT_ADDRESS_S_LETTER_MAIN_ROAD_F,
                             dominio_sector_ciudad=names.EXT_ADDRESS_TYPE_CITY_SECTOR_D,
                             sector_ciudad=names.EXT_ADDRESS_S_CITY_SECTOR_F,
                             valor_via_generadora=names.EXT_ADDRESS_S_VALUE_GENERATOR_ROAD_F,
                             letra_via_generadora=names.EXT_ADDRESS_S_LETTER_GENERATOR_ROAD_F,
                             numero_predio=names.EXT_ADDRESS_S_PARCEL_NUMBER_F,
                             dominio_sector_predio=names.EXT_ADDRESS_TYPE_PARCEL_SECTOR_D,
                             sector_predio=names.EXT_ADDRESS_S_PARCEL_SECTOR_F,
                             complemento=names.EXT_ADDRESS_S_COMPLEMENT_F,
                             nombre_predio=names.EXT_ADDRESS_S_PARCEL_NAME_F)))]

    query = {
        QueryNames.LEVEL_TABLE: {
            QueryNames.LEVEL_TABLE_NAME: names.OP_PLOT_T,
            QueryNames.LEVEL_TABLE_ALIAS: names.OP_PLOT_T,
            QueryNames.FILTER_SUB_LEVEL: FilterSubLevel(names.T_ID_F, names.OP_PLOT_T, names.T_ID_F),
            QueryNames.TABLE_FIELDS: [OwnField(names.OP_PLOT_T_PLOT_AREA_F, "Área terreno [m2]"),
                                      RelateOwnFieldObject(names.EXT_ADDRESS_S, names.EXT_ADDRESS_S,
                                                           required_address_fields,
                                                           names.EXT_ADDRESS_S_OP_PLOT_F)],
            QueryNames.LEVEL_TABLE: {
                QueryNames.LEVEL_TABLE_NAME: names.OP_PARCEL_T,
                QueryNames.LEVEL_TABLE_ALIAS: names.OP_PARCEL_T,
                QueryNames.FILTER_SUB_LEVEL: FilterSubLevel(names.COL_UE_BAUNIT_T_PARCEL_F,
                                                            names.COL_UE_BAUNIT_T,
                                                            names.COL_UE_BAUNIT_T_OP_PLOT_F),
                QueryNames.TABLE_FIELDS: [
                    OwnField(names.COL_BAUNIT_T_NAME_F, "Nombre"),
                    OwnField(names.OP_PARCEL_T_DEPARTMENT_F, "Departamento"),
                    OwnField(names.OP_PARCEL_T_MUNICIPALITY_F, "Municipio"),
                    OwnField(names.OP_PARCEL_T_NUPRE_F, "NUPRE"),
                    OwnField(names.OP_PARCEL_T_FMI_F, "FMI"),
                    OwnField(names.OP_PARCEL_T_PARCEL_NUMBER_F, "Número predial"),
                    OwnField(names.OP_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F, "Número predial anterior"),
                    DomainOwnField(names.OP_PARCEL_T_TYPE_F, "Tipo", names.OP_PARCEL_TYPE_D)
                ],
                QueryNames.LEVEL_TABLE: {
                    QueryNames.LEVEL_TABLE_NAME: names.OP_BUILDING_T,
                    QueryNames.LEVEL_TABLE_ALIAS: names.OP_BUILDING_T,
                    QueryNames.FILTER_SUB_LEVEL: FilterSubLevel(names.COL_UE_BAUNIT_T_OP_BUILDING_F,
                                                                names.COL_UE_BAUNIT_T,
                                                                names.COL_UE_BAUNIT_T_PARCEL_F),
                    QueryNames.TABLE_FIELDS: [
                        OwnField(names.OP_BUILDING_T_BUILDING_AREA_F, "Área construcción"),
                        RelateOwnFieldObject(names.EXT_ADDRESS_S, names.EXT_ADDRESS_S,
                                             required_address_fields, names.EXT_ADDRESS_S_OP_BUILDING_F)
                    ],
                    QueryNames.LEVEL_TABLE: {
                        QueryNames.LEVEL_TABLE_NAME: names.OP_BUILDING_UNIT_T,
                        QueryNames.LEVEL_TABLE_ALIAS: names.OP_BUILDING_UNIT_T,
                        QueryNames.FILTER_SUB_LEVEL: FilterSubLevel(names.T_ID_F, names.OP_BUILDING_UNIT_T,
                                                                    names.OP_BUILDING_UNIT_T_BUILDING_F),
                        QueryNames.TABLE_FIELDS: [
                            OwnField(names.OP_BUILDING_UNIT_T_TOTAL_FLOORS_F, "Número de pisos"),
                            OwnField(names.OP_BUILDING_UNIT_T_TOTAL_ROOMS_F, "Número de habitaciones"),
                            OwnField(names.OP_BUILDING_UNIT_T_TOTAL_BATHROOMS_F, "Número de baños"),
                            OwnField(names.OP_BUILDING_UNIT_T_TOTAL_LOCALS_F, "Número de locales"),
                            DomainOwnField(names.OP_BUILDING_UNIT_T_BUILDING_TYPE_F, "Tipo construcción",
                                           names.OP_BUILDING_TYPE_D),
                            DomainOwnField(names.OP_BUILDING_UNIT_T_BUILDING_UNIT_TYPE_F,
                                           "Tipo unidad de construcción", names.OP_BUILDING_UNIT_TYPE_D),
                            DomainOwnField(names.OP_BUILDING_UNIT_T_FLOOR_TYPE_F, "Tipo de planta",
                                           names.OP_BUILDING_FLOOR_TYPE_D),
                            DomainOwnField(names.OP_BUILDING_UNIT_T_DOMAIN_TYPE_F, "Tipo dominio",
                                           names.OP_DOMAIN_BUILDING_TYPE_D),
                            OwnField(names.OP_BUILDING_UNIT_T_FLOOR_F, "Ubicación en el piso"),
                            OwnField(names.OP_BUILDING_UNIT_T_BUILT_AREA_F, "Área construida [m2]"),
                            DomainOwnField(names.OP_BUILDING_UNIT_T_USE_F, "Uso",
                                           names.OP_BUILDING_UNIT_USE_D),
                            RelateOwnFieldObject(names.EXT_ADDRESS_S, names.EXT_ADDRESS_S,
                                                 required_address_fields, names.EXT_ADDRESS_S_OP_BUILDING_UNIT_F)
                        ]
                    }
                }
            }
        }
    }

    return query
