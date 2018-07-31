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
    QgsFeatureRequest,
    NULL
)
from qgis.PyQt.QtCore import QVariant, QCoreApplication
from qgis.PyQt.QtWidgets import QDialog

import processing

from ..config.general_config import (
    DEFAULT_EPSG,
    TRUSTWORTHY_FIELD_NAME,
    GROUP_FIELD_NAME
)
from ..utils import get_ui_class

DIALOG_UI = get_ui_class('controlled_measurement_dialog.ui')

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
        self.mMapLayerComboBox.layerChanged.connect(self.tFieldComboBox.setLayer)
        self.mMapLayerComboBox.layerChanged.connect(self.pnFieldComboBox.setLayer)

        self.mFieldComboBox.setLayer(self.mMapLayerComboBox.currentLayer())
        self.tFieldComboBox.setLayer(self.mMapLayerComboBox.currentLayer())
        self.pnFieldComboBox.setLayer(self.mMapLayerComboBox.currentLayer())

    def accept_dialog(self):
        input_layer = self.mMapLayerComboBox.currentLayer()
        tolerance = self.dsb_tolerance.value()
        definition_field = self.mFieldComboBox.currentField()
        time_tolerance = self.time_tolerance.value()
        time_field = self.tFieldComboBox.currentField()
        point_name = self.pnFieldComboBox.currentField()

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

        layer_with_groups = res['native:mergevectorlayers_1:output']

        # Add trustworthy field and fill it
        layer_with_groups.dataProvider().addAttributes([QgsField(TRUSTWORTHY_FIELD_NAME, QVariant.String)])
        layer_with_groups.updateFields()
        layer_with_trustworthy = self.validate_trustworthy(layer_with_groups, time_tolerance, time_field)

        QgsProject.instance().addMapLayer(layer_with_trustworthy)
        self.average_per_group(layer_with_trustworthy, point_name)

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
        else:
            res = None
            msg = "Model Group_Points was not found and cannot be opened!"

        return res, msg

    def validate_trustworthy(self, layer, time_tolerance, time_field):
        """
        This function goes through the groups obtained from the model and
        updates the trustworthy field called trustworthy as the case may be
        (True or False), also if True uses the auxiliary function time_filter
        to determine the records that are not within the allowed time range.
        """

        groups_num = layer.uniqueValues(layer.fields().indexFromName(GROUP_FIELD_NAME))
        idx_time_field = layer.fields().indexFromName(time_field)
        new_layer = self.copy_attribs(layer, "Previous Average Points")

        for group in groups_num:
            if group is None:
                not_group_features = [f for f in layer.getFeatures("\"{}\" IS NULL".format(GROUP_FIELD_NAME))]
                for feature in not_group_features:
                    feature.setAttribute(TRUSTWORTHY_FIELD_NAME, "False")

                new_layer.dataProvider().addFeatures(not_group_features)
            else:
                if time_field:
                    independent_features, dependent_features = self.time_filter(
                        layer=layer,
                        features=layer.getFeatures("\"{}\"={}".format(GROUP_FIELD_NAME, group)),
                        idx=idx_time_field,
                        time_tolerance=time_tolerance)

                    independent_features = [f for f in independent_features]
                    dependent_features = [f for f in dependent_features]
                else:
                    independent_features = [f for f in layer.getFeatures("\"{}\"={}".format(GROUP_FIELD_NAME, group))]
                    dependent_features = []

                if len(independent_features) > 1:
                    for feature in independent_features:
                        feature.setAttribute(TRUSTWORTHY_FIELD_NAME, "True")

                    for feature in dependent_features:
                        feature.setAttribute(TRUSTWORTHY_FIELD_NAME, "False")

                    new_layer.dataProvider().addFeatures(independent_features)
                    new_layer.dataProvider().addFeatures(dependent_features)
                else:
                    for feature in independent_features:
                        feature.setAttribute(TRUSTWORTHY_FIELD_NAME, "False")
                        feature.setAttribute(GROUP_FIELD_NAME, NULL)

                    for feature in dependent_features:
                        feature.setAttribute(TRUSTWORTHY_FIELD_NAME, "False")

                    new_layer.dataProvider().addFeatures(independent_features)
                    new_layer.dataProvider().addFeatures(dependent_features)

        return new_layer

    def copy_attribs(self, layer, name):
        destLYR = QgsVectorLayer("Point?crs=EPSG:{}".format(DEFAULT_EPSG), name, "memory")
        destLYR.dataProvider().addAttributes(layer.fields())
        destLYR.updateFields()
        return destLYR

    def time_filter(self, layer, features, idx, time_tolerance):
        """ Filters a time field and returns which features are within the
        allowed time range and which are not."""
        dates = {}
        for feat in features:
            attrs = feat.attributes()
            dates[feat.id()] = attrs[idx]
        ids = {}
        pivot = 0
        ids[list(dates.keys())[list(dates.values()).index(sorted(dates.values())[0])]] = sorted(dates.values())[0]
        for i in range(0, len(sorted(dates.values()))):
            if abs(sorted(dates.values())[pivot].secsTo(sorted(dates.values())[i]) / 60) > time_tolerance:
                ids[list(dates.keys())[list(dates.values()).index(sorted(dates.values())[i])]] = \
                sorted(dates.values())[i]
                pivot = i
            else:
                pass
        features = layer.getFeatures(QgsFeatureRequest().setFilterFids(sorted(ids.keys())))
        no_features = layer.getFeatures(
            QgsFeatureRequest().setFilterFids([i for i in sorted(dates.keys()) if i not in sorted(ids.keys())]))
        return features, no_features

    def concat_point_name(self, features, point_name_idx):
        """
        If field is of type String, concatenate, otherwise preserve first value
        """
        feature_attrs = features[0].attributes()[:]
        for i in range(1, len(features)):
            if features[i].attributes()[point_name_idx] != feature_attrs[point_name_idx]:
                if type(features[i].attributes()[point_name_idx]) == str: # Concatenate values
                    feature_attrs[point_name_idx] = ";".join([feature_attrs[point_name_idx], features[i].attributes()[point_name_idx]])
                else: # Let first feature's value
                    feature_attrs.insert(point_name_idx, feature_attrs[point_name_idx])
            else:
                feature_attrs[i] = feature_attrs[point_name_idx]

        return feature_attrs

    def average_per_group(self, source_layer, point_name):
        idx = source_layer.fields().indexOf(GROUP_FIELD_NAME)
        group_ids = source_layer.uniqueValues(idx)

        layer = self.copy_attribs(source_layer, "Average Points")

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
            features = [f for f in source_layer.getFeatures("\"{}\"={} AND \"{}\" = 'True'".format(GROUP_FIELD_NAME, group_id, TRUSTWORTHY_FIELD_NAME))]
            if not len(features):
                continue

            new_attrs = self.concat_point_name(features, source_layer.fields().indexFromName(point_name))
            fields_values = dict(zip(range(0, len(features[0].attributes())), new_attrs))

            x_mean = 0
            y_mean = 0
            count = 0
            x_list = []
            y_list = []
            for feature in source_layer.getFeatures('"{}" = {}'.format(GROUP_FIELD_NAME, group_id)):
                current_point = feature.geometry().asPoint()
                x_list.append(current_point.x())
                y_list.append(current_point.y())

            if x_list and y_list:
                x_mean = statistics.mean(x_list)
                y_mean = statistics.mean(y_list)
                x_stdev = statistics.pstdev(x_list)
                y_stdev = statistics.pstdev(y_list)
            else:
                continue

            geom = QgsGeometry.fromPointXY(QgsPointXY(x_mean, y_mean))
            fields = layer.fields()
            fields_values.update({
                fields.indexOf("group_id"): group_id,
                fields.indexOf("count"): len(x_list),
                fields.indexOf("x_mean"): x_mean,
                fields.indexOf("y_mean"): y_mean,
                fields.indexOf("x_stdev"): x_stdev,
                fields.indexOf("y_stdev"): y_stdev
            })
            new_feature = QgsVectorLayerUtils.createFeature(layer, geom, fields_values)
            new_features.append(new_feature)

        layer.dataProvider().addFeatures(new_features)
        features = source_layer.getFeatures("\"{}\" IS NULL".format(GROUP_FIELD_NAME))
        layer.dataProvider().addFeatures(features)
        QgsProject.instance().addMapLayer(layer)

        self.qgis_utils.message_emitted.emit(
            QCoreApplication.translate("ControlledMeasurementDialog",
                                       "A new average point layer has been added to the map!"),
            Qgis.Info)


    def show_help(self):
        self.qgis_utils.show_help("controlled_measurement")
