from enum import Enum

from qgis.core import (QgsFeatureRequest,
                       QgsExpressionContext,
                       QgsExpressionContextScope,
                       NULL,
                       QgsExpression)

from asistente_ladm_col.logic.ladm_col.queries.per_component.generic_query_objects import (OwnField,
                                                                                           DomainOwnField,
                                                                                           EvalExprOwnField,
                                                                                           AbsRelateFields,
                                                                                           RelateOwnFieldObject,
                                                                                           RelateOwnFieldValue,
                                                                                           RelateRemoteFieldValue,
                                                                                           RelateRemoteFieldObject,
                                                                                           FilterSubLevel)
from asistente_ladm_col.logic.ladm_col.data.ladm_data import LADM_DATA

LEVEL_TABLE = 'level_table'
LEVEL_TABLE_NAME = 'level_table_name'
LEVEL_TABLE_ALIAS = 'level_table_alias'
LEVEL_SELECT_TABLE_FIELD = 'level_select_table_field'
FILTER_SUB_LEVEL = 'filter_sub_level'
TABLE_FIELDS = 'table_fields'

ATTRIBUTES_RESPONSE = "attributes"
ID_FEATURE_RESPONSE = "id"


class GenericQueryType(Enum):
    IGAC_BASIC_QUERY = 1
    IGAC_PHYSICAL_QUERY = 2
    IGAC_LEGAL_QUERY = 3
    IGAC_ECONOMIC_QUERY = 4


