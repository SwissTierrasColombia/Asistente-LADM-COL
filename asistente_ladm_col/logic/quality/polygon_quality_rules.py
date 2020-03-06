import processing
from qgis.PyQt.QtCore import (QCoreApplication,
                              QVariant,
                              QSettings)
from qgis.core import (Qgis,
                       QgsField,
                       QgsVectorLayer,
                       QgsVectorLayerUtils,
                       QgsWkbTypes,
                       QgsFeatureRequest)

from asistente_ladm_col.config.general_config import (LAYER,
                                                      LAYER_NAME,
                                                      DEFAULT_USE_ROADS_VALUE)
from asistente_ladm_col.config.enums import QualityRuleEnum
from asistente_ladm_col.config.translation_strings import (ERROR_PLOT_IS_NOT_COVERED_BY_BOUNDARY,
                                                           ERROR_NO_MORE_BOUNDARY_FACE_STRING_TABLE,
                                                           ERROR_DUPLICATE_MORE_BOUNDARY_FACE_STRING_TABLE,
                                                           ERROR_NO_LESS_TABLE,
                                                           ERROR_DUPLICATE_LESS_TABLE,
                                                           ERROR_BUILDING_IS_NOT_OVER_A_PLOT,
                                                           ERROR_BUILDING_CROSSES_A_PLOT_LIMIT,
                                                           ERROR_BUILDING_UNIT_IS_NOT_OVER_A_PLOT,
                                                           ERROR_BUILDING_UNIT_CROSSES_A_PLOT_LIMIT)
from asistente_ladm_col.logic.quality.utils_quality_rules import UtilsQualityRules
from asistente_ladm_col.lib.logger import Logger


