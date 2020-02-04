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
from qgis.core import (NULL,
                       QgsFeatureRequest,
                       QgsExpression,
                       QgsWkbTypes,
                       QgsFeature)
from asistente_ladm_col.config.general_config import LAYER
from asistente_ladm_col.config.gui.change_detection_config import (PLOT_GEOMETRY_KEY,
                                                                   DICT_KEY_PARTIES,
                                                                   DICT_KEY_PARCEL_T_DEPARTMENT_F,
                                                                   DICT_KEY_PARCEL_T_FMI_F,
                                                                   DICT_KEY_PARCEL_T_PARCEL_NUMBER_F,
                                                                   DICT_KEY_PARCEL_T_CONDITION_F,
                                                                   DICT_KEY_PARCEL_T_NAME_F,
                                                                   DICT_KEY_PARTY_T_DOCUMENT_TYPE_F,
                                                                   DICT_KEY_PARTY_T_DOCUMENT_ID_F,
                                                                   DICT_KEY_PARTY_T_NAME_F,
                                                                   DICT_KEY_PARTY_T_RIGHT,
                                                                   DICT_KEY_PLOT_T_AREA_F)
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

    def get_plots_related_to_parcels_supplies(self, db, t_ids, field_name, gc_plot_layer=None):
        """
        :param db: DB Connector object
        :param t_ids: list of parcel t_ids in supplies model
        :param field_name: The field name to get from DB for the matching features, use None for the QGIS internal ID
        :param gc_plot_layer: Plot QGIS layer, in case it exists already in the caller
        :return: list of plot ids related to the parcel from supplies model
        """
        if not t_ids:
            return []

        layers = {
            db.names.GC_PLOT_T: {'name': db.names.GC_PLOT_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None}
        }

        if gc_plot_layer is not None:
            del layers[db.names.GC_PLOT_T]

        if layers:
            self.qgis_utils.get_layers(db, layers, load=True)
            if not layers:
                return None

            if db.names.GC_PLOT_T in layers:
                gc_plot_layer = layers[db.names.GC_PLOT_T][LAYER]

        expression = QgsExpression("{} IN ('{}') ".format(db.names.GC_PLOT_T_GC_PARCEL_F, "','".join([str(t_id) for t_id in t_ids])))
        features = self.get_features_by_expression(gc_plot_layer, db.names.T_ID_F, expression, with_attributes=True)

        plot_ids = list()
        for feature in features:
            if field_name is None:  # We are only interested in the QGIS internal id, no need to get other fields
                plot_ids.append(feature.id())
            else:
                field_found = gc_plot_layer.fields().indexOf(field_name) != -1
                if field_found:
                    plot_ids.append(feature[field_name])

        return plot_ids

    def get_parcels_related_to_plots_supplies(self, db, t_ids, field_name, gc_parcel_table=None):
        """
        :param db: DB Connector object
        :param t_ids: list of plot t_ids
        :param field_name: The field name to get from DB for the matching features, use None for the QGIS internal ID
        :param gc_parcel_table: Parcel QGIS layer, in case it exists already in the caller
        :return: list of parcel ids related to the plot
        """

        if not t_ids:
            return []

        layers = {
            db.names.GC_PARCEL_T: {'name': db.names.GC_PARCEL_T, 'geometry': None, LAYER: None},
            db.names.GC_PLOT_T: {'name': db.names.GC_PLOT_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None}
        }

        if gc_parcel_table is not None:
            del layers[db.names.GC_PARCEL_T]

        if layers:
            self.qgis_utils.get_layers(db, layers, load=True)
            if not layers:
                return None

            if db.names.GC_PARCEL_T in layers:
                gc_parcel_table = layers[db.names.GC_PARCEL_T][LAYER]

            if db.names.GC_PLOT_T in layers:
                gc_plot_layer = layers[db.names.GC_PLOT_T][LAYER]

        expression = QgsExpression("{} IN ({})".format(db.names.T_ID_F,
                                                       ",".join([str(t_id) for t_id in t_ids])))
        features = self.get_features_by_expression(gc_plot_layer, db.names.T_ID_F, expression, with_attributes=True)

        parcel_t_ids = list()
        for feature in features:
            parcel_t_ids.append(feature[db.names.GC_PLOT_T_GC_PARCEL_F])

        if field_name == db.names.T_ID_F:
            return parcel_t_ids

        parcel_ids = list()
        expression = QgsExpression("{} IN ({})".format(db.names.T_ID_F,
                                                          ",".join([str(id) for id in parcel_t_ids])))

        if field_name is None:
            features = self.get_features_by_expression(gc_parcel_table, db.names.T_ID_F, expression)
        else:
            features = self.get_features_by_expression(gc_parcel_table, db.names.T_ID_F, expression, with_attributes=True)

        for feature in features:
            if field_name is None: # We are only interested in the QGIS internal id, no need to get other fields
                parcel_ids.append(feature.id())
            else:
                field_found = gc_parcel_table.fields().indexOf(field_name) != -1
                if field_found:
                    parcel_ids.append(feature[field_name])

        return parcel_ids

    def get_parcel_data_to_compare_changes_supplies(self, db, search_criterion=None, layer_modifiers=dict()):
        """
        :param db: DB Connector object
        :param search_criterion: FieldName-Value pair to search in parcel layer (None for getting all parcels)
        :return: dict with parcel info for comparisons
        """

        mapping_parcels_field = self.mapping_parcel_fields_for_supplies(db.names)
        mapping_party_field = self.mapping_party_fields_for_supplies(db.names)
        mapping_plot_field = self.mapping_plot_fields_for_supplies(db.names)

        layers = {
            db.names.GC_PARCEL_T: {'name': db.names.GC_PARCEL_T, 'geometry': None, LAYER: None},
            db.names.GC_PLOT_T: {'name': db.names.GC_PLOT_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            db.names.GC_OWNER_T: {'name': db.names.GC_OWNER_T, 'geometry': None, LAYER: None}
        }

        self.qgis_utils.get_layers(db, layers, load=True, layer_modifiers=layer_modifiers)
        if not layers:
            return None

        # ===================== Start adding parcel info ==================================================
        parcel_fields = [f.name() for f in layers[db.names.GC_PARCEL_T][LAYER].fields()]
        parcel_features = self.get_features_by_search_criterion(layers[db.names.GC_PARCEL_T][LAYER], db.names.T_ID_F, search_criterion=search_criterion, with_attributes=True)

        dict_features = dict()
        for feature in parcel_features:
            dict_attrs = dict()

            for parcel_field, common_key_value_parcel in mapping_parcels_field.items():  # parcel fields to compare
                if parcel_field in parcel_fields:
                    if parcel_field == db.names.GC_PARCEL_T_CONDITION_F:
                        # Go for domain value, instead of t_id
                        value = self.get_domain_value_from_code(db, db.names.GC_PARCEL_TYPE_D, feature.attribute(parcel_field))
                    else:
                        value = feature.attribute(parcel_field)
                elif parcel_field == DICT_KEY_PARCEL_T_DEPARTMENT_F:
                    value = feature.attribute(db.names.GC_PARCEL_T_PARCEL_NUMBER_F)[:2]
                elif parcel_field == DICT_KEY_PARCEL_T_NAME_F:
                    value = NULL
                dict_attrs[common_key_value_parcel] = value
            dict_attrs[db.names.T_ID_F] = feature[db.names.T_ID_F]

            # Group dictionary by parcel number common key
            if dict_attrs[DICT_KEY_PARCEL_T_PARCEL_NUMBER_F] in dict_features:
                dict_features[dict_attrs[DICT_KEY_PARCEL_T_PARCEL_NUMBER_F]].append(dict_attrs)
            else:
                dict_features[dict_attrs[DICT_KEY_PARCEL_T_PARCEL_NUMBER_F]] = [dict_attrs]

        # =====================  Start adding plot info ==================================================
        plot_fields = [f.name() for f in layers[db.names.GC_PLOT_T][LAYER].fields()]
        parcel_t_ids = [parcel_feature[db.names.T_ID_F] for parcel_feature in parcel_features]

        expression_plot_features = QgsExpression("{} IN ('{}')".format(db.names.GC_PLOT_T_GC_PARCEL_F, "','".join([str(parcel_t_id) for parcel_t_id in parcel_t_ids])))
        plot_features = self.get_features_by_expression(layers[db.names.GC_PLOT_T][LAYER], db.names.T_ID_F, expression_plot_features, with_attributes=True, with_geometry=True)
        dict_parcel_plot = {plot_feature[db.names.GC_PLOT_T_GC_PARCEL_F]: plot_feature[db.names.T_ID_F] for plot_feature in plot_features}
        dict_plot_features = {plot_feature[db.names.T_ID_F]: plot_feature for plot_feature in plot_features}

        for feature in dict_features:
            for item in dict_features[feature]:
                if item[db.names.T_ID_F] in dict_parcel_plot:
                    if dict_parcel_plot[item[db.names.T_ID_F]] in dict_plot_features:
                        plot_feature = dict_plot_features[dict_parcel_plot[item[db.names.T_ID_F]]]
                        for plot_field, common_key_value_plot in mapping_plot_field.items():  # plot fields to compare
                            if plot_field in plot_fields:
                                if plot_feature[plot_field] != NULL:
                                    item[common_key_value_plot] = plot_feature[plot_field]
                                else:
                                    item[common_key_value_plot] = NULL

                        item[PLOT_GEOMETRY_KEY] = plot_feature.geometry()
                else:
                    item[PLOT_GEOMETRY_KEY] = None  # No associated plot

        # ===================== Start adding party info ==================================================
        party_fields = [f.name() for f in layers[db.names.GC_OWNER_T][LAYER].fields()]
        expression_parties_features = QgsExpression("{} IN ({})".format(db.names.GC_OWNER_T_PARCEL_ID_F, ",".join([str(id) for id in parcel_t_ids])))
        party_features = self.get_features_by_expression(layers[db.names.GC_OWNER_T][LAYER], db.names.T_ID_F, expression_parties_features, with_attributes=True)

        dict_parcel_parties = dict()
        for party_feature in party_features:
            if party_feature[db.names.GC_OWNER_T_PARCEL_ID_F] in dict_parcel_parties:
                dict_parcel_parties[party_feature[db.names.GC_OWNER_T_PARCEL_ID_F]].append(party_feature[db.names.T_ID_F])
            else:
                dict_parcel_parties[party_feature[db.names.GC_OWNER_T_PARCEL_ID_F]] = [party_feature[db.names.T_ID_F]]

        dict_parties = dict()
        for party_feature in party_features:
            dict_party = dict()
            for party_field, common_key_value_party in mapping_party_field.items():  # Party fields to compare
                if party_field in party_fields:
                    dict_party[common_key_value_party] = party_feature[party_field]
                elif party_field == DICT_KEY_PARTY_T_NAME_F:
                    dict_party[common_key_value_party] = "{} {} {} {}".format(party_feature[db.names.GC_OWNER_T_FIRST_NAME_1_F],
                                                                              party_feature[db.names.GC_OWNER_T_FIRST_NAME_2_F],
                                                                              party_feature[db.names.GC_OWNER_T_SURNAME_1_F],
                                                                              party_feature[db.names.GC_OWNER_T_SURNAME_2_F])
                elif party_field == DICT_KEY_PARTY_T_RIGHT:
                    dict_party[common_key_value_party] = NULL
            dict_parties[party_feature[db.names.T_ID_F]] = dict_party

        for id_parcel in dict_parcel_parties:
            party_info = list()
            for id_party in dict_parcel_parties[id_parcel]:
                if id_party in dict_parties:
                    party_info.append(dict_parties[id_party])

            dict_parcel_parties[id_parcel] = party_info

        # Append party info
        for feature in dict_features:
            for item in dict_features[feature]:
                if item[db.names.T_ID_F] in dict_parcel_parties:
                    # Make join
                    if DICT_KEY_PARTIES in item:
                        item[DICT_KEY_PARTIES].append(dict_parcel_parties[item[db.names.T_ID_F]])
                    else:
                        item[DICT_KEY_PARTIES] = dict_parcel_parties[item[db.names.T_ID_F]]
                else:
                    item[DICT_KEY_PARTIES] = NULL

        return dict_features

    def get_plots_related_to_parcels(self, db, t_ids, field_name, plot_layer=None, uebaunit_table=None):
        """
        :param db: DB Connector object
        :param t_ids: list of parcel t_ids
        :param field_name: The field name to get from DB for the matching features, use None for the QGIS internal ID
        :param plot_layer: Plot QGIS layer, in case it exists already in the caller
        :param uebaunit_table: UEBaunit QGIS table, in case it exists already in the caller
        :return: list of plot ids related to the parcel
        """

        if not t_ids:
            return []

        layers = {
            db.names.OP_PLOT_T: {'name': db.names.OP_PLOT_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            db.names.COL_UE_BAUNIT_T: {'name': db.names.COL_UE_BAUNIT_T, 'geometry': None, LAYER: None}
        }

        if plot_layer is not None:
            del layers[db.names.OP_PLOT_T]
        if uebaunit_table is not None:
            del layers[db.names.COL_UE_BAUNIT_T]

        if layers:
            self.qgis_utils.get_layers(db, layers, load=True)
            if not layers:
                return None

            if db.names.OP_PLOT_T in layers:
                plot_layer = layers[db.names.OP_PLOT_T][LAYER]

            if db.names.COL_UE_BAUNIT_T in layers:
                uebaunit_table = layers[db.names.COL_UE_BAUNIT_T][LAYER]

        expression = QgsExpression("{} IN ('{}') AND {} IS NOT NULL".format(
                                                    db.names.COL_UE_BAUNIT_T_PARCEL_F,
                                                    "','".join([str(t_id) for t_id in t_ids]),
                                                    db.names.COL_UE_BAUNIT_T_OP_PLOT_F))
        features = self.get_features_by_expression(uebaunit_table, db.names.T_ID_F, expression, with_attributes=True)

        plot_t_ids = list()
        for feature in features:
            plot_t_ids.append(feature[db.names.COL_UE_BAUNIT_T_OP_PLOT_F])

        if field_name == db.names.T_ID_F:
            return plot_t_ids

        plot_ids = list()
        expression = QgsExpression("{} IN ('{}')".format(db.names.T_ID_F, "','".join([str(id) for id in plot_t_ids])))

        if field_name is None:
            features = self.get_features_by_expression(plot_layer, db.names.T_ID_F, expression)
        else:
            features = self.get_features_by_expression(plot_layer, db.names.T_ID_F, expression, with_attributes=True)

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

        if not t_ids:
            return []

        layers = {
            db.names.OP_PARCEL_T: {'name': db.names.OP_PARCEL_T, 'geometry': None, LAYER: None},
            db.names.COL_UE_BAUNIT_T: {'name': db.names.COL_UE_BAUNIT_T, 'geometry': None, LAYER: None}
        }

        if parcel_table is not None:
            del layers[db.names.OP_PARCEL_T]
        if uebaunit_table is not None:
            del layers[db.names.COL_UE_BAUNIT_T]

        if layers:
            self.qgis_utils.get_layers(db, layers, load=True)
            if not layers:
                return None

            if db.names.OP_PARCEL_T in layers:
                parcel_table = layers[db.names.OP_PARCEL_T][LAYER]

            if db.names.COL_UE_BAUNIT_T in layers:
                uebaunit_table = layers[db.names.COL_UE_BAUNIT_T][LAYER]


        expression = QgsExpression("{} IN ({}) AND {} IS NOT NULL".format(
                                                    db.names.COL_UE_BAUNIT_T_OP_PLOT_F,
                                                    ",".join([str(t_id) for t_id in t_ids]),
                                                    db.names.COL_UE_BAUNIT_T_PARCEL_F))
        features = self.get_features_by_expression(uebaunit_table, db.names.T_ID_F, expression, with_attributes=True)

        parcel_t_ids = list()
        for feature in features:
            parcel_t_ids.append(feature[db.names.COL_UE_BAUNIT_T_PARCEL_F])

        if field_name == db.names.T_ID_F:
            return parcel_t_ids

        parcel_ids = list()
        expression = QgsExpression("{} IN ({})".format(db.names.T_ID_F,
                                                          ",".join([str(id) for id in parcel_t_ids])))

        if field_name is None:
            features = self.get_features_by_expression(parcel_table, db.names.T_ID_F, expression)
        else:
            features = self.get_features_by_expression(parcel_table, db.names.T_ID_F, expression, with_attributes=True)

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

        mapping_parcels_field = self.mapping_parcel_fields(db.names)
        mapping_party_field = self.mapping_party_fields(db.names)
        mapping_plot_field = self.mapping_plot_fields(db.names)

        layers = {
            db.names.OP_PARCEL_T: {'name': db.names.OP_PARCEL_T, 'geometry': None, LAYER: None},
            db.names.OP_PLOT_T: {'name': db.names.OP_PLOT_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            db.names.OP_RIGHT_T: {'name': db.names.OP_RIGHT_T, 'geometry': None, LAYER: None},
            db.names.OP_PARTY_T: {'name': db.names.OP_PARTY_T, 'geometry': None, LAYER: None},
            db.names.OP_GROUP_PARTY_T: {'name': db.names.OP_GROUP_PARTY_T, 'geometry': None, LAYER: None},
            db.names.COL_UE_BAUNIT_T: {'name': db.names.COL_UE_BAUNIT_T, 'geometry': None, LAYER: None},
            db.names.MEMBERS_T: {'name': db.names.MEMBERS_T, 'geometry': None, LAYER: None},
        }

        if db.cadastral_form_model_exists():
            # TODO: Replace property record card for correct table model
            # layers[PROPERTY_RECORD_CARD_TABLE] = {'name': PROPERTY_RECORD_CARD_TABLE, 'geometry': None, LAYER: None}
            pass

        self.qgis_utils.get_layers(db, layers, load=True, layer_modifiers=layer_modifiers)
        if not layers:
            return None

        parcel_features = self.get_features_by_search_criterion(layers[db.names.OP_PARCEL_T][LAYER], db.names.T_ID_F, search_criterion=search_criterion, with_attributes=True)

        # ===================== Start adding parcel info ==================================================
        dict_features = dict()
        for feature in parcel_features:
            dict_attrs = dict()
            for field in layers[db.names.OP_PARCEL_T][LAYER].fields():
                if field.name() in mapping_parcels_field.keys():  # parcel fields to compare
                    if field.name() == db.names.OP_PARCEL_T_PARCEL_TYPE_F:
                        # Go for domain value, instead of t_id
                        value = self.get_domain_value_from_code(db, db.names.OP_CONDITION_PARCEL_TYPE_D, feature.attribute(field.name()))
                    else:
                        value = feature.attribute(field.name())

                    key_value_parcel = mapping_parcels_field[field.name()]
                    dict_attrs[key_value_parcel] = value
            dict_attrs[db.names.T_ID_F] = feature[db.names.T_ID_F]

            # Group dictionary by parcel number common key
            if dict_attrs[DICT_KEY_PARCEL_T_PARCEL_NUMBER_F] in dict_features:
                dict_features[dict_attrs[DICT_KEY_PARCEL_T_PARCEL_NUMBER_F]].append(dict_attrs)
            else:
                dict_features[dict_attrs[DICT_KEY_PARCEL_T_PARCEL_NUMBER_F]] = [dict_attrs]

        # =====================  Start adding plot info ==================================================
        parcel_t_ids = [parcel_feature[db.names.T_ID_F] for parcel_feature in parcel_features]
        expression_uebaunit_features = QgsExpression("{} IN ({}) AND {} IS NOT NULL".format(db.names.COL_UE_BAUNIT_T_PARCEL_F, ",".join([str(id) for id in parcel_t_ids]), db.names.COL_UE_BAUNIT_T_OP_PLOT_F))
        uebaunit_features = self.get_features_by_expression(layers[db.names.COL_UE_BAUNIT_T][LAYER], db.names.T_ID_F, expression_uebaunit_features, with_attributes=True)

        plot_t_ids = [feature[db.names.COL_UE_BAUNIT_T_OP_PLOT_F] for feature in uebaunit_features]
        expression_plot_features = QgsExpression("{} IN ('{}')".format(db.names.T_ID_F, "','".join([str(id) for id in plot_t_ids])))
        plot_features = self.get_features_by_expression(layers[db.names.OP_PLOT_T][LAYER], db.names.T_ID_F, expression_plot_features, with_attributes=True, with_geometry=True)

        dict_parcel_plot = {uebaunit_feature[db.names.COL_UE_BAUNIT_T_PARCEL_F]: uebaunit_feature[db.names.COL_UE_BAUNIT_T_OP_PLOT_F] for uebaunit_feature in uebaunit_features}
        dict_plot_features = {plot_feature[db.names.T_ID_F]: plot_feature for plot_feature in plot_features}

        for feature in dict_features:
            for item in dict_features[feature]:
                if item[db.names.T_ID_F] in dict_parcel_plot:
                    if dict_parcel_plot[item[db.names.T_ID_F]] in dict_plot_features:
                        plot_feature = dict_plot_features[dict_parcel_plot[item[db.names.T_ID_F]]]
                        for plot_field, common_key_value_plot in mapping_plot_field.items():  # plot fields to compare
                            if plot_feature[plot_field] != NULL:
                                item[common_key_value_plot] = plot_feature[plot_field]
                            else:
                                item[common_key_value_plot] = NULL

                            item[PLOT_GEOMETRY_KEY] = plot_feature.geometry()
                else:
                    item[PLOT_GEOMETRY_KEY] = None  # No associated plot

        # ===================== Start adding party info ==================================================
        expression_right_features = QgsExpression("{} IN ({})".format(db.names.COL_BAUNIT_RRR_T_UNIT_F, ",".join([str(id) for id in parcel_t_ids])))
        right_features = self.get_features_by_expression(layers[db.names.OP_RIGHT_T][LAYER], db.names.T_ID_F, expression_right_features, with_attributes=True)

        dict_party_right = {right_feature[db.names.COL_RRR_PARTY_T_OP_PARTY_F]: right_feature for right_feature in right_features if right_feature[db.names.COL_RRR_PARTY_T_OP_PARTY_F] != NULL}
        party_t_ids = [right_feature[db.names.COL_RRR_PARTY_T_OP_PARTY_F] for right_feature in right_features if right_feature[db.names.COL_RRR_PARTY_T_OP_PARTY_F] != NULL]
        expression_party_features = QgsExpression("{} IN ({})".format(db.names.T_ID_F, ",".join([str(id) for id in party_t_ids])))
        party_features = self.get_features_by_expression(layers[db.names.OP_PARTY_T][LAYER], db.names.T_ID_F, expression_party_features, with_attributes=True)

        dict_parcel_parties = dict()
        for right_feature in right_features:
            if right_feature[db.names.COL_BAUNIT_RRR_T_UNIT_F] != NULL and right_feature[db.names.COL_RRR_PARTY_T_OP_PARTY_F] != NULL:
                if right_feature[db.names.COL_BAUNIT_RRR_T_UNIT_F] in dict_parcel_parties:
                    if right_feature[db.names.COL_RRR_PARTY_T_OP_PARTY_F] not in dict_parcel_parties[right_feature[db.names.COL_BAUNIT_RRR_T_UNIT_F]]:
                        dict_parcel_parties[right_feature[db.names.COL_BAUNIT_RRR_T_UNIT_F]].append(right_feature[db.names.COL_RRR_PARTY_T_OP_PARTY_F])
                else:
                    dict_parcel_parties[right_feature[db.names.COL_BAUNIT_RRR_T_UNIT_F]] = [right_feature[db.names.COL_RRR_PARTY_T_OP_PARTY_F]]

        dict_parties = dict()
        for party_feature in party_features:
            dict_party = dict()
            for party_field, common_key_value_party in mapping_party_field.items():  # party fields to compare
                if party_field == db.names.OP_PARTY_T_DOCUMENT_TYPE_F:
                    dict_party[common_key_value_party] = self.get_domain_value_from_code(db, db.names.OP_PARTY_DOCUMENT_TYPE_D, party_feature[party_field])
                else:
                    dict_party[common_key_value_party] = party_feature[party_field]
            # Add extra attribute from right table
            right_type_id = dict_party_right[party_feature[db.names.T_ID_F]][db.names.OP_RIGHT_T_TYPE_F]
            dict_party[DICT_KEY_PARTY_T_RIGHT] = self.get_domain_value_from_code(db, db.names.OP_RIGHT_TYPE_D, right_type_id)
            dict_parties[party_feature[db.names.T_ID_F]] = dict_party

        for id_parcel in dict_parcel_parties:
            party_info = list()
            for id_party in dict_parcel_parties[id_parcel]:
                if id_party in dict_parties:
                    party_info.append(dict_parties[id_party])

            dict_parcel_parties[id_parcel] = party_info

        # Append party info
        for feature in dict_features:
            for item in dict_features[feature]:
                if item[db.names.T_ID_F] in dict_parcel_parties:
                    # Make join
                    if DICT_KEY_PARTIES in item:
                        item[DICT_KEY_PARTIES].append(dict_parcel_parties[item[db.names.T_ID_F]])
                    else:
                        item[DICT_KEY_PARTIES] = dict_parcel_parties[item[db.names.T_ID_F]]
                else:
                    item[DICT_KEY_PARTIES] = NULL

        # =====================  Start add group party info ==================================================
        dict_parcel_group_parties = dict()  # {id_parcel: [id_group_party1, id_group_party2]}
        for right_feature in right_features:
            if right_feature[db.names.COL_BAUNIT_RRR_T_UNIT_F] != NULL and right_feature[db.names.COL_RRR_PARTY_T_OP_GROUP_PARTY_F] != NULL:
                if right_feature[db.names.COL_BAUNIT_RRR_T_UNIT_F] in dict_parcel_group_parties:
                    if right_feature[db.names.COL_RRR_PARTY_T_OP_GROUP_PARTY_F] not in dict_parcel_group_parties[right_feature[db.names.COL_BAUNIT_RRR_T_UNIT_F]]:
                        dict_parcel_group_parties[right_feature[db.names.COL_BAUNIT_RRR_T_UNIT_F]].append(right_feature[db.names.COL_RRR_PARTY_T_OP_GROUP_PARTY_F])
                else:
                    dict_parcel_group_parties[right_feature[db.names.COL_BAUNIT_RRR_T_UNIT_F]] = [right_feature[db.names.COL_RRR_PARTY_T_OP_GROUP_PARTY_F]]

        dict_group_party_right = {right_feature[db.names.COL_RRR_PARTY_T_OP_GROUP_PARTY_F]: right_feature for right_feature in right_features if right_feature[db.names.COL_RRR_PARTY_T_OP_GROUP_PARTY_F] != NULL}
        group_party_t_ids = [right_feature[db.names.COL_RRR_PARTY_T_OP_GROUP_PARTY_F] for right_feature in right_features if right_feature[db.names.COL_RRR_PARTY_T_OP_GROUP_PARTY_F] != NULL]
        expression_members_features = QgsExpression("{} IN ({})".format(db.names.MEMBERS_T_GROUP_PARTY_F, ",".join([str(id) for id in group_party_t_ids])))
        members_features = self.get_features_by_expression(layers[db.names.MEMBERS_T][LAYER], db.names.T_ID_F, expression_members_features, with_attributes=True)

        dict_group_party_parties = dict()  # {id_group_party: [id_party1, id_party2]}
        for members_feature in members_features:
            if members_feature[db.names.MEMBERS_T_GROUP_PARTY_F] != NULL and members_feature[db.names.MEMBERS_T_PARTY_F] != NULL:
                if members_feature[db.names.MEMBERS_T_GROUP_PARTY_F] in dict_group_party_parties:
                    if members_feature[db.names.MEMBERS_T_PARTY_F] not in dict_group_party_parties[members_feature[db.names.MEMBERS_T_GROUP_PARTY_F]]:
                        dict_group_party_parties[members_feature[db.names.MEMBERS_T_GROUP_PARTY_F]].append(members_feature[db.names.MEMBERS_T_PARTY_F])
                else:
                    dict_group_party_parties[members_feature[db.names.MEMBERS_T_GROUP_PARTY_F]] = [members_feature[db.names.MEMBERS_T_PARTY_F]]

        party_t_ids = [members_feature[db.names.MEMBERS_T_PARTY_F] for members_feature in members_features if members_feature[db.names.MEMBERS_T_PARTY_F] != NULL]
        party_t_ids = list(set(party_t_ids))

        expression_party_features = QgsExpression("{} IN ({})".format(db.names.T_ID_F, ",".join([str(id) for id in party_t_ids])))
        party_features = self.get_features_by_expression(layers[db.names.OP_PARTY_T][LAYER], db.names.T_ID_F, expression_party_features, with_attributes=True)

        dict_parties = dict()  # {id_party: {tipo_documento: CC, documento_identidad: 123456, nombre: Pepito}}
        for party_feature in party_features:
            dict_party = dict()
            for party_field, common_key_value_party in mapping_party_field.items():  # party fields to compare
                if party_field == db.names.OP_PARTY_T_DOCUMENT_TYPE_F:
                    dict_party[common_key_value_party] = self.get_domain_value_from_code(db, db.names.OP_PARTY_DOCUMENT_TYPE_D, party_feature[party_field])
                else:
                    dict_party[common_key_value_party] = party_feature[party_field]
            dict_parties[party_feature[db.names.T_ID_F]] = dict_party

        # Reuse the dict to replace id_group_party for party info:
        #   {id_group_party: [{tipo_documento: CC, documento_identidad: 123456, nombre: Pepito, 'derecho': Dominio}, ..., {}] }
        for id_group_party in dict_group_party_parties:
            party_info = list()
            for id_party in dict_group_party_parties[id_group_party]:
                if id_party in dict_parties:
                    # Add extra attribute from right table
                    right_type_id = dict_group_party_right[id_group_party][db.names.OP_RIGHT_T_TYPE_F]
                    dict_parties[id_party][DICT_KEY_PARTY_T_RIGHT] = self.get_domain_value_from_code(db, db.names.OP_RIGHT_TYPE_D, right_type_id)
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
        for feature in dict_features:
            for item in dict_features[feature]:
                if item[db.names.T_ID_F] in dict_parcel_group_parties:
                    # Make join
                    if DICT_KEY_PARTIES in item:
                        if item[DICT_KEY_PARTIES]:
                            for info in dict_parcel_group_parties[item[db.names.T_ID_F]]:
                                item[DICT_KEY_PARTIES].append(info)
                        else:
                            item[DICT_KEY_PARTIES] = dict_parcel_group_parties[item[db.names.T_ID_F]]
                    else:
                        item[DICT_KEY_PARTIES] = dict_parcel_group_parties[item[db.names.T_ID_F]]

        # =====================  Start add record card info ==================================================
        # TODO: Replace property record card for correct table model
        # if db.cadastral_form_model_exists():
        #     expr_property_record_card_features = QgsExpression("{} IN ({})".format(PROPERTY_RECORD_CARD_PARCEL_ID_FIELD, ",".join([str(id) for id in parcel_t_ids])))
        #     property_record_card_features = self.get_features_by_expression(layers[PROPERTY_RECORD_CARD_TABLE][LAYER], db.names.T_ID_F, expr_property_record_card_features, with_attributes=True)
        #
        #     dict_property_record_card_features = {property_record_card_feature[PROPERTY_RECORD_CARD_PARCEL_ID_FIELD]: property_record_card_feature for property_record_card_feature in property_record_card_features}
        #
        #     for feature in dict_features:
        #         for item in dict_features[feature]:
        #             if item[db.names.T_ID_F] in dict_property_record_card_features:
        #                 property_record_card_feature = dict_property_record_card_features[item[db.names.T_ID_F]]
        #                 for PROPERTY_RECORD_CARD_FIELD in PROPERTY_RECORD_CARD_FIELDS_TO_COMPARE:
        #                     if property_record_card_feature[PROPERTY_RECORD_CARD_FIELD] != NULL:
        #                         item[PROPERTY_RECORD_CARD_FIELD] = property_record_card_feature[PROPERTY_RECORD_CARD_FIELD]
        #                     else:
        #                         item[PROPERTY_RECORD_CARD_FIELD] = NULL

        return dict_features

    def get_features_by_search_criterion(self, layer, t_id_name, search_criterion=None, with_attributes=False, with_geometry=False):
        if search_criterion is not None:
            field_name = list(search_criterion.keys())[0]
            field_value = list(search_criterion.values())[0]
            expression = QgsExpression("{}='{}'".format(field_name, field_value))
            features = self.get_features_by_expression(layer, t_id_name, expression=expression, with_attributes=with_attributes, with_geometry=with_geometry)
        else:
            features = self.get_features_by_expression(layer, t_id_name, with_attributes=with_attributes, with_geometry=with_geometry)

        return features

    def get_features_by_expression(self, layer, t_id_name, expression=None, with_attributes=False, with_geometry=False):
        # TODO: It should be possible to pass a list of attributes to retrieve

        if expression is None:
            request = QgsFeatureRequest()
        else:
            request = QgsFeatureRequest(expression)

        if not with_geometry:
            request.setFlags(QgsFeatureRequest.NoGeometry)
        if not with_attributes:
            field_idx = layer.fields().indexFromName(t_id_name)
            request.setSubsetOfAttributes([field_idx])  # Note: this adds a new flag

        return [feature for feature in layer.getFeatures(request)]

    @staticmethod
    def get_features_from_t_ids(layer, t_id_name, t_ids, no_attributes=False, no_geometry=False):
        request = QgsFeatureRequest(QgsExpression("{} IN ('{}')".format(t_id_name, "','".join([str(t_id) for t_id in t_ids]))))

        if no_geometry:
            request.setFlags(QgsFeatureRequest.NoGeometry)
        if no_attributes:
            field_idx = layer.fields().indexFromName(t_id_name)
            request.setSubsetOfAttributes([field_idx])  # Note: this adds a new flag

        return [feature for feature in layer.getFeatures(request)]

    @staticmethod
    def mapping_parcel_fields_for_supplies(names):
        return {
            DICT_KEY_PARCEL_T_DEPARTMENT_F: DICT_KEY_PARCEL_T_DEPARTMENT_F,
            names.GC_PARCEL_T_FMI_F: DICT_KEY_PARCEL_T_FMI_F,
            names.GC_PARCEL_T_PARCEL_NUMBER_F: DICT_KEY_PARCEL_T_PARCEL_NUMBER_F,
            names.GC_PARCEL_T_CONDITION_F: DICT_KEY_PARCEL_T_CONDITION_F,
            DICT_KEY_PARCEL_T_NAME_F: DICT_KEY_PARCEL_T_NAME_F
        }

    @staticmethod
    def mapping_party_fields_for_supplies(names):
        return {
            names.GC_OWNER_T_DOCUMENT_TYPE_F: DICT_KEY_PARTY_T_DOCUMENT_TYPE_F,
            names.GC_OWNER_T_DOCUMENT_ID_F: DICT_KEY_PARTY_T_DOCUMENT_ID_F,
            DICT_KEY_PARTY_T_NAME_F: DICT_KEY_PARTY_T_NAME_F,
            DICT_KEY_PARTY_T_RIGHT: DICT_KEY_PARTY_T_RIGHT
        }

    @staticmethod
    def mapping_plot_fields_for_supplies(names):
        return {
            names.GC_PLOT_T_ALPHANUMERIC_AREA: DICT_KEY_PLOT_T_AREA_F
        }

    @staticmethod
    def mapping_parcel_fields(names):
        return {
            names.OP_PARCEL_T_DEPARTMENT_F: DICT_KEY_PARCEL_T_DEPARTMENT_F,
            names.OP_PARCEL_T_FMI_F: DICT_KEY_PARCEL_T_FMI_F,
            names.OP_PARCEL_T_PARCEL_NUMBER_F: DICT_KEY_PARCEL_T_PARCEL_NUMBER_F,
            names.OP_PARCEL_T_PARCEL_TYPE_F: DICT_KEY_PARCEL_T_CONDITION_F,
            names.COL_BAUNIT_T_NAME_F: DICT_KEY_PARCEL_T_NAME_F
        }

    @staticmethod
    def mapping_party_fields(names):
        return {
            names.OP_PARTY_T_DOCUMENT_TYPE_F: DICT_KEY_PARTY_T_DOCUMENT_TYPE_F,
            names.OP_PARTY_T_DOCUMENT_ID_F: DICT_KEY_PARTY_T_DOCUMENT_ID_F,
            names.COL_PARTY_T_NAME_F: DICT_KEY_PARTY_T_NAME_F
        }

    @staticmethod
    def mapping_plot_fields(names):
        return {
            names.OP_PLOT_T_PLOT_AREA_F: DICT_KEY_PLOT_T_AREA_F
        }

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
        cached_res = db.names.get_domain_code(domain_table_name, value)
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
                    db.names.cache_domain_value(domain_table_name, res, value)

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
        cached_res = db.names.get_domain_value(domain_table_name, code)
        if cached_res is not None:
            self.logger.debug(__name__, "(From cache!) Get domain ({}) {} from code ({}): {}".format(
                domain_table_name, db.names.ILICODE_F if value_is_ilicode else db.names.DISPLAY_NAME_F, code, cached_res))
            return cached_res

        if type(domain_table) is str:
            domain_table = self.qgis_utils.get_layer(db, domain_table, None, True, emit_map_freeze=False)

        if domain_table is not None:
            features = self.get_features_from_t_ids(domain_table, db.names.T_ID_F, [code], no_attributes=False, no_geometry=True)
            if features:
                res = features[0][db.names.ILICODE_F if value_is_ilicode else db.names.DISPLAY_NAME_F]
                if res is not None:
                    db.names.cache_domain_value(domain_table_name, code, res)

        self.logger.debug(__name__, "Get domain ({}) {} from code ({}): {}".format(
            domain_table_name, db.names.ILICODE_F if value_is_ilicode else db.names.DISPLAY_NAME_F, code, res))

        return res
