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
from functools import partial

from qgis.PyQt.QtCore import (Qt,
                              QObject,
                              pyqtSignal,
                              QCoreApplication,
                              QSettings)

from qgis.core import (Qgis,
                       QgsApplication,
                       QgsExpression,
                       QgsFeatureRequest,
                       QgsProject,
                       QgsVectorLayer,
                       QgsEditFormConfig,
                       QgsProcessingFeatureSourceDefinition,
                       QgsWkbTypes,
                       QgsSnappingConfig,
                       QgsTolerance,
                       QgsVectorLayerUtils)

import processing

from ..config.table_mapping_config import (ADMINISTRATIVE_SOURCE_TABLE,
                                           COL_RESTRICTION_TYPE_RIGHT_OF_WAY_VALUE,
                                           ID_FIELD,
                                           PARCEL_TABLE,
                                           PLOT_TABLE,
                                           RESTRICTION_TABLE_PARCEL_FIELD,
                                           UEBAUNIT_TABLE,
                                           UEBAUNIT_TABLE_PARCEL_FIELD,
                                           UEBAUNIT_TABLE_RIGHT_OF_WAY_FIELD,
                                           RESTRICTION_TABLE_DESCRIPTION_FIELD,
                                           RESTRICTION_TABLE,
                                           RIGHT_OF_WAY_TABLE,
                                           RIGHT_OF_WAY_TABLE_IDENTIFICATOR_FIELD,
                                           RRR_SOURCE_RELATION_TABLE,
                                           RRR_SOURCE_RESTRICTION_FIELD,
                                           RRR_SOURCE_SOURCE_FIELD,
                                           SURVEY_POINT_TABLE,
                                           TYPE_FIELD,
                                           UEBAUNIT_TABLE_PLOT_FIELD)

from ..config.general_config import (DEFAULT_EPSG,
                                     PLUGIN_NAME,
                                     TranslatableConfigStrings)


