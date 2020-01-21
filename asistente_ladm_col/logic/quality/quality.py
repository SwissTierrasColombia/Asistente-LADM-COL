# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2018-04-16
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
from qgis.PyQt.QtCore import (QObject,
                              QCoreApplication,
                              QVariant,
                              QSettings,
                              pyqtSignal)
from qgis.core import (Qgis,
                       QgsField,
                       QgsGeometry,
                       QgsPointXY,
                       QgsProcessingFeedback,
                       QgsProject,
                       QgsSpatialIndex,
                       QgsVectorLayer,
                       QgsVectorLayerUtils,
                       QgsWkbTypes,
                       QgsFeatureRequest,
                       NULL,
                       QgsRectangle)
import processing

from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.logic.quality.logic_checks import LogicChecks
from asistente_ladm_col.utils.qgis_model_baker_utils import QgisModelBakerUtils
from asistente_ladm_col.config.general_config import (LAYER,
                                                      DEFAULT_USE_ROADS_VALUE,
                                                      LOG_QUALITY_LIST_ITEM_ERROR_OPEN,
                                                      LOG_QUALITY_LIST_ITEM_CORRECT_OPEN,
                                                      LOG_QUALITY_LIST_ITEM_ERROR_CLOSE,
                                                      LOG_QUALITY_LIST_ITEM_CORRECT_CLOSE,
                                                      LOG_QUALITY_LIST_ITEM_OPEN,
                                                      LOG_QUALITY_LIST_ITEM_CLOSE,
                                                      CHECK_OVERLAPS_IN_BOUNDARY_POINTS,
                                                      CHECK_OVERLAPS_IN_CONTROL_POINTS,
                                                      CHECK_BOUNDARY_POINTS_COVERED_BY_BOUNDARY_NODES,
                                                      CHECK_BOUNDARY_POINTS_COVERED_BY_PLOT_NODES,
                                                      CHECK_OVERLAPS_IN_BOUNDARIES,
                                                      CHECK_BOUNDARIES_ARE_NOT_SPLIT,
                                                      CHECK_BOUNDARIES_COVERED_BY_PLOTS,
                                                      CHECK_BOUNDARY_NODES_COVERED_BY_BOUNDARY_POINTS,
                                                      CHECK_PLOT_NODES_COVERED_BY_BOUNDARY_POINTS,
                                                      CHECK_DANGLES_IN_BOUNDARIES,
                                                      CHECK_OVERLAPS_IN_PLOTS,
                                                      CHECK_OVERLAPS_IN_BUILDINGS,
                                                      CHECK_OVERLAPS_IN_RIGHTS_OF_WAY,
                                                      CHECK_PLOTS_COVERED_BY_BOUNDARIES,
                                                      CHECK_RIGHT_OF_WAY_OVERLAPS_BUILDINGS,
                                                      CHECK_GAPS_IN_PLOTS,
                                                      CHECK_MULTIPART_IN_RIGHT_OF_WAY,
                                                      CHECK_BUILDING_WITHIN_PLOTS,
                                                      CHECK_BUILDING_UNIT_WITHIN_PLOTS,
                                                      ERROR_PLOT_IS_NOT_COVERED_BY_BOUNDARY,
                                                      ERROR_BOUNDARY_IS_NOT_COVERED_BY_PLOT,
                                                      ERROR_NO_MORE_BOUNDARY_FACE_STRING_TABLE,
                                                      ERROR_DUPLICATE_MORE_BOUNDARY_FACE_STRING_TABLE,
                                                      ERROR_NO_LESS_TABLE,
                                                      ERROR_DUPLICATE_LESS_TABLE,
                                                      ERROR_NO_FOUND_POINT_BFS,
                                                      ERROR_DUPLICATE_POINT_BFS,
                                                      ERROR_BOUNDARY_POINT_IS_NOT_COVERED_BY_BOUNDARY_NODE,
                                                      ERROR_BOUNDARY_NODE_IS_NOT_COVERED_BY_BOUNDARY_POINT,
                                                      ERROR_BUILDING_IS_NOT_OVER_A_PLOT,
                                                      ERROR_BUILDING_CROSSES_A_PLOT_LIMIT,
                                                      ERROR_BUILDING_UNIT_IS_NOT_OVER_A_PLOT,
                                                      ERROR_BUILDING_UNIT_CROSSES_A_PLOT_LIMIT)
from asistente_ladm_col.config.table_mapping_config import Names
from asistente_ladm_col.utils.utils import Utils
from asistente_ladm_col.utils.decorators import _log_quality_checks


