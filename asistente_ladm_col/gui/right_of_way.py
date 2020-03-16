# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 03/12/18
        git sha              : :%H$
        copyright            : (C) 2018 by Sergio Ramírez (Incige SAS)
        email                : sergio.ramirez@incige.com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""

from qgis.PyQt.QtCore import (QObject,
                              QCoreApplication)
from qgis.core import (Qgis,
                       QgsProcessingFeatureSourceDefinition,
                       QgsWkbTypes,
                       QgsVectorLayerUtils)

import processing
from asistente_ladm_col.config.general_config import LAYER
from asistente_ladm_col.config.ladm_names import LADMNames
from asistente_ladm_col.lib.logger import Logger


class RightOfWay(QObject):
    def __init__(self, iface, qgis_utils, names):
        QObject.__init__(self)
        self.iface = iface
        self.qgis_utils = qgis_utils
        self.logger = Logger()
        self.names = names

        self._layers = {
            self.names.OP_PLOT_T: {'name': self.names.OP_PLOT_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            self.names.OP_RIGHT_OF_WAY_T: {'name': self.names.OP_RIGHT_OF_WAY_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            self.names.OP_SURVEY_POINT_T: {'name': self.names.OP_SURVEY_POINT_T, 'geometry': None, LAYER: None}
        }

        self._right_of_way_line_layer = None
        self.addedFeatures = None

    def fill_right_of_way_relations(self, db):
        layers = {
            self.names.OP_ADMINISTRATIVE_SOURCE_T: {'name': self.names.OP_ADMINISTRATIVE_SOURCE_T, 'geometry': None, LAYER: None},
            self.names.OP_PARCEL_T: {'name': self.names.OP_PARCEL_T, 'geometry': None, LAYER: None},
            self.names.OP_PLOT_T: {'name': self.names.OP_PLOT_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            self.names.OP_RESTRICTION_T: {'name': self.names.OP_RESTRICTION_T, 'geometry': None, LAYER: None},
            self.names.OP_RESTRICTION_TYPE_D: {'name': self.names.OP_RESTRICTION_TYPE_D, 'geometry': None, LAYER: None},
            self.names.OP_RIGHT_OF_WAY_T: {'name': self.names.OP_RIGHT_OF_WAY_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            self.names.COL_RRR_SOURCE_T: {'name': self.names.COL_RRR_SOURCE_T, 'geometry': None, LAYER: None},
            self.names.OP_SURVEY_POINT_T: {'name': self.names.OP_SURVEY_POINT_T, 'geometry': None, LAYER: None},
            self.names.COL_UE_BAUNIT_T: {'name': self.names.COL_UE_BAUNIT_T, 'geometry': None, LAYER: None}
        }

        # Load layers
        self.qgis_utils.get_layers(db, layers, load=True)
        if not layers:
            return None

        exp = "\"{}\" = '{}'".format(self.names.ILICODE_F, LADMNames.RESTRICTION_TYPE_D_RIGHT_OF_WAY_ILICODE_VALUE)
        restriction_right_of_way_t_id = [feature for feature in layers[self.names.OP_RESTRICTION_TYPE_D][LAYER].getFeatures(exp)][0][self.names.T_ID_F]

        if layers[self.names.OP_PLOT_T][LAYER].selectedFeatureCount() == 0 or layers[self.names.OP_RIGHT_OF_WAY_T][LAYER].selectedFeatureCount() == 0 or layers[self.names.OP_ADMINISTRATIVE_SOURCE_T][LAYER].selectedFeatureCount() == 0:
            if self.qgis_utils.get_layer_from_layer_tree(db, self.names.OP_PLOT_T, geometry_type=QgsWkbTypes.PolygonGeometry) is None:
                self.logger.message_with_button_load_layer_emitted.emit(
                    QCoreApplication.translate("RightOfWay",
                                               "First load the layer {} into QGIS and select at least one plot!").format(self.names.OP_PLOT_T),
                    QCoreApplication.translate("RightOfWay", "Load layer {} now").format(self.names.OP_PLOT_T),
                    self.names.OP_PLOT_T,
                    Qgis.Warning)
            else:
                self.logger.warning_msg(__name__, QCoreApplication.translate("RightOfWay",
                    "Select at least one benefited plot, one right of way and at least one administrative source to create relations!"))
                return
        else:
            ue_baunit_features = layers[self.names.COL_UE_BAUNIT_T][LAYER].getFeatures()
            # Get unique pairs id_right_of_way-id_parcel
            existing_pairs = [(ue_baunit_feature[self.names.COL_UE_BAUNIT_T_PARCEL_F], ue_baunit_feature[self.names.COL_UE_BAUNIT_T_OP_RIGHT_OF_WAY_F]) for ue_baunit_feature in ue_baunit_features]
            existing_pairs = set(existing_pairs)

            plot_ids = [f[self.names.T_ID_F] for f in layers[self.names.OP_PLOT_T][LAYER].selectedFeatures()]

            right_of_way_id = layers[self.names.OP_RIGHT_OF_WAY_T][LAYER].selectedFeatures()[0].attribute(self.names.T_ID_F)
            id_pairs = list()
            for plot in plot_ids:
                exp = "\"{uebaunit}\" = {plot}".format(uebaunit=self.names.COL_UE_BAUNIT_T_OP_PLOT_F, plot=plot)
                parcels = layers[self.names.COL_UE_BAUNIT_T][LAYER].getFeatures(exp)
                for parcel in parcels:
                    id_pair = (parcel.attribute(self.names.COL_UE_BAUNIT_T_PARCEL_F), right_of_way_id)
                    id_pairs.append(id_pair)

            if len(id_pairs) < len(plot_ids):
                # If any relationship plot-parcel is not found, we don't need to continue
                self.qlogger.warning_msg(__name__, QCoreApplication.translate("RightOfWay",
                    "One or more pairs id_plot-id_parcel weren't found, this is needed to create benefited and restriction relations."))
                return

            if id_pairs:
                new_features = list()
                for id_pair in id_pairs:
                    if not id_pair in existing_pairs:
                        #Create feature
                        new_feature = QgsVectorLayerUtils().createFeature(layers[self.names.COL_UE_BAUNIT_T][LAYER])
                        new_feature.setAttribute(self.names.COL_UE_BAUNIT_T_PARCEL_F, id_pair[0])
                        new_feature.setAttribute(self.names.COL_UE_BAUNIT_T_OP_RIGHT_OF_WAY_F, id_pair[1])
                        self.logger.info(__name__, "Saving RightOfWay-Parcel: {}-{}".format(id_pair[1], id_pair[0]))
                        new_features.append(new_feature)

                layers[self.names.COL_UE_BAUNIT_T][LAYER].dataProvider().addFeatures(new_features)
                self.logger.info_msg(__name__, QCoreApplication.translate("RightOfWay",
                    "{} out of {} records were saved into {}! {} out of {} records already existed in the database.").format(
                        len(new_features),
                        len(id_pairs),
                        self.names.COL_UE_BAUNIT_T,
                        len(id_pairs) - len(new_features),
                        len(id_pairs)
                    ))

            spatial_join_layer = processing.run("qgis:joinattributesbylocation",
                                                {
                                                    'INPUT': layers[self.names.OP_PLOT_T][LAYER],
                                                    'JOIN': QgsProcessingFeatureSourceDefinition(layers[self.names.OP_RIGHT_OF_WAY_T][LAYER].id(), True),
                                                    'PREDICATE': [0],
                                                    'JOIN_FIELDS': [self.names.T_ID_F],
                                                    'METHOD': 0,
                                                    'DISCARD_NONMATCHING': True,
                                                    'PREFIX': '',
                                                    'OUTPUT': 'memory:'})['OUTPUT']

            restriction_features = layers[self.names.OP_RESTRICTION_T][LAYER].getFeatures()
            existing_restriction_pairs = [(restriction_feature[self.names.COL_BAUNIT_RRR_T_UNIT_F], restriction_feature[self.names.COL_RRR_T_DESCRIPTION_F]) for restriction_feature in restriction_features]
            existing_restriction_pairs = set(existing_restriction_pairs)
            id_pairs_restriction = list()
            plot_ids = spatial_join_layer.getFeatures()

            for plot in plot_ids:
                exp = "\"uebaunit\" = {plot}".format(uebaunit=self.names.COL_UE_BAUNIT_T_OP_PLOT_F, plot=plot.attribute(self.names.T_ID_F))
                parcels = layers[self.names.COL_UE_BAUNIT_T][LAYER].getFeatures(exp)
                for parcel in parcels:
                    id_pair_restriction = (parcel.attribute(self.names.COL_UE_BAUNIT_T_PARCEL_F), QCoreApplication.translate("RightOfWay", "Right of way"))
                    id_pairs_restriction.append(id_pair_restriction)

            new_restriction_features = list()
            if id_pairs_restriction:
                for id_pair in id_pairs_restriction:
                    if not id_pair in existing_restriction_pairs:
                        #Create feature
                        new_feature = QgsVectorLayerUtils().createFeature(layers[self.names.OP_RESTRICTION_T][LAYER])
                        new_feature.setAttribute(self.names.COL_BAUNIT_RRR_T_UNIT_F, id_pair[0])
                        new_feature.setAttribute(self.names.COL_RRR_T_DESCRIPTION_F, id_pair[1])
                        new_feature.setAttribute(self.names.OP_RESTRICTION_T_TYPE_F, restriction_right_of_way_t_id)
                        self.logger.info(__name__, "Saving RightOfWay-Parcel: {}-{}".format(id_pair[1], id_pair[0]))
                        new_restriction_features.append(new_feature)

                layers[self.names.OP_RESTRICTION_T][LAYER].dataProvider().addFeatures(new_restriction_features)
                self.logger.info_msg(__name__, QCoreApplication.translate("RightOfWay",
                    "{} out of {} records were saved into {}! {} out of {} records already existed in the database.").format(
                        len(new_restriction_features),
                        len(id_pairs_restriction),
                        self.names.OP_RESTRICTION_T,
                        len(id_pairs_restriction) - len(new_restriction_features),
                        len(id_pairs_restriction)
                    ))

            administrative_source_ids = [f[self.names.T_ID_F] for f in layers[self.names.OP_ADMINISTRATIVE_SOURCE_T][LAYER].selectedFeatures()]

            source_relation_features = layers[self.names.COL_RRR_SOURCE_T][LAYER].getFeatures()

            existing_source_pairs = [(source_relation_feature[self.names.COL_RRR_SOURCE_T_SOURCE_F], source_relation_feature[self.names.COL_RRR_SOURCE_T_OP_RESTRICTION_F]) for source_relation_feature in source_relation_features]
            existing_source_pairs = set(existing_source_pairs)

            rrr_source_relation_pairs = list()

            for administrative_source_id in administrative_source_ids:
                for restriction_feature in new_restriction_features:
                    rrr_source_relation_pair = (administrative_source_id, restriction_feature.attribute(self.names.T_ID_F))
                    rrr_source_relation_pairs.append(rrr_source_relation_pair)

            new_rrr_source_relation_features = list()
            if rrr_source_relation_pairs:
                for id_pair in rrr_source_relation_pairs:
                    if not id_pair in existing_source_pairs:
                        new_feature = QgsVectorLayerUtils().createFeature(layers[self.names.COL_RRR_SOURCE_T][LAYER])
                        new_feature.setAttribute(self.names.COL_RRR_SOURCE_T_SOURCE_F, id_pair[0])
                        new_feature.setAttribute(self.names.COL_RRR_SOURCE_T_OP_RESTRICTION_F, id_pair[1])
                        self.logger.info(__name__, "Saving Restriction-Source: {}-{}".format(id_pair[1], id_pair[0]))
                        new_rrr_source_relation_features.append(new_feature)

                layers[self.names.COL_RRR_SOURCE_T][LAYER].dataProvider().addFeatures(new_rrr_source_relation_features)
                self.logger.info_msg(__name__, QCoreApplication.translate("RightOfWay",
                    "{} out of {} records were saved into {}! {} out of {} records already existed in the database.").format(
                        len(new_rrr_source_relation_features),
                        len(rrr_source_relation_pairs),
                        self.names.COL_RRR_SOURCE_T,
                        len(rrr_source_relation_pairs) - len(new_rrr_source_relation_features),
                        len(rrr_source_relation_pairs)
                    ))
