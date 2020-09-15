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
                       QgsVectorLayerUtils)

import processing

from asistente_ladm_col.config.enums import EnumLayerRegistryType
from asistente_ladm_col.config.ladm_names import LADMNames
from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.lib.logger import Logger


class RightOfWay(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.logger = Logger()
        self.app = AppInterface()

        self._right_of_way_line_layer = None
        self.addedFeatures = None

    def fill_right_of_way_relations(self, db):
        layers = {
            db.names.LC_ADMINISTRATIVE_SOURCE_T: None,
            db.names.LC_PARCEL_T: None,
            db.names.LC_PLOT_T: None,
            db.names.LC_RESTRICTION_T: None,
            db.names.LC_RESTRICTION_TYPE_D: None,
            db.names.LC_RIGHT_OF_WAY_T: None,
            db.names.COL_RRR_SOURCE_T: None,
            db.names.LC_SURVEY_POINT_T: None,
            db.names.COL_UE_BAUNIT_T: None
        }

        # Load layers
        self.app.core.get_layers(db, layers, load=True)
        if not layers:
            return None

        exp = "\"{}\" = '{}'".format(db.names.ILICODE_F, LADMNames.RESTRICTION_TYPE_D_RIGHT_OF_WAY_ILICODE_VALUE)
        restriction_right_of_way_t_id = [feature for feature in layers[db.names.LC_RESTRICTION_TYPE_D].getFeatures(exp)][0][db.names.T_ID_F]

        if layers[db.names.LC_PLOT_T].selectedFeatureCount() == 0 or layers[db.names.LC_RIGHT_OF_WAY_T].selectedFeatureCount() == 0 or layers[db.names.LC_ADMINISTRATIVE_SOURCE_T].selectedFeatureCount() == 0:
            if self.app.core.get_ladm_layer_from_qgis(db, db.names.LC_PLOT_T, EnumLayerRegistryType.IN_CANVAS) is None:
                self.logger.message_with_button_load_layer_emitted.emit(
                    QCoreApplication.translate("RightOfWay",
                                               "First load the layer {} into QGIS and select at least one plot!").format(db.names.LC_PLOT_T),
                    QCoreApplication.translate("RightOfWay", "Load layer {} now").format(db.names.LC_PLOT_T),
                    db.names.LC_PLOT_T,
                    Qgis.Warning)
            else:
                self.logger.warning_msg(__name__, QCoreApplication.translate("RightOfWay",
                    "Select at least one benefited plot, one right of way and at least one administrative source to create relations!"))
                return
        else:
            ue_baunit_features = layers[db.names.COL_UE_BAUNIT_T].getFeatures()
            # Get unique pairs id_right_of_way-id_parcel
            existing_pairs = [(ue_baunit_feature[db.names.COL_UE_BAUNIT_T_PARCEL_F], ue_baunit_feature[db.names.COL_UE_BAUNIT_T_LC_RIGHT_OF_WAY_F]) for ue_baunit_feature in ue_baunit_features]
            existing_pairs = set(existing_pairs)

            plot_ids = [f[db.names.T_ID_F] for f in layers[db.names.LC_PLOT_T].selectedFeatures()]

            right_of_way_id = layers[db.names.LC_RIGHT_OF_WAY_T].selectedFeatures()[0].attribute(db.names.T_ID_F)
            id_pairs = list()
            for plot in plot_ids:
                exp = "\"{uebaunit}\" = {plot}".format(uebaunit=db.names.COL_UE_BAUNIT_T_LC_PLOT_F, plot=plot)
                parcels = layers[db.names.COL_UE_BAUNIT_T].getFeatures(exp)
                for parcel in parcels:
                    id_pair = (parcel.attribute(db.names.COL_UE_BAUNIT_T_PARCEL_F), right_of_way_id)
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
                        new_feature = QgsVectorLayerUtils().createFeature(layers[db.names.COL_UE_BAUNIT_T])
                        new_feature.setAttribute(db.names.COL_UE_BAUNIT_T_PARCEL_F, id_pair[0])
                        new_feature.setAttribute(db.names.COL_UE_BAUNIT_T_LC_RIGHT_OF_WAY_F, id_pair[1])
                        self.logger.info(__name__, "Saving RightOfWay-Parcel: {}-{}".format(id_pair[1], id_pair[0]))
                        new_features.append(new_feature)

                layers[db.names.COL_UE_BAUNIT_T].dataProvider().addFeatures(new_features)
                self.logger.info_msg(__name__, QCoreApplication.translate("RightOfWay",
                    "{} out of {} records were saved into {}! {} out of {} records already existed in the database.").format(
                        len(new_features),
                        len(id_pairs),
                        db.names.COL_UE_BAUNIT_T,
                        len(id_pairs) - len(new_features),
                        len(id_pairs)
                    ))

            spatial_join_layer = processing.run("qgis:joinattributesbylocation",
                                                {
                                                    'INPUT': layers[db.names.LC_PLOT_T],
                                                    'JOIN': QgsProcessingFeatureSourceDefinition(layers[db.names.LC_RIGHT_OF_WAY_T].id(), True),
                                                    'PREDICATE': [0],
                                                    'JOIN_FIELDS': [db.names.T_ID_F],
                                                    'METHOD': 0,
                                                    'DISCARD_NONMATCHING': True,
                                                    'PREFIX': '',
                                                    'OUTPUT': 'memory:'})['OUTPUT']

            restriction_features = layers[db.names.LC_RESTRICTION_T].getFeatures()
            existing_restriction_pairs = [(restriction_feature[db.names.COL_BAUNIT_RRR_T_UNIT_F], restriction_feature[db.names.COL_RRR_T_DESCRIPTION_F]) for restriction_feature in restriction_features]
            existing_restriction_pairs = set(existing_restriction_pairs)
            id_pairs_restriction = list()
            plot_ids = spatial_join_layer.getFeatures()

            for plot in plot_ids:
                exp = "\"uebaunit\" = {plot}".format(uebaunit=db.names.COL_UE_BAUNIT_T_LC_PLOT_F, plot=plot.attribute(db.names.T_ID_F))
                parcels = layers[db.names.COL_UE_BAUNIT_T].getFeatures(exp)
                for parcel in parcels:
                    id_pair_restriction = (parcel.attribute(db.names.COL_UE_BAUNIT_T_PARCEL_F), QCoreApplication.translate("RightOfWay", "Right of way"))
                    id_pairs_restriction.append(id_pair_restriction)

            new_restriction_features = list()
            if id_pairs_restriction:
                for id_pair in id_pairs_restriction:
                    if not id_pair in existing_restriction_pairs:
                        #Create feature
                        new_feature = QgsVectorLayerUtils().createFeature(layers[db.names.LC_RESTRICTION_T])
                        new_feature.setAttribute(db.names.COL_BAUNIT_RRR_T_UNIT_F, id_pair[0])
                        new_feature.setAttribute(db.names.COL_RRR_T_DESCRIPTION_F, id_pair[1])
                        new_feature.setAttribute(db.names.LC_RESTRICTION_T_TYPE_F, restriction_right_of_way_t_id)
                        self.logger.info(__name__, "Saving RightOfWay-Parcel: {}-{}".format(id_pair[1], id_pair[0]))
                        new_restriction_features.append(new_feature)

                layers[db.names.LC_RESTRICTION_T].dataProvider().addFeatures(new_restriction_features)
                self.logger.info_msg(__name__, QCoreApplication.translate("RightOfWay",
                    "{} out of {} records were saved into {}! {} out of {} records already existed in the database.").format(
                        len(new_restriction_features),
                        len(id_pairs_restriction),
                        db.names.LC_RESTRICTION_T,
                        len(id_pairs_restriction) - len(new_restriction_features),
                        len(id_pairs_restriction)
                    ))

            administrative_source_ids = [f[db.names.T_ID_F] for f in layers[db.names.LC_ADMINISTRATIVE_SOURCE_T].selectedFeatures()]

            source_relation_features = layers[db.names.COL_RRR_SOURCE_T].getFeatures()

            existing_source_pairs = [(source_relation_feature[db.names.COL_RRR_SOURCE_T_SOURCE_F], source_relation_feature[db.names.COL_RRR_SOURCE_T_LC_RESTRICTION_F]) for source_relation_feature in source_relation_features]
            existing_source_pairs = set(existing_source_pairs)

            rrr_source_relation_pairs = list()

            for administrative_source_id in administrative_source_ids:
                for restriction_feature in new_restriction_features:
                    rrr_source_relation_pair = (administrative_source_id, restriction_feature.attribute(db.names.T_ID_F))
                    rrr_source_relation_pairs.append(rrr_source_relation_pair)

            new_rrr_source_relation_features = list()
            if rrr_source_relation_pairs:
                for id_pair in rrr_source_relation_pairs:
                    if not id_pair in existing_source_pairs:
                        new_feature = QgsVectorLayerUtils().createFeature(layers[db.names.COL_RRR_SOURCE_T])
                        new_feature.setAttribute(db.names.COL_RRR_SOURCE_T_SOURCE_F, id_pair[0])
                        new_feature.setAttribute(db.names.COL_RRR_SOURCE_T_LC_RESTRICTION_F, id_pair[1])
                        self.logger.info(__name__, "Saving Restriction-Source: {}-{}".format(id_pair[1], id_pair[0]))
                        new_rrr_source_relation_features.append(new_feature)

                layers[db.names.COL_RRR_SOURCE_T].dataProvider().addFeatures(new_rrr_source_relation_features)
                self.logger.info_msg(__name__, QCoreApplication.translate("RightOfWay",
                    "{} out of {} records were saved into {}! {} out of {} records already existed in the database.").format(
                        len(new_rrr_source_relation_features),
                        len(rrr_source_relation_pairs),
                        db.names.COL_RRR_SOURCE_T,
                        len(rrr_source_relation_pairs) - len(new_rrr_source_relation_features),
                        len(rrr_source_relation_pairs)
                    ))