class QualityUtils(QObject):
    log_quality_show_message_emitted = pyqtSignal(str, int)
    log_quality_show_button_emitted = pyqtSignal()
    log_quality_set_initial_progress_emitted = pyqtSignal(str)
    log_quality_set_final_progress_emitted = pyqtSignal(str)

    def __init__(self, qgis_utils):
        QObject.__init__(self)
        self.qgis_utils = qgis_utils
        self.logger = Logger()
        self.logic = LogicChecks()
        self.utils = Utils()
        self.qgis_model_baker_utils = QgisModelBakerUtils()
        self.log_dialog_quality_text_content = ""
        self.total_time = 0

    def set_count_topology_rules(self, count):
        self.log_quality_show_message_emitted.emit(QCoreApplication.translate("QualityUtils", ""), count)

    def generate_log_button(self):
        self.log_quality_show_button_emitted.emit()

    def get_log_dialog_quality_text(self):
        return self.log_dialog_quality_text, self.total_time

    def initialize_log_dialog_quality(self):
        self.log_dialog_quality_text = ""
        self.total_time = 0

    def log_message(self, msg, type=Qgis.Critical):
        if type == Qgis.Critical:
            prefix = LOG_QUALITY_LIST_ITEM_ERROR_OPEN
            suffix = LOG_QUALITY_LIST_ITEM_ERROR_CLOSE
        elif type == Qgis.Success:
            prefix = LOG_QUALITY_LIST_ITEM_CORRECT_OPEN
            suffix = LOG_QUALITY_LIST_ITEM_CORRECT_CLOSE
        else: # Qgis.Info
            prefix = LOG_QUALITY_LIST_ITEM_OPEN
            suffix = LOG_QUALITY_LIST_ITEM_CLOSE

        self.log_dialog_quality_text_content += "{}{}{}".format(prefix, msg, suffix)

    @_log_quality_checks
    def check_boundary_points_covered_by_boundary_nodes(self, db, rule_name, translated_strings):

        layers = {
            db.names.OP_BOUNDARY_T: {'name': db.names.OP_BOUNDARY_T, 'geometry': None, LAYER: None},
            db.names.POINT_BFS_T: {'name': db.names.POINT_BFS_T, 'geometry': None, LAYER: None},
            db.names.OP_BOUNDARY_POINT_T: {'name': db.names.OP_BOUNDARY_POINT_T, 'geometry': None, LAYER: None}
        }

        self.qgis_utils.get_layers(db, layers, load=True)
        if not layers:
            return None

        elif layers[db.names.OP_BOUNDARY_POINT_T][LAYER].featureCount() == 0:
            self.log_message(QCoreApplication.translate("QGISUtils",
                             "There are no boundary points to check 'boundary points should be covered by boundary nodes'."), Qgis.Info)
        else:
            error_layer = QgsVectorLayer("Point?crs={}".format(layers[db.names.OP_BOUNDARY_POINT_T][LAYER].sourceCrs().authid()),
                                         translated_strings[CHECK_BOUNDARY_POINTS_COVERED_BY_BOUNDARY_NODES],
                                         "memory")

            data_provider = error_layer.dataProvider()
            data_provider.addAttributes([QgsField('boundary_point_id', QVariant.Int),
                                         QgsField('boundary_id', QVariant.Int),
                                         QgsField('error_type', QVariant.String)])
            error_layer.updateFields()

            features = self.get_boundary_points_features_not_covered_by_boundary_nodes(db, layers[db.names.OP_BOUNDARY_POINT_T][LAYER], layers[db.names.OP_BOUNDARY_T][LAYER], layers[db.names.POINT_BFS_T][LAYER], error_layer, translated_strings, db.names.T_ID_F)
            error_layer.dataProvider().addFeatures(features)

            if error_layer.featureCount() > 0:
                added_layer = self.add_error_layer(error_layer)

                self.log_message(QCoreApplication.translate(
                                 "QGISUtils", "A memory layer with {} boundary points not covered by boundary nodes has been added to the map!")
                                 .format(added_layer.featureCount()))

            else:
                self.log_message(QCoreApplication.translate("QGISUtils",
                                 "All boundary points are covered by boundary nodes!"), Qgis.Success)

    def get_boundary_points_features_not_covered_by_boundary_nodes(self, db, boundary_point_layer, boundary_layer, point_bfs_layer, error_layer, translated_strings, id_field):
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
            item = [f[id_field], f.geometry().asWkt()]
            if item not in filter_fs:
                filter_fs.append(item)
                fs.append(f)
        del filter_fs
        boundary_nodes_layer.dataProvider().addFeatures(fs)

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

        exp_point_bfs = '"{}" is not null and "{}" is not null'.format(db.names.POINT_BFS_T_OP_BOUNDARY_POINT_F, db.names.POINT_BFS_T_OP_BOUNDARY_F)
        list_point_bfs = [{'boundary_point_id': feature[db.names.POINT_BFS_T_OP_BOUNDARY_POINT_F], 'boundary_id': feature[db.names.POINT_BFS_T_OP_BOUNDARY_F]}
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
                                                                  {0: boundary_point_id,
                                                                   1: None,
                                                                   2: translated_strings[ERROR_BOUNDARY_POINT_IS_NOT_COVERED_BY_BOUNDARY_NODE]})
                features.append(new_feature)


        # No registered in point_bfs
        if no_register_point_bfs is not None:
            for error_no_register in set(no_register_point_bfs):
                boundary_point_id = error_no_register[0]  # boundary_point_id
                boundary_id = error_no_register[1]  # boundary_id
                boundary_point_geom = dict_boundary_point[boundary_point_id].geometry()
                new_feature = QgsVectorLayerUtils().createFeature(error_layer, boundary_point_geom,
                                                                  {0: boundary_point_id,
                                                                   1: boundary_id,
                                                                   2: translated_strings[ERROR_NO_FOUND_POINT_BFS]})
                features.append(new_feature)

        # Duplicate in point_bfs
        if duplicate_in_point_bfs is not None:
            for error_duplicate in set(duplicate_in_point_bfs):
                boundary_point_id = error_duplicate[0]  # boundary_point_id
                boundary_id = error_duplicate[1]  # boundary_id
                boundary_point_geom = dict_boundary_point[boundary_point_id].geometry()
                new_feature = QgsVectorLayerUtils().createFeature(error_layer, boundary_point_geom,
                                                                  {0: boundary_point_id,
                                                                   1: boundary_id,
                                                                   2: translated_strings[ERROR_DUPLICATE_POINT_BFS]})
                features.append(new_feature)

        return features

    @_log_quality_checks
    def check_boundary_nodes_covered_by_boundary_points(self, db, rule_name, translated_strings):
        layers = {
            db.names.OP_BOUNDARY_POINT_T: {'name': db.names.OP_BOUNDARY_POINT_T, 'geometry': None, LAYER: None},
            db.names.POINT_BFS_T: {'name': db.names.POINT_BFS_T, 'geometry': None, LAYER: None},
            db.names.OP_BOUNDARY_T: {'name': db.names.OP_BOUNDARY_T, 'geometry': None, LAYER: None}
        }

        self.qgis_utils.get_layers(db, layers, load=True)
        if not layers:
            return None

        elif layers[db.names.OP_BOUNDARY_T][LAYER].featureCount() == 0:
            self.log_message(QCoreApplication.translate("QGISUtils",
                             "There are no boundaries to check 'missing boundary points in boundaries'."), Qgis.Info)
        else:
            error_layer = QgsVectorLayer("Point?crs={}".format(layers[db.names.OP_BOUNDARY_T][LAYER].sourceCrs().authid()),
                                         translated_strings[CHECK_BOUNDARY_NODES_COVERED_BY_BOUNDARY_POINTS],
                                         "memory")
            data_provider = error_layer.dataProvider()
            data_provider.addAttributes([QgsField('boundary_point_id', QVariant.Int),
                                         QgsField('boundary_id', QVariant.Int),
                                         QgsField('error_type', QVariant.String)])

            error_layer.updateFields()

            features = self.get_boundary_nodes_features_not_covered_by_boundary_points(db, layers[db.names.OP_BOUNDARY_POINT_T][LAYER], layers[db.names.OP_BOUNDARY_T][LAYER], layers[db.names.POINT_BFS_T][LAYER], error_layer, translated_strings, db.names.T_ID_F)
            data_provider.addFeatures(features)

            if error_layer.featureCount() > 0:
                added_layer = self.add_error_layer(error_layer)

                self.log_message(QCoreApplication.translate("QGISUtils",
                    "A memory layer with {} boundary vertices with no associated boundary points or with boundary points wrongly registered in the PointBFS table been added to the map!").format(added_layer.featureCount()))

            else:
                self.log_message(QCoreApplication.translate("QGISUtils",
                                 "There are no missing boundary points in boundaries."), Qgis.Success)

    def get_boundary_nodes_features_not_covered_by_boundary_points(self, db, boundary_point_layer, boundary_layer, point_bfs_layer, error_layer, translated_strings, id_field):
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

        exp_point_bfs = '"{}" is not null and "{}" is not null'.format(db.names.POINT_BFS_T_OP_BOUNDARY_POINT_F, db.names.POINT_BFS_T_OP_BOUNDARY_F)
        list_point_bfs = [{'boundary_point_id': feature[db.names.POINT_BFS_T_OP_BOUNDARY_POINT_F], 'boundary_id': feature[db.names.POINT_BFS_T_OP_BOUNDARY_F]}
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
                                                                  {0: None,  1: boundary_id, 2: translated_strings[ERROR_BOUNDARY_NODE_IS_NOT_COVERED_BY_BOUNDARY_POINT]})
                features.append(new_feature)

        # Duplicate in point_bfs
        if duplicate_in_point_bfs is not None:
            for error_duplicate in set(duplicate_in_point_bfs):
                boundary_point_id = error_duplicate[0]
                boundary_node_id = error_duplicate[1]
                boundary_node_geom = dict_boundary_nodes[boundary_node_id].geometry()
                boundary_id = dict_boundary_nodes[boundary_node_id][id_field]  # get boundary id
                new_feature = QgsVectorLayerUtils().createFeature(error_layer, boundary_node_geom,
                                                                  {0: boundary_point_id, 1: boundary_id, 2: translated_strings[ERROR_DUPLICATE_POINT_BFS]})
                features.append(new_feature)

        # No registered in point_bfs
        if no_register_point_bfs is not None:
            for error_no_register in set(no_register_point_bfs):
                boundary_point_id = error_no_register[0]
                boundary_node_id = error_no_register[1]
                boundary_node_geom = dict_boundary_nodes[boundary_node_id].geometry()
                boundary_id = dict_boundary_nodes[boundary_node_id][id_field]  # get boundary id
                new_feature = QgsVectorLayerUtils().createFeature(error_layer, boundary_node_geom,
                                                                  {0: boundary_point_id, 1: boundary_id, 2: translated_strings[ERROR_NO_FOUND_POINT_BFS]})
                features.append(new_feature)

        return features

    @_log_quality_checks
    def check_plot_nodes_covered_by_boundary_points(self, db, rule_name, translated_strings):
        layers = {
            db.names.OP_PLOT_T: {'name': db.names.OP_PLOT_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            db.names.OP_BOUNDARY_POINT_T: {'name': db.names.OP_BOUNDARY_POINT_T, 'geometry': None, LAYER: None}
        }
        self.qgis_utils.get_layers(db, layers, load=True)
        if not layers:
            return None

        if layers[db.names.OP_PLOT_T][LAYER].featureCount() == 0:
            self.log_message(QCoreApplication.translate("QGISUtils",
                             "There are no plots to check 'Plots should be covered by boundary points'."), Qgis.Info)
        else:
            error_layer = QgsVectorLayer("Point?crs={}".format(layers[db.names.OP_PLOT_T][LAYER].sourceCrs().authid()),
                                         translated_strings[CHECK_PLOT_NODES_COVERED_BY_BOUNDARY_POINTS],
                                         "memory")

            data_provider = error_layer.dataProvider()
            data_provider.addAttributes([QgsField('plot_id', QVariant.Int)])
            error_layer.updateFields()

            topology_rule = 'plot_nodes_covered_by_boundary_points'
            features = self.get_boundary_points_features_not_covered_by_plot_nodes_and_viceversa(db, layers[db.names.OP_BOUNDARY_POINT_T][LAYER], layers[db.names.OP_PLOT_T][LAYER], error_layer, topology_rule, db.names.T_ID_F)
            error_layer.dataProvider().addFeatures(features)

            if error_layer.featureCount() > 0:
                added_layer = self.add_error_layer(error_layer)
                self.log_message(QCoreApplication.translate(
                                 "QGISUtils",
                                 "A memory layer with {} plot nodes not covered by boundary points has been added to the map!")
                                 .format(added_layer.featureCount()))

            else:
                self.log_message(QCoreApplication.translate("QGISUtils",
                                 "All plot nodes are covered by boundary points!"), Qgis.Success)

    @_log_quality_checks
    def check_boundary_points_covered_by_plot_nodes(self, db, rule_name, translated_strings):
        layers = {
            db.names.OP_PLOT_T: {'name': db.names.OP_PLOT_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            db.names.OP_BOUNDARY_POINT_T: {'name': db.names.OP_BOUNDARY_POINT_T, 'geometry': None, LAYER: None}
        }

        self.qgis_utils.get_layers(db, layers, load=True)
        if not layers:
            return None

        if layers[db.names.OP_BOUNDARY_POINT_T][LAYER].featureCount() == 0:
            self.log_message(QCoreApplication.translate("QGISUtils",
                             "There are no boundary points to check 'boundary points should be covered by Plot nodes'."), Qgis.Info)

        else:
            error_layer = QgsVectorLayer("Point?crs={}".format(layers[db.names.OP_BOUNDARY_POINT_T][LAYER].sourceCrs().authid()),
                                         translated_strings[CHECK_BOUNDARY_POINTS_COVERED_BY_PLOT_NODES],
                                         "memory")

            data_provider = error_layer.dataProvider()
            data_provider.addAttributes([QgsField('boundary_point_id', QVariant.Int)])
            error_layer.updateFields()

            topology_rule = 'boundary_points_covered_by_plot_nodes'
            features = self.get_boundary_points_features_not_covered_by_plot_nodes_and_viceversa(db, layers[db.names.OP_BOUNDARY_POINT_T][LAYER], layers[db.names.OP_PLOT_T][LAYER], error_layer, topology_rule, db.names.T_ID_F)
            error_layer.dataProvider().addFeatures(features)

            if error_layer.featureCount() > 0:
                added_layer = self.add_error_layer(error_layer)

                self.log_message(QCoreApplication.translate("QGISUtils",
                    "A memory layer with {} boundary points not covered by plot nodes has been added to the map!").format(added_layer.featureCount()))

            else:
                self.log_message(QCoreApplication.translate("QGISUtils",
                                 "All boundary points are covered by plot nodes!"), Qgis.Success)

    def get_boundary_points_features_not_covered_by_plot_nodes_and_viceversa(self, db, boundary_point_layer, plot_layer, error_layer, topology_rule, id_field):
        tmp_plot_nodes_layer = processing.run("native:extractvertices", {'INPUT': plot_layer, 'OUTPUT': 'memory:'})['OUTPUT']

        # layer is created with unique vertices
        # It is necessary because 'remove duplicate vertices' processing algorithm does not filter the data as wee need them
        plot_nodes_layer = QgsVectorLayer("Point?crs={}".format(plot_layer.sourceCrs().authid()), 'unique boundary nodes', "memory")
        data_provider = plot_nodes_layer.dataProvider()
        data_provider.addAttributes([QgsField(id_field, QVariant.Int)])
        plot_nodes_layer.updateFields()

        id_field_idx = tmp_plot_nodes_layer.fields().indexFromName(id_field)
        request = QgsFeatureRequest().setSubsetOfAttributes([id_field_idx])

        filter_fs = list()
        fs = list()
        for f in tmp_plot_nodes_layer.getFeatures(request):
            item = [f[id_field], f.geometry().asWkt()]
            if item not in filter_fs:
                filter_fs.append(item)
                fs.append(f)
        plot_nodes_layer.dataProvider().addFeatures(fs)

        input_layer = None
        join_layer = None

        if topology_rule == 'boundary_points_covered_by_plot_nodes':
            input_layer = boundary_point_layer
            join_layer = plot_nodes_layer
        elif topology_rule == 'plot_nodes_covered_by_boundary_points':
            input_layer = plot_nodes_layer
            join_layer = boundary_point_layer

        # get non matching features between boundary point and plot node
        spatial_join_layer = processing.run("qgis:joinattributesbylocation",
                                                   {'INPUT': input_layer,
                                                    'JOIN': join_layer,
                                                    'PREDICATE': [0], # Intersects
                                                    'JOIN_FIELDS': [db.names.T_ID_F],
                                                    'METHOD': 0,
                                                    'DISCARD_NONMATCHING': False,
                                                    'PREFIX': '',
                                                    'NON_MATCHING': 'memory:'})['NON_MATCHING']
        features = list()

        for feature in spatial_join_layer.getFeatures():
            feature_id = feature[db.names.T_ID_F]
            feature_geom = feature.geometry()
            new_feature = QgsVectorLayerUtils().createFeature(error_layer, feature_geom, {0: feature_id})
            features.append(new_feature)

        return features

    @_log_quality_checks
    def check_overlapping_points(self, db, point_layer_name, rule_name, translated_strings):
        """
        Shows which points are overlapping
        :param db: db connection instance
        :param entity: points layer
        :return:
        """
        features = []
        point_layer = self.qgis_utils.get_layer(db, point_layer_name, load=True)
        if not point_layer:
            return

        if point_layer.featureCount() == 0:
            self.log_message(QCoreApplication.translate("QGISUtils",
                             "There are no points in layer '{}' to check for overlaps!").format(point_layer_name), Qgis.Info)

        else:
            error_layer_name = ''
            if point_layer_name == db.names.OP_BOUNDARY_POINT_T:
                error_layer_name = translated_strings[CHECK_OVERLAPS_IN_BOUNDARY_POINTS]
            elif point_layer_name == db.names.OP_CONTROL_POINT_T:
                error_layer_name = translated_strings[CHECK_OVERLAPS_IN_CONTROL_POINTS]

            error_layer = QgsVectorLayer("Point?crs={}".format(point_layer.sourceCrs().authid()),
                                         error_layer_name, "memory")
            data_provider = error_layer.dataProvider()
            data_provider.addAttributes([QgsField("point_count", QVariant.Int), QgsField("intersecting_ids", QVariant.String) ])
            error_layer.updateFields()

            overlapping = self.qgis_utils.geometry.get_overlapping_points(point_layer)
            flat_overlapping = [id for items in overlapping for id in items]  # Build a flat list of ids

            t_ids = {f.id(): f[db.names.T_ID_F] for f in point_layer.getFeatures(flat_overlapping)}

            for items in overlapping:
                # We need a feature geometry, pick the first id to get it
                feature = point_layer.getFeature(items[0])
                point = feature.geometry()
                new_feature = QgsVectorLayerUtils().createFeature(
                    error_layer,
                    point,
                    {0: len(items), 1: ", ".join([str(t_ids[i]) for i in items])})
                features.append(new_feature)

            error_layer.dataProvider().addFeatures(features)

            if error_layer.featureCount() > 0:
                added_layer = self.add_error_layer(error_layer)
                self.log_message(QCoreApplication.translate("QGISUtils",
                                 "A memory layer with {} overlapping points in '{}' has been added to the map!").format(
                                 added_layer.featureCount(), point_layer_name))
            else:
                self.log_message(QCoreApplication.translate("QGISUtils",
                                 "There are no overlapping points in layer '{}'!").format(point_layer_name), Qgis.Success)

    @_log_quality_checks
    def check_plots_covered_by_boundaries(self, db, rule_name, translated_strings):
        # read data
        layers = {
            db.names.OP_PLOT_T: {'name': db.names.OP_PLOT_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            db.names.OP_BOUNDARY_T: {'name': db.names.OP_BOUNDARY_T, 'geometry': None, LAYER: None},
            db.names.LESS_BFS_T: {'name': db.names.LESS_BFS_T, 'geometry': None, LAYER: None},
            db.names.MORE_BFS_T: {'name': db.names.MORE_BFS_T, 'geometry': None, LAYER: None}
        }
        self.qgis_utils.get_layers(db, layers, load=True)
        if not layers:
            return None

        if layers[db.names.OP_PLOT_T][LAYER].featureCount() == 0:
            self.log_message(QCoreApplication.translate("QGISUtils",
                             "There are no plots to check 'plots should be covered by boundaries'."), Qgis.Info)
        else:
            error_layer = QgsVectorLayer("MultiLineString?crs={}".format(layers[db.names.OP_PLOT_T][LAYER].sourceCrs().authid()),
                                         translated_strings[CHECK_PLOTS_COVERED_BY_BOUNDARIES],
                                         "memory")

            data_provider = error_layer.dataProvider()
            data_provider.addAttributes([QgsField('plot_id', QVariant.Int),
                                         QgsField('boundary_id', QVariant.Int),
                                         QgsField('error_type', QVariant.String)])
            error_layer.updateFields()

            features = self.get_plot_features_not_covered_by_boundaries(db,
                                                                        layers[db.names.OP_PLOT_T][LAYER],
                                                                        layers[db.names.OP_BOUNDARY_T][LAYER],
                                                                        layers[db.names.MORE_BFS_T][LAYER],
                                                                        layers[db.names.LESS_BFS_T][LAYER],
                                                                        error_layer,
                                                                        translated_strings,
                                                                        db.names.T_ID_F)
            if features:
                error_layer.dataProvider().addFeatures(features)
                added_layer = self.add_error_layer(error_layer)

                self.log_message(QCoreApplication.translate("QGISUtils",
                                 "A memory layer with {} plots not covered by boundaries has been added to the map!").format(added_layer.featureCount()))

            else:
                self.log_message(QCoreApplication.translate("QGISUtils",
                                 "All plots are covered by boundaries!"), Qgis.Success)

    def get_plot_features_not_covered_by_boundaries(self, db, plot_layer, boundary_layer, more_bfs_layer, less_layer, error_layer, translated_strings, id_field):
        """
        Returns all plot features that have errors when checking if they are covered by boundaries.
        That is both geometric and alphanumeric (topology table) errors.
        """
        type_tplg_error = {0: translated_strings[ERROR_PLOT_IS_NOT_COVERED_BY_BOUNDARY],
                           1: translated_strings[ERROR_NO_MORE_BOUNDARY_FACE_STRING_TABLE],
                           2: translated_strings[ERROR_DUPLICATE_MORE_BOUNDARY_FACE_STRING_TABLE],
                           3: translated_strings[ERROR_NO_LESS_TABLE],
                           4: translated_strings[ERROR_DUPLICATE_LESS_TABLE]}

        plot_as_lines_layer = processing.run("ladm_col:polygonstolines", {'INPUT': plot_layer, 'OUTPUT': 'memory:'})['OUTPUT']

        # create dict with layer data
        id_field_idx = plot_as_lines_layer.fields().indexFromName(id_field)
        request = QgsFeatureRequest().setSubsetOfAttributes([id_field_idx])
        dict_plot_as_lines = {feature[id_field]: feature for feature in plot_as_lines_layer.getFeatures(request)}

        id_field_idx = boundary_layer.fields().indexFromName(id_field)
        request = QgsFeatureRequest().setSubsetOfAttributes([id_field_idx])
        dict_boundary = {feature[id_field]: feature for feature in boundary_layer.getFeatures(request)}

        exp_more = '"{}" is not null and "{}" is not null'.format(db.names.MORE_BFS_T_OP_BOUNDARY_F, db.names.MORE_BFS_T_OP_PLOT_F)
        list_more_bfs = [{'plot_id': feature[db.names.MORE_BFS_T_OP_PLOT_F], 'boundary_id': feature[db.names.MORE_BFS_T_OP_BOUNDARY_F]}
                         for feature in more_bfs_layer.getFeatures(exp_more)]

        exp_less = '"{}" is not null and "{}" is not null'.format(db.names.LESS_BFS_T_OP_BOUNDARY_F, db.names.LESS_BFS_T_OP_PLOT_F)
        list_less = [{'plot_id': feature[db.names.LESS_BFS_T_OP_PLOT_F], 'boundary_id': feature[db.names.LESS_BFS_T_OP_BOUNDARY_F]}
                     for feature in less_layer.getFeatures(exp_less)]

        tmp_inner_rings_layer = self.qgis_utils.geometry.get_inner_rings_layer(plot_layer, db.names.T_ID_F)
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

        # spatial joins between inner rings and boundary
        spatial_join_inner_rings_boundary_layer = processing.run("qgis:joinattributesbylocation",
                                                                 {'INPUT': inner_rings_layer,
                                                                  'JOIN': boundary_layer,
                                                                  'PREDICATE': [0],  # Intersects
                                                                  'JOIN_FIELDS': [id_field],
                                                                  'METHOD': 0,
                                                                  'DISCARD_NONMATCHING': True,
                                                                  'PREFIX': '',
                                                                  'OUTPUT': 'memory:'})['OUTPUT']
        # The id field has the same name for both layers
        # This list is only used to check plot's inner rings without boundaries
        dict_spatial_join_inner_rings_boundary = [{'plot_ring_id': '{}-{}'.format(feature[id_field], feature['AUTO']), 'boundary_id': feature[id_field + '_2']}
                                                  for feature in spatial_join_inner_rings_boundary_layer.getFeatures()]

        # list create for filter inner rings from spatial join with between plot and boundary
        list_spatial_join_plot_ring_boundary = [{'plot_id': feature[id_field],
                                                   'boundary_id': feature[id_field + '_2']}
                                                  for feature in spatial_join_inner_rings_boundary_layer.getFeatures()]

        # Spatial join between plot as lines and boundary
        spatial_join_plot_boundary_layer = processing.run("qgis:joinattributesbylocation",
                                                          {'INPUT': plot_as_lines_layer,
                                                           'JOIN': boundary_layer,
                                                           'PREDICATE': [0],
                                                           'JOIN_FIELDS': [id_field],
                                                           'METHOD': 0,
                                                           'DISCARD_NONMATCHING': True,
                                                           'PREFIX': '',
                                                           'OUTPUT': 'memory:'})['OUTPUT']
        # The id field has the same name for both layers
        dict_spatial_join_plot_boundary = [{'plot_id': feature[id_field], 'boundary_id': feature[id_field + '_2']}
                                           for feature in spatial_join_plot_boundary_layer.getFeatures()]

        #####################################################
        # Validation of geometric errors
        #####################################################

        # Identify plots with geometry problems and remove coincidence in spatial join between plot as line and boundary
        # and inner_rings and boundary. No need to check further topological rules for plots

        errors_plot_boundary_diffs = self.qgis_utils.geometry.difference_plot_boundary(plot_as_lines_layer, boundary_layer, db.names.T_ID_F)
        for error_diff in errors_plot_boundary_diffs:
            plot_id = error_diff['id']
            # All plots with geometric errors are eliminated. It is not necessary check more
            # in spatial join between plot as line and boundary
            for item_sj in dict_spatial_join_plot_boundary.copy():
                if item_sj['plot_id'] == plot_id:
                    dict_spatial_join_plot_boundary.remove(item_sj)

            # All plots with geometric errors are eliminated. It is not necessary check more
            # in spatial join between inner_rings and boundary
            for item_sj in dict_spatial_join_inner_rings_boundary.copy():
                if int(item_sj['plot_ring_id'].split('-')[0]) == plot_id:
                    dict_spatial_join_inner_rings_boundary.remove(item_sj)

        ######################################################
        # Validation of errors in alphanumeric topology tables
        ######################################################

        # start validation for more_bfs table
        # remove spatial join intersection with geometries that no contain lines. Because it is not necessary to check
        for item_sj in dict_spatial_join_plot_boundary.copy():
            boundary_id = item_sj['boundary_id']
            plot_id = item_sj['plot_id']

            if item_sj in list_spatial_join_plot_ring_boundary:
                # it is removed because it is registered in the spatial join between rings and boundaries
                # and it shouldn't be registered in the topology table of more_bfs
                dict_spatial_join_plot_boundary.remove(item_sj)
            else:
                plot_geom = dict_plot_as_lines[plot_id].geometry()
                boundary_geom = dict_boundary[boundary_id].geometry()
                intersection = plot_geom.intersection(boundary_geom)

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
                            dict_spatial_join_plot_boundary.remove(item_sj)
                    else:
                        dict_spatial_join_plot_boundary.remove(item_sj)

        # Check relation between plot and boundary not registered in more_bfs
        errors_not_in_more_bfs = list()
        errors_duplicate_in_more_bfs = list()
        for item_sj_pb in dict_spatial_join_plot_boundary:
            count_more_bfs = list_more_bfs.count(item_sj_pb)
            if count_more_bfs > 1:
                errors_duplicate_in_more_bfs.append((item_sj_pb['plot_id'], item_sj_pb['boundary_id']))
            elif count_more_bfs == 0:
                errors_not_in_more_bfs.append((item_sj_pb['plot_id'], item_sj_pb['boundary_id']))

        # finalize validation for more_bfs table

        # start validation for less table

        errors_not_in_less = list()
        errors_duplicate_in_less = list()
        # start validation for more_bfs table
        # remove spatial join intersection with geometries that no contain lines.
        # Because it is not necessary to check topology register
        for inner_ring in dict_spatial_join_inner_rings_boundary:
            boundary_id = inner_ring['boundary_id']
            plot_ring_id = inner_ring['plot_ring_id']

            boundary_geom = dict_boundary[boundary_id].geometry()
            inner_ring_geom = dict_inner_rings[plot_ring_id].geometry()

            # check intersections difference to line, we check that collections dont have lines parts
            intersection = inner_ring_geom.intersection(boundary_geom)
            has_line = False
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
                    errors_not_in_less.append((plot_ring_id, boundary_id))  # not registered less table
        # finalize validation for less table

        features = list()

        # plot not covered by boundary
        for plot_boundary_diff in errors_plot_boundary_diffs:
            plot_id = plot_boundary_diff['id']
            plot_geom = plot_boundary_diff['geometry']
            new_feature = QgsVectorLayerUtils().createFeature(error_layer, plot_geom,
                                                              {0: plot_id, 1: None, 2: type_tplg_error[0]})
            features.append(new_feature)

        # not registered more bfs
        if errors_not_in_more_bfs:
            for error_more_bfs in set(errors_not_in_more_bfs):
                plot_id = error_more_bfs[0]  # plot_id
                boundary_id = error_more_bfs[1]  # boundary_id
                geom_plot = dict_plot_as_lines[plot_id].geometry()
                new_feature = QgsVectorLayerUtils().createFeature(error_layer, geom_plot,
                                                                  {0: plot_id, 1: boundary_id, 2: type_tplg_error[1]})
                features.append(new_feature)

        # Duplicate in more bfs
        if errors_duplicate_in_more_bfs:
            for error_more_bfs in set(errors_duplicate_in_more_bfs):
                plot_id = error_more_bfs[0]  # plot_id
                boundary_id = error_more_bfs[1]  # boundary_id
                geom_plot = dict_plot_as_lines[plot_id].geometry()
                new_feature = QgsVectorLayerUtils().createFeature(error_layer, geom_plot,
                                                                  {0: plot_id, 1: boundary_id, 2: type_tplg_error[2]})
                features.append(new_feature)

        # not registered less
        if errors_not_in_less:
            for error_less in set(errors_not_in_less):
                plot_ring_id = error_less[0]  # plot_ring_id
                plot_id = int(plot_ring_id.split('-')[0]) # plot_id
                boundary_id = error_less[1]  # boundary_id
                geom_ring = dict_inner_rings[plot_ring_id].geometry()
                new_feature = QgsVectorLayerUtils().createFeature(error_layer, geom_ring,
                                                                  {0: plot_id, 1: boundary_id, 2: type_tplg_error[3]})
                features.append(new_feature)

        # Duplicate in less
        if errors_duplicate_in_less:
            for error_less in set(errors_duplicate_in_less):
                plot_ring_id = error_less[0]  # plot_ring_id
                plot_id = int(plot_ring_id.split('-')[0]) # plot_id
                boundary_id = error_less[1]  # boundary_id
                geom_ring = dict_inner_rings[plot_ring_id].geometry()
                new_feature = QgsVectorLayerUtils().createFeature(error_layer, geom_ring,
                                                                  {0: plot_id, 1: boundary_id, 2: type_tplg_error[4]})
                features.append(new_feature)

        return features

    @_log_quality_checks
    def check_boundaries_covered_by_plots(self, db, rule_name, translated_strings):
        # read data
        layers = {
            db.names.OP_PLOT_T: {'name': db.names.OP_PLOT_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            db.names.OP_BOUNDARY_T: {'name': db.names.OP_BOUNDARY_T, 'geometry': None, LAYER: None},
            db.names.LESS_BFS_T: {'name': db.names.LESS_BFS_T, 'geometry': None, LAYER: None},
            db.names.MORE_BFS_T: {'name': db.names.MORE_BFS_T, 'geometry': None, LAYER: None}
        }

        self.qgis_utils.get_layers(db, layers, load=True)
        if not layers:
            return None

        # validate data
        if layers[db.names.OP_BOUNDARY_T][LAYER].featureCount() == 0:
            self.log_message(QCoreApplication.translate("QGISUtils",
                             "There are no boundaries to check 'boundaries should be covered by plots'."), Qgis.Info)
        else:
            error_layer = QgsVectorLayer("MultiLineString?crs={}".format(layers[db.names.OP_BOUNDARY_T][LAYER].sourceCrs().authid()),
                                         translated_strings[CHECK_BOUNDARIES_COVERED_BY_PLOTS],
                                         "memory")

            data_provider = error_layer.dataProvider()
            data_provider.addAttributes([QgsField('plot_id', QVariant.Int),
                                         QgsField('boundary_id', QVariant.Int),
                                         QgsField('error_type', QVariant.String)])
            error_layer.updateFields()

            features = self.get_boundary_features_not_covered_by_plots(db,
                                                                       layers[db.names.OP_PLOT_T][LAYER],
                                                                       layers[db.names.OP_BOUNDARY_T][LAYER],
                                                                       layers[db.names.MORE_BFS_T][LAYER],
                                                                       layers[db.names.LESS_BFS_T][LAYER],
                                                                       error_layer,
                                                                       translated_strings,
                                                                       db.names.T_ID_F)

            if features:
                error_layer.dataProvider().addFeatures(features)
                added_layer = self.add_error_layer(error_layer)

                self.log_message(QCoreApplication.translate("QGISUtils",
                                 "A memory layer with {} boundaries not covered by plots has been added to the map!").format(added_layer.featureCount()))

            else:
                self.log_message(QCoreApplication.translate("QGISUtils",
                                 "All boundaries are covered by plots!"), Qgis.Success)

    def get_boundary_features_not_covered_by_plots(self, db, plot_layer, boundary_layer, more_bfs_layer, less_layer, error_layer, translated_strings, id_field):
        """
        Return all boundary features that have errors when checking if they are covered by plots.
        This takes into account both geometric and alphanumeric (topology table) errors.
        """
        type_tplg_error = {0: translated_strings[ERROR_BOUNDARY_IS_NOT_COVERED_BY_PLOT],
                           1: translated_strings[ERROR_NO_MORE_BOUNDARY_FACE_STRING_TABLE],
                           2: translated_strings[ERROR_DUPLICATE_MORE_BOUNDARY_FACE_STRING_TABLE],
                           3: translated_strings[ERROR_NO_LESS_TABLE],
                           4: translated_strings[ERROR_DUPLICATE_LESS_TABLE]}

        plot_as_lines_layer = processing.run("ladm_col:polygonstolines", {'INPUT': plot_layer, 'OUTPUT': 'memory:'})['OUTPUT']

        # create dict with layer data
        id_field_idx = plot_as_lines_layer.fields().indexFromName(id_field)
        request = QgsFeatureRequest().setSubsetOfAttributes([id_field_idx])
        dict_plot_as_lines = {feature[id_field]: feature for feature in plot_as_lines_layer.getFeatures(request)}

        id_field_idx = boundary_layer.fields().indexFromName(id_field)
        request = QgsFeatureRequest().setSubsetOfAttributes([id_field_idx])
        dict_boundary = {feature[id_field]: feature for feature in boundary_layer.getFeatures(request)}

        exp_more = '"{}" is not null and "{}" is not null'.format(db.names.MORE_BFS_T_OP_BOUNDARY_F, db.names.MORE_BFS_T_OP_PLOT_F)
        list_more_bfs = [{'plot_id': feature[db.names.MORE_BFS_T_OP_PLOT_F], 'boundary_id': feature[db.names.MORE_BFS_T_OP_BOUNDARY_F]}
                         for feature in more_bfs_layer.getFeatures(exp_more)]

        exp_less = '"{}" is not null and "{}" is not null'.format(db.names.LESS_BFS_T_OP_BOUNDARY_F, db.names.LESS_BFS_T_OP_PLOT_F)
        list_less = [{'plot_id': feature[db.names.LESS_BFS_T_OP_PLOT_F], 'boundary_id': feature[db.names.LESS_BFS_T_OP_BOUNDARY_F]}
                     for feature in less_layer.getFeatures(exp_less)]

        tmp_inner_rings_layer = self.qgis_utils.geometry.get_inner_rings_layer(plot_layer, db.names.T_ID_F)
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

        # The id field has the same name for both layers
        # This list is only used to check plot's inner rings without boundaries
        list_spatial_join_boundary_inner_rings = [{'plot_ring_id': '{}-{}'.format(feature[id_field + '_2'], feature['AUTO']), 'boundary_id': feature[id_field]}
                                                  for feature in spatial_join_inner_rings_boundary_layer.getFeatures()]

        # list create for filter inner rings from spatial join with between plot and boundary
        list_spatial_join_boundary_plot_ring = [{'plot_id': feature[id_field + '_2'],
                                                 'boundary_id': feature[id_field]}
                                                for feature in spatial_join_inner_rings_boundary_layer.getFeatures()]

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

        errors_boundary_plot_diffs = self.qgis_utils.geometry.difference_boundary_plot(boundary_layer, plot_as_lines_layer, db.names.T_ID_F)
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
                                                              {0: plot_id, 1: boundary_id, 2: type_tplg_error[0]})
            features.append(new_feature)

        # No registered more bfs
        if errors_not_in_more_bfs:
            for error_more_bfs in set(errors_not_in_more_bfs):
                plot_id = error_more_bfs[0]  # plot_id
                boundary_id = error_more_bfs[1]  # boundary_id
                geom_boundary = dict_boundary[boundary_id].geometry()
                new_feature = QgsVectorLayerUtils().createFeature(error_layer, geom_boundary,
                                                                  {0: plot_id, 1: boundary_id, 2: type_tplg_error[1]})
                features.append(new_feature)

        # Duplicate in more bfs
        if errors_duplicate_in_more_bfs:
            for error_more_bfs in set(errors_duplicate_in_more_bfs):
                plot_id = error_more_bfs[0]  # plot_id
                boundary_id = error_more_bfs[1]  # boundary_id
                geom_boundary = dict_boundary[boundary_id].geometry()
                new_feature = QgsVectorLayerUtils().createFeature(error_layer, geom_boundary,
                                                                  {0: plot_id, 1: boundary_id, 2: type_tplg_error[2]})
                features.append(new_feature)

        # No registered less
        if errors_not_in_less:
            for error_less in set(errors_not_in_less):
                plot_ring_id = error_less[0]  # plot_ring_id
                plot_id = int(plot_ring_id.split('-')[0]) # plot_id
                boundary_id = error_less[1]  # boundary_id
                geom_ring = dict_inner_rings[plot_ring_id].geometry()
                new_feature = QgsVectorLayerUtils().createFeature(error_layer, geom_ring,
                                                                  {0: plot_id, 1: boundary_id, 2: type_tplg_error[3]})
                features.append(new_feature)

        # Duplicate in less
        if errors_duplicate_in_less:
            for error_less in set(errors_duplicate_in_less):
                plot_ring_id = error_less[0]  # plot_ring_id
                plot_id = int(plot_ring_id.split('-')[0]) # plot_id
                boundary_id = error_less[1]  # boundary_id
                geom_ring = dict_inner_rings[plot_ring_id].geometry()
                new_feature = QgsVectorLayerUtils().createFeature(error_layer, geom_ring,
                                                                  {0: plot_id, 1: boundary_id, 2: type_tplg_error[4]})
                features.append(new_feature)

        return features

    @_log_quality_checks
    def check_overlapping_polygons(self, db, polygon_layer_name, rule_name, translated_strings):
        polygon_layer = self.qgis_utils.get_layer(db, polygon_layer_name, QgsWkbTypes.PolygonGeometry, load=True)
        if not polygon_layer:
            return

        if polygon_layer:
            error_layer_name = ''
            if polygon_layer_name == db.names.OP_PLOT_T:
                error_layer_name = translated_strings[CHECK_OVERLAPS_IN_PLOTS]
            elif polygon_layer_name == db.names.OP_BUILDING_T:
                error_layer_name = translated_strings[CHECK_OVERLAPS_IN_BUILDINGS]
            elif polygon_layer_name == db.names.OP_RIGHT_OF_WAY_T:
                error_layer_name = translated_strings[CHECK_OVERLAPS_IN_RIGHTS_OF_WAY]

            error_layer = QgsVectorLayer("Polygon?crs={}".format(polygon_layer.sourceCrs().authid()),
                                         error_layer_name, "memory")
            data_provider = error_layer.dataProvider()
            data_provider.addAttributes([QgsField("polygon_id", QVariant.Int),
                                         QgsField("overlapping_ids", QVariant.String),
                                         QgsField("count_parts", QVariant.Int)])
            error_layer.updateFields()

            if QgsWkbTypes.isMultiType(polygon_layer.wkbType()) and \
                polygon_layer.geometryType() == QgsWkbTypes.PolygonGeometry:
                polygon_layer = processing.run("native:multiparttosingleparts",
                                               {'INPUT': polygon_layer, 'OUTPUT': 'memory:'})['OUTPUT']

            overlapping = self.qgis_utils.geometry.get_overlapping_polygons(polygon_layer)

            flat_overlapping = [id for items in overlapping for id in items]  # Build a flat list of ids
            flat_overlapping = list(set(flat_overlapping))  # unique values

            if type(polygon_layer) == QgsVectorLayer: # A string might come from processing for empty layers
                t_ids = {f.id(): f[db.names.T_ID_F] for f in polygon_layer.getFeatures() if f.id() in flat_overlapping}

            features = []

            for overlapping_item in overlapping:
                polygon_id_field = overlapping_item[0]
                overlapping_id_field = overlapping_item[1]
                polygon_intersection = self.qgis_utils.geometry.get_intersection_polygons(polygon_layer, polygon_id_field, overlapping_id_field)

                if polygon_intersection is not None:
                    new_feature = QgsVectorLayerUtils().createFeature(
                        error_layer,
                        polygon_intersection,
                        {0: t_ids[polygon_id_field],
                         1: t_ids[overlapping_id_field],
                         2: len(polygon_intersection.asMultiPolygon()) if polygon_intersection.isMultipart() else 1})

                    features.append(new_feature)

            error_layer.dataProvider().addFeatures(features)

            if error_layer.featureCount() > 0:
                added_layer = self.add_error_layer(error_layer)

                self.log_message(QCoreApplication.translate("QGISUtils",
                                 "A memory layer with {} overlapping polygons in layer '{}' has been added to the map!").format(
                                 added_layer.featureCount(), polygon_layer_name))

            else:
                self.log_message(QCoreApplication.translate("QGISUtils",
                                 "There are no overlapping polygons in layer '{}'!").format(polygon_layer_name), Qgis.Success)

    @_log_quality_checks
    def check_overlaps_in_boundaries(self, db, rule_name, translated_strings):
        boundary_layer = self.qgis_utils.get_layer(db, db.names.OP_BOUNDARY_T, load=True)
        if not boundary_layer:
            return

        if boundary_layer:
            overlapping = self.qgis_utils.geometry.get_overlapping_lines(boundary_layer)
            if overlapping is None:
                self.log_message(QCoreApplication.translate("QGISUtils",
                                 "There are no boundaries to check for overlaps!"), Qgis.Info)

            else:
                error_point_layer = overlapping['native:saveselectedfeatures_3:Intersected_Points']
                error_line_layer = overlapping['native:saveselectedfeatures_2:Intersected_Lines']
                if type(error_point_layer) is QgsVectorLayer:
                    error_point_layer.setName("{} (point intersections)".format(
                        translated_strings[CHECK_OVERLAPS_IN_BOUNDARIES]
                    ))
                if type(error_line_layer) is QgsVectorLayer:
                    error_line_layer.setName("{} (line intersections)".format(
                        translated_strings[CHECK_OVERLAPS_IN_BOUNDARIES]
                    ))

                if (type(error_point_layer) is not QgsVectorLayer and \
                   type(error_line_layer) is not QgsVectorLayer) or \
                   (error_point_layer.featureCount() == 0 and \
                   error_line_layer.featureCount() == 0):

                    self.log_message(QCoreApplication.translate("QGISUtils",
                                     "There are no overlapping boundaries."), Qgis.Success)

                else:
                    msg = ''

                    if type(error_point_layer) is QgsVectorLayer and error_point_layer.featureCount() > 0:
                        added_point_layer = self.add_error_layer(error_point_layer)
                        msg = QCoreApplication.translate("QGISUtils",
                            "A memory layer with {} overlapping boundaries (point intersections) has been added to the map.").format(added_point_layer.featureCount())

                    if type(error_line_layer) is QgsVectorLayer and error_line_layer.featureCount() > 0:
                        added_line_layer = self.add_error_layer(error_line_layer)
                        msg = QCoreApplication.translate("QGISUtils",
                            "A memory layer with {} overlapping boundaries (line intersections) has been added to the map.").format(added_line_layer.featureCount())

                    if type(error_point_layer) is QgsVectorLayer and \
                       type(error_line_layer) is QgsVectorLayer and \
                       error_point_layer.featureCount() > 0 and \
                       error_line_layer.featureCount() > 0:
                        msg = QCoreApplication.translate("QGISUtils",
                            "Two memory layers with overlapping boundaries ({} point intersections and {} line intersections) have been added to the map.").format(added_point_layer.featureCount(), added_line_layer.featureCount())

                    self.log_message(msg)

    @_log_quality_checks
    def check_boundaries_are_not_split(self, db, rule_name, translated_strings):
        """
        An split boundary is an incomplete boundary because it is connected to
        a single boundary and therefore, they don't represent a change in
        boundary (colindancia).
        """
        features = []
        boundary_layer = self.qgis_utils.get_layer(db, db.names.OP_BOUNDARY_T, load=True)
        if not boundary_layer:
            return

        if boundary_layer.featureCount() == 0:
            self.log_message(QCoreApplication.translate("QGISUtils",
                             "There are no boundaries to check 'boundaries should not be split'!"), Qgis.Info)

        else:
            wrong_boundaries = self.qgis_utils.geometry.get_boundaries_connected_to_single_boundary(boundary_layer)

            if wrong_boundaries is None:
                self.log_message(QCoreApplication.translate("QGISUtils",
                                 "There are no wrong boundaries!"), Qgis.Success)
            else:
                error_layer = QgsVectorLayer("LineString?crs={}".format(boundary_layer.sourceCrs().authid()),
                                translated_strings[CHECK_BOUNDARIES_ARE_NOT_SPLIT],
                                "memory")
                pr = error_layer.dataProvider()
                pr.addAttributes([QgsField("boundary_id", QVariant.Int)])
                error_layer.updateFields()

                for feature in wrong_boundaries:
                    new_feature = QgsVectorLayerUtils().createFeature(error_layer, feature.geometry(),
                                                                      {0: feature[db.names.T_ID_F]})
                    features.append(new_feature)

                error_layer.dataProvider().addFeatures(features)
                if error_layer.featureCount() > 0:
                    added_layer = self.add_error_layer(error_layer)
                    self.log_message(QCoreApplication.translate("QGISUtils",
                                     "A memory layer with {} wrong boundaries has been added to the map!").format(added_layer.featureCount()))
                else:
                    self.log_message(QCoreApplication.translate("QGISUtils",
                                     "There are no wrong boundaries."), Qgis.Success)

    @_log_quality_checks
    def check_missing_boundary_points_in_boundaries(self, db, translated_strings):
        """
        Not used anymore but kept for reference
        """
        layers = {
            db.names.OP_BOUNDARY_POINT_T: {'name': db.names.OP_BOUNDARY_POINT_T, 'geometry': None, LAYER: None},
            db.names.POINT_BFS_T: {'name': db.names.POINT_BFS_T, 'geometry': None, LAYER: None},
            db.names.OP_BOUNDARY_T: {'name': db.names.OP_BOUNDARY_T, 'geometry': None, LAYER: None}
        }

        self.qgis_utils.get_layers(db, layers, load=True)
        if not layers:
            return None

        if layers[db.names.OP_BOUNDARY_T][LAYER].featureCount() == 0:
            self.logger.info_msg(__name__, QCoreApplication.translate("QualityUtils",
                                           "There are no boundaries to check 'missing boundary points in boundaries'."))
            return

        error_layer = QgsVectorLayer("Point?crs={}".format(layers[db.names.OP_BOUNDARY_T][LAYER].sourceCrs().authid()),
                                     translated_strings[CHECK_BOUNDARY_NODES_COVERED_BY_BOUNDARY_POINTS],
                                     "memory")
        data_provider = error_layer.dataProvider()
        data_provider.addAttributes([QgsField('boundary_point_id', QVariant.Int),
                                     QgsField('boundary_id', QVariant.Int),
                                     QgsField('error_type', QVariant.String)])

        error_layer.updateFields()

        # check missing points
        missing_points = self.get_missing_boundary_points_in_boundaries(db, layers[db.names.OP_BOUNDARY_POINT_T][LAYER], layers[db.names.OP_BOUNDARY_T][LAYER])

        new_features = list()
        for key, point_list in missing_points.items():
            for point in point_list:
                new_feature = QgsVectorLayerUtils().createFeature(
                    error_layer,
                    point,
                    {
                        0: None,
                        1: key,
                        2: QCoreApplication.translate("QGISUtils", "Missing boundary point in boundary")})
                new_features.append(new_feature)

        dic_points_ccl = dict()
        for feature_point_ccl in layers[db.names.POINT_BFS_T][LAYER].getFeatures():
            key = "{}-{}".format(feature_point_ccl[db.names.COL_POINT_SOURCE_T_OP_BOUNDARY_POINT_F], feature_point_ccl[db.names.POINT_BFS_T_OP_BOUNDARY_F])
            if key in dic_points_ccl:
                dic_points_ccl[key] += 1
            else:
                dic_points_ccl.update({key:1})

        # verify that the relation between boundary point and boundary is registered in the topology table
        points_selected = self.qgis_utils.geometry.join_boundary_points_with_boundary_discard_nonmatching(layers[db.names.OP_BOUNDARY_POINT_T][LAYER], layers[db.names.OP_BOUNDARY_T][LAYER], db.names.T_ID_F)

        for point_selected in points_selected:
            boundary_point_id = point_selected[db.names.T_ID_F]
            boundary_id = point_selected['{}_2'.format(db.names.T_ID_F)]
            key_query = "{}-{}".format(boundary_point_id, boundary_id)

            if key_query in dic_points_ccl:
                if dic_points_ccl[key_query] > 1:
                    new_features.append(QgsVectorLayerUtils().createFeature(error_layer, point_selected.geometry(),
                        {0: boundary_point_id,
                         1: boundary_id,
                         2: QCoreApplication.translate("QGISUtils", "Relation found more than once in the PointBFS table")}))
            else:
                new_features.append(QgsVectorLayerUtils().createFeature(error_layer, point_selected.geometry(),
                    {0: boundary_point_id,
                     1: boundary_id,
                     2: QCoreApplication.translate("QGISUtils", "Relation not found in the PointBFS table")}))
        data_provider.addFeatures(new_features)

        if error_layer.featureCount() > 0:
            added_layer = self.add_error_layer(error_layer)

            self.logger.info_msg(__name__, QCoreApplication.translate("QualityUtils",
                "A memory layer with {} boundary vertices with no associated boundary points or with boundary points wrongly registered in the PointBFS table been added to the map!").format(added_layer.featureCount()))
        else:
            self.logger.info_msg(__name__, QCoreApplication.translate("QGISUtils",
                                           "There are no missing boundary points in boundaries."))

    def check_missing_survey_points_in_buildings(self, db):
        """
        Not used anymore but kept for reference.
        """
        layers = {
            db.names.OP_SURVEY_POINT_T: {'name': db.names.OP_SURVEY_POINT_T, 'geometry': None, LAYER: None},
            db.names.OP_BUILDING_T: {'name': db.names.OP_BUILDING_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None}
        }
        self.qgis_utils.get_layers(db, layers, load=True)
        if not layers:
            return None

        if layers[db.names.OP_BUILDING_T][LAYER].featureCount() == 0:
            self.logger.info_msg(__name__, QCoreApplication.translate("QGISUtils",
                "There are no buildings to check 'missing survey points in buildings'."))
            return

        error_layer = QgsVectorLayer("Point?crs={}".format(layers[db.names.OP_BUILDING_T][LAYER].sourceCrs().authid()),
                                     QCoreApplication.translate("QGISUtils", "Missing survey points in buildings"),
                                     "memory")
        data_provider = error_layer.dataProvider()
        data_provider.addAttributes([QgsField("building_id", QVariant.Int)])
        error_layer.updateFields()

        missing_points = self.get_missing_boundary_points_in_boundaries(db, layers[db.names.OP_SURVEY_POINT_T][LAYER], layers[db.names.OP_BUILDING_T][LAYER])

        new_features = list()
        for key, point_list in missing_points.items():
            for point in point_list:
                new_feature = QgsVectorLayerUtils().createFeature(error_layer, point, {0: key})
                new_features.append(new_feature)

        data_provider.addFeatures(new_features)

        if error_layer.featureCount() > 0:
            added_layer = self.add_error_layer(error_layer)

            self.logger.info_msg(__name__, QCoreApplication.translate("QualityUtils",
                "A memory layer with {} building vertices with no associated survey points has been added to the map!").format(added_layer.featureCount()))
        else:
            self.logger.info_msg(__name__, QCoreApplication.translate("QualityUtils",
                "There are no missing survey points in buildings."))

    @_log_quality_checks
    def check_dangles_in_boundaries(self, db, rule_name, translated_strings):
        boundary_layer = self.qgis_utils.get_layer(db, db.names.OP_BOUNDARY_T, load=True)
        if not boundary_layer:
            return

        if boundary_layer.featureCount() == 0:
            self.log_message(QCoreApplication.translate("QualityUtils",
                             "There are no boundaries to check for dangles."), Qgis.Info)

        else:
            error_layer = QgsVectorLayer("Point?crs={}".format(boundary_layer.sourceCrs().authid()),
                                translated_strings[CHECK_DANGLES_IN_BOUNDARIES],
                                "memory")
            pr = error_layer.dataProvider()
            pr.addAttributes([QgsField("boundary_id", QVariant.Int)])
            error_layer.updateFields()

            end_points, dangle_ids = self.get_dangle_ids(boundary_layer)

            new_features = []
            for dangle in end_points.getFeatures(dangle_ids):
                new_feature = QgsVectorLayerUtils().createFeature(end_points, dangle.geometry(), {0: dangle[db.names.T_ID_F]})
                new_features.append(new_feature)

            error_layer.dataProvider().addFeatures(new_features)

            if error_layer.featureCount() > 0:
                added_layer = self.add_error_layer(error_layer)

                self.log_message(QCoreApplication.translate("QualityUtils",
                                 "A memory layer with {} boundary dangles has been added to the map!").format(added_layer.featureCount()))

            else:
                self.log_message(QCoreApplication.translate("QualityUtils",
                                 "Boundaries have no dangles!"), Qgis.Success)

    def get_missing_boundary_points_in_boundaries(self, db, boundary_point_layer, boundary_layer):
        res = dict()

        feedback = QgsProcessingFeedback()
        extracted_vertices = processing.run("native:extractvertices", {'INPUT':boundary_layer,'OUTPUT':'memory:'}, feedback=feedback)
        extracted_vertices_layer = extracted_vertices['OUTPUT']

        # From vertices layer, get points with no overlap
        overlapping_points = self.qgis_utils.geometry.get_overlapping_points(extracted_vertices_layer)

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

    @_log_quality_checks
    def check_right_of_way_overlaps_buildings(self, db, rule_name, translated_strings):

        layers = {
            db.names.OP_RIGHT_OF_WAY_T: {'name': db.names.OP_RIGHT_OF_WAY_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            db.names.OP_BUILDING_T: {'name': db.names.OP_BUILDING_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None}
        }

        self.qgis_utils.get_layers(db, layers, load=True)
        if not layers:
            return None

        if layers[db.names.OP_RIGHT_OF_WAY_T][LAYER].featureCount() == 0:
            self.log_message(QCoreApplication.translate("QualityUtils",
                             "There are no Right of Way features to check 'Right of Way should not overlap buildings'."), Qgis.Info)

        elif layers[db.names.OP_BUILDING_T][LAYER].featureCount() == 0:
            self.log_message(QCoreApplication.translate("QualityUtils",
                             "There are no buildings to check 'Right of Way should not overlap buildings'."), Qgis.Info)

        else:
            error_layer = QgsVectorLayer("MultiPolygon?crs={}".format(layers[db.names.OP_BUILDING_T][LAYER].sourceCrs().authid()),
                                         translated_strings[CHECK_RIGHT_OF_WAY_OVERLAPS_BUILDINGS],
                                         "memory")
            data_provider = error_layer.dataProvider()
            data_provider.addAttributes([QgsField("right_of_way_id", QVariant.Int)])
            data_provider.addAttributes([QgsField("building_id", QVariant.Int)])
            error_layer.updateFields()

            ids, overlapping_polygons = self.qgis_utils.geometry.get_inner_intersections_between_polygons(layers[db.names.OP_RIGHT_OF_WAY_T][LAYER], layers[db.names.OP_BUILDING_T][LAYER])

            if overlapping_polygons is not None:
                new_features = list()
                for key, polygon in zip(ids, overlapping_polygons.asGeometryCollection()):
                    new_feature = QgsVectorLayerUtils().createFeature(error_layer, polygon, {0: key[0], 1: key[1]}) # right_of_way_id, building_id
                    new_features.append(new_feature)

                data_provider.addFeatures(new_features)

            if error_layer.featureCount() > 0:
                added_layer = self.add_error_layer(error_layer)

                self.log_message(QCoreApplication.translate("QualityUtils",
                                 "A memory layer with {} Right of Way-Building overlaps has been added to the map!").format(
                                 added_layer.featureCount()))
            else:
                self.log_message(QCoreApplication.translate("QualityUtils",
                                 "There are no Right of Way-Building overlaps."), Qgis.Success)

    @_log_quality_checks
    def check_gaps_in_plots(self, db, rule_name, translated_strings):
        use_roads = bool(QSettings().value('Asistente-LADM_COL/quality/use_roads', DEFAULT_USE_ROADS_VALUE, bool))
        plot_layer = self.qgis_utils.get_layer(db, db.names.OP_PLOT_T, QgsWkbTypes.PolygonGeometry, True)
        if not plot_layer:
            return

        if plot_layer.featureCount() == 0:
            self.log_message(QCoreApplication.translate("QualityUtils",
                             "There are no Plot features to check 'Plot should not have gaps'."), Qgis.Info)

        else:
            error_layer = QgsVectorLayer("MultiPolygon?crs={}".format(plot_layer.sourceCrs().authid()),
                                         translated_strings[CHECK_GAPS_IN_PLOTS],
                                         "memory")
            data_provider = error_layer.dataProvider()
            data_provider.addAttributes([QgsField("id", QVariant.Int)])
            error_layer.updateFields()

            gaps = self.qgis_utils.geometry.get_gaps_in_polygon_layer(plot_layer, use_roads)

            if gaps is not None:
                new_features = list()
                for geom, id in zip(gaps, range(0, len(gaps))):
                    feature = QgsVectorLayerUtils().createFeature(error_layer, geom, {0: id})
                    new_features.append(feature)

                data_provider.addFeatures(new_features)

            if error_layer.featureCount() > 0:
                added_layer = self.add_error_layer(error_layer)

                self.log_message(QCoreApplication.translate("QualityUtils",
                                 "A memory layer with {} gaps in layer Plots has been added to the map!").format(added_layer.featureCount()))

            else:
                self.log_message(QCoreApplication.translate("QualityUtils",
                                 "There are no gaps in layer Plot."), Qgis.Success)

    @_log_quality_checks
    def check_multiparts_in_right_of_way(self, db, rule_name, translated_strings):
        right_of_way_layer = self.qgis_utils.get_layer(db, db.names.OP_RIGHT_OF_WAY_T, QgsWkbTypes.PolygonGeometry, True)
        if not right_of_way_layer:
            return

        if right_of_way_layer.featureCount() == 0:
            self.log_message(QCoreApplication.translate("QualityUtils",
                             "There are no Right Of Way features to check 'Right Of Way should not have Multipart geometries'."), Qgis.Info)

        else:
            error_layer = QgsVectorLayer("Polygon?crs={}".format(right_of_way_layer.sourceCrs().authid()),
                                         translated_strings[CHECK_MULTIPART_IN_RIGHT_OF_WAY],
                                         "memory")
            data_provider = error_layer.dataProvider()
            data_provider.addAttributes([QgsField("original_id", QVariant.Int)])
            error_layer.updateFields()

            multi_parts, ids = self.qgis_utils.geometry.get_multipart_geoms(right_of_way_layer)

            if multi_parts is not None:
                new_features = list()
                for geom, id in zip(multi_parts, ids):
                    feature = QgsVectorLayerUtils().createFeature(error_layer, geom, {0: id})
                    new_features.append(feature)

                data_provider.addFeatures(new_features)

            if error_layer.featureCount() > 0:
                added_layer = self.add_error_layer(error_layer)

                self.log_message(QCoreApplication.translate("QualityUtils",
                                 "A memory layer with {} multipart geometries in layer Right Of Way has been added to the map!").format(
                                 added_layer.featureCount()))

            else:
                self.log_message(QCoreApplication.translate("QualityUtils",
                                 "There are no multipart geometries in layer Right Of Way."), Qgis.Success)

    @_log_quality_checks
    def check_parcel_right_relationship(self, db, rule_name, translated_strings):
        table_name = QCoreApplication.translate("LogicChecksConfigStrings", "Logic Consistency Errors in table '{}'").format(db.names.OP_PARCEL_T)
        error_layer = None
        error_layer_exist = False

        # Check if error layer exist
        group = self.qgis_utils.get_error_layers_group()

        # Check if layer is loaded
        layers = group.findLayers()
        for layer in layers:
            if layer.name() == table_name:
                error_layer = layer.layer()
                error_layer_exist = True
                break

        errors_count, error_layer = self.logic.get_parcel_right_relationship_errors(db, error_layer, table_name, translated_strings)

        if errors_count > 0:
            if error_layer_exist is False:
                added_layer = self.add_error_layer(error_layer)
            else:
                added_layer = error_layer

            self.log_message(QCoreApplication.translate("QualityUtils",
                             "A memory layer with {} parcel errors has been added to the map!").format(added_layer.featureCount()))

        else:
            self.log_message(QCoreApplication.translate("QualityUtils",
                             "Parcel-Right relationships are correct!"), Qgis.Success)

    @_log_quality_checks
    def check_fraction_sum_for_party_groups(self, db, rule_name):
        error_layer = None
        error_layer = self.logic.get_fractions_which_sum_is_not_one(db, error_layer)

        if error_layer.featureCount() > 0:
            added_layer = self.add_error_layer(error_layer)

            self.log_message(QCoreApplication.translate("QualityUtils",
                             "A memory layer with {} fractions which do not sum 1 has been added to the map!").format(
                             added_layer.featureCount()))
        else:
            self.log_message(QCoreApplication.translate("QualityUtils",
                             "Group Party Fractions are correct!"), Qgis.Success)

    def get_dangle_ids(self, boundary_layer):
        # 1. Run extract specific vertices
        # 2. Call to get_overlapping_points
        # 3. Obtain dangle ids (those not present in overlapping points result)
        res = processing.run("qgis:extractspecificvertices", {
                'INPUT': boundary_layer,
                'VERTICES': '0,-1', # First and last
                'OUTPUT': 'memory:'
            },
            feedback=QgsProcessingFeedback()
        )
        end_points = res['OUTPUT']

        end_point_ids = [point.id() for point in end_points.getFeatures()]
        overlapping_points = self.qgis_utils.geometry.get_overlapping_points(end_points)

        # Unpack list of lists into single list
        overlapping_point_ids = [item for sublist in overlapping_points for item in sublist]

        return (end_points, list(set(end_point_ids) - set(overlapping_point_ids)))

    def add_error_layer(self, error_layer):
        group = self.qgis_utils.get_error_layers_group()

        # Check if layer is loaded and remove it
        layers = group.findLayers()
        for layer in layers:
            if layer.name() == error_layer.name():
                group.removeLayer(layer.layer())
                break

        added_layer = QgsProject.instance().addMapLayer(error_layer, False)
        index = self.qgis_model_baker_utils.get_suggested_index_for_layer(added_layer, group)
        added_layer = group.insertLayer(index, added_layer).layer()
        if added_layer.isSpatial():
            # db connection is none because we are using a memory layer
            self.qgis_utils.symbology.set_layer_style_from_qml(None, added_layer, is_error_layer=True)
        return added_layer

    @_log_quality_checks
    def find_duplicate_records_in_a_table(self, db, rule_name):
        logic_consistency_tables = db.names.get_logic_consistency_tables()
        for table in logic_consistency_tables:
            fields = logic_consistency_tables[table]

            error_layer = None
            error_layer = self.logic.get_duplicate_records_in_a_table(db, table, fields, error_layer, db.names.T_ID_F)

            if error_layer.featureCount() > 0:
                added_layer = self.add_error_layer(error_layer)

                self.log_message(QCoreApplication.translate("QualityUtils",
                                 "A memory layer with {error_count} duplicate records from {table} has been added to the map!").format(error_count=added_layer.featureCount(), table=table))

            else:
                self.log_message(QCoreApplication.translate("QualityUtils",
                                 "There are no repeated records in {table}!").format(table=table), Qgis.Success)

    @_log_quality_checks
    def basic_logic_validations(self, db, rule, rule_name):
        logic_validation_queries = db.get_logic_validation_queries()
        query = logic_validation_queries[rule]['query']
        table_name = logic_validation_queries[rule]['table_name']
        table = logic_validation_queries[rule]['table']
        desc_error = logic_validation_queries[rule]['desc_error']

        error_layer = None
        error_layer_exist = False

        # Check if error layer exist
        group = self.qgis_utils.get_error_layers_group()

        # Check if layer is loaded
        layers = group.findLayers()
        for layer in layers:
            if layer.name() == table_name:
                error_layer = layer.layer()
                error_layer_exist = True
                break

        if error_layer_exist is False:
            error_layer = QgsVectorLayer("NoGeometry", table_name, "memory")
            pr = error_layer.dataProvider()
            pr.addAttributes([QgsField(QCoreApplication.translate("QualityConfigStrings", "{table}_id").format(table=table), QVariant.Int),
                              QgsField(QCoreApplication.translate("QualityConfigStrings", "error_type"), QVariant.String)])
            error_layer.updateFields()

        records = db.execute_sql_query(query)

        new_features = []
        for record in records:
            new_feature = QgsVectorLayerUtils().createFeature(error_layer,QgsGeometry(), {0: record[db.names.T_ID_F], 1:desc_error})
            new_features.append(new_feature)

        error_layer.dataProvider().addFeatures(new_features)

        if len(new_features) > 0:
            if error_layer_exist is False:
                added_layer = self.add_error_layer(error_layer)
            else:
                added_layer = error_layer

            self.log_message(QCoreApplication.translate("QualityUtils",
                             "A memory layer with {error_count} error record(s) from {table} has been added to the map!").format(error_count=len(new_features), table=table))

        else:
            self.log_message(QCoreApplication.translate("QualityUtils",
                             "No errors found when checking '{rule}' for '{table}'!").format(rule=logic_validation_queries[rule]['desc_error'], table=table), Qgis.Success)

    @_log_quality_checks
    def advanced_logic_validations(self, db, rule, rule_name):
        logic_validation_queries = db.get_logic_validation_queries()
        table_name = logic_validation_queries[rule]['table_name']
        table = logic_validation_queries[rule]['table']

        error_layer = None
        error_layer_exist = False

        # Check if error layer exist
        group = self.qgis_utils.get_error_layers_group()

        # Check if layer is loaded
        layers = group.findLayers()
        for layer in layers:
            if layer.name() == table_name:
                error_layer = layer.layer()
                error_layer_exist = True
                break

        if rule == 'COL_PARTY_TYPE_NATURAL_VALIDATION':
            errors_count, error_layer = self.logic.col_party_type_natural_validation(db, rule, error_layer)
        elif rule == 'COL_PARTY_TYPE_NO_NATURAL_VALIDATION':
            errors_count, error_layer = self.logic.col_party_type_no_natural_validation(db, rule, error_layer)
        elif rule == 'PARCEL_TYPE_AND_22_POSITION_OF_PARCEL_NUMBER_VALIDATION':
            errors_count, error_layer = self.logic.parcel_type_and_22_position_of_parcel_number_validation(db, rule, error_layer)
        elif rule == 'UEBAUNIT_PARCEL_VALIDATION':
            errors_count, error_layer = self.logic.uebaunit_parcel_validation(db, rule, error_layer)

        if errors_count > 0:
            if error_layer_exist is False:
                added_layer = self.add_error_layer(error_layer)
            else:
                added_layer = error_layer

            self.log_message(QCoreApplication.translate("QualityUtils", "A memory layer with {error_count} error record(s) from {table} has been added to the map!").format(
                    error_count=errors_count, table=table))
        else:
            self.log_message(QCoreApplication.translate("QualityUtils",
                             "No errors found when checking '{rule}' for '{table}'!").format(rule=logic_validation_queries[rule]['desc_error'], table=table), Qgis.Success)

    @_log_quality_checks
    def check_building_within_plots(self, db, rule_name, translated_strings):
        layers = {
            db.names.OP_BUILDING_T: {'name': db.names.OP_BUILDING_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            db.names.OP_PLOT_T: {'name': db.names.OP_PLOT_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None}
        }
        self.qgis_utils.get_layers(db, layers, load=True)
        if not layers:
            return None

        if layers[db.names.OP_BUILDING_T][LAYER].featureCount() == 0:
            self.log_message(QCoreApplication.translate("QualityUtils",
                             "There are no buildings to check 'Building should be within Plots'."), Qgis.Info)

        else:  
            error_layer = QgsVectorLayer("MultiPolygon?crs={}".format(layers[db.names.OP_BUILDING_T][LAYER].sourceCrs().authid()),
                                        translated_strings[CHECK_BUILDING_WITHIN_PLOTS],
                                        "memory")
            data_provider = error_layer.dataProvider()
            data_provider.addAttributes([QgsField('building_id', QVariant.Int),
                                        QgsField('error_type', QVariant.String)])

            error_layer.updateFields()

            buildings_with_no_plot, buildings_not_within_plot = self.qgis_utils.geometry.get_buildings_out_of_plots(layers[db.names.OP_BUILDING_T][LAYER], layers[db.names.OP_PLOT_T][LAYER], db.names.T_ID_F)

            new_features = list()
            for building_with_no_plot in buildings_with_no_plot:
                new_feature = QgsVectorLayerUtils().createFeature(
                                error_layer,
                                building_with_no_plot.geometry(),
                                {0: building_with_no_plot[db.names.T_ID_F],
                                1: translated_strings[ERROR_BUILDING_IS_NOT_OVER_A_PLOT]})
                new_features.append(new_feature)

            for building_not_within_plot in buildings_not_within_plot:
                new_feature = QgsVectorLayerUtils().createFeature(
                                error_layer,
                                building_not_within_plot.geometry(),
                                {0: building_not_within_plot[db.names.T_ID_F],
                                1: translated_strings[ERROR_BUILDING_CROSSES_A_PLOT_LIMIT]})
                new_features.append(new_feature)

            data_provider.addFeatures(new_features)

            if error_layer.featureCount() > 0:
                added_layer = self.add_error_layer(error_layer)

                self.log_message(QCoreApplication.translate("QualityUtils",
                                 "A memory layer with {} buildings not within a plot has been added to the map!").format(added_layer.featureCount()))

            else:
                self.log_message(QCoreApplication.translate("QualityUtils",
                                 "All buildings are within a plot."), Qgis.Success)

    @_log_quality_checks
    def check_building_unit_within_plots(self, db, rule_name, translated_strings):
        layers = {
            db.names.OP_BUILDING_UNIT_T: {'name': db.names.OP_BUILDING_UNIT_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            db.names.OP_PLOT_T: {'name': db.names.OP_PLOT_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None}
        }

        self.qgis_utils.get_layers(db, layers, load=True)
        if not layers:
            return None

        if layers[db.names.OP_BUILDING_UNIT_T][LAYER].featureCount() == 0:
            self.log_message(QCoreApplication.translate("QualityUtils",
                             "There are no buildings to check 'Building should be within Plots'."), Qgis.Info)

        else:  
            error_layer = QgsVectorLayer("MultiPolygon?crs={}".format(layers[db.names.OP_BUILDING_UNIT_T][LAYER].sourceCrs().authid()),
                                        translated_strings[CHECK_BUILDING_UNIT_WITHIN_PLOTS],
                                        "memory")
            data_provider = error_layer.dataProvider()
            data_provider.addAttributes([QgsField('building_unit_id', QVariant.Int),
                                        QgsField('error_type', QVariant.String)])

            error_layer.updateFields()

            building_units_with_no_plot, building_units_not_within_plot = self.qgis_utils.geometry.get_buildings_out_of_plots(layers[db.names.OP_BUILDING_UNIT_T][LAYER], layers[db.names.OP_PLOT_T][LAYER], db.names.T_ID_F)

            new_features = list()
            for building_unit_with_no_plot in building_units_with_no_plot:
                new_feature = QgsVectorLayerUtils().createFeature(
                                error_layer,
                                building_unit_with_no_plot.geometry(),
                                {0: building_unit_with_no_plot[db.names.T_ID_F],
                                1: translated_strings[ERROR_BUILDING_UNIT_IS_NOT_OVER_A_PLOT]})
                new_features.append(new_feature)

            for building_unit_not_within_plot in building_units_not_within_plot:
                new_feature = QgsVectorLayerUtils().createFeature(
                                error_layer,
                                building_unit_not_within_plot.geometry(),
                                {0: building_unit_not_within_plot[db.names.T_ID_F],
                                1: translated_strings[ERROR_BUILDING_UNIT_CROSSES_A_PLOT_LIMIT]})
                new_features.append(new_feature)

            data_provider.addFeatures(new_features)

            if error_layer.featureCount() > 0:
                added_layer = self.add_error_layer(error_layer)

                self.log_message(QCoreApplication.translate("QualityUtils",
                                 "A memory layer with {} building units not within a plot has been added to the map!").format(added_layer.featureCount()))
            else:
                self.log_message(QCoreApplication.translate("QualityUtils",
                                 "All building units are within a plot."), Qgis.Success)