class PolygonQualityRules:
    def __init__(self, qgis_utils, translated_strings):
        self.translated_strings = translated_strings
        self.qgis_utils = qgis_utils
        self.logger = Logger()

    def check_overlapping_polygons(self, db, polygon_layer_name):
        polygon_layer = self.qgis_utils.get_layer(db, polygon_layer_name, load=True)
        if not polygon_layer:
            return

        if polygon_layer:
            error_layer_name = ''
            if polygon_layer_name == db.names.OP_PLOT_T:
                error_layer_name = self.translated_strings[QualityRuleEnum.Polygon.OVERLAPS_IN_PLOTS]
            elif polygon_layer_name == db.names.OP_BUILDING_T:
                error_layer_name = self.translated_strings[QualityRuleEnum.Polygon.OVERLAPS_IN_BUILDINGS]
            elif polygon_layer_name == db.names.OP_RIGHT_OF_WAY_T:
                error_layer_name = self.translated_strings[QualityRuleEnum.Polygon.OVERLAPS_IN_RIGHTS_OF_WAY]

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
                added_layer = UtilsQualityRules.add_error_layer(db, self.qgis_utils, error_layer)

                return (QCoreApplication.translate("PolygonQualityRules",
                                 "A memory layer with {} overlapping polygons in layer '{}' has been added to the map!").format(
                                 added_layer.featureCount(), polygon_layer_name), Qgis.Critical)

            else:
                return (QCoreApplication.translate("PolygonQualityRules",
                                 "There are no overlapping polygons in layer '{}'!").format(polygon_layer_name), Qgis.Success)

    def check_plots_covered_by_boundaries(self, db):
        # read data
        layers = {
            db.names.OP_PLOT_T: {LAYER_NAME: db.names.OP_PLOT_T, LAYER: None},
            db.names.OP_BOUNDARY_T: {LAYER_NAME: db.names.OP_BOUNDARY_T, LAYER: None},
            db.names.LESS_BFS_T: {LAYER_NAME: db.names.LESS_BFS_T, LAYER: None},
            db.names.MORE_BFS_T: {LAYER_NAME: db.names.MORE_BFS_T, LAYER: None}
        }
        self.qgis_utils.get_layers(db, layers, load=True)
        if not layers:
            return None

        if layers[db.names.OP_PLOT_T][LAYER].featureCount() == 0:
            return (QCoreApplication.translate("PolygonQualityRules",
                             "There are no plots to check 'plots should be covered by boundaries'."), Qgis.Info)
        else:
            error_layer = QgsVectorLayer("MultiLineString?crs={}".format(layers[db.names.OP_PLOT_T][LAYER].sourceCrs().authid()),
                                         self.translated_strings[QualityRuleEnum.Polygon.PLOTS_COVERED_BY_BOUNDARIES],
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
                                                                        db.names.T_ID_F)
            if features:
                error_layer.dataProvider().addFeatures(features)
                added_layer = UtilsQualityRules.add_error_layer(db, self.qgis_utils, error_layer)

                return (QCoreApplication.translate("PolygonQualityRules",
                                 "A memory layer with {} plots not covered by boundaries has been added to the map!").format(added_layer.featureCount()), Qgis.Critical)

            else:
                return (QCoreApplication.translate("PolygonQualityRules",
                                 "All plots are covered by boundaries!"), Qgis.Success)

    def check_right_of_way_overlaps_buildings(self, db):

        layers = {
            db.names.OP_RIGHT_OF_WAY_T: {LAYER_NAME: db.names.OP_RIGHT_OF_WAY_T, LAYER: None},
            db.names.OP_BUILDING_T: {LAYER_NAME: db.names.OP_BUILDING_T, LAYER: None}
        }

        self.qgis_utils.get_layers(db, layers, load=True)
        if not layers:
            return None

        if layers[db.names.OP_RIGHT_OF_WAY_T][LAYER].featureCount() == 0:
            return (QCoreApplication.translate("PolygonQualityRules",
                             "There are no Right of Way features to check 'Right of Way should not overlap buildings'."), Qgis.Info)

        elif layers[db.names.OP_BUILDING_T][LAYER].featureCount() == 0:
            return (QCoreApplication.translate("PolygonQualityRules",
                             "There are no buildings to check 'Right of Way should not overlap buildings'."), Qgis.Info)

        else:
            error_layer = QgsVectorLayer("MultiPolygon?crs={}".format(layers[db.names.OP_BUILDING_T][LAYER].sourceCrs().authid()),
                                         self.translated_strings[QualityRuleEnum.Polygon.RIGHT_OF_WAY_OVERLAPS_BUILDINGS],
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
                added_layer = UtilsQualityRules.add_error_layer(db, self.qgis_utils, error_layer)

                return (QCoreApplication.translate("PolygonQualityRules",
                                 "A memory layer with {} Right of Way-Building overlaps has been added to the map!").format(
                                 added_layer.featureCount()), Qgis.Critical)
            else:
                return (QCoreApplication.translate("PolygonQualityRules",
                                 "There are no Right of Way-Building overlaps."), Qgis.Success)

    def check_gaps_in_plots(self, db):
        use_roads = bool(QSettings().value('Asistente-LADM_COL/quality/use_roads', DEFAULT_USE_ROADS_VALUE, bool))
        plot_layer = self.qgis_utils.get_layer(db, db.names.OP_PLOT_T, True)
        if not plot_layer:
            return

        if plot_layer.featureCount() == 0:
            return (QCoreApplication.translate("PolygonQualityRules",
                             "There are no Plot features to check 'Plot should not have gaps'."), Qgis.Info)

        else:
            error_layer = QgsVectorLayer("MultiPolygon?crs={}".format(plot_layer.sourceCrs().authid()),
                                         self.translated_strings[QualityRuleEnum.Polygon.GAPS_IN_PLOTS],
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
                added_layer = UtilsQualityRules.add_error_layer(db, self.qgis_utils, error_layer)

                return (QCoreApplication.translate("PolygonQualityRules",
                                 "A memory layer with {} gaps in layer Plots has been added to the map!").format(added_layer.featureCount()), Qgis.Critical)

            else:
                return (QCoreApplication.translate("PolygonQualityRules",
                                 "There are no gaps in layer Plot."), Qgis.Success)

    def check_multiparts_in_right_of_way(self, db):
        right_of_way_layer = self.qgis_utils.get_layer(db, db.names.OP_RIGHT_OF_WAY_T, True)
        if not right_of_way_layer:
            return

        if right_of_way_layer.featureCount() == 0:
            return (QCoreApplication.translate("PolygonQualityRules",
                             "There are no Right Of Way features to check 'Right Of Way should not have Multipart geometries'."), Qgis.Info)

        else:
            error_layer = QgsVectorLayer("Polygon?crs={}".format(right_of_way_layer.sourceCrs().authid()),
                                         self.translated_strings[QualityRuleEnum.Polygon.MULTIPART_IN_RIGHT_OF_WAY],
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
                added_layer = UtilsQualityRules.add_error_layer(db, self.qgis_utils, error_layer)

                return (QCoreApplication.translate("PolygonQualityRules",
                                 "A memory layer with {} multipart geometries in layer Right Of Way has been added to the map!").format(
                                 added_layer.featureCount()), Qgis.Critical)

            else:
                return (QCoreApplication.translate("PolygonQualityRules",
                                 "There are no multipart geometries in layer Right Of Way."), Qgis.Success)

    def check_plot_nodes_covered_by_boundary_points(self, db):
        layers = {
            db.names.OP_PLOT_T: {LAYER_NAME: db.names.OP_PLOT_T, LAYER: None},
            db.names.OP_BOUNDARY_POINT_T: {LAYER_NAME: db.names.OP_BOUNDARY_POINT_T, LAYER: None}
        }
        self.qgis_utils.get_layers(db, layers, load=True)
        if not layers:
            return None

        if layers[db.names.OP_PLOT_T][LAYER].featureCount() == 0:
            return (QCoreApplication.translate("PolygonQualityRules",
                             "There are no plots to check 'Plots should be covered by boundary points'."), Qgis.Info)
        else:
            error_layer = QgsVectorLayer("Point?crs={}".format(layers[db.names.OP_PLOT_T][LAYER].sourceCrs().authid()),
                                         self.translated_strings[QualityRuleEnum.Polygon.PLOT_NODES_COVERED_BY_BOUNDARY_POINTS],
                                         "memory")

            data_provider = error_layer.dataProvider()
            data_provider.addAttributes([QgsField('plot_id', QVariant.Int)])
            error_layer.updateFields()

            topology_rule = 'plot_nodes_covered_by_boundary_points'
            features = UtilsQualityRules.get_boundary_points_features_not_covered_by_plot_nodes_and_viceversa(db, layers[db.names.OP_BOUNDARY_POINT_T][LAYER], layers[db.names.OP_PLOT_T][LAYER], error_layer, topology_rule, db.names.T_ID_F)
            error_layer.dataProvider().addFeatures(features)

            if error_layer.featureCount() > 0:
                added_layer = UtilsQualityRules.add_error_layer(db, self.qgis_utils, error_layer)
                return (QCoreApplication.translate(
                                 "PolygonQualityRules",
                                 "A memory layer with {} plot nodes not covered by boundary points has been added to the map!")
                                 .format(added_layer.featureCount()), Qgis.Critical)

            else:
                return (QCoreApplication.translate("PolygonQualityRules",
                                 "All plot nodes are covered by boundary points!"), Qgis.Success)

    def check_building_within_plots(self, db):
        layers = {
            db.names.OP_BUILDING_T: {LAYER_NAME: db.names.OP_BUILDING_T, LAYER: None},
            db.names.OP_PLOT_T: {LAYER_NAME: db.names.OP_PLOT_T, LAYER: None}
        }
        self.qgis_utils.get_layers(db, layers, load=True)
        if not layers:
            return None

        if layers[db.names.OP_BUILDING_T][LAYER].featureCount() == 0:
            return (QCoreApplication.translate("PolygonQualityRules",
                             "There are no buildings to check 'Building should be within Plots'."), Qgis.Info)

        else:
            error_layer = QgsVectorLayer("MultiPolygon?crs={}".format(layers[db.names.OP_BUILDING_T][LAYER].sourceCrs().authid()),
                                        self.translated_strings[QualityRuleEnum.Polygon.BUILDINGS_SHOULD_BE_WITHIN_PLOTS],
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
                                1: self.translated_strings[ERROR_BUILDING_IS_NOT_OVER_A_PLOT]})
                new_features.append(new_feature)

            for building_not_within_plot in buildings_not_within_plot:
                new_feature = QgsVectorLayerUtils().createFeature(
                                error_layer,
                                building_not_within_plot.geometry(),
                                {0: building_not_within_plot[db.names.T_ID_F],
                                1: self.translated_strings[ERROR_BUILDING_CROSSES_A_PLOT_LIMIT]})
                new_features.append(new_feature)

            data_provider.addFeatures(new_features)

            if error_layer.featureCount() > 0:
                added_layer = UtilsQualityRules.add_error_layer(db, self.qgis_utils, error_layer)

                return (QCoreApplication.translate("PolygonQualityRules",
                                 "A memory layer with {} buildings not within a plot has been added to the map!").format(added_layer.featureCount()), Qgis.Critical)

            else:
                return (QCoreApplication.translate("PolygonQualityRules",
                                 "All buildings are within a plot."), Qgis.Success)

    def check_building_unit_within_plots(self, db):
        layers = {
            db.names.OP_BUILDING_UNIT_T: {LAYER_NAME: db.names.OP_BUILDING_UNIT_T, LAYER: None},
            db.names.OP_PLOT_T: {LAYER_NAME: db.names.OP_PLOT_T, LAYER: None}
        }

        self.qgis_utils.get_layers(db, layers, load=True)
        if not layers:
            return None

        if layers[db.names.OP_BUILDING_UNIT_T][LAYER].featureCount() == 0:
            return (QCoreApplication.translate("PolygonQualityRules",
                             "There are no buildings to check 'Building should be within Plots'."), Qgis.Info)

        else:
            error_layer = QgsVectorLayer("MultiPolygon?crs={}".format(layers[db.names.OP_BUILDING_UNIT_T][LAYER].sourceCrs().authid()),
                                        self.translated_strings[QualityRuleEnum.Polygon.BUILDING_UNITS_SHOULD_BE_WITHIN_PLOTS],
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
                                1: self.translated_strings[ERROR_BUILDING_UNIT_IS_NOT_OVER_A_PLOT]})
                new_features.append(new_feature)

            for building_unit_not_within_plot in building_units_not_within_plot:
                new_feature = QgsVectorLayerUtils().createFeature(
                                error_layer,
                                building_unit_not_within_plot.geometry(),
                                {0: building_unit_not_within_plot[db.names.T_ID_F],
                                1: self.translated_strings[ERROR_BUILDING_UNIT_CROSSES_A_PLOT_LIMIT]})
                new_features.append(new_feature)

            data_provider.addFeatures(new_features)

            if error_layer.featureCount() > 0:
                added_layer = UtilsQualityRules.add_error_layer(db, self.qgis_utils, error_layer)

                return (QCoreApplication.translate("PolygonQualityRules",
                                 "A memory layer with {} building units not within a plot has been added to the map!").format(added_layer.featureCount()), Qgis.Critical)
            else:
                return (QCoreApplication.translate("PolygonQualityRules",
                                 "All building units are within a plot."), Qgis.Success)

    # UTILS METHODS
    def get_plot_features_not_covered_by_boundaries(self, db, plot_layer, boundary_layer, more_bfs_layer, less_layer, error_layer, id_field):
        """
        Returns all plot features that have errors when checking if they are covered by boundaries.
        That is both geometric and alphanumeric (topology table) errors.
        """
        type_tplg_error = {0: self.translated_strings[ERROR_PLOT_IS_NOT_COVERED_BY_BOUNDARY],
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

        errors_plot_boundary_diffs = self.qgis_utils.geometry.difference_plot_boundary(db.names, plot_as_lines_layer, boundary_layer, db.names.T_ID_F)
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