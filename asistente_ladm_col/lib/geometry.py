# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2018-04-16
        git sha              : :%H$
        copyright            : (C) 2018 by Germán Carrillo (BSF Swissphoto)
                               (C) 2018 by Leonardo Cardona (BSF Swissphoto)
        email                : gcarrillo@linuxmail.org
                               leocardonapiedrahita@gmail.com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""
import gc
from math import sqrt

from qgis.PyQt.QtCore import (QCoreApplication,
                              QObject,
                              QVariant)
from qgis.core import (QgsField,
                       QgsGeometry,
                       QgsPolygon,
                       QgsMultiPolygon,
                       QgsFeatureRequest,
                       QgsLineString,
                       QgsMultiLineString,
                       QgsProcessingFeedback,
                       QgsProcessingException,
                       QgsSpatialIndex,
                       QgsVectorLayer,
                       QgsVectorLayerEditUtils,
                       QgsVectorLayerUtils,
                       QgsWkbTypes,
                       edit,
                       QgsFeatureSource)

import processing

from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.lib.processing.custom_processing_feedback import CustomFeedbackWithErrors
from asistente_ladm_col.utils.crs_utils import get_crs_authid


class GeometryUtils(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.logger = Logger()

    def get_pair_boundary_plot(self, boundary_layer, plot_layer, id_field, use_selection=True):
        id_field_idx = plot_layer.fields().indexFromName(id_field)
        request = QgsFeatureRequest().setSubsetOfAttributes([id_field_idx])
        polygons = plot_layer.getSelectedFeatures(request) if use_selection else plot_layer.getFeatures(request)
        intersect_more_pairs = list()
        intersect_less_pairs = list()

        if boundary_layer.featureCount() == 0:
            return intersect_more_pairs, intersect_less_pairs

        id_field_idx = boundary_layer.fields().indexFromName(id_field)
        request = QgsFeatureRequest().setSubsetOfAttributes([id_field_idx])
        dict_features = {feature.id(): feature for feature in boundary_layer.getFeatures(request)}
        index = QgsSpatialIndex(boundary_layer)
        candidate_features = None

        for polygon in polygons:
            bbox = polygon.geometry().boundingBox()
            bbox.scale(1.001)
            candidates_ids = index.intersects(bbox)

            candidate_features = [dict_features[candidate_id] for candidate_id in candidates_ids]

            for candidate_feature in candidate_features:
                polygon_geom = polygon.geometry()
                is_multipart = polygon_geom.isMultipart()
                candidate_geometry = candidate_feature.geometry()

                if polygon_geom.intersects(candidate_geometry):
                    # Does the current multipolygon have inner rings?
                    has_inner_rings = False
                    multi_polygon = None
                    single_polygon = None

                    if is_multipart:
                        multi_polygon = polygon_geom.constGet()
                        for part in range(multi_polygon.numGeometries()):
                            if multi_polygon.ringCount(part) > 1:
                                has_inner_rings = True
                                break
                    else:
                        single_polygon = polygon_geom.constGet()
                        if single_polygon.numInteriorRings() > 0:
                            has_inner_rings = True

                    # Now we'll test intersections against borders
                    if has_inner_rings:
                        # In this case we need to identify whether the
                        # intersection is with outer rings (goes to MOREBFS
                        # table) or with inner rings (goes to LESS table)
                        multi_outer_rings = QgsMultiLineString()
                        multi_inner_rings = QgsMultiLineString()

                        if is_multipart and multi_polygon:
                            for i in range(multi_polygon.numGeometries()):
                                temp_polygon = multi_polygon.geometryN(i)
                                multi_outer_rings.addGeometry(temp_polygon.exteriorRing().clone())
                                for j in range(temp_polygon.numInteriorRings()):
                                    multi_inner_rings.addGeometry(temp_polygon.interiorRing(j).clone())

                        elif not is_multipart and single_polygon:
                            multi_outer_rings.addGeometry(single_polygon.exteriorRing().clone())
                            for j in range(single_polygon.numInteriorRings()):
                                multi_inner_rings.addGeometry(single_polygon.interiorRing(j).clone())

                        outer_intersection = QgsGeometry(multi_outer_rings).intersection(candidate_geometry)
                        if not outer_intersection.isEmpty():
                            intersection_type = outer_intersection.type()
                            if intersection_type == QgsWkbTypes.LineGeometry:
                                intersect_more_pairs.append((polygon[id_field], candidate_feature[id_field]))
                            else:
                                self.logger.warning(__name__,
                                    "(MoreBFS) Intersection between plot (t_id={}) and boundary (t_id={}) is a geometry of type: {}".format(
                                        polygon[id_field],
                                        candidate_feature[id_field],
                                        intersection_type))

                        inner_intersection = QgsGeometry(multi_inner_rings).intersection(candidate_geometry)
                        if not inner_intersection.isEmpty():
                            intersection_type = inner_intersection.type()
                            if intersection_type == QgsWkbTypes.LineGeometry:
                                intersect_less_pairs.append((polygon[id_field], candidate_feature[id_field]))
                            else:
                                self.logger.warning(__name__,
                                    "(Less) Intersection between plot (t_id={}) and boundary (t_id={}) is a geometry of type: {}".format(
                                        polygon[id_field],
                                        candidate_feature[id_field],
                                        intersection_type))

                    else:
                        boundary = None
                        if is_multipart and multi_polygon:
                            boundary = multi_polygon.boundary()
                        elif not is_multipart and single_polygon:
                            boundary = single_polygon.boundary()

                        simple_intersection = QgsGeometry(boundary).intersection(candidate_geometry)
                        if not simple_intersection.isEmpty():
                            intersection_type = simple_intersection.type()
                            if boundary and intersection_type == QgsWkbTypes.LineGeometry:
                                intersect_more_pairs.append((polygon[id_field], candidate_feature[id_field]))
                            else:
                                self.logger.warning(__name__,
                                    "(MoreBFS) Intersection between plot (t_id={}) and boundary (t_id={}) is a geometry of type: {}".format(
                                        polygon[id_field],
                                        candidate_feature[id_field],
                                        intersection_type))
        # free up memory
        del candidate_features
        del dict_features
        gc.collect()
        return intersect_more_pairs, intersect_less_pairs

    def get_pair_boundary_boundary_point(self, boundary_layer, boundary_point_layer, id_field, use_selection=True, tolerance=0):
        id_field_idx = boundary_layer.fields().indexFromName(id_field)
        request = QgsFeatureRequest().setSubsetOfAttributes([id_field_idx])
        lines = boundary_layer.getSelectedFeatures(request) if use_selection else boundary_layer.getFeatures(request)
        intersect_pairs = list()

        if boundary_point_layer.featureCount() == 0:
            return intersect_pairs

        id_field_idx = boundary_point_layer.fields().indexFromName(id_field)
        request = QgsFeatureRequest().setSubsetOfAttributes([id_field_idx])
        dict_features = {feature.id(): feature for feature in boundary_point_layer.getFeatures(request)}
        index = QgsSpatialIndex(boundary_point_layer)
        candidate_features = None

        tolerance_in_m = tolerance/1000
        for line in lines:
            bbox = line.geometry().boundingBox()
            candidates_ids = index.intersects(bbox.buffered(tolerance_in_m))
            candidate_features = [dict_features[candidate_id] for candidate_id in candidates_ids]
            for candidate_feature in candidate_features:
                candidate_point = candidate_feature.geometry().asPoint()
                for line_vertex in line.geometry().asPolyline():
                    intersects = False
                    if tolerance_in_m:
                        intersects = sqrt((line_vertex.x() - candidate_point.x()) ** 2 +
                                          (line_vertex.y() - candidate_point.y()) ** 2) <= tolerance_in_m
                    else:
                        intersects = (line_vertex.x() == candidate_point.x() and line_vertex.y() == candidate_point.y())

                    if intersects:
                        pair = (line[id_field], candidate_feature[id_field])
                        if pair not in intersect_pairs:
                            intersect_pairs.append(pair)
        # free up memory
        del candidate_features
        del dict_features
        gc.collect()
        return intersect_pairs

    def get_polyline_as_single_segments(self, polyline):
        """
        Copied from:
        https://github.com/qgis/QGIS/blob/55203a0fc2b8e35fa2909da77a84bbfde8fcba5c/python/plugins/processing/algs/qgis/Explode.py#L99
        """
        segments = []
        for i in range(polyline.numPoints() - 1):
            ptA = polyline.pointN(i)
            ptB = polyline.pointN(i + 1)
            segment = QgsGeometry(QgsLineString([ptA, ptB]))
            segments.append(segment)
        return segments

    def extract_as_single_segments(self, geom):
        """
        Copied from:
        https://github.com/qgis/QGIS/blob/55203a0fc2b8e35fa2909da77a84bbfde8fcba5c/python/plugins/processing/algs/qgis/Explode.py#L89
        """
        segments = []
        if geom.isMultipart():
            for part in range(geom.constGet().numGeometries()):
                segments.extend(self.get_polyline_as_single_segments(geom.constGet().geometryN(part)))
        else:
            segments.extend(self.get_polyline_as_single_segments(geom.constGet()))
        return segments

    def get_overlapping_points(self, point_layer):
        """
        Returns a list of lists, where inner lists are ids of overlapping
        points, e.g., [[1, 3], [19, 2, 8]].
        """
        res = list()
        if point_layer.featureCount() == 0:
            return res

        set_points = set()
        index = QgsSpatialIndex(point_layer)

        request = QgsFeatureRequest().setSubsetOfAttributes([])
        for feature in point_layer.getFeatures(request):
            if feature.geometry().isEmpty():
                continue  # Skip NULL or EMPTY geometries
                
            if not feature.id() in set_points:
                ids = index.intersects(feature.geometry().boundingBox())

                if len(ids) > 1: # Points do overlap!
                    set_points = set_points.union(set(ids))
                    res.append(ids)

        return res

    def get_overlapping_lines(self, line_layer, use_selection=True):
        """
        Returns a dict whose key is a pair of line ids where there are
        intersections, and whose value is a list of intersection geometries
        """
        if line_layer.featureCount() == 0:
            return None

        feedback = CustomFeedbackWithErrors()
        try:
            dict_res = processing.run("model:Overlapping_Boundaries", {
                'Boundary': line_layer,
                'native:extractbyexpression_3:Intersected_Lines': 'TEMPORARY_OUTPUT',
                'native:deleteduplicategeometries_1:Intersected_Points': 'TEMPORARY_OUTPUT'
            }, feedback=feedback)
        except QgsProcessingException as e:
            self.logger.warning(__name__, QCoreApplication.translate("Geometry",
                                                                     "Error running the model to extract overlapping boundaries. Details: {}".format(
                                                                         feedback.msg)))
            dict_res = dict()

        return dict_res

    def get_overlapping_polygons(self, polygon_layer):
        """
        Obtains overlapping polygons from a single layer
        :param polygon_layer: vector layer with geometry type polygon
        :return: List of lists with pairs of overlapping polygons' ids,
        e.g., [[1, 2], [1, 3]]
        """
        list_overlapping_polygons = list()
        if type(polygon_layer) != QgsVectorLayer or \
            QgsWkbTypes.PolygonGeometry != polygon_layer.geometryType() or \
            polygon_layer.featureCount() == 0:
            return list_overlapping_polygons

        request = QgsFeatureRequest().setSubsetOfAttributes([])
        dict_features = {feature.id(): feature for feature in polygon_layer.getFeatures(request)}
        index = QgsSpatialIndex(polygon_layer)
        candidate_features = None

        for feature in polygon_layer.getFeatures(request):
            bbox = feature.geometry().boundingBox()
            bbox.scale(1.001)
            candidates_ids = index.intersects(bbox)
            candidate_features = [dict_features[candidate_id] for candidate_id in candidates_ids]

            for candidate_feature in candidate_features:
                is_overlap = feature.geometry().overlaps(candidate_feature.geometry()) or \
                             feature.geometry().contains(candidate_feature.geometry()) or \
                             feature.geometry().within(candidate_feature.geometry())

                if is_overlap:
                    if feature.id() != candidate_feature.id():
                        overlapping_polygons = sorted([feature.id(), candidate_feature.id()])
                        if overlapping_polygons not in list_overlapping_polygons:
                            list_overlapping_polygons.append(overlapping_polygons)

        # free up memory
        del candidate_features
        del dict_features
        gc.collect()
        return list_overlapping_polygons

    def get_intersection_polygons(self, polygon_layer, polygon_id, overlapping_id):
        feature_polygon = polygon_layer.getFeature(polygon_id)
        feature_overlap = polygon_layer.getFeature(overlapping_id)

        listGeoms = list()
        intersection = feature_polygon.geometry().intersection(feature_overlap.geometry())

        if not intersection.isEmpty():
            if intersection.type() == QgsWkbTypes.PolygonGeometry:
                listGeoms.append(intersection)
            elif intersection.wkbType() in [QgsWkbTypes.GeometryCollection,
                QgsWkbTypes.GeometryCollectionM, QgsWkbTypes.GeometryCollectionZ,
                QgsWkbTypes.GeometryCollectionZM]:
                for part in intersection.asGeometryCollection():
                    if part.type() == QgsWkbTypes.PolygonGeometry:
                        listGeoms.append(part)

        return QgsGeometry.collectGeometry(listGeoms) if len(listGeoms) > 0 else None

    def get_inner_intersections_between_polygons(self, polygon_layer_1, polygon_layer_2):
        """
        Discard intersections other than inner intersections (i.e., only returns
        polygon intersections)
        """
        ids = list()
        list_overlapping = list()
        request = QgsFeatureRequest().setSubsetOfAttributes([])
        dict_features = {feature.id(): feature for feature in polygon_layer_2.getFeatures(request)}
        index = QgsSpatialIndex(polygon_layer_2)
        candidate_features = None

        for feature in polygon_layer_1.getFeatures(request):
            bbox = feature.geometry().boundingBox()
            candidates_ids = index.intersects(bbox)
            candidate_features = [dict_features[candidate_id] for candidate_id in candidates_ids]

            for candidate_feature in candidate_features:
                candidate_feature_geo = candidate_feature.geometry()
                if feature.geometry().intersects(candidate_feature_geo) and not feature.geometry().touches(candidate_feature_geo):
                    intersection = feature.geometry().intersection(candidate_feature_geo)

                    if not intersection.isEmpty():
                        if intersection.type() == QgsWkbTypes.PolygonGeometry:
                            ids.append([feature.id(), candidate_feature.id()])
                            list_overlapping.append(intersection)
                        elif intersection.wkbType() in [QgsWkbTypes.GeometryCollection,
                                                        QgsWkbTypes.GeometryCollectionM, QgsWkbTypes.GeometryCollectionZ,
                                                        QgsWkbTypes.GeometryCollectionZM]:
                            for part in intersection.asGeometryCollection():
                                if part.type() == QgsWkbTypes.PolygonGeometry:
                                    ids.append([feature.id(), candidate_feature.id()])
                                    list_overlapping.append(part)
        # free up memory
        del candidate_features
        del dict_features
        gc.collect()
        return ids, QgsGeometry.collectGeometry(list_overlapping) if len(list_overlapping) > 0 else None

    def get_gaps_in_polygon_layer(self, layer, include_roads):
        """
        Find gaps in a continuous layer in space.

        Ported/adapted to Python from:
        https://github.com/qgis/QGIS/blob/2c536307476e205b83d86863b903d7ea9d628f0d/src/plugins/topology/topolTest.cpp#L579-L726
        """
        request = QgsFeatureRequest().setSubsetOfAttributes([])
        features = layer.getFeatures(request)
        featureCollection = list()

        for feature in features:
            if feature.geometry().isEmpty():
                continue

            if not feature.geometry().isGeosValid():
                continue

            if feature.geometry().isMultipart() and feature.geometry().type() == QgsWkbTypes.PolygonGeometry:
                for polygon in feature.geometry().asMultiPolygon():
                    featureCollection.append(QgsGeometry.fromPolygonXY(polygon))
                continue

            featureCollection.append(feature.geometry())

        union_geom = QgsGeometry.unaryUnion(featureCollection)
        buffer_extent = QgsGeometry.fromRect(union_geom.boundingBox()).buffer(2, 3)  # Enlarged envelope
        buffer_diff = buffer_extent.difference(QgsGeometry.fromRect(union_geom.boundingBox()))  # Like a donut
        diff_geoms = buffer_extent.difference(union_geom).difference(buffer_diff)  # The negative of original polys cut by extent

        if not diff_geoms:
            self.logger.debug(__name__, "Gaps in polygon layer: no difference result, no errors...")
            return list()

        feature_error = list()

        if diff_geoms.type() == QgsWkbTypes.PolygonGeometry and not QgsWkbTypes.isMultiType(diff_geoms.wkbType()):
            diff_geoms.convertToMultiType()

        try:
            for geometry in diff_geoms.asMultiPolygon():
                conflict_geom = QgsGeometry.fromPolygonXY(geometry)
                touches_union = conflict_geom.touches(union_geom)
                intersects_buffer = conflict_geom.intersects(buffer_diff)

                if touches_union and intersects_buffer:  # It's not an internal gap
                    # Cases to discard this geometry
                    #  1) We don't want to include roads,
                    #  2) We're dealing with a single polygon or block (cuadra), so we don't want the exterior gaps
                    if not include_roads or not union_geom.isMultipart():
                        continue

                feature_error.append(conflict_geom)
        except TypeError as e:
            self.logger.warning_msg(__name__,
                                    QCoreApplication.translate("Geometry",
                                                               "Checking polygon gaps we found a '{}' geometry, which is not supported! Please report the issue.").format(
                                        QgsWkbTypes.displayString(diff_geoms.wkbType())))

        unified_error = QgsGeometry.collectGeometry(feature_error)
        feature_error.clear()

        # We don't want to cut by extent, it's better to cut by a convex hull (TODO: or even better by a concave hull)
        aux_convex_hull = union_geom.convexHull()
        clean_errors = unified_error.intersection(aux_convex_hull)

        return self.extract_geoms_by_type(clean_errors, [QgsWkbTypes.PolygonGeometry])

    def add_topological_vertices(self, layer1, layer2):
        """
        Modify layer1 adding vertices that are in layer2 and not in layer1

        Ideally, we could pass the whole layer2 as parameter for
        addTopologicalPoints or, at least, pass one multi-geometry containing
        all geometries from layer2. However, on the one side, the
        addTopologicalPoints function doesn't support a layer as parameter and,
        on the other side, there is a bug in the function that doesn't let it
        work with multi-geometries. That's why we need to traverse the whole
        layer2 in search for its individual geometries. We do use a SpatialIndex
        nonetheless, to improve efficiency.
        """
        if QgsWkbTypes.isMultiType(layer2.wkbType()):
            layer2 = processing.run("native:multiparttosingleparts", {'INPUT': layer2, 'OUTPUT': 'TEMPORARY_OUTPUT'})['OUTPUT']

        if layer2.geometryType() == QgsWkbTypes.PolygonGeometry:
            layer2 = processing.run("ladm_col:polygonstolines", {'INPUT': layer2, 'OUTPUT': 'TEMPORARY_OUTPUT'})['OUTPUT']

        geom_added = list()
        index = QgsSpatialIndex(layer2)
        dict_features_layer2 = None
        candidate_features = None

        with edit(layer1):
            edit_layer = QgsVectorLayerEditUtils(layer1)
            dict_features_layer2 = {f.id(): f for f in layer2.getFeatures(QgsFeatureRequest().setNoAttributes())}

            for feature in layer1.getFeatures(QgsFeatureRequest().setNoAttributes()):
                bbox = feature.geometry().boundingBox()
                candidate_ids = index.intersects(bbox)
                candidate_features = [dict_features_layer2[candidate_id] for candidate_id in candidate_ids]

                for candidate_feature in candidate_features:
                    if candidate_feature.id() not in geom_added:
                        edit_layer.addTopologicalPoints(candidate_feature.geometry())
                        geom_added.append(candidate_feature.id())

        # free up memory
        del candidate_features
        del dict_features_layer2
        gc.collect()

    def difference_plot_boundary(self, names, plots_as_lines_layer, boundary_layer, id_field):
        """
        Advanced difference function that, unlike the traditional function,
        takes into account not shared vertices to build difference geometries.
        """
        approx_diff_layer = processing.run("native:difference",
                                           {'INPUT': plots_as_lines_layer,
                                            'OVERLAY': boundary_layer,
                                            'OUTPUT': 'TEMPORARY_OUTPUT'})['OUTPUT']
        self.add_topological_vertices(approx_diff_layer, boundary_layer)

        # add_topological_vertices may produce invalid geometries, so we better play safe and fix them
        fixed_geometries = processing.run("native:fixgeometries",
                                          {'INPUT': approx_diff_layer,
                                           'OUTPUT': 'TEMPORARY_OUTPUT'})['OUTPUT']

        diff_layer = processing.run("native:difference",
                                    {'INPUT': fixed_geometries,
                                     'OVERLAY': boundary_layer,
                                     'OUTPUT': 'TEMPORARY_OUTPUT'})['OUTPUT']
        difference_features = [{'geometry': feature.geometry(), 'id': feature[id_field]}
                               for feature in diff_layer.getFeatures()]

        return difference_features

    def difference_boundary_plot(self, names, boundary_layer, plot_as_lines_layer, id_field):
        """
        Advanced difference function that, unlike the traditional function,
        takes into account not shared vertices to build difference geometries.
        """
        approx_diff_layer = processing.run("native:difference",
                                           {'INPUT': boundary_layer,
                                            'OVERLAY': plot_as_lines_layer,
                                            'OUTPUT': 'TEMPORARY_OUTPUT'})['OUTPUT']
        self.add_topological_vertices(plot_as_lines_layer, approx_diff_layer)

        # add_topological_vertices may produce invalid geometries, so we better play safe and fix them
        fixed_geometries = processing.run("native:fixgeometries",
                                          {'INPUT': plot_as_lines_layer,
                                           'OUTPUT': 'TEMPORARY_OUTPUT'})['OUTPUT']

        diff_layer = processing.run("native:difference",
                                    {'INPUT': approx_diff_layer,
                                     'OVERLAY': fixed_geometries,
                                     'OUTPUT': 'TEMPORARY_OUTPUT'})['OUTPUT']

        difference_features = [{'geometry': feature.geometry(), 'id': feature[id_field]}
                               for feature in diff_layer.getFeatures()]

        return difference_features

    def extract_geoms_by_type(self, geometry_collection, geometry_types):
        """
        Get a list of geometries with type in geometry_types from a geometry
        collection
        """
        geom_list = list()
        for geometry in geometry_collection.asGeometryCollection():
            if geometry.isMultipart():
                for i in range(geometry.numGeometries()):
                    geom_list.append(geometry.geometryN(i))
            else:
                geom_list.append(geometry)

        return [geom for geom in geom_list if geom.type() in geometry_types]

    def get_multipart_geoms(self, layer):
        """
        Get a list of geometries and ids with geometry type multipart and multiple
        geometries
        """
        request = QgsFeatureRequest().setSubsetOfAttributes([])
        features = layer.getFeatures(request)
        featureCollection = list()
        ids = list()
        for feature in features:
            geometry = feature.geometry()
            const_geom = geometry.constGet()
            if geometry.isMultipart() and const_geom.partCount() > 1:
                for i in range(const_geom.numGeometries()):
                    geom = QgsGeometry.fromWkt(const_geom.geometryN(i).asWkt())
                    featureCollection.append(geom)
                    ids.append(feature.id())
        return featureCollection, ids

    def get_begin_end_vertices_from_lines(self, layer):
        point_layer = processing.run("native:extractspecificvertices",
                                     {'VERTICES': '0,-1', 'INPUT': layer, 'OUTPUT': 'TEMPORARY_OUTPUT' })['OUTPUT']

        point_layer_uniques = processing.run("native:deleteduplicategeometries",
                                             {'INPUT': point_layer, 'OUTPUT': 'TEMPORARY_OUTPUT'})['OUTPUT']

        return point_layer_uniques

    def get_boundaries_connected_to_single_boundary(self, names, boundary_layer):
        """
        Get all boundary lines that have an end vertex with no change in
        boundary (colindancia), that is boundary lines that are connected with
        just one boundary line.
        """
        points_layer = self.get_begin_end_vertices_from_lines(boundary_layer)
        id_field_idx = boundary_layer.fields().indexFromName(names.T_ID_F)
        uuid_field_idx = boundary_layer.fields().indexFromName(names.T_ILI_TID_F)
        request = QgsFeatureRequest().setSubsetOfAttributes([id_field_idx, uuid_field_idx])
        dict_features = {feature.id(): feature for feature in boundary_layer.getFeatures(request)}
        index = QgsSpatialIndex(boundary_layer)
        ids_boundaries_list = list()
        candidate_features = None

        for feature in points_layer.getFeatures(request):
            bbox = feature.geometry().boundingBox()
            candidate_ids = index.intersects(bbox)
            candidate_features = [dict_features[candidate_id] for candidate_id in candidate_ids]
            intersect_ids = list()

            for candidate_feature in candidate_features:
                if candidate_feature.geometry().intersects(feature.geometry()):
                    intersect_ids.append(candidate_feature.id())

            if len(intersect_ids) == 2:
                # For valid lines, we get more than two intersections (think
                # about a 'Y')
                ids_boundaries_list.extend(intersect_ids)

        selected_ids = list(set(ids_boundaries_list)) # get unique ids
        selected_features = [dict_features[selected_id] for selected_id in selected_ids]

        # free up memory
        del candidate_features
        del dict_features
        gc.collect()

        return selected_features

    def join_boundary_points_with_boundary_discard_nonmatching(self, boundary_point_layer, boundary_layer, id_field):
        spatial_join_layer = processing.run("native:joinattributesbylocation",
                                            {
                                                'INPUT': boundary_point_layer,
                                                'JOIN': boundary_layer,
                                                'PREDICATE': [0],
                                                'JOIN_FIELDS': [id_field],
                                                'METHOD': 0,
                                                'DISCARD_NONMATCHING': True,
                                                'PREFIX': '',
                                                'OUTPUT': 'TEMPORARY_OUTPUT'})['OUTPUT']

        id_field_idx = spatial_join_layer.fields().indexFromName(id_field)
        request = QgsFeatureRequest().setSubsetOfAttributes([id_field_idx])
        return spatial_join_layer.getFeatures(request)

    def get_inner_rings_layer(self, names, plot_layer, id_field, use_selection=False):
        id_field_idx = plot_layer.fields().indexFromName(id_field)
        request = QgsFeatureRequest().setSubsetOfAttributes([id_field_idx])
        polygons = plot_layer.getSelectedFeatures(request) if use_selection else plot_layer.getFeatures(request)

        layer = QgsVectorLayer("LineString?crs={}".format(get_crs_authid(plot_layer.sourceCrs())), "rings", "memory")
        data_provider = layer.dataProvider()
        data_provider.addAttributes([QgsField(names.T_ID_F, QVariant.Int)])
        layer.updateFields()

        features = []

        for polygon in polygons:
            polygon_geom = polygon.geometry()
            is_multipart = polygon_geom.isMultipart()

            # Does the current multipolygon have inner rings?
            has_inner_rings = False
            multi_polygon = None
            single_polygon = None

            if is_multipart:

                multi_polygon = polygon_geom.constGet()

                # TODO: remove when the error is resolved
                if type(multi_polygon) != QgsMultiPolygon:
                    geom = QgsMultiPolygon()
                    geom.fromWkt(polygon_geom.asWkt())
                    multi_polygon = geom

                for part in range(multi_polygon.numGeometries()):
                    if multi_polygon.ringCount(part) > 1:
                        has_inner_rings = True
                        break
            else:
                single_polygon = polygon_geom.constGet()

                # TODO: remove when the error is resolved
                if type(single_polygon) != QgsPolygon:
                    geom = QgsPolygon()
                    geom.fromWkt(polygon_geom.asWkt())
                    single_polygon = geom

                if single_polygon.numInteriorRings() > 0:
                    has_inner_rings = True

            if has_inner_rings:

                if is_multipart and multi_polygon:
                    for i in range(multi_polygon.numGeometries()):
                        temp_polygon = multi_polygon.geometryN(i)

                        # TODO: remove when the error is resolved
                        if type(temp_polygon) != QgsPolygon:
                            geom = QgsPolygon()
                            geom.fromWkt(temp_polygon.asWkt())
                            temp_polygon = geom

                        for j in range(temp_polygon.numInteriorRings()):
                            new_feature = QgsVectorLayerUtils().createFeature(layer, QgsGeometry(
                                temp_polygon.interiorRing(j).clone()), {0: polygon[id_field]})
                            features.append(new_feature)

                elif not is_multipart and single_polygon:
                    for j in range(single_polygon.numInteriorRings()):
                        new_feature = QgsVectorLayerUtils().createFeature(layer, QgsGeometry(
                            single_polygon.interiorRing(j).clone()), {0: polygon[id_field]})
                        features.append(new_feature)

        layer.dataProvider().addFeatures(features)
        layer.updateExtents()
        layer.reload()
        return layer

    def build_boundaries(self, boundary_layer):
        params = {'boundaries': boundary_layer, 'native:multiparttosingleparts_1:built_boundaries': 'TEMPORARY_OUTPUT'}
        built_boundaries_layer = processing.run("model:Build_Boundaries", params)['native:multiparttosingleparts_1:built_boundaries']
        return built_boundaries_layer

    @staticmethod
    def get_relationships_among_polygons(input_layer, intersect_layer, key=None, attrs=list(), get_geometry=False):
        """
        Gets relationships among two polygon layers.

        :param input_layer: Input polygon layer
        :param intersect_layer: Intersect polygon layer
        :param key: None to use QGIS id, otherwise it expects an id to use as response key
        :param attrs: List of attributes to retrieve
        :param get_geometry: Whether the resulting dicts should contain geometry or not
        :return: 3 dicts with the given key. Example of 1 dict: {key: {'attrs':{attr1:v1,...}, 'geom':QgsGeometry}}
        """
        # attrs = attributes or []
        def build_response_dict():
            res = dict()
            if not key and not attrs and not get_geometry:  # We just need the QGIS id
                res = {fid: dict() for fid in input_layer.selectedFeatureIds()}
            else:
                for f in input_layer.selectedFeatures():
                    f_attrs = {attr: f[attr] for attr in attrs}
                    values = {'attrs': f_attrs, 'geometry': f.geometry() if get_geometry else None}
                    res[f[key] if key else f.id()] = values
            return res

        # 1) Select input layer features disjoint from intersect layer features
        processing.run("native:selectbylocation", {'INPUT': input_layer,
                                                   'PREDICATE': [2],  # disjoint
                                                   'INTERSECT': intersect_layer,
                                                   'METHOD': 0})
        input_disjoint = build_response_dict()

        # 2) Select input layer features within within itersect layer features
        processing.run("native:selectbylocation", {'INPUT': input_layer,
                                                   'PREDICATE': [6],  # are within
                                                   'INTERSECT': intersect_layer,
                                                   'METHOD': 0})
        input_within = build_response_dict()
        fids_within = input_layer.selectedFeatureIds()  # We'll use them after the next run

        # 3) Select input layer features that intersect the intersect layer features
        processing.run("native:selectbylocation", {'INPUT': input_layer,
                                                   'PREDICATE': [0],  # intersects
                                                   'INTERSECT': intersect_layer,
                                                   'METHOD': 0})
        # We need to select those features that intersect but are not within
        # (i.e. overlap, contain) intersect layer features
        fids_intersect = input_layer.selectedFeatureIds()
        input_layer.selectByIds(list(set(fids_intersect) - set(fids_within)))
        input_overlaps = build_response_dict()

        input_layer.removeSelection()

        return input_disjoint, input_overlaps, input_within

    @staticmethod
    def get_intersection_features(layer, geometries, id_field=None):
        """
        Return a list of lists, every list has the feature ids of features
        that intersect with every geometry. If id_field is None return QGIS id.

        layer: QgsVectorLayer
        geometries: list of QgsGeometries (Order is not modified)
        """
        if id_field:
            id_field_idx = layer.fields().indexFromName(id_field)
            request = QgsFeatureRequest().setSubsetOfAttributes([id_field_idx])
            dict_features = {feature.id(): feature for feature in layer.getFeatures(request)}
        else:
            request = QgsFeatureRequest().setNoAttributes()
            dict_features = {feature.id(): feature for feature in layer.getFeatures(request)}

        index = QgsSpatialIndex(layer)

        intersecting_ids = list()
        for geometry in geometries:
            bbox = geometry.boundingBox()
            bbox.scale(1.001)
            candidates_ids = index.intersects(bbox)
            candidate_features = [dict_features[candidate_id] for candidate_id in candidates_ids]
            feature_ids = list()
            for candidate_feature in candidate_features:
                candidate_geometry = candidate_feature.geometry()
                if geometry.intersects(candidate_geometry):
                    if id_field:
                        feature_ids.append(candidate_feature[id_field])
                    else:
                        feature_ids.append(candidate_feature.id())
            intersecting_ids.append(feature_ids)
        return intersecting_ids

    @staticmethod
    def get_polygon_nodes_layer(polygon_layer, id_field):
        """
        Layer is created with unique vertices. It is necessary because 'remove duplicate vertices' processing
        algorithm does not filter the data as we need them
        """
        tmp_plot_nodes_layer = processing.run("native:extractvertices", {'INPUT': polygon_layer, 'OUTPUT': 'TEMPORARY_OUTPUT'})['OUTPUT']

        duplicate_nodes_layer = processing.run("native:fieldcalculator", {
            'INPUT': tmp_plot_nodes_layer,
            'FIELD_NAME': 'wkt_geom',
            'FIELD_TYPE': 2,  # String
            'FIELD_LENGTH': 255,
            'FIELD_PRECISION': 3,
            'NEW_FIELD': True,
            'FORMULA': 'geom_to_wkt( $geometry )',
            'OUTPUT': 'TEMPORARY_OUTPUT'
        })['OUTPUT']

        unique_nodes_layer = processing.run("native:removeduplicatesbyattribute", {
            'INPUT': duplicate_nodes_layer,
            'FIELDS': [id_field, 'wkt_geom'],
            'OUTPUT': 'TEMPORARY_OUTPUT'})['OUTPUT']
        GeometryUtils.create_spatial_index(unique_nodes_layer)

        return unique_nodes_layer

    @staticmethod
    def get_non_intersecting_geometries(input_layer, join_layer, id_field):
        # get non matching features between input and join layer
        spatial_join_layer = processing.run("native:joinattributesbylocation",
                                            {'INPUT': input_layer,
                                             'JOIN': join_layer,
                                             'PREDICATE': [0],  # Intersects
                                             'JOIN_FIELDS': [id_field],
                                             'METHOD': 0,
                                             'DISCARD_NONMATCHING': False,
                                             'PREFIX': '',
                                             'NON_MATCHING': 'TEMPORARY_OUTPUT'})['NON_MATCHING']
        features = list()

        for feature in spatial_join_layer.getFeatures():
            # When the two layers have the same attribute, the field of the layer
            # that makes the join is renamed and the input layer preserves the same name
            feature_id = feature[id_field]  # We use input layer field
            feature_geom = feature.geometry()
            features.append((feature_id, feature_geom))

        return features

    def get_dangle_ids(self, boundary_layer):
        # 1. Run extract specific vertices
        # 2. Call to get_overlapping_points
        # 3. Obtain dangle ids (those not present in overlapping points result)
        res = processing.run("native:extractspecificvertices", {
                'INPUT': boundary_layer,
                'VERTICES': '0,-1', # First and last
                'OUTPUT': 'TEMPORARY_OUTPUT'
            },
            feedback=QgsProcessingFeedback()
        )
        end_points = res['OUTPUT']

        end_point_ids = [point.id() for point in end_points.getFeatures()]
        overlapping_points = self.get_overlapping_points(end_points)

        # Unpack list of lists into single list
        overlapping_point_ids = [item for sublist in overlapping_points for item in sublist]

        return (end_points, list(set(end_point_ids) - set(overlapping_point_ids)))

    @staticmethod
    def create_spatial_index(layer):
        if layer.hasSpatialIndex() != QgsFeatureSource.SpatialIndexPresent:
            processing.run("native:createspatialindex", {'INPUT': layer})
