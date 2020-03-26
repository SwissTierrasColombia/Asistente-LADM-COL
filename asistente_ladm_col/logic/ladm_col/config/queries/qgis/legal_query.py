from asistente_ladm_col.logic.ladm_col.config.queries.queries_config_utils import get_full_alias
from asistente_ladm_col.config.mapping_config import QueryNames
from asistente_ladm_col.logic.ladm_col.ladm_query_objects import (OwnField,
                                                                  DomainOwnField,
                                                                  EvalExprOwnField,
                                                                  RelatedOwnFieldObject,
                                                                  RelatedOwnFieldValue,
                                                                  RelatedRemoteFieldValue,
                                                                  FilterSubLevel)
from qgis.core import QgsExpression


def get_igac_legal_query(names, ladm_units):
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
        RelatedOwnFieldValue('Archivo fuente', names.EXT_ARCHIVE_S,
                             OwnField(names.EXT_ARCHIVE_S_DATA_F, 'Archivo fuente'),
                             names.EXT_ARCHIVE_S_OP_ADMINISTRATIVE_SOURCE_F)
    ]

    op_party_fields = [
        DomainOwnField(names.OP_PARTY_T_TYPE_F, "Tipo", names.OP_PARTY_TYPE_D),
        OwnField(names.OP_PARTY_T_DOCUMENT_ID_F, 'Cédula de ciudadanía'),
        OwnField(names.COL_PARTY_T_NAME_F, 'Nombre'),
        OwnField(names.OP_PARTY_T_GENRE_F, 'Género'),
        RelatedOwnFieldObject(names.OP_PARTY_CONTACT_T, names.OP_PARTY_CONTACT_T, op_party_contact_fields,
                              names.OP_PARTY_CONTACT_T_OP_PARTY_F)
    ]

    op_group_party_party_fields = [
        DomainOwnField(names.OP_PARTY_T_TYPE_F, "Tipo", names.OP_PARTY_TYPE_D),
        OwnField(names.OP_PARTY_T_DOCUMENT_ID_F, 'Cédula de ciudadanía'),
        OwnField(names.COL_PARTY_T_NAME_F, 'Nombre'),
        OwnField(names.OP_PARTY_T_GENRE_F, 'Género'),
        RelatedOwnFieldObject(names.OP_PARTY_CONTACT_T, names.OP_PARTY_CONTACT_T, op_party_contact_fields,
                              names.OP_PARTY_CONTACT_T_OP_PARTY_F),
        RelatedRemoteFieldValue(names.FRACTION_S,
                                names.FRACTION_S,
                                EvalExprOwnField("fracción",
                                                QgsExpression(
                                                    "round({numerador}/{denominador} * 100, 2)".format(
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
            QueryNames.TABLE_FIELDS: [OwnField(names.OP_PLOT_T_PLOT_AREA_F, get_full_alias("Área", ladm_units, names.OP_PLOT_T, names.OP_PLOT_T_PLOT_AREA_F))],
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
