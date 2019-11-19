# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-03-20
        git sha              : :%H$
        copyright            : (C) 2019 by Germán Carrillo (BSF Swissphoto)
        email                : gcarrillo@linuxmail.org
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.core import (QgsApplication,
                       NULL,
                       QgsFeatureRequest,
                       QgsExpression,
                       QgsWkbTypes,
                       QgsFeature)
from asistente_ladm_col.config.general_config import (LAYER,
                                                      PLOT_GEOMETRY_KEY)
from asistente_ladm_col.config.table_mapping_config import Names
from asistente_ladm_col.lib.logger import Logger

# TODO: Update with correct field
# PROPERTY_RECORD_CARD_FIELDS_TO_COMPARE = [PROPERTY_RECORD_CARD_SECTOR_FIELD,
#                                           PROPERTY_RECORD_CARD_LOCALITY_FIELD,
#                                           PROPERTY_RECORD_CARD_BLOCK_TOWN_FIELD,
#                                           PROPERTY_RECORD_CARD_ECONOMIC_DESTINATION_FIELD]


class LADM_DATA():
    """
    High-level class to get related information from the LADM-COL database.
    """
    def __init__(self, qgis_utils):
        self.qgis_utils = qgis_utils
        self.logger = Logger()
        self.names = Names()

    def get_plots_related_to_parcels(self, db, t_ids, field_name, plot_layer=None, uebaunit_table=None):
        """
        :param db: DB Connector object
        :param t_ids: list of parcel t_ids
        :param field_name: The field name to get from DB for the matching features, use None for the QGIS internal ID
        :param plot_layer: Plot QGIS layer, in case it exists already in the caller
        :param uebaunit_table: UEBaunit QGIS table, in case it exists already in the caller
        :return: list of plot ids related to the parcel
        """
        layers = {
            self.names.OP_PLOT_T: {'name': self.names.OP_PLOT_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            self.names.COL_UE_BAUNIT_T: {'name': self.names.COL_UE_BAUNIT_T, 'geometry': None, LAYER: None}
        }

        if plot_layer is not None:
            del layers[self.names.OP_PLOT_T]
        if uebaunit_table is not None:
            del layers[self.names.COL_UE_BAUNIT_T]

        if layers:
            self.qgis_utils.get_layers(db, layers, load=True)
            if not layers:
                return None

            if self.names.OP_PLOT_T in layers:
                plot_layer = layers[self.names.OP_PLOT_T][LAYER]

            if self.names.COL_UE_BAUNIT_T in layers:
                uebaunit_table = layers[self.names.COL_UE_BAUNIT_T][LAYER]

        expression = QgsExpression("{} IN ('{}') AND {} IS NOT NULL".format(
                                                    self.names.COL_UE_BAUNIT_T_PARCEL_F,
                                                    "','".join([str(t_id) for t_id in t_ids]),
                                                    self.names.COL_UE_BAUNIT_T_OP_PLOT_F))
        features = self.get_features_by_expression(uebaunit_table, expression, with_attributes=True)

        plot_t_ids = list()
        for feature in features:
            plot_t_ids.append(feature[self.names.COL_UE_BAUNIT_T_OP_PLOT_F])

        if field_name == self.names.T_ID_F:
            return plot_t_ids

        plot_ids = list()
        expression = QgsExpression("{} IN ('{}')".format(self.names.T_ID_F, "','".join([str(id) for id in plot_t_ids])))

        if field_name is None:
            features = self.get_features_by_expression(plot_layer, expression)
        else:
            features = self.get_features_by_expression(plot_layer, expression, with_attributes=True)

        for feature in features:
            if field_name is None: # We are only interested in the QGIS internal id, no need to get other fields
                plot_ids.append(feature.id())
            else:
                field_found = plot_layer.fields().indexOf(field_name) != -1
                if field_found:
                    plot_ids.append(feature[field_name])

        return plot_ids

    def get_parcels_related_to_plots(self, db, t_ids, field_name, parcel_table=None, uebaunit_table=None):
        """
        :param db: DB Connector object
        :param t_ids: list of plot t_ids
        :param field_name: The field name to get from DB for the matching features, use None for the QGIS internal ID
        :param parcel_table: Parcel QGIS layer, in case it exists already in the caller
        :param uebaunit_table: UEBaunit QGIS table, in case it exists already in the caller
        :return: list of parcel ids related to the parcel
        """
        layers = {
            self.names.OP_PARCEL_T: {'name': self.names.OP_PARCEL_T, 'geometry': None, LAYER: None},
            self.names.COL_UE_BAUNIT_T: {'name': self.names.COL_UE_BAUNIT_T, 'geometry': None, LAYER: None}
        }

        if parcel_table is not None:
            del layers[self.names.OP_PARCEL_T]
        if uebaunit_table is not None:
            del layers[self.names.COL_UE_BAUNIT_T]

        if layers:
            self.qgis_utils.get_layers(db, layers, load=True)
            if not layers:
                return None

            if self.names.OP_PARCEL_T in layers:
                parcel_table = layers[self.names.OP_PARCEL_T][LAYER]

            if self.names.COL_UE_BAUNIT_T in layers:
                uebaunit_table = layers[self.names.COL_UE_BAUNIT_T][LAYER]


        expression = QgsExpression("{} IN ({}) AND {} IS NOT NULL".format(
                                                    self.names.COL_UE_BAUNIT_T_OP_PLOT_F,
                                                    ",".join([str(t_id) for t_id in t_ids]),
                                                    self.names.COL_UE_BAUNIT_T_PARCEL_F))
        features = self.get_features_by_expression(uebaunit_table, expression, with_attributes=True)

        parcel_t_ids = list()
        for feature in features:
            parcel_t_ids.append(feature[self.names.COL_UE_BAUNIT_T_PARCEL_F])

        if field_name == self.names.T_ID_F:
            return parcel_t_ids

        parcel_ids = list()
        expression = QgsExpression("{} IN ({})".format(self.names.T_ID_F,
                                                          ",".join([str(id) for id in parcel_t_ids])))

        if field_name is None:
            features = self.get_features_by_expression(parcel_table, expression)
        else:
            features = self.get_features_by_expression(parcel_table, expression, with_attributes=True)

        for feature in features:
            if field_name is None: # We are only interested in the QGIS internal id, no need to get other fields
                parcel_ids.append(feature.id())
            else:
                field_found = parcel_table.fields().indexOf(field_name) != -1
                if field_found:
                    parcel_ids.append(feature[field_name])

        return parcel_ids

    def get_parcel_data_to_compare_changes(self, db, search_criterion=None, layer_modifiers=dict()):
        """
        :param db: DB Connector object
        :param search_criterion: FieldName-Value pair to search in parcel layer (None for getting all parcels)
        :return: dict with parcel info for comparisons
        """
        parcel_fields_to_compare = self.get_parcel_fields_to_compare()
        party_fields_to_compare = self.get_party_fields_to_compare()
        plot_fields_to_compare = self.get_plot_fields_to_compare()
        layers = {
            self.names.OP_PARCEL_T: {'name': self.names.OP_PARCEL_T, 'geometry': None, LAYER: None},
            self.names.OP_PLOT_T: {'name': self.names.OP_PLOT_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            self.names.OP_RIGHT_T: {'name': self.names.OP_RIGHT_T, 'geometry': None, LAYER: None},
            self.names.OP_PARTY_T: {'name': self.names.OP_PARTY_T, 'geometry': None, LAYER: None},
            self.names.OP_GROUP_PARTY_T: {'name': self.names.OP_GROUP_PARTY_T, 'geometry': None, LAYER: None},
            self.names.COL_UE_BAUNIT_T: {'name': self.names.COL_UE_BAUNIT_T, 'geometry': None, LAYER: None},
            self.names.MEMBERS_T: {'name': self.names.MEMBERS_T, 'geometry': None, LAYER: None},
        }

        if db.cadastral_form_model_exists():
            # TODO: Replace property record card for correct table model
            # layers[PROPERTY_RECORD_CARD_TABLE] = {'name': PROPERTY_RECORD_CARD_TABLE, 'geometry': None, LAYER: None}
            pass

        self.qgis_utils.get_layers(db, layers, load=True, layer_modifiers=layer_modifiers)
        if not layers:
            return None

        parcel_features = self.get_features_by_search_criterion(layers[self.names.OP_PARCEL_T][LAYER], search_criterion=search_criterion, with_attributes=True)

        # ===================== Start adding parcel info ==================================================
        dict_features = dict()
        for feature in parcel_features:
            dict_attrs = dict()
            for field in layers[self.names.OP_PARCEL_T][LAYER].fields():
                if field.name() in parcel_fields_to_compare:
                    if field.name() == self.names.OP_PARCEL_T_PARCEL_TYPE_F:
                        # Go for domain value, instead of t_id
                        value = self.get_domain_value_from_code(db, self.names.OP_CONDITION_PARCEL_TYPE_D, feature.attribute(field.name()))
                    else:
                        value = feature.attribute(field.name())
                    dict_attrs[field.name()] = value

            dict_attrs[self.names.T_ID_F] = feature[self.names.T_ID_F]

            if dict_attrs[self.names.OP_PARCEL_T_PARCEL_NUMBER_F] in dict_features:
                dict_features[dict_attrs[self.names.OP_PARCEL_T_PARCEL_NUMBER_F]].append(dict_attrs)
            else:
                dict_features[dict_attrs[self.names.OP_PARCEL_T_PARCEL_NUMBER_F]] = [dict_attrs]

        # =====================  Start adding plot info ==================================================
        parcel_t_ids = [parcel_feature[self.names.T_ID_F] for parcel_feature in parcel_features]
        expression_uebaunit_features = QgsExpression("{} IN ({}) AND {} IS NOT NULL".format(self.names.COL_UE_BAUNIT_T_PARCEL_F, ",".join([str(id) for id in parcel_t_ids]), self.names.COL_UE_BAUNIT_T_OP_PLOT_F))
        uebaunit_features = self.get_features_by_expression(layers[self.names.COL_UE_BAUNIT_T][LAYER], expression_uebaunit_features, with_attributes=True)

        plot_t_ids = [feature[self.names.COL_UE_BAUNIT_T_OP_PLOT_F] for feature in uebaunit_features]
        expression_plot_features = QgsExpression("{} IN ('{}')".format(self.names.T_ID_F, "','".join([str(id) for id in plot_t_ids])))
        plot_features = self.get_features_by_expression(layers[self.names.OP_PLOT_T][LAYER], expression_plot_features, with_attributes=True, with_geometry=True)

        dict_parcel_plot = {uebaunit_feature[self.names.COL_UE_BAUNIT_T_PARCEL_F]: uebaunit_feature[self.names.COL_UE_BAUNIT_T_OP_PLOT_F] for uebaunit_feature in uebaunit_features}
        dict_plot_features = {plot_feature[self.names.T_ID_F]: plot_feature for plot_feature in plot_features}

        for feature in dict_features:
            for item in dict_features[feature]:
                if item[self.names.T_ID_F] in dict_parcel_plot:
                    if dict_parcel_plot[item[self.names.T_ID_F]] in dict_plot_features:
                        plot_feature = dict_plot_features[dict_parcel_plot[item[self.names.T_ID_F]]]
                        for plot_field in plot_fields_to_compare:
                            if plot_feature[plot_field] != NULL:
                                item[plot_field] = plot_feature[plot_field]
                            else:
                                item[plot_field] = NULL

                            item[PLOT_GEOMETRY_KEY] = plot_feature.geometry()
                else:
                    item[PLOT_GEOMETRY_KEY] = None  # No associated plot

        # ===================== Start adding party info ==================================================
        expression_right_features = QgsExpression("{} IN ({})".format(self.names.COL_BAUNIT_RRR_T_UNIT_F, ",".join([str(id) for id in parcel_t_ids])))
        right_features = self.get_features_by_expression(layers[self.names.OP_RIGHT_T][LAYER], expression_right_features, with_attributes=True)

        dict_party_right = {right_feature[self.names.COL_RRR_PARTY_T_OP_PARTY_F]: right_feature for right_feature in right_features if right_feature[self.names.COL_RRR_PARTY_T_OP_PARTY_F] != NULL}
        party_t_ids = [right_feature[self.names.COL_RRR_PARTY_T_OP_PARTY_F] for right_feature in right_features if right_feature[self.names.COL_RRR_PARTY_T_OP_PARTY_F] != NULL]
        expression_party_features = QgsExpression("{} IN ({})".format(self.names.T_ID_F, ",".join([str(id) for id in party_t_ids])))
        party_features = self.get_features_by_expression(layers[self.names.OP_PARTY_T][LAYER], expression_party_features, with_attributes=True)

        dict_parcel_parties = dict()
        for right_feature in right_features:
            if right_feature[self.names.COL_BAUNIT_RRR_T_UNIT_F] != NULL and right_feature[self.names.COL_RRR_PARTY_T_OP_PARTY_F] != NULL:
                if right_feature[self.names.COL_BAUNIT_RRR_T_UNIT_F] in dict_parcel_parties:
                    if right_feature[self.names.COL_RRR_PARTY_T_OP_PARTY_F] not in dict_parcel_parties[right_feature[self.names.COL_BAUNIT_RRR_T_UNIT_F]]:
                        dict_parcel_parties[right_feature[self.names.COL_BAUNIT_RRR_T_UNIT_F]].append(right_feature[self.names.COL_RRR_PARTY_T_OP_PARTY_F])
                else:
                    dict_parcel_parties[right_feature[self.names.COL_BAUNIT_RRR_T_UNIT_F]] = [right_feature[self.names.COL_RRR_PARTY_T_OP_PARTY_F]]

        dict_parties = dict()
        for party_feature in party_features:
            dict_party = dict()
            for party_field in party_fields_to_compare:
                if party_field == self.names.OP_PARTY_T_DOCUMENT_TYPE_F:
                    dict_party[party_field] = self.get_domain_value_from_code(db, self.names.OP_PARTY_DOCUMENT_TYPE_D, party_feature[party_field])
                else:
                    dict_party[party_field] = party_feature[party_field]
            # Add extra attribute from right table
            right_type_id = dict_party_right[party_feature[self.names.T_ID_F]][self.names.OP_RIGHT_T_TYPE_F]
            dict_party['derecho'] = self.get_domain_value_from_code(db, self.names.OP_RIGHT_TYPE_D, right_type_id)
            dict_parties[party_feature[self.names.T_ID_F]] = dict_party

        for id_parcel in dict_parcel_parties:
            party_info = list()
            for id_party in dict_parcel_parties[id_parcel]:
                if id_party in dict_parties:
                    party_info.append(dict_parties[id_party])

            dict_parcel_parties[id_parcel] = party_info

        # Append party info
        tag_party = self.names.get_dict_plural()[self.names.OP_PARTY_T]
        for feature in dict_features:
            for item in dict_features[feature]:
                if item[self.names.T_ID_F] in dict_parcel_parties:
                    # Make join
                    if tag_party in item:
                        item[tag_party].append(dict_parcel_parties[item[self.names.T_ID_F]])
                    else:
                        item[tag_party] = dict_parcel_parties[item[self.names.T_ID_F]]
                else:
                    item[tag_party] = NULL

        # =====================  Start add group party info ==================================================
        dict_parcel_group_parties = dict()  # {id_parcel: [id_group_party1, id_group_party2]}
        for right_feature in right_features:
            if right_feature[self.names.COL_BAUNIT_RRR_T_UNIT_F] != NULL and right_feature[self.names.COL_RRR_PARTY_T_OP_GROUP_PARTY_F] != NULL:
                if right_feature[self.names.COL_BAUNIT_RRR_T_UNIT_F] in dict_parcel_group_parties:
                    if right_feature[self.names.COL_RRR_PARTY_T_OP_GROUP_PARTY_F] not in dict_parcel_group_parties[right_feature[self.names.COL_BAUNIT_RRR_T_UNIT_F]]:
                        dict_parcel_group_parties[right_feature[self.names.COL_BAUNIT_RRR_T_UNIT_F]].append(right_feature[self.names.COL_RRR_PARTY_T_OP_GROUP_PARTY_F])
                else:
                    dict_parcel_group_parties[right_feature[self.names.COL_BAUNIT_RRR_T_UNIT_F]] = [right_feature[self.names.COL_RRR_PARTY_T_OP_GROUP_PARTY_F]]

        dict_group_party_right = {right_feature[self.names.COL_RRR_PARTY_T_OP_GROUP_PARTY_F]: right_feature for right_feature in right_features if right_feature[self.names.COL_RRR_PARTY_T_OP_GROUP_PARTY_F] != NULL}
        group_party_t_ids = [right_feature[self.names.COL_RRR_PARTY_T_OP_GROUP_PARTY_F] for right_feature in right_features if right_feature[self.names.COL_RRR_PARTY_T_OP_GROUP_PARTY_F] != NULL]
        expression_members_features = QgsExpression("{} IN ({})".format(self.names.MEMBERS_T_GROUP_PARTY_F, ",".join([str(id) for id in group_party_t_ids])))
        members_features = self.get_features_by_expression(layers[self.names.MEMBERS_T][LAYER], expression_members_features, with_attributes=True)

        dict_group_party_parties = dict()  # {id_group_party: [id_party1, id_party2]}
        for members_feature in members_features:
            if members_feature[self.names.MEMBERS_T_GROUP_PARTY_F] != NULL and members_feature[self.names.MEMBERS_T_PARTY_F] != NULL:
                if members_feature[self.names.MEMBERS_T_GROUP_PARTY_F] in dict_group_party_parties:
                    if members_feature[self.names.MEMBERS_T_PARTY_F] not in dict_group_party_parties[members_feature[self.names.MEMBERS_T_GROUP_PARTY_F]]:
                        dict_group_party_parties[members_feature[self.names.MEMBERS_T_GROUP_PARTY_F]].append(members_feature[self.names.MEMBERS_T_PARTY_F])
                else:
                    dict_group_party_parties[members_feature[self.names.MEMBERS_T_GROUP_PARTY_F]] = [members_feature[self.names.MEMBERS_T_PARTY_F]]

        party_t_ids = [members_feature[self.names.MEMBERS_T_PARTY_F] for members_feature in members_features if members_feature[self.names.MEMBERS_T_PARTY_F] != NULL]
        party_t_ids = list(set(party_t_ids))

        expression_party_features = QgsExpression("{} IN ({})".format(self.names.T_ID_F, ",".join([str(id) for id in party_t_ids])))
        party_features = self.get_features_by_expression(layers[self.names.OP_PARTY_T][LAYER], expression_party_features, with_attributes=True)

        dict_parties = dict()  # {id_party: {tipo_documento: CC, documento_identidad: 123456, nombre: Pepito}}
        for party_feature in party_features:
            dict_party = dict()
            for party_field in party_fields_to_compare:
                if party_field == self.names.OP_PARTY_T_DOCUMENT_TYPE_F:
                    dict_party[party_field] = self.get_domain_value_from_code(db, self.names.OP_PARTY_DOCUMENT_TYPE_D, party_feature[party_field])
                else:
                    dict_party[party_field] = party_feature[party_field]
            dict_parties[party_feature[self.names.T_ID_F]] = dict_party

        # Reuse the dict to replace id_group_party for party info:
        #   {id_group_party: [{tipo_documento: CC, documento_identidad: 123456, nombre: Pepito, 'derecho': Dominio}, ..., {}] }
        for id_group_party in dict_group_party_parties:
            party_info = list()
            for id_party in dict_group_party_parties[id_group_party]:
                if id_party in dict_parties:
                    # Add extra attribute from right table
                    right_type_id = dict_group_party_right[id_group_party][self.names.OP_RIGHT_T_TYPE_F]
                    dict_parties[id_party]['derecho'] = self.get_domain_value_from_code(db, self.names.OP_RIGHT_TYPE_D, right_type_id)
                    party_info.append(dict_parties[id_party])
            dict_group_party_parties[id_group_party] = party_info

        for id_parcel in dict_parcel_group_parties:
            group_party_info = list()
            for id_group_party in dict_parcel_group_parties[id_parcel]:
                if id_group_party in dict_group_party_parties:
                    for party_info in dict_group_party_parties[id_group_party]:
                        group_party_info.append(party_info)
            dict_parcel_group_parties[id_parcel] = group_party_info

        # Append group party info
        tag_group_party = self.names.get_dict_plural()[self.names.OP_PARTY_T]
        for feature in dict_features:
            for item in dict_features[feature]:
                if item[self.names.T_ID_F] in dict_parcel_group_parties:
                    # Make join
                    if tag_group_party in item:
                        if item[tag_group_party]:
                            for info in dict_parcel_group_parties[item[self.names.T_ID_F]]:
                                item[tag_group_party].append(info)
                        else:
                            item[tag_group_party] = dict_parcel_group_parties[item[self.names.T_ID_F]]
                    else:
                        item[tag_group_party] = dict_parcel_group_parties[item[self.names.T_ID_F]]

        # =====================  Start add record card info ==================================================
        # TODO: Replace property record card for correct table model
        # if db.cadastral_form_model_exists():
        #     expr_property_record_card_features = QgsExpression("{} IN ({})".format(PROPERTY_RECORD_CARD_PARCEL_ID_FIELD, ",".join([str(id) for id in parcel_t_ids])))
        #     property_record_card_features = self.get_features_by_expression(layers[PROPERTY_RECORD_CARD_TABLE][LAYER], expr_property_record_card_features, with_attributes=True)
        #
        #     dict_property_record_card_features = {property_record_card_feature[PROPERTY_RECORD_CARD_PARCEL_ID_FIELD]: property_record_card_feature for property_record_card_feature in property_record_card_features}
        #
        #     for feature in dict_features:
        #         for item in dict_features[feature]:
        #             if item[self.names.T_ID_F] in dict_property_record_card_features:
        #                 property_record_card_feature = dict_property_record_card_features[item[self.names.T_ID_F]]
        #                 for PROPERTY_RECORD_CARD_FIELD in PROPERTY_RECORD_CARD_FIELDS_TO_COMPARE:
        #                     if property_record_card_feature[PROPERTY_RECORD_CARD_FIELD] != NULL:
        #                         item[PROPERTY_RECORD_CARD_FIELD] = property_record_card_feature[PROPERTY_RECORD_CARD_FIELD]
        #                     else:
        #                         item[PROPERTY_RECORD_CARD_FIELD] = NULL

        return dict_features

    def get_features_by_search_criterion(self, layer, search_criterion=None, with_attributes=False, with_geometry=False):
        if search_criterion is not None:
            field_name = list(search_criterion.keys())[0]
            field_value = list(search_criterion.values())[0]
            expression = QgsExpression("{}='{}'".format(field_name, field_value))
            features = self.get_features_by_expression(layer, expression=expression, with_attributes=with_attributes, with_geometry=with_geometry)
        else:
            features = self.get_features_by_expression(layer, with_attributes=with_attributes, with_geometry=with_geometry)

        return features

    def get_features_by_expression(self, layer, expression=None, with_attributes=False, with_geometry=False):
        # TODO: It should be possible to pass a list of attributes to retrieve

        if expression is None:
            request = QgsFeatureRequest()
        else:
            request = QgsFeatureRequest(expression)

        if not with_geometry:
            request.setFlags(QgsFeatureRequest.NoGeometry)
        if not with_attributes:
            field_idx = layer.fields().indexFromName(self.names.T_ID_F)
            request.setSubsetOfAttributes([field_idx])  # Note: this adds a new flag

        return [feature for feature in layer.getFeatures(request)]

    def get_features_from_t_ids(self, layer, t_ids, no_attributes=False, no_geometry=False):
        request = QgsFeatureRequest(QgsExpression("{} IN ('{}')".format(self.names.T_ID_F, "','".join([str(t_id) for t_id in t_ids]))))

        if no_geometry:
            request.setFlags(QgsFeatureRequest.NoGeometry)
        if no_attributes:
            field_idx = layer.fields().indexFromName(self.names.T_ID_F)
            request.setSubsetOfAttributes([field_idx])  # Note: this adds a new flag

        return [feature for feature in layer.getFeatures(request)]

    def get_parcel_fields_to_compare(self):
        return [self.names.OP_PARCEL_T_PARCEL_NUMBER_F,
                self.names.OP_PARCEL_T_FMI_F,
                self.names.COL_BAUNIT_T_NAME_F,
                self.names.OP_PARCEL_T_DEPARTMENT_F,
                self.names.OP_PARCEL_T_PARCEL_TYPE_F]

    def get_party_fields_to_compare(self):
        return [self.names.OP_PARTY_T_DOCUMENT_TYPE_F,  # Right type will also be added to parties
                self.names.OP_PARTY_T_DOCUMENT_ID_F,
                self.names.COL_PARTY_T_NAME_F]

    def get_plot_fields_to_compare(self):
        return [self.names.OP_PLOT_T_PLOT_AREA_F]  # Geometry is also used but handled differently

    def get_domain_code_from_value(self, db, domain_table, value, value_is_ilicode=True):
        """
        Get the t_id corresponding to a domain value. First look at the response in a cache.

        :param db: DB Connector object.
        :param domain_table: Table name or QgsVectorLayer
        :param value: Value to search in the domain.
        :param value_is_ilicode: Whether is an iliCode or a display name.
        :return: The t_id corresponding to the given value or None.
        """
        res = None
        domain_table_name = ''

        if type(domain_table) is str:
            domain_table_name = domain_table
        else:  # QgsVectorLayer
            domain_table_name = domain_table.name()

        # Try to get it from cache
        cached_res = self.names.get_domain_code(domain_table_name, value)
        if cached_res is not None:
            self.logger.debug(__name__, "(From cache!) Get domain ({}) code from {} ({}): {}".format(
                domain_table_name, db.names.ILICODE_F if value_is_ilicode else db.names.DISPLAY_NAME_F, value, cached_res))
            return cached_res

        if type(domain_table_name) is str:
            domain_table = self.qgis_utils.get_layer(db, domain_table, None, True, emit_map_freeze=False)

        if domain_table is not None:
            domain_table_name = domain_table.name()

            expression = "\"{}\" = '{}'".format(db.names.ILICODE_F if value_is_ilicode else db.names.DISPLAY_NAME_F, value)
            request = QgsFeatureRequest(QgsExpression(expression))
            request.setSubsetOfAttributes([db.names.T_ID_F], domain_table.fields())

            features = domain_table.getFeatures(request)
            feature = QgsFeature()
            if features.nextFeature(feature):
                res = feature[db.names.T_ID_F]
                if res is not None:
                    self.names.cache_domain_value(domain_table_name, res, value)

        self.logger.debug(__name__, "Get domain ({}) code from {} ({}): {}".format(
            domain_table_name, db.names.ILICODE_F if value_is_ilicode else db.names.DISPLAY_NAME_F, value, res))

        return res

    def get_domain_value_from_code(self, db, domain_table, code, value_is_ilicode=True):
        """
        Get the domain value corresponding to a t_id. First look at the response in a cache.

        :param db: DB Connector object.
        :param domain_table: Table name or QgsVectorLayer
        :param value: t_id to search in the domain.
        :param value_is_ilicode: Whether the result should be iliCode or display name.
        :return: The value corresponding to the given t_id or None.
        """
        res = None
        domain_table_name = ''

        if type(domain_table) is str:
            domain_table_name = domain_table
        else:  # QgsVectorLayer
            domain_table_name = domain_table.name()

        # Try to get it from cache
        cached_res = self.names.get_domain_value(domain_table_name, code)
        if cached_res is not None:
            self.logger.debug(__name__, "(From cache!) Get domain ({}) {} from code ({}): {}".format(
                domain_table_name, db.names.ILICODE_F if value_is_ilicode else db.names.DISPLAY_NAME_F, code, cached_res))
            return cached_res

        if type(domain_table) is str:
            domain_table = self.qgis_utils.get_layer(db, domain_table, None, True, emit_map_freeze=False)

        if domain_table is not None:
            features = self.get_features_from_t_ids(domain_table, [code], no_attributes=False, no_geometry=True)
            if features:
                res = features[0][db.names.ILICODE_F if value_is_ilicode else db.names.DISPLAY_NAME_F]
                if res is not None:
                    self.names.cache_domain_value(domain_table_name, code, res)

        self.logger.debug(__name__, "Get domain ({}) {} from code ({}): {}".format(
            domain_table_name, db.names.ILICODE_F if value_is_ilicode else db.names.DISPLAY_NAME_F, code, res))

        return res