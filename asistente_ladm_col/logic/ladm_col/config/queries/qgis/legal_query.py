from asistente_ladm_col.logic.ladm_col.config.queries.queries_config_utils import get_full_alias
from asistente_ladm_col.config.mapping_config import QueryNames
from asistente_ladm_col.logic.ladm_col.ladm_query_objects import (OwnField,
                                                                  DomainOwnField,
                                                                  EvalExpressionOwnField,
                                                                  RelatedOwnFieldObject,
                                                                  RelatedOwnFieldValue,
                                                                  RelatedRemoteFieldValue,
                                                                  FilterSubLevel)
from qgis.core import QgsExpression


def get_igac_legal_query(names, ladm_units):
    lc_party_contact_fields = [
        OwnField(names.LC_PARTY_CONTACT_T_TELEPHONE_NUMBER_1_F, 'Teléfono 1'),
        OwnField(names.LC_PARTY_CONTACT_T_TELEPHONE_NUMBER_2_F, 'Teléfono 2'),
        OwnField(names.LC_PARTY_CONTACT_T_NOTIFICATION_ADDRESS_F, 'Domicilio notificación'),
        OwnField(names.LC_PARTY_CONTACT_T_EMAIL_F, 'Correo electrónico')
    ]

    lc_administrative_source_fields = [
        DomainOwnField(names.LC_ADMINISTRATIVE_SOURCE_T_TYPE_F, "Tipo de fuente administrativa",
                       names.LC_ADMINISTRATIVE_SOURCE_TYPE_D),
        OwnField(names.LC_ADMINISTRATIVE_SOURCE_T_EMITTING_ENTITY_F, "Ente emisor"),
        DomainOwnField(names.COL_SOURCE_T_AVAILABILITY_STATUS_F, "Estado disponibilidad",
                       names.COL_AVAILABILITY_TYPE_D),
        RelatedOwnFieldValue('Archivo fuente', names.EXT_ARCHIVE_S,
                             OwnField(names.EXT_ARCHIVE_S_DATA_F, 'Archivo fuente'),
                             names.EXT_ARCHIVE_S_LC_ADMINISTRATIVE_SOURCE_F)
    ]

    lc_party_fields = [
        DomainOwnField(names.LC_PARTY_T_TYPE_F, "Tipo", names.LC_PARTY_TYPE_D),
        OwnField(names.LC_PARTY_T_DOCUMENT_ID_F, 'Cédula de ciudadanía'),
        OwnField(names.COL_PARTY_T_NAME_F, 'Nombre'),
        OwnField(names.LC_PARTY_T_GENRE_F, 'Género'),
        RelatedOwnFieldObject(names.LC_PARTY_CONTACT_T, names.LC_PARTY_CONTACT_T, lc_party_contact_fields,
                              names.LC_PARTY_CONTACT_T_LC_PARTY_F)
    ]

    lc_group_party_party_fields = [
        DomainOwnField(names.LC_PARTY_T_TYPE_F, "Tipo", names.LC_PARTY_TYPE_D),
        OwnField(names.LC_PARTY_T_DOCUMENT_ID_F, 'Cédula de ciudadanía'),
        OwnField(names.COL_PARTY_T_NAME_F, 'Nombre'),
        OwnField(names.LC_PARTY_T_GENRE_F, 'Género'),
        RelatedOwnFieldObject(names.LC_PARTY_CONTACT_T, names.LC_PARTY_CONTACT_T, lc_party_contact_fields,
                              names.LC_PARTY_CONTACT_T_LC_PARTY_F),
        RelatedRemoteFieldValue(names.FRACTION_S,
                                names.FRACTION_S,
                                EvalExpressionOwnField("fracción",
                                                       QgsExpression(
                                                    "round({numerador}/{denominador} * 100, 2)".format(
                                                        denominador=names.FRACTION_S_DENOMINATOR_F,
                                                        numerador=names.FRACTION_S_NUMERATOR_F
                                                    ))),
                                names.FRACTION_S_MEMBER_F,
                                FilterSubLevel(names.T_ID_F, names.MEMBERS_T, names.MEMBERS_T_PARTY_F))
    ]

    lc_group_party_fields = [
        DomainOwnField(names.COL_GROUP_PARTY_T_TYPE_F, "Tipo de agrupación de interesados",
                       names.COL_GROUP_PARTY_TYPE_D),
        OwnField(names.COL_PARTY_T_NAME_F, "Nombre")
    ]

    query = {
        QueryNames.LEVEL_TABLE: {
            QueryNames.LEVEL_TABLE_NAME: names.LC_PLOT_T,
            QueryNames.LEVEL_TABLE_ALIAS: names.LC_PLOT_T,
            QueryNames.FILTER_SUB_LEVEL: FilterSubLevel(names.T_ID_F, names.LC_PLOT_T, names.T_ID_F),
            QueryNames.TABLE_FIELDS: [OwnField(names.LC_PLOT_T_PLOT_AREA_F, get_full_alias("Área", ladm_units, names.LC_PLOT_T, names.LC_PLOT_T_PLOT_AREA_F))],
            QueryNames.LEVEL_TABLE: {
                QueryNames.LEVEL_TABLE_NAME: names.LC_PARCEL_T,
                QueryNames.LEVEL_TABLE_ALIAS: names.LC_PARCEL_T,
                QueryNames.FILTER_SUB_LEVEL: FilterSubLevel(names.COL_UE_BAUNIT_T_PARCEL_F,
                                                            names.COL_UE_BAUNIT_T,
                                                            names.COL_UE_BAUNIT_T_LC_PLOT_F),
                QueryNames.TABLE_FIELDS: [
                    OwnField(names.COL_BAUNIT_T_NAME_F, "Nombre"),
                    OwnField(names.LC_PARCEL_T_ID_OPERATION_F, "Id operación"),
                    OwnField(names.LC_PARCEL_T_FMI_F, "FMI"),
                    OwnField(names.LC_PARCEL_T_PARCEL_NUMBER_F, "Número predial"),
                    OwnField(names.LC_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F, "Número predial anterior")
                ],
                '1' + QueryNames.LEVEL_TABLE: {
                    QueryNames.LEVEL_TABLE_NAME: names.LC_RIGHT_T,
                    QueryNames.LEVEL_TABLE_ALIAS: names.LC_RIGHT_T,
                    QueryNames.FILTER_SUB_LEVEL: FilterSubLevel(names.T_ID_F, names.LC_RIGHT_T,
                                                                names.COL_BAUNIT_RRR_T_UNIT_F),
                    QueryNames.TABLE_FIELDS: [
                        DomainOwnField(names.LC_RIGHT_T_TYPE_F, "Tipo de derecho", names.LC_RIGHT_TYPE_D),
                        OwnField(names.COL_RRR_T_DESCRIPTION_F, "Descripción")
                    ],
                    '1' + QueryNames.LEVEL_TABLE: {
                        QueryNames.LEVEL_TABLE_NAME: names.LC_ADMINISTRATIVE_SOURCE_T,
                        QueryNames.LEVEL_TABLE_ALIAS: names.LC_ADMINISTRATIVE_SOURCE_T,
                        QueryNames.FILTER_SUB_LEVEL: FilterSubLevel(names.COL_RRR_SOURCE_T_SOURCE_F,
                                                                    names.COL_RRR_SOURCE_T,
                                                                    names.COL_RRR_SOURCE_T_LC_RIGHT_F),
                        QueryNames.TABLE_FIELDS: lc_administrative_source_fields
                    },
                    '2' + QueryNames.LEVEL_TABLE: {
                        QueryNames.LEVEL_TABLE_NAME: names.LC_PARTY_T,
                        QueryNames.LEVEL_TABLE_ALIAS: names.LC_PARTY_T,
                        QueryNames.FILTER_SUB_LEVEL: FilterSubLevel(names.COL_RRR_PARTY_T_LC_PARTY_F,
                                                                    names.LC_RIGHT_T,
                                                                    names.T_ID_F),
                        QueryNames.TABLE_FIELDS: lc_party_fields
                    },
                    '3' + QueryNames.LEVEL_TABLE: {
                        QueryNames.LEVEL_TABLE_NAME: names.LC_GROUP_PARTY_T,
                        QueryNames.LEVEL_TABLE_ALIAS: names.LC_GROUP_PARTY_T,
                        QueryNames.FILTER_SUB_LEVEL: FilterSubLevel(names.COL_RRR_PARTY_T_LC_GROUP_PARTY_F,
                                                                    names.LC_RIGHT_T,
                                                                    names.T_ID_F),
                        QueryNames.TABLE_FIELDS: lc_group_party_fields,
                        QueryNames.LEVEL_TABLE: {
                            QueryNames.LEVEL_TABLE_NAME: names.LC_PARTY_T,
                            QueryNames.LEVEL_TABLE_ALIAS: names.LC_PARTY_T,
                            QueryNames.FILTER_SUB_LEVEL: FilterSubLevel(names.MEMBERS_T_PARTY_F,
                                                                        names.MEMBERS_T,
                                                                        names.MEMBERS_T_GROUP_PARTY_F),
                            QueryNames.TABLE_FIELDS: lc_group_party_party_fields
                        },
                    }
                },
                '2' + QueryNames.LEVEL_TABLE: {
                    QueryNames.LEVEL_TABLE_NAME: names.LC_RESTRICTION_T,
                    QueryNames.LEVEL_TABLE_ALIAS: names.LC_RESTRICTION_T,
                    QueryNames.FILTER_SUB_LEVEL: FilterSubLevel(names.T_ID_F, names.LC_RESTRICTION_T,
                                                                names.COL_BAUNIT_RRR_T_UNIT_F),
                    QueryNames.TABLE_FIELDS: [
                        DomainOwnField(names.LC_RESTRICTION_T_TYPE_F, "Tipo de restricción",
                                       names.LC_RESTRICTION_TYPE_D),
                        OwnField(names.COL_RRR_T_DESCRIPTION_F, "Descripción")
                    ],
                    '1' + QueryNames.LEVEL_TABLE: {
                        QueryNames.LEVEL_TABLE_NAME: names.LC_ADMINISTRATIVE_SOURCE_T,
                        QueryNames.LEVEL_TABLE_ALIAS: names.LC_ADMINISTRATIVE_SOURCE_T,
                        QueryNames.FILTER_SUB_LEVEL: FilterSubLevel(names.COL_RRR_SOURCE_T_SOURCE_F,
                                                                    names.COL_RRR_SOURCE_T,
                                                                    names.COL_RRR_SOURCE_T_LC_RESTRICTION_F),
                        QueryNames.TABLE_FIELDS: lc_administrative_source_fields
                    },
                    '2' + QueryNames.LEVEL_TABLE: {
                        QueryNames.LEVEL_TABLE_NAME: names.LC_PARTY_T,
                        QueryNames.LEVEL_TABLE_ALIAS: names.LC_PARTY_T,
                        QueryNames.FILTER_SUB_LEVEL: FilterSubLevel(names.COL_RRR_PARTY_T_LC_PARTY_F,
                                                                    names.LC_RESTRICTION_T,
                                                                    names.T_ID_F),
                        QueryNames.TABLE_FIELDS: lc_party_fields
                    },
                    '3' + QueryNames.LEVEL_TABLE: {
                        QueryNames.LEVEL_TABLE_NAME: names.LC_GROUP_PARTY_T,
                        QueryNames.LEVEL_TABLE_ALIAS: names.LC_GROUP_PARTY_T,
                        QueryNames.FILTER_SUB_LEVEL: FilterSubLevel(names.COL_RRR_PARTY_T_LC_GROUP_PARTY_F,
                                                                    names.LC_RESTRICTION_T,
                                                                    names.T_ID_F),
                        QueryNames.TABLE_FIELDS: lc_group_party_fields,
                        QueryNames.LEVEL_TABLE: {
                            QueryNames.LEVEL_TABLE_NAME: names.LC_PARTY_T,
                            QueryNames.LEVEL_TABLE_ALIAS: names.LC_PARTY_T,
                            QueryNames.FILTER_SUB_LEVEL: FilterSubLevel(names.MEMBERS_T_PARTY_F,
                                                                        names.MEMBERS_T,
                                                                        names.MEMBERS_T_GROUP_PARTY_F),
                            QueryNames.TABLE_FIELDS: lc_group_party_party_fields
                        }
                    }
                }
            }
        }
    }

    return query
