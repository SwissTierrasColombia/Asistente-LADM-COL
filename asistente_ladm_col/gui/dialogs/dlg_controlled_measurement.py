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

from qgis.PyQt.QtCore import (QVariant,
                              QCoreApplication)
from qgis.PyQt.QtWidgets import QDialog
from qgis.core import (Qgis,
                       QgsApplication,
                       QgsProject,
                       QgsGeometry,
                       QgsPointXY,
                       QgsVectorLayer,
                       QgsField,
                       QgsVectorLayerUtils,
                       QgsMapLayerProxyModel)

import processing
from ...utils import get_ui_class

DIALOG_UI = get_ui_class('dialogs/dlg_controlled_measurement.ui')
GROUP_ID = 'AUTO' # If you change this, adjust the Group_Points as well


class ControlledMeasurementDialog(QDialog, DIALOG_UI):
    def __init__(self, qgis_utils):
        QDialog.__init__(self)
        self.setupUi(self)
        self.qgis_utils = qgis_utils

        self.mMapLayerComboBox.setFilters(QgsMapLayerProxyModel.PointLayer)

        self.accepted.connect(self.accept_dialog)
        self.buttonBox.helpRequested.connect(self.show_help)

    def accept_dialog(self):
        input_layer = self.mMapLayerComboBox.currentLayer()
        tolerance = self.dsb_tolerance.value()

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

        # Run model
        model = QgsApplication.processingRegistry().algorithmById("model:Group_Points")
        if model:
            params = {
                'inputpoints': input_layer.name(),
                'bufferdistance': tolerance,
                'native:multiparttosingleparts_2:output': 'memory:'
            }
            res = processing.run("model:Group_Points", params)
        else:
            self.qgis_utils.message_emitted.emit(
                QCoreApplication.translate("ControlledMeasurementDialog",
                                           "Model Group_Points was not found and cannot be opened!"),
                Qgis.Warning)

        # Create memory layer with average points
        groups = res['native:multiparttosingleparts_2:output']
        if not(type(groups) == QgsVectorLayer and groups.isValid()):
            return

        idx = groups.fields().indexOf(GROUP_ID)
        group_ids = groups.uniqueValues(idx)

        layer = QgsVectorLayer("Point?crs={}".format(input_layer.sourceCrs().authid()), "Average Points", "memory")
        layer.dataProvider().addAttributes([
            QgsField("group_id", QVariant.Int),
            QgsField("count", QVariant.Int),
            QgsField("x_mean", QVariant.Double),
            QgsField("y_mean", QVariant.Double),
            QgsField("x_stdev", QVariant.Double),
            QgsField("y_stdev", QVariant.Double)
        ])
        layer.updateFields()
        new_features = []

        for group_id in group_ids:
            x_mean = 0
            y_mean = 0
            count = 0
            x_list = []
            y_list = []
            for feature in groups.getFeatures('"{}" = {}'.format(GROUP_ID, group_id)):
                current_point = feature.geometry().asPoint()
                x_list.append(current_point.x())
                y_list.append(current_point.y())

            x_mean = statistics.mean(x_list)
            y_mean = statistics.mean(y_list)
            x_stdev = statistics.pstdev(x_list)
            y_stdev = statistics.pstdev(y_list)
            geom = QgsGeometry.fromPointXY(QgsPointXY(x_mean, y_mean))

            new_feature = QgsVectorLayerUtils.createFeature(layer, geom,
                {
                    0: group_id,
                    1: len(x_list),
                    2: x_mean,
                    3: y_mean,
                    4: x_stdev,
                    5: y_stdev
                }
            )
            new_features.append(new_feature)

        layer.dataProvider().addFeatures(new_features)
        QgsProject.instance().addMapLayer(layer)

        self.qgis_utils.message_emitted.emit(
            QCoreApplication.translate("ControlledMeasurementDialog",
                                       "A new average point layer has been added to the map!"),
            Qgis.Info)

    def show_help(self):
        self.qgis_utils.show_help("controlled_measurement")
