import processing
from qgis.PyQt.QtCore import (QCoreApplication,
                              QVariant)
from qgis.core import (Qgis,
                       QgsField,
                       QgsGeometry,
                       QgsPointXY,
                       QgsProcessingFeedback,
                       QgsSpatialIndex,
                       QgsVectorLayer,
                       QgsVectorLayerUtils,
                       QgsFeatureRequest,
                       NULL,
                       QgsRectangle)

from asistente_ladm_col.config.general_config import (LAYER,
                                                      LAYER_NAME)
from asistente_ladm_col.config.enums import QualityRuleEnum
from asistente_ladm_col.config.translation_strings import (ERROR_NO_FOUND_POINT_BFS,
                                                           ERROR_DUPLICATE_POINT_BFS,
                                                           ERROR_BOUNDARY_POINT_IS_NOT_COVERED_BY_BOUNDARY_NODE)
from asistente_ladm_col.logic.quality.utils_quality_rules import UtilsQualityRules
from asistente_ladm_col.lib.logger import Logger


class PointQualityRules:
    def __init__(self, qgis_utils, translated_strings):
        self.translated_strings = translated_strings
        self.qgis_utils = qgis_utils
        self.logger = Logger()

    def check_overlapping_points(self, db, point_layer_name):
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
            return (QCoreApplication.translate("PointQualityRules",
                             "There are no points in layer '{}' to check for overlaps!").format(point_layer_name), Qgis.Info)

        else:
            error_layer_name = ''
            if point_layer_name == db.names.OP_BOUNDARY_POINT_T:
                error_layer_name = self.translated_strings[QualityRuleEnum.Point.OVERLAPS_IN_BOUNDARY_POINTS]
            elif point_layer_name == db.names.OP_CONTROL_POINT_T:
                error_layer_name = self.translated_strings[QualityRuleEnum.Point.OVERLAPS_IN_CONTROL_POINTS]

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
                added_layer = UtilsQualityRules.add_error_layer(db, self.qgis_utils, error_layer)
                return (QCoreApplication.translate("PointQualityRules",
                                                   "A memory layer with {} overlapping points in '{}' has been added to the map!").format(added_layer.featureCount(), point_layer_name),
                        Qgis.Critical)
            else:
                return (QCoreApplication.translate("PointQualityRules",
                                                   "There are no overlapping points in layer '{}'!").format(point_layer_name),
                        Qgis.Success)

    def check_boundary_points_covered_by_boundary_nodes(self, db):

        layers = {
            db.names.OP_BOUNDARY_T: {LAYER_NAME: db.names.OP_BOUNDARY_T, LAYER: None},
            db.names.POINT_BFS_T: {LAYER_NAME: db.names.POINT_BFS_T, LAYER: None},
            db.names.OP_BOUNDARY_POINT_T: {LAYER_NAME: db.names.OP_BOUNDARY_POINT_T, LAYER: None}
        }

        self.qgis_utils.get_layers(db, layers, load=True)
        if not layers:
            return None

        elif layers[db.names.OP_BOUNDARY_POINT_T][LAYER].featureCount() == 0:
            return (QCoreApplication.translate("PointQualityRules",
                             "There are no boundary points to check 'boundary points should be covered by boundary nodes'."), Qgis.Info)
        else:
            error_layer = QgsVectorLayer("Point?crs={}".format(layers[db.names.OP_BOUNDARY_POINT_T][LAYER].sourceCrs().authid()),
                                         self.translated_strings[QualityRuleEnum.Point.BOUNDARY_POINTS_COVERED_BY_PLOT_NODES],
                                         "memory")

            data_provider = error_layer.dataProvider()
            data_provider.addAttributes([QgsField('boundary_point_id', QVariant.Int),
                                         QgsField('boundary_id', QVariant.Int),
                                         QgsField('error_type', QVariant.String)])
            error_layer.updateFields()

            features = self.get_boundary_points_features_not_covered_by_boundary_nodes(db, layers[db.names.OP_BOUNDARY_POINT_T][LAYER], layers[db.names.OP_BOUNDARY_T][LAYER], layers[db.names.POINT_BFS_T][LAYER], error_layer, db.names.T_ID_F)
            error_layer.dataProvider().addFeatures(features)

            if error_layer.featureCount() > 0:
                added_layer = UtilsQualityRules.add_error_layer(db, self.qgis_utils, error_layer)

                return (QCoreApplication.translate(
                                 "PointQualityRules", "A memory layer with {} boundary points not covered by boundary nodes has been added to the map!")
                                 .format(added_layer.featureCount()), Qgis.Critical)

            else:
                return (QCoreApplication.translate("PointQualityRules",
                                 "All boundary points are covered by boundary nodes!"), Qgis.Success)

    def check_boundary_points_covered_by_plot_nodes(self, db):
        layers = {
            db.names.OP_PLOT_T: {LAYER_NAME: db.names.OP_PLOT_T, LAYER: None},
            db.names.OP_BOUNDARY_POINT_T: {LAYER_NAME: db.names.OP_BOUNDARY_POINT_T, LAYER: None}
        }

        self.qgis_utils.get_layers(db, layers, load=True)
        if not layers:
            return None

        if layers[db.names.OP_BOUNDARY_POINT_T][LAYER].featureCount() == 0:
            return (QCoreApplication.translate("PointQualityRules",
                             "There are no boundary points to check 'boundary points should be covered by Plot nodes'."), Qgis.Info)

        else:
            error_layer = QgsVectorLayer("Point?crs={}".format(layers[db.names.OP_BOUNDARY_POINT_T][LAYER].sourceCrs().authid()),
                                         self.translated_strings[QualityRuleEnum.Point.BOUNDARY_POINTS_COVERED_BY_PLOT_NODES],
                                         "memory")

            data_provider = error_layer.dataProvider()
            data_provider.addAttributes([QgsField('boundary_point_id', QVariant.Int)])
            error_layer.updateFields()

            topology_rule = 'boundary_points_covered_by_plot_nodes'
            features = UtilsQualityRules.get_boundary_points_features_not_covered_by_plot_nodes_and_viceversa(db, layers[db.names.OP_BOUNDARY_POINT_T][LAYER], layers[db.names.OP_PLOT_T][LAYER], error_layer, topology_rule, db.names.T_ID_F)
            error_layer.dataProvider().addFeatures(features)

            if error_layer.featureCount() > 0:
                added_layer = UtilsQualityRules.add_error_layer(db, self.qgis_utils, error_layer)

                return (QCoreApplication.translate("PointQualityRules",
                    "A memory layer with {} boundary points not covered by plot nodes has been added to the map!").format(added_layer.featureCount()), Qgis.Critical)

            else:
                return (QCoreApplication.translate("PointQualityRules",
                                 "All boundary points are covered by plot nodes!"), Qgis.Success)

    def check_missing_boundary_points_in_boundaries(self, db):
        """
        Not used anymore but kept for reference
        """
        layers = {
            db.names.OP_BOUNDARY_POINT_T: {LAYER_NAME: db.names.OP_BOUNDARY_POINT_T, LAYER: None},
            db.names.POINT_BFS_T: {LAYER_NAME: db.names.POINT_BFS_T, LAYER: None},
            db.names.OP_BOUNDARY_T: {LAYER_NAME: db.names.OP_BOUNDARY_T, LAYER: None}
        }

        self.qgis_utils.get_layers(db, layers, load=True)
        if not layers:
            return None

        if layers[db.names.OP_BOUNDARY_T][LAYER].featureCount() == 0:
            self.logger.info_msg(__name__, QCoreApplication.translate("PointQualityRules",
                                           "There are no boundaries to check 'missing boundary points in boundaries'."))
            return

        error_layer = QgsVectorLayer("Point?crs={}".format(layers[db.names.OP_BOUNDARY_T][LAYER].sourceCrs().authid()),
                                     self.translated_strings[QualityRuleEnum.Line.BOUNDARY_NODES_COVERED_BY_BOUNDARY_POINTS],
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
                        2: QCoreApplication.translate("PointQualityRules", "Missing boundary point in boundary")})
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
                         2: QCoreApplication.translate("PointQualityRules", "Relation found more than once in the PointBFS table")}))
            else:
                new_features.append(QgsVectorLayerUtils().createFeature(error_layer, point_selected.geometry(),
                    {0: boundary_point_id,
                     1: boundary_id,
                     2: QCoreApplication.translate("PointQualityRules", "Relation not found in the PointBFS table")}))
        data_provider.addFeatures(new_features)

        if error_layer.featureCount() > 0:
            added_layer = UtilsQualityRules.add_error_layer(db, self.qgis_utils, error_layer)

            self.logger.info_msg(__name__, QCoreApplication.translate("PointQualityRules",
                "A memory layer with {} boundary vertices with no associated boundary points or with boundary points wrongly registered in the PointBFS table been added to the map!").format(added_layer.featureCount()))
        else:
            self.logger.info_msg(__name__, QCoreApplication.translate("PointQualityRules",
                                           "There are no missing boundary points in boundaries."))

    def check_missing_survey_points_in_buildings(self, db):
        """
        Not used anymore but kept for reference.
        """
        layers = {
            db.names.OP_SURVEY_POINT_T: {LAYER_NAME: db.names.OP_SURVEY_POINT_T, LAYER: None},
            db.names.OP_BUILDING_T: {LAYER_NAME: db.names.OP_BUILDING_T, LAYER: None}
        }
        self.qgis_utils.get_layers(db, layers, load=True)
        if not layers:
            return None

        if layers[db.names.OP_BUILDING_T][LAYER].featureCount() == 0:
            self.logger.info_msg(__name__, QCoreApplication.translate("PointQualityRules",
                "There are no buildings to check 'missing survey points in buildings'."))
            return

        error_layer = QgsVectorLayer("Point?crs={}".format(layers[db.names.OP_BUILDING_T][LAYER].sourceCrs().authid()),
                                     QCoreApplication.translate("PointQualityRules", "Missing survey points in buildings"),
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
            added_layer = UtilsQualityRules.add_error_layer(db, self.qgis_utils, error_layer)

            self.logger.info_msg(__name__, QCoreApplication.translate("PointQualityRules",
                "A memory layer with {} building vertices with no associated survey points has been added to the map!").format(added_layer.featureCount()))
        else:
            self.logger.info_msg(__name__, QCoreApplication.translate("PointQualityRules",
                "There are no missing survey points in buildings."))

    # UTILS METHODS
    def get_boundary_points_features_not_covered_by_boundary_nodes(self, db, boundary_point_layer, boundary_layer, point_bfs_layer, error_layer, id_field):
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
                                                                   2: self.translated_strings[ERROR_BOUNDARY_POINT_IS_NOT_COVERED_BY_BOUNDARY_NODE]})
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
                                                                   2: self.translated_strings[ERROR_NO_FOUND_POINT_BFS]})
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
                                                                   2: self.translated_strings[ERROR_DUPLICATE_POINT_BFS]})
                features.append(new_feature)

        return features

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
