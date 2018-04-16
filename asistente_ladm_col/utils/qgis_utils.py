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
                       QgsSpatialIndex, QgsVectorLayer, QgsMultiLineString,
                       QgsField,
                       QgsMapLayer,
                       QgsPointXY,
                       QgsMultiPoint, QgsMultiLineString, QgsGeometryCollection,
                       QgsApplication, QgsProcessingFeedback)
from qgis.PyQt.QtCore import (Qt, QObject, pyqtSignal, QCoreApplication,
                              QVariant, QSettings)
import processing

from .project_generator_utils import ProjectGeneratorUtils
from .qt_utils import OverrideCursor
from .symbology import SymbologyUtils
from ..gui.settings_dialog import SettingsDialog
from ..config.table_mapping_config import (BFS_TABLE_BOUNDARY_FIELD,
                                           BFS_TABLE_BOUNDARY_POINT_FIELD,
                                           BOUNDARY_POINT_TABLE,
                                           BOUNDARY_TABLE,
                                           DEFAULT_EPSG,
                                           DEFAULT_TOO_LONG_BOUNDARY_SEGMENTS_TOLERANCE,
                                           ERROR_LAYER_GROUP,
                                           ID_FIELD,
                                           LENGTH_FIELD_BOUNDARY_TABLE,
                                           LESS_TABLE,
                                           LESS_TABLE_BOUNDARY_FIELD,
                                           LESS_TABLE_PLOT_FIELD,
                                           LOCAL_ID_FIELD,
                                           PLOT_TABLE,
                                           MOREBFS_TABLE_PLOT_FIELD,
                                           MOREBFS_TABLE_BOUNDARY_FIELD,
                                           MORE_BOUNDARY_FACE_STRING_TABLE,
                                           NAMESPACE_FIELD,
                                           NAMESPACE_PREFIX,
                                           POINT_BOUNDARY_FACE_STRING_TABLE,
                                           VIDA_UTIL_FIELD)
from ..config.refactor_fields_mappings import get_refactor_fields_mapping

