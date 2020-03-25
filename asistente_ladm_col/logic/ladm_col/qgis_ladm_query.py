import processing

from qgis.core import (QgsFeatureRequest,
                       QgsExpressionContext,
                       QgsExpressionContextScope,
                       NULL,
                       QgsExpression)

from asistente_ladm_col.logic.ladm_col.config.queries.qgis.basic_query import get_igac_basic_query
from asistente_ladm_col.logic.ladm_col.config.queries.qgis.legal_query import get_igac_legal_query
from asistente_ladm_col.logic.ladm_col.config.queries.qgis.economic_query import get_igac_economic_query
from asistente_ladm_col.logic.ladm_col.config.queries.qgis.physical_query import get_igac_physical_query
from asistente_ladm_col.logic.ladm_col.config.queries.qgis.property_record_card_query import get_igac_property_record_card_query

from asistente_ladm_col.logic.ladm_col.ladm_query_objects import (OwnField,
                                                                  DomainOwnField,
                                                                  EvalExprOwnField,
                                                                  AbsRelatedFields,
                                                                  RelatedOwnFieldObject,
                                                                  RelatedOwnFieldValue,
                                                                  RelatedRemoteFieldValue,
                                                                  RelatedRemoteFieldObject,
                                                                  SpatialFilterSubLevel,
                                                                  FilterSubLevel)

from asistente_ladm_col.logic.ladm_col.ladm_data import LADMDATA
from asistente_ladm_col.config.mapping_config import QueryNames
from asistente_ladm_col.config.enums import (EnumSpatialOperationType,
                                             EnumLADMQueryType)


