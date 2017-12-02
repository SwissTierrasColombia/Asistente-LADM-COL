# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2017-11-14
        git sha              : :%H$
        copyright            : (C) 2017 by Germán Carrillo (BSF Swissphoto)
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
from qgis.core import (QgsGeometry, QgsLineString, QgsDefaultValue, QgsProject,
                       QgsWkbTypes, QgsVectorLayerUtils, QgsDataSourceUri,
                       QgsSpatialIndex, QgsVectorLayer)
from qgis.gui import QgsMessageBar
from qgis.PyQt.QtCore import QObject, pyqtSignal

from ..config.table_mapping_config import (BOUNDARY_POINT_TABLE,
                                           BOUNDARY_TABLE,
                                           CCL_TABLE_BOUNDARY_FIELD,
                                           CCL_TABLE_BOUNDARY_POINT_FIELD,
                                           ID_FIELD,
                                           POINT_BOUNDARY_FACE_STRING_TABLE)

class QGISUtils(QObject):

    message_emitted = pyqtSignal(str, int) # Message, level
    map_refresh_requested = pyqtSignal()

    def __init__(self):
        QObject.__init__(self)

    def get_layer(self, db, layer_name, load=False):
        # If layer is in LayerTree, return it
        layer = self.get_layer_from_layer_tree(layer_name, db.schema)
        if layer is not None:
            return layer

        # Layer is not loaded, create it and load it if 'load' is True
        res, uri = db.get_uri_for_layer(layer_name)
        if not res:
            print("uri",uri)
            return None

        layer = QgsVectorLayer(uri, layer_name.capitalize(), db.provider)
        if layer.isValid():
            if load:
                QgsProject.instance().addMapLayer(layer)
            return layer

        return None

    def get_layer_from_layer_tree(self, layer_name, schema=None):
        for k,layer in QgsProject.instance().mapLayers().items():
            if layer.dataProvider().name() == 'postgres':
                if QgsDataSourceUri(layer.source()).table() == layer_name.lower() and \
                    QgsDataSourceUri(layer.source()).schema() == schema:
                    return layer
            else:
                if '|layername=' in layer.source(): # GeoPackage layers
                    if layer.source().split()[-1] == layer_name.lower():
                        return layer
        return None

    def configureAutomaticField(self, layer, field, expression):
        index = layer.fields().indexFromName(field)
        default_value = QgsDefaultValue(expression, True)
        layer.setDefaultValueDefinition(index, default_value)

    def extractAsSingleSegments(self, geom):
        """
        Copied from:
        https://github.com/qgis/QGIS/blob/55203a0fc2b8e35fa2909da77a84bbfde8fcba5c/python/plugins/processing/algs/qgis/Explode.py#L89
        """
        segments = []
        if geom.isMultipart():
            for part in range(geom.constGet().numGeometries()):
                segments.extend(self.getPolylineAsSingleSegments(geom.constGet().geometryN(part)))
        else:
            segments.extend(self.getPolylineAsSingleSegments(geom.constGet()))
        return segments

    def getPolylineAsSingleSegments(self, polyline):
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

    def explode_boundaries(self, db):
        layer = self.get_layer_from_layer_tree(BOUNDARY_TABLE, db.schema)

        if layer is None:
            self.message_emitted.emit(self.tr("First load the layer {}!".format(BOUNDARY_TABLE)), QgsMessageBar.WARNING)
            return

        num_boundaries = len(layer.selectedFeatures())
        if num_boundaries == 0:
            self.message_emitted.emit(self.tr("First select at least a boundary!"), QgsMessageBar.WARNING)
            return

        segments = list()
        for f in layer.selectedFeatures():
            segments.extend(self.extractAsSingleSegments(f.geometry()))

        # Remove the selected lines, we'll add exploded segments in a while
        layer.deleteFeatures([sf.id() for sf in layer.selectedFeatures()])

        # Create features based on segment geometries
        exploded_features = list()
        for segment in segments:
            feature = QgsVectorLayerUtils().createFeature(layer, segment)
            exploded_features.append(feature)

        layer.addFeatures(exploded_features)
        self.message_emitted.emit(self.tr("{} feature(s) was/were exploded generating {} feature(s).".format(num_boundaries, len(exploded_features))), QgsMessageBar.INFO)
        self.map_refresh_requested.emit()

    def merge_boundaries(self, db):
        layer = self.get_layer_from_layer_tree(BOUNDARY_TABLE, db.schema)
        if layer is None:
            self.message_emitted.emit(self.tr("First load the layer {}!".format(BOUNDARY_TABLE)), QgsMessageBar.WARNING)
            return

        if len(layer.selectedFeatures()) < 2:
            self.message_emitted.emit(self.tr("Select at least 2 boundaries!"), QgsMessageBar.WARNING)
            return

        num_boundaries = len(layer.selectedFeatures())
        unionGeom = layer.selectedFeatures()[0].geometry()
        for f in layer.selectedFeatures()[1:]:
            if not f.geometry().isNull():
                unionGeom = unionGeom.combine(f.geometry())

        # Remove the selected lines, we'll add exploded segments in a while
        layer.deleteFeatures([sf.id() for sf in layer.selectedFeatures()])

        # Convert to mulipart geometry if needed
        if QgsWkbTypes.isMultiType(layer.wkbType()) and not unionGeom.isMultipart():
            unionGeom.convertToMultiType()

        feature = QgsVectorLayerUtils().createFeature(layer, unionGeom)
        layer.addFeature(feature)
        self.message_emitted.emit(self.tr("{} features were merged!".format(num_boundaries)), QgsMessageBar.INFO)
        self.map_refresh_requested.emit()

    def fill_topology_table_pointbfs(self, db):
        print(db.get_description())
        bfs_layer = self.get_layer(db, POINT_BOUNDARY_FACE_STRING_TABLE, True)
        print("puntoccl found:", bfs_layer is not None)
        bfs_features = bfs_layer.getFeatures()

        # Get unique pairs id_boundary-id_boundary_point
        existing_pairs = [(bfs_feature[CCL_TABLE_BOUNDARY_FIELD], bfs_feature[CCL_TABLE_BOUNDARY_POINT_FIELD]) for bfs_feature in bfs_features]
        existing_pairs = set(existing_pairs)

        boundary_layer = self.get_layer(db, BOUNDARY_TABLE)
        boundary_point_layer = self.get_layer(db, BOUNDARY_POINT_TABLE)
        id_pairs = self.get_pair_boundary_boundary_point(boundary_layer, boundary_point_layer)

        if id_pairs:
            bfs_layer.startEditing()
            features = list()
            for id_pair in id_pairs:
                if not id_pair in existing_pairs: # Avoid duplicated pairs in the DB
                    # Create feature
                    feature = QgsVectorLayerUtils().createFeature(bfs_layer)
                    feature.setAttribute(CCL_TABLE_BOUNDARY_FIELD, id_pair[0])
                    feature.setAttribute(CCL_TABLE_BOUNDARY_POINT_FIELD, id_pair[1])
                    features.append(feature)
                    print(id_pair)
            bfs_layer.addFeatures(features)
            bfs_layer.commitChanges()
            print("{} out of {} records were saved into {}! {} records already existed in the database.".format(
                len(features),
                len(id_pairs),
                POINT_BOUNDARY_FACE_STRING_TABLE,
                len(id_pairs) - len(features)
            ))
        else:
            print("No pairs id_boundary-id_boundary_point found.")

    def get_pair_boundary_boundary_point(self, boundary_layer, boundary_point_layer):
        lines = boundary_layer.getSelectedFeatures()
        points = boundary_point_layer.getFeatures()
        index = QgsSpatialIndex(boundary_point_layer)
        intersect_pairs = list()
        for line in lines:
            bbox = line.geometry().boundingBox()
            bbox.scale(1.001)
            candidates_ids = index.intersects(bbox)
            #print(candidates_ids)
            candidates_features = boundary_point_layer.getFeatures(candidates_ids)
            for candidate_feature in candidates_features:
                #if line.geometry().intersects(candidate_feature.geometry()):
                #    intersect_pair.append(line['t_id'], candidate_feature['t_id'])
                candidate_point = candidate_feature.geometry().asPoint()
                for line_vertex in line.geometry().asPolyline():
                    if abs(line_vertex.x() - candidate_point.x()) < 0.001 \
                       and abs(line_vertex.y() - candidate_point.y()) < 0.001:
                        intersect_pairs.append((line[ID_FIELD], candidate_feature[ID_FIELD]))
        return intersect_pairs
