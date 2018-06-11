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
import socket
import webbrowser

from qgis.core import (QgsGeometry, QgsLineString, QgsDefaultValue, QgsProject,
                       QgsWkbTypes, QgsVectorLayerUtils, QgsDataSourceUri, Qgis,
                       QgsSpatialIndex, QgsVectorLayer, QgsMultiLineString,
                       QgsField,
                       QgsMapLayer,
                       QgsPointXY,
                       QgsMultiPoint, QgsMultiLineString, QgsGeometryCollection,
                       QgsApplication, QgsProcessingFeedback, QgsRelation,
                       QgsExpressionContextUtils, QgsEditorWidgetSetup)
from qgis.PyQt.QtCore import (Qt, QObject, pyqtSignal, QCoreApplication,
                              QVariant, QSettings, QLocale, QUrl, QFile)

import processing

from .project_generator_utils import ProjectGeneratorUtils
from .qt_utils import OverrideCursor
from .symbology import SymbologyUtils
from .geometry import GeometryUtils
from ..gui.settings_dialog import SettingsDialog
from ..config.general_config import (
    DEFAULT_EPSG,
    ERROR_LAYER_GROUP,
    MODULE_HELP_MAPPING,
    TEST_SERVER,
    HELP_URL,
    PLUGIN_VERSION,
    REFERENCING_LAYER,
    REFERENCING_FIELD,
    RELATION_NAME,
    REFERENCED_LAYER,
    REFERENCED_FIELD,
    RELATION_TYPE,
    DOMAIN_CLASS_RELATION,
    PLUGIN_DIR,
    QGIS_LANG,
    HELP_DIR_NAME
)
from ..config.table_mapping_config import (BFS_TABLE_BOUNDARY_FIELD,
                                           BFS_TABLE_BOUNDARY_POINT_FIELD,
                                           BOUNDARY_POINT_TABLE,
                                           BOUNDARY_TABLE,
                                           CUSTOM_WIDGET_CONFIGURATION,
                                           DICT_DISPLAY_EXPRESSIONS,
                                           EXTFILE_DATA_FIELD,
                                           EXTFILE_TABLE,
                                           ID_FIELD,
                                           LAYER_VARIABLES,
                                           LENGTH_FIELD_BOUNDARY_TABLE,
                                           LESS_TABLE,
                                           LESS_TABLE_BOUNDARY_FIELD,
                                           LESS_TABLE_PLOT_FIELD,
                                           LOCAL_ID_FIELD,
                                           MOREBFS_TABLE_PLOT_FIELD,
                                           MOREBFS_TABLE_BOUNDARY_FIELD,
                                           MORE_BOUNDARY_FACE_STRING_TABLE,
                                           NAMESPACE_FIELD,
                                           NAMESPACE_PREFIX,
                                           PLOT_TABLE,
                                           POINT_BOUNDARY_FACE_STRING_TABLE,
                                           REFERENCE_POINT_FIELD,
                                           SURVEY_POINT_TABLE,
                                           VIDA_UTIL_FIELD)
from ..config.refactor_fields_mappings import get_refactor_fields_mapping
from ..lib.source_handler import SourceHandler

