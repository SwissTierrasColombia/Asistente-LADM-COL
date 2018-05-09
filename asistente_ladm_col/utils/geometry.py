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
from qgis.core import (
    Qgis,
    QgsApplication,
    QgsGeometry,
    QgsLineString,
    QgsMultiLineString,
    QgsPointXY,
    QgsSpatialIndex,
    QgsVectorLayerUtils,
    QgsWkbTypes
)
from qgis.PyQt.QtCore import QObject, QCoreApplication, QVariant, QSettings

from ..config.table_mapping_config import ID_FIELD
from ..config.general_config import PLUGIN_NAME

class GeometryUtils(QObject):

    def __init__(self):
        QObject.__init__(self)
        self.log = QgsApplication.messageLog()

    def get_pair_boundary_plot(self, boundary_layer, plot_layer, use_selection=True):
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
                            intersect_more_pairs.append((polygon[ID_FIELD], candidate_feature[ID_FIELD]))
                        else:
                            self.log.logMessage(
                                "(MoreBFS) Intersection between plot (t_id={}) and boundary (t_id={}) is a geometry of type: {}".format(
                                    polygon[ID_FIELD],
                                    candidate_feature[ID_FIELD],
                                    intersection_type),
                                PLUGIN_NAME,
                                Qgis.Warning
                            )

                        intersection_type = QgsGeometry(multi_inner_rings).intersection(candidate_geometry).type()
                        if intersection_type == QgsWkbTypes.LineGeometry:
                            intersect_less_pairs.append((polygon[ID_FIELD], candidate_feature[ID_FIELD]))
                        else:
                            self.log.logMessage(
                                "(Less) Intersection between plot (t_id={}) and boundary (t_id={}) is a geometry of type: {}".format(
                                    polygon[ID_FIELD],
                                    candidate_feature[ID_FIELD],
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
                            intersect_more_pairs.append((polygon[ID_FIELD], candidate_feature[ID_FIELD]))
                        else:
                            self.log.logMessage(
                                "(MoreBFS) Intersection between plot (t_id={}) and boundary (t_id={}) is a geometry of type: {}".format(
                                    polygon[ID_FIELD],
                                    candidate_feature[ID_FIELD],
                                    intersection_type),
                                PLUGIN_NAME,
                                Qgis.Warning
                            )

        return (intersect_more_pairs, intersect_less_pairs)

    def get_pair_boundary_boundary_point(self, boundary_layer, boundary_point_layer, use_selection=True):
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
                        pair = (line[ID_FIELD], candidate_feature[ID_FIELD])
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
        Return a dict whose key is a pair of line ids where there are
        intersections, and whose value is a list of intersection geometries
        """
        dict_res = dict()

        def insert_into_res(ids, geometry):
            """
            Local function to append a geometry into a list for each pair of ids
            """
            pair = "{}-{}".format(min(ids), max(ids))
            if pair not in dict_res:
                dict_res[pair] = [geometry]
            else: # Pair is in dict already
                duplicate = False
                for existing_geometry in dict_res[pair]:
                    if geometry.isGeosEqual(existing_geometry):
                        # isGeosEqual gives True for lines even if they have
                        # the orientation inverted
                        duplicate = True
                        break

                if not duplicate:
                    dict_res[pair].append(geometry)

        lines = line_layer.getFeatures()
        index = QgsSpatialIndex(line_layer)

        for line in lines:
            line_geometry = line.geometry()
            bbox = line_geometry.boundingBox()
            bbox.scale(1.001)
            candidates_ids = index.intersects(bbox)
            candidates_ids.remove(line.id()) # Remove auto-intersection
            candidates_features = line_layer.getFeatures(candidates_ids)

            for candidate_feature in candidates_features:
                candidate_geometry = candidate_feature.geometry()

                if line_geometry.intersects(candidate_geometry):
                    intersection = line_geometry.intersection(candidate_geometry)

                    if intersection.type() == QgsWkbTypes.PointGeometry and line_geometry.touches(candidate_geometry):
                        pass # Don't insert intersections where end points are involved

                    elif intersection.wkbType() == QgsWkbTypes.GeometryCollection:
                        geometry_collection = intersection.asGeometryCollection()

                        for geometry in geometry_collection:
                            if geometry.type() == QgsWkbTypes.PointGeometry:

                                if geometry.touches(candidate_geometry):
                                    pass # End point intersection in a collection
                                else:
                                    insert_into_res([line[ID_FIELD], candidate_feature[ID_FIELD]], geometry)

                            elif geometry.type() == QgsWkbTypes.LineGeometry:
                                insert_into_res([line[ID_FIELD], candidate_feature[ID_FIELD]], geometry)

                    else: # Point and not touches; lines
                        insert_into_res([line[ID_FIELD], candidate_feature[ID_FIELD]], intersection)

                else:
                    # Intersections between an end point and the interior of a
                    # segment (not a vertex) are not discovered by QGIS so far.
                    # We need to use this workaround in the meantime
                    edge_vertex = [line_geometry.asPolyline()[0], line_geometry.asPolyline()[-1]]

                    for edge in edge_vertex:
                        edge_point = QgsGeometry.fromPointXY(QgsPointXY(edge))

                        if abs(edge_point.distance(candidate_geometry)) < 0.0001 and not edge_point.touches(candidate_geometry):
                            insert_into_res([line[ID_FIELD], candidate_feature[ID_FIELD]], edge_point)

        return dict_res
