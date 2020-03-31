import processing
from qgis.PyQt.QtCore import (QCoreApplication,
                              QVariant)
from qgis.core import (Qgis,
                       QgsField,
                       QgsProcessingFeedback,
                       QgsVectorLayer,
                       QgsVectorLayerUtils,
                       QgsWkbTypes,
                       QgsFeatureRequest,
                       NULL)

from asistente_ladm_col.config.enums import EnumQualityRule
from asistente_ladm_col.config.translation_strings import (ERROR_BOUNDARY_IS_NOT_COVERED_BY_PLOT,
                                                           ERROR_NO_MORE_BOUNDARY_FACE_STRING_TABLE,
                                                           ERROR_DUPLICATE_MORE_BOUNDARY_FACE_STRING_TABLE,
                                                           ERROR_NO_LESS_TABLE,
                                                           ERROR_DUPLICATE_LESS_TABLE,
                                                           ERROR_NO_FOUND_POINT_BFS,
                                                           ERROR_DUPLICATE_POINT_BFS,
                                                           ERROR_BOUNDARY_NODE_IS_NOT_COVERED_BY_BOUNDARY_POINT)
from asistente_ladm_col.logic.quality.utils_quality_rules import UtilsQualityRules
from asistente_ladm_col.lib.logger import Logger


