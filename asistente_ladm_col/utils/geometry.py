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
from qgis.PyQt.QtCore import QObject
from qgis.core import (
    Qgis,
    QgsApplication,
    QgsGeometry,
    QgsLineString,
    QgsMultiLineString,
    QgsSpatialIndex,
    QgsWkbTypes,
    QgsProcessingFeedback,
    QgsVectorLayer,
    QgsVectorLayerEditUtils
)
from qgis.core import edit

import processing
from ..config.general_config import PLUGIN_NAME, DEFAULT_POLYGON_AREA_TOLERANCE
from ..config.table_mapping_config import ID_FIELD

class GeometryUtils(QObject):

    def __init__(self):
        QObject.__init__(self)
        self.log = QgsApplication.messageLog()

    def get_pair_boundary_plot(self, boundary_layer, plot_layer, id_field=ID_FIELD, use_selection=True):
        lines = boundary_layer.getFeatures()
        polygons = plot_layer.getSelectedFeatures() if use_selection else plot_layer.getFeatures()
        intersect_more_pairs = list()
        intersect_less_pairs = list()

        if boundary_layer.featureCount() == 0:
            return (intersect_more_pairs, intersect_less_pairs)

        index = QgsSpatialIndex(boundary_layer)

        for polygon in polygons:
            bbox = polygon.geometry().boundingBox()
            bbox.scale(1.001)
            candidates_ids = index.intersects(bbox)

            candidates_features = boundary_layer.getFeatures(candidates_ids)

            for candidate_feature in candidates_features:
                polygon_geom = polygon.geometry()
                is_multipart = polygon_geom.isMultipart()
                candidate_geometry = candidate_feature.geometry()

                if polygon_geom.intersects(candidate_geometry):
                    # Does the current multipolygon have inner rings?
                    has_inner_rings = False
                    multi_polygon = None
                    single_polygon = None

                    if is_multipart:
                        multi_polygon = polygon_geom.get()
                        for part in range(multi_polygon.numGeometries()):
                            if multi_polygon.ringCount(part) > 1:
                                has_inner_rings = True
                                break
                    else:
                        single_polygon = polygon_geom.get()
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

                        intersection_type = QgsGeometry(multi_outer_rings).intersection(candidate_geometry).type()
                        if intersection_type == QgsWkbTypes.LineGeometry:
                            intersect_more_pairs.append((polygon[id_field], candidate_feature[id_field]))
                        else:
                            self.log.logMessage(
                                "(MoreBFS) Intersection between plot (t_id={}) and boundary (t_id={}) is a geometry of type: {}".format(
                                    polygon[id_field],
                                    candidate_feature[id_field],
                                    intersection_type),
                                PLUGIN_NAME,
                                Qgis.Warning
                            )

                        intersection_type = QgsGeometry(multi_inner_rings).intersection(candidate_geometry).type()
                        if intersection_type == QgsWkbTypes.LineGeometry:
                            intersect_less_pairs.append((polygon[id_field], candidate_feature[id_field]))
                        else:
                            self.log.logMessage(
                                "(Less) Intersection between plot (t_id={}) and boundary (t_id={}) is a geometry of type: {}".format(
                                    polygon[id_field],
                                    candidate_feature[id_field],
                                    intersection_type),
                                PLUGIN_NAME,
                                Qgis.Warning
                            )

                    else:
                        boundary = None
                        if is_multipart and multi_polygon:
                            boundary = multi_polygon.boundary()
                        elif not is_multipart and single_polygon:
                            boundary = single_polygon.boundary()

                        intersection_type = QgsGeometry(boundary).intersection(candidate_geometry).type()
                        if boundary and intersection_type == QgsWkbTypes.LineGeometry:
                            intersect_more_pairs.append((polygon[id_field], candidate_feature[id_field]))
                        else:
                            self.log.logMessage(
                                "(MoreBFS) Intersection between plot (t_id={}) and boundary (t_id={}) is a geometry of type: {}".format(
                                    polygon[id_field],
                                    candidate_feature[id_field],
                                    intersection_type),
                                PLUGIN_NAME,
                                Qgis.Warning
                            )

        return (intersect_more_pairs, intersect_less_pairs)

    def get_pair_boundary_boundary_point(self, boundary_layer, boundary_point_layer, id_field=ID_FIELD, use_selection=True):
        lines = boundary_layer.getSelectedFeatures() if use_selection else boundary_layer.getFeatures()
        points = boundary_point_layer.getFeatures()
        intersect_pairs = list()

        if boundary_point_layer.featureCount() == 0:
            return intersect_pairs

        index = QgsSpatialIndex(boundary_point_layer)

        for line in lines:
            bbox = line.geometry().boundingBox()
            bbox.scale(1.001)
            candidates_ids = index.intersects(bbox)
            candidates_features = boundary_point_layer.getFeatures(candidates_ids)
            for candidate_feature in candidates_features:
                #if line.geometry().intersects(candidate_feature.geometry()):
                #    intersect_pair.append(line['t_id'], candidate_feature['t_id'])
                candidate_point = candidate_feature.geometry().asPoint()
                for line_vertex in line.geometry().asPolyline():
                    if abs(line_vertex.x() - candidate_point.x()) < 0.001 \
                       and abs(line_vertex.y() - candidate_point.y()) < 0.001:
                        pair = (line[id_field], candidate_feature[id_field])
                        if pair not in intersect_pairs:
                            intersect_pairs.append(pair)
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
        index = QgsSpatialIndex(point_layer.getFeatures())

        for feature in point_layer.getFeatures():
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

        feedback = QgsProcessingFeedback()
        dict_res = processing.run("model:Overlapping_Boundaries", {
                    'Boundary':line_layer,
                    'native:saveselectedfeatures_2:Intersected_Lines':'memory:',
                    'native:saveselectedfeatures_3:Intersected_Points':'memory:'
                },
                feedback=feedback)

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

        index = QgsSpatialIndex(polygon_layer)

        for feature in polygon_layer.getFeatures():
            bbox = feature.geometry().boundingBox()
            bbox.scale(1.001)
            candidates_ids = index.intersects(bbox)
            candidates_features = polygon_layer.getFeatures(candidates_ids)

            for candidate_feature in candidates_features:
                is_overlap = feature.geometry().overlaps(candidate_feature.geometry()) or \
                             feature.geometry().contains(candidate_feature.geometry()) or \
                             feature.geometry().within(candidate_feature.geometry())

                if is_overlap:
                    if feature.id() != candidate_feature.id():
                        overlapping_polygons = sorted([feature.id(), candidate_feature.id()])
                        if overlapping_polygons not in list_overlapping_polygons:
                            list_overlapping_polygons.append(overlapping_polygons)

        return list_overlapping_polygons

    def get_intersection_polygons(self, polygon_layer, polygon_id, overlapping_id):
        feature_polygon = polygon_layer.getFeature(polygon_id)
        feature_overlap = polygon_layer.getFeature(overlapping_id)

        listGeoms = list()
        intersection = feature_polygon.geometry().intersection(feature_overlap.geometry())

        if intersection.type() == QgsWkbTypes.PolygonGeometry:
            if intersection.area() > DEFAULT_POLYGON_AREA_TOLERANCE:
                listGeoms.append(intersection)
        elif intersection.wkbType() in [QgsWkbTypes.GeometryCollection,
            QgsWkbTypes.GeometryCollectionM, QgsWkbTypes.GeometryCollectionZ,
            QgsWkbTypes.GeometryCollectionZM]:
            for part in intersection.asGeometryCollection():
                if part.type() == QgsWkbTypes.PolygonGeometry:
                    if part.area() > DEFAULT_POLYGON_AREA_TOLERANCE:
                        listGeoms.append(part)

        return QgsGeometry.collectGeometry(listGeoms) if len(listGeoms) > 0 else None

    def get_inner_intersections_between_polygons(self, polygon_layer_1, polygon_layer_2):
        """
        Discard intersections other than inner intersections (i.e., only returns
        polygon intersections)
        """
        ids = list()
        list_overlapping = list()
        index = QgsSpatialIndex(polygon_layer_2)

        for feature in polygon_layer_1.getFeatures():
            bbox = feature.geometry().boundingBox()
            candidates_ids = index.intersects(bbox)
            candidates_features = polygon_layer_2.getFeatures(candidates_ids)

            for candidate_feature in candidates_features:
                candidate_feature_geo = candidate_feature.geometry()
                if feature.geometry().intersects(candidate_feature_geo) and not feature.geometry().touches(candidate_feature_geo):
                    intersection = feature.geometry().intersection(candidate_feature_geo)

                    if intersection.type() == QgsWkbTypes.PolygonGeometry and intersection.area() > DEFAULT_POLYGON_AREA_TOLERANCE:
                        ids.append([feature.id(), candidate_feature.id()])
                        list_overlapping.append(intersection)
                    elif intersection.wkbType() in [QgsWkbTypes.GeometryCollection,
                                                    QgsWkbTypes.GeometryCollectionM, QgsWkbTypes.GeometryCollectionZ,
                                                    QgsWkbTypes.GeometryCollectionZM]:
                        for part in intersection.asGeometryCollection():
                            if part.type() == QgsWkbTypes.PolygonGeometry and intersection.area() > DEFAULT_POLYGON_AREA_TOLERANCE:
                                ids.append([feature.id(), candidate_feature.id()])
                                list_overlapping.append(part)

        return ids, QgsGeometry.collectGeometry(list_overlapping) if len(list_overlapping) > 0 else None

    def get_gaps_in_polygon_layer(self, layer, include_roads):
        """
        Find gaps in a continuous layer in space.

        Ported/adapted to Python from:
        https://github.com/qgis/QGIS/blob/2c536307476e205b83d86863b903d7ea9d628f0d/src/plugins/topology/topolTest.cpp#L579-L726
        """
        features = layer.getFeatures()
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
        aux_convex_hull = union_geom.convexHull()
        buffer_extent = QgsGeometry.fromRect(union_geom.boundingBox()).buffer(2, 3)
        buffer_diff = buffer_extent.difference(QgsGeometry.fromRect(union_geom.boundingBox()))
        diff_geoms = buffer_extent.difference(union_geom).difference(buffer_diff)

        if not diff_geoms:
            return None

        feature_error = list()
        if not diff_geoms.isMultipart():
            if include_roads and diff_geoms.touches(union_geom) and diff_geoms.intersects(buffer_diff):
                print("Unique value and no error")
                return None

        for geometry in diff_geoms.asMultiPolygon():
            conflict_geom = QgsGeometry.fromPolygonXY(geometry)
            if not include_roads and conflict_geom.touches(union_geom) and conflict_geom.intersects(buffer_diff):
                continue

            if not union_geom.isMultipart() and conflict_geom.touches(union_geom) and conflict_geom.intersects(buffer_diff):
                continue

            feature_error.append(conflict_geom)

        unified_error = QgsGeometry.collectGeometry(feature_error)
        feature_error.clear()
        clean_errors = unified_error.intersection(aux_convex_hull)

        return self.extract_geoms_by_type(clean_errors, [QgsWkbTypes.PolygonGeometry])

    def add_topological_vertices(self, layer1, layer2):
        """
        Modify layer1 adding vertices that are in layer2 and not in layer1

        Ideally, we could pass the whole layer2 as parameter for
        addTopologicalPoints or, at least, pass one multi-geometry containing
        all geometries from layer2. However, onthe one side, the
        addTopologicalPoints function doesn't support a layer as parameter and,
        on the other side, there is a bug in the function that doesn't let it
        work with multi-geometries. That's why we need to traverse the whole
        layer2 in search for its individual geometries. We do use a SpatialIndex
        nonetheless, to improve efficiency.
        """
        if QgsWkbTypes.isMultiType(layer2.wkbType()):
            layer2 = processing.run("native:multiparttosingleparts", {'INPUT': layer2, 'OUTPUT': 'memory:'})['OUTPUT']

        if layer2.geometryType() == QgsWkbTypes.PolygonGeometry:
            layer2 = processing.run("qgis:polygonstolines", {'INPUT': layer2, 'OUTPUT': 'memory:'})['OUTPUT']

        index = QgsSpatialIndex(layer2)
        with edit(layer1):
            edit_layer = QgsVectorLayerEditUtils(layer1)

            for feature in layer1.getFeatures():
                bbox = feature.geometry().boundingBox()
                intersects_ids = index.intersects(bbox)
                intersect_features = layer2.getFeatures(intersects_ids)

                for intersect_feature in intersect_features:
                    edit_layer.addTopologicalPoints(intersect_feature.geometry())

    def line_polygon_layer_difference(self, input_layer_a, input_layer_b):
        if input_layer_a.geometryType() == QgsWkbTypes.PolygonGeometry:
            input_layer_a = processing.run("qgis:polygonstolines", {'INPUT': input_layer_a, 'OUTPUT': 'memory:'})['OUTPUT']
        if input_layer_b.geometryType() == QgsWkbTypes.PolygonGeometry:
            input_layer_b = processing.run("qgis:polygonstolines", {'INPUT': input_layer_b, 'OUTPUT': 'memory:'})['OUTPUT']
        diff_layer = processing.run("native:difference", {'INPUT': input_layer_a, 'OVERLAY': input_layer_b, 'OUTPUT': 'memory:'})['OUTPUT']
        return diff_layer

    def difference_plot_boundary(self, plot_layer, boundary_layer, id_field=ID_FIELD):
        """
        Advanced difference function that, unlike the traditional function,
        takes into account not shared vertices to build difference geometries.
        """
        difference_features = list()
        polygons_layer = self.clone_layer(plot_layer)

        if not polygons_layer:
            print("Plots layer was not cloned correctly")
            return []

        self.add_topological_vertices(polygons_layer, boundary_layer)
        differences_layer = self.line_polygon_layer_difference(polygons_layer, boundary_layer)

        for feature in differences_layer.getFeatures():
            difference_features.append({
                'geometry': feature.geometry(),
                'id': feature[id_field]})

        return difference_features

    def difference_boundary_plot(self, boundary_layer, plot_layer, id_field=ID_FIELD):
        """
        Advanced difference function that, unlike the traditional function,
        takes into account not shared vertices to build difference geometries.
        """
        difference_features = list()
        polygons_layer = self.clone_layer(plot_layer)

        if id(plot_layer) == id(polygons_layer):
            print("Plots layer was not cloned correctly")

        self.add_topological_vertices(polygons_layer, boundary_layer)
        differences_layer = self.line_polygon_layer_difference(boundary_layer, polygons_layer)

        for feature in differences_layer.getFeatures():
            difference_features.append({
                'geometry': feature.geometry(),
                'id': feature[id_field]})

        return difference_features

    def clone_layer(self, layer):
        layer.selectAll()
        clone_layer = processing.run("native:saveselectedfeatures", {'INPUT': layer, 'OUTPUT': 'memory:'})['OUTPUT']
        layer.removeSelection()

        return clone_layer if type(clone_layer) == QgsVectorLayer else False

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
        features = layer.getFeatures()
        featureCollection = list()
        ids = list()
        for feature in features:
            if feature.geometry().isMultipart() and feature.geometry().constGet().partCount() > 1 and feature.geometry().type() == QgsWkbTypes.PolygonGeometry:
                for polygon in feature.geometry().asMultiPolygon():
                    featureCollection.append(QgsGeometry.fromPolygonXY(polygon))
                    ids.append(feature.id())
                    continue
        return featureCollection, ids
