# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2020-03-06
        git sha              : :%H$
        copyright            : (C) 2020 by Leo Cardona (BSF Swissphoto)
                               (C) 2020 by Germán Carrillo (BSF Swissphoto)
        email                : leo.cardona.p@gmail.com
                               gcarrillo@linuxmail.org
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
 """
import processing

from qgis.PyQt.QtCore import QVariant
from qgis.core import (QgsField,
                       QgsProject,
                       QgsVectorLayer,
                       QgsVectorLayerUtils,
                       QgsFeatureRequest)

from asistente_ladm_col.utils.qgis_model_baker_utils import QgisModelBakerUtils


class UtilsQualityRules:

    @staticmethod
    def get_boundary_points_features_not_covered_by_plot_nodes(boundary_point_layer, plot_layer, id_field):
        plot_nodes_layer = UtilsQualityRules.get_plot_nodes_layer(plot_layer, id_field)
        return UtilsQualityRules.get_points_not_covered_by_points(boundary_point_layer, plot_nodes_layer, id_field)

    @staticmethod
    def get_plot_nodes_features_not_covered_by_boundary_points(boundary_point_layer, plot_layer, id_field):
        plot_nodes_layer = UtilsQualityRules.get_plot_nodes_layer(plot_layer, id_field)
        return UtilsQualityRules.get_points_not_covered_by_points(plot_nodes_layer, boundary_point_layer, id_field)

    @staticmethod
    def get_plot_nodes_layer(plot_layer, id_field):
        """
        Layer is created with unique vertices. It is necessary because 'remove duplicate vertices' processing
        algorithm does not filter the data as wee need them
        """
        tmp_plot_nodes_layer = processing.run("native:extractvertices", {'INPUT': plot_layer, 'OUTPUT': 'memory:'})['OUTPUT']
        plot_nodes_layer = QgsVectorLayer("Point?crs={}".format(plot_layer.sourceCrs().authid()), 'unique boundary nodes', "memory")
        data_provider = plot_nodes_layer.dataProvider()
        data_provider.addAttributes([QgsField(id_field, QVariant.String)])
        plot_nodes_layer.updateFields()

        id_field_idx = tmp_plot_nodes_layer.fields().indexFromName(id_field)
        request = QgsFeatureRequest().setSubsetOfAttributes([id_field_idx])

        filter_fs = list()
        fs = list()
        for f in tmp_plot_nodes_layer.getFeatures(request):
            item = [f[id_field], f.geometry().asWkt()]
            if item not in filter_fs:
                filter_fs.append(item)
                new_feature = QgsVectorLayerUtils().createFeature(plot_nodes_layer, f.geometry(), {0: f[id_field]})
                fs.append(new_feature)

        plot_nodes_layer.dataProvider().addFeatures(fs)
        return plot_nodes_layer

    @staticmethod
    def get_points_not_covered_by_points(input_layer, join_layer, id_field):
        # get non matching features between input and join layer
        spatial_join_layer = processing.run("qgis:joinattributesbylocation",
                                            {'INPUT': input_layer,
                                             'JOIN': join_layer,
                                             'PREDICATE': [0],  # Intersects
                                             'JOIN_FIELDS': [id_field],
                                             'METHOD': 0,
                                             'DISCARD_NONMATCHING': False,
                                             'PREFIX': '',
                                             'NON_MATCHING': 'memory:'})['NON_MATCHING']
        features = list()

        for feature in spatial_join_layer.getFeatures():
            # When the two layers have the same attribute, the field of the layer
            # that makes the join is rename and input layer conserve the same name
            feature_id = feature[id_field]  # Whe use input layer field
            feature_geom = feature.geometry()
            features.append((feature_id, feature_geom))

        return features

    @staticmethod
    def add_error_layer(db, qgis_utils, error_layer):
        group = qgis_utils.get_error_layers_group()

        # Check if layer is loaded and remove it
        layers = group.findLayers()
        for layer in layers:
            if layer.name() == error_layer.name():
                group.removeLayer(layer.layer())
                break

        added_layer = QgsProject.instance().addMapLayer(error_layer, False)
        index = QgisModelBakerUtils().get_suggested_index_for_layer(added_layer, group)
        added_layer = group.insertLayer(index, added_layer).layer()
        if added_layer.isSpatial():
            # db connection is none because we are using a memory layer
            qgis_utils.symbology.set_layer_style_from_qml(db, added_layer, is_error_layer=True)
        return added_layer
