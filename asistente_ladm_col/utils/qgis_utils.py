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
import os

from qgis.core import (QgsGeometry, QgsLineString, QgsDefaultValue, QgsProject,
                       QgsWkbTypes, QgsVectorLayerUtils, QgsDataSourceUri, Qgis,
                       QgsSpatialIndex, QgsVectorLayer, QgsMultiLineString)
from qgis.PyQt.QtCore import QObject, pyqtSignal, QCoreApplication

from ..config.table_mapping_config import (BFS_TABLE_BOUNDARY_FIELD,
                                           BFS_TABLE_BOUNDARY_POINT_FIELD,
                                           BOUNDARY_POINT_TABLE,
                                           BOUNDARY_TABLE,
                                           ID_FIELD,
                                           LESS_TABLE,
                                           LESS_TABLE_BOUNDARY_FIELD,
                                           LESS_TABLE_PLOT_FIELD,
                                           PLOT_TABLE,
                                           MOREBFS_TABLE_PLOT_FIELD,
                                           MOREBFS_TABLE_BOUNDARY_FIELD,
                                           MORE_BOUNDARY_FACE_STRING_TABLE,
                                           POINT_BOUNDARY_FACE_STRING_TABLE,
                                           VIDA_UTIL_FIELD_BOUNDARY_TABLE)

