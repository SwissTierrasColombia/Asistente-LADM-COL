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
    QgsRectangle
)
from qgis.PyQt.QtCore import QObject, QCoreApplication, QVariant, QSettings
from processing.tools.dataobjects import createContext
import processing

from ..config.table_mapping_config import (
    BOUNDARY_POINT_TABLE,
    BOUNDARY_TABLE,
    DEFAULT_EPSG,
    DEFAULT_TOO_LONG_BOUNDARY_SEGMENTS_TOLERANCE,
    ID_FIELD
)

class QualityUtils(QObject):

    def __init__(self, qgis_utils):
        QObject.__init__(self)
        self.qgis_utils = qgis_utils

    def check_overlaps_in_boundary_points(self, db):
        features = []
        boundary_point_layer = self.qgis_utils.get_layer(db, BOUNDARY_POINT_TABLE, load=True)

        if boundary_point_layer is None:
            self.qgis_utils.message_emitted.emit(
                QCoreApplication.translate("QGISUtils",
                                           "Table {} not found in DB! {}").format(BOUNDARY_POINT_TABLE, db.get_description()),
                Qgis.Warning)
            return

        error_layer = QgsVectorLayer("Point?crs=EPSG:{}".format(DEFAULT_EPSG), QCoreApplication.translate("QGISUtils", "Overlapping boundary points"), "memory")
        data_provider = error_layer.dataProvider()
        data_provider.addAttributes([QgsField("point_count", QVariant.Int)])
        error_layer.updateFields()

        overlapping = self.get_overlapping_points(boundary_point_layer)

        for items in overlapping:
            feature = boundary_point_layer.getFeature(items[0]) # We need a feature geometry, pick the first id to get it
            point = feature.geometry()
            new_feature = QgsVectorLayerUtils().createFeature(error_layer, point, {0: len(items)})
            features.append(new_feature)

        error_layer.dataProvider().addFeatures(features)

        if error_layer.featureCount() > 0:
            group = self.qgis_utils.get_error_layers_group()
            added_layer = QgsProject.instance().addMapLayer(error_layer, False)
            added_layer = group.addLayer(added_layer).layer()
            self.qgis_utils.symbology.set_point_error_symbol(added_layer)

            self.qgis_utils.message_emitted.emit(
            QCoreApplication.translate("QGISUtils",
                                            "A memory layer with {} overlapping Boundary Points has been added to the map!").format(added_layer.featureCount()), Qgis.Info)
        else:
            self.qgis_utils.message_emitted.emit(
                QCoreApplication.translate("QGISUtils",
                                           "There are no overlapping boundary points."), Qgis.Info)


    def check_overlaps_in_boundaries(self, db):
        boundary_layer = self.qgis_utils.get_layer(db, BOUNDARY_TABLE, load=True)

        if boundary_layer is None:
            self.qgis_utils.message_emitted.emit(
                QCoreApplication.translate("QGISUtils",
                                           "Table {} not found in DB! {}").format(BOUNDARY_TABLE, db.get_description()),
                Qgis.Warning)
            return

        error_point_layer = QgsVectorLayer("MultiPoint?crs=EPSG:{}".format(DEFAULT_EPSG), "Overlapping boundaries (point intersections)", "memory")
        error_line_layer = QgsVectorLayer("MultiLineString?crs=EPSG:{}".format(DEFAULT_EPSG), "Overlapping boundaries (line intersections)", "memory")
        data_provider_point = error_point_layer.dataProvider()
        data_provider_line = error_line_layer.dataProvider()
        data_provider_point.addAttributes([QgsField("intersecting_boundaries", QVariant.String)])
        data_provider_line.addAttributes([QgsField("intersecting_boundaries", QVariant.String)])
        error_point_layer.updateFields()
        error_line_layer.updateFields()

        overlapping = self.get_overlapping_lines(boundary_layer)
        line_features = list()
        point_features = list()

        for pair, geometry_list in overlapping.items():
            for geometry in geometry_list:
                # Insert a features per intersection geometry
                if geometry.type() == QgsWkbTypes.PointGeometry:
                    new_feature = QgsVectorLayerUtils().createFeature(error_point_layer, geometry, {0: pair})
                    point_features.append(new_feature)

                elif geometry.type() == QgsWkbTypes.LineGeometry:
                    new_feature = QgsVectorLayerUtils().createFeature(error_line_layer, geometry, {0: pair})
                    line_features.append(new_feature)

                elif geometry.wkbType() == QgsWkbTypes.GeometryCollection:
                    collection = geometry.asGeometryCollection()

                    for collection_item in collection:
                        if collection_item.type() == QgsWkbTypes.PointGeometry:
                            new_feature = QgsVectorLayerUtils().createFeature(error_point_layer, collection_item, {0: pair})
                            point_features.append(new_feature)

                        elif collection_item.type() == QgsWkbTypes.LineGeometry:
                            new_feature = QgsVectorLayerUtils().createFeature(error_line_layer, collection_item, {0: pair})
                            line_features.append(new_feature)

        error_point_layer.dataProvider().addFeatures(point_features)
        error_line_layer.dataProvider().addFeatures(line_features)

        if error_point_layer.featureCount() > 0:
            # We want to have a feature per pair of ids, so collect several features
            # into a single feature for each pair of ids
            res = processing.run("native:collect", {'INPUT':error_point_layer, 'FIELD':['intersecting_boundaries'],'OUTPUT':'memory:'}, feedback=QgsProcessingFeedback())
            if type(res['OUTPUT']) == QgsVectorLayer:
                error_point_layer = res['OUTPUT']
                error_point_layer.setName(QCoreApplication.translate("QGISUtils", "Overlapping boundaries (point intersections)"))

        if error_line_layer.featureCount() > 0:
            res = processing.run("native:collect", {'INPUT':error_line_layer, 'FIELD':['intersecting_boundaries'],'OUTPUT':'memory:'}, feedback=QgsProcessingFeedback())
            if type(res['OUTPUT']) == QgsVectorLayer:
                error_line_layer = res['OUTPUT']
                error_line_layer.setName(QCoreApplication.translate("QGISUtils","Overlapping boundaries (line intersections)"))

        if error_point_layer.featureCount() > 0 or error_line_layer.featureCount() > 0:
            group = self.qgis_utils.get_error_layers_group()
            msg = ''

            if error_point_layer.featureCount() > 0:
                added_point_layer = QgsProject.instance().addMapLayer(error_point_layer, False)
                added_point_layer = group.addLayer(added_point_layer).layer()
                self.qgis_utils.symbology.set_point_error_symbol(added_point_layer)
                msg = QCoreApplication.translate("QGISUtils",
                    "A memory layer with {} overlapping boundaries (point intersections) has been added to the map.").format(added_point_layer.featureCount())

            if error_line_layer.featureCount() > 0:
                added_line_layer = QgsProject.instance().addMapLayer(error_line_layer, False)
                added_line_layer = group.addLayer(added_line_layer).layer()
                self.qgis_utils.symbology.set_line_error_symbol(added_line_layer)
                msg = QCoreApplication.translate("QGISUtils",
                    "A memory layer with {} overlapping boundaries (line intersections) has been added to the map.").format(added_line_layer.featureCount())

            if error_point_layer.featureCount() > 0 and error_line_layer.featureCount() > 0:
                msg = QCoreApplication.translate("QGISUtils",
                    "Two memory layers with overlapping boundaries ({} point intersections and {} line intersections) have been added to the map.").format(added_point_layer.featureCount(), added_line_layer.featureCount())

            self.qgis_utils.message_emitted.emit(msg, Qgis.Info)
        else:
            self.qgis_utils.message_emitted.emit(
                QCoreApplication.translate("QGISUtils",
                                           "There are no overlapping boundaries."), Qgis.Info)


    def check_too_long_segments(self, db):
        tolerance = int(QSettings().value('Asistente-LADM_COL/quality/too_long_tolerance', DEFAULT_TOO_LONG_BOUNDARY_SEGMENTS_TOLERANCE)) # meters
        features = []
        boundary_layer = self.qgis_utils.get_layer(db, BOUNDARY_TABLE, load=True)

        if boundary_layer is None:
            self.qgis_utils.message_emitted.emit(
                QCoreApplication.translate("QGISUtils",
                                           "Table {} not found in the DB! {}").format(BOUNDARY_TABLE, db.get_description()),
                Qgis.Warning)
            return

        error_layer = QgsVectorLayer("LineString?crs=EPSG:{}".format(DEFAULT_EPSG),
                            QCoreApplication.translate("QGISUtils",
                                "Boundary segments longer than {}m.").format(tolerance),
                            "memory")
        pr = error_layer.dataProvider()
        pr.addAttributes([QgsField("boundary_id", QVariant.Int),
                          QgsField("distance", QVariant.Double)])
        error_layer.updateFields()

        for feature in boundary_layer.getFeatures():
            lines = feature.geometry()
            if lines.isMultipart():
                for part in range(lines.constGet().numGeometries()):
                    line = lines.constGet().geometryN(part)
                    segments_info = self.get_too_long_segments_from_simple_line(line, tolerance)
                    for segment_info in segments_info:
                        new_feature = QgsVectorLayerUtils().createFeature(error_layer, segment_info[0], {0:feature.id(), 1:segment_info[1]})
                        features.append(new_feature)
            else:
                segments_info = self.get_too_long_segments_from_simple_line(lines.constGet(), tolerance)
                for segment_info in segments_info:
                    new_feature = QgsVectorLayerUtils().createFeature(error_layer, segment_info[0], {0:feature.id(), 1:segment_info[1]})
                    features.append(new_feature)

        error_layer.dataProvider().addFeatures(features)
        if error_layer.featureCount() > 0:
            group = self.qgis_utils.get_error_layers_group()
            added_layer = QgsProject.instance().addMapLayer(error_layer, False)
            added_layer = group.addLayer(added_layer).layer()
            self.qgis_utils.symbology.set_line_error_symbol(added_layer)
            self.qgis_utils.message_emitted.emit(
                QCoreApplication.translate("QGISUtils",
                                           "A memory layer with {} boundary segments longer than {}m. has been added to the map!").format(added_layer.featureCount(), tolerance),
                Qgis.Info)
        else:
            self.qgis_utils.message_emitted.emit(
                QCoreApplication.translate("QGISUtils",
                                           "All boundary segments are within the tolerance ({}m.)!").format(tolerance),
                Qgis.Info)

    def check_missing_boundary_points_vertices(self, db):
        features = []
        boundary_point_layer = self.qgis_utils.get_layer(db, BOUNDARY_POINT_TABLE, load=True)
        boundary_layer = self.qgis_utils.get_layer(db, BOUNDARY_TABLE, load=True)

        if boundary_point_layer is None:
            self.message_emitted.emit(
                QCoreApplication.translate("QGISUtils",
                                           "Table {} not found in DB! {}").format(BOUNDARY_POINT_TABLE, db.get_description()),
                Qgis.Warning)
            return

        if boundary_layer is None:
            self.message_emitted.emit(
                QCoreApplication.translate("QGISUtils",
                                           "Table {} not found in DB! {}").format(BOUNDARY_TABLE, db.get_description()),
                Qgis.Warning)
            return

        error_layer = QgsVectorLayer("Point?crs=EPSG:{}".format(DEFAULT_EPSG), "Missing boundary points vertices", "memory")
        data_provider = error_layer.dataProvider()
        data_provider.addAttributes([QgsField("point_count", QVariant.Int)])
        error_layer.updateFields()

        missing_points = self.get_missing_boundary_points_vertices(boundary_point_layer, boundary_layer)

        for item in missing_points:
            new_feature = QgsVectorLayerUtils().createFeature(error_layer, item)
            data_provider.addFeature(new_feature)

        if error_layer.featureCount() > 0:
            group = self.qgis_utils.get_error_layers_group()
            added_layer = QgsProject.instance().addMapLayer(error_layer, False)
            added_layer = group.addLayer(added_layer).layer()
            self.qgis_utils.symbology.set_point_error_symbol(added_layer)

            self.qgis_utils.message_emitted.emit(
            QCoreApplication.translate("QGISUtils",
                                            "A memory layer with {} missing Boundary Points vertices has been added to the map!").format(added_layer.featureCount()), Qgis.Info)
        else:
            self.qgis_utils.message_emitted.emit(
                QCoreApplication.translate("QGISUtils",
                                           "There are no missing boundary points vertices."), Qgis.Info)

    def get_too_long_segments_from_simple_line(self, line, tolerance):
        segments_info = list()
        vertices = line.vertices()
        vertex1 = None
        if vertices.hasNext():
            vertex1 = vertices.next()
        while vertices.hasNext():
            vertex2 = vertices.next()
            distance = vertex1.distance(vertex2)
            if distance > tolerance:
                segment = QgsGeometry.fromPolyline([vertex1, vertex2])
                segments_info.append([segment, distance])
            vertex1 = vertex2
        return segments_info

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

    def get_missing_boundary_points_vertices(self, point_layer, boundary_layer):

        res = list()

        feedback = QgsProcessingFeedback()
        extracted_vertices = processing.run("native:extractvertices", {'INPUT':boundary_layer,'OUTPUT':'memory:'}, feedback=feedback)
        extracted_vertices_layer = extracted_vertices['OUTPUT']
        cleaned_vertices = processing.run("qgis:deleteduplicategeometries", {'INPUT':extracted_vertices_layer,'OUTPUT':'memory:'}, feedback=feedback)
        cleaned_vertices_layer = cleaned_vertices['OUTPUT']

        context = createContext()
        indexB = QgsSpatialIndex(point_layer.getFeatures(QgsFeatureRequest().setSubsetOfAttributes([]).setDestinationCrs(cleaned_vertices_layer.sourceCrs(), context.transformContext())), feedback)

        for featA in cleaned_vertices_layer.getFeatures():
            if featA.hasGeometry():
                geom = featA.geometry()
                diff_geom = QgsGeometry(geom)
                point_vert = {'x':diff_geom.asPoint().x(),'y':diff_geom.asPoint().y()}
                bbox = QgsRectangle(QgsPointXY(point_vert['x']-0.0001,point_vert['y']-0.0001),QgsPointXY(point_vert['x']+0.0001,point_vert['y']+0.0001))
                intersects = indexB.intersects(bbox)
                if intersects:
                    pass #Don't insert intersection points
                else:
                    res.append(diff_geom)
        return res
