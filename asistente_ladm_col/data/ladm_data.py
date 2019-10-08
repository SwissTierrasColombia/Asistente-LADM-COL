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
                       QgsWkbTypes)
from ..config.general_config import (LAYER,
                                     PLOT_GEOMETRY_KEY)
from ..config.table_mapping_config import (ID_FIELD,
                                           DICT_PLURAL,
                                           PLOT_TABLE,
                                           PLOT_CALCULATED_AREA_FIELD,
                                           RIGHT_TABLE,
                                           RIGHT_TABLE_PARCEL_FIELD,
                                           RIGHT_TABLE_PARTY_FIELD,
                                           RIGHT_TABLE_GROUP_PARTY_FIELD,
                                           RIGHT_TABLE_TYPE_FIELD,
                                           COL_PARTY_TABLE,
                                           COL_PARTY_DOC_TYPE_FIELD,
                                           LA_GROUP_PARTY_TABLE,
                                           MEMBERS_TABLE,
                                           MEMBERS_PARTY_FIELD,
                                           MEMBERS_GROUP_PARTY_FIELD,
                                           DOCUMENT_ID_FIELD,
                                           COL_PARTY_NAME_FIELD,
                                           UEBAUNIT_TABLE_PARCEL_FIELD,
                                           UEBAUNIT_TABLE_PLOT_FIELD,
                                           UEBAUNIT_TABLE,
                                           PARCEL_TABLE,
                                           PARCEL_NUMBER_FIELD,
                                           PROPERTY_RECORD_CARD_TABLE,
                                           PROPERTY_RECORD_CARD_PARCEL_ID_FIELD,
                                           PROPERTY_RECORD_CARD_SECTOR_FIELD,
                                           PROPERTY_RECORD_CARD_BLOCK_TOWN_FIELD,
                                           PROPERTY_RECORD_CARD_ECONOMIC_DESTINATION_FIELD,
                                           PROPERTY_RECORD_CARD_LOCALITY_FIELD,
                                           FMI_FIELD,
                                           PARCEL_NAME_FIELD,
                                           DEPARTMENT_FIELD,
                                           ZONE_FIELD,
                                           PARCEL_TYPE_FIELD,
                                           MUNICIPALITY_FIELD)

PARCEL_FIELDS_TO_COMPARE = [PARCEL_NUMBER_FIELD,
                            PARCEL_TYPE_FIELD,
                            FMI_FIELD,
                            PARCEL_NAME_FIELD,
                            DEPARTMENT_FIELD,
                            MUNICIPALITY_FIELD,
                            ZONE_FIELD,
                            #NUPRE_FIELD,
                            PARCEL_TYPE_FIELD]

PARTY_FIELDS_TO_COMPARE = [COL_PARTY_DOC_TYPE_FIELD,  # Right type will also be added to parties
                           DOCUMENT_ID_FIELD,
                           COL_PARTY_NAME_FIELD]

PLOT_FIELDS_TO_COMPARE = [PLOT_CALCULATED_AREA_FIELD]  # Geometry is also used but handled differenlty

PROPERTY_RECORD_CARD_FIELDS_TO_COMPARE = [PROPERTY_RECORD_CARD_SECTOR_FIELD,
                                          PROPERTY_RECORD_CARD_LOCALITY_FIELD,
                                          PROPERTY_RECORD_CARD_BLOCK_TOWN_FIELD,
                                          PROPERTY_RECORD_CARD_ECONOMIC_DESTINATION_FIELD]