class QGISUtils(QObject):

    activate_layer_requested = pyqtSignal(QgsMapLayer)
    clear_status_bar_emitted = pyqtSignal()
    layer_symbology_changed = pyqtSignal(str) # layer id
    message_emitted = pyqtSignal(str, int) # Message, level
    message_with_duration_emitted = pyqtSignal(str, int, int) # Message, level, duration
    message_with_button_load_layer_emitted = pyqtSignal(str, str, list, int) # Message, button text, [layer_name, geometry_type], level
    message_with_button_load_layers_emitted = pyqtSignal(str, str, dict, int) # Message, button text, layers_dict, level
    map_refresh_requested = pyqtSignal()
    map_freeze_requested = pyqtSignal(bool)
    status_bar_message_emitted = pyqtSignal(str, int) # Message, duration
    zoom_full_requested = pyqtSignal()
    zoom_to_selected_requested = pyqtSignal()

    def __init__(self):
        QObject.__init__(self)
        self.project_generator_utils = ProjectGeneratorUtils()
        self.symbology = SymbologyUtils()
        self.geometry = GeometryUtils()

        self.__settings_dialog = None
        self._source_handler = None
        self._layers = list()
        self._relations = list()

    def set_db_connection(self, mode, dict_conn):
        """
        Set plugin's main DB connection manually

        mode: 'pg' or 'gpkg'
        dict_conn: key-values (host, port, database, schema, user, password, dbfile)
        """
        dlg = self.get_settings_dialog()
        dlg.set_db_connection(mode, dict_conn)

    def get_settings_dialog(self):
        if self.__settings_dialog is None:
            self.__settings_dialog = SettingsDialog(qgis_utils=self)
            self.__settings_dialog.cache_layers_and_relations_requested.connect(self.cache_layers_and_relations)

        return self.__settings_dialog

    def get_db_connection(self):
        self.__settings_dialog = self.get_settings_dialog()
        return self.__settings_dialog.get_db_connection()

    def get_source_handler(self):
        if self._source_handler is None:
            self._source_handler = SourceHandler(self)
        return self._source_handler

    def cache_layers_and_relations(self, db):
        self.status_bar_message_emitted.emit(QCoreApplication.translate("QGISUtils",
            "Extracting relations and domains from the database... This is done only once per session!"), 0)
        QCoreApplication.processEvents()

        with OverrideCursor(Qt.WaitCursor):
            self._layers, self._relations = self.project_generator_utils.get_layers_and_relations_info(db)

        self.clear_status_bar_emitted.emit()

    def get_related_layers(self, layer_names, already_loaded):
        # For a given layer we load its domains, all its related layers and
        # the domains of those related layers
        related_layers = list()
        for relation in self._relations:
            for layer_name in layer_names:
                if relation[REFERENCING_LAYER] == layer_name:
                    if relation[REFERENCED_LAYER] not in already_loaded:
                        related_layers.append(relation[REFERENCED_LAYER])

        related_layers.extend(self.get_related_domains(related_layers, already_loaded))
        return related_layers

    def get_related_domains(self, layer_names, already_loaded):
        related_domains = list()
        for relation in self._relations:
            if relation[RELATION_TYPE] == DOMAIN_CLASS_RELATION:
                for layer_name in layer_names:
                    if relation[REFERENCING_LAYER] == layer_name:
                        if relation[REFERENCED_LAYER] not in already_loaded:
                            related_domains.append(relation[REFERENCED_LAYER])

        return related_domains

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
        additional_layers_to_load = list()

        self.map_freeze_requested.emit(True)

        profiler = QgsApplication.profiler()
        with OverrideCursor(Qt.WaitCursor):
            profiler.start("existing_layers")
            for layer_id, layer_info in layers.items():
                layer_obj = None
                ladm_layers = self.get_ladm_layers_from_layer_tree(db)

                # If layer is in LayerTree, return it
                for ladm_layer in ladm_layers:
                    if layer_info['name'] == ladm_layer.dataProvider().uri().table():
                        if layer_info['geometry'] is not None and layer_info['geometry'] != ladm_layer.geometryType():
                            continue

                        layer_obj = ladm_layer

                response_layers[layer_id] = layer_obj
            profiler.end()
            print("Existing layers",profiler.totalTime())
            profiler.clear()
            if load:
                layers_to_load = [layers[layer_id]['name'] for layer_id, layer_obj in response_layers.items() if layer_obj is None]

                if layers_to_load:
                    # Get related layers from cached relations and add them to
                    # list of layers to load, Project Generator will set relations
                    already_loaded = [ladm_layer.dataProvider().uri().table() for ladm_layer in ladm_layers]
                    profiler.start("related_layers")
                    additional_layers_to_load = self.get_related_layers(layers_to_load, already_loaded)
                    profiler.end()
                    print("Related layers",profiler.totalTime())
                    profiler.clear()
                    all_layers_to_load = list(set(layers_to_load + additional_layers_to_load))

                    self.status_bar_message_emitted.emit(QCoreApplication.translate("QGISUtils",
                        "Loading LADM_COL layers to QGIS and configuring their relations and forms..."), 0)
                    QCoreApplication.processEvents()
                    profiler.start("load_layers")
                    self.project_generator_utils.load_layers(all_layers_to_load, db)
                    profiler.end()
                    print("Load layers",profiler.totalTime())
                    profiler.clear()

                    # Now that all layers are loaded, update response dict
                    # and apply post_load_configurations to new layers
                    missing_layers = {layer_id: {'name': layers[layer_id]['name'], 'geometry': layers[layer_id]['geometry']} for layer_id, layer_obj in response_layers.items() if layer_obj is None}

                    profiler.start("post_load")
                    # Apply post-load configs to all just loaded layers
                    for layer in self.get_ladm_layers_from_layer_tree(db):
                        layer_name = layer.dataProvider().uri().table()
                        layer_geometry = layer.geometryType()

                        if layer_name in all_layers_to_load:
                            # Discard already loaded layers

                            for layer_id, layer_info in missing_layers.items():
                                # This should update response_layers dict with
                                # newly added layer objects
                                if layer_info['name'] == layer_name:
                                    if layer_info['geometry'] is not None and layer_info['geometry'] != layer_geometry:
                                        continue

                                    response_layers[layer_id] = layer
                                    del missing_layers[layer_id] # Don't look for this layer anymore
                                    break

                            self.post_load_configurations(layer)

                    profiler.end()
                    print("Post load",profiler.totalTime())
                    profiler.clear()
                    self.clear_status_bar_emitted.emit()

        self.map_freeze_requested.emit(False)
        self.map_refresh_requested.emit()
        self.activate_layer_requested.emit(list(response_layers.values())[0])

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
        self.configure_missing_relations(layer)
        self.set_display_expressions(layer)
        self.set_layer_variables(layer)
        self.set_custom_widgets(layer)
        self.set_custom_events(layer)
        self.set_automatic_fields(layer)
        if layer.isSpatial():
            self.symbology.set_layer_style_from_qml(layer)

    def configure_missing_relations(self, layer):
        layer_name = layer.dataProvider().uri().table()

        db_relations = list()
        for relation in self._relations:
            if relation[REFERENCING_LAYER] == layer_name:
                db_relations.append(relation)

        qgis_relations = QgsProject.instance().relationManager().referencingRelations(layer)
        qgis_rels = list()
        for qgis_relation in qgis_relations:
            qgis_rel = dict()
            referenced_layer = qgis_relation.referencedLayer()
            qgis_rel[REFERENCED_LAYER] = referenced_layer.dataProvider().uri().table()
            qgis_rel[REFERENCED_FIELD] = referenced_layer.fields()[qgis_relation.referencedFields()[0]].name()
            qgis_rel[REFERENCING_FIELD] = layer.fields()[qgis_relation.referencingFields()[0]].name()
            qgis_rels.append(qgis_rel)

        new_relations = list()
        # Compare relations, configure what is missing
        for db_relation in db_relations:
            found = False
            for qgis_rel in qgis_rels:
                # We known that referencing_layer already matches, so don't check
                if qgis_rel[REFERENCED_LAYER] == db_relation[REFERENCED_LAYER] and \
                    qgis_rel[REFERENCING_FIELD] == db_relation[REFERENCING_FIELD] and \
                    qgis_rel[REFERENCED_FIELD] == db_relation[REFERENCED_FIELD]:

                    found = True
                    break

            if not found:
                # This relation is not configured into QGIS, let's do it
                new_rel = QgsRelation()
                new_rel.setReferencingLayer(layer.id())
                referenced_layer = self.get_layer_from_layer_tree(db_relation[REFERENCED_LAYER], layer.dataProvider().uri().schema())
                if referenced_layer is None:
                    # Referenced_layer NOT FOUND in layer tree...
                    continue
                new_rel.setReferencedLayer(referenced_layer.id())
                new_rel.addFieldPair(db_relation[REFERENCING_FIELD], db_relation[REFERENCED_FIELD])
                new_rel.setId(db_relation[RELATION_NAME]) #generateId()
                new_rel.setName(db_relation[RELATION_NAME])

                new_relations.append(new_rel)

        all_qgis_relations = list(QgsProject.instance().relationManager().relations().values())
        all_qgis_relations.extend(new_relations)
        QgsProject.instance().relationManager().setRelations(all_qgis_relations)

    def set_display_expressions(self, layer):
        if layer.name() in DICT_DISPLAY_EXPRESSIONS:
            layer.setDisplayExpression(DICT_DISPLAY_EXPRESSIONS[layer.name()])

    def set_layer_variables(self, layer):
        if layer.name() in LAYER_VARIABLES:
            for variable, value in LAYER_VARIABLES[layer.name()].items():
                QgsExpressionContextUtils.setLayerVariable(layer, variable, value)

    def set_custom_widgets(self, layer):
        layer_name = layer.name()
        if layer_name in CUSTOM_WIDGET_CONFIGURATION:
            editor_widget_setup = QgsEditorWidgetSetup(
                    CUSTOM_WIDGET_CONFIGURATION[layer_name]['type'],
                    CUSTOM_WIDGET_CONFIGURATION[layer_name]['config'])
            index = layer.fields().indexFromName(EXTFILE_DATA_FIELD)
            layer.setEditorWidgetSetup(index, editor_widget_setup)

    def set_custom_events(self, layer):
        if layer.name() == EXTFILE_TABLE:
            self._source_handler = self.get_source_handler()
            self._source_handler.message_with_duration_emitted.connect(self.message_with_duration_emitted)
            self._source_handler.handle_source_upload(layer, EXTFILE_DATA_FIELD)

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

        # centroid must be calculated automatically from geometry
        #if layer.fields().indexFromName(REFERENCE_POINT_FIELD) != -1:
        #    self.configure_automatic_field(layer, REFERENCE_POINT_FIELD, "centroid($geometry)")

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

    def check_if_and_disable_automatic_fields(self, db, layer_name, geometry_type=None):
        settings = QSettings()
        automatic_fields_definition = {}
        if settings.value('Asistente-LADM_COL/automatic_values/disable_automatic_fields', True, bool):
            automatic_fields_definition = self.disable_automatic_fields(db, layer_name, geometry_type)

        return automatic_fields_definition

    def disable_automatic_fields(self, db, layer_name, geometry_type=None):
        layer = self.get_layer(db, layer_name, geometry_type, True)
        automatic_fields_definition = {idx: layer.defaultValueDefinition(idx) for idx in layer.attributeList()}

        for field in layer.fields():
            self.reset_automatic_field(layer, field.name())

        return automatic_fields_definition

    def check_if_and_enable_automatic_fields(self, db, automatic_fields_definition, layer_name, geometry_type=None):
        if automatic_fields_definition:
            settings = QSettings()
            if settings.value('Asistente-LADM_COL/automatic_values/disable_automatic_fields', True, bool):
                self.enable_automatic_fields(db,
                                             automatic_fields_definition,
                                             layer_name,
                                             geometry_type)

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

        # Skip checking point overlaps if layer is Surver points
        if target_layer_name != SURVEY_POINT_TABLE:
            overlapping = self.geometry.get_overlapping_points(csv_layer) # List of lists of ids
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

        QgsProject.instance().addMapLayer(target_point_layer)
        self.zoom_full_requested.emit()
        self.message_emitted.emit(
            QCoreApplication.translate("QGISUtils",
                                       "{} points were added succesfully to '{}'.").format(len(new_features), target_layer_name),
            Qgis.Info)

        return True

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
        id_pairs = self.geometry.get_pair_boundary_boundary_point(boundary_layer, boundary_point_layer, use_selection=use_selection)

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
        id_more_pairs, id_less_pairs = self.geometry.get_pair_boundary_plot(boundary_layer, plot_layer, use_selection=use_selection)

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

    def get_error_layers_group(self):
        root = QgsProject.instance().layerTreeRoot()
        group = root.findGroup(ERROR_LAYER_GROUP)
        if group is None:
            index = self.project_generator_utils.get_first_index_for_layer_type('unknown') # unknown is the option for groups
            group = root.insertGroup(index if index is not None else -1, ERROR_LAYER_GROUP)

        return group

    def turn_transaction_off(self):
        QgsProject.instance().setAutoTransaction(False)

    def show_etl_model(self, db, input_layer, ladm_col_layer_name):

        model = QgsApplication.processingRegistry().algorithmById("model:ETL-model")
        if model:
            automatic_fields_definition = self.check_if_and_disable_automatic_fields(db, ladm_col_layer_name)

            mapping = get_refactor_fields_mapping(ladm_col_layer_name, self)
            output = self.get_layer(db, ladm_col_layer_name, geometry_type=None, load=True)
            self.activate_layer_requested.emit(input_layer)
            params = {
                'INPUT': input_layer.name(),
                'mapping': mapping,
                'output': output.name()
            }
            processing.execAlgorithmDialog("model:ETL-model", params)

            self.check_if_and_enable_automatic_fields(db,
                                                      automatic_fields_definition,
                                                      ladm_col_layer_name)
        else:
            self.message_emitted.emit(
                QCoreApplication.translate("QGISUtils",
                                           "Model ETL-model was not found and cannot be opened!"),
                Qgis.Info)

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
            segments.extend(self.geometry.extract_as_single_segments(f.geometry()))

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

    def upload_source_files(self, db):
        extfile_layer = self.get_layer(db, EXTFILE_TABLE, None, True)
        if extfile_layer is None:
            self.message_emitted.emit(
                QCoreApplication.translate("QGISUtils", "Layer {} not found in the DB! {}").format(EXTFILE_TABLE, db.get_description()),
                Qgis.Warning)
            return

        field_index = extfile_layer.fields().indexFromName(EXTFILE_DATA_FIELD)
        features = list()

        if extfile_layer.selectedFeatureCount():
            features = extfile_layer.selectedFeatures()
        else:
            features = [f for f in extfile_layer.getFeatures()]

        self._source_handler = self.get_source_handler()
        new_values = self._source_handler.upload_files(extfile_layer, field_index, features)
        if new_values:
            extfile_layer.dataProvider().changeAttributeValues(new_values)

    def is_connected(self, hostname):
        try:
            host = socket.gethostbyname(hostname)
            s = socket.create_connection((host, 80), 2)
            return True
        except:
            pass
        return False

    def show_help(self, module='', offline=False):
        url = ''
        section = MODULE_HELP_MAPPING[module]

        # If we don't have Internet access check if the documentation is in the
        # expected local dir and show it. Otherwise, show a warning message.
        web_url = "{}/{}/{}".format(HELP_URL, QGIS_LANG, PLUGIN_VERSION)

        is_connected = self.is_connected(TEST_SERVER)
        if offline or not is_connected:
            basepath = os.path.dirname(os.path.abspath(__file__))

            help_path = os.path.join(
                PLUGIN_DIR,
                HELP_DIR_NAME,
                QGIS_LANG
            )
            if os.path.exists(help_path):
                url = os.path.join("file://", help_path)
            else:
                if is_connected:
                    self.message_with_duration_emitted.emit(
                        QCoreApplication.translate("QGISUtils",
                                                   "The local help could not be found in '{}' and cannot be open.").format(help_path),
                        Qgis.Warning,
                        20)
                else:
                    self.message_with_duration_emitted.emit(
                        QCoreApplication.translate("QGISUtils",
                                                   "Is your computer connected to Internet? If so, go to <a href=\"{}\">online help</a>.").format(web_url),
                        Qgis.Warning,
                        20)
                return
        else:
            url = web_url

        webbrowser.open("{}/{}".format(url, section))
