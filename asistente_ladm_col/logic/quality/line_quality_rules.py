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
                       QgsVectorLayer,
                       QgsVectorLayerUtils,
                       QgsWkbTypes,
                       QgsFeatureRequest,
                       NULL)

from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.config.enums import EnumQualityRule
from asistente_ladm_col.config.quality_rules_config import (QUALITY_RULE_ERROR_CODE_E200101,
                                                            QUALITY_RULE_ERROR_CODE_E200201,
                                                            QUALITY_RULE_ERROR_CODE_E200301,
                                                            QUALITY_RULE_ERROR_CODE_E200302,
                                                            QUALITY_RULE_ERROR_CODE_E200303,
                                                            QUALITY_RULE_ERROR_CODE_E200304,
                                                            QUALITY_RULE_ERROR_CODE_E200305,
                                                            QUALITY_RULE_ERROR_CODE_E200401,
                                                            QUALITY_RULE_ERROR_CODE_E200402,
                                                            QUALITY_RULE_ERROR_CODE_E200403,
                                                            QUALITY_RULE_ERROR_CODE_E200501, 
                                                            QUALITY_RULE_LAYERS,
                                                            QUALITY_RULE_LADM_COL_LAYERS, 
                                                            HAS_ADJUSTED_LAYERS)
from asistente_ladm_col.lib.geometry import GeometryUtils
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.lib.quality_rule.quality_rule_manager import QualityRuleManager
from asistente_ladm_col.utils.utils import get_uuid_dict


