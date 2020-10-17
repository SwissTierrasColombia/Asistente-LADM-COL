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
import locale
import uuid

from qgis.PyQt.QtCore import (QObject,
                              QCoreApplication)
from qgis.core import (NULL,
                       QgsFeatureRequest,
                       QgsExpression,
                       QgsFeature,
                       QgsVectorLayer,
                       QgsVectorLayerUtils,
                       QgsAggregateCalculator)
from asistente_ladm_col.config.enums import EnumLogMode
from asistente_ladm_col.config.general_config import (DEFAULT_LOG_MODE,
                                                      DEFAULT_DATASET_NAME)
from asistente_ladm_col.config.change_detection_config import (PLOT_GEOMETRY_KEY,
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
from asistente_ladm_col.config.ladm_names import LADMNames
from asistente_ladm_col.config.query_names import QueryNames
from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.lib.db.db_connector import DBConnector
from asistente_ladm_col.lib.ladm_col_models import LADMColModelRegistry
from asistente_ladm_col.lib.logger import Logger


class LADMData(QObject):
    """
    High-level class to get related information from the LADM-COL database.
    """
    def __init__(self):
        QObject.__init__(self)
        self.logger = Logger()
        self.app = AppInterface()

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

        layers = {db.names.GC_PLOT_T: None}

        if gc_plot_layer is not None:
            del layers[db.names.GC_PLOT_T]

        if layers:
            self.app.core.get_layers(db, layers, load=True)
            if not layers:
                return None

            if db.names.GC_PLOT_T in layers:
                gc_plot_layer = layers[db.names.GC_PLOT_T]

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
            db.names.GC_PARCEL_T: None,
            db.names.GC_PLOT_T: None
        }

        if gc_parcel_table is not None:
            del layers[db.names.GC_PARCEL_T]

        if layers:
            self.app.core.get_layers(db, layers, load=True)
            if not layers:
                return None

            if db.names.GC_PARCEL_T in layers:
                gc_parcel_table = layers[db.names.GC_PARCEL_T]

            if db.names.GC_PLOT_T in layers:
                gc_plot_layer = layers[db.names.GC_PLOT_T]

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
            db.names.GC_PARCEL_T: None,
            db.names.GC_PLOT_T: None,
            db.names.GC_OWNER_T: None,
            db.names.GC_PARCEL_TYPE_D: None
        }

        self.app.core.get_layers(db, layers, load=True, layer_modifiers=layer_modifiers)
        if not layers:
            return None

        # ===================== Start adding parcel info ==================================================
        parcel_fields = [f.name() for f in layers[db.names.GC_PARCEL_T].fields()]
        parcel_features = self.get_features_by_search_criterion(layers[db.names.GC_PARCEL_T], db.names.T_ID_F, search_criterion=search_criterion, with_attributes=True)

        dict_features = dict()
        for feature in parcel_features:
            dict_attrs = dict()

            for parcel_field, common_key_value_parcel in mapping_parcels_field.items():  # parcel fields to compare
                if parcel_field in parcel_fields:
                    if parcel_field == db.names.GC_PARCEL_T_CONDITION_F:
                        # Go for domain value, instead of t_id
                        value = self.get_domain_value_from_code(db, layers[db.names.GC_PARCEL_TYPE_D], feature.attribute(parcel_field))
                    else:
                        value = feature.attribute(parcel_field)
                elif parcel_field == DICT_KEY_PARCEL_T_DEPARTMENT_F:
                    value = feature.attribute(db.names.GC_PARCEL_T_PARCEL_NUMBER_F)[:2]
                elif parcel_field == DICT_KEY_PARCEL_T_NAME_F:
                    value = NULL  # There is no parcel name in supplies model
                dict_attrs[common_key_value_parcel] = value

            dict_attrs[db.names.T_ID_F] = feature[db.names.T_ID_F]  # Finally store t_id

            # Group dictionary by parcel number common key
            if dict_attrs[DICT_KEY_PARCEL_T_PARCEL_NUMBER_F] in dict_features:
                dict_features[dict_attrs[DICT_KEY_PARCEL_T_PARCEL_NUMBER_F]].append(dict_attrs)
            else:
                dict_features[dict_attrs[DICT_KEY_PARCEL_T_PARCEL_NUMBER_F]] = [dict_attrs]

        # =====================  Start adding plot info ==================================================
        plot_fields = [f.name() for f in layers[db.names.GC_PLOT_T].fields()]
        parcel_t_ids = [parcel_feature[db.names.T_ID_F] for parcel_feature in parcel_features]

        expression_plot_features = QgsExpression("{} IN ('{}')".format(db.names.GC_PLOT_T_GC_PARCEL_F, "','".join([str(parcel_t_id) for parcel_t_id in parcel_t_ids])))
        plot_features = self.get_features_by_expression(layers[db.names.GC_PLOT_T], db.names.T_ID_F, expression_plot_features, with_attributes=True, with_geometry=True)
        dict_parcel_plot = {plot_feature[db.names.GC_PLOT_T_GC_PARCEL_F]: plot_feature[db.names.T_ID_F] for plot_feature in plot_features}
        dict_plot_features = {plot_feature[db.names.T_ID_F]: plot_feature for plot_feature in plot_features}

        for feature in dict_features:
            for item in dict_features[feature]:
                if item[db.names.T_ID_F] in dict_parcel_plot:
                    if dict_parcel_plot[item[db.names.T_ID_F]] in dict_plot_features:
                        plot_feature = dict_plot_features[dict_parcel_plot[item[db.names.T_ID_F]]]
                        for plot_field, common_key_value_plot in mapping_plot_field.items():  # plot fields to compare
                            if plot_field in plot_fields:
                                item[common_key_value_plot] = plot_feature[plot_field]

                        item[PLOT_GEOMETRY_KEY] = plot_feature.geometry()
                else:
                    item[PLOT_GEOMETRY_KEY] = None  # No associated plot

        # ===================== Start adding party info ==================================================
        party_fields = [f.name() for f in layers[db.names.GC_OWNER_T].fields()]
        expression_parties_features = QgsExpression("{} IN ({})".format(db.names.GC_OWNER_T_PARCEL_ID_F, ",".join([str(id) for id in parcel_t_ids])))
        party_features = self.get_features_by_expression(layers[db.names.GC_OWNER_T], db.names.T_ID_F, expression_parties_features, with_attributes=True)

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
            db.names.LC_PLOT_T: None,
            db.names.COL_UE_BAUNIT_T: None
        }

        if plot_layer is not None:
            del layers[db.names.LC_PLOT_T]
        if uebaunit_table is not None:
            del layers[db.names.COL_UE_BAUNIT_T]

        if layers:
            self.app.core.get_layers(db, layers, load=True)
            if not layers:
                return None

            if db.names.LC_PLOT_T in layers:
                plot_layer = layers[db.names.LC_PLOT_T]

            if db.names.COL_UE_BAUNIT_T in layers:
                uebaunit_table = layers[db.names.COL_UE_BAUNIT_T]

        expression = QgsExpression("{} IN ('{}') AND {} IS NOT NULL".format(
                                                    db.names.COL_UE_BAUNIT_T_PARCEL_F,
                                                    "','".join([str(t_id) for t_id in t_ids]),
                                                    db.names.COL_UE_BAUNIT_T_LC_PLOT_F))
        features = self.get_features_by_expression(uebaunit_table, db.names.T_ID_F, expression, with_attributes=True)

        plot_t_ids = list()
        for feature in features:
            plot_t_ids.append(feature[db.names.COL_UE_BAUNIT_T_LC_PLOT_F])

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
            db.names.LC_PARCEL_T: None,
            db.names.COL_UE_BAUNIT_T: None
        }

        if parcel_table is not None:
            del layers[db.names.LC_PARCEL_T]
        if uebaunit_table is not None:
            del layers[db.names.COL_UE_BAUNIT_T]

        if layers:
            self.app.core.get_layers(db, layers, load=True)
            if not layers:
                return None

            if db.names.LC_PARCEL_T in layers:
                parcel_table = layers[db.names.LC_PARCEL_T]

            if db.names.COL_UE_BAUNIT_T in layers:
                uebaunit_table = layers[db.names.COL_UE_BAUNIT_T]


        expression = QgsExpression("{} IN ({}) AND {} IS NOT NULL".format(
                                                    db.names.COL_UE_BAUNIT_T_LC_PLOT_F,
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
            db.names.LC_PARCEL_T: None,
            db.names.LC_PLOT_T: None,
            db.names.LC_RIGHT_T: None,
            db.names.LC_PARTY_T: None,
            db.names.LC_GROUP_PARTY_T: None,
            db.names.COL_UE_BAUNIT_T: None,
            db.names.MEMBERS_T: None,
            db.names.LC_CONDITION_PARCEL_TYPE_D: None,
            db.names.LC_PARTY_DOCUMENT_TYPE_D: None,
            db.names.LC_RIGHT_TYPE_D: None,
            db.names.LC_PARTY_DOCUMENT_TYPE_D: None
        }

        self.app.core.get_layers(db, layers, load=True, layer_modifiers=layer_modifiers)
        if not layers:
            return None

        parcel_features = self.get_features_by_search_criterion(layers[db.names.LC_PARCEL_T], db.names.T_ID_F, search_criterion=search_criterion, with_attributes=True)

        # ===================== Start adding parcel info ==================================================
        dict_features = dict()
        for feature in parcel_features:
            dict_attrs = dict()
            for field in layers[db.names.LC_PARCEL_T].fields():
                if field.name() in mapping_parcels_field.keys():  # parcel fields to compare
                    if field.name() == db.names.LC_PARCEL_T_PARCEL_TYPE_F:
                        # Go for domain value, instead of t_id
                        value = self.get_domain_value_from_code(db, layers[db.names.LC_CONDITION_PARCEL_TYPE_D], feature.attribute(field.name()))
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
        expression_uebaunit_features = QgsExpression("{} IN ({}) AND {} IS NOT NULL".format(db.names.COL_UE_BAUNIT_T_PARCEL_F, ",".join([str(id) for id in parcel_t_ids]), db.names.COL_UE_BAUNIT_T_LC_PLOT_F))
        uebaunit_features = self.get_features_by_expression(layers[db.names.COL_UE_BAUNIT_T], db.names.T_ID_F, expression_uebaunit_features, with_attributes=True)

        plot_t_ids = [feature[db.names.COL_UE_BAUNIT_T_LC_PLOT_F] for feature in uebaunit_features]
        expression_plot_features = QgsExpression("{} IN ('{}')".format(db.names.T_ID_F, "','".join([str(id) for id in plot_t_ids])))
        plot_features = self.get_features_by_expression(layers[db.names.LC_PLOT_T], db.names.T_ID_F, expression_plot_features, with_attributes=True, with_geometry=True)

        dict_parcel_plot = {uebaunit_feature[db.names.COL_UE_BAUNIT_T_PARCEL_F]: uebaunit_feature[db.names.COL_UE_BAUNIT_T_LC_PLOT_F] for uebaunit_feature in uebaunit_features}
        dict_plot_features = {plot_feature[db.names.T_ID_F]: plot_feature for plot_feature in plot_features}

        for feature in dict_features:
            for item in dict_features[feature]:
                if item[db.names.T_ID_F] in dict_parcel_plot:
                    if dict_parcel_plot[item[db.names.T_ID_F]] in dict_plot_features:
                        plot_feature = dict_plot_features[dict_parcel_plot[item[db.names.T_ID_F]]]
                        for plot_field, common_key_value_plot in mapping_plot_field.items():  # plot fields to compare
                            item[common_key_value_plot] = plot_feature[plot_field]
                            item[PLOT_GEOMETRY_KEY] = plot_feature.geometry()
                else:
                    item[PLOT_GEOMETRY_KEY] = None  # No associated plot

        # ===================== Start adding party info ==================================================
        expression_right_features = QgsExpression("{} IN ({})".format(db.names.COL_BAUNIT_RRR_T_UNIT_F, ",".join([str(id) for id in parcel_t_ids])))
        right_features = self.get_features_by_expression(layers[db.names.LC_RIGHT_T], db.names.T_ID_F, expression_right_features, with_attributes=True)

        dict_party_right = {right_feature[db.names.COL_RRR_PARTY_T_LC_PARTY_F]: right_feature for right_feature in right_features if right_feature[db.names.COL_RRR_PARTY_T_LC_PARTY_F] != NULL}
        party_t_ids = [right_feature[db.names.COL_RRR_PARTY_T_LC_PARTY_F] for right_feature in right_features if right_feature[db.names.COL_RRR_PARTY_T_LC_PARTY_F] != NULL]
        expression_party_features = QgsExpression("{} IN ({})".format(db.names.T_ID_F, ",".join([str(id) for id in party_t_ids])))
        party_features = self.get_features_by_expression(layers[db.names.LC_PARTY_T], db.names.T_ID_F, expression_party_features, with_attributes=True)

        dict_parcel_parties = dict()
        for right_feature in right_features:
            if right_feature[db.names.COL_BAUNIT_RRR_T_UNIT_F] != NULL and right_feature[db.names.COL_RRR_PARTY_T_LC_PARTY_F] != NULL:
                if right_feature[db.names.COL_BAUNIT_RRR_T_UNIT_F] in dict_parcel_parties:
                    if right_feature[db.names.COL_RRR_PARTY_T_LC_PARTY_F] not in dict_parcel_parties[right_feature[db.names.COL_BAUNIT_RRR_T_UNIT_F]]:
                        dict_parcel_parties[right_feature[db.names.COL_BAUNIT_RRR_T_UNIT_F]].append(right_feature[db.names.COL_RRR_PARTY_T_LC_PARTY_F])
                else:
                    dict_parcel_parties[right_feature[db.names.COL_BAUNIT_RRR_T_UNIT_F]] = [right_feature[db.names.COL_RRR_PARTY_T_LC_PARTY_F]]

        dict_parties = dict()
        for party_feature in party_features:
            dict_party = dict()
            for party_field, common_key_value_party in mapping_party_field.items():  # party fields to compare
                if party_field == db.names.LC_PARTY_T_DOCUMENT_TYPE_F:
                    dict_party[common_key_value_party] = self.get_domain_value_from_code(db, layers[db.names.LC_PARTY_DOCUMENT_TYPE_D], party_feature[party_field])
                else:
                    dict_party[common_key_value_party] = party_feature[party_field]
            # Add extra attribute from right table
            right_type_id = dict_party_right[party_feature[db.names.T_ID_F]][db.names.LC_RIGHT_T_TYPE_F]
            dict_party[DICT_KEY_PARTY_T_RIGHT] = self.get_domain_value_from_code(db, layers[db.names.LC_RIGHT_TYPE_D], right_type_id)
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
            if right_feature[db.names.COL_BAUNIT_RRR_T_UNIT_F] != NULL and right_feature[db.names.COL_RRR_PARTY_T_LC_GROUP_PARTY_F] != NULL:
                if right_feature[db.names.COL_BAUNIT_RRR_T_UNIT_F] in dict_parcel_group_parties:
                    if right_feature[db.names.COL_RRR_PARTY_T_LC_GROUP_PARTY_F] not in dict_parcel_group_parties[right_feature[db.names.COL_BAUNIT_RRR_T_UNIT_F]]:
                        dict_parcel_group_parties[right_feature[db.names.COL_BAUNIT_RRR_T_UNIT_F]].append(right_feature[db.names.COL_RRR_PARTY_T_LC_GROUP_PARTY_F])
                else:
                    dict_parcel_group_parties[right_feature[db.names.COL_BAUNIT_RRR_T_UNIT_F]] = [right_feature[db.names.COL_RRR_PARTY_T_LC_GROUP_PARTY_F]]

        dict_group_party_right = {right_feature[db.names.COL_RRR_PARTY_T_LC_GROUP_PARTY_F]: right_feature for right_feature in right_features if right_feature[db.names.COL_RRR_PARTY_T_LC_GROUP_PARTY_F] != NULL}
        group_party_t_ids = [right_feature[db.names.COL_RRR_PARTY_T_LC_GROUP_PARTY_F] for right_feature in right_features if right_feature[db.names.COL_RRR_PARTY_T_LC_GROUP_PARTY_F] != NULL]
        expression_members_features = QgsExpression("{} IN ({})".format(db.names.MEMBERS_T_GROUP_PARTY_F, ",".join([str(id) for id in group_party_t_ids])))
        members_features = self.get_features_by_expression(layers[db.names.MEMBERS_T], db.names.T_ID_F, expression_members_features, with_attributes=True)

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
        party_features = self.get_features_by_expression(layers[db.names.LC_PARTY_T], db.names.T_ID_F, expression_party_features, with_attributes=True)

        dict_parties = dict()  # {id_party: {tipo_documento: CC, documento_identidad: 123456, nombre: Pepito}}
        for party_feature in party_features:
            dict_party = dict()
            for party_field, common_key_value_party in mapping_party_field.items():  # party fields to compare
                if party_field == db.names.LC_PARTY_T_DOCUMENT_TYPE_F:
                    dict_party[common_key_value_party] = self.get_domain_value_from_code(db, layers[db.names.LC_PARTY_DOCUMENT_TYPE_D], party_feature[party_field])
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
                    right_type_id = dict_group_party_right[id_group_party][db.names.LC_RIGHT_T_TYPE_F]
                    dict_parties[id_party][DICT_KEY_PARTY_T_RIGHT] = self.get_domain_value_from_code(db, layers[db.names.LC_RIGHT_TYPE_D], right_type_id)
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
    def get_t_ids_from_fids(layer, t_id_name, fids):
        request = QgsFeatureRequest(fids)
        request.setFlags(QgsFeatureRequest.NoGeometry)
        field_idx = layer.fields().indexFromName(t_id_name)
        request.setSubsetOfAttributes([field_idx])  # Note: this adds a new flag

        return [feature[t_id_name] for feature in layer.getFeatures(request)]

    @staticmethod
    def get_fids_from_key_values(layer, attribute_name, attribute_values):
        request = QgsFeatureRequest(QgsExpression("{} in ({})".format(attribute_name, ",".join(str(value) for value in attribute_values))))
        request.setFlags(QgsFeatureRequest.NoGeometry)
        request.setNoAttributes()  # Note: this adds a new flag

        return [feature.id() for feature in layer.getFeatures(request)]

    # Two different models (supplies and survey), different field names
    # in each model, so we need to map them to a common key for each field

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
            names.GC_PLOT_T_ALPHANUMERIC_AREA_F: DICT_KEY_PLOT_T_AREA_F
        }

    @staticmethod
    def mapping_parcel_fields(names):
        return {
            names.LC_PARCEL_T_DEPARTMENT_F: DICT_KEY_PARCEL_T_DEPARTMENT_F,
            names.LC_PARCEL_T_FMI_F: DICT_KEY_PARCEL_T_FMI_F,
            names.LC_PARCEL_T_PARCEL_NUMBER_F: DICT_KEY_PARCEL_T_PARCEL_NUMBER_F,
            names.LC_PARCEL_T_PARCEL_TYPE_F: DICT_KEY_PARCEL_T_CONDITION_F,
            names.COL_BAUNIT_T_NAME_F: DICT_KEY_PARCEL_T_NAME_F
        }

    @staticmethod
    def mapping_party_fields(names):
        return {
            names.LC_PARTY_T_DOCUMENT_TYPE_F: DICT_KEY_PARTY_T_DOCUMENT_TYPE_F,
            names.LC_PARTY_T_DOCUMENT_ID_F: DICT_KEY_PARTY_T_DOCUMENT_ID_F,
            names.COL_PARTY_T_NAME_F: DICT_KEY_PARTY_T_NAME_F
        }

    @staticmethod
    def mapping_plot_fields(names):
        return {
            names.LC_PLOT_T_PLOT_AREA_F: DICT_KEY_PLOT_T_AREA_F
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
        value_not_found = False
        domain_table_name = ''

        if not isinstance(db, DBConnector) \
                or not (isinstance(domain_table, str) or isinstance(domain_table, QgsVectorLayer)) \
                or not isinstance(value_is_ilicode, bool):
            return None

        if type(domain_table) is str:
            domain_table_name = domain_table
        else:  # QgsVectorLayer
            domain_table_name = domain_table.name()

        # Try to get it from cache
        found_in_cache, cached_value = db.names.get_domain_code(domain_table_name, value, value_is_ilicode)

        if found_in_cache:
            if DEFAULT_LOG_MODE == EnumLogMode.DEV:
                self.logger.debug(__name__, "(From cache!) Get domain ({}) code from {} ({}): {}".format(
                    domain_table_name, db.names.ILICODE_F if value_is_ilicode else db.names.DISPLAY_NAME_F, value, cached_value))
            return cached_value

        # Not in cache, let's go for the value and cache it
        # TODO: We could even cache all domain values from current table in the first call.

        if type(domain_table) is str:
            domain_table = self.app.core.get_layer(db, domain_table, False, emit_map_freeze=False)

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
                    db.names.cache_domain_value(domain_table_name, res, value, value_is_ilicode)
            else:
                value_not_found = True
        else:
            value_not_found = True

        if value_not_found:
            db.names.cache_wrong_query(QueryNames.VALUE_KEY, domain_table_name, None, value, value_is_ilicode)

        if DEFAULT_LOG_MODE == EnumLogMode.DEV:
            self.logger.debug(__name__, "Get domain ({}) code from {} ({}): {}".format(
                domain_table_name, db.names.ILICODE_F if value_is_ilicode else db.names.DISPLAY_NAME_F, value, res))

        return res

    def get_domain_value_from_code(self, db, domain_table, code, value_is_ilicode=True):
        """
        Get the domain value corresponding to a t_id. First look at the response in a cache.

        :param db: DB Connector object.
        :param domain_table: Table name or QgsVectorLayer
        :param code: t_id to search in the domain.
        :param value_is_ilicode: Whether the result should be iliCode or display name.
        :return: The value corresponding to the given t_id or None.
        """
        res = None
        value_not_found = False
        domain_table_name = ''

        if not isinstance(db, DBConnector) \
                or not (isinstance(domain_table, str) or isinstance(domain_table, QgsVectorLayer)) \
                or not isinstance(value_is_ilicode, bool):
            return None

        if type(domain_table) is str:
            domain_table_name = domain_table
        else:  # QgsVectorLayer
            domain_table_name = domain_table.name()

        # Try to get it from cache
        found_in_cache, cached_value = db.names.get_domain_value(domain_table_name, code, value_is_ilicode)
        if found_in_cache:
            if DEFAULT_LOG_MODE == EnumLogMode.DEV:
                self.logger.debug(__name__, "(From cache!) Get domain ({}) {} from code ({}): {}".format(
                    domain_table_name, db.names.ILICODE_F if value_is_ilicode else db.names.DISPLAY_NAME_F, code, cached_value))
            return cached_value

        # Not in cache, let's go for the value and cache it
        # TODO: We could even cache all domain values from current table in the first call.

        if type(domain_table) is str:
            domain_table = self.app.core.get_layer(db, domain_table, False, emit_map_freeze=False)

        if domain_table is not None:
            features = self.get_features_from_t_ids(domain_table, db.names.T_ID_F, [code], no_attributes=False, no_geometry=True)
            if features:
                res = features[0][db.names.ILICODE_F if value_is_ilicode else db.names.DISPLAY_NAME_F]
                if res is not None:
                    db.names.cache_domain_value(domain_table_name, code, res, value_is_ilicode)
            else:
                value_not_found = True
        else:
            value_not_found = True

        if value_not_found:
            db.names.cache_wrong_query(QueryNames.CODE_KEY, domain_table_name, res, None, value_is_ilicode)

        if DEFAULT_LOG_MODE == EnumLogMode.DEV:
            self.logger.debug(__name__, "Get domain ({}) {} from code ({}): {}".format(
                domain_table_name, db.names.ILICODE_F if value_is_ilicode else db.names.DISPLAY_NAME_F, code, res))

        return res

    """
    FIELD DATA CAPTURE Model
    """
    def get_parcel_data_field_data_capture(self, names, fdc_parcel_layer, get_field_name):
        request = QgsFeatureRequest()
        field_names = [names.FDC_PARCEL_T_PARCEL_NUMBER_F, get_field_name]
        request.setSubsetOfAttributes(field_names, fdc_parcel_layer.fields())

        return {feature.id(): (feature[names.FDC_PARCEL_T_PARCEL_NUMBER_F], feature[get_field_name]) for feature in fdc_parcel_layer.getFeatures(request)}

    @staticmethod
    def get_plots_related_to_parcels_field_data_capture(names, fdc_parcel_layer, fdc_plot_layer, get_feature=False, fids=list(), t_ids=list()):
        """
        :param names: Table and field names from the DB
        :param fdc_parcel_layer: parcel layer from the Field Data Capture model
        :param fdc_plot_layer: plot layer from the Field Data Capture model
        :param get_feature: Whether to get whole features or just fids
        :param fids: list of parcel fids.
        :param t_ids: list of parcel t_ids. If present, they'll be used, no matter that fids is also passed.
        :return: list of plot fids related to the given parcel fids
        """
        if not t_ids:
            t_ids = LADMData.get_t_ids_from_fids(fdc_parcel_layer, names.T_ID_F, fids)

        request = QgsFeatureRequest(QgsExpression("{} in ({})".format(names.FDC_PLOT_T_PARCEL_F, ",".join([str(t_id) for t_id in t_ids]))))
        request.setFlags(QgsFeatureRequest.NoGeometry)
        request.setNoAttributes()

        if get_feature:
            return [feature for feature in fdc_plot_layer.getFeatures(request)]

        return [feature.id() for feature in fdc_plot_layer.getFeatures(request)]  # Just fids

    @staticmethod
    def get_parcels_related_to_plots_field_data_capture(names, fids, fdc_plot_layer, fdc_parcel_layer):
        """
        :param names: Table and field names from the DB
        :param fids: list of plot ids
        :param fdc_plot_layer: plot layer from the Field Data Capture model
        :param fdc_parcel_layer: parcel layer from the Field Data Capture model
        :return: list of parcel ids related to the given plot ids
        """
        request = QgsFeatureRequest(fids)
        request.setFlags(QgsFeatureRequest.NoGeometry)
        field_idx = fdc_plot_layer.fields().indexFromName(names.FDC_PLOT_T_PARCEL_F)
        request.setSubsetOfAttributes([field_idx])
        parcel_t_ids = [feature[names.FDC_PLOT_T_PARCEL_F] for feature in fdc_plot_layer.getFeatures(request)]

        request = QgsFeatureRequest(QgsExpression("{} in ({})".format(names.T_ID_F, ",".join([str(t_id) for t_id in parcel_t_ids]))))
        request.setNoAttributes()

        return [feature.id() for feature in fdc_parcel_layer.getFeatures(request)]

    @staticmethod
    def save_allocation_for_receiver_field_data_capture(parcel_ids, receiver_id, referencing_field, fdc_parcel_layer):
        field_idx = fdc_parcel_layer.fields().indexOf(referencing_field)
        attr_map = {parcel_id: {field_idx: receiver_id} for parcel_id in parcel_ids}

        return fdc_parcel_layer.dataProvider().changeAttributeValues(attr_map)

    @staticmethod
    def get_parcels_for_receiver_field_data_capture(attr_name, receiver_id, referencing_field, fdc_parcel_layer):
        request = QgsFeatureRequest(QgsExpression("{} = {}".format(referencing_field, receiver_id)))
        request.setSubsetOfAttributes([attr_name], fdc_parcel_layer.fields())

        return {feature.id(): feature[attr_name] for feature in fdc_parcel_layer.getFeatures(request)}

    @staticmethod
    def discard_parcel_allocation_field_data_capture(db, parcel_ids, fdc_parcel_layer):
        value, msg = LADMData.get_or_create_default_ili2db_basket(db)
        if not value:
            return False
        return LADMData.change_attribute_value(fdc_parcel_layer, db.names.T_BASKET_F, value, parcel_ids)

    @staticmethod
    def get_fdc_user_name(names, feature, full_name=True):
        if full_name:
            name = feature[names.FDC_USER_T_NAME_F]
        else:  # Just initial letters for each name part, except the last name (e.g., gacarrillor)
            name = LADMData.get_name_alias(feature[names.FDC_USER_T_NAME_F])

        return name.strip()

    @staticmethod
    def get_name_alias(name):
        alias = ""
        parts = name.split(" ")
        if len(parts) == 1:
            alias = name
        elif len(parts) == 2:
            alias = parts[0][:1] + parts[1]
        elif len(parts) == 3:
            alias = parts[0][:1] + parts[1] + parts[2][:1]
        elif len(parts) > 3:
            alias = parts[0][:1] + parts[1] + parts[2][:1] + parts[3][:1]
        return alias.lower() or '-'  # No names? Then avoid falsy value

    @staticmethod
    def get_layer_expressions_per_receiver_field_data_capture(names, receiver_type, referencing_field, referenced_field, fdc_parcel_layer, fdc_plot_layer, fdc_user_layer):
        """
        Based on parcels that are allocated to receivers, get expressions to get related objects in the DB.
        For surveyors we need the expressions to select features and export to offline projects, whereas
        for Coordinators we need the expressions to know what objects belong to a given basket.

        Note: Currently, this method is aimed at surveyors.

        :param names: Table and Field names object from the DB connector
        :param receiver_type: Type of receiver
        :param referencing_field: Parcel layer field referencing receivers
        :param referenced_field: Receivers layer field referenced by parcels
        :param fdc_parcel_layer: Parcel QgsVectorLayer
        :param fdc_plot_layer: Plot QgsVectorLayer
        :param fdc_user_layer: User QgsVectorLayer
        :return: {receiver_id: {parcel_layer_name: "expr_parcels", plot_layer_name: "expr_plots", ...}
        """
        layer_expressions_per_receiver = dict()
        receiver_dict = LADMData.get_fdc_receivers_data(names, fdc_user_layer, referenced_field, receiver_type, False)

        # Get receiver_ids that actually have at least one parcel assigned (basically, an INNER JOIN)
        # For that: Go to parcel layer and get uniques, then filter that list comparing it with receiver ids from users
        receiver_idx = fdc_parcel_layer.fields().indexOf(referencing_field)
        receiver_ids = fdc_parcel_layer.uniqueValues(receiver_idx)

        # Make sure the list contains only valid receivers
        # First part of the conditional:
        #   Specially useful when receiver id is a t_basket, because we might get baskets that don't belong to receivers
        # Second part of the conditional:
        #   When the receiver id is a t_id, chances are parcels are not allocated, and then NULL may come in that list
        receiver_ids = [receiver_id for receiver_id in receiver_ids if receiver_id in receiver_dict and receiver_id is not NULL]

        for receiver_id in receiver_ids:
            # Get parcels per receiver id --> {parcel_id: parcel_t_id}
            parcel_data = LADMData.get_parcels_for_receiver_field_data_capture(names.T_ID_F,  # We want parcel t_ids
                                                                               receiver_id,
                                                                               referencing_field,
                                                                               fdc_parcel_layer)
            parcel_t_ids = list(parcel_data.values())

            # Get plots from parcels
            plot_ids = LADMData.get_plots_related_to_parcels_field_data_capture(names,
                                                                                fdc_parcel_layer,
                                                                                fdc_plot_layer,
                                                                                t_ids=parcel_t_ids)

            # Warning: Use QGIS ids if you're sure it'll get always the same records.
            # For some reason that does not happen with parcels, that's why we prefer t_ids.
            layer_expressions_per_receiver[receiver_dict[receiver_id][0]] = {
                names.FDC_PARCEL_T: LADMData.build_layer_expression(parcel_t_ids, names.T_ID_F),
                names.FDC_PLOT_T: LADMData.build_layer_expression(plot_ids),
                names.FDC_USER_T: LADMData.build_layer_expression([receiver_id], referenced_field)  # t_id or t_basket
            }
            # TODO: Do the same with other tables (rights, parties, etc.)

        return layer_expressions_per_receiver

    @staticmethod
    def build_layer_expression(values, field='$id'):
        expression = ""
        if values:
            if len(values) == 1:
                expression = "{} = {}".format(field, values[0])
            else:  # len(fids) > 1
                expression = "{} in ({})".format(field, ",".join([str(fid) for fid in values]))

        return expression

    @staticmethod
    def set_basket_for_features_related_to_allocated_parcels_field_data_capture(db, receiver_type, referencing_field, referenced_field, fdc_parcel_layer, fdc_plot_layer, fdc_user_layer):
        """
        Based on parcels that are allocated to receivers, get related objects in the DB and set the receiver's basket id
        to them. Note that both user and parcel layers already have the basket id correctly set.

        :param db: DB connector object
        :param receiver_type: Type of receiver
        :param referencing_field: Parcel layer field referencing receivers
        :param referenced_field: Receivers layer field referenced by parcels
        :param fdc_parcel_layer: Parcel QgsVectorLayer
        :param fdc_plot_layer: Plot QgsVectorLayer
        :param fdc_user_layer: User QgsVectorLayer
        :return: {receiver_id: {parcel_layer_name: "expr_parcels", plot_layer_name: "expr_plots", ...}
        """
        names = db.names
        receiver_dict = LADMData.get_fdc_receivers_data(names, fdc_user_layer, referenced_field, receiver_type, False)

        # Get receiver_ids that actually have at least one parcel assigned (basically, an INNER JOIN)
        # For that: Go to parcel layer and get uniques, then filter that list comparing it with receiver ids from users
        receiver_idx = fdc_parcel_layer.fields().indexOf(referencing_field)
        receiver_ids = fdc_parcel_layer.uniqueValues(receiver_idx)

        # Make sure the list contains only valid receivers
        # First part of the conditional:
        #   Specially useful when receiver id is a t_basket, because we might get baskets that don't belong to receivers
        # Second part of the conditional:
        #   When the receiver id is a t_id, chances are parcels are not allocated, and then NULL may come in that list
        receiver_ids = [receiver_id for receiver_id in receiver_ids if receiver_id in receiver_dict and receiver_id is not NULL]

        # Before setting receiver basket ids to objects related to allocated parcels,
        # let's reset basket ids in tables, setting them to the default basket.
        default_basket_id, msg = LADMData.get_or_create_default_ili2db_basket(db)
        if default_basket_id is None:
            return False, msg

        res = LADMData.change_attribute_value(fdc_plot_layer, referenced_field, default_basket_id)
        if not res:
            return False, QCoreApplication.translate("LADMData",
                                                     "Could not write default basket id ({}) to Plot layer.").format(default_basket_id)

        Logger().info(__name__, "Setting basket ids to db objects related to {} receivers...".format(len(receiver_ids)))
        for receiver_id in receiver_ids:
            # Get parcels per receiver id --> {parcel_id: parcel_t_id}
            parcel_data = LADMData.get_parcels_for_receiver_field_data_capture(names.T_ID_F,  # We want parcel t_ids
                                                                               receiver_id,
                                                                               referencing_field,
                                                                               fdc_parcel_layer)
            parcel_t_ids = list(parcel_data.values())

            # Get plots from parcels and write the basket
            plot_ids = LADMData.get_plots_related_to_parcels_field_data_capture(names,
                                                                                fdc_parcel_layer,
                                                                                fdc_plot_layer,
                                                                                get_feature=False,  # get_fids
                                                                                t_ids=parcel_t_ids)
            if plot_ids:
                res = LADMData.change_attribute_value(fdc_plot_layer,
                                                      referenced_field,
                                                      receiver_id,
                                                      plot_ids)
                if not res:
                    return False, QCoreApplication.translate("LADMData",
                                                             "Could not write basket id {} to Plot layer for receiver {}.".format(
                                                                 receiver_id,
                                                                 receiver_dict[receiver_id][0]))

            Logger().info(__name__, "--> Basket exported for receiver {}: {} parcels, {} plots".format(receiver_id,
                                                                                                       len(parcel_t_ids),
                                                                                                       len(plot_ids)))

            # TODO: Do the same with other tables (rights, parties, buildings, etc.)

        return True, "Success!"

    @staticmethod
    def change_attribute_value(layer, field_name, value, fids=list(), filter=''):
        """
        Change attribute values for a vector layer.
        WARNING: If you don't pass fids nor filter, this method writes the value to ALL layer features!!!

        :param layer: QgsVectorLayer to modify
        :param field_name: Name of the field to be modified
        :param value: Value to be written in the corresponding field
        :param fids: List of QGIS ids for features that will be modified
        :param filter: String expression to filter features that will be modified
        :return: Whether the update was successful or not
        """
        idx = layer.fields().indexOf(field_name)
        attr_map = dict()
        if fids:
            attr_map = {fid: {idx: value} for fid in fids}
        else:
            if filter:
                request = QgsFeatureRequest(QgsExpression(filter))
            else:
                request = QgsFeatureRequest()

            request.setFlags(QgsFeatureRequest.NoGeometry)
            request.setNoAttributes()
            features = layer.getFeatures(request)
            attr_map = {feature.id(): {idx: value} for feature in features}

        Logger().debug(__name__, "Changing '{}'.'{}' to '{}' ({} features)".format(layer.name(),
                                                                                   field_name,
                                                                                   value,
                                                                                   len(attr_map)))
        return layer.dataProvider().changeAttributeValues(attr_map)

    @staticmethod
    def get_fdc_receivers_data(names, fdc_user_layer, id_field_name, receiver_type, full_name=True, extra_attr_name=''):
        """
        Get receiver's filtered data

        :param names: DB names object
        :param fdc_user_layer: User QgsVectorLayer
        :param id_field_name: Name of the field to be used as dictionary keys
        :param receiver_type: T_id of the role type we want to filter
        :param full_name: Whether to get the full name or just an alias for the user
        :param extra_attr_name: Name of an extra field to append to the result

        :return: Receiver's dictionary: {id: (name, extra_attribute)}
        """
        receivers_data = dict()
        if not extra_attr_name:
            extra_attr_name = names.FDC_USER_T_DOCUMENT_ID_F

        # Filter by role (note that receiver_type should be the t_id of the 'user type' domain value)
        for feature in fdc_user_layer.getFeatures("{} = {}".format(names.FDC_USER_T_ROLE_F, receiver_type)):
            receivers_data[feature[id_field_name]] = (LADMData.get_fdc_user_name(names, feature, full_name),
                                                      feature[extra_attr_name])

        return receivers_data

    @staticmethod
    def save_receiver(receiver_data, fdc_user_layer):
        attrs = dict()
        for field_name, value in receiver_data.items():
            attrs[fdc_user_layer.fields().indexOf(field_name)] = value

        feature = QgsVectorLayerUtils().createFeature(fdc_user_layer, attributes=attrs)
        return fdc_user_layer.dataProvider().addFeatures([feature])

    @staticmethod
    def __delete_receiver(attribute_name, attribute_value, fdc_user_layer):
        return fdc_user_layer.dataProvider().deleteFeatures(LADMData.get_fids_from_key_values(fdc_user_layer,
                                                                                              attribute_name,
                                                                                              [attribute_value]))

    @staticmethod
    def delete_surveyor(names, receiver_id, fdc_user_layer):
        res = LADMData.__delete_receiver(names.T_BASKET_F, receiver_id, fdc_user_layer)
        msg = ''
        if not res:
            msg = QCoreApplication.translate("LADMData", "There was an error deleting the surveyor.")
        return res, msg

    def delete_coordinator(self, db, receiver_id, surveyor_type, fdc_user_layer):
        # To delete a coordinator, he/she cannot have associated surveyors.
        # Once the coordinator is deleted, we attempt to delete his associated basket. If we cannot do it, we leave it
        # there, his allocated objects will be reset next time the data is exported to XTF.
        res = False
        msg = ''

        # Get dict of all users that are surveyors: {t_id_1: (name_1, t_basket_1), ...}
        surveyors = LADMData.get_fdc_receivers_data(db.names, fdc_user_layer, db.names.T_ID_F, surveyor_type, extra_attr_name=db.names.T_BASKET_F)
        coordinator_surveyors = [str(k) for k,v in surveyors.items() if v[1] == receiver_id]

        if not coordinator_surveyors:
            self.logger.debug(__name__, "The coordinator (BID: {}) has no associated surveyors, so we can proceed deleting it.")
            res = LADMData.__delete_receiver(db.names.T_BASKET_F, receiver_id, fdc_user_layer)

            if res:  # Let's attempt to delete his associated basket from the db
                basket_table = LADMData.get_basket_table(db)
                basket_fid = LADMData.get_fids_from_key_values(basket_table, db.names.T_ID_F, [receiver_id])
                res_basket = basket_table.dataProvider().deleteFeatures(basket_fid)
                if not res_basket:  # Get rid of the error displayed by the provider in the message bar
                    self.logger.clear_message_bar()
                    self.logger.debug(__name__, "The basket () couldn't be deleted. It is probably used in a DB object (however, in the next export to XTF it will be replaced).".format(receiver_id))
                else:
                    self.logger.debug(__name__, "The associated basket () was deleted as well!".format(receiver_id))

            else:  # The coordinator has no associated surveyors but couldn't be deleted
                msg = QCoreApplication.translate("LADMData",
                                                 "The coordinator cannot be removed. (Hint: He/she could have associated parcels)")
        else:
            self.logger.debug(__name__, "Surveyors found for coordinator (BID: {}): {}".format(receiver_id, ",".join(coordinator_surveyors)))
            msg = QCoreApplication.translate("LADMData",
                                             "This coordinator has {} associated surveyors. He/she needs to delete his surveyors before you can delete the coordinator!").format(len(coordinator_surveyors))

        return res, msg

    @staticmethod
    def get_summary_of_allocation_field_data_capture(names, receiver_type, referencing_field, referenced_field, fdc_parcel_layer, fdc_user_layer):
        surveyors_data = LADMData.get_fdc_receivers_data(names, fdc_user_layer, referenced_field, receiver_type)
        surveyor_parcel_count = dict()  # {surveyor_name: parcel_count}
        params = QgsAggregateCalculator.AggregateParameters()
        for surveyor_id, surveyor_data in surveyors_data.items():
            params.filter = "{} = {}".format(referencing_field, surveyor_id)
            surveyor_name = surveyors_data[surveyor_id][0]  # (name, doc_id)
            surveyor_parcel_count[surveyor_name] = int(fdc_parcel_layer.aggregate(QgsAggregateCalculator.Count,
                                                                                  referencing_field,
                                                                                  params)[0])  # val (float), res (bool)

        return sorted(surveyor_parcel_count.items(), key=lambda x:locale.strxfrm(x[0]))

    @staticmethod
    def get_count_of_not_allocated_parcels_to_receivers_field_data_capture(names, receiver_type, fdc_parcel_layer, fdc_user_layer):
        """
        :param names: Table and field names
        :param receiver_type: Type of receiver
        :param fdc_parcel_layer: QgsVectorLayer
        :param fdc_user_layer: QgsVectorLayer
        :return: Count of not allocated parcels
        """
        receivers_data = LADMData.get_fdc_receivers_data(names, fdc_user_layer, names.T_BASKET_F, receiver_type)
        receivers_ids = list(receivers_data.keys())  # t_baskets
        params = QgsAggregateCalculator.AggregateParameters()

        # We need to count parcels that have no basket associated with users (not that all parcels have baskets, even if
        # it is the default basket created at import time)
        params.filter = "{} not in ({})".format(names.T_BASKET_F, ",".join([str(receiver_id) for receiver_id in receivers_ids]))

        return int(fdc_parcel_layer.aggregate(QgsAggregateCalculator.Count,
                                              names.T_BASKET_F,
                                              params)[0])  # val (float), res (bool)

    @staticmethod
    def get_basket_table(db):
        return QgsVectorLayer(db.get_qgis_layer_uri(db.names.T_ILI2DB_BASKET_T), 'baskets', db.provider)

    @staticmethod
    def get_dataset_table(db):
        return QgsVectorLayer(db.get_qgis_layer_uri(db.names.T_ILI2DB_DATASET_T), 'datasets', db.provider)

    @staticmethod
    def get_or_create_ili2db_basket(db, dataset_name, topic_name, get_feature=False):
        """
        Get or create an ili2db basket by dataset name.
        If you need to find several baskets, or if you need a specific basket from a dataset, this is not the function
        for you; either use create_ili2db_basket() or get the baskets table and do it by yourself :)

        In the get mode, this function gets only the first basket found in the dataset, so it's better suited for
        datasets that will have a single basket (like the default field data capture dataset).

        :param db: DB connector object
        :param dataset_name: name of the dataset to be searched or to be used as new dataset name
        :param topic_name: name of the topic the basket applies to...
        :param get_feature: Whether to get the whole feature or just its t_id
        :return: Tuple: t_id (or None), message (useful in case of failure)
        """
        basket_table = LADMData.get_basket_table(db)

        dataset_t_id, msg = LADMData.get_or_create_ili2db_dataset_t_id(db, dataset_name)
        Logger().info(__name__, "Dataset id: {}".format(dataset_t_id))
        if dataset_t_id is None:
            return None, msg

        # We have the dataset, so go for the first basket we find in such dataset, otherwise create one
        baskets = [f for f in basket_table.getFeatures("{} = {}".format(db.names.BASKET_T_DATASET_F, dataset_t_id))]
        if baskets:
            return baskets[0] if get_feature else baskets[0][db.names.T_ID_F], "Success!"

        # Create basket since we didn't find it
        basket_feature, msg = LADMData.create_ili2db_basket(db, dataset_t_id, topic_name, basket_table)

        return basket_feature if get_feature else basket_feature[db.names.T_ID_F], "Success!"

    @staticmethod
    def create_ili2db_basket(db, dataset_t_id, topic_name, basket_table=None):
        if not basket_table:
            basket_table = LADMData.get_basket_table(db)

        t_id_idx = basket_table.fields().indexOf(db.names.T_ID_F)
        max_value = basket_table.maximumValue(t_id_idx) or 0
        new_basket_t_id = max_value + 1  # Basket t_id is not a serial, we need to create it manually...
        attrs = {
            t_id_idx: new_basket_t_id,
            basket_table.fields().indexOf(db.names.BASKET_T_DATASET_F): dataset_t_id,
            basket_table.fields().indexOf(db.names.T_ILI_TID_F): str(uuid.uuid4()),
            basket_table.fields().indexOf(db.names.BASKET_T_TOPIC_F): topic_name,
            basket_table.fields().indexOf(db.names.BASKET_T_ATTACHMENT_KEY_F): "..."
        }
        basket_feature = QgsVectorLayerUtils().createFeature(basket_table, attributes=attrs)
        res = basket_table.dataProvider().addFeatures([basket_feature])
        if not res:
            msg = QCoreApplication.translate("LADMData", "A basket could not be found (or created)!!!")
            Logger().warning(__name__, msg)
            return None, msg

        return basket_feature, "Success!"


    @staticmethod
    def get_or_create_ili2db_dataset_t_id(db, dataset_name):
        """
        Get or create an ili2db dataset by name

        :param db: DB connector
        :param dataset_name: name of the dataset to be searched or to be used as new dataset name
        :return: Dataset t_id or None (if it was not possible to create it), message (useful for failures)
        """
        dataset_table = LADMData.get_dataset_table(db)
        datasets = [f for f in dataset_table.getFeatures("{} = '{}'".format(db.names.DATASET_T_DATASETNAME_F, dataset_name))]

        if datasets:
            return datasets[0][db.names.T_ID_F], "Success!"
        else:
            t_id_idx = dataset_table.fields().indexOf(db.names.T_ID_F)
            max_value = dataset_table.maximumValue(t_id_idx) or 0
            new_dataset_t_id = max_value + 1  # Dataset t_id is not a serial, we need to create it manually...
            attrs = {
                t_id_idx: new_dataset_t_id,
                dataset_table.fields().indexOf(db.names.DATASET_T_DATASETNAME_F): dataset_name
            }
            feature = QgsVectorLayerUtils().createFeature(dataset_table, attributes=attrs)
            res = dataset_table.dataProvider().addFeatures([feature])
            if not res:
                msg = QCoreApplication.translate("LADMData", "A dataset could not be found (or created)!!!")
                Logger().warning(__name__, msg)
                return None, msg

            return new_dataset_t_id, "Success!"

    @staticmethod
    def get_or_create_default_ili2db_basket(db):
        fdc_model = LADMColModelRegistry().model(LADMNames.FIELD_DATA_CAPTURE_MODEL_KEY).full_name()
        default_basket_id, msg = LADMData.get_or_create_ili2db_basket(db,
                                                                      DEFAULT_DATASET_NAME,
                                                                      "{}.{}".format(fdc_model, LADMNames.FDC_TOPIC_NAME))
        Logger().info(__name__, "Default basket_id: {}".format(default_basket_id))
        return default_basket_id, msg

    @staticmethod
    def get_document_types(names, fdc_document_types_table):
        data = dict()
        for feature in fdc_document_types_table.getFeatures():
            data[feature[names.T_ID_F]] = feature[names.DISPLAY_NAME_F]

        return data