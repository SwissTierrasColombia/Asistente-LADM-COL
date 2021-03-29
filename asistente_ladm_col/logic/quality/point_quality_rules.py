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
from qgis.PyQt.QtCore import (QCoreApplication,
                              QVariant)
from qgis.core import (Qgis,
                       QgsField,
                       QgsFeature,
                       QgsGeometry,
                       QgsPointXY,
                       QgsProcessingFeedback,
                       QgsSpatialIndex,
                       QgsVectorLayer,
                       QgsVectorLayerUtils,
                       QgsFeatureRequest,
                       NULL,
                       QgsRectangle)

from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.config.enums import EnumQualityRule
from asistente_ladm_col.lib.geometry import GeometryUtils
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.lib.quality_rule.quality_rule_manager import QualityRuleManager

from asistente_ladm_col.config.quality_rules_config import (QUALITY_RULE_ERROR_CODE_E100101,
                                                            QUALITY_RULE_ERROR_CODE_E100201,
                                                            QUALITY_RULE_ERROR_CODE_E100301,
                                                            QUALITY_RULE_ERROR_CODE_E100302,
                                                            QUALITY_RULE_ERROR_CODE_E100303,
                                                            QUALITY_RULE_ERROR_CODE_E100401,
                                                            QUALITY_RULE_LAYERS)