class GenericQueryManager:

    def __init__(self, db, qgis_utils):
        self._db = db
        self.names = self._db.names
        self.qgis_utils = qgis_utils
        self.ladm_data = LADM_DATA(self.qgis_utils)

    def _get_structure_legal_query(self):
        op_party_contact_fields = [
            OwnField(self.names.OP_PARTY_CONTACT_T_TELEPHONE_NUMBER_1_F, 'Teléfono 1'),
            OwnField(self.names.OP_PARTY_CONTACT_T_TELEPHONE_NUMBER_2_F, 'Teléfono 2'),
            OwnField(self.names.OP_PARTY_CONTACT_T_NOTIFICATION_ADDRESS_F, 'Domicilio notificación'),
            OwnField(self.names.OP_PARTY_CONTACT_T_EMAIL_F, 'Correo electrónico'),
            DomainOwnField(self.names.OP_PARTY_CONTACT_T_DATA_SOURCE_F, 'Origen de datos', self.names.OP_INSTITUTION_TYPE_D)
        ]

        op_administrative_source_fields = [
            DomainOwnField(self.names.OP_ADMINISTRATIVE_SOURCE_T_TYPE_F, "Tipo de fuente administrativa", self.names.OP_ADMINISTRATIVE_SOURCE_TYPE_D),
            OwnField(self.names.OP_ADMINISTRATIVE_SOURCE_T_EMITTING_ENTITY_F, "Ente emisor"),
            DomainOwnField(self.names.COL_SOURCE_T_AVAILABILITY_STATUS_F, "Estado disponibilidad", self.names.COL_AVAILABILITY_TYPE_D),
            RelateOwnFieldValue('Archivo fuente', self.names.EXT_ARCHIVE_S, OwnField(self.names.EXT_ARCHIVE_S_DATA_F, 'Archivo fuente'), self.names.EXT_ARCHIVE_S_OP_ADMINISTRATIVE_SOURCE_F)
        ]

        op_party_fields = [
            DomainOwnField(self.names.OP_PARTY_T_TYPE_F, "Tipo", self.names.OP_PARTY_TYPE_D),
            OwnField(self.names.OP_PARTY_T_DOCUMENT_ID_F, 'Cédula de ciudadanía'),
            OwnField(self.names.COL_PARTY_T_NAME_F, 'Nombre'),
            OwnField(self.names.OP_PARTY_T_GENRE_F, 'Género'),
            RelateOwnFieldObject(self.names.OP_PARTY_CONTACT_T, self.names.OP_PARTY_CONTACT_T, op_party_contact_fields, self.names.OP_PARTY_CONTACT_T_OP_PARTY_F)
        ]

        op_group_party_party_fields = [
            DomainOwnField(self.names.OP_PARTY_T_TYPE_F, "Tipo", self.names.OP_PARTY_TYPE_D),
            OwnField(self.names.OP_PARTY_T_DOCUMENT_ID_F, 'Cédula de ciudadanía'),
            OwnField(self.names.COL_PARTY_T_NAME_F, 'Nombre'),
            OwnField(self.names.OP_PARTY_T_GENRE_F, 'Género'),
            RelateOwnFieldObject(self.names.OP_PARTY_CONTACT_T, self.names.OP_PARTY_CONTACT_T, op_party_contact_fields, self.names.OP_PARTY_CONTACT_T_OP_PARTY_F),
            RelateRemoteFieldValue(self.names.FRACTION_S,
                                   self.names.FRACTION_S,
                                   EvalExprOwnField("fracción",
                                                    QgsExpression(
                                                        "round({numerador}/{denominador} * 100, 3)".format(
                                                            denominador=self.names.FRACTION_S_DENOMINATOR_F,
                                                            numerador=self.names.FRACTION_S_NUMERATOR_F
                                                        ))),
                                   self.names.FRACTION_S_MEMBER_F,
                                   FilterSubLevel(self.names.T_ID_F, self.names.MEMBERS_T, self.names.MEMBERS_T_PARTY_F))
        ]

        op_group_party_fields = [
            DomainOwnField(self.names.COL_GROUP_PARTY_T_TYPE_F, "Tipo de agrupación de interesados", self.names.COL_GROUP_PARTY_TYPE_D),
            OwnField(self.names.COL_PARTY_T_NAME_F, "Nombre")
        ]

        query = {
            LEVEL_TABLE: {
                LEVEL_TABLE_NAME: self.names.OP_PLOT_T,
                LEVEL_TABLE_ALIAS: self.names.OP_PLOT_T,
                LEVEL_SELECT_TABLE_FIELD: self.names.T_ID_F,
                FILTER_SUB_LEVEL: FilterSubLevel(self.names.T_ID_F, self.names.OP_PLOT_T, self.names.T_ID_F),
                TABLE_FIELDS: [OwnField(self.names.OP_PLOT_T_PLOT_AREA_F, "Área terreno [m2]")],
                LEVEL_TABLE: {
                    LEVEL_TABLE_NAME: self.names.OP_PARCEL_T,
                    LEVEL_TABLE_ALIAS: self.names.OP_PARCEL_T,
                    LEVEL_SELECT_TABLE_FIELD: self.names.T_ID_F,
                    FILTER_SUB_LEVEL: FilterSubLevel(self.names.COL_UE_BAUNIT_T_PARCEL_F,
                                                     self.names.COL_UE_BAUNIT_T,
                                                     self.names.COL_UE_BAUNIT_T_OP_PLOT_F),
                    TABLE_FIELDS: [
                        OwnField(self.names.COL_BAUNIT_T_NAME_F, "Nombre"),
                        OwnField(self.names.OP_PARCEL_T_NUPRE_F, "NUPRE"),
                        OwnField(self.names.OP_PARCEL_T_FMI_F, "FMI"),
                        OwnField(self.names.OP_PARCEL_T_PARCEL_NUMBER_F, "Número predial"),
                        OwnField(self.names.OP_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F, "Número predial anterior")
                    ],
                    '1'+LEVEL_TABLE: {
                        LEVEL_TABLE_NAME: self.names.OP_RIGHT_T,
                        LEVEL_TABLE_ALIAS: self.names.OP_RIGHT_T,
                        LEVEL_SELECT_TABLE_FIELD: self.names.T_ID_F,
                        FILTER_SUB_LEVEL: FilterSubLevel(self.names.T_ID_F, self.names.OP_RIGHT_T, self.names.COL_BAUNIT_RRR_T_UNIT_F),
                        TABLE_FIELDS: [
                            DomainOwnField(self.names.OP_RIGHT_T_TYPE_F, "Tipo de derecho", self.names.OP_RIGHT_TYPE_D),
                            OwnField(self.names.COL_RRR_T_DESCRIPTION_F, "Descripción")
                        ],
                        '1' + LEVEL_TABLE: {
                            LEVEL_TABLE_NAME: self.names.OP_ADMINISTRATIVE_SOURCE_T,
                            LEVEL_TABLE_ALIAS: self.names.OP_ADMINISTRATIVE_SOURCE_T,
                            LEVEL_SELECT_TABLE_FIELD: self.names.T_ID_F,
                            FILTER_SUB_LEVEL: FilterSubLevel(self.names.COL_RRR_SOURCE_T_SOURCE_F,
                                                             self.names.COL_RRR_SOURCE_T,
                                                             self.names.COL_RRR_SOURCE_T_OP_RIGHT_F),
                            TABLE_FIELDS: op_administrative_source_fields
                        },
                        '2' + LEVEL_TABLE: {
                            LEVEL_TABLE_NAME: self.names.OP_PARTY_T,
                            LEVEL_TABLE_ALIAS: self.names.OP_PARTY_T,
                            LEVEL_SELECT_TABLE_FIELD: self.names.T_ID_F,
                            FILTER_SUB_LEVEL: FilterSubLevel(self.names.COL_RRR_PARTY_T_OP_PARTY_F,
                                                             self.names.OP_RIGHT_T,
                                                             self.names.T_ID_F),
                            TABLE_FIELDS: op_party_fields
                        },
                        '3' + LEVEL_TABLE: {
                            LEVEL_TABLE_NAME: self.names.OP_GROUP_PARTY_T,
                            LEVEL_TABLE_ALIAS: self.names.OP_GROUP_PARTY_T,
                            LEVEL_SELECT_TABLE_FIELD: self.names.T_ID_F,
                            FILTER_SUB_LEVEL: FilterSubLevel(self.names.COL_RRR_PARTY_T_OP_GROUP_PARTY_F,
                                                             self.names.OP_RIGHT_T,
                                                             self.names.T_ID_F),
                            TABLE_FIELDS: op_group_party_fields,
                            LEVEL_TABLE: {
                                LEVEL_TABLE_NAME: self.names.OP_PARTY_T,
                                LEVEL_TABLE_ALIAS: self.names.OP_PARTY_T,
                                LEVEL_SELECT_TABLE_FIELD: self.names.T_ID_F,
                                FILTER_SUB_LEVEL: FilterSubLevel(self.names.MEMBERS_T_PARTY_F,
                                                                 self.names.MEMBERS_T,
                                                                 self.names.MEMBERS_T_GROUP_PARTY_F),
                                TABLE_FIELDS: op_group_party_party_fields
                            },
                        }
                    },
                    '2'+LEVEL_TABLE: {
                        LEVEL_TABLE_NAME: self.names.OP_RESTRICTION_T,
                        LEVEL_TABLE_ALIAS: self.names.OP_RESTRICTION_T,
                        LEVEL_SELECT_TABLE_FIELD: self.names.T_ID_F,
                        FILTER_SUB_LEVEL: FilterSubLevel(self.names.T_ID_F, self.names.OP_RESTRICTION_T, self.names.COL_BAUNIT_RRR_T_UNIT_F),
                        TABLE_FIELDS: [
                            DomainOwnField(self.names.OP_RESTRICTION_T_TYPE_F, "Tipo de restricción", self.names.OP_RESTRICTION_TYPE_D),
                            OwnField(self.names.COL_RRR_T_DESCRIPTION_F, "Descripción")
                        ],
                        '1' + LEVEL_TABLE: {
                            LEVEL_TABLE_NAME: self.names.OP_ADMINISTRATIVE_SOURCE_T,
                            LEVEL_TABLE_ALIAS: self.names.OP_ADMINISTRATIVE_SOURCE_T,
                            LEVEL_SELECT_TABLE_FIELD: self.names.T_ID_F,
                            FILTER_SUB_LEVEL: FilterSubLevel(self.names.COL_RRR_SOURCE_T_SOURCE_F,
                                                             self.names.COL_RRR_SOURCE_T,
                                                             self.names.COL_RRR_SOURCE_T_OP_RESTRICTION_F),
                            TABLE_FIELDS: op_administrative_source_fields
                        },
                        '2' + LEVEL_TABLE: {
                            LEVEL_TABLE_NAME: self.names.OP_PARTY_T,
                            LEVEL_TABLE_ALIAS: self.names.OP_PARTY_T,
                            LEVEL_SELECT_TABLE_FIELD: self.names.T_ID_F,
                            FILTER_SUB_LEVEL: FilterSubLevel(self.names.COL_RRR_PARTY_T_OP_PARTY_F,
                                                             self.names.OP_RESTRICTION_T,
                                                             self.names.T_ID_F),
                            TABLE_FIELDS: op_party_fields
                        },
                        '3' + LEVEL_TABLE: {
                            LEVEL_TABLE_NAME: self.names.OP_GROUP_PARTY_T,
                            LEVEL_TABLE_ALIAS: self.names.OP_GROUP_PARTY_T,
                            LEVEL_SELECT_TABLE_FIELD: self.names.T_ID_F,
                            FILTER_SUB_LEVEL: FilterSubLevel(self.names.COL_RRR_PARTY_T_OP_GROUP_PARTY_F,
                                                             self.names.OP_RESTRICTION_T,
                                                             self.names.T_ID_F),
                            TABLE_FIELDS: op_group_party_fields,
                            LEVEL_TABLE: {
                                LEVEL_TABLE_NAME: self.names.OP_PARTY_T,
                                LEVEL_TABLE_ALIAS: self.names.OP_PARTY_T,
                                LEVEL_SELECT_TABLE_FIELD: self.names.T_ID_F,
                                FILTER_SUB_LEVEL: FilterSubLevel(self.names.MEMBERS_T_PARTY_F,
                                                                 self.names.MEMBERS_T,
                                                                 self.names.MEMBERS_T_GROUP_PARTY_F),
                                TABLE_FIELDS: op_group_party_party_fields
                            }
                        }
                    }
                }
            }
        }

        return query

    def _get_structure_basic_query(self):
        required_address_fields = [
            DomainOwnField(self.names.EXT_ADDRESS_S_ADDRESS_TYPE_F, "Tipo dirección", self.names.EXT_ADDRESS_TYPE_D),
            OwnField(self.names.EXT_ADDRESS_S_POSTAL_CODE_F, 'Código postal'),
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
                                 dominio_clase_via_principal=self.names.EXT_ADDRESS_TYPE_MAIN_ROAD_CLASS_D,
                                 clase_via_principal=self.names.EXT_ADDRESS_S_MAIN_ROAD_CLASS_F,
                                 valor_via_principal=self.names.EXT_ADDRESS_S_VALUE_MAIN_ROAD_F,
                                 letra_via_principal=self.names.EXT_ADDRESS_S_LETTER_MAIN_ROAD_F,
                                 dominio_sector_ciudad=self.names.EXT_ADDRESS_TYPE_CITY_SECTOR_D,
                                 sector_ciudad=self.names.EXT_ADDRESS_S_CITY_SECTOR_F,
                                 valor_via_generadora=self.names.EXT_ADDRESS_S_VALUE_GENERATOR_ROAD_F,
                                 letra_via_generadora=self.names.EXT_ADDRESS_S_LETTER_GENERATOR_ROAD_F,
                                 numero_predio=self.names.EXT_ADDRESS_S_PARCEL_NUMBER_F,
                                 dominio_sector_predio=self.names.EXT_ADDRESS_TYPE_PARCEL_SECTOR_D,
                                 sector_predio=self.names.EXT_ADDRESS_S_PARCEL_SECTOR_F,
                                 complemento=self.names.EXT_ADDRESS_S_COMPLEMENT_F,
                                 nombre_predio=self.names.EXT_ADDRESS_S_PARCEL_NAME_F)))]

        query = {
            LEVEL_TABLE: {
                LEVEL_TABLE_NAME: self.names.OP_PLOT_T,
                LEVEL_TABLE_ALIAS: self.names.OP_PLOT_T,
                LEVEL_SELECT_TABLE_FIELD: self.names.T_ID_F,
                FILTER_SUB_LEVEL: FilterSubLevel(self.names.T_ID_F, self.names.OP_PLOT_T, self.names.T_ID_F),
                TABLE_FIELDS: [OwnField(self.names.OP_PLOT_T_PLOT_AREA_F, "Área terreno [m2]"),
                               RelateOwnFieldObject(self.names.EXT_ADDRESS_S, self.names.EXT_ADDRESS_S, required_address_fields, self.names.EXT_ADDRESS_S_OP_PLOT_F)],
                LEVEL_TABLE: {
                    LEVEL_TABLE_NAME: self.names.OP_PARCEL_T,
                    LEVEL_TABLE_ALIAS: self.names.OP_PARCEL_T,
                    LEVEL_SELECT_TABLE_FIELD: self.names.T_ID_F,
                    FILTER_SUB_LEVEL: FilterSubLevel(self.names.COL_UE_BAUNIT_T_PARCEL_F, self.names.COL_UE_BAUNIT_T, self.names.COL_UE_BAUNIT_T_OP_PLOT_F),
                    TABLE_FIELDS: [
                        OwnField(self.names.COL_BAUNIT_T_NAME_F, "Nombre"),
                        OwnField(self.names.OP_PARCEL_T_DEPARTMENT_F, "Departamento"),
                        OwnField(self.names.OP_PARCEL_T_MUNICIPALITY_F, "Municipio"),
                        OwnField(self.names.OP_PARCEL_T_NUPRE_F, "NUPRE"),
                        OwnField(self.names.OP_PARCEL_T_FMI_F, "FMI"),
                        OwnField(self.names.OP_PARCEL_T_PARCEL_NUMBER_F, "Número predial"),
                        OwnField(self.names.OP_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F, "Número predial anterior"),
                        DomainOwnField(self.names.OP_PARCEL_T_TYPE_F, "Tipo", self.names.OP_PARCEL_TYPE_D)
                    ],
                    LEVEL_TABLE: {
                        LEVEL_TABLE_NAME: self.names.OP_BUILDING_T,
                        LEVEL_TABLE_ALIAS: self.names.OP_BUILDING_T,
                        LEVEL_SELECT_TABLE_FIELD: self.names.T_ID_F,
                        FILTER_SUB_LEVEL: FilterSubLevel(self.names.COL_UE_BAUNIT_T_OP_BUILDING_F, self.names.COL_UE_BAUNIT_T, self.names.COL_UE_BAUNIT_T_PARCEL_F),
                        TABLE_FIELDS: [
                            OwnField(self.names.OP_BUILDING_T_BUILDING_AREA_F, "Área construcción"),
                            RelateOwnFieldObject(self.names.EXT_ADDRESS_S, self.names.EXT_ADDRESS_S, required_address_fields, self.names.EXT_ADDRESS_S_OP_BUILDING_F)
                        ],
                        LEVEL_TABLE: {
                            LEVEL_TABLE_NAME: self.names.OP_BUILDING_UNIT_T,
                            LEVEL_TABLE_ALIAS: self.names.OP_BUILDING_UNIT_T,
                            LEVEL_SELECT_TABLE_FIELD: self.names.T_ID_F,
                            FILTER_SUB_LEVEL: FilterSubLevel(self.names.T_ID_F, self.names.OP_BUILDING_UNIT_T, self.names.OP_BUILDING_UNIT_T_BUILDING_F),
                            TABLE_FIELDS: [
                                OwnField(self.names.OP_BUILDING_UNIT_T_TOTAL_FLOORS_F, "Número de pisos"),
                                OwnField(self.names.OP_BUILDING_UNIT_T_TOTAL_ROOMS_F, "Número de habitaciones"),
                                OwnField(self.names.OP_BUILDING_UNIT_T_TOTAL_BATHROOMS_F, "Número de baños"),
                                OwnField(self.names.OP_BUILDING_UNIT_T_TOTAL_LOCALS_F, "Número de locales"),
                                DomainOwnField(self.names.OP_BUILDING_UNIT_T_BUILDING_TYPE_F, "Tipo construcción", self.names.OP_BUILDING_TYPE_D),
                                DomainOwnField(self.names.OP_BUILDING_UNIT_T_BUILDING_UNIT_TYPE_F, "Tipo unidad de construcción", self.names.OP_BUILDING_UNIT_TYPE_D),
                                DomainOwnField(self.names.OP_BUILDING_UNIT_T_FLOOR_TYPE_F, "Tipo de planta", self.names.OP_BUILDING_FLOOR_TYPE_D),
                                DomainOwnField(self.names.OP_BUILDING_UNIT_T_DOMAIN_TYPE_F, "Tipo dominio", self.names.OP_DOMAIN_BUILDING_TYPE_D),
                                OwnField(self.names.OP_BUILDING_UNIT_T_FLOOR_F, "Ubicación en el piso"),
                                OwnField(self.names.OP_BUILDING_UNIT_T_BUILT_AREA_F, "Área construida [m2]"),
                                DomainOwnField(self.names.OP_BUILDING_UNIT_T_USE_F, "Uso", self.names.OP_BUILDING_UNIT_USE_D),
                                RelateOwnFieldObject(self.names.EXT_ADDRESS_S, self.names.EXT_ADDRESS_S, required_address_fields, self.names.EXT_ADDRESS_S_OP_BUILDING_UNIT_F)
                            ]
                        }
                    }
                }
            }
        }

        return query

    def execute_generic_query(self, enum_generic_query, filter_field_value):
        response = dict()
        query = dict()

        if GenericQueryType.IGAC_BASIC_QUERY == enum_generic_query:
            query = self._get_structure_basic_query()
        elif GenericQueryType.IGAC_PHYSICAL_QUERY == enum_generic_query:
            pass
        elif GenericQueryType.IGAC_LEGAL_QUERY == enum_generic_query:
            query = self._get_structure_legal_query()
        elif GenericQueryType.IGAC_ECONOMIC_QUERY == enum_generic_query:
            pass

        self.execute_query(response, query[LEVEL_TABLE], filter_field_value)
        return response

    def execute_legal_query(self, filter_field_value):
        return self.execute_generic_query(GenericQueryType.IGAC_LEGAL_QUERY, filter_field_value)

    def execute_basic_query(self, filter_field_value):
        return self.execute_generic_query(GenericQueryType.IGAC_BASIC_QUERY, filter_field_value)

    def execute_query(self, response, level_dict, filter_field_value):
        table_name = level_dict[LEVEL_TABLE_NAME]
        level_alias = level_dict[LEVEL_TABLE_ALIAS]
        select_table_field = level_dict[LEVEL_SELECT_TABLE_FIELD]
        layer = self.qgis_utils.get_layer(self._db, table_name, None, True)
        filter_sub_level =  level_dict[FILTER_SUB_LEVEL]
        t_id_features = self.get_features_ids_sub_level(filter_sub_level, filter_field_value)

        response[level_alias] = list()

        dict_fields_and_alias = dict()
        for required_table_field in level_dict[TABLE_FIELDS]:
            if isinstance(required_table_field, OwnField):
                dict_fields_and_alias[required_table_field.field_name] = required_table_field.field_alias

        fields_names = list(dict_fields_and_alias.keys())
        select_features = self.get_features(layer, select_table_field, fields_names, t_id_features)

        for select_feature in select_features:
            node_response = dict()
            node_response[ID_FEATURE_RESPONSE] = select_feature[self.names.T_ID_F]

            node_fields_response = dict()
            for field in level_dict[TABLE_FIELDS]:
                if isinstance(field, DomainOwnField):
                    domain_table = field.domain_table
                    domain_code = select_feature[field.field_name]
                    domain_value = self.ladm_data.get_domain_value_from_code(self._db, domain_table, domain_code, False)
                    node_fields_response[field.field_alias] = domain_value
                elif isinstance(field, OwnField):
                    node_fields_response[field.field_alias] = select_feature[field.field_name] if select_feature[field.field_name] != NULL else None
                elif isinstance(field, EvalExprOwnField):
                    node_fields_response[field.field_alias] = self.get_eval_expr_value(layer, select_feature, field.expression)
                elif isinstance(field, AbsRelateFields):
                    if isinstance(field, RelateRemoteFieldObject):
                        node_fields_response[field.field_alias] = self.get_relate_remote_field_object(field, [str(select_feature[self.names.T_ID_F])])
                    elif isinstance(field, RelateRemoteFieldValue):
                        node_fields_response[field.field_alias] = self.get_relate_remote_field_value(field, [str(select_feature[self.names.T_ID_F])])
                    elif isinstance(field, RelateOwnFieldObject):
                        node_fields_response[field.field_alias] = self.get_relate_own_field_object(field, [str(select_feature[self.names.T_ID_F])])
                    elif isinstance(field, RelateOwnFieldValue):
                        node_fields_response[field.field_alias] = self.get_relate_own_field_value(field, [str(select_feature[self.names.T_ID_F])])

            for dict_key in level_dict:
                if dict_key.endswith(LEVEL_TABLE):
                    self.execute_query(node_fields_response, level_dict[dict_key], [str(select_feature[self.names.T_ID_F])])

            node_response[ATTRIBUTES_RESPONSE] = node_fields_response
            response[level_alias].append(node_response)

    def get_relate_remote_field_object(self, field, filter_field_value):
        filter_sub_level = field.filter_sub_level
        t_id_features = self.get_relate_own_field_object(filter_sub_level, filter_field_value)
        return self.get_relate_own_field_value(field, t_id_features)

    def get_relate_remote_field_value(self, field, filter_field_value):
        filter_sub_level = field.filter_sub_level
        t_id_features = self.get_features_ids_sub_level(filter_sub_level, filter_field_value)
        return self.get_relate_own_field_value(field, t_id_features)

    def get_relate_own_field_object(self, field, filter_field_values):
        relate_layer = self.qgis_utils.get_layer(self._db, field.relate_table, None, True)
        dict_fields_and_alias =  self.get_dict_fields_and_alias(field.relate_table_fields)
        fields_names = list(dict_fields_and_alias.keys())
        fields_names.append(self.names.T_ID_F)

        features = self.get_features(relate_layer, field.relate_table_filter_field, fields_names, filter_field_values)

        list_relate_result = list()
        for feature in features:
            dict_relate_field = dict()
            dict_relate_field[ID_FEATURE_RESPONSE] = feature[self.names.T_ID_F]
            dict_attributes = dict()
            for field_relation in field.relate_table_fields:
                if isinstance(field_relation, DomainOwnField):
                    domain_table = field_relation.domain_table
                    domain_code = feature[field_relation.field_name]
                    domain_value = self.ladm_data.get_domain_value_from_code(self._db, domain_table, domain_code, False)
                    dict_attributes[field_relation.field_alias] = domain_value
                elif isinstance(field_relation, OwnField):
                    dict_attributes[field_relation.field_alias] = feature[field_relation.field_name] if feature[field_relation.field_name] != NULL else None
                elif isinstance(field_relation, EvalExprOwnField):
                    dict_attributes[field_relation.field_alias] = self.get_eval_expr_value(relate_layer, feature, field_relation.expression)

            dict_relate_field[ATTRIBUTES_RESPONSE] = dict_attributes
            list_relate_result.append(dict_relate_field)

        return list_relate_result

    def get_relate_own_field_value(self, field, filter_field_values):
        relate_layer = self.qgis_utils.get_layer(self._db, field.relate_table, None, True)
        required_field = field.relate_table_field
        dict_fields_and_alias = self.get_dict_fields_and_alias([required_field])
        fields_names = list(dict_fields_and_alias.keys())
        fields_names.append(self.names.T_ID_F)

        features = self.get_features(relate_layer, field.relate_table_filter_field, fields_names, filter_field_values)

        field_value = None
        for feature in features:
            if isinstance(required_field, DomainOwnField):
                domain_table = required_field.domain_table
                domain_code = feature[required_field.field_name]
                domain_value = self.ladm_data.get_domain_value_from_code(self._db, domain_table, domain_code, False)
                field_value = domain_value
            elif isinstance(required_field, OwnField):
                field_value = feature[required_field.field_name] if feature[required_field.field_name] != NULL else None
            elif isinstance(required_field, EvalExprOwnField):
                field_value = self.get_eval_expr_value(relate_layer, feature, required_field.expression)

        return field_value

    @staticmethod
    def get_eval_expr_value(layer, feature, expression):
        eval_feature = layer.getFeature(feature.id())  # this is necessary because the feature is filtered and may not have all the necessary fields
        context = QgsExpressionContext()
        scope = QgsExpressionContextScope()
        scope.setFeature(eval_feature)
        context.appendScope(scope)
        expression.prepare(context)
        display_value = expression.evaluate(context)

        return display_value

    @staticmethod
    def get_dict_fields_and_alias(table_fields):
        dict_fields_and_alias = dict()
        for required_table_field in table_fields:
            if isinstance(required_table_field, OwnField):
                dict_fields_and_alias[required_table_field.field_name] = required_table_field.field_alias
        return dict_fields_and_alias

    @staticmethod
    def get_features_ids(layer, requered_field, filter_field, filter_field_value):
        expression = QgsExpression("{} in ({}) and {} is not null".format(filter_field, ', '.join(filter_field_value), requered_field))
        request = QgsFeatureRequest(expression)
        field_idx = layer.fields().indexFromName(requered_field)
        request.setFlags(QgsFeatureRequest.NoGeometry)
        request.setSubsetOfAttributes([field_idx])  # Note: this adds a new flag
        features_ids = [str(feature[requered_field]) for feature in layer.getFeatures(request)]
        return features_ids

    def get_features_ids_sub_level(self, filter_sub_level, filter_field_value):
        filter_field = filter_sub_level.filter_field_in_sub_level_table
        sub_level_table = filter_sub_level.sub_level_table
        required_field = filter_sub_level.required_field_sub_level_table
        sub_level_layer = self.qgis_utils.get_layer(self._db, sub_level_table, None, True)
        t_id_features = self.get_features_ids(sub_level_layer, required_field, filter_field, filter_field_value)
        return t_id_features

    def get_features(self, layer, filter_field, fields_names, t_id_features):
        fields_idx = list()
        for field in fields_names:
            field_idx = layer.fields().indexFromName(field)
            fields_idx.append(field_idx)

        expression = QgsExpression('{} in ({})'.format(filter_field, ', '.join(t_id_features)))
        request = QgsFeatureRequest(expression)

        request.setFlags(QgsFeatureRequest.NoGeometry)
        request.setSubsetOfAttributes(fields_idx)  # Note: this adds a new flag
        select_features = [feature for feature in layer.getFeatures(request)]
        return select_features