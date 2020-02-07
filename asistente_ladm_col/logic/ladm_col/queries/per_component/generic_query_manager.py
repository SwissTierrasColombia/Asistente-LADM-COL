from qgis.core import (QgsFeatureRequest,
                       QgsExpression)

from asistente_ladm_col.logic.ladm_col.queries.per_component.generic_query_objects import (OwnField,
                                                                                           DomainOwnField,
                                                                                           RelateFields,
                                                                                           FilterSubLevel)
from asistente_ladm_col.logic.ladm_col.data.ladm_data import LADM_DATA

LEVEL_TABLE = 'level_table'
LEVEL_TABLE_NAME = 'level_table_name'
LEVEL_TABLE_ALIAS = 'level_table_alias'
FILTER_SUB_LEVEL_TABLE = 'filter_items_table'
ATTRIBUTES_TABLE = 'attributes_table'
TABLE_FIELDS = 'direct_table_fields'

ATTRIBUTES_RESPONSE = "attributes"
ID_FEATURE_RESPONSE = "id"


class GenericQueryManager:

    def __init__(self, db, qgis_utils):
        self._db = db
        self.names = self._db.names
        self.qgis_utils = qgis_utils
        self.ladm_data = LADM_DATA(self.qgis_utils)

    def _get_structure_basic_query(self):
        query = {
            LEVEL_TABLE: {
                LEVEL_TABLE_NAME: self.names.OP_PLOT_T,
                LEVEL_TABLE_ALIAS: "Terrenos",
                FILTER_SUB_LEVEL_TABLE: FilterSubLevel(self.names.T_ID_F, self.names.OP_PLOT_T, self.names.T_ID_F),
                ATTRIBUTES_TABLE: {
                    TABLE_FIELDS: [OwnField(self.names.OP_PLOT_T_PLOT_AREA_F, "Área de terreno [m2]"),
                                   RelateFields("Direcciones",
                                               self.names.EXT_ADDRESS_S, [
                                                   DomainOwnField(self.names.EXT_ADDRESS_S_ADDRESS_TYPE_F, "Tipo dirección", self.names.EXT_ADDRESS_TYPE_D)
                                               ],
                                               self.names.EXT_ADDRESS_S_OP_PLOT_F)]
                },
                LEVEL_TABLE: {
                    LEVEL_TABLE_NAME: self.names.OP_PARCEL_T,
                    LEVEL_TABLE_ALIAS: "Predio",
                    FILTER_SUB_LEVEL_TABLE: FilterSubLevel(self.names.COL_UE_BAUNIT_T_PARCEL_F, self.names.COL_UE_BAUNIT_T, self.names.COL_UE_BAUNIT_T_OP_PLOT_F),
                    ATTRIBUTES_TABLE: {
                        TABLE_FIELDS: [
                            OwnField(self.names.COL_BAUNIT_T_NAME_F, "Nombre"),
                            OwnField(self.names.OP_PARCEL_T_DEPARTMENT_F, "Departamento"),
                            OwnField(self.names.OP_PARCEL_T_MUNICIPALITY_F, "Municipio"),
                            OwnField(self.names.OP_PARCEL_T_NUPRE_F, "NUPRE"),
                            OwnField(self.names.OP_PARCEL_T_FMI_F, "FMI"),
                            OwnField(self.names.OP_PARCEL_T_PARCEL_NUMBER_F, "Número predial"),
                            OwnField(self.names.OP_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F, "Número predial anterior"),
                            DomainOwnField(self.names.OP_PARCEL_T_TYPE_F, "Tipo", self.names.OP_PARCEL_TYPE_D)
                        ]
                    },
                    LEVEL_TABLE: {
                        LEVEL_TABLE_NAME: self.names.OP_BUILDING_T,
                        LEVEL_TABLE_ALIAS: "Construcciones",
                        FILTER_SUB_LEVEL_TABLE: FilterSubLevel(self.names.COL_UE_BAUNIT_T_OP_BUILDING_F, self.names.COL_UE_BAUNIT_T, self.names.COL_UE_BAUNIT_T_PARCEL_F),
                        ATTRIBUTES_TABLE: {
                            TABLE_FIELDS: [
                                OwnField(self.names.OP_BUILDING_T_BUILDING_AREA_F, "Área construcción"),
                                RelateFields("Direcciones",
                                            self.names.EXT_ADDRESS_S, [
                                                DomainOwnField(self.names.EXT_ADDRESS_S_ADDRESS_TYPE_F, "Tipo dirección", self.names.EXT_ADDRESS_TYPE_D)
                                            ],
                                            self.names.EXT_ADDRESS_S_OP_BUILDING_F)
                            ]
                        },
                        LEVEL_TABLE: {
                            LEVEL_TABLE_NAME: self.names.OP_BUILDING_UNIT_T,
                            LEVEL_TABLE_ALIAS: "Unidades de construcción",
                            FILTER_SUB_LEVEL_TABLE: FilterSubLevel(self.names.T_ID_F, self.names.OP_BUILDING_UNIT_T, self.names.OP_BUILDING_UNIT_T_BUILDING_F),
                            ATTRIBUTES_TABLE: {
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
                                    RelateFields("Direcciones",
                                                self.names.EXT_ADDRESS_S, [
                                                    DomainOwnField(self.names.EXT_ADDRESS_S_ADDRESS_TYPE_F, "Tipo dirección", self.names.EXT_ADDRESS_TYPE_D)
                                                ],
                                                self.names.EXT_ADDRESS_S_OP_BUILDING_UNIT_F)
                                ]
                            }
                        }
                    }
                }
            }
        }

        return query

    def execute_basic_query(self, filter_field_value):
        response = dict()
        query = self._get_structure_basic_query()
        self.execute_query(response, query[LEVEL_TABLE], filter_field_value)
        return response

    def execute_query(self, response, level_dict, filter_field_value):
        table_name = level_dict[LEVEL_TABLE_NAME]
        filter_sub_level =  level_dict[FILTER_SUB_LEVEL_TABLE]
        filter_field = filter_sub_level.filter_field_in_sub_level_table
        sub_level_table = filter_sub_level.sub_level_table
        required_field = filter_sub_level.required_field_sub_level_table

        layer = self.qgis_utils.get_layer(self._db, table_name, None, True)
        sub_level_layer = self.qgis_utils.get_layer(self._db, sub_level_table, None, True)
        t_id_features = self.get_features_ids(sub_level_layer, required_field, filter_field, filter_field_value)

        response[table_name] = list()

        dict_fields_and_alias = dict()
        for required_table_field in level_dict[ATTRIBUTES_TABLE][TABLE_FIELDS]:
            if isinstance(required_table_field, OwnField):
                dict_fields_and_alias[required_table_field.field_name] = required_table_field.field_alias

        fields_names = list(dict_fields_and_alias.keys())
        select_features = self.get_features(layer, self.names.T_ID_F, fields_names, t_id_features)

        for select_features in select_features:
            node_response = dict()
            node_response[ID_FEATURE_RESPONSE] = select_features[self.names.T_ID_F]

            node_fields_response = dict()
            for field in level_dict[ATTRIBUTES_TABLE][TABLE_FIELDS]:
                if isinstance(field, DomainOwnField):
                    domain_table = field.domain_table
                    domain_code = select_features[field.field_name]
                    domain_value = self.ladm_data.get_domain_value_from_code(self._db, domain_table, domain_code, False)
                    node_fields_response[field.field_alias] = domain_value
                elif isinstance(field, OwnField):
                    node_fields_response[field.field_alias] = select_features[field.field_name]
                elif isinstance(field, RelateFields):
                    node_fields_response[field.field_alias] = self.get_relate_field(field, select_features[self.names.T_ID_F])

            if LEVEL_TABLE in level_dict:
                self.execute_query(node_fields_response, level_dict[LEVEL_TABLE], [str(select_features[self.names.T_ID_F])])

            node_response[ATTRIBUTES_RESPONSE] = node_fields_response
            response[table_name].append(node_response)

    def get_relate_field(self, field, filter_field_value):
        relate_layer = self.qgis_utils.get_layer(self._db, field.relate_table, None, True)
        dict_fields_and_alias =  self.get_dict_fields_and_alias(field.relate_table_fields)
        fields_names = list(dict_fields_and_alias.keys())
        fields_names += [self.names.T_ID_F]

        features = self.get_features(relate_layer, field.relate_table_filter_field, fields_names, [str(filter_field_value)])

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
                    dict_attributes[field_relation.field_alias] = feature[field_relation.field_name]
            dict_relate_field[ATTRIBUTES_RESPONSE] = dict_attributes
            list_relate_result.append(dict_relate_field)

        return list_relate_result

    @staticmethod
    def get_dict_fields_and_alias(table_fields):
        dict_fields_and_alias = dict()
        for required_table_field in table_fields:
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