class RightOfWay(QObject):

    def __init__(self, iface, qgis_utils):
        QObject.__init__(self)
        self.qgis_utils = qgis_utils
        self.iface = iface
        self.log = QgsApplication.messageLog()

        self._right_of_way_layer = None
        self._right_of_way_line_layer = None
        self.addedFeatures = None

    def prepare_right_of_way_creation(self, db, iface):
        # Load layers
        self.add_db_required_layers(db, iface)

        # Disable transactions groups and configure Snapping
        self.set_layers_settings()

        # Don't suppress feature form
        form_config = self._right_of_way_layer.editFormConfig()
        form_config.setSuppress(QgsEditFormConfig.SuppressOff)
        self._right_of_way_layer.setEditFormConfig(form_config)

        # Enable edition mode
        iface.layerTreeView().setCurrentLayer(self._right_of_way_layer)
        self._right_of_way_layer.startEditing()
        iface.actionAddFeature().trigger()

        iface.messageBar().pushMessage('Asistente LADM_COL',
            QCoreApplication.translate("CreateRightOfWayCadastreWizard",
                                       "You can now start capturing right of ways digitizing on the map..."),
            Qgis.Info)

    def prepare_right_of_way_line_creation(self, db, translatable_config_strings, iface, width_value):
        # Load layers
        self.add_db_required_layers(db, iface)
        # Add Memory line layer
        self._right_of_way_line_layer = QgsVectorLayer("MultiLineString?crs=EPSG:{}".format(DEFAULT_EPSG),
                                                       translatable_config_strings.RIGHT_OF_WAY_LINE_LAYER, "memory")
        QgsProject.instance().addMapLayer(self._right_of_way_line_layer, True)

        # Disable transactions groups and configure Snapping
        self.set_layers_settings()

        # Suppress feature form
        form_config = self._right_of_way_line_layer.editFormConfig()
        form_config.setSuppress(QgsEditFormConfig.SuppressOn)
        self._right_of_way_line_layer.setEditFormConfig(form_config)

        # Enable edition mode
        iface.layerTreeView().setCurrentLayer(self._right_of_way_line_layer)
        self._right_of_way_line_layer.startEditing()
        iface.actionAddFeature().trigger()

        self._right_of_way_line_layer.featureAdded.connect(self.store_features_ids)
        self._right_of_way_line_layer.editCommandEnded.connect(self.update_attributes_after_adding)
        self._right_of_way_line_layer.committedFeaturesAdded.connect(partial(self.finish_right_of_way_line, width_value, iface))

        iface.messageBar().pushMessage('Asistente LADM_COL',
            QCoreApplication.translate("CreateRightOfWayCadastreWizard",
                                       "You can now start capturing right of way lines digitizing on the map..."),
            Qgis.Info)

    def set_layers_settings(self):
        # Disable transactions groups
        QgsProject.instance().setAutoTransaction(False)

        # Configure Snapping
        snapping = QgsProject.instance().snappingConfig()
        snapping.setEnabled(True)
        snapping.setMode(QgsSnappingConfig.AllLayers)
        snapping.setType(QgsSnappingConfig.Vertex)
        snapping.setUnits(QgsTolerance.Pixels)
        snapping.setTolerance(9)
        QgsProject.instance().setSnappingConfig(snapping)

    def add_db_required_layers(self, db, iface):
        # Load layers
        res_layers = self.qgis_utils.get_layers(db, {
            PLOT_TABLE: {'name': PLOT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry},
            RIGHT_OF_WAY_TABLE: {'name': RIGHT_OF_WAY_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry},
            SURVEY_POINT_TABLE: {'name': SURVEY_POINT_TABLE, 'geometry': None}
        }, load=True)

        self._plot_layer = res_layers[PLOT_TABLE]
        self._right_of_way_layer = res_layers[RIGHT_OF_WAY_TABLE]
        self._survey_point_layer = res_layers[SURVEY_POINT_TABLE]

        if self._plot_layer is None:
            iface.messageBar().pushMessage('Asistente LADM_COL',
                QCoreApplication.translate("CreateRightOfWayCadastreWizard",
                                           "Plot layer couldn't be found... {}").format(db.get_description()),
                Qgis.Warning)
            return

        if self._right_of_way_layer is None:
            iface.messageBar().pushMessage('Asistente LADM_COL',
                QCoreApplication.translate("CreateRightOfWayCadastreWizard",
                                           "Right of Way layer couldn't be found... {}").format(db.get_description()),
                Qgis.Warning)
            return

        if self._survey_point_layer is None:
            iface.messageBar().pushMessage('Asistente LADM_COL',
                QCoreApplication.translate("CreateRightOfWayCadastreWizard",
                                           "Survey Point layer couldn't be found... {}").format(db.get_description()),
                Qgis.Warning)
            return

        form_config = self._right_of_way_layer.editFormConfig()
        form_config.setSuppress(QgsEditFormConfig.SuppressOff)
        self._right_of_way_layer.setEditFormConfig(form_config)

    def store_features_ids(self, featId):
         """
         This method only stores featIds in a class variable. It's required to avoid a bug with SLOTS connected to
         featureAdded.
         """
         self.addedFeatures = featId

    def update_attributes_after_adding(self):
        layer = self.sender() # Get the layer that has sent the signal
        layer.featureAdded.disconnect(self.store_features_ids)
        self.log.logMessage("RigthOfWayLine's featureAdded SIGNAL disconnected", PLUGIN_NAME, Qgis.Info)
        res = layer.commitChanges()
        QgsProject.instance().removeMapLayer(layer)
        self.addedFeatures = None

    def finish_right_of_way_line(self, width_value, iface):
        self._right_of_way_line_layer.committedFeaturesAdded.disconnect()
        self.log.logMessage("RigthOfWayLine's committedFeaturesAdded SIGNAL disconnected", PLUGIN_NAME, Qgis.Info)

        params = {'INPUT':self._right_of_way_line_layer,
                  'DISTANCE':width_value,
                  'SEGMENTS':5,
                  'END_CAP_STYLE':1, # Flat
                  'JOIN_STYLE':2,
                  'MITER_LIMIT':2,
                  'DISSOLVE':False,
                  'OUTPUT':'memory:'}
        buffered_right_of_way_layer = processing.run("native:buffer", params)['OUTPUT']

        buffer_geometry = buffered_right_of_way_layer.getFeature(1).geometry()
        feature = QgsVectorLayerUtils().createFeature(self._right_of_way_layer, buffer_geometry)

        if feature:
            self._right_of_way_layer.startEditing()
            self._right_of_way_layer.addFeature(feature)
            form = iface.getFeatureForm(self._right_of_way_layer, feature)
            form.show()

    def fill_right_of_way_relations(self, db):
        # Load layers
        res_layers = self.qgis_utils.get_layers(db, {
            ADMINISTRATIVE_SOURCE_TABLE: {'name': ADMINISTRATIVE_SOURCE_TABLE, 'geometry': None},
            PARCEL_TABLE: {'name': PARCEL_TABLE, 'geometry': None},
            PLOT_TABLE: {'name': PLOT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry},
            RESTRICTION_TABLE: {'name': RESTRICTION_TABLE, 'geometry': None},
            RIGHT_OF_WAY_TABLE: {'name': RIGHT_OF_WAY_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry},
            RRR_SOURCE_RELATION_TABLE: {'name': RRR_SOURCE_RELATION_TABLE, 'geometry': None},
            SURVEY_POINT_TABLE: {'name': SURVEY_POINT_TABLE, 'geometry': None},
            UEBAUNIT_TABLE: {'name': UEBAUNIT_TABLE, 'geometry': None}
        }, load=True)

        self._administrative_source_layer = res_layers[ADMINISTRATIVE_SOURCE_TABLE]
        self._parcel_layer = res_layers[PARCEL_TABLE]
        self._plot_layer = res_layers[PLOT_TABLE]
        self._restriction_layer = res_layers[RESTRICTION_TABLE]
        self._right_of_way_layer = res_layers[RIGHT_OF_WAY_TABLE]
        self._survey_point_layer = res_layers[SURVEY_POINT_TABLE]
        self._rrr_source_relation_layer = res_layers[RRR_SOURCE_RELATION_TABLE]
        self._uebaunit_table = res_layers[UEBAUNIT_TABLE]

        if self._parcel_layer is None:
            self.qgis_utils.message_emitted.emit(
                QCoreApplication.translate("RightOfWay", "Table {} not found in the DB! {}").format(PARCEL_TABLE, db.get_description()),
                Qgis.Warning)
            return

        if self._right_of_way_layer is None:
            self.qgis_utils.message_emitted.emit(
                QCoreApplication.translate("RightOfWay", "Table {} not found in the DB! {}").format(RIGHT_OF_WAY_TABLE, db.get_description()),
                Qgis.Warning)
            return

        if self._uebaunit_table is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                QCoreApplication.translate("RightOfWay",
                                           "UEBAUNIT table couldn't be found... {}").format(self._db.get_description()),
                Qgis.Warning)
            return

        if self._plot_layer.selectedFeatureCount() == 0 or self._right_of_way_layer.selectedFeatureCount() == 0 or self._administrative_source_layer.selectedFeatureCount() == 0:
            if self.qgis_utils.get_layer_from_layer_tree(db, PLOT_TABLE, geometry_type=QgsWkbTypes.PolygonGeometry) is None:
                self.qgis_utils.message_with_button_load_layer_emitted.emit(
                    QCoreApplication.translate("RightOfWay",
                                               "First load the layer {} into QGIS and select at least one plot!").format(PLOT_TABLE),
                    QCoreApplication.translate("RightOfWay", "Load layer {} now").format(PLOT_TABLE),
                    [PLOT_TABLE, None],
                    Qgis.Warning)
            else:
                self.qgis_utils.message_emitted.emit(
                    QCoreApplication.translate("RightOfWay", "Select at least one benefited plot, one right of way and at least one administrative source to create relations!"),
                    Qgis.Warning)
                return
        else:
            ue_baunit_features = self._uebaunit_table.getFeatures()
            # Get unique pairs id_right_of_way-id_parcel
            existing_pairs = [(ue_baunit_feature[UEBAUNIT_TABLE_PARCEL_FIELD], ue_baunit_feature[UEBAUNIT_TABLE_RIGHT_OF_WAY_FIELD]) for ue_baunit_feature in ue_baunit_features]
            existing_pairs = set(existing_pairs)

            plot_ids = [f[ID_FIELD] for f in self._plot_layer.selectedFeatures()]

            right_of_way_id = self._right_of_way_layer.selectedFeatures()[0].attribute(ID_FIELD)
            id_pairs = list()
            for plot in plot_ids:
                exp = "\"{uebaunit}\" = {plot}".format(uebaunit=UEBAUNIT_TABLE_PLOT_FIELD, plot=plot)
                parcels = self._uebaunit_table.getFeatures(exp)
                for parcel in parcels:
                    id_pair = (parcel.attribute(UEBAUNIT_TABLE_PARCEL_FIELD), right_of_way_id)
                    id_pairs.append(id_pair)

            if len(id_pairs) < len(plot_ids):
                # If any relationship plot-parcel is not found, we don't need to continue
                self.qgis_utils.message_emitted.emit(
                    QCoreApplication.translate("RightOfWay", "One or more pairs id_plot-id_parcel weren't found, this is needed to create benefited and restriction relations."),
                    Qgis.Warning)
                return

            if id_pairs:
                new_features = list()
                for id_pair in id_pairs:
                    if not id_pair in existing_pairs:
                        #Create feature
                        new_feature = QgsVectorLayerUtils().createFeature(self._uebaunit_table)
                        new_feature.setAttribute(UEBAUNIT_TABLE_PARCEL_FIELD, id_pair[0])
                        new_feature.setAttribute(UEBAUNIT_TABLE_RIGHT_OF_WAY_FIELD, id_pair[1])
                        self.log.logMessage("Saving RightOfWay-Parcel: {}-{}".format(id_pair[1], id_pair[0]), PLUGIN_NAME, Qgis.Info)
                        new_features.append(new_feature)

                self._uebaunit_table.dataProvider().addFeatures(new_features)
                self.qgis_utils.message_emitted.emit(
                    QCoreApplication.translate("RightOfWay",
                                       "{} out of {} records were saved into {}! {} out of {} records already existed in the database.").format(
                        len(new_features),
                        len(id_pairs),
                        UEBAUNIT_TABLE,
                        len(id_pairs) - len(new_features),
                        len(id_pairs)
                        ),
                        Qgis.Info)

            spatial_join_layer = processing.run("qgis:joinattributesbylocation",
                                                {
                                                    'INPUT': self._plot_layer,
                                                    'JOIN': QgsProcessingFeatureSourceDefinition(self._right_of_way_layer.id(), True),
                                                    'PREDICATE': [0],
                                                    'JOIN_FIELDS': [ID_FIELD, RIGHT_OF_WAY_TABLE_IDENTIFICATOR_FIELD],
                                                    'METHOD': 0,
                                                    'DISCARD_NONMATCHING': True,
                                                    'PREFIX': '',
                                                    'OUTPUT': 'memory:'})['OUTPUT']

            restriction_features = self._restriction_layer.getFeatures()

            existing_restriction_pairs = [(restriction_feature[RESTRICTION_TABLE_PARCEL_FIELD], restriction_feature[RESTRICTION_TABLE_DESCRIPTION_FIELD]) for restriction_feature in restriction_features]
            existing_restriction_pairs = set(existing_restriction_pairs)
            id_pairs_restriction = list()
            plot_ids = spatial_join_layer.getFeatures()

            for plot in plot_ids:
                exp = "\"uebaunit\" = {plot}".format(uebaunit=UEBAUNIT_TABLE_PLOT_FIELD, plot=plot.attribute(ID_FIELD))
                parcels = self._uebaunit_table.getFeatures(exp)
                for parcel in parcels:
                    id_pair_restriction = (parcel.attribute(UEBAUNIT_TABLE_PARCEL_FIELD), "Asociada a la servidumbre {}".format(plot.attribute(RIGHT_OF_WAY_TABLE_IDENTIFICATOR_FIELD)))
                    id_pairs_restriction.append(id_pair_restriction)

            new_restriction_features = list()
            if id_pairs_restriction:
                for id_pair in id_pairs_restriction:
                    if not id_pair in existing_restriction_pairs:
                        #Create feature
                        new_feature = QgsVectorLayerUtils().createFeature(self._restriction_layer)
                        new_feature.setAttribute(RESTRICTION_TABLE_PARCEL_FIELD, id_pair[0])
                        new_feature.setAttribute(RESTRICTION_TABLE_DESCRIPTION_FIELD, id_pair[1])
                        new_feature.setAttribute(TYPE_FIELD, COL_RESTRICTION_TYPE_RIGHT_OF_WAY_VALUE)
                        self.log.logMessage("Saving RightOfWay-Parcel: {}-{}".format(id_pair[1], id_pair[0]), PLUGIN_NAME, Qgis.Info)
                        new_restriction_features.append(new_feature)

                self._restriction_layer.dataProvider().addFeatures(new_restriction_features)
                self.qgis_utils.message_emitted.emit(
                    QCoreApplication.translate("RightOfWay",
                                       "{} out of {} records were saved into {}! {} out of {} records already existed in the database.").format(
                        len(new_restriction_features),
                        len(id_pairs_restriction),
                        RESTRICTION_TABLE,
                        len(id_pairs_restriction) - len(new_restriction_features),
                        len(id_pairs_restriction)
                        ),
                        Qgis.Info)

            administrative_source_ids = [f[ID_FIELD] for f in self._administrative_source_layer.selectedFeatures()]

            source_relation_features = self._rrr_source_relation_layer.getFeatures()

            existing_source_pairs = [(source_relation_feature[RRR_SOURCE_SOURCE_FIELD], source_relation_feature[RRR_SOURCE_RESTRICTION_FIELD]) for source_relation_feature in source_relation_features]
            existing_source_pairs = set(existing_source_pairs)

            rrr_source_relation_pairs = list()

            for administrative_source_id in administrative_source_ids:
                for restriction_feature in new_restriction_features:
                    rrr_source_relation_pair = (administrative_source_id, restriction_feature.attribute(ID_FIELD))
                    rrr_source_relation_pairs.append(rrr_source_relation_pair)

            new_rrr_source_relation_features = list()
            if rrr_source_relation_pairs:
                for id_pair in rrr_source_relation_pairs:
                    if not id_pair in existing_source_pairs:
                        new_feature = QgsVectorLayerUtils().createFeature(self._rrr_source_relation_layer)
                        new_feature.setAttribute(RRR_SOURCE_SOURCE_FIELD, id_pair[0])
                        new_feature.setAttribute(RRR_SOURCE_RESTRICTION_FIELD, id_pair[1])
                        self.log.logMessage("Saving Restriction-Source: {}-{}".format(id_pair[1], id_pair[0]), PLUGIN_NAME, Qgis.Info)
                        new_rrr_source_relation_features.append(new_feature)

                self._rrr_source_relation_layer.dataProvider().addFeatures(new_rrr_source_relation_features)
                self.qgis_utils.message_emitted.emit(
                    QCoreApplication.translate("RightOfWay",
                                       "{} out of {} records were saved into {}! {} out of {} records already existed in the database.").format(
                        len(new_rrr_source_relation_features),
                        len(rrr_source_relation_pairs),
                        RRR_SOURCE_RELATION_TABLE,
                        len(rrr_source_relation_pairs) - len(new_rrr_source_relation_features),
                        len(rrr_source_relation_pairs)
                        ),
                        Qgis.Info)
