from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsFeatureRequest,
                       QgsExpression)

LEVEL_TABLE = 'level_table'
LEVEL_TABLE_NAME = 'level_table_name'
LEVEL_TABLE_ALIAS = 'level_table_alias'
FILTER_ITEMS_TABLE = 'filter_items_table'
REQUIRED_FIELD_SUB_LEVEL_TABLE = "field_sub_level"
SUB_LEVEL_TABLE = 'sub_level_table'
FILTER_FIELD_IN_SUB_LEVEL_TABLE = 'id_field_table_in_sub_level'
ATTRIBUTES_TABLE = 'attributes_table'

TABLE_FIELDS = 'direct_table_fields'
TABLE_FIELD_NAME = 'direct_table_field_name'
TABLE_FIELD_ALIAS = 'direct_table_field_alias'
TYPE_FIELD = "type_field"
TYPE_FIELD_DIRECT = "type_field_direct"

ATTRIBUTES_RESPONSE = "attributes"
ID_FEATURE_RESPONSE = "id"

class GenericQueryManager:

    def __init__(self, db, qgis_utils):
        self._db = db
        self.names = self._db.names
        self.qgis_utils = qgis_utils

    def _get_structure_basic_query(self):
        query = {
            LEVEL_TABLE:{
                LEVEL_TABLE_NAME: self.names.OP_PLOT_T,
                LEVEL_TABLE_ALIAS: QCoreApplication.translate("GenericQueryManager", "Plot"),
                FILTER_ITEMS_TABLE: {
                    REQUIRED_FIELD_SUB_LEVEL_TABLE: self.names.T_ID_F,
                    SUB_LEVEL_TABLE: self.names.OP_PLOT_T,
                    FILTER_FIELD_IN_SUB_LEVEL_TABLE: self.names.T_ID_F
                },
                ATTRIBUTES_TABLE:{
                    TABLE_FIELDS: [
                        {
                            TABLE_FIELD_NAME: self.names.OP_PLOT_T_PLOT_AREA_F,
                            TABLE_FIELD_ALIAS: QCoreApplication.translate("GenericQueryManager", "Plot area"),
                            TYPE_FIELD: TYPE_FIELD_DIRECT
                        }
                    ]
                },
                LEVEL_TABLE: {
                    LEVEL_TABLE_NAME: self.names.OP_PARCEL_T,
                    LEVEL_TABLE_ALIAS: QCoreApplication.translate("GenericQueryManager", "Parcel"),
                    FILTER_ITEMS_TABLE: {
                        REQUIRED_FIELD_SUB_LEVEL_TABLE: self.names.COL_UE_BAUNIT_T_PARCEL_F,
                        SUB_LEVEL_TABLE: self.names.COL_UE_BAUNIT_T,
                        FILTER_FIELD_IN_SUB_LEVEL_TABLE: self.names.COL_UE_BAUNIT_T_OP_PLOT_F
                    },
                    ATTRIBUTES_TABLE: {
                        TABLE_FIELDS: [
                            {
                                TABLE_FIELD_NAME: self.names.COL_BAUNIT_T_NAME_F,
                                TABLE_FIELD_ALIAS: QCoreApplication.translate("GenericQueryManager", "Name"),
                                TYPE_FIELD: TYPE_FIELD_DIRECT
                            },
                            {
                                TABLE_FIELD_NAME: self.names.OP_PARCEL_T_DEPARTMENT_F,
                                TABLE_FIELD_ALIAS: QCoreApplication.translate("GenericQueryManager", "Department"),
                                TYPE_FIELD: TYPE_FIELD_DIRECT
                            },
                            {
                                TABLE_FIELD_NAME: self.names.OP_PARCEL_T_MUNICIPALITY_F,
                                TABLE_FIELD_ALIAS: QCoreApplication.translate("GenericQueryManager", "Municipality"),
                                TYPE_FIELD: TYPE_FIELD_DIRECT
                            },
                            {
                                TABLE_FIELD_NAME: self.names.OP_PARCEL_T_NUPRE_F,
                                TABLE_FIELD_ALIAS: QCoreApplication.translate("GenericQueryManager", "NUPRE"),
                                TYPE_FIELD: TYPE_FIELD_DIRECT
                            },
                            {
                                TABLE_FIELD_NAME: self.names.OP_PARCEL_T_PARCEL_NUMBER_F,
                                TABLE_FIELD_ALIAS: QCoreApplication.translate("GenericQueryManager", "Parcel number"),
                                TYPE_FIELD: TYPE_FIELD_DIRECT
                            },
                            {
                                TABLE_FIELD_NAME: self.names.OP_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F,
                                TABLE_FIELD_ALIAS: QCoreApplication.translate("GenericQueryManager", "Previous parcel number"),
                                TYPE_FIELD: TYPE_FIELD_DIRECT
                            }
                        ]
                    },
                    LEVEL_TABLE: {
                        LEVEL_TABLE_NAME: self.names.OP_BUILDING_T,
                        LEVEL_TABLE_ALIAS: QCoreApplication.translate("GenericQueryManager", "Buildings"),
                        FILTER_ITEMS_TABLE: {
                            REQUIRED_FIELD_SUB_LEVEL_TABLE: self.names.COL_UE_BAUNIT_T_OP_BUILDING_F,
                            SUB_LEVEL_TABLE: self.names.COL_UE_BAUNIT_T,
                            FILTER_FIELD_IN_SUB_LEVEL_TABLE: self.names.COL_UE_BAUNIT_T_PARCEL_F
                        },
                        ATTRIBUTES_TABLE: {
                            TABLE_FIELDS: [
                                {
                                    TABLE_FIELD_NAME: self.names.OP_BUILDING_T_BUILDING_AREA_F,
                                    TABLE_FIELD_ALIAS: QCoreApplication.translate("GenericQueryManager", "Building area"),
                                    TYPE_FIELD: TYPE_FIELD_DIRECT
                                }
                            ]
                        },
                        LEVEL_TABLE: {
                            LEVEL_TABLE_NAME: self.names.OP_BUILDING_UNIT_T,
                            LEVEL_TABLE_ALIAS: QCoreApplication.translate("GenericQueryManager", "Building unit"),
                            FILTER_ITEMS_TABLE: {
                                REQUIRED_FIELD_SUB_LEVEL_TABLE: self.names.T_ID_F,
                                SUB_LEVEL_TABLE: self.names.OP_BUILDING_UNIT_T,
                                FILTER_FIELD_IN_SUB_LEVEL_TABLE: self.names.OP_BUILDING_UNIT_T_BUILDING_F
                            },
                            ATTRIBUTES_TABLE: {
                                TABLE_FIELDS: [
                                    {
                                        TABLE_FIELD_NAME: self.names.OP_BUILDING_UNIT_T_TOTAL_FLOORS_F,
                                        TABLE_FIELD_ALIAS: QCoreApplication.translate("GenericQueryManager", "Total floors"),
                                        TYPE_FIELD: TYPE_FIELD_DIRECT
                                    },{
                                        TABLE_FIELD_NAME: self.names.OP_BUILDING_UNIT_T_TOTAL_ROOMS_F,
                                        TABLE_FIELD_ALIAS: QCoreApplication.translate("GenericQueryManager", "Total rooms"),
                                        TYPE_FIELD: TYPE_FIELD_DIRECT
                                    },{
                                        TABLE_FIELD_NAME: self.names.OP_BUILDING_UNIT_T_TOTAL_BATHROOMS_F,
                                        TABLE_FIELD_ALIAS: QCoreApplication.translate("GenericQueryManager", "Total bathrooms"),
                                        TYPE_FIELD: TYPE_FIELD_DIRECT
                                    },{
                                        TABLE_FIELD_NAME: self.names.OP_BUILDING_UNIT_T_TOTAL_LOCALS_F,
                                        TABLE_FIELD_ALIAS: QCoreApplication.translate("GenericQueryManager", "Total locals"),
                                        TYPE_FIELD: TYPE_FIELD_DIRECT
                                    },{
                                        TABLE_FIELD_NAME: self.names.OP_BUILDING_UNIT_T_FLOOR_F,
                                        TABLE_FIELD_ALIAS: QCoreApplication.translate("GenericQueryManager", "Floor"),
                                        TYPE_FIELD: TYPE_FIELD_DIRECT
                                    },{
                                        TABLE_FIELD_NAME: self.names.OP_BUILDING_UNIT_T_BUILT_AREA_F,
                                        TABLE_FIELD_ALIAS: QCoreApplication.translate("GenericQueryManager", "Built area"),
                                        TYPE_FIELD: TYPE_FIELD_DIRECT
                                    }
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
        filter_field = level_dict[FILTER_ITEMS_TABLE][FILTER_FIELD_IN_SUB_LEVEL_TABLE]
        sub_level_table = level_dict[FILTER_ITEMS_TABLE][SUB_LEVEL_TABLE]
        required_field = level_dict[FILTER_ITEMS_TABLE][REQUIRED_FIELD_SUB_LEVEL_TABLE]

        layer = self.qgis_utils.get_layer(self._db, table_name, None, True)
        sub_level_layer = self.qgis_utils.get_layer(self._db, sub_level_table, None, True)
        t_id_features = self.get_features_ids(sub_level_layer, required_field, filter_field, filter_field_value)

        response[table_name] = list()

        ##########################################################################
        # Get direct fields
        ##########################################################################
        dic_direct_fields_and_alias = dict()
        for table_field in level_dict[ATTRIBUTES_TABLE][TABLE_FIELDS]:
            if table_field[TYPE_FIELD] == TYPE_FIELD_DIRECT:
                dic_direct_fields_and_alias[table_field[TABLE_FIELD_NAME]] = table_field[TABLE_FIELD_ALIAS]

        direct_fields_names = list(dic_direct_fields_and_alias.keys())
        select_features = self.get_features(layer, direct_fields_names, t_id_features)

        for select_features in select_features:
            direct_response = dict()
            direct_response[ID_FEATURE_RESPONSE] = select_features[self.names.T_ID_F]
            direct_response[ATTRIBUTES_RESPONSE] = list()

            direct_fields_response = dict()
            for direct_field_name in direct_fields_names:
                direct_fields_response[dic_direct_fields_and_alias[direct_field_name]] = select_features[direct_field_name]

            if LEVEL_TABLE in level_dict:
                self.execute_query(direct_fields_response, level_dict[LEVEL_TABLE], [str(select_features[self.names.T_ID_F])])

            direct_response[ATTRIBUTES_RESPONSE].append(direct_fields_response)
            response[table_name].append(direct_response)

    def get_features_ids(self, layer, requered_field, filter_field, filter_field_value):
        expression = QgsExpression("{} in ({}) and {} is not null".format(filter_field, ', '.join(filter_field_value), requered_field))
        request = QgsFeatureRequest(expression)
        field_idx = layer.fields().indexFromName(requered_field)
        request.setFlags(QgsFeatureRequest.NoGeometry)
        request.setSubsetOfAttributes([field_idx])  # Note: this adds a new flag
        features_ids = [str(feature[requered_field]) for feature in layer.getFeatures(request)]
        return features_ids

    def get_features(self, layer, fields, t_id_features):
        fields_idx = list()
        for field in fields:
            field_idx = layer.fields().indexFromName(field)
            fields_idx.append(field_idx)

        expression = QgsExpression('{} in ({})'.format(self.names.T_ID_F, ', '.join(t_id_features)))
        request = QgsFeatureRequest(expression)

        request.setFlags(QgsFeatureRequest.NoGeometry)
        request.setSubsetOfAttributes(fields_idx)  # Note: this adds a new flag
        select_features = [feature for feature in layer.getFeatures(request)]
        return select_features