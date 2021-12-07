# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2020-02-24
        git sha              : :%H$
        copyright            : (C) 2020 by Leonardo Cardona (BSF Swissphoto)
        email                : leo.cardona.p@gmail.com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""
import processing

from qgis.core import (QgsFeatureRequest,
                       QgsExpressionContext,
                       QgsExpressionContextScope,
                       NULL,
                       QgsExpression)

from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.logic.ladm_col.config.queries.qgis.basic_query import get_igac_basic_query
from asistente_ladm_col.logic.ladm_col.config.queries.qgis.legal_query import get_igac_legal_query
from asistente_ladm_col.logic.ladm_col.config.queries.qgis.economic_query import get_igac_economic_query
from asistente_ladm_col.logic.ladm_col.config.queries.qgis.physical_query import get_igac_physical_query
from asistente_ladm_col.logic.ladm_col.config.queries.qgis.property_record_card_query import get_igac_property_record_card_query

from asistente_ladm_col.logic.ladm_col.ladm_query_objects import (OwnField,
                                                                  DomainOwnField,
                                                                  EvalExpressionOwnField,
                                                                  AbsRelatedFields,
                                                                  RelatedOwnFieldObject,
                                                                  RelatedOwnFieldValue,
                                                                  RelatedRemoteFieldValue,
                                                                  RelatedRemoteFieldObject,
                                                                  SpatialFilterSubLevel,
                                                                  FilterSubLevel)

from asistente_ladm_col.logic.ladm_col.ladm_data import LADMData
from asistente_ladm_col.config.query_names import QueryNames
from asistente_ladm_col.config.enums import (EnumSpatialOperationType,
                                             EnumLADMQueryType)