class LineQualityRules:
    def __init__(self):
        self.app = AppInterface()
        self.logger = Logger()
        self.geometry = GeometryUtils()
        self.quality_rules_manager = QualityRuleManager()

    def check_overlaps_in_boundaries(self, db, layer_dict):
        rule = self.quality_rules_manager.get_quality_rule(EnumQualityRule.Line.OVERLAPS_IN_BOUNDARIES)
        boundary_layer = list(layer_dict[QUALITY_RULE_LAYERS].values())[0] if layer_dict[QUALITY_RULE_LAYERS] else None

        if not boundary_layer:
            return QCoreApplication.translate("LineQualityRules", "'Boundary' layer not found!"), Qgis.Critical, list()

        # Create error layers structure
        error_point_layer = QgsVectorLayer("MultiPoint?crs={}".format(boundary_layer.sourceCrs().authid()), "{} (puntos)".format(rule.error_table_name), "memory")
        data_provider = error_point_layer.dataProvider()
        data_provider.addAttributes(rule.error_table_fields)
        error_point_layer.updateFields()

        error_line_layer = QgsVectorLayer("MultiLineString?crs={}".format(boundary_layer.sourceCrs().authid()), "{} (líneas)".format(rule.error_table_name), "memory")
        data_provider = error_line_layer.dataProvider()
        data_provider.addAttributes(rule.error_table_fields)
        error_line_layer.updateFields()

        if boundary_layer:
            overlapping = self.geometry.get_overlapping_lines(boundary_layer)
            if overlapping is None:
                return (QCoreApplication.translate("LineQualityRules",
                                 "There are no boundaries to check for overlaps!"), Qgis.Warning, list())
            elif not overlapping:  # overlapping might be {}
                return (QCoreApplication.translate("LineQualityRules",
                                 "There was an error extracting overlapping boundaries! See the log for details."), Qgis.Warning, list())
            else:
                points_intersected = overlapping['native:saveselectedfeatures_3:Intersected_Points']
                lines_intersected = overlapping['native:saveselectedfeatures_2:Intersected_Lines']

                if isinstance(points_intersected, QgsVectorLayer):
                    point_features = list()
                    if points_intersected.featureCount() > 0:
                        for feature in points_intersected.getFeatures():
                            new_feature = QgsVectorLayerUtils().createFeature(
                                error_point_layer,
                                feature.geometry(),
                                {0: feature[db.names.T_ILI_TID_F],
                                 1: feature["{}_2".format(db.names.T_ILI_TID_F)],
                                 2: self.quality_rules_manager.get_error_message(QUALITY_RULE_ERROR_CODE_E200101),
                                 3: QUALITY_RULE_ERROR_CODE_E200101})
                            point_features.append(new_feature)
                    error_point_layer.dataProvider().addFeatures(point_features)

                if isinstance(lines_intersected, QgsVectorLayer):
                    line_features = list()
                    if lines_intersected.featureCount() > 0:
                        for feature in lines_intersected.getFeatures():
                            new_feature = QgsVectorLayerUtils().createFeature(
                                error_line_layer,
                                feature.geometry(),
                                {0: feature[db.names.T_ILI_TID_F],
                                 1: feature["{}_2".format(db.names.T_ILI_TID_F)],
                                 2: self.quality_rules_manager.get_error_message(QUALITY_RULE_ERROR_CODE_E200101),
                                 3: QUALITY_RULE_ERROR_CODE_E200101})
                            line_features.append(new_feature)

                    error_line_layer.dataProvider().addFeatures(line_features)

                if error_point_layer.featureCount() == 0 and error_line_layer.featureCount() == 0:
                    return QCoreApplication.translate("LineQualityRules", "There are no overlapping boundaries."), \
                           Qgis.Success, [error_point_layer, error_line_layer]
                else:
                    msg = ""
                    if error_point_layer.featureCount() and error_line_layer.featureCount():
                        msg = QCoreApplication.translate("LineQualityRules",
                                                         "Two memory layers with overlapping boundaries ({} point intersections and {} line intersections) have been added to the map.").format(error_point_layer.featureCount(), error_line_layer.featureCount())
                    elif error_point_layer.featureCount():
                        msg = QCoreApplication.translate("LineQualityRules",
                                                         "A memory layer with {} overlapping boundaries (point intersections) has been added to the map.").format(error_point_layer.featureCount())
                    elif error_line_layer.featureCount():
                        msg = QCoreApplication.translate("LineQualityRules",
                                                         "A memory layer with {} overlapping boundaries (line intersections) has been added to the map.").format(error_line_layer.featureCount())
                    return msg, Qgis.Critical, [error_point_layer, error_line_layer]

    def check_boundaries_are_not_split(self, db, layer_dict):
        """
        An split boundary is an incomplete boundary because it is connected to
        a single boundary and therefore, they don't represent a change in
        boundary (colindancia).
        """
        rule = self.quality_rules_manager.get_quality_rule(EnumQualityRule.Line.BOUNDARIES_ARE_NOT_SPLIT)

        features = []
        boundary_layer = list(layer_dict[QUALITY_RULE_LAYERS].values())[0] if layer_dict[QUALITY_RULE_LAYERS] else None
        if not boundary_layer:
            return QCoreApplication.translate("LineQualityRules", "'Boundary' layer not found!"), Qgis.Critical, list()

        if boundary_layer.featureCount() == 0:
            return (QCoreApplication.translate("LineQualityRules",
                             "There are no boundaries to check 'boundaries should not be split'!"), Qgis.Warning, list())

        else:
            wrong_boundaries = self.geometry.get_boundaries_connected_to_single_boundary(db.names, boundary_layer)

            if wrong_boundaries is None:
                return (QCoreApplication.translate("LineQualityRules",
                                 "There are no wrong boundaries!"), Qgis.Success, list())
            else:
                error_layer = QgsVectorLayer("LineString?crs={}".format(boundary_layer.sourceCrs().authid()),
                                             rule.error_table_name, "memory")
                pr = error_layer.dataProvider()
                pr.addAttributes(rule.error_table_fields)
                error_layer.updateFields()

                # Get geometries from LADM-COL original layer. If not HAS_ADJUSTED_LAYERS, it's OK to get
                # them from wrong_boundaries list, as it would have been created from original geoms
                if layer_dict[HAS_ADJUSTED_LAYERS]:
                    ladm_col_boundary_layer = list(layer_dict[QUALITY_RULE_LADM_COL_LAYERS].values())[0] if layer_dict[QUALITY_RULE_LADM_COL_LAYERS] else boundary_layer
                    wrong_tids = ",".join([str(f[db.names.T_ID_F]) for f in wrong_boundaries])  # Use t_id, which is indexed
                    geoms = {f[db.names.T_ILI_TID_F]:f.geometry() for f in ladm_col_boundary_layer.getFeatures("{} IN ({})".format(db.names.T_ID_F, wrong_tids))}
                else:
                    geoms = {f[db.names.T_ILI_TID_F]: f.geometry() for f in wrong_boundaries}

                for feature in wrong_boundaries:
                    new_feature = QgsVectorLayerUtils().createFeature(error_layer,
                                                                      geoms[feature[db.names.T_ILI_TID_F]],
                                                                      {0: feature[db.names.T_ILI_TID_F],
                                                                       1: self.quality_rules_manager.get_error_message(QUALITY_RULE_ERROR_CODE_E200201),
                                                                       2: QUALITY_RULE_ERROR_CODE_E200201})
                    features.append(new_feature)

                error_layer.dataProvider().addFeatures(features)
                if error_layer.featureCount() > 0:
                    return (QCoreApplication.translate("LineQualityRules",
                                     "A memory layer with {} wrong boundaries has been added to the map!").format(error_layer.featureCount()), Qgis.Critical, [error_layer])
                else:
                    return (QCoreApplication.translate("LineQualityRules",
                                     "There are no wrong boundaries."), Qgis.Success, [error_layer])

    def check_boundaries_covered_by_plots(self, db, layer_dict):
        rule = self.quality_rules_manager.get_quality_rule(EnumQualityRule.Line.BOUNDARIES_COVERED_BY_PLOTS)

        layers = layer_dict[QUALITY_RULE_LAYERS]

        if not layers:
            return QCoreApplication.translate("LineQualityRules", "At least one required layer (plot, boundary, more BFS, less BFS) was not found!"), Qgis.Critical, list()

        # validate data
        if layers[db.names.LC_BOUNDARY_T].featureCount() == 0:
            return (QCoreApplication.translate("LineQualityRules",
                             "There are no boundaries to check 'boundaries should be covered by plots'."), Qgis.Warning, list())
        else:
            error_layer = QgsVectorLayer("MultiLineString?crs={}".format(layers[db.names.LC_BOUNDARY_T].sourceCrs().authid()),
                                         rule.error_table_name, "memory")

            data_provider = error_layer.dataProvider()
            data_provider.addAttributes(rule.error_table_fields)
            error_layer.updateFields()

            features = self.get_boundary_features_not_covered_by_plots(db,
                                                                       layers[db.names.LC_PLOT_T],
                                                                       layers[db.names.LC_BOUNDARY_T],
                                                                       layers[db.names.MORE_BFS_T],
                                                                       layers[db.names.LESS_BFS_T],
                                                                       error_layer,
                                                                       db.names.T_ID_F)

            if features:
                error_layer.dataProvider().addFeatures(features)
                return (QCoreApplication.translate("LineQualityRules",
                                 "A memory layer with {} boundaries not covered by plots has been added to the map!").format(error_layer.featureCount()), Qgis.Critical, [error_layer])
            else:
                return (QCoreApplication.translate("LineQualityRules",
                                 "All boundaries are covered by plots!"), Qgis.Success, [error_layer])

    def check_boundary_nodes_covered_by_boundary_points(self, db, layer_dict):
        rule = self.quality_rules_manager.get_quality_rule(EnumQualityRule.Line.BOUNDARY_NODES_COVERED_BY_BOUNDARY_POINTS)

        layers = layer_dict[QUALITY_RULE_LAYERS]

        if not layers:
            return QCoreApplication.translate("LineQualityRules", "At least one required layer (boundary point, boundary, point BFS) was not found!"), Qgis.Critical, list()
        elif layers[db.names.LC_BOUNDARY_T].featureCount() == 0:
            return (QCoreApplication.translate("LineQualityRules",
                             "There are no boundaries to check 'missing boundary points in boundaries'."), Qgis.Warning, list())
        else:
            error_layer = QgsVectorLayer("Point?crs={}".format(layers[db.names.LC_BOUNDARY_T].sourceCrs().authid()),
                                         rule.error_table_name, "memory")
            data_provider = error_layer.dataProvider()
            data_provider.addAttributes(rule.error_table_fields)
            error_layer.updateFields()

            features = self.get_boundary_nodes_features_not_covered_by_boundary_points(db,
                                                                                       layers[db.names.LC_BOUNDARY_POINT_T],
                                                                                       layers[db.names.LC_BOUNDARY_T],
                                                                                       layers[db.names.POINT_BFS_T],
                                                                                       error_layer,
                                                                                       db.names.T_ID_F)
            data_provider.addFeatures(features)

            if error_layer.featureCount() > 0:
                return (QCoreApplication.translate("LineQualityRules",
                    "A memory layer with {} boundary vertices with no associated boundary points or with boundary points wrongly registered in the PointBFS table been added to the map!").format(added_layer.featureCount()), Qgis.Critical, [error_layer])

            else:
                return (QCoreApplication.translate("LineQualityRules",
                                 "There are no missing boundary points in boundaries."), Qgis.Success, [error_layer])

    def check_dangles_in_boundaries(self, db, layer_dict):
        rule = self.quality_rules_manager.get_quality_rule(EnumQualityRule.Line.DANGLES_IN_BOUNDARIES)

        boundary_layer = list(layer_dict[QUALITY_RULE_LAYERS].values())[0] if layer_dict[QUALITY_RULE_LAYERS] else None
        if not boundary_layer:
            return QCoreApplication.translate("LineQualityRules", "'Boundary' layer was not found!"), Qgis.Critical, list()

        if boundary_layer.featureCount() == 0:
            return (QCoreApplication.translate("LineQualityRules",
                             "There are no boundaries to check for dangles."), Qgis.Warning, list())

        else:
            error_layer = QgsVectorLayer("Point?crs={}".format(boundary_layer.sourceCrs().authid()),
                                         rule.error_table_name, "memory")
            pr = error_layer.dataProvider()
            pr.addAttributes(rule.error_table_fields)
            error_layer.updateFields()

            end_points, dangle_ids = self.geometry.get_dangle_ids(boundary_layer)

            new_features = []
            for dangle in end_points.getFeatures(dangle_ids):
                new_feature = QgsVectorLayerUtils().createFeature(end_points,
                                                                  dangle.geometry(),
                                                                  {0: dangle[db.names.T_ILI_TID_F],
                                                                   1: self.quality_rules_manager.get_error_message(QUALITY_RULE_ERROR_CODE_E200501),
                                                                   2: QUALITY_RULE_ERROR_CODE_E200501})
                new_features.append(new_feature)

            error_layer.dataProvider().addFeatures(new_features)

            if error_layer.featureCount() > 0:
                return (QCoreApplication.translate("LineQualityRules",
                                 "A memory layer with {} boundary dangles has been added to the map!").format(added_layer.featureCount()), Qgis.Critical, [error_layer])

            else:
                return (QCoreApplication.translate("LineQualityRules",
                                 "Boundaries have no dangles!"), Qgis.Success, [error_layer])


    # UTILITY METHODS
    def get_boundary_nodes_features_not_covered_by_boundary_points(self, db, boundary_point_layer, boundary_layer, point_bfs_layer, error_layer, id_field):
        dict_uuid_boundary_point = get_uuid_dict(boundary_point_layer, db.names, db.names.T_ID_F)
        dict_uuid_boundary = get_uuid_dict(boundary_layer, db.names, db.names.T_ID_F)
        tmp_boundary_nodes_layer = processing.run("native:extractvertices", {'INPUT': boundary_layer, 'OUTPUT': 'memory:'})['OUTPUT']

        # layer is created with unique vertices, it is necessary because 'remove duplicate vertices' processing algorithm does not filter the data as we need them
        boundary_nodes_unique_layer = QgsVectorLayer("Point?crs={}".format(boundary_layer.sourceCrs().authid()), 'unique boundary nodes', "memory")
        data_provider = boundary_nodes_unique_layer.dataProvider()
        data_provider.addAttributes([QgsField(id_field, QVariant.Int)])
        boundary_nodes_unique_layer.updateFields()

        id_field_idx = tmp_boundary_nodes_layer.fields().indexFromName(id_field)
        request = QgsFeatureRequest().setSubsetOfAttributes([id_field_idx])

        filter_fs = list()
        fs = list()
        for f in tmp_boundary_nodes_layer.getFeatures(request):
            item = [f[id_field], f.geometry().asWkt()]
            if item not in filter_fs:
                filter_fs.append(item)
                fs.append(f)
        boundary_nodes_unique_layer.dataProvider().addFeatures(fs)

        # Create an autoincremental field to have an identifying field
        boundary_nodes_layer = processing.run("native:addautoincrementalfield",
                                              {'INPUT': boundary_nodes_unique_layer,
                                               'FIELD_NAME': 'AUTO',
                                               'START': 0,
                                               'GROUP_FIELDS': [],
                                               'SORT_EXPRESSION': '',
                                               'SORT_ASCENDING': True,
                                               'SORT_NULLS_FIRST': False,
                                               'OUTPUT': 'memory:'})['OUTPUT']

        # Spatial Join between boundary_nodes and boundary_points
        spatial_join_layer = processing.run("qgis:joinattributesbylocation",
                                            {'INPUT': boundary_nodes_layer,
                                             'JOIN': boundary_point_layer,
                                             'PREDICATE': [0],  # Intersects
                                             'JOIN_FIELDS': [db.names.T_ID_F],
                                             'METHOD': 0,
                                             'DISCARD_NONMATCHING': False,
                                             'PREFIX': '',
                                             'OUTPUT': 'memory:'})['OUTPUT']

        # create dict with layer data
        id_field_idx = boundary_nodes_layer.fields().indexFromName(id_field)
        request = QgsFeatureRequest().setSubsetOfAttributes([id_field_idx])
        dict_boundary_nodes = {feature['AUTO']: feature for feature in boundary_nodes_layer.getFeatures(request)}

        exp_point_bfs = '"{}" is not null and "{}" is not null'.format(db.names.POINT_BFS_T_LC_BOUNDARY_POINT_F, db.names.POINT_BFS_T_LC_BOUNDARY_F)
        list_point_bfs = [{'boundary_point_id': feature[db.names.POINT_BFS_T_LC_BOUNDARY_POINT_F], 'boundary_id': feature[db.names.POINT_BFS_T_LC_BOUNDARY_F]}
                          for feature in point_bfs_layer.getFeatures(exp_point_bfs)]

        list_spatial_join_boundary_node_boundary_point = [{'boundary_point_id': feature[id_field + '_2'],
                                                           'boundary_node_id': feature['AUTO']}
                                                          for feature in spatial_join_layer.getFeatures()]

        boundary_node_without_boundary_point = list()
        no_register_point_bfs = list()
        duplicate_in_point_bfs = list()

        # point_bfs topology check
        for item_sj in list_spatial_join_boundary_node_boundary_point:
            boundary_node_id = item_sj['boundary_node_id']
            boundary_point_id = item_sj['boundary_point_id']

            if boundary_point_id != NULL:

                boundary_id = dict_boundary_nodes[boundary_node_id][id_field]  # get boundary id
                item_sj_check = {'boundary_point_id': boundary_point_id, 'boundary_id': boundary_id}  # dict to check

                if item_sj_check not in list_point_bfs:
                    no_register_point_bfs.append((boundary_point_id, boundary_node_id))  # no registered in point bfs
                elif list_point_bfs.count(item_sj_check) > 1:
                    duplicate_in_point_bfs.append((boundary_point_id, boundary_node_id))  # duplicate in point bfs
            else:
                boundary_node_without_boundary_point.append(boundary_node_id)  # boundary node without boundary point

        features = list()

        # boundary node without boundary point
        if boundary_node_without_boundary_point is not None:
            for item in boundary_node_without_boundary_point:
                boundary_node_id = item
                boundary_node_geom = dict_boundary_nodes[boundary_node_id].geometry()
                boundary_id = dict_boundary_nodes[boundary_node_id][id_field]  # get boundary id
                new_feature = QgsVectorLayerUtils().createFeature(error_layer, boundary_node_geom,
                                                                  {0: dict_uuid_boundary.get(boundary_id),
                                                                   1: None,
                                                                   2: self.quality_rules_manager.get_error_message(QUALITY_RULE_ERROR_CODE_E200401),
                                                                   3: QUALITY_RULE_ERROR_CODE_E200401})
                features.append(new_feature)

        # Duplicate in point_bfs
        if duplicate_in_point_bfs is not None:
            for error_duplicate in set(duplicate_in_point_bfs):
                boundary_point_id = error_duplicate[0]
                boundary_node_id = error_duplicate[1]
                boundary_node_geom = dict_boundary_nodes[boundary_node_id].geometry()
                boundary_id = dict_boundary_nodes[boundary_node_id][id_field]  # get boundary id
                new_feature = QgsVectorLayerUtils().createFeature(error_layer, boundary_node_geom,
                                                                  {0: dict_uuid_boundary.get(boundary_id),
                                                                   1: dict_uuid_boundary_point.get(boundary_point_id),
                                                                   2: self.quality_rules_manager.get_error_message(QUALITY_RULE_ERROR_CODE_E200403),
                                                                   3: QUALITY_RULE_ERROR_CODE_E200403})
                features.append(new_feature)

        # No registered in point_bfs
        if no_register_point_bfs is not None:
            for error_no_register in set(no_register_point_bfs):
                boundary_point_id = error_no_register[0]
                boundary_node_id = error_no_register[1]
                boundary_node_geom = dict_boundary_nodes[boundary_node_id].geometry()
                boundary_id = dict_boundary_nodes[boundary_node_id][id_field]  # get boundary id
                new_feature = QgsVectorLayerUtils().createFeature(error_layer, boundary_node_geom,
                                                                  {0: dict_uuid_boundary.get(boundary_id),
                                                                   1: dict_uuid_boundary_point.get(boundary_point_id),
                                                                   2: self.quality_rules_manager.get_error_message(QUALITY_RULE_ERROR_CODE_E200402),
                                                                   3: QUALITY_RULE_ERROR_CODE_E200402})
                features.append(new_feature)

        return features

    def get_boundary_features_not_covered_by_plots(self, db, plot_layer, boundary_layer, more_bfs_layer, less_layer, error_layer, id_field):
        """
        Return all boundary features that have errors when checking if they are covered by plots.
        This takes into account both geometric and alphanumeric (topology table) errors.
        """
        dict_uuid_plot = get_uuid_dict(plot_layer, db.names, db.names.T_ID_F)
        dict_uuid_boundary = get_uuid_dict(boundary_layer, db.names, db.names.T_ID_F)
        plot_as_lines_layer = processing.run("ladm_col:polygonstolines", {'INPUT': plot_layer, 'OUTPUT': 'memory:'})['OUTPUT']

        # create dict with layer data
        id_field_idx = plot_as_lines_layer.fields().indexFromName(id_field)
        request = QgsFeatureRequest().setSubsetOfAttributes([id_field_idx])
        dict_plot_as_lines = {feature[id_field]: feature for feature in plot_as_lines_layer.getFeatures(request)}

        id_field_idx = boundary_layer.fields().indexFromName(id_field)
        request = QgsFeatureRequest().setSubsetOfAttributes([id_field_idx])
        dict_boundary = {feature[id_field]: feature for feature in boundary_layer.getFeatures(request)}

        exp_more = '"{}" is not null and "{}" is not null'.format(db.names.MORE_BFS_T_LC_BOUNDARY_F, db.names.MORE_BFS_T_LC_PLOT_F)
        list_more_bfs = [{'plot_id': feature[db.names.MORE_BFS_T_LC_PLOT_F], 'boundary_id': feature[db.names.MORE_BFS_T_LC_BOUNDARY_F]}
                         for feature in more_bfs_layer.getFeatures(exp_more)]

        exp_less = '"{}" is not null and "{}" is not null'.format(db.names.LESS_BFS_T_LC_BOUNDARY_F, db.names.LESS_BFS_T_LC_PLOT_F)
        list_less = [{'plot_id': feature[db.names.LESS_BFS_T_LC_PLOT_F], 'boundary_id': feature[db.names.LESS_BFS_T_LC_BOUNDARY_F]}
                     for feature in less_layer.getFeatures(exp_less)]

        tmp_inner_rings_layer = self.geometry.get_inner_rings_layer(db.names, plot_layer, db.names.T_ID_F)
        inner_rings_layer = processing.run("native:addautoincrementalfield",
                                           {'INPUT': tmp_inner_rings_layer,
                                            'FIELD_NAME': 'AUTO',
                                            'START': 0,
                                            'GROUP_FIELDS': [],
                                            'SORT_EXPRESSION': '',
                                            'SORT_ASCENDING': True,
                                            'SORT_NULLS_FIRST': False,
                                            'OUTPUT': 'memory:'})['OUTPUT']

        id_field_idx = inner_rings_layer.fields().indexFromName(id_field)
        auto_idx = inner_rings_layer.fields().indexFromName('AUTO')
        request = QgsFeatureRequest().setSubsetOfAttributes([id_field_idx, auto_idx])
        dict_inner_rings = {'{}-{}'.format(feature[id_field], feature['AUTO']): feature for feature in inner_rings_layer.getFeatures(request)}

        # spatial joins between boundary and inner rings
        # we use as input layer the rings because it is the existing information
        # in the terrain polygons and filters better because they are less records
        spatial_join_inner_rings_boundary_layer = processing.run("qgis:joinattributesbylocation",
                                                                 {'INPUT': boundary_layer,
                                                                  'JOIN': inner_rings_layer,
                                                                  'PREDICATE': [0],  # Intersects
                                                                  'JOIN_FIELDS': [id_field, 'AUTO'],
                                                                  'METHOD': 0,
                                                                  'DISCARD_NONMATCHING': True,
                                                                  'PREFIX': '',
                                                                  'OUTPUT': 'memory:'})['OUTPUT']

        list_spatial_join_boundary_inner_rings = list()
        list_spatial_join_boundary_plot_ring = list()
        for feature in spatial_join_inner_rings_boundary_layer.getFeatures():
            # The id field has the same name for both layers
            # This list is only used to check plot's inner rings without boundaries
            list_spatial_join_boundary_inner_rings.append({'plot_ring_id': '{}-{}'.format(feature[id_field + '_2'], feature['AUTO']), 'boundary_id': feature[id_field]})

            # list create for filter inner rings from spatial join with between plot and boundary
            list_spatial_join_boundary_plot_ring.append({'plot_id': feature[id_field + '_2'], 'boundary_id': feature[id_field]})

        # Spatial join between boundary and plots as lines
        spatial_join_boundary_plot_layer = processing.run("qgis:joinattributesbylocation",
                                                          {'INPUT': boundary_layer,
                                                           'JOIN': plot_as_lines_layer,
                                                           'PREDICATE': [0],
                                                           'JOIN_FIELDS': [id_field],
                                                           'METHOD': 0,
                                                           'DISCARD_NONMATCHING': True,
                                                           'PREFIX': '',
                                                           'OUTPUT': 'memory:'})['OUTPUT']

        # The id field has the same name for both layers
        list_spatial_join_boundary_plot = [{'plot_id': feature[id_field + '_2'], 'boundary_id': feature[id_field]}
                                           for feature in spatial_join_boundary_plot_layer.getFeatures()]


        #####################################################
        # Validation of geometric errors
        #####################################################

        # Identify plots with geometry problems and remove coincidence in spatial join between plot as line and boundary
        # and inner_rings and boundary. If the geometry fails, there is no need to check further topological rules for
        # plots

        errors_boundary_plot_diffs = self.geometry.difference_boundary_plot(db.names, boundary_layer, plot_as_lines_layer, db.names.T_ID_F)
        for error_diff in errors_boundary_plot_diffs:
            boundary_id = error_diff['id']
            # All boundaries with geometric errors are eliminated. It is not necessary check more
            # in spatial join between boundary and plot as line
            for item_sj in list_spatial_join_boundary_plot.copy():
                if item_sj['boundary_id'] == boundary_id:
                    list_spatial_join_boundary_plot.remove(item_sj)

            # All boundaries with geometric errors are eliminated. It is not necessary check more
            # in spatial join between boundary and inner_rings
            for item_sj in list_spatial_join_boundary_inner_rings.copy():
                if item_sj['boundary_id'] == boundary_id:
                    list_spatial_join_boundary_inner_rings.remove(item_sj)

        ######################################################
        # Validation of errors in alphanumeric topology tables
        ######################################################

        # start validation in alphanumeric topology tables for more_bfs
        # remove spatial join intersection with geometries that no contain lines. Because it is not necessary to check
        for item_sj in list_spatial_join_boundary_plot.copy():
            boundary_id = item_sj['boundary_id']
            plot_id = item_sj['plot_id']

            if item_sj in list_spatial_join_boundary_plot_ring:
                # it is removed because it is registered in the spatial join between rings and boundaries
                # and it shouldn't be registered in the topology table of more_bfs
                list_spatial_join_boundary_plot.remove(item_sj)
            else:
                boundary_geom = dict_boundary[boundary_id].geometry()
                plot_geom = dict_plot_as_lines[plot_id].geometry()
                intersection = boundary_geom.intersection(plot_geom)

                if not intersection.isEmpty():
                    if intersection.type() != QgsWkbTypes.LineGeometry:
                        if intersection.type() == QgsWkbTypes.UnknownGeometry:
                            has_line = False
                            for part in intersection.asGeometryCollection():
                                if part.isMultipart():
                                    for i in range(part.numGeometries()):
                                        if QgsWkbTypes.geometryType(
                                                part.geometryN(i).wkbType()) == QgsWkbTypes.LineGeometry:
                                            has_line = True
                                            break
                                else:
                                    if part.type() == QgsWkbTypes.LineGeometry:
                                        has_line = True
                                        break
                            if not has_line:
                                # Remove point intersections plot-boundary
                                list_spatial_join_boundary_plot.remove(item_sj)
                        else:
                            list_spatial_join_boundary_plot.remove(item_sj)

        # Check relation between plot and boundary not registered in more_bfs
        errors_not_in_more_bfs = list()
        errors_duplicate_in_more_bfs = list()
        for item_sj_bp in list_spatial_join_boundary_plot:
            count_more_bfs = list_more_bfs.count(item_sj_bp)
            if count_more_bfs > 1:
                errors_duplicate_in_more_bfs.append((item_sj_bp['plot_id'], item_sj_bp['boundary_id']))
            elif count_more_bfs == 0:
                # Check for the special case of two contiguous plots, one of them covers the common boundary, but the
                # other one does not! This should be still a geometry error but is not captured by the code above. Only
                # in this point of the whole checks we can validate between the individual boundary and the individual
                # plot.
                boundary_geom = dict_boundary[item_sj_bp['boundary_id']].geometry()
                plot_geom = dict_plot_as_lines[item_sj_bp['plot_id']].geometry()
                intersection = boundary_geom.intersection(plot_geom)

                if not intersection.isEmpty():
                    if intersection.isGeosEqual(boundary_geom):
                        errors_not_in_more_bfs.append((item_sj_bp['plot_id'], item_sj_bp['boundary_id']))
                    else:
                        errors_boundary_plot_diffs.append({
                            'id': item_sj_bp['boundary_id'],
                            'id_plot': item_sj_bp['plot_id'],
                            'geometry': boundary_geom})

        # finalize validation in more_bfs table

        # start validation in less table
        errors_not_in_less = list()
        errors_duplicate_in_less = list()
        # start validation in alphanumeric topology tables for less
        # remove spatial join intersection with geometries that do not contain lines.
        # Because it is not necessary to check topology register
        for inner_ring in list_spatial_join_boundary_inner_rings:
            boundary_id = inner_ring['boundary_id']
            plot_ring_id = inner_ring['plot_ring_id']

            boundary_geom = dict_boundary[boundary_id].geometry()
            inner_ring_geom = dict_inner_rings[plot_ring_id].geometry()

            # check intersections difference to line, we check that collections do not have lines parts
            intersection = boundary_geom.intersection(inner_ring_geom)
            has_line = False

            if not intersection.isEmpty():
                if intersection.type() != QgsWkbTypes.LineGeometry:
                    if intersection.type() == QgsWkbTypes.UnknownGeometry:
                        for part in intersection.asGeometryCollection():
                            if part.isMultipart():
                                for i in range(part.numGeometries()):
                                    if QgsWkbTypes.geometryType(part.geometryN(i).wkbType()) == QgsWkbTypes.LineGeometry:
                                        has_line = True
                                        break
                            else:
                                if part.type() == QgsWkbTypes.LineGeometry:
                                    has_line = True
                                    break
                else:
                    has_line = True

            if has_line:
                tmp_dict_plot_boundary = {'plot_id': int(plot_ring_id.split('-')[0]), 'boundary_id': boundary_id}
                count_less = list_less.count(tmp_dict_plot_boundary)

                if count_less >1:
                    errors_duplicate_in_less.append((plot_ring_id, boundary_id))  # duplicate in less table
                elif count_less == 0:
                    errors_not_in_less.append((plot_ring_id, boundary_id))  # no registered less table
        # finalize validation for less table

        features = list()

        # boundary not covered by plot
        for boundary_plot_diff in errors_boundary_plot_diffs:
            boundary_id = boundary_plot_diff['id']
            boundary_geom = boundary_plot_diff['geometry']
            plot_id = boundary_plot_diff['id_plot'] if 'id_plot' in boundary_plot_diff else None
            new_feature = QgsVectorLayerUtils().createFeature(error_layer, boundary_geom,
                                                              {0: dict_uuid_boundary.get(boundary_id),
                                                               1: dict_uuid_plot.get(plot_id),
                                                               2: self.quality_rules_manager.get_error_message(QUALITY_RULE_ERROR_CODE_E200301),
                                                               3: QUALITY_RULE_ERROR_CODE_E200301})
            features.append(new_feature)

        # No registered more bfs
        if errors_not_in_more_bfs:
            for error_more_bfs in set(errors_not_in_more_bfs):
                plot_id = error_more_bfs[0]  # plot_id
                boundary_id = error_more_bfs[1]  # boundary_id
                geom_boundary = dict_boundary[boundary_id].geometry()
                new_feature = QgsVectorLayerUtils().createFeature(error_layer,
                                                                  geom_boundary,
                                                                  {0: dict_uuid_boundary.get(boundary_id),
                                                                   1: dict_uuid_plot.get(plot_id),
                                                                   2: self.quality_rules_manager.get_error_message(QUALITY_RULE_ERROR_CODE_E200304),
                                                                   3: QUALITY_RULE_ERROR_CODE_E200304})
                features.append(new_feature)

        # Duplicate in more bfs
        if errors_duplicate_in_more_bfs:
            for error_more_bfs in set(errors_duplicate_in_more_bfs):
                plot_id = error_more_bfs[0]  # plot_id
                boundary_id = error_more_bfs[1]  # boundary_id
                geom_boundary = dict_boundary[boundary_id].geometry()
                new_feature = QgsVectorLayerUtils().createFeature(error_layer,
                                                                  geom_boundary,
                                                                  {0: dict_uuid_boundary.get(boundary_id),
                                                                   1: dict_uuid_plot.get(plot_id),
                                                                   2: self.quality_rules_manager.get_error_message(QUALITY_RULE_ERROR_CODE_E200302),
                                                                   3: QUALITY_RULE_ERROR_CODE_E200302})
                features.append(new_feature)

        # No registered less
        if errors_not_in_less:
            for error_less in set(errors_not_in_less):
                plot_ring_id = error_less[0]  # plot_ring_id
                plot_id = int(plot_ring_id.split('-')[0]) # plot_id
                boundary_id = error_less[1]  # boundary_id
                geom_ring = dict_inner_rings[plot_ring_id].geometry()
                new_feature = QgsVectorLayerUtils().createFeature(error_layer,
                                                                  geom_ring,
                                                                  {0: dict_uuid_boundary.get(boundary_id),
                                                                   1: dict_uuid_plot.get(plot_id),
                                                                   2: self.quality_rules_manager.get_error_message(QUALITY_RULE_ERROR_CODE_E200305),
                                                                   3: QUALITY_RULE_ERROR_CODE_E200305})
                features.append(new_feature)

        # Duplicate in less
        if errors_duplicate_in_less:
            for error_less in set(errors_duplicate_in_less):
                plot_ring_id = error_less[0]  # plot_ring_id
                plot_id = int(plot_ring_id.split('-')[0]) # plot_id
                boundary_id = error_less[1]  # boundary_id
                geom_ring = dict_inner_rings[plot_ring_id].geometry()
                new_feature = QgsVectorLayerUtils().createFeature(error_layer,
                                                                  geom_ring,
                                                                  {0: dict_uuid_boundary.get(boundary_id),
                                                                   1: dict_uuid_plot.get(plot_id),
                                                                   2: self.quality_rules_manager.get_error_message(QUALITY_RULE_ERROR_CODE_E200303),
                                                                   3: QUALITY_RULE_ERROR_CODE_E200303})
                features.append(new_feature)

        return features