class QGISUtils(QObject):

    layer_symbology_changed = pyqtSignal(str) # layer id
    message_emitted = pyqtSignal(str, int) # Message, level
    message_with_button_load_layer_emitted = pyqtSignal(str, str, list, int) # Message, button text, [layer_name, geometry_type], level
    message_with_button_load_layers_emitted = pyqtSignal(str, str, dict, int) # Message, button text, layers_dict, level
    map_refresh_requested = pyqtSignal()
    zoom_full_requested = pyqtSignal()
    zoom_to_selected_requested = pyqtSignal()

    def __init__(self):
        QObject.__init__(self)
        self.project_generator_utils = ProjectGeneratorUtils()
        self.symbology = SymbologyUtils()
        self.__settings_dialog = None

    def set_db_connection(self, mode, dict_conn):
        """
        Set plugin's main DB connection manually

        mode: 'pg' or 'gpkg'
        dict_conn: key-values (host, port, database, schema, user, password, dbfile)
        """
        self.get_settings_dialog().set_db_connection(mode, dict_conn)

    def get_settings_dialog(self):
        self.__settings_dialog = SettingsDialog(qgis_utils=self)
        return self.__settings_dialog

    def get_db_connection(self):
        self.__settings_dialog = self.get_settings_dialog()
        return self.__settings_dialog.get_db_connection()

    def get_layer(self, db, layer_name, geometry_type=None, load=False):
        # Handy function to avoid sending a whole dict when all we need is a single table/layer
        res_layer = self.get_layers(db, {layer_name: {'name': layer_name, 'geometry': geometry_type}}, load)
        return res_layer[layer_name]

    def get_layers(self, db, layers, load=False):
        # layers = {layer_id : {name: ABC, geometry: DEF}}
        # layer_id should match layer_name most of the times, but if the same
        # layer has multiple geometries, layer_id should contain the geometry
        # type to make the layer_id unique

        # Response is a dict like this:
        # layers = {layer_id: layer_object} layer_object might be None
        response_layers = dict()

        with OverrideCursor(Qt.WaitCursor):
            for layer_id, layer_info in layers.items():
                # If layer is in LayerTree, return it
                layer_obj = self.get_layer_from_layer_tree(layer_info['name'], db.schema, layer_info['geometry'])
                response_layers[layer_id] = layer_obj

            if load:
                layers_to_load = [layers[layer_id]['name'] for layer_id, layer_obj in response_layers.items() if layer_obj is None]
                if layers_to_load:
                    self.project_generator_utils.load_layers(layers_to_load, db)

                    # Once load_layers() is called, go through the layer tree to get
                    # newly added layers
                    missing_layers = {layer_id: {'name': layers[layer_id]['name'], 'geometry': layers[layer_id]['geometry']} for layer_id, layer_obj in response_layers.items() if layer_obj is None}
                    for layer_id, layer_info in missing_layers.items():
                        # This should update None objects to newly added layer objects
                        response_layers[layer_id] = self.get_layer_from_layer_tree(layer_info['name'], db.schema, layer_info['geometry'])

                        if response_layers[layer_id] is not None:
                            self.post_load_configurations(response_layers[layer_id])

        return response_layers

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

    def get_ladm_layers_from_layer_tree(self, db):
        ladm_layers = list()

        for k,layer in QgsProject.instance().mapLayers().items():
            if db.mode == 'pg':
                if layer.dataProvider().name() == 'postgres':

                    layer_uri = layer.dataProvider().uri()
                    db_uri = QgsDataSourceUri(db.uri)

                    if layer_uri.schema() == db.schema and \
                       layer_uri.database() == db_uri.database() and \
                       layer_uri.host() == db_uri.host() and \
                       layer_uri.port() == db_uri.port() and \
                       layer_uri.username() == db_uri.username() and \
                       layer_uri.password() == db_uri.password():

                        ladm_layers.append(layer)

            elif db.mode == 'gpkg':
                # To be implemented for GeoPackage layers
                pass

        return ladm_layers

    def automatic_namespace_local_id_configuration_changed(self, db):
        layers = self.get_ladm_layers_from_layer_tree(db)
        for layer in layers:
            self.set_automatic_fields_namespace_local_id(layer)

    def post_load_configurations(self, layer):
        # Do some post-load work, such as setting styles or
        # setting automatic fields for that layer
        self.set_automatic_fields(layer)
        self.symbology.set_layer_style(layer)

    def configure_automatic_field(self, layer, field, expression):
        index = layer.fields().indexFromName(field)
        default_value = QgsDefaultValue(expression, True) # Calculate on update
        layer.setDefaultValueDefinition(index, default_value)

    def reset_automatic_field(self, layer, field):
        self.configure_automatic_field(layer, field, "")

    def set_automatic_fields(self, layer):
        layer_name = layer.name()
        self.set_automatic_fields_namespace_local_id(layer)

        if layer.fields().indexFromName(VIDA_UTIL_FIELD) != -1:
            self.configure_automatic_field(layer, VIDA_UTIL_FIELD, "now()")

        if layer_name == BOUNDARY_TABLE:
            self.configure_automatic_field(layer, LENGTH_FIELD_BOUNDARY_TABLE, "$length")

    def set_automatic_fields_namespace_local_id(self, layer):
        layer_name = layer.name()

        ns_enabled, ns_field, ns_value = self.get_namespace_field_and_value(layer_name)
        lid_enabled, lid_field, lid_value = self.get_local_id_field_and_value(layer_name)

        if ns_enabled and ns_field:
            self.configure_automatic_field(layer, ns_field, ns_value)
        elif not ns_enabled and ns_field:
            self.reset_automatic_field(layer, ns_field)

        if lid_enabled and lid_field:
            self.configure_automatic_field(layer, lid_field, lid_value)
        elif not lid_enabled and lid_field:
            self.reset_automatic_field(layer, lid_field)

    def get_namespace_field_and_value(self, layer_name):
        namespace_enabled = QSettings().value('Asistente-LADM_COL/automatic_values/namespace_enabled', True, bool)

        field_prefix = NAMESPACE_PREFIX[layer_name] if layer_name in NAMESPACE_PREFIX else None
        namespace_field = field_prefix + NAMESPACE_FIELD if field_prefix else None

        if namespace_field is not None:
            namespace = str(QSettings().value('Asistente-LADM_COL/automatic_values/namespace_prefix', ""))
            namespace_value = "'{}{}{}'".format(namespace, "_" if namespace else "", layer_name).upper()
        else:
            namespace_value = None

        return (namespace_enabled, namespace_field, namespace_value)

    def get_local_id_field_and_value(self, layer_name):
        local_id_enabled = QSettings().value('Asistente-LADM_COL/automatic_values/local_id_enabled', True, bool)

        field_prefix = NAMESPACE_PREFIX[layer_name] if layer_name in NAMESPACE_PREFIX else None
        local_id_field = field_prefix + LOCAL_ID_FIELD if field_prefix else None

        if local_id_field is not None:
            local_id_value = '"{}"'.format(ID_FIELD)
        else:
            local_id_value = None

        return (local_id_enabled, local_id_field, local_id_value)

    def disable_automatic_fields(self, db, layer_name, geometry_type=None):
        layer = self.get_layer(db, layer_name, geometry_type, True)
        automatic_fields_definition = {idx: layer.defaultValueDefinition(idx) for idx in layer.attributeList()}

        for field in layer.fields():
            self.reset_automatic_field(layer, field.name())

        return automatic_fields_definition

    def enable_automatic_fields(self, db, automatic_fields_definition, layer_name, geometry_type=None):
        layer = self.get_layer(db, layer_name, geometry_type, True)

        for idx, default_definition in automatic_fields_definition.items():
            layer.setDefaultValueDefinition(idx, default_definition)

    def copy_csv_to_db(self, csv_path, delimiter, longitude, latitude, db, target_layer_name):
        if not csv_path or not os.path.exists(csv_path):
            self.message_emitted.emit(
                QCoreApplication.translate("QGISUtils",
                                           "No CSV file given or file doesn't exist."),
                Qgis.Warning)
            return False

        # Create QGIS vector layer
        uri = "file:///{}?delimiter={}&xField={}&yField={}&crs=EPSG:{}".format(
              csv_path,
              delimiter,
              longitude,
              latitude,
              DEFAULT_EPSG
           )
        csv_layer = QgsVectorLayer(uri, os.path.basename(csv_path), "delimitedtext")
        if not csv_layer.isValid():
            self.message_emitted.emit(
                QCoreApplication.translate("QGISUtils",
                                           "CSV layer not valid!"),
                Qgis.Warning)
            return False

        overlapping = self.get_overlapping_points(csv_layer) # List of lists of ids
        overlapping = [id for items in overlapping for id in items] # Build a flat list of ids

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
                                           "The point layer '{}' couldn't be found in the DB... {}").format(target_layer_name, db.get_description()),
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
        self.turn_transaction_off()
        layer = self.get_layer_from_layer_tree(BOUNDARY_TABLE, db.schema)

        if layer is None:
            self.message_with_button_load_layer_emitted.emit(
                QCoreApplication.translate("QGISUtils",
                                           "First load the layer {} into QGIS!").format(BOUNDARY_TABLE),
                QCoreApplication.translate("QGISUtils",
                                           "Load layer {} now").format(BOUNDARY_TABLE),
                [BOUNDARY_TABLE, None],
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
        self.turn_transaction_off()
        layer = self.get_layer_from_layer_tree(BOUNDARY_TABLE, db.schema)
        if layer is None:
            self.message_with_button_load_layer_emitted.emit(
                QCoreApplication.translate("QGISUtils",
                                           "First load the layer {} into QGIS!").format(BOUNDARY_TABLE),
                QCoreApplication.translate("QGISUtils", "Load layer {} now").format(BOUNDARY_TABLE),
                [BOUNDARY_TABLE, None],
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
        res_layers = self.get_layers(db, {
            BOUNDARY_TABLE: {'name': BOUNDARY_TABLE, 'geometry':None},
            POINT_BOUNDARY_FACE_STRING_TABLE: {'name': POINT_BOUNDARY_FACE_STRING_TABLE, 'geometry':None},
            BOUNDARY_POINT_TABLE: {'name':BOUNDARY_POINT_TABLE, 'geometry':None}}, load=True)

        boundary_layer = res_layers[BOUNDARY_TABLE]
        if boundary_layer is None:
            self.message_emitted.emit(
                QCoreApplication.translate("QGISUtils",
                                           "Table {} not found in the DB! {}").format(BOUNDARY_TABLE, db.get_description()),
                Qgis.Warning)
            return
        if use_selection and boundary_layer.selectedFeatureCount() == 0:
            if self.get_layer_from_layer_tree(BOUNDARY_TABLE, schema=db.schema) is None:
                self.message_with_button_load_layer_emitted.emit(
                    QCoreApplication.translate("QGISUtils",
                                               "First load the layer {} into QGIS and select at least one boundary!").format(BOUNDARY_TABLE),
                    QCoreApplication.translate("QGISUtils", "Load layer {} now").format(BOUNDARY_TABLE),
                    [BOUNDARY_TABLE, None],
                    Qgis.Warning)
            else:
                self.message_emitted.emit(
                    QCoreApplication.translate("QGISUtils", "First select at least one boundary!"),
                    Qgis.Warning)
            return

        bfs_layer = res_layers[POINT_BOUNDARY_FACE_STRING_TABLE]
        if bfs_layer is None:
            self.message_emitted.emit(
                QCoreApplication.translate("QGISUtils", "Table {} not found in the DB! {}").format(POINT_BOUNDARY_FACE_STRING_TABLE, db.get_description()),
                Qgis.Warning)
            return

        bfs_features = bfs_layer.getFeatures()

        # Get unique pairs id_boundary-id_boundary_point
        existing_pairs = [(bfs_feature[BFS_TABLE_BOUNDARY_FIELD], bfs_feature[BFS_TABLE_BOUNDARY_POINT_FIELD]) for bfs_feature in bfs_features]
        existing_pairs = set(existing_pairs)

        boundary_point_layer = res_layers[BOUNDARY_POINT_TABLE]
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
                        intersect_pairs.append((line[ID_FIELD], candidate_feature[ID_FIELD]))
        return intersect_pairs

    def fill_topology_tables_morebfs_less(self, db, use_selection=True):
        res_layers = self.get_layers(db, {
            PLOT_TABLE: {'name': PLOT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry},
            MORE_BOUNDARY_FACE_STRING_TABLE: {'name': MORE_BOUNDARY_FACE_STRING_TABLE, 'geometry':None},
            LESS_TABLE: {'name': LESS_TABLE, 'geometry':None},
            BOUNDARY_TABLE: {'name':BOUNDARY_TABLE, 'geometry':None}}, load=True)

        plot_layer = res_layers[PLOT_TABLE]
        if plot_layer is None:
            self.message_emitted.emit(
                QCoreApplication.translate("QGISUtils", "Table {} not found in the DB! {}").format(PLOT_TABLE, db.get_description()),
                Qgis.Warning)
            return

        if use_selection and plot_layer.selectedFeatureCount() == 0:
            if self.get_layer_from_layer_tree(PLOT_TABLE, schema=db.schema, geometry_type=QgsWkbTypes.PolygonGeometry) is None:
                self.message_with_button_load_layer_emitted.emit(
                    QCoreApplication.translate("QGISUtils",
                                               "First load the layer {} into QGIS and select at least one plot!").format(PLOT_TABLE),
                    QCoreApplication.translate("QGISUtils", "Load layer {} now").format(PLOT_TABLE),
                    [PLOT_TABLE, None],
                    Qgis.Warning)
            else:
                self.message_emitted.emit(
                    QCoreApplication.translate("QGISUtils", "First select at least one plot!"),
                    Qgis.Warning)
            return

        more_bfs_layer = res_layers[MORE_BOUNDARY_FACE_STRING_TABLE]
        if more_bfs_layer is None:
            self.message_emitted.emit(
                QCoreApplication.translate("QGISUtils", "Table {} not found in the DB! {}").format(MORE_BOUNDARY_FACE_STRING_TABLE, db.get_description()),
                Qgis.Warning)
            return

        less_layer = res_layers[LESS_TABLE]
        if less_layer is None:
            self.message_emitted.emit(
                QCoreApplication.translate("QGISUtils", "Table {} not found in the DB! {}").format(LESS_TABLE, db.get_description()),
                Qgis.Warning)
            return

        more_bfs_features = more_bfs_layer.getFeatures()
        less_features = less_layer.getFeatures()

        # Get unique pairs id_boundary-id_plot in both tables
        existing_more_pairs = [(more_bfs_feature[MOREBFS_TABLE_PLOT_FIELD], more_bfs_feature[MOREBFS_TABLE_BOUNDARY_FIELD]) for more_bfs_feature in more_bfs_features]
        existing_more_pairs = set(existing_more_pairs)
        existing_less_pairs = [(less_feature[LESS_TABLE_PLOT_FIELD], less_feature[LESS_TABLE_BOUNDARY_FIELD]) for less_feature in less_features]
        existing_less_pairs = set(existing_less_pairs)

        boundary_layer = res_layers[BOUNDARY_TABLE]
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
                QCoreApplication.translate("QGISUtils", "No pairs id_boundary-id_plot found for '{}' table.".format(LESS_TABLE)),
                Qgis.Info)

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
                            print("WARNING: (MoreBFS) Intersection between plot (t_id={}) and boundary (t_id={}) is a geometry of type: {}".format(
                                polygon[ID_FIELD],
                                candidate_feature[ID_FIELD],
                                intersection_type))

                        intersection_type = QgsGeometry(multi_inner_rings).intersection(candidate_geometry).type()
                        if intersection_type == QgsWkbTypes.LineGeometry:
                            intersect_less_pairs.append((polygon[ID_FIELD], candidate_feature[ID_FIELD]))
                        else:
                            print("WARNING: (Less) Intersection between plot (t_id={}) and boundary (t_id={}) is a geometry of type: {}".format(
                                polygon[ID_FIELD],
                                candidate_feature[ID_FIELD],
                                intersection_type))

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
                            print("WARNING: (MoreBFS) Intersection between plot (t_id={}) and boundary (t_id={}) is a geometry of type: {}".format(
                                polygon[ID_FIELD],
                                candidate_feature[ID_FIELD],
                                intersection_type))

        return (intersect_more_pairs, intersect_less_pairs)

    def polygonize_boundaries(self, db):
        res_layers = self.get_layers(db, {
            PLOT_TABLE: {'name': PLOT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry},
            BOUNDARY_TABLE: {'name':BOUNDARY_TABLE, 'geometry':None}}, load=True)

        boundaries = res_layers[BOUNDARY_TABLE]
        if boundaries is None:
            self.message_emitted.emit(
                QCoreApplication.translate("QGISUtils", "Layer {} not found in the DB! {}").format(BOUNDARY_TABLE, db.get_description()),
                Qgis.Warning)
            return
        selected_boundaries = boundaries.selectedFeatures()
        if not selected_boundaries:
            self.message_emitted.emit(
                QCoreApplication.translate("QGISUtils", "First select boundaries!"),
                Qgis.Warning)
            return

        plots = res_layers[PLOT_TABLE]
        if plots is None:
            self.message_emitted.emit(
                QCoreApplication.translate("QGISUtils", "Layer {} not found in the DB! {}").format(PLOT_TABLE, db.get_description()),
                Qgis.Warning)
            return

        boundary_geometries = [f.geometry() for f in selected_boundaries]
        collection = QgsGeometry().polygonize(boundary_geometries)
        features = list()
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

    def check_overlaps_in_boundary_points(self, db):
        features = []
        boundary_point_layer = self.get_layer(db, BOUNDARY_POINT_TABLE, load=True)

        if boundary_point_layer is None:
            self.message_emitted.emit(
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
            group = self.get_error_layers_group()
            added_layer = QgsProject.instance().addMapLayer(error_layer, False)
            added_layer = group.addLayer(added_layer).layer()
            self.symbology.set_point_error_symbol(added_layer)

            self.message_emitted.emit(
            QCoreApplication.translate("QGISUtils",
                                            "A memory layer with {} overlapping Boundary Points has been added to the map!").format(added_layer.featureCount()), Qgis.Info)
        else:
            self.message_emitted.emit(
                QCoreApplication.translate("QGISUtils",
                                           "There are no overlapping boundary points."), Qgis.Info)

    def check_overlaps_in_boundaries(self, db):
        boundary_layer = self.get_layer(db, BOUNDARY_TABLE, load=True)

        if boundary_layer is None:
            self.message_emitted.emit(
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

        # We want to have a feature per pair of ids, so collect several features
        # into a single feature for each pair of ids
        feedback = QgsProcessingFeedback()
        res = processing.run("native:collect", {'INPUT':error_point_layer, 'FIELD':['intersecting_boundaries'],'OUTPUT':'memory:'}, feedback=feedback)
        error_point_layer = res['OUTPUT']
        error_point_layer.setName(QCoreApplication.translate("QGISUtils", "Overlapping boundaries (point intersections)"))
        res = processing.run("native:collect", {'INPUT':error_line_layer, 'FIELD':['intersecting_boundaries'],'OUTPUT':'memory:'}, feedback=feedback)
        error_line_layer = res['OUTPUT']
        error_line_layer.setName(QCoreApplication.translate("QGISUtils","Overlapping boundaries (line intersections)"))

        if error_point_layer.featureCount() > 0 or error_line_layer.featureCount() > 0:
            group = self.get_error_layers_group()
            msg = ''

            if error_point_layer.featureCount() > 0:
                added_point_layer = QgsProject.instance().addMapLayer(error_point_layer, False)
                added_point_layer = group.addLayer(added_point_layer).layer()
                self.symbology.set_point_error_symbol(added_point_layer)
                msg = QCoreApplication.translate("QGISUtils",
                    "A memory layer with {} overlapping boundaries (point intersections) has been added to the map.").format(added_point_layer.featureCount())

            if error_line_layer.featureCount() > 0:
                added_line_layer = QgsProject.instance().addMapLayer(error_line_layer, False)
                added_line_layer = group.addLayer(added_line_layer).layer()
                self.symbology.set_line_error_symbol(added_line_layer)
                msg = QCoreApplication.translate("QGISUtils",
                    "A memory layer with {} overlapping boundaries (line intersections) has been added to the map.").format(added_line_layer.featureCount())

            if error_point_layer.featureCount() > 0 and error_line_layer.featureCount() > 0:
                msg = QCoreApplication.translate("QGISUtils",
                    "Two memory layers with overlapping boundaries ({} point intersections and {} line intersections) have been added to the map.").format(added_point_layer.featureCount(), added_line_layer.featureCount())

            self.message_emitted.emit(msg, Qgis.Info)
        else:
            self.message_emitted.emit(
                QCoreApplication.translate("QGISUtils",
                                           "There are no overlapping boundaries."), Qgis.Info)

    def check_too_long_segments(self, db):
        tolerance = int(QSettings().value('Asistente-LADM_COL/quality/too_long_tolerance', DEFAULT_TOO_LONG_BOUNDARY_SEGMENTS_TOLERANCE)) # meters
        features = []
        boundary_layer = self.get_layer(db, BOUNDARY_TABLE, load=True)

        if boundary_layer is None:
            self.message_emitted.emit(
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
            group = self.get_error_layers_group()
            added_layer = QgsProject.instance().addMapLayer(error_layer, False)
            added_layer = group.addLayer(added_layer).layer()
            self.symbology.set_line_error_symbol(added_layer)
            self.message_emitted.emit(
                QCoreApplication.translate("QGISUtils",
                                           "A memory layer with {} boundary segments longer than {}m. has been added to the map!").format(added_layer.featureCount(), tolerance),
                Qgis.Info)
        else:
            self.message_emitted.emit(
                QCoreApplication.translate("QGISUtils",
                                           "All boundary segments are within the tolerance ({}m.)!").format(tolerance),
                Qgis.Info)

    def get_error_layers_group(self):
        root = QgsProject.instance().layerTreeRoot()
        group = root.findGroup(ERROR_LAYER_GROUP)
        if group is None:
            index = self.project_generator_utils.get_first_index_for_geometry_type(QgsWkbTypes.UnknownGeometry)
            group = root.insertGroup(index if index is not None else -1, ERROR_LAYER_GROUP)

        return group

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

    def turn_transaction_off(self):
        QgsProject.instance().setAutoTransaction(False)

    def show_etl_model(self, db, input_layer, ladm_col_layer_name):
        model = QgsApplication.processingRegistry().algorithmById("model:ETL-model")
        if model:
            mapping = get_refactor_fields_mapping(ladm_col_layer_name, self)
            output = self.get_layer(db, ladm_col_layer_name, geometry_type=None, load=True)
            processing.execAlgorithmDialog("model:ETL-model", {
                    'INPUT': input_layer.name(),
                    'mapping': mapping,
                    'output': output.name()
                }
            )
        else:
            self.message_emitted.emit(
                QCoreApplication.translate("QGISUtils",
                                           "Model ETL-model was not found and cannot be opened!"),
                Qgis.Info)