class LineQualityRules:
    def __init__(self, qgis_utils, translated_strings):
        self.translated_strings = translated_strings
        self.qgis_utils = qgis_utils
        self.logger = Logger()

    def check_overlaps_in_boundaries(self, db):
        boundary_layer = self.qgis_utils.get_layer(db, db.names.OP_BOUNDARY_T, load=True)
        if not boundary_layer:
            return

        if boundary_layer:
            overlapping = self.qgis_utils.geometry.get_overlapping_lines(boundary_layer)
            if overlapping is None:
                return (QCoreApplication.translate("LineQualityRules",
                                 "There are no boundaries to check for overlaps!"), Qgis.Info)

            else:
                error_point_layer = overlapping['native:saveselectedfeatures_3:Intersected_Points']
                error_line_layer = overlapping['native:saveselectedfeatures_2:Intersected_Lines']
                if type(error_point_layer) is QgsVectorLayer:
                    error_point_layer.setName("{} (point intersections)".format(
                        self.translated_strings[EnumQualityRule.Line.OVERLAPS_IN_BOUNDARIES]
                    ))
                if type(error_line_layer) is QgsVectorLayer:
                    error_line_layer.setName("{} (line intersections)".format(
                        self.translated_strings[EnumQualityRule.Line.OVERLAPS_IN_BOUNDARIES]
                    ))

                if (type(error_point_layer) is not QgsVectorLayer and
                    type(error_line_layer) is not QgsVectorLayer) or \
                   (error_point_layer.featureCount() == 0 and
                    error_line_layer.featureCount() == 0):

                    return (QCoreApplication.translate("LineQualityRules",
                                     "There are no overlapping boundaries."), Qgis.Success)

                else:
                    msg = ''

                    if type(error_point_layer) is QgsVectorLayer and error_point_layer.featureCount() > 0:
                        added_point_layer = UtilsQualityRules.add_error_layer(db, self.qgis_utils, error_point_layer)
                        msg = QCoreApplication.translate("LineQualityRules",
                            "A memory layer with {} overlapping boundaries (point intersections) has been added to the map.").format(added_point_layer.featureCount())

                    if type(error_line_layer) is QgsVectorLayer and error_line_layer.featureCount() > 0:
                        added_line_layer = UtilsQualityRules.add_error_layer(db, self.qgis_utils, error_line_layer)
                        msg = QCoreApplication.translate("LineQualityRules",
                            "A memory layer with {} overlapping boundaries (line intersections) has been added to the map.").format(added_line_layer.featureCount())

                    if type(error_point_layer) is QgsVectorLayer and \
                       type(error_line_layer) is QgsVectorLayer and \
                       error_point_layer.featureCount() > 0 and \
                       error_line_layer.featureCount() > 0:
                        msg = QCoreApplication.translate("LineQualityRules",
                            "Two memory layers with overlapping boundaries ({} point intersections and {} line intersections) have been added to the map.").format(added_point_layer.featureCount(), added_line_layer.featureCount())

                    return (msg, Qgis.Critical)

    def check_boundaries_are_not_split(self, db):
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
            return (QCoreApplication.translate("LineQualityRules",
                             "There are no boundaries to check 'boundaries should not be split'!"), Qgis.Info)

        else:
            wrong_boundaries = self.qgis_utils.geometry.get_boundaries_connected_to_single_boundary(db.names, boundary_layer)

            if wrong_boundaries is None:
                return (QCoreApplication.translate("LineQualityRules",
                                 "There are no wrong boundaries!"), Qgis.Success)
            else:
                error_layer = QgsVectorLayer("LineString?crs={}".format(boundary_layer.sourceCrs().authid()),
                                             self.translated_strings[EnumQualityRule.Line.BOUNDARIES_ARE_NOT_SPLIT],
                                "memory")
                pr = error_layer.dataProvider()
                pr.addAttributes([QgsField("id_lindero", QVariant.Int)])
                error_layer.updateFields()

                for feature in wrong_boundaries:
                    new_feature = QgsVectorLayerUtils().createFeature(error_layer, feature.geometry(),
                                                                      {0: feature[db.names.T_ID_F]})
                    features.append(new_feature)

                error_layer.dataProvider().addFeatures(features)
                if error_layer.featureCount() > 0:
                    added_layer = UtilsQualityRules.add_error_layer(db, self.qgis_utils, error_layer)
                    return (QCoreApplication.translate("LineQualityRules",
                                     "A memory layer with {} wrong boundaries has been added to the map!").format(added_layer.featureCount()), Qgis.Critical)
                else:
                    return (QCoreApplication.translate("LineQualityRules",
                                     "There are no wrong boundaries."), Qgis.Success)

    def check_boundaries_covered_by_plots(self, db):
        # read data
        layers = {
            db.names.OP_PLOT_T: None,
            db.names.OP_BOUNDARY_T: None,
            db.names.LESS_BFS_T: None,
            db.names.MORE_BFS_T: None
        }

        self.qgis_utils.get_layers(db, layers, load=True)
        if not layers:
            return None

        # validate data
        if layers[db.names.OP_BOUNDARY_T].featureCount() == 0:
            return (QCoreApplication.translate("LineQualityRules",
                             "There are no boundaries to check 'boundaries should be covered by plots'."), Qgis.Info)
        else:
            error_layer = QgsVectorLayer("MultiLineString?crs={}".format(layers[db.names.OP_BOUNDARY_T].sourceCrs().authid()),
                                         self.translated_strings[EnumQualityRule.Line.BOUNDARIES_COVERED_BY_PLOTS],
                                         "memory")

            data_provider = error_layer.dataProvider()
            data_provider.addAttributes([QgsField('id_terreno', QVariant.Int),
                                         QgsField('id_lindero', QVariant.Int),
                                         QgsField('tipo_de_error', QVariant.String)])
            error_layer.updateFields()

            features = self.get_boundary_features_not_covered_by_plots(db,
                                                                       layers[db.names.OP_PLOT_T],
                                                                       layers[db.names.OP_BOUNDARY_T],
                                                                       layers[db.names.MORE_BFS_T],
                                                                       layers[db.names.LESS_BFS_T],
                                                                       error_layer,
                                                                       db.names.T_ID_F)

            if features:
                error_layer.dataProvider().addFeatures(features)
                added_layer = UtilsQualityRules.add_error_layer(db, self.qgis_utils, error_layer)

                return (QCoreApplication.translate("LineQualityRules",
                                 "A memory layer with {} boundaries not covered by plots has been added to the map!").format(added_layer.featureCount()), Qgis.Critical)

            else:
                return (QCoreApplication.translate("LineQualityRules",
                                 "All boundaries are covered by plots!"), Qgis.Success)

    def check_boundary_nodes_covered_by_boundary_points(self, db):
        layers = {
            db.names.OP_BOUNDARY_POINT_T: None,
            db.names.POINT_BFS_T: None,
            db.names.OP_BOUNDARY_T: None
        }

        self.qgis_utils.get_layers(db, layers, load=True)
        if not layers:
            return None

        elif layers[db.names.OP_BOUNDARY_T].featureCount() == 0:
            return (QCoreApplication.translate("LineQualityRules",
                             "There are no boundaries to check 'missing boundary points in boundaries'."), Qgis.Info)
        else:
            error_layer = QgsVectorLayer("Point?crs={}".format(layers[db.names.OP_BOUNDARY_T].sourceCrs().authid()),
                                         self.translated_strings[EnumQualityRule.Line.BOUNDARY_NODES_COVERED_BY_BOUNDARY_POINTS],
                                         "memory")
            data_provider = error_layer.dataProvider()
            data_provider.addAttributes([QgsField('id_punto_lindero', QVariant.Int),
                                         QgsField('id_lindero', QVariant.Int),
                                         QgsField('tipo_de_error', QVariant.String)])

            error_layer.updateFields()

            features = self.get_boundary_nodes_features_not_covered_by_boundary_points(db, layers[db.names.OP_BOUNDARY_POINT_T], layers[db.names.OP_BOUNDARY_T], layers[db.names.POINT_BFS_T], error_layer, db.names.T_ID_F)
            data_provider.addFeatures(features)

            if error_layer.featureCount() > 0:
                added_layer = UtilsQualityRules.add_error_layer(db, self.qgis_utils, error_layer)

                return (QCoreApplication.translate("LineQualityRules",
                    "A memory layer with {} boundary vertices with no associated boundary points or with boundary points wrongly registered in the PointBFS table been added to the map!").format(added_layer.featureCount()), Qgis.Critical)

            else:
                return (QCoreApplication.translate("LineQualityRules",
                                 "There are no missing boundary points in boundaries."), Qgis.Success)

    def check_dangles_in_boundaries(self, db):
        boundary_layer = self.qgis_utils.get_layer(db, db.names.OP_BOUNDARY_T, load=True)
        if not boundary_layer:
            return

        if boundary_layer.featureCount() == 0:
            return (QCoreApplication.translate("LineQualityRules",
                             "There are no boundaries to check for dangles."), Qgis.Info)

        else:
            error_layer = QgsVectorLayer("Point?crs={}".format(boundary_layer.sourceCrs().authid()),
                                         self.translated_strings[EnumQualityRule.Line.DANGLES_IN_BOUNDARIES],
                                "memory")
            pr = error_layer.dataProvider()
            pr.addAttributes([QgsField("id_lindero", QVariant.Int)])
            error_layer.updateFields()

            end_points, dangle_ids = self.get_dangle_ids(boundary_layer)

            new_features = []
            for dangle in end_points.getFeatures(dangle_ids):
                new_feature = QgsVectorLayerUtils().createFeature(end_points, dangle.geometry(), {0: dangle[db.names.T_ID_F]})
                new_features.append(new_feature)

            error_layer.dataProvider().addFeatures(new_features)

            if error_layer.featureCount() > 0:
                added_layer = UtilsQualityRules.add_error_layer(db, self.qgis_utils, error_layer)

                return (QCoreApplication.translate("LineQualityRules",
                                 "A memory layer with {} boundary dangles has been added to the map!").format(added_layer.featureCount()), Qgis.Critical)

            else:
                return (QCoreApplication.translate("LineQualityRules",
                                 "Boundaries have no dangles!"), Qgis.Success)

    # UTILS METHODS

    def get_boundary_nodes_features_not_covered_by_boundary_points(self, db, boundary_point_layer, boundary_layer, point_bfs_layer, error_layer, id_field):
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
                                                                  {0: None,  1: boundary_id, 2: self.translated_strings[ERROR_BOUNDARY_NODE_IS_NOT_COVERED_BY_BOUNDARY_POINT]})
                features.append(new_feature)

        # Duplicate in point_bfs
        if duplicate_in_point_bfs is not None:
            for error_duplicate in set(duplicate_in_point_bfs):
                boundary_point_id = error_duplicate[0]
                boundary_node_id = error_duplicate[1]
                boundary_node_geom = dict_boundary_nodes[boundary_node_id].geometry()
                boundary_id = dict_boundary_nodes[boundary_node_id][id_field]  # get boundary id
                new_feature = QgsVectorLayerUtils().createFeature(error_layer, boundary_node_geom,
                                                                  {0: boundary_point_id, 1: boundary_id, 2: self.translated_strings[ERROR_DUPLICATE_POINT_BFS]})
                features.append(new_feature)

        # No registered in point_bfs
        if no_register_point_bfs is not None:
            for error_no_register in set(no_register_point_bfs):
                boundary_point_id = error_no_register[0]
                boundary_node_id = error_no_register[1]
                boundary_node_geom = dict_boundary_nodes[boundary_node_id].geometry()
                boundary_id = dict_boundary_nodes[boundary_node_id][id_field]  # get boundary id
                new_feature = QgsVectorLayerUtils().createFeature(error_layer, boundary_node_geom,
                                                                  {0: boundary_point_id, 1: boundary_id, 2: self.translated_strings[ERROR_NO_FOUND_POINT_BFS]})
                features.append(new_feature)

        return features

    def get_boundary_features_not_covered_by_plots(self, db, plot_layer, boundary_layer, more_bfs_layer, less_layer, error_layer, id_field):
        """
        Return all boundary features that have errors when checking if they are covered by plots.
        This takes into account both geometric and alphanumeric (topology table) errors.
        """
        type_tplg_error = {0: self.translated_strings[ERROR_BOUNDARY_IS_NOT_COVERED_BY_PLOT],
                           1: self.translated_strings[ERROR_NO_MORE_BOUNDARY_FACE_STRING_TABLE],
                           2: self.translated_strings[ERROR_DUPLICATE_MORE_BOUNDARY_FACE_STRING_TABLE],
                           3: self.translated_strings[ERROR_NO_LESS_TABLE],
                           4: self.translated_strings[ERROR_DUPLICATE_LESS_TABLE]}

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

        tmp_inner_rings_layer = self.qgis_utils.geometry.get_inner_rings_layer(db.names, plot_layer, db.names.T_ID_F)
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

        errors_boundary_plot_diffs = self.qgis_utils.geometry.difference_boundary_plot(db.names, boundary_layer, plot_as_lines_layer, db.names.T_ID_F)
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