class LADM_DATA():
    """
    High-level class to get related information from the LADM-COL database.
    """
    def __init__(self, qgis_utils):
        self.qgis_utils = qgis_utils
        self.log = QgsApplication.messageLog()

    def get_plots_related_to_parcels(self, db, t_ids, field_name=ID_FIELD, plot_layer=None, uebaunit_table=None):
        """
        :param db: DB Connector object
        :param t_ids: list of parcel t_ids
        :param field_name: The field name to get from DB for the matching features, use None for the QGIS internal ID
        :param plot_layer: Plot QGIS layer, in case it exists already in the caller
        :param uebaunit_table: UEBaunit QGIS table, in case it exists already in the caller
        :return: list of plot ids related to the parcel
        """
        layers = {
            PLOT_TABLE: {'name': PLOT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            UEBAUNIT_TABLE: {'name': UEBAUNIT_TABLE, 'geometry': None, LAYER: None}
        }

        if plot_layer is not None:
            del layers[PLOT_TABLE]
        if uebaunit_table is not None:
            del layers[UEBAUNIT_TABLE]

        if layers:
            self.qgis_utils.get_layers(db, layers, load=True)
            if not layers:
                return None

            if PLOT_TABLE in layers:
                plot_layer = layers[PLOT_TABLE][LAYER]

            if UEBAUNIT_TABLE in layers:
                uebaunit_table = layers[UEBAUNIT_TABLE][LAYER]

        expression = QgsExpression("{} IN ('{}') AND {} IS NOT NULL".format(
                                                    UEBAUNIT_TABLE_PARCEL_FIELD,
                                                    "','".join([str(t_id) for t_id in t_ids]),
                                                    UEBAUNIT_TABLE_PLOT_FIELD))
        features = LADM_DATA.get_features_by_expression(uebaunit_table, expression, with_attributes=True)

        plot_t_ids = list()
        for feature in features:
            plot_t_ids.append(feature[UEBAUNIT_TABLE_PLOT_FIELD])

        if field_name == ID_FIELD:
            return plot_t_ids

        plot_ids = list()
        expression = QgsExpression("{} IN ('{}')".format(ID_FIELD, "','".join([str(id) for id in plot_t_ids])))

        if field_name is None:
            features = LADM_DATA.get_features_by_expression(plot_layer, expression)
        else:
            features = LADM_DATA.get_features_by_expression(plot_layer, expression, with_attributes=True)

        for feature in features:
            if field_name is None: # We are only interested in the QGIS internal id, no need to get other fields
                plot_ids.append(feature.id())
            else:
                field_found = plot_layer.fields().indexOf(field_name) != -1
                if field_found:
                    plot_ids.append(feature[field_name])

        return plot_ids

    def get_parcels_related_to_plots(self, db, t_ids, field_name=ID_FIELD, parcel_table=None, uebaunit_table=None):
        """
        :param db: DB Connector object
        :param t_ids: list of plot t_ids
        :param field_name: The field name to get from DB for the matching features, use None for the QGIS internal ID
        :param parcel_table: Parcel QGIS layer, in case it exists already in the caller
        :param uebaunit_table: UEBaunit QGIS table, in case it exists already in the caller
        :return: list of parcel ids related to the parcel
        """
        layers = {
            PARCEL_TABLE: {'name': PARCEL_TABLE, 'geometry': None, LAYER: None},
            UEBAUNIT_TABLE: {'name': UEBAUNIT_TABLE, 'geometry': None, LAYER: None}
        }

        if parcel_table is not None:
            del layers[PARCEL_TABLE]
        if uebaunit_table is not None:
            del layers[UEBAUNIT_TABLE]

        if layers:
            self.qgis_utils.get_layers(db, layers, load=True)
            if not layers:
                return None

            if PARCEL_TABLE in layers:
                parcel_table = layers[PARCEL_TABLE][LAYER]

            if UEBAUNIT_TABLE in layers:
                uebaunit_table = layers[UEBAUNIT_TABLE][LAYER]


        expression = QgsExpression("{} IN ({}) AND {} IS NOT NULL".format(
                                                    UEBAUNIT_TABLE_PLOT_FIELD,
                                                    ",".join([str(t_id) for t_id in t_ids]),
                                                    UEBAUNIT_TABLE_PARCEL_FIELD))
        features = LADM_DATA.get_features_by_expression(uebaunit_table, expression, with_attributes=True)

        parcel_t_ids = list()
        for feature in features:
            parcel_t_ids.append(feature[UEBAUNIT_TABLE_PARCEL_FIELD])

        if field_name == ID_FIELD:
            return parcel_t_ids

        parcel_ids = list()
        expression = QgsExpression("{} IN ({})".format(ID_FIELD,
                                                          ",".join([str(id) for id in parcel_t_ids])))

        if field_name is None:
            features = LADM_DATA.get_features_by_expression(parcel_table, expression)
        else:
            features = LADM_DATA.get_features_by_expression(parcel_table, expression, with_attributes=True)

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
        layers = {
            PARCEL_TABLE: {'name': PARCEL_TABLE, 'geometry': None, LAYER: None},
            PLOT_TABLE: {'name': PLOT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            RIGHT_TABLE: {'name': RIGHT_TABLE, 'geometry': None, LAYER: None},
            COL_PARTY_TABLE: {'name': COL_PARTY_TABLE, 'geometry': None, LAYER: None},
            LA_GROUP_PARTY_TABLE: {'name': LA_GROUP_PARTY_TABLE, 'geometry': None, LAYER: None},
            UEBAUNIT_TABLE: {'name': UEBAUNIT_TABLE, 'geometry': None, LAYER: None},
            MEMBERS_TABLE: {'name': MEMBERS_TABLE, 'geometry': None, LAYER: None},
        }

        if db.cadastral_form_model_exists():
            layers[PROPERTY_RECORD_CARD_TABLE] = {'name': PROPERTY_RECORD_CARD_TABLE, 'geometry': None, LAYER: None}

        self.qgis_utils.get_layers(db, layers, load=True, layer_modifiers=layer_modifiers)
        if not layers:
            return None

        parcel_features = LADM_DATA.get_features_by_search_criterion(layers[PARCEL_TABLE][LAYER], search_criterion=search_criterion, with_attributes=True)

        # ===================== Start adding parcel info ==================================================
        dict_features = dict()
        for feature in parcel_features:
            dict_attrs = dict()
            for field in layers[PARCEL_TABLE][LAYER].fields():
                if field.name() in PARCEL_FIELDS_TO_COMPARE:
                    value = feature.attribute(field.name())
                    dict_attrs[field.name()] = value

            dict_attrs[ID_FIELD] = feature[ID_FIELD]

            if dict_attrs[PARCEL_NUMBER_FIELD] in dict_features:
                dict_features[dict_attrs[PARCEL_NUMBER_FIELD]].append(dict_attrs)
            else:
                dict_features[dict_attrs[PARCEL_NUMBER_FIELD]] = [dict_attrs]

        # =====================  Start adding plot info ==================================================
        parcel_t_ids = [parcel_feature[ID_FIELD] for parcel_feature in parcel_features]
        expression_uebaunit_features = QgsExpression("{} IN ({}) AND {} IS NOT NULL".format(UEBAUNIT_TABLE_PARCEL_FIELD, ",".join([str(id) for id in parcel_t_ids]), UEBAUNIT_TABLE_PLOT_FIELD))
        uebaunit_features = LADM_DATA.get_features_by_expression(layers[UEBAUNIT_TABLE][LAYER], expression_uebaunit_features, with_attributes=True)

        plot_t_ids = [feature[UEBAUNIT_TABLE_PLOT_FIELD] for feature in uebaunit_features]
        expression_plot_features = QgsExpression("{} IN ('{}')".format(ID_FIELD, "','".join([str(id) for id in plot_t_ids])))
        plot_features = LADM_DATA.get_features_by_expression(layers[PLOT_TABLE][LAYER], expression_plot_features, with_attributes=True, with_geometry=True)

        dict_parcel_plot = {uebaunit_feature[UEBAUNIT_TABLE_PARCEL_FIELD]: uebaunit_feature[UEBAUNIT_TABLE_PLOT_FIELD] for uebaunit_feature in uebaunit_features}
        dict_plot_features = {plot_feature[ID_FIELD]: plot_feature for plot_feature in plot_features}

        for feature in dict_features:
            for item in dict_features[feature]:
                if item[ID_FIELD] in dict_parcel_plot:
                    if dict_parcel_plot[item[ID_FIELD]] in dict_plot_features:
                        plot_feature = dict_plot_features[dict_parcel_plot[item[ID_FIELD]]]
                        for PLOT_FIELD in PLOT_FIELDS_TO_COMPARE:
                            if plot_feature[PLOT_FIELD] != NULL:
                                item[PLOT_FIELD] = plot_feature[PLOT_FIELD]
                            else:
                                item[PLOT_FIELD] = NULL

                            item[PLOT_GEOMETRY_KEY] = plot_feature.geometry()
                else:
                    item[PLOT_GEOMETRY_KEY] = None  # No associated plot

        # ===================== Start adding party info ==================================================
        expression_right_features = QgsExpression("{} IN ({})".format(RIGHT_TABLE_PARCEL_FIELD, ",".join([str(id) for id in parcel_t_ids])))
        right_features = LADM_DATA.get_features_by_expression(layers[RIGHT_TABLE][LAYER], expression_right_features, with_attributes=True)

        dict_party_right = {right_feature[RIGHT_TABLE_PARTY_FIELD]: right_feature for right_feature in right_features if right_feature[RIGHT_TABLE_PARTY_FIELD] != NULL}
        party_t_ids = [right_feature[RIGHT_TABLE_PARTY_FIELD] for right_feature in right_features if right_feature[RIGHT_TABLE_PARTY_FIELD] != NULL]
        expression_party_features = QgsExpression("{} IN ({})".format(ID_FIELD, ",".join([str(id) for id in party_t_ids])))
        party_features = LADM_DATA.get_features_by_expression(layers[COL_PARTY_TABLE][LAYER], expression_party_features, with_attributes=True)

        dict_parcel_parties = dict()
        for right_feature in right_features:
            if right_feature[RIGHT_TABLE_PARCEL_FIELD] != NULL and right_feature[RIGHT_TABLE_PARTY_FIELD] != NULL:
                if right_feature[RIGHT_TABLE_PARCEL_FIELD] in dict_parcel_parties:
                    if right_feature[RIGHT_TABLE_PARTY_FIELD] not in dict_parcel_parties[right_feature[RIGHT_TABLE_PARCEL_FIELD]]:
                        dict_parcel_parties[right_feature[RIGHT_TABLE_PARCEL_FIELD]].append(right_feature[RIGHT_TABLE_PARTY_FIELD])
                else:
                    dict_parcel_parties[right_feature[RIGHT_TABLE_PARCEL_FIELD]] = [right_feature[RIGHT_TABLE_PARTY_FIELD]]

        dict_parties = dict()
        for party_feature in party_features:
            dict_party = dict()
            for PARTY_FIELD in PARTY_FIELDS_TO_COMPARE:
                dict_party[PARTY_FIELD] = party_feature[PARTY_FIELD]
            # Add extra attribute from right table
            dict_party['derecho'] = dict_party_right[party_feature[ID_FIELD]][RIGHT_TABLE_TYPE_FIELD]
            dict_parties[party_feature[ID_FIELD]] = dict_party

        for id_parcel in dict_parcel_parties:
            party_info = list()
            for id_party in dict_parcel_parties[id_parcel]:
                if id_party in dict_parties:
                    party_info.append(dict_parties[id_party])

            dict_parcel_parties[id_parcel] = party_info

        # Append party info
        tag_party = DICT_PLURAL[COL_PARTY_TABLE]
        for feature in dict_features:
            for item in dict_features[feature]:
                if item[ID_FIELD] in dict_parcel_parties:
                    # Make join
                    if tag_party in item:
                        item[tag_party].append(dict_parcel_parties[item[ID_FIELD]])
                    else:
                        item[tag_party] = dict_parcel_parties[item[ID_FIELD]]
                else:
                    item[tag_party] = NULL

        # =====================  Start add group party info ==================================================
        dict_parcel_group_parties = dict()  # {id_parcel: [id_group_party1, id_group_party2]}
        for right_feature in right_features:
            if right_feature[RIGHT_TABLE_PARCEL_FIELD] != NULL and right_feature[RIGHT_TABLE_GROUP_PARTY_FIELD] != NULL:
                if right_feature[RIGHT_TABLE_PARCEL_FIELD] in dict_parcel_group_parties:
                    if right_feature[RIGHT_TABLE_GROUP_PARTY_FIELD] not in dict_parcel_group_parties[right_feature[RIGHT_TABLE_PARCEL_FIELD]]:
                        dict_parcel_group_parties[right_feature[RIGHT_TABLE_PARCEL_FIELD]].append(right_feature[RIGHT_TABLE_GROUP_PARTY_FIELD])
                else:
                    dict_parcel_group_parties[right_feature[RIGHT_TABLE_PARCEL_FIELD]] = [right_feature[RIGHT_TABLE_GROUP_PARTY_FIELD]]

        dict_group_party_right = {right_feature[RIGHT_TABLE_GROUP_PARTY_FIELD]: right_feature for right_feature in right_features if right_feature[RIGHT_TABLE_GROUP_PARTY_FIELD] != NULL}
        group_party_t_ids = [right_feature[RIGHT_TABLE_GROUP_PARTY_FIELD] for right_feature in right_features if right_feature[RIGHT_TABLE_GROUP_PARTY_FIELD] != NULL]
        expression_members_features = QgsExpression("{} IN ({})".format(MEMBERS_GROUP_PARTY_FIELD, ",".join([str(id) for id in group_party_t_ids])))
        members_features = LADM_DATA.get_features_by_expression(layers[MEMBERS_TABLE][LAYER], expression_members_features, with_attributes=True)

        dict_group_party_parties = dict()  # {id_group_party: [id_party1, id_party2]}
        for members_feature in members_features:
            if members_feature[MEMBERS_GROUP_PARTY_FIELD] != NULL and members_feature[MEMBERS_PARTY_FIELD] != NULL:
                if members_feature[MEMBERS_GROUP_PARTY_FIELD] in dict_group_party_parties:
                    if members_feature[MEMBERS_PARTY_FIELD] not in dict_group_party_parties[members_feature[MEMBERS_GROUP_PARTY_FIELD]]:
                        dict_group_party_parties[members_feature[MEMBERS_GROUP_PARTY_FIELD]].append(members_feature[MEMBERS_PARTY_FIELD])
                else:
                    dict_group_party_parties[members_feature[MEMBERS_GROUP_PARTY_FIELD]] = [members_feature[MEMBERS_PARTY_FIELD]]

        party_t_ids = [members_feature[MEMBERS_PARTY_FIELD] for members_feature in members_features if members_feature[MEMBERS_PARTY_FIELD] != NULL]
        party_t_ids = list(set(party_t_ids))

        expression_party_features = QgsExpression("{} IN ({})".format(ID_FIELD, ",".join([str(id) for id in party_t_ids])))
        party_features = LADM_DATA.get_features_by_expression(layers[COL_PARTY_TABLE][LAYER], expression_party_features, with_attributes=True)

        dict_parties = dict()  # {id_party: {tipo_documento: CC, documento_identidad: 123456, nombre: Pepito}}
        for party_feature in party_features:
            dict_party = dict()
            for PARTY_FIELD in PARTY_FIELDS_TO_COMPARE:
                dict_party[PARTY_FIELD] = party_feature[PARTY_FIELD]
            dict_parties[party_feature[ID_FIELD]] = dict_party

        # Reuse the dict to replace id_group_party for party info:
        #   {id_group_party: [{tipo_documento: CC, documento_identidad: 123456, nombre: Pepito, 'derecho': Dominio}, ..., {}] }
        for id_group_party in dict_group_party_parties:
            party_info = list()
            for id_party in dict_group_party_parties[id_group_party]:
                if id_party in dict_parties:
                    # Add extra attribute from right table
                    dict_parties[id_party]['derecho'] = dict_group_party_right[id_group_party][RIGHT_TABLE_TYPE_FIELD]
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
        tag_group_party = DICT_PLURAL[COL_PARTY_TABLE]
        for feature in dict_features:
            for item in dict_features[feature]:
                if item[ID_FIELD] in dict_parcel_group_parties:
                    # Make join
                    if tag_group_party in item:
                        if item[tag_group_party]:
                            for info in dict_parcel_group_parties[item[ID_FIELD]]:
                                item[tag_group_party].append(info)
                        else:
                            item[tag_group_party] = dict_parcel_group_parties[item[ID_FIELD]]
                    else:
                        item[tag_group_party] = dict_parcel_group_parties[item[ID_FIELD]]

        # =====================  Start add record card info ==================================================
        if db.cadastral_form_model_exists():
            expr_property_record_card_features = QgsExpression("{} IN ({})".format(PROPERTY_RECORD_CARD_PARCEL_ID_FIELD, ",".join([str(id) for id in parcel_t_ids])))
            property_record_card_features = LADM_DATA.get_features_by_expression(layers[PROPERTY_RECORD_CARD_TABLE][LAYER], expr_property_record_card_features, with_attributes=True)

            dict_property_record_card_features = {property_record_card_feature[PROPERTY_RECORD_CARD_PARCEL_ID_FIELD]: property_record_card_feature for property_record_card_feature in property_record_card_features}

            for feature in dict_features:
                for item in dict_features[feature]:
                    if item[ID_FIELD] in dict_property_record_card_features:
                        property_record_card_feature = dict_property_record_card_features[item[ID_FIELD]]
                        for PROPERTY_RECORD_CARD_FIELD in PROPERTY_RECORD_CARD_FIELDS_TO_COMPARE:
                            if property_record_card_feature[PROPERTY_RECORD_CARD_FIELD] != NULL:
                                item[PROPERTY_RECORD_CARD_FIELD] = property_record_card_feature[PROPERTY_RECORD_CARD_FIELD]
                            else:
                                item[PROPERTY_RECORD_CARD_FIELD] = NULL

        return dict_features

    @staticmethod
    def get_features_by_search_criterion(layer, search_criterion=None, with_attributes=False, with_geometry=False):
        if search_criterion is not None:
            field_name = list(search_criterion.keys())[0]
            field_value = list(search_criterion.values())[0]
            expression = QgsExpression("{}='{}'".format(field_name, field_value))
            features = LADM_DATA.get_features_by_expression(layer, expression=expression, with_attributes=with_attributes, with_geometry=with_geometry)
        else:
            features = LADM_DATA.get_features_by_expression(layer, with_attributes=with_attributes, with_geometry=with_geometry)

        return features

    @staticmethod
    def get_features_by_expression(layer, expression=None, with_attributes=False, with_geometry=False):
        # TODO: It should be possible to pass a list of attributes to retrieve

        if expression is None:
            request = QgsFeatureRequest()
        else:
            request = QgsFeatureRequest(expression)

        if not with_geometry:
            request.setFlags(QgsFeatureRequest.NoGeometry)
        if not with_attributes:
            field_idx = layer.fields().indexFromName(ID_FIELD)
            request.setSubsetOfAttributes([field_idx])  # Note: this adds a new flag

        return [feature for feature in layer.getFeatures(request)]

    def get_features_from_t_ids(self, layer, t_ids, no_attributes=False, no_geometry=False):
        request = QgsFeatureRequest(QgsExpression("{} IN ('{}')".format(ID_FIELD, "','".join([str(t_id) for t_id in t_ids]))))

        if no_geometry:
            request.setFlags(QgsFeatureRequest.NoGeometry)
        if no_attributes:
            field_idx = layer.fields().indexFromName(ID_FIELD)
            request.setSubsetOfAttributes([field_idx])  # Note: this adds a new flag

        return [feature for feature in layer.getFeatures(request)]
