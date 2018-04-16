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
    QgsWkbTypes
)
from qgis.PyQt.QtCore import QObject, QCoreApplication, QVariant, QSettings
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

        overlapping = self.qgis_utils.geometry.get_overlapping_points(boundary_point_layer)

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

        overlapping = self.qgis_utils.geometry.get_overlapping_lines(boundary_layer)
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