class PointQualityRules:
    def __init__(self):
        self.quality_rules_manager = QualityRuleManager()
        self.logger = Logger()
        self.app = AppInterface()
        self.geometry = GeometryUtils()

    def check_overlapping_boundary_point(self, db, layers):
        rule = self.quality_rules_manager.get_quality_rule(EnumQualityRule.Point.OVERLAPS_IN_BOUNDARY_POINTS)
        return self.__check_overlapping_points(db, rule, layers, QUALITY_RULE_ERROR_CODE_E100101)

    def check_overlapping_control_point(self, db, layers):
        rule = self.quality_rules_manager.get_quality_rule(EnumQualityRule.Point.OVERLAPS_IN_CONTROL_POINTS)
        return self.__check_overlapping_points(db, rule, layers, QUALITY_RULE_ERROR_CODE_E100201)

    def __check_overlapping_points(self, db, rule, layer_dict, error_code):
        """
        Shows which points are overlapping
        :param db: db connection instance
        :param layer_dict: Dict with layer name and layer object
        :return: msg, Qgis.MessageLevel
        """
        features = []
        layer_name = list(layer_dict[QUALITY_RULE_LAYERS].keys())[0] if layer_dict[QUALITY_RULE_LAYERS] else None
        point_layer = list(layer_dict[QUALITY_RULE_LAYERS].values())[0] if layer_dict[QUALITY_RULE_LAYERS] else None
        if not point_layer:
            return QCoreApplication.translate("PointQualityRules", "'{}' layer not found!").format(layer_name), Qgis.Critical

        if point_layer.featureCount() == 0:
            return (QCoreApplication.translate("PointQualityRules",
                                               "There are no points in layer '{}' to check for overlaps!").format(layer_name), Qgis.Warning)

        else:
            error_layer = QgsVectorLayer("Point?crs={}".format(point_layer.sourceCrs().authid()), rule.error_table_name, "memory")
            data_provider = error_layer.dataProvider()
            data_provider.addAttributes(rule.error_table_fields)
            error_layer.updateFields()

            overlapping = self.geometry.get_overlapping_points(point_layer)
            flat_overlapping = [id for items in overlapping for id in items]  # Build a flat list of ids

            dict_uuids = {f.id(): f[db.names.T_ILI_TID_F] for f in point_layer.getFeatures(flat_overlapping)}

            for items in overlapping:
                # We need a feature geometry, pick the first id to get it
                feature = point_layer.getFeature(items[0])
                point = feature.geometry()
                new_feature = QgsVectorLayerUtils().createFeature(
                    error_layer,
                    point,
                    {0: ", ".join([str(dict_uuids.get(i)) for i in items]),
                     1: len(items),
                     2: self.quality_rules_manager.get_error_message(error_code),
                     3: error_code})
                features.append(new_feature)

            error_layer.dataProvider().addFeatures(features)

            if error_layer.featureCount() > 0:
                added_layer = self.app.gui.add_error_layer(db, error_layer)
                return (QCoreApplication.translate("PointQualityRules",
                                                   "A memory layer with {} overlapping points in '{}' has been added to the map!").format(added_layer.featureCount(), layer_name),
                        Qgis.Critical)
            else:
                return (QCoreApplication.translate("PointQualityRules",
                                                   "There are no overlapping points in layer '{}'!").format(layer_name),
                        Qgis.Success)

    def check_boundary_points_covered_by_boundary_nodes(self, db, layer_dict):
        rule = self.quality_rules_manager.get_quality_rule(EnumQualityRule.Point.BOUNDARY_POINTS_COVERED_BY_BOUNDARY_NODES)

        layers = layer_dict[QUALITY_RULE_LAYERS]

        if not layers:
            return QCoreApplication.translate("PointQualityRules", "At least one required layer (boundary, boundary point, point_bfs) was not found!"), Qgis.Critical

        elif layers[db.names.LC_BOUNDARY_POINT_T].featureCount() == 0:
            return (QCoreApplication.translate("PointQualityRules",
                             "There are no boundary points to check 'boundary points should be covered by boundary nodes'."), Qgis.Warning)
        else:
            error_layer = QgsVectorLayer("Point?crs={}".format(layers[db.names.LC_BOUNDARY_POINT_T].sourceCrs().authid()),
                                         rule.error_table_name, "memory")

            data_provider = error_layer.dataProvider()
            data_provider.addAttributes(rule.error_table_fields)
            error_layer.updateFields()

            features = self.get_boundary_points_not_covered_by_boundary_nodes(db, layers[db.names.LC_BOUNDARY_POINT_T], layers[db.names.LC_BOUNDARY_T], layers[db.names.POINT_BFS_T], error_layer, db.names.T_ID_F)
            error_layer.dataProvider().addFeatures(features)

            if error_layer.featureCount() > 0:
                added_layer = self.app.gui.add_error_layer(db, error_layer)

                return (QCoreApplication.translate(
                                 "PointQualityRules", "A memory layer with {} boundary points not covered by boundary nodes has been added to the map!")
                                 .format(added_layer.featureCount()), Qgis.Critical)

            else:
                return (QCoreApplication.translate("PointQualityRules",
                                 "All boundary points are covered by boundary nodes!"), Qgis.Success)

    def check_boundary_points_covered_by_plot_nodes(self, db, layer_dict):
        rule = self.quality_rules_manager.get_quality_rule(EnumQualityRule.Point.BOUNDARY_POINTS_COVERED_BY_PLOT_NODES)

        layers = layer_dict[QUALITY_RULE_LAYERS]

        if not layers:
            return QCoreApplication.translate("PointQualityRules", "At least one required layer (plot, boundary point) was not found!"), Qgis.Critical

        if layers[db.names.LC_BOUNDARY_POINT_T].featureCount() == 0:
            return (QCoreApplication.translate("PointQualityRules",
                             "There are no boundary points to check 'boundary points should be covered by Plot nodes'."), Qgis.Warning)

        else:
            error_layer = QgsVectorLayer("Point?crs={}".format(layers[db.names.LC_BOUNDARY_POINT_T].sourceCrs().authid()),
                                         rule.error_table_name,
                                         "memory")

            data_provider = error_layer.dataProvider()
            data_provider.addAttributes(rule.error_table_fields)
            error_layer.updateFields()

            point_list = self.get_boundary_points_features_not_covered_by_plot_nodes(layers[db.names.LC_BOUNDARY_POINT_T],
                                                                                     layers[db.names.LC_PLOT_T],
                                                                                     db.names.T_ILI_TID_F)
            features = list()
            for point in point_list:
                new_feature = QgsVectorLayerUtils().createFeature(error_layer,
                                                                  point[1],  # Geometry
                                                                  {0: point[0],  # feature uuid
                                                                   1: self.quality_rules_manager.get_error_message(QUALITY_RULE_ERROR_CODE_E100401),
                                                                   2: QUALITY_RULE_ERROR_CODE_E100401})
                features.append(new_feature)

            error_layer.dataProvider().addFeatures(features)

            if error_layer.featureCount() > 0:
                added_layer = self.app.gui.add_error_layer(db, error_layer)

                return (QCoreApplication.translate("PointQualityRules",
                    "A memory layer with {} boundary points not covered by plot nodes has been added to the map!").format(added_layer.featureCount()), Qgis.Critical)

            else:
                return (QCoreApplication.translate("PointQualityRules",
                                 "All boundary points are covered by plot nodes!"), Qgis.Success)

    # UTILITY METHODS
    def get_boundary_points_not_covered_by_boundary_nodes(self, db, boundary_point_layer, boundary_layer, point_bfs_layer, error_layer, id_field):
        dict_uuid_boundary = {f[id_field]: f[db.names.T_ILI_TID_F] for f in boundary_layer.getFeatures()}
        dict_uuid_boundary_point = {f[id_field]: f[db.names.T_ILI_TID_F] for f in boundary_point_layer.getFeatures()}

        tmp_boundary_nodes_layer = processing.run("native:extractvertices", {'INPUT': boundary_layer, 'OUTPUT': 'memory:'})['OUTPUT']

        # layer is created with unique vertices
        # It is necessary because 'remove duplicate vertices' processing algorithm does not filter the data as we need them
        boundary_nodes_layer = QgsVectorLayer("Point?crs={}".format(boundary_layer.sourceCrs().authid()), 'unique boundary nodes', "memory")
        data_provider = boundary_nodes_layer.dataProvider()
        data_provider.addAttributes([QgsField(id_field, QVariant.Int)])
        boundary_nodes_layer.updateFields()

        id_field_idx = tmp_boundary_nodes_layer.fields().indexFromName(id_field)
        request = QgsFeatureRequest().setSubsetOfAttributes([id_field_idx])

        filter_fs = []
        fs = []
        for f in tmp_boundary_nodes_layer.getFeatures(request):
            f_id = f[id_field]
            f_geom = f.geometry()

            new_feature = QgsFeature()
            new_feature.setGeometry(f_geom)
            new_feature.setAttributes([f_id])

            item = [f_id, f_geom.asWkt()]
            if item not in filter_fs:
                filter_fs.append(item)
                fs.append(new_feature)
        del filter_fs
        boundary_nodes_layer.dataProvider().addFeatures(fs)
        processing.run("native:createspatialindex",
                       {'INPUT': boundary_nodes_layer})  # spatial index is created for better performance

        # Spatial Join between boundary_points and boundary_nodes
        spatial_join_layer = processing.run("qgis:joinattributesbylocation",
                       {'INPUT': boundary_point_layer,
                        'JOIN': boundary_nodes_layer,
                        'PREDICATE': [0], # Intersects
                        'JOIN_FIELDS': [db.names.T_ID_F],
                        'METHOD': 0,
                        'DISCARD_NONMATCHING': False,
                        'PREFIX': '',
                        'OUTPUT': 'memory:'})['OUTPUT']

        # create dict with layer data
        id_field_idx = boundary_point_layer.fields().indexFromName(id_field)
        request = QgsFeatureRequest().setSubsetOfAttributes([id_field_idx])
        dict_boundary_point = {feature[id_field]: feature for feature in boundary_point_layer.getFeatures(request)}

        exp_point_bfs = '"{}" is not null and "{}" is not null'.format(db.names.POINT_BFS_T_LC_BOUNDARY_POINT_F, db.names.POINT_BFS_T_LC_BOUNDARY_F)
        list_point_bfs = [{'boundary_point_id': feature[db.names.POINT_BFS_T_LC_BOUNDARY_POINT_F], 'boundary_id': feature[db.names.POINT_BFS_T_LC_BOUNDARY_F]}
                     for feature in point_bfs_layer.getFeatures(exp_point_bfs)]

        spatial_join_boundary_point_boundary_node = [{'boundary_point_id': feature[id_field],
                                                     'boundary_id': feature[id_field + '_2']}
                                                     for feature in spatial_join_layer.getFeatures()]

        boundary_point_without_boundary_node = list()
        no_register_point_bfs = list()
        duplicate_in_point_bfs = list()

        # point_bfs topology check
        for item_sj in spatial_join_boundary_point_boundary_node:
            boundary_point_id = item_sj['boundary_point_id']
            boundary_id = item_sj['boundary_id']

            if boundary_id != NULL:
                if item_sj not in list_point_bfs:
                    no_register_point_bfs.append((boundary_point_id, boundary_id))  # no registered in point bfs
                elif list_point_bfs.count(item_sj) > 1:
                    duplicate_in_point_bfs.append((boundary_point_id, boundary_id))  # duplicate in point bfs
            else:
                boundary_point_without_boundary_node.append(boundary_point_id) # boundary point without boundary node

        features = list()

        # boundary point without boundary node
        if boundary_point_without_boundary_node is not None:
            for item in boundary_point_without_boundary_node:
                boundary_point_id = item  # boundary_point_id
                boundary_point_geom = dict_boundary_point[boundary_point_id].geometry()
                new_feature = QgsVectorLayerUtils().createFeature(error_layer, boundary_point_geom,
                                                                  {0: dict_uuid_boundary_point.get(boundary_point_id),
                                                                   1: None,
                                                                   2: self.quality_rules_manager.get_error_message(QUALITY_RULE_ERROR_CODE_E100301),
                                                                   3: QUALITY_RULE_ERROR_CODE_E100301})
                features.append(new_feature)


        # No registered in point_bfs
        if no_register_point_bfs is not None:
            for error_no_register in set(no_register_point_bfs):
                boundary_point_id = error_no_register[0]  # boundary_point_id
                boundary_id = error_no_register[1]  # boundary_id
                boundary_point_geom = dict_boundary_point[boundary_point_id].geometry()
                new_feature = QgsVectorLayerUtils().createFeature(error_layer, boundary_point_geom,
                                                                  {0: dict_uuid_boundary_point.get(boundary_point_id),
                                                                   1: dict_uuid_boundary.get(boundary_id),
                                                                   2: self.quality_rules_manager.get_error_message(QUALITY_RULE_ERROR_CODE_E100302),
                                                                   3: QUALITY_RULE_ERROR_CODE_E100302})
                features.append(new_feature)

        # Duplicate in point_bfs
        if duplicate_in_point_bfs is not None:
            for error_duplicate in set(duplicate_in_point_bfs):
                boundary_point_id = error_duplicate[0]  # boundary_point_id
                boundary_id = error_duplicate[1]  # boundary_id
                boundary_point_geom = dict_boundary_point[boundary_point_id].geometry()
                new_feature = QgsVectorLayerUtils().createFeature(error_layer, boundary_point_geom,
                                                                  {0: dict_uuid_boundary_point.get(boundary_point_id),
                                                                   1: dict_uuid_boundary.get(boundary_id),
                                                                   2: self.quality_rules_manager.get_error_message(QUALITY_RULE_ERROR_CODE_E100303),
                                                                   3: QUALITY_RULE_ERROR_CODE_E100303})
                features.append(new_feature)

        return features

    def get_missing_boundary_points_in_boundaries(self, db, boundary_point_layer, boundary_layer):
        res = dict()

        feedback = QgsProcessingFeedback()
        extracted_vertices = processing.run("native:extractvertices", {'INPUT':boundary_layer,'OUTPUT':'memory:'}, feedback=feedback)
        extracted_vertices_layer = extracted_vertices['OUTPUT']

        # From vertices layer, get points with no overlap
        overlapping_points = self.geometry.get_overlapping_points(extracted_vertices_layer)

        extracted_vertices_ids = [feature.id() for feature in extracted_vertices_layer.getFeatures()]

        # Unpack list of lists into single list
        overlapping_point_ids = [item for sublist in overlapping_points for item in sublist]

        # Unpack list of lists into single list selecting only the first point
        # per list. That means, discard overlapping points, and only keep one
        cleaned_point_ids = [sublist[0] for sublist in overlapping_points]

        # All vertices (even duplicated, due to the alg we use), minus all
        # overlapping ids, plus only one of the overlapping ids
        # This gets a list of all vertex ids with no duplicates
        no_duplicate_ids = list(set(extracted_vertices_ids) - set(overlapping_point_ids)) + cleaned_point_ids

        if boundary_point_layer.featureCount() == 0:
            # Return all extracted and cleaned vertices
            for feature in extracted_vertices_layer.getFeatures(no_duplicate_ids):
                if feature[db.names.T_ID_F] in res:
                    res[feature[db.names.T_ID_F]].append(feature.geometry())
                else:
                    res[feature[db.names.T_ID_F]] = [feature.geometry()]

            return res

        index = QgsSpatialIndex(boundary_point_layer.getFeatures(QgsFeatureRequest().setSubsetOfAttributes([])), feedback)

        for feature in extracted_vertices_layer.getFeatures(no_duplicate_ids):
            if feature.hasGeometry():
                geom = feature.geometry()
                diff_geom = QgsGeometry(geom)

                # Use a custom bbox to include very near but not exactly equal points
                point_vert = {'x': diff_geom.asPoint().x(), 'y': diff_geom.asPoint().y()}
                bbox = QgsRectangle(
                    QgsPointXY(point_vert['x'] - 0.0001, point_vert['y'] - 0.0001),
                    QgsPointXY(point_vert['x'] + 0.0001, point_vert['y'] + 0.0001)
                )
                intersects = index.intersects(bbox)

                if not intersects:
                    if feature[db.names.T_ID_F] in res:
                        res[feature[db.names.T_ID_F]].append(diff_geom)
                    else:
                        res[feature[db.names.T_ID_F]] = [diff_geom]
        return res

    @staticmethod
    def get_boundary_points_features_not_covered_by_plot_nodes(boundary_point_layer, plot_layer, id_field):
        plot_nodes_layer = GeometryUtils.get_polygon_nodes_layer(plot_layer, id_field)
        return GeometryUtils.get_non_intersecting_geometries(boundary_point_layer, plot_nodes_layer, id_field)
