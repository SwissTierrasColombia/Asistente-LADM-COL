# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2018-05-02
        git sha              : :%H$
        copyright            : (C) 2018 by Germán Carrillo (BSF Swissphoto)
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
import statistics

from qgis.core import (
    Qgis,
    QgsApplication,
    QgsProject,
    QgsGeometry,
    QgsPointXY,
    QgsVectorLayer,
    QgsField,
    QgsVectorLayerUtils,
    QgsMapLayerProxyModel,
    QgsFieldProxyModel,
)
from qgis.PyQt.QtCore import QVariant, QCoreApplication
from qgis.PyQt.QtWidgets import QDialog

import processing

from ..utils import get_ui_class

DIALOG_UI = get_ui_class('controlled_measurement_dialog.ui')
GROUP_ID = 'belongs_to_group' # If you change this, adjust the Group_Points as well

class ControlledMeasurementDialog(QDialog, DIALOG_UI):
    def __init__(self, qgis_utils):
        QDialog.__init__(self)
        self.setupUi(self)
        self.qgis_utils = qgis_utils

        self.mMapLayerComboBox.setFilters(QgsMapLayerProxyModel.PointLayer)
        self.mFieldComboBox.setFilters(QgsFieldProxyModel.String)

        self.accepted.connect(self.accept_dialog)
        self.buttonBox.helpRequested.connect(self.show_help)

        self.mMapLayerComboBox.layerChanged.connect(self.mFieldComboBox.setLayer)
        self.mFieldComboBox.setLayer(self.mMapLayerComboBox.currentLayer())

    def accept_dialog(self):
        input_layer = self.mMapLayerComboBox.currentLayer()
        tolerance = self.dsb_tolerance.value()
        definition_field = self.mFieldComboBox.currentField()

        if input_layer is None:
            self.qgis_utils.message_emitted.emit(
                QCoreApplication.translate("ControlledMeasurementDialog",
                                           "First select a point layer!"),
                Qgis.Warning)
            return

        if tolerance <= 0:
            self.qgis_utils.message_emitted.emit(
                QCoreApplication.translate("ControlledMeasurementDialog",
                                           "Set a tolerance greater than zero!"),
                Qgis.Warning)
            return

        res, msg = self.run_group_points_model(input_layer, tolerance, definition_field)
        if res is None:
            self.qgis_utils.message_emitted.emit(
            QCoreApplication.translate("ControlledMeasurementDialog", msg), Qgis.Warning)
            return

        # Create memory layer with average points
        groups = self.time_validate(res['native:mergevectorlayers_1:output'])
        if not(type(groups) == QgsVectorLayer and groups.isValid()):
            return

        idx = groups.fields().indexOf(GROUP_ID)

        group_ids = groups.uniqueValues(idx)

        # layer = QgsVectorLayer("Point?crs=EPSG:3116", "Average Points", "memory")
        layer = self.copy_attribs(groups, "Average Points")
        layer.dataProvider().addAttributes([
            QgsField("group_id", QVariant.Int),
            QgsField("count", QVariant.Int),
            QgsField("x_mean", QVariant.Double),
            QgsField("y_mean", QVariant.Double),
            QgsField("x_stdev", QVariant.Double),
            QgsField("y_stdev", QVariant.Double),
        ])
        layer.updateFields()
        new_features = []

        for group_id in group_ids:
            feature = [f for f in groups.getFeatures("\"{}\"={}".format(GROUP_ID, group_id))]
            try:
                trusty = feature[0].attributes()[groups.fields().indexFromName("trusty")]
            except:
                trusty = 'False'
            x_mean = 0
            y_mean = 0
            count = 0
            x_list = []
            y_list = []
            for feature in groups.getFeatures('"{}" = {}'.format(GROUP_ID, group_id)):
                current_point = feature.geometry().asPoint()
                x_list.append(current_point.x())
                y_list.append(current_point.y())

            if x_list and y_list != []:
                x_mean = statistics.mean(x_list)
                y_mean = statistics.mean(y_list)
                x_stdev = statistics.pstdev(x_list)
                y_stdev = statistics.pstdev(y_list)
            else:
                continue
            geom = QgsGeometry.fromPointXY(QgsPointXY(x_mean, y_mean))

            new_feature = QgsVectorLayerUtils.createFeature(layer, geom,
                {
                    16: trusty,
                    17: group_id,
                    18: len(x_list),
                    19: x_mean,
                    20: y_mean,
                    21: x_stdev,
                    22: y_stdev
                }
            )
            new_features.append(new_feature)

        layer.dataProvider().addFeatures(new_features)
        features = groups.getFeatures("\"{}\" IS NULL".format("belongs_to_group"))
        layer.dataProvider().addFeatures(features)
        layer.commitChanges()
        QgsProject.instance().addMapLayer(layer)

        self.qgis_utils.message_emitted.emit(
            QCoreApplication.translate("ControlledMeasurementDialog",
                                       "A new average point layer has been added to the map!"),
            Qgis.Info)

    def run_group_points_model(self, input_layer, tolerance, definition_field):
        # Run model
        model = QgsApplication.processingRegistry().algorithmById("model:Group_Points")
        if model:
            params = {
                '1_Inputpoints': input_layer.source(),
                '2_Typedefinition': definition_field,
                '3_Tolerance': tolerance,
                'native:multiparttosingleparts_2:output': 'memory:',
                'native:mergevectorlayers_1:output': 'memory:'
            }
            res = processing.run("model:Group_Points", params)
            msg = "Model Group_Points and execute OK!"
            return res, msg
        else:
            res = None
            msg = "Model Group_Points was not found and cannot be opened!"
            return res, msg

    def time_validate(self, input_features):
        groups_num = input_features.uniqueValues(input_features.fields().indexFromName("belongs_to_group"))

        new_layer = self.copy_attribs(input_features)
        time_layer = self.copy_attribs(input_features)
        time2_layer = self.copy_attribs(input_features)
        for i in groups_num:
            if i is None:
                new_layer.startEditing()
                features = input_features.getFeatures("\"{}\" IS NULL".format("belongs_to_group"))
                new_layer.dataProvider().addFeatures(features)
                [new_layer.changeAttributeValue(feat.id(), feat.fields().indexOf("trusty"), "False") for feat in
                 new_layer.getFeatures()]
                new_layer.commitChanges()
            else:
                features = input_features.getFeatures("\"{}\"={}".format("belongs_to_group", i))
                fg = len([f for f in features])
                if fg > 1:
                    # features = time_filter(features)
                    features = input_features.getFeatures("\"{}\"={}".format("belongs_to_group", i))
                    time_layer.startEditing()
                    time_layer.dataProvider().addFeatures(features)
                    [time_layer.changeAttributeValue(feat.id(), feat.fields().indexOf("trusty"), "True") for feat in
                     time_layer.getFeatures()]
                    time_layer.updateFields()
                else:
                    features = input_features.getFeatures("\"{}\"={}".format("belongs_to_group", i))
                    time2_layer.startEditing()
                    time2_layer.dataProvider().addFeatures(features)
                    [time2_layer.changeAttributeValue(feat.id(), feat.fields().indexOf("trusty"), "False") for feat in
                     time2_layer.getFeatures()]
                    time2_layer.updateFields()
                time_layer.commitChanges()
                time2_layer.commitChanges()

        new_layer.startEditing()
        new_layer.dataProvider().addFeatures(time_layer.getFeatures())
        new_layer.dataProvider().addFeatures(time2_layer.getFeatures())
        new_layer.commitChanges()
        QgsProject.instance().addMapLayer(new_layer)
        return new_layer

    def copy_attribs(self, sourceLYR, name="Previous Average Points"):
        destLYR = QgsVectorLayer("Point?crs=EPSG:3116", name, "memory")
        destLYR.startEditing()
        destLYR.dataProvider().addAttributes(sourceLYR.fields())
        destLYR.addAttribute(QgsField("trusty", QVariant.String))
        destLYR.updateFields()
        return destLYR

    def show_help(self):
        self.qgis_utils.show_help("controlled_measurement")