class QGISLADMQuery:

    def __init__(self, qgis_utils):
        self.qgis_utils = qgis_utils
        self.ladm_data = LADMDATA(self.qgis_utils)

    def get_igac_property_record_card_info(self, db, **kwargs):
        return self._execute_ladm_query(db, EnumLADMQueryType.IGAC_PROPERTY_RECORD_CARD_INFO, kwargs)

    def get_igac_economic_info(self, db, **kwargs):
        return self._execute_ladm_query(db, EnumLADMQueryType.IGAC_ECONOMIC_INFO, kwargs)

    def get_igac_physical_info(self, db, **kwargs):
        return self._execute_ladm_query(db, EnumLADMQueryType.IGAC_PHYSICAL_INFO, kwargs)

    def get_igac_legal_info(self, db, **kwargs):
        return self._execute_ladm_query(db, EnumLADMQueryType.IGAC_LEGAL_INFO, kwargs)

    def get_igac_basic_info(self, db, **kwargs):
        return self._execute_ladm_query(db, EnumLADMQueryType.IGAC_BASIC_INFO, kwargs)

    def _execute_ladm_query(self, db, query_type, kwargs):
        params = QGISLADMQuery._get_parameters(kwargs)
        filter_field_values = self._get_plots_ids_from_params(db, params)

        response = dict()
        query = dict()

        ladm_units = db.get_ladm_units()
        if EnumLADMQueryType.IGAC_BASIC_INFO == query_type:
            query = get_igac_basic_query(db.names, ladm_units)
        elif EnumLADMQueryType.IGAC_PHYSICAL_INFO == query_type:
            query = get_igac_physical_query(db.names, ladm_units)
        elif EnumLADMQueryType.IGAC_LEGAL_INFO == query_type:
            query = get_igac_legal_query(db.names, ladm_units)
        elif EnumLADMQueryType.IGAC_ECONOMIC_INFO == query_type:
            query = get_igac_economic_query(db.names, ladm_units)
        elif EnumLADMQueryType.IGAC_PROPERTY_RECORD_CARD_INFO == query_type:
            query = get_igac_property_record_card_query(db.names, ladm_units)

        self._execute_query(db, response, query[QueryNames.LEVEL_TABLE], filter_field_values)
        return response

    def _get_plots_ids_from_params(self, db, params):
        plots_ids = list()

        if params[QueryNames.SEARCH_KEY_PLOT_T_IDS] != 'NULL':
            plots_ids = params[QueryNames.SEARCH_KEY_PLOT_T_IDS]

        if params[QueryNames.SEARCH_KEY_PARCEL_FMI] != 'NULL' or params[QueryNames.SEARCH_KEY_PARCEL_NUMBER] != 'NULL' or params[QueryNames.SEARCH_KEY_PREVIOUS_PARCEL_NUMBER] != 'NULL':

            parcel_layer = self.qgis_utils.get_layer(db, db.names.OP_PARCEL_T, False)
            ue_baunit_layer = self.qgis_utils.get_layer(db, db.names.COL_UE_BAUNIT_T, False)

            if params[QueryNames.SEARCH_KEY_PARCEL_FMI] != 'NULL':
                expr = QgsExpression("{} like '{}'".format(db.names.OP_PARCEL_T_FMI_F, params[QueryNames.SEARCH_KEY_PARCEL_FMI]))
                plots_ids.extend(self._filter_plots_ids_from_expresion(db, parcel_layer, ue_baunit_layer, expr))

            if params[QueryNames.SEARCH_KEY_PARCEL_NUMBER] != 'NULL':
                expr = QgsExpression("{} like '{}'".format(db.names.OP_PARCEL_T_PARCEL_NUMBER_F, params[QueryNames.SEARCH_KEY_PARCEL_NUMBER]))
                plots_ids.extend(self._filter_plots_ids_from_expresion(db, parcel_layer, ue_baunit_layer, expr))

            if params[QueryNames.SEARCH_KEY_PREVIOUS_PARCEL_NUMBER] != 'NULL':
                expr = QgsExpression("{} like '{}'".format(db.names.OP_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F, params[QueryNames.SEARCH_KEY_PREVIOUS_PARCEL_NUMBER]))
                plots_ids.extend(self._filter_plots_ids_from_expresion(db, parcel_layer, ue_baunit_layer, expr))

        return plots_ids

    @staticmethod
    def _filter_plots_ids_from_expresion(db, parcel_layer, ue_baunit_layer, expr_select_parcels):

        # Only required field in parcel layer
        fields_idx = list()
        for field in [db.names.T_ID_F, db.names.OP_PARCEL_T_FMI_F, db.names.OP_PARCEL_T_PARCEL_NUMBER_F, db.names.OP_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F]:
            field_idx = parcel_layer.fields().indexFromName(field)
            fields_idx.append(field_idx)

        request = QgsFeatureRequest(expr_select_parcels)
        request.setFlags(QgsFeatureRequest.NoGeometry)
        request.setSubsetOfAttributes(fields_idx)  # Note: this adds a new flag
        select_parcels = parcel_layer.getFeatures(request)
        parcels_ids = [select_parcel[db.names.T_ID_F] for select_parcel in select_parcels]

        # Only required field in ue baunit layer
        field_idx = parcel_layer.fields().indexFromName(db.names.COL_UE_BAUNIT_T_OP_PLOT_F)
        expr_select_plots = QgsExpression('{} in ({}) AND {} IS NOT NULL'.format(db.names.COL_UE_BAUNIT_T_PARCEL_F, ','.join([str(parcel_id) for parcel_id in parcels_ids]), db.names.COL_UE_BAUNIT_T_OP_PLOT_F))
        request = QgsFeatureRequest(expr_select_plots)
        request.setFlags(QgsFeatureRequest.NoGeometry)
        request.setSubsetOfAttributes([field_idx])  # Note: this adds a new flag
        select_plots = ue_baunit_layer.getFeatures(request)
        plots_ids = [select_plot[db.names.COL_UE_BAUNIT_T_OP_PLOT_F] for select_plot in select_plots]

        return plots_ids

    def _execute_query(self, db, response, level_dict, filter_field_values):
        table_name = level_dict[QueryNames.LEVEL_TABLE_NAME]
        level_alias = level_dict[QueryNames.LEVEL_TABLE_ALIAS]
        layer = self.qgis_utils.get_layer(db, table_name, False)
        filter_sub_level = level_dict[QueryNames.FILTER_SUB_LEVEL]
        t_id_features = self._get_features_ids_sub_level(db, filter_sub_level, filter_field_values)

        response[level_alias] = list()
        dict_fields_and_alias = dict()
        for required_table_field in level_dict[QueryNames.TABLE_FIELDS]:
            if isinstance(required_table_field, OwnField):
                dict_fields_and_alias[required_table_field.field_name] = required_table_field.field_alias

        fields_names = list(dict_fields_and_alias.keys())
        select_features = self._get_features(layer, db.names.T_ID_F, fields_names, t_id_features)

        for select_feature in select_features:
            node_response = dict()
            node_response[QueryNames.ID_FEATURE_RESPONSE] = select_feature[db.names.T_ID_F]

            node_fields_response = dict()
            for field in level_dict[QueryNames.TABLE_FIELDS]:
                if isinstance(field, DomainOwnField):
                    domain_table = field.domain_table
                    domain_code = select_feature[field.field_name]
                    domain_value = self.ladm_data.get_domain_value_from_code(db, domain_table, domain_code, False)
                    node_fields_response[field.field_alias] = domain_value
                elif isinstance(field, OwnField):
                    node_fields_response[field.field_alias] = select_feature[field.field_name] if select_feature[field.field_name] != NULL else None
                elif isinstance(field, EvalExprOwnField):
                    node_fields_response[field.field_alias] = self._get_eval_expr_value(layer, select_feature, field.expression)
                elif isinstance(field, AbsRelatedFields):
                    if isinstance(field, RelatedRemoteFieldObject):
                        node_fields_response[field.field_alias] = self._get_relate_remote_field_object(db, field, [select_feature[db.names.T_ID_F]])
                    elif isinstance(field, RelatedRemoteFieldValue):
                        node_fields_response[field.field_alias] = self._get_relate_remote_field_value(db, field, [select_feature[db.names.T_ID_F]])
                    elif isinstance(field, RelatedOwnFieldObject):
                        node_fields_response[field.field_alias] = self._get_relate_own_field_object(db, field, [select_feature[db.names.T_ID_F]])
                    elif isinstance(field, RelatedOwnFieldValue):
                        node_fields_response[field.field_alias] = self._get_relate_own_field_value(db, field, [select_feature[db.names.T_ID_F]])

            for dict_key in level_dict:
                if dict_key.endswith(QueryNames.LEVEL_TABLE):
                    self._execute_query(db, node_fields_response, level_dict[dict_key], [select_feature[db.names.T_ID_F]])

            node_response[QueryNames.ATTRIBUTES_RESPONSE] = node_fields_response
            response[level_alias].append(node_response)

    def _get_relate_remote_field_object(self, db, field, filter_field_values):
        filter_sub_level = field.filter_sub_level
        t_id_features = self._get_relate_own_field_object(db, filter_sub_level, filter_field_values)
        return self._get_relate_own_field_value(db, field, t_id_features)

    def _get_relate_remote_field_value(self, db, field, filter_field_values):
        filter_sub_level = field.filter_sub_level
        t_id_features = self._get_features_ids_sub_level(db, filter_sub_level, filter_field_values)
        return self._get_relate_own_field_value(db, field, t_id_features)

    def _get_relate_own_field_object(self, db, field, filter_field_values):
        relate_layer = self.qgis_utils.get_layer(db, field.relate_table, False)
        dict_fields_and_alias =  self._get_dict_fields_and_alias(field.relate_table_fields)
        fields_names = list(dict_fields_and_alias.keys())
        fields_names.append(db.names.T_ID_F)

        features = self._get_features(relate_layer, field.relate_table_filter_field, fields_names, filter_field_values)

        list_relate_result = list()
        for feature in features:
            dict_relate_field = dict()
            dict_relate_field[QueryNames.ID_FEATURE_RESPONSE] = feature[db.names.T_ID_F]
            dict_attributes = dict()
            for field_relation in field.relate_table_fields:
                if isinstance(field_relation, DomainOwnField):
                    domain_table = field_relation.domain_table
                    domain_code = feature[field_relation.field_name]
                    domain_value = self.ladm_data.get_domain_value_from_code(db, domain_table, domain_code, False)
                    dict_attributes[field_relation.field_alias] = domain_value
                elif isinstance(field_relation, OwnField):
                    dict_attributes[field_relation.field_alias] = feature[field_relation.field_name] if feature[field_relation.field_name] != NULL else None
                elif isinstance(field_relation, EvalExprOwnField):
                    dict_attributes[field_relation.field_alias] = self._get_eval_expr_value(relate_layer, feature, field_relation.expression)

            dict_relate_field[QueryNames.ATTRIBUTES_RESPONSE] = dict_attributes
            list_relate_result.append(dict_relate_field)

        return list_relate_result

    def _get_relate_own_field_value(self, db, field, filter_field_values):
        relate_layer = self.qgis_utils.get_layer(db, field.relate_table, False)
        required_field = field.relate_table_field
        dict_fields_and_alias = self._get_dict_fields_and_alias([required_field])
        fields_names = list(dict_fields_and_alias.keys())
        fields_names.append(db.names.T_ID_F)

        features = self._get_features(relate_layer, field.relate_table_filter_field, fields_names, filter_field_values)

        field_value = None
        for feature in features:
            if isinstance(required_field, DomainOwnField):
                domain_table = required_field.domain_table
                domain_code = feature[required_field.field_name]
                domain_value = self.ladm_data.get_domain_value_from_code(db, domain_table, domain_code, False)
                field_value = domain_value
            elif isinstance(required_field, OwnField):
                field_value = feature[required_field.field_name] if feature[required_field.field_name] != NULL else None
            elif isinstance(required_field, EvalExprOwnField):
                field_value = self._get_eval_expr_value(relate_layer, feature, required_field.expression)

        return field_value

    def _get_features_ids_by_filter(self, db, filter_sub_level, filter_field_values):  # filter_field_values it is a list with only one item
        sub_level_table = filter_sub_level.sub_level_table
        required_field = filter_sub_level.required_field_sub_level_table
        sub_level_layer = self.qgis_utils.get_layer(db, sub_level_table, False)

        if isinstance(filter_sub_level, FilterSubLevel):
            filter_field = filter_sub_level.filter_field_in_sub_level_table
            expression = QgsExpression("{} in ({}) and {} is not null".format(filter_field, ', '.join(str(filter_field_value) for filter_field_value in filter_field_values), required_field))
            request = QgsFeatureRequest(expression)
            field_idx = sub_level_layer.fields().indexFromName(required_field)
            request.setFlags(QgsFeatureRequest.NoGeometry)
            request.setSubsetOfAttributes([field_idx])  # Note: this adds a new flag
            features_ids = [feature[required_field] for feature in sub_level_layer.getFeatures(request)]
            return features_ids

        elif isinstance(filter_sub_level, SpatialFilterSubLevel):
            level_table = filter_sub_level.level_table
            spatial_operation = filter_sub_level.spatial_operation
            level_layer = self.qgis_utils.get_layer(db, level_table, False)
            filter_level_layer = processing.run("native:extractbyattribute", {'INPUT': level_layer, 'FIELD': db.names.T_ID_F, 'OPERATOR': 0, 'VALUE': filter_field_values[0], 'OUTPUT': 'memory:'})['OUTPUT']

            parameters = {'INPUT': sub_level_layer, 'INTERSECT': filter_level_layer, 'OUTPUT': 'memory:'}
            if spatial_operation == EnumSpatialOperationType.INTERSECTS:
                parameters['PREDICATE'] = [0]  # Intersects
            elif spatial_operation == EnumSpatialOperationType.OVERLAPS:
                parameters['PREDICATE'] = [5]  # Overlaps
            elif spatial_operation == EnumSpatialOperationType.CONTAINS:
                parameters['PREDICATE'] = [1]  # Contains

            filter_sub_level_layer = processing.run("native:extractbylocation", parameters)['OUTPUT']

            features_ids = [feature[required_field] for feature in filter_sub_level_layer.getFeatures()]
            return features_ids

    def _get_features_ids_sub_level(self, db, filter_sub_level, filter_field_values):
        t_id_features = list()
        for filter_field_value in filter_field_values:
            t_id_features.extend(self._get_features_ids_by_filter(db, filter_sub_level, [filter_field_value]))

        sub_filter_sub_level = filter_sub_level.filter_sub_level  # Recursivity to get features t_ids associate to the first filter
        if sub_filter_sub_level:
             return self._get_features_ids_sub_level(db, sub_filter_sub_level, t_id_features)
        else:
            return t_id_features

    @staticmethod
    def _get_eval_expr_value(layer, feature, expression):
        eval_feature = layer.getFeature(feature.id())  # this is necessary because the feature is filtered and may not have all the necessary fields
        context = QgsExpressionContext()
        scope = QgsExpressionContextScope()
        scope.setFeature(eval_feature)
        context.appendScope(scope)
        expression.prepare(context)
        display_value = expression.evaluate(context)

        return display_value

    @staticmethod
    def _get_dict_fields_and_alias(table_fields):
        dict_fields_and_alias = dict()
        for required_table_field in table_fields:
            if isinstance(required_table_field, OwnField):
                dict_fields_and_alias[required_table_field.field_name] = required_table_field.field_alias
        return dict_fields_and_alias

    @staticmethod
    def _get_features(layer, filter_field, fields_names, t_id_features):
        if not t_id_features:
            return list()

        fields_idx = list()
        for field in fields_names:
            field_idx = layer.fields().indexFromName(field)
            fields_idx.append(field_idx)

        expression = QgsExpression('{} in ({})'.format(filter_field, ', '.join( str(t_id_feature) for t_id_feature in t_id_features)))
        request = QgsFeatureRequest(expression)

        request.setFlags(QgsFeatureRequest.NoGeometry)
        request.setSubsetOfAttributes(fields_idx)  # Note: this adds a new flag
        select_features = [feature for feature in layer.getFeatures(request)]
        return select_features

    @staticmethod
    def _get_parameters(kwargs):
        params = {
            QueryNames.SEARCH_KEY_PLOT_T_IDS: 'NULL',
            QueryNames.SEARCH_KEY_PARCEL_FMI: 'NULL',
            QueryNames.SEARCH_KEY_PARCEL_NUMBER: 'NULL',
            QueryNames.SEARCH_KEY_PREVIOUS_PARCEL_NUMBER: 'NULL'
        }

        params.update(kwargs)
        return params