class QGISUtils(QObject):

    message_emitted = pyqtSignal(str, int) # Message, level
    message_with_button_load_layer_emitted = pyqtSignal(str, str, list, int) # Message, button text, callback, level
    map_refresh_requested = pyqtSignal()
    zoom_full_requested = pyqtSignal()
    zoom_to_selected_requested = pyqtSignal()

    def __init__(self):
        QObject.__init__(self)

    def get_layer(self, db, layer_name, geometry_type=None, load=False):
        # If layer is in LayerTree, return it
        layer = self.get_layer_from_layer_tree(layer_name, db.schema, geometry_type)
        if layer is not None:
            return layer

        # Layer is not loaded, create it and load it if 'load' is True
        res, uri = db.get_uri_for_layer(layer_name, geometry_type)
        if not res:
            return None

        layer = QgsVectorLayer(uri, layer_name.capitalize(), db.provider)
        if layer.isValid():
            if load:
                QgsProject.instance().addMapLayer(layer)
            return layer

        return None

    def get_layer_from_layer_tree(self, layer_name, schema=None, geometry_type=None):
        for k,layer in QgsProject.instance().mapLayers().items():
            if layer.dataProvider().name() == 'postgres':
                if QgsDataSourceUri(layer.source()).table() == layer_name.lower() and \
                    QgsDataSourceUri(layer.source()).schema() == schema:
                    if geometry_type is not None:
                        if layer.geometryType() == geometry_type:
                            return layer
                    else:
                        return layer
            else:
                if '|layername=' in layer.source(): # GeoPackage layers
                    if layer.source().split()[-1] == layer_name.lower():
                        if geometry_type is not None:
                            if layer.geometryType() == geometry_type:
                                return layer
                        else:
                            return layer
        return None

    def configureAutomaticField(self, layer, field, expression):
        index = layer.fields().indexFromName(field)
        default_value = QgsDefaultValue(expression, True)
        layer.setDefaultValueDefinition(index, default_value)


    def copy_csv_to_db(self, csv_path, delimiter, longitude, latitude, db, target_layer_name):
        if not csv_path or not os.path.exists(csv_path):
            self.message_emitted.emit(
                QCoreApplication.translate("QGISUtils",
                                           "No CSV file given or file doesn't exist."),
                Qgis.Warning)
            return False

        # Create QGIS vector layer
        uri = "file:///{}?delimiter={}&xField={}&yField={}&crs=EPSG:3116".format(
              csv_path,
              delimiter,
              longitude,
              latitude
           )
        csv_layer = QgsVectorLayer(uri, os.path.basename(csv_path), "delimitedtext")
        if not csv_layer.isValid():
            self.message_emitted.emit(
                QCoreApplication.translate("QGISUtils",
                                           "CSV layer not valid!"),
                Qgis.Warning)
            return False

        overlapping = self.validate_non_overlapping_points(csv_layer)
        if overlapping:
            self.message_emitted.emit(
                QCoreApplication.translate("QGISUtils",
                                           "There are overlapping points, we cannot import them into the DB! See selected points."),
                Qgis.Warning)
            QgsProject.instance().addMapLayer(csv_layer)
            csv_layer.selectByIds(overlapping)
            self.zoom_to_selected_requested.emit()
            return False

        target_point_layer = self.get_layer(db, target_layer_name, load=True)
        if target_point_layer is None:
            self.message_emitted.emit(
                QCoreApplication.translate("QGISUtils",
                                           "The point layer '{}' couldn't be found in the DB...").format(target_layer_name),
                Qgis.Warning)
            return False

        # Define a mapping between CSV and target layer
        mapping = dict()
        for target_idx in target_point_layer.fields().allAttributesList():
            target_field = target_point_layer.fields().field(target_idx)
            csv_idx = csv_layer.fields().indexOf(target_field.name())
            if csv_idx != -1 and target_field.name() != ID_FIELD:
                mapping[target_idx] = csv_idx

        # Copy and Paste
        new_features = []
        for in_feature in csv_layer.getFeatures():
            attrs = {target_idx: in_feature[csv_idx] for target_idx, csv_idx in mapping.items()}
            new_feature = QgsVectorLayerUtils().createFeature(target_point_layer, in_feature.geometry(), attrs)
            new_features.append(new_feature)

        target_point_layer.dataProvider().addFeatures(new_features)

        #self.iface.copySelectionToClipboard(csv_layer)
        #target_point_layer.startEditing()
        #self.iface.pasteFromClipboard(target_point_layer)
        #target_point_layer.commitChanges()

        QgsProject.instance().addMapLayer(target_point_layer)
        self.zoom_full_requested.emit()
        self.message_emitted.emit(
            QCoreApplication.translate("QGISUtils",
                                       "{} points were added succesfully to '{}'.").format(len(new_features), target_layer_name),
            Qgis.Info)
        return True

    def validate_non_overlapping_points(self, point_layer):
        # Validate non-overlapping points
        index = QgsSpatialIndex(point_layer.getFeatures())
        for feature in point_layer.getFeatures():
            res = index.intersects(feature.geometry().boundingBox())
            if len(res) > 1:
                return res
        return []

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
            self.message_with_button_load_layer_emitted.emit(
                QCoreApplication.translate("QGISUtils",
                                           "First load the layer {} into QGIS!").format(BOUNDARY_TABLE),
                QCoreApplication.translate("QGISUtils",
                                           "Load layer {} now").format(BOUNDARY_TABLE),
                [BOUNDARY_TABLE],
                Qgis.Warning)
            return

        num_boundaries = len(layer.selectedFeatures())
        if num_boundaries == 0:
            self.message_emitted.emit(
                QCoreApplication.translate("QGISUtils",
                                           "First select at least one boundary!"),
                Qgis.Warning)
            return

        segments = list()
        for f in layer.selectedFeatures():
            segments.extend(self.extractAsSingleSegments(f.geometry()))

        layer.startEditing() # Safe, even if layer is already on editing state

        # Remove the selected lines, we'll add exploded segments in a while
        layer.deleteFeatures([sf.id() for sf in layer.selectedFeatures()])

        # Create features based on segment geometries
        exploded_features = list()
        for segment in segments:
            feature = QgsVectorLayerUtils().createFeature(layer, segment)
            exploded_features.append(feature)

        layer.addFeatures(exploded_features)
        self.message_emitted.emit(
            QCoreApplication.translate("QGISUtils",
                                       "{} feature(s) was/were exploded generating {} feature(s).").format(num_boundaries, len(exploded_features)),
            Qgis.Info)
        self.map_refresh_requested.emit()

    def merge_boundaries(self, db):
        layer = self.get_layer_from_layer_tree(BOUNDARY_TABLE, db.schema)
        if layer is None:
            self.message_with_button_load_layer_emitted.emit(
                QCoreApplication.translate("QGISUtils",
                                           "First load the layer {} into QGIS!").format(BOUNDARY_TABLE),
                QCoreApplication.translate("QGISUtils", "Load layer {} now").format(BOUNDARY_TABLE),
                [BOUNDARY_TABLE],
                Qgis.Warning)
            return

        if len(layer.selectedFeatures()) < 2:
            self.message_emitted.emit(
                QCoreApplication.translate("QGISUtils", "First select at least 2 boundaries!"),
                Qgis.Warning)
            return

        num_boundaries = len(layer.selectedFeatures())
        unionGeom = layer.selectedFeatures()[0].geometry()
        for f in layer.selectedFeatures()[1:]:
            if not f.geometry().isNull():
                unionGeom = unionGeom.combine(f.geometry())

        layer.startEditing() # Safe, even if layer is already on editing state

        # Remove the selected lines, we'll add exploded segments in a while
        layer.deleteFeatures([sf.id() for sf in layer.selectedFeatures()])

        # Convert to multipart geometry if needed
        if QgsWkbTypes.isMultiType(layer.wkbType()) and not unionGeom.isMultipart():
            unionGeom.convertToMultiType()

        feature = QgsVectorLayerUtils().createFeature(layer, unionGeom)
        layer.addFeature(feature)
        self.message_emitted.emit(
            QCoreApplication.translate("QGISUtils", "{} features were merged!").format(num_boundaries),
            Qgis.Info)
        self.map_refresh_requested.emit()

    def fill_topology_table_pointbfs(self, db, use_selection=True):
        boundary_layer = self.get_layer(db, BOUNDARY_TABLE)
        if boundary_layer is None:
            self.message_emitted.emit(
                QCoreApplication.translate("QGISUtils",
                                           "Table {} not found in the DB!").format(BOUNDARY_TABLE),
                Qgis.Warning)
            return
        if use_selection and boundary_layer.selectedFeatureCount() == 0:
            if self.get_layer_from_layer_tree(BOUNDARY_TABLE, schema=db.schema) is None:
                self.message_with_button_load_layer_emitted.emit(
                    QCoreApplication.translate("QGISUtils",
                                               "First load the layer {} into QGIS and select at least one boundary!").format(BOUNDARY_TABLE),
                    QCoreApplication.translate("QGISUtils", "Load layer {} now").format(BOUNDARY_TABLE),
                    [BOUNDARY_TABLE],
                    Qgis.Warning)
            else:
                self.message_emitted.emit(
                    QCoreApplication.translate("QGISUtils", "First select at least one boundary!"),
                    Qgis.Warning)
            return

        bfs_layer = self.get_layer(db, POINT_BOUNDARY_FACE_STRING_TABLE, load=True)
        if bfs_layer is None:
            self.message_emitted.emit(
                QCoreApplication.translate("QGISUtils", "Table {} not found in the DB!").format(POINT_BOUNDARY_FACE_STRING_TABLE),
                Qgis.Warning)
            return

        bfs_features = bfs_layer.getFeatures()

        # Get unique pairs id_boundary-id_boundary_point
        existing_pairs = [(bfs_feature[BFS_TABLE_BOUNDARY_FIELD], bfs_feature[BFS_TABLE_BOUNDARY_POINT_FIELD]) for bfs_feature in bfs_features]
        existing_pairs = set(existing_pairs)

        boundary_point_layer = self.get_layer(db, BOUNDARY_POINT_TABLE)
        id_pairs = self.get_pair_boundary_boundary_point(boundary_layer, boundary_point_layer, use_selection)

        if id_pairs:
            bfs_layer.startEditing()
            features = list()
            for id_pair in id_pairs:
                if not id_pair in existing_pairs: # Avoid duplicated pairs in the DB
                    # Create feature
                    feature = QgsVectorLayerUtils().createFeature(bfs_layer)
                    feature.setAttribute(BFS_TABLE_BOUNDARY_FIELD, id_pair[0])
                    feature.setAttribute(BFS_TABLE_BOUNDARY_POINT_FIELD, id_pair[1])
                    features.append(feature)
            bfs_layer.addFeatures(features)
            bfs_layer.commitChanges()
            self.message_emitted.emit(
                QCoreApplication.translate("QGISUtils",
                                           "{} out of {} records were saved into {}! {} out of {} records already existed in the database.").format(
                    len(features),
                    len(id_pairs),
                    POINT_BOUNDARY_FACE_STRING_TABLE,
                    len(id_pairs) - len(features),
                    len(id_pairs)
                ),
                Qgis.Info)
        else:
            self.message_emitted.emit(
                QCoreApplication.translate("QGISUtils", "No pairs id_boundary-id_boundary_point found."),
                Qgis.Info)

    def get_pair_boundary_boundary_point(self, boundary_layer, boundary_point_layer, use_selection=True):
        lines = boundary_layer.getSelectedFeatures() if use_selection else boundary_layer.getFeatures()
        points = boundary_point_layer.getFeatures()
        index = QgsSpatialIndex(boundary_point_layer)
        intersect_pairs = list()
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
                        intersect_pairs.append((line[ID_FIELD], candidate_feature[ID_FIELD]))
        return intersect_pairs

    def fill_topology_tables_morebfs_less(self, db, use_selection=True):
        plot_layer = self.get_layer(db, PLOT_TABLE, QgsWkbTypes.PolygonGeometry)
        if plot_layer is None:
            self.message_emitted.emit(
                QCoreApplication.translate("QGISUtils", "Table {} not found in the DB!").format(PLOT_TABLE),
                Qgis.Warning)
            return

        if use_selection and plot_layer.selectedFeatureCount() == 0:
            if self.get_layer_from_layer_tree(PLOT_TABLE, schema=db.schema, geometry_type=QgsWkbTypes.PolygonGeometry) is None:
                self.message_with_button_load_layer_emitted.emit(
                    QCoreApplication.translate("QGISUtils",
                                               "First load the layer {} into QGIS and select at least one plot!").format(PLOT_TABLE),
                    QCoreApplication.translate("QGISUtils", "Load layer {} now").format(PLOT_TABLE),
                    [PLOT_TABLE],
                    Qgis.Warning)
            else:
                self.message_emitted.emit(
                    QCoreApplication.translate("QGISUtils", "First select at least one plot!"),
                    Qgis.Warning)
            return

        more_bfs_layer = self.get_layer(db, MORE_BOUNDARY_FACE_STRING_TABLE, load=True)
        if more_bfs_layer is None:
            self.message_emitted.emit(
                QCoreApplication.translate("QGISUtils", "Table {} not found in the DB!").format(MORE_BOUNDARY_FACE_STRING_TABLE),
                Qgis.Warning)
            return

        less_layer = self.get_layer(db, LESS_TABLE, load=True)
        if less_layer is None:
            self.message_emitted.emit(
                QCoreApplication.translate("QGISUtils", "Table {} not found in the DB!").format(LESS_TABLE),
                Qgis.Warning)
            return

        more_bfs_features = more_bfs_layer.getFeatures()
        less_features = less_layer.getFeatures()

        # Get unique pairs id_boundary-id_plot in both tables
        existing_more_pairs = [(more_bfs_feature[MOREBFS_TABLE_PLOT_FIELD], more_bfs_feature[MOREBFS_TABLE_BOUNDARY_FIELD]) for more_bfs_feature in more_bfs_features]
        existing_more_pairs = set(existing_more_pairs)
        existing_less_pairs = [(less_feature[LESS_TABLE_PLOT_FIELD], less_feature[LESS_TABLE_BOUNDARY_FIELD]) for less_feature in less_features]
        existing_less_pairs = set(existing_less_pairs)

        boundary_layer = self.get_layer(db, BOUNDARY_TABLE)
        id_more_pairs, id_less_pairs = self.get_pair_boundary_plot(boundary_layer, plot_layer, use_selection)

        if id_more_pairs:
            more_bfs_layer.startEditing()
            features = list()
            for id_pair in id_more_pairs:
                if not id_pair in existing_more_pairs: # Avoid duplicated pairs in the DB
                    # Create feature
                    feature = QgsVectorLayerUtils().createFeature(more_bfs_layer)
                    feature.setAttribute(MOREBFS_TABLE_PLOT_FIELD, id_pair[0])
                    feature.setAttribute(MOREBFS_TABLE_BOUNDARY_FIELD, id_pair[1])
                    features.append(feature)
            more_bfs_layer.addFeatures(features)
            more_bfs_layer.commitChanges()
            self.message_emitted.emit(
                QCoreApplication.translate("QGISUtils", "{} out of {} records were saved into '{}'! {} out of {} records already existed in the database.").format(
                    len(features),
                    len(id_more_pairs),
                    MORE_BOUNDARY_FACE_STRING_TABLE,
                    len(id_more_pairs) - len(features),
                    len(id_more_pairs)
                ),
                Qgis.Info)
        else:
            self.message_emitted.emit(
                QCoreApplication.translate("QGISUtils", "No pairs id_boundary-id_plot found for '{}' table.".format(MORE_BOUNDARY_FACE_STRING_TABLE)),
                Qgis.Info)

        if id_less_pairs:
            less_layer.startEditing()
            features = list()
            for id_pair in id_less_pairs:
                if not id_pair in existing_less_pairs: # Avoid duplicated pairs in the DB
                    # Create feature
                    feature = QgsVectorLayerUtils().createFeature(less_layer)
                    feature.setAttribute(LESS_TABLE_PLOT_FIELD, id_pair[0])
                    feature.setAttribute(LESS_TABLE_BOUNDARY_FIELD, id_pair[1])
                    features.append(feature)
            less_layer.addFeatures(features)
            less_layer.commitChanges()
            self.message_emitted.emit(
                QCoreApplication.translate("QGISUtils", "{} out of {} records were saved into '{}'! {} out of {} records already existed in the database.").format(
                    len(features),
                    len(id_less_pairs),
                    LESS_TABLE,
                    len(id_less_pairs) - len(features),
                    len(id_less_pairs)
                ),
                Qgis.Info)
        else:
            self.message_emitted.emit(
                QCoreApplication.translate("QGISUtils", "No pairs id_boundary-id_plot found for '{}' table.".format(MORE_BOUNDARY_FACE_STRING_TABLE)),
                Qgis.Info)

    def get_pair_boundary_plot(self, boundary_layer, plot_layer, use_selection=True):
        lines = boundary_layer.getFeatures()
        polygons = plot_layer.getSelectedFeatures() if use_selection else plot_layer.getFeatures()
        index = QgsSpatialIndex(boundary_layer)
        intersect_more_pairs = list()
        intersect_less_pairs = list()

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

                        if QgsGeometry(multi_outer_rings).intersection(candidate_geometry).type() == QgsWkbTypes.LineGeometry:
                            intersect_more_pairs.append((polygon[ID_FIELD], candidate_feature[ID_FIELD]))
                        if QgsGeometry(multi_inner_rings).intersection(candidate_geometry).type() == QgsWkbTypes.LineGeometry:
                            intersect_less_pairs.append((polygon[ID_FIELD], candidate_feature[ID_FIELD]))

                    else:
                        boundary = None
                        if is_multipart and multi_polygon:
                            boundary = multi_polygon.boundary()
                        elif not is_multipart and single_polygon:
                            boundary = single_polygon.boundary()

                        if boundary and QgsGeometry(boundary).intersection(candidate_geometry).type() == QgsWkbTypes.LineGeometry:
                            intersect_more_pairs.append((polygon[ID_FIELD], candidate_feature[ID_FIELD]))

        return (intersect_more_pairs, intersect_less_pairs)

    def polygonize_boundaries(self, db):
        boundaries = self.get_layer(db, BOUNDARY_TABLE)
        if boundaries is None:
            self.message_emitted.emit(
                QCoreApplication.translate("QGISUtils", "Layer {} not found in the DB!").format(BOUNDARY_TABLE),
                Qgis.Warning)
            return
        selected_boundaries = boundaries.selectedFeatures()
        if not selected_boundaries:
            self.message_emitted.emit(
                QCoreApplication.translate("QGISUtils", "First select boundaries!"),
                Qgis.Warning)
            return

        plots = self.get_layer(db, PLOT_TABLE, QgsWkbTypes.PolygonGeometry, load=True)
        if plots is None:
            self.message_emitted.emit(
                QCoreApplication.translate("QGISUtils", "Layer {} not found in the DB!").format(PLOT_TABLE),
                Qgis.Warning)
            return

        boundary_geometries = [f.geometry() for f in selected_boundaries]
        collection = QgsGeometry().polygonize(boundary_geometries)
        features = list()
        self.configureAutomaticField(plots, VIDA_UTIL_FIELD_BOUNDARY_TABLE, "now()")
        for polygon in collection.asGeometryCollection():
            feature = QgsVectorLayerUtils().createFeature(plots, polygon)
            features.append(feature)

        if features:
            plots.startEditing()
            plots.addFeatures(features)
            self.map_refresh_requested.emit()
            self.message_emitted.emit(
                QCoreApplication.translate("QGISUtils", "{} new plot(s) has(have) been created!").format(len(features)),
                Qgis.Info)
        else:
            self.message_emitted.emit(
                QCoreApplication.translate("QGISUtils", "No plot could be created. Make sure selected boundaries are closed!"),
                Qgis.Warning)
            return