class QGISLADMQuery:

    def __init__(self):
        self.app = AppInterface()
        self.ladm_data = LADMData()

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
        filter_field_values = self._get_plot_ids_from_params(db, params)

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

    def _get_plot_ids_from_params(self, db, params):
        """
        Get plot ids depending on a defined filter in params
            SEARCH_KEY_PARCEL_FMI: Get plots id associated with parcel filter by parcel FMI
            SEARCH_KEY_PARCEL_NUMBER: Get plots id associated with parcel filter by parcel number
            SEARCH_KEY_PREVIOUS_PARCEL_NUMBER: Get plots id associated with parcel filter by previous parcel number
        """
        plot_ids = list()

        if params[QueryNames.SEARCH_KEY_PLOT_T_IDS] != 'NULL':
            plot_ids = params[QueryNames.SEARCH_KEY_PLOT_T_IDS]

        if params[QueryNames.SEARCH_KEY_PARCEL_FMI] != 'NULL' or params[QueryNames.SEARCH_KEY_PARCEL_NUMBER] != 'NULL' or params[QueryNames.SEARCH_KEY_PREVIOUS_PARCEL_NUMBER] != 'NULL':
            layers = {db.names.LC_PARCEL_T: None,
                      db.names.COL_UE_BAUNIT_T: None}
            self.app.core.get_layers(db, layers, False)

            if layers:
                parcel_layer = layers[db.names.LC_PARCEL_T]
                ue_baunit_layer = layers[db.names.COL_UE_BAUNIT_T]

                if params[QueryNames.SEARCH_KEY_PARCEL_FMI] != 'NULL':
                    expr = QgsExpression("{} like '{}'".format(db.names.LC_PARCEL_T_FMI_F, params[QueryNames.SEARCH_KEY_PARCEL_FMI]))
                    plot_ids.extend(self._filter_plots_ids_from_expresion(db, parcel_layer, ue_baunit_layer, expr))

                if params[QueryNames.SEARCH_KEY_PARCEL_NUMBER] != 'NULL':
                    expr = QgsExpression("{} like '{}'".format(db.names.LC_PARCEL_T_PARCEL_NUMBER_F, params[QueryNames.SEARCH_KEY_PARCEL_NUMBER]))
                    plot_ids.extend(self._filter_plots_ids_from_expresion(db, parcel_layer, ue_baunit_layer, expr))

                if params[QueryNames.SEARCH_KEY_PREVIOUS_PARCEL_NUMBER] != 'NULL':
                    expr = QgsExpression("{} like '{}'".format(db.names.LC_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F, params[QueryNames.SEARCH_KEY_PREVIOUS_PARCEL_NUMBER]))
                    plot_ids.extend(self._filter_plots_ids_from_expresion(db, parcel_layer, ue_baunit_layer, expr))

        return plot_ids

    @staticmethod
    def _filter_plots_ids_from_expresion(db, parcel_layer, ue_baunit_layer, expression_select_parcels):
        """
        Get plots ids depending of a defined filter expression
        """
        # Only required field in parcel layer
        fields_idx = list()
        for field in [db.names.T_ID_F, db.names.LC_PARCEL_T_FMI_F, db.names.LC_PARCEL_T_PARCEL_NUMBER_F, db.names.LC_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F]:
            fields_idx.append(parcel_layer.fields().indexFromName(field))

        request = QgsFeatureRequest(expression_select_parcels)
        request.setFlags(QgsFeatureRequest.NoGeometry)
        request.setSubsetOfAttributes(fields_idx)  # Note: this adds a new flag
        parcels = parcel_layer.getFeatures(request)
        parcel_ids = [select_parcel[db.names.T_ID_F] for select_parcel in parcels]

        # Only required field in ue baunit layer
        field_idx = parcel_layer.fields().indexFromName(db.names.COL_UE_BAUNIT_T_LC_PLOT_F)
        expression_select_plots = QgsExpression('{} in ({}) AND {} IS NOT NULL'.format(db.names.COL_UE_BAUNIT_T_PARCEL_F, ','.join([str(parcel_id) for parcel_id in parcel_ids]), db.names.COL_UE_BAUNIT_T_LC_PLOT_F))
        request = QgsFeatureRequest(expression_select_plots)
        request.setFlags(QgsFeatureRequest.NoGeometry)
        request.setSubsetOfAttributes([field_idx])  # Note: this adds a new flag
        plots = ue_baunit_layer.getFeatures(request)

        return [plot[db.names.COL_UE_BAUNIT_T_LC_PLOT_F] for plot in plots]  # Plot ids

    def _execute_query(self, db, response, level_dict, filter_field_values):
        """
        Recursive function that allows solving the queries defined using the LADM Query Objects.
        Recursion ends when the last nesting level is reached.
        :param db: database connection instance
        :param response: object that is recursively built with the response.
        :param level_dict: nesting level dictionary to solve
        :param filter_field_values: list of filter field values
        :return dictionary with the query result
        """
        table_name = level_dict[QueryNames.LEVEL_TABLE_NAME]
        level_alias = level_dict[QueryNames.LEVEL_TABLE_ALIAS]
        layer = self.app.core.get_layer(db, table_name, False)
        filter_sub_level = level_dict[QueryNames.FILTER_SUB_LEVEL]
        t_id_features = self._get_features_ids_sub_level(db, filter_sub_level, filter_field_values)

        response[level_alias] = list()
        dict_fields_and_alias = dict()
        for required_table_field in level_dict[QueryNames.TABLE_FIELDS]:
            if isinstance(required_table_field, OwnField):
                dict_fields_and_alias[required_table_field.field_name] = required_table_field.field_alias

        field_names = list(dict_fields_and_alias.keys())
        features = self._get_features(layer, db.names.T_ID_F, field_names, t_id_features)

        for feature in features:
            node_response = dict()
            node_response[QueryNames.ID_FEATURE_RESPONSE] = feature[db.names.T_ID_F]

            node_fields_response = dict()
            for field in level_dict[QueryNames.TABLE_FIELDS]:
                if isinstance(field, DomainOwnField):
                    domain_table = field.domain_table
                    domain_code = feature[field.field_name]
                    domain_value = self.ladm_data.get_domain_value_from_code(db, domain_table, domain_code, False)
                    node_fields_response[field.field_alias] = domain_value
                elif isinstance(field, OwnField):
                    node_fields_response[field.field_alias] = feature[field.field_name] if feature[field.field_name] != NULL else None
                elif isinstance(field, EvalExpressionOwnField):
                    node_fields_response[field.field_alias] = self._get_eval_expr_value(layer, feature, field.expression)
                elif isinstance(field, AbsRelatedFields):
                    if isinstance(field, RelatedRemoteFieldObject):
                        node_fields_response[field.field_alias] = self._get_relate_remote_field_object(db, field, [feature[db.names.T_ID_F]])
                    elif isinstance(field, RelatedRemoteFieldValue):
                        node_fields_response[field.field_alias] = self._get_relate_remote_field_value(db, field, [feature[db.names.T_ID_F]])
                    elif isinstance(field, RelatedOwnFieldObject):
                        node_fields_response[field.field_alias] = self._get_relate_own_field_object(db, field, [feature[db.names.T_ID_F]])
                    elif isinstance(field, RelatedOwnFieldValue):
                        node_fields_response[field.field_alias] = self._get_relate_own_field_value(db, field, [feature[db.names.T_ID_F]])

            for dict_key in level_dict:
                if dict_key.endswith(QueryNames.LEVEL_TABLE):
                    self._execute_query(db, node_fields_response, level_dict[dict_key], [feature[db.names.T_ID_F]])

            node_response[QueryNames.ATTRIBUTES_RESPONSE] = node_fields_response
            response[level_alias].append(node_response)

    def _get_relate_remote_field_object(self, db, field, filter_field_values):
        t_id_features = self._get_relate_own_field_object(db, field.filter_sub_level, filter_field_values)
        return self._get_relate_own_field_value(db, field, t_id_features)

    def _get_relate_remote_field_value(self, db, field, filter_field_values):
        t_id_features = self._get_features_ids_sub_level(db, field.filter_sub_level, filter_field_values)
        return self._get_relate_own_field_value(db, field, t_id_features)

    def _get_relate_own_field_object(self, db, field, filter_field_values):
        """
        Get relate own field object

        :param db: database connection instance
        :param field: AbsRelatedFields
        :param filter_field_values: list of field values used to apply the filter
        return list of dict with required fields
        """
        referenced_layer = self.app.core.get_layer(db, field.referenced_layer, False)
        dict_fields_and_alias =  self._get_dict_fields_and_alias(field.required_fields_referenced_layer)
        field_names = list(dict_fields_and_alias.keys())
        field_names.append(db.names.T_ID_F)

        features = self._get_features(referenced_layer, field.referenced_field, field_names, filter_field_values)

        list_result = list()
        for feature in features:
            dict_referenced_field = dict()
            dict_referenced_field[QueryNames.ID_FEATURE_RESPONSE] = feature[db.names.T_ID_F]
            dict_attributes = dict()
            for field_relation in field.required_fields_referenced_layer:
                if isinstance(field_relation, DomainOwnField):
                    domain_table = field_relation.domain_table
                    domain_code = feature[field_relation.field_name]
                    domain_value = self.ladm_data.get_domain_value_from_code(db, domain_table, domain_code, False)
                    dict_attributes[field_relation.field_alias] = domain_value
                elif isinstance(field_relation, OwnField):
                    dict_attributes[field_relation.field_alias] = feature[field_relation.field_name] if feature[field_relation.field_name] != NULL else None
                elif isinstance(field_relation, EvalExpressionOwnField):
                    dict_attributes[field_relation.field_alias] = self._get_eval_expr_value(referenced_layer, feature, field_relation.expression)

            dict_referenced_field[QueryNames.ATTRIBUTES_RESPONSE] = dict_attributes
            list_result.append(dict_referenced_field)

        return list_result

    def _get_relate_own_field_value(self, db, field, filter_field_values):
        """
        Get relate own field value.

        :param db: database connection instance
        :param field: AbsRelatedFields
        :param filter_field_values: list of field values used to apply the filter
        :return required field value
        """
        referenced_layer = self.app.core.get_layer(db, field.referenced_layer, False)
        required_field_referenced_layer = field.required_field_referenced_layer
        dict_fields_and_alias = self._get_dict_fields_and_alias([required_field_referenced_layer])
        field_names = list(dict_fields_and_alias.keys())
        field_names.append(db.names.T_ID_F)

        features = self._get_features(referenced_layer, field.referenced_field, field_names, filter_field_values)

        field_value = None
        for feature in features:
            if isinstance(required_field_referenced_layer, DomainOwnField):
                domain_table = required_field_referenced_layer.domain_table
                domain_code = feature[required_field_referenced_layer.field_name]
                domain_value = self.ladm_data.get_domain_value_from_code(db, domain_table, domain_code, False)
                field_value = domain_value
            elif isinstance(required_field_referenced_layer, OwnField):
                field_value = feature[required_field_referenced_layer.field_name] if feature[required_field_referenced_layer.field_name] != NULL else None
            elif isinstance(required_field_referenced_layer, EvalExpressionOwnField):
                field_value = self._get_eval_expr_value(referenced_layer, feature, required_field_referenced_layer.expression)

        return field_value

    def _get_features_ids_by_filter(self, db, filter_sub_level, filter_field_values):
        """
        Get feature ids using filter.

        :param db: database connection instance
        :param filter_sub_level: LADM Query filter
        :param filter_field_values: it is a list with only one item

        return list feature ids filters
        """
        referenced_layer = filter_sub_level.referenced_layer
        required_field_referenced_layer = filter_sub_level.required_field_referenced_layer
        sub_level_layer = self.app.core.get_layer(db, referenced_layer, False)

        if isinstance(filter_sub_level, FilterSubLevel):
            referenced_field = filter_sub_level.referenced_field
            expression = QgsExpression("{} in ({}) and {} is not null".format(referenced_field, ', '.join(str(filter_field_value) for filter_field_value in filter_field_values), required_field_referenced_layer))
            request = QgsFeatureRequest(expression)
            field_idx = sub_level_layer.fields().indexFromName(required_field_referenced_layer)
            request.setFlags(QgsFeatureRequest.NoGeometry)
            request.setSubsetOfAttributes([field_idx])  # Note: this adds a new flag
            feature_ids = [feature[required_field_referenced_layer] for feature in sub_level_layer.getFeatures(request)]
            return feature_ids

        elif isinstance(filter_sub_level, SpatialFilterSubLevel):
            referencing_layer = filter_sub_level.referencing_layer
            spatial_operation = filter_sub_level.spatial_operation
            level_layer = self.app.core.get_layer(db, referencing_layer, False)
            filter_level_layer = processing.run("native:extractbyattribute", {'INPUT': level_layer, 'FIELD': db.names.T_ID_F, 'OPERATOR': 0, 'VALUE': filter_field_values[0], 'OUTPUT': 'memory:'})['OUTPUT']

            parameters = {'INPUT': sub_level_layer, 'INTERSECT': filter_level_layer, 'OUTPUT': 'memory:'}
            if spatial_operation == EnumSpatialOperationType.INTERSECTS:
                parameters['PREDICATE'] = [0]  # Intersects
            elif spatial_operation == EnumSpatialOperationType.OVERLAPS:
                parameters['PREDICATE'] = [5]  # Overlaps
            elif spatial_operation == EnumSpatialOperationType.CONTAINS:
                parameters['PREDICATE'] = [1]  # Contains

            filter_sub_level_layer = processing.run("native:extractbylocation", parameters)['OUTPUT']

            feature_ids = [feature[required_field_referenced_layer] for feature in filter_sub_level_layer.getFeatures()]
            return feature_ids

    def _get_features_ids_sub_level(self, db, filter_sub_level, filter_field_values):
        """
        Get feature t_id values associated to sub level filter.
        This method is recursive and its recursion ends when all the filters it has nested are resolved.

        :param db: database connection instance
        :param filter_sub_level: custom LADM Query Filter
        :param filter_field_values: list of field values to be filtered
        return list of t_ids
        """
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

        return expression.evaluate(context)

    @staticmethod
    def _get_dict_fields_and_alias(table_fields):
        dict_fields_and_alias = dict()
        for required_table_field in table_fields:
            if isinstance(required_table_field, OwnField):
                dict_fields_and_alias[required_table_field.field_name] = required_table_field.field_alias
        return dict_fields_and_alias

    @staticmethod
    def _get_features(layer, referenced_field, field_names, t_id_features):
        if not t_id_features:
            return list()

        fields_idx = [layer.fields().indexFromName(field) for field in field_names]

        expression = QgsExpression('{} in ({})'.format(referenced_field, ', '.join( str(t_id_feature) for t_id_feature in t_id_features)))
        request = QgsFeatureRequest(expression)
        request.setFlags(QgsFeatureRequest.NoGeometry)
        request.setSubsetOfAttributes(fields_idx)  # Note: this adds a new flag

        features = [feature for feature in layer.getFeatures(request)]
        return features

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

    @staticmethod
    def get_duplicate_records_in_table(db, table_name, fields_to_check):
        raise NotImplementedError

    @staticmethod
    def get_group_party_fractions_that_do_not_make_one(db):
        raise NotImplementedError

    @staticmethod
    def get_invalid_col_party_type_natural(db):
        raise NotImplementedError

    @staticmethod
    def get_invalid_col_party_type_no_natural(db):
        raise NotImplementedError

    @staticmethod
    def get_parcels_with_invalid_department_code(db):
        raise NotImplementedError

    @staticmethod
    def get_parcels_with_invalid_municipality_code(db):
        raise NotImplementedError

    @staticmethod
    def get_parcels_with_invalid_parcel_number(db):
        raise NotImplementedError

    @staticmethod
    def get_parcels_with_invalid_parcel_type_and_22_position_number(db):
        raise NotImplementedError

    @staticmethod
    def get_parcels_with_invalid_previous_parcel_number(db):
        raise NotImplementedError

    @staticmethod
    def get_parcels_with_no_right(db):
        raise NotImplementedError

    @staticmethod
    def get_parcels_with_repeated_domain_right(db):
        raise NotImplementedError

    @staticmethod
    def get_uebaunit_parcel(db):
        raise NotImplementedError

    @staticmethod
    def get_inconsistent_building_units(db):
        raise NotImplementedError
