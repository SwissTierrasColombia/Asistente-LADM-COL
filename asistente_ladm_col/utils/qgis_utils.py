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
import ast
import datetime
import glob
import os
import socket
import webbrowser

from qgis.PyQt.QtCore import (Qt,
                              QObject,
                              pyqtSignal,
                              QCoreApplication,
                              QSettings)
from qgis.PyQt.QtWidgets import (QProgressBar,
                                 QMessageBox)
from qgis.core import (Qgis,
                       QgsApplication,
                       QgsEditFormConfig,
                       QgsAttributeEditorContainer,
                       QgsAttributeEditorElement,
                       QgsDataSourceUri,
                       QgsDefaultValue,
                       QgsEditorWidgetSetup,
                       QgsExpression,
                       QgsExpressionContextUtils,
                       QgsFieldConstraints,
                       QgsLayerTreeGroup,
                       QgsLayerTreeNode,
                       QgsMapLayer,
                       QgsOptionalExpression,
                       QgsProcessingFeatureSourceDefinition,
                       QgsProject,
                       QgsTolerance,
                       QgsSnappingConfig,
                       QgsProperty,
                       QgsRelation,
                       QgsVectorLayer,
                       QgsVectorLayerUtils,
                       QgsWkbTypes)

import processing
from .decorators import _activate_processing_plugin
from .geometry import GeometryUtils
from .qgis_model_baker_utils import QgisModelBakerUtils
from .qt_utils import OverrideCursor
from .symbology import SymbologyUtils
from ..config.general_config import (DEFAULT_EPSG,
                                     LAYER,
                                     FIELD_MAPPING_PATH,
                                     MAXIMUM_FIELD_MAPPING_FILES_PER_TABLE,
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
                                     PLUGIN_NAME,
                                     HELP_DIR_NAME,
                                     translated_strings)
from ..config.refactor_fields_mappings import get_refactor_fields_mapping
from ..config.table_mapping_config import (POINT_BFS_TABLE_BOUNDARY_FIELD,
                                           BFS_TABLE_BOUNDARY_POINT_FIELD,
                                           BOUNDARY_POINT_TABLE,
                                           BOUNDARY_TABLE,
                                           BUILDING_UNIT_TABLE,
                                           CUSTOM_WIDGET_CONFIGURATION,
                                           DICT_AUTOMATIC_VALUES,
                                           DICT_DISPLAY_EXPRESSIONS,
                                           EXTFILE_DATA_FIELD,
                                           EXTFILE_TABLE,
                                           FORM_GROUPS,
                                           LAYER_CONSTRAINTS,
                                           LAYER_VARIABLES,
                                           LESS_TABLE,
                                           LESS_TABLE_BOUNDARY_FIELD,
                                           LESS_TABLE_PLOT_FIELD,
                                           LOCAL_ID_FIELD,
                                           MOREBFS_TABLE_PLOT_FIELD,
                                           MOREBFS_TABLE_BOUNDARY_FIELD,
                                           MORE_BOUNDARY_FACE_STRING_TABLE,
                                           NAMESPACE_FIELD,
                                           NAMESPACE_PREFIX,
                                           NUMBER_OF_FLOORS,
                                           POINT_BOUNDARY_FACE_STRING_TABLE,
                                           VIDA_UTIL_FIELD,
                                           ADMINISTRATIVE_SOURCE_TABLE,
                                           COL_RESTRICTION_TYPE_RIGHT_OF_WAY_VALUE,
                                           ID_FIELD,
                                           PARCEL_TABLE,
                                           PLOT_TABLE,
                                           UEBAUNIT_TABLE,
                                           UEBAUNIT_TABLE_PARCEL_FIELD,
                                           UEBAUNIT_TABLE_RIGHT_OF_WAY_FIELD,
                                           UEBAUNIT_TABLE_PLOT_FIELD,
                                           RESTRICTION_TABLE_PARCEL_FIELD,
                                           RESTRICTION_TABLE_DESCRIPTION_FIELD,
                                           RESTRICTION_TABLE,
                                           RIGHT_OF_WAY_TABLE,
                                           RIGHT_OF_WAY_TABLE_IDENTIFICATOR_FIELD,
                                           RRR_SOURCE_RELATION_TABLE,
                                           RRR_SOURCE_RESTRICTION_FIELD,
                                           RRR_SOURCE_SOURCE_FIELD,
                                           SURVEY_POINT_TABLE,
                                           TYPE_FIELD)
from ..config.translator import (
    QGIS_LANG,
    PLUGIN_DIR
)
from ..gui.settings_dialog import SettingsDialog
from ..lib.db.db_connector import DBConnector
from ..lib.source_handler import SourceHandler


class QGISUtils(QObject):
    action_add_feature_requested = pyqtSignal()
    action_vertex_tool_requested = pyqtSignal()
    activate_layer_requested = pyqtSignal(QgsMapLayer)
    clear_status_bar_emitted = pyqtSignal()
    clear_message_bar_emitted = pyqtSignal()
    create_progress_message_bar_emitted = pyqtSignal(str, QProgressBar)
    remove_error_group_requested = pyqtSignal()
    layer_symbology_changed = pyqtSignal(str) # layer id
    db_connection_changed = pyqtSignal(DBConnector, bool) # dbconn, ladm_col_db
    message_emitted = pyqtSignal(str, int) # Message, level
    message_with_duration_emitted = pyqtSignal(str, int, int) # Message, level, duration
    message_with_button_load_layer_emitted = pyqtSignal(str, str, list, int) # Message, button text, [layer_name, geometry_type], level
    message_with_button_load_layers_emitted = pyqtSignal(str, str, dict, int) # Message, button text, layers_dict, level
    message_with_open_table_attributes_button_emitted = pyqtSignal(str, str, int, QgsVectorLayer, str)  # Message, button text, layers_dict, level
    message_with_button_download_report_dependency_emitted = pyqtSignal(str) # Message
    message_with_button_remove_report_dependency_emitted = pyqtSignal(str) # Message
    map_refresh_requested = pyqtSignal()
    map_freeze_requested = pyqtSignal(bool)
    set_node_visibility_requested = pyqtSignal(QgsLayerTreeNode, bool)
    status_bar_message_emitted = pyqtSignal(str, int) # Message, duration
    zoom_full_requested = pyqtSignal()
    zoom_to_selected_requested = pyqtSignal()

    def __init__(self, layer_tree_view=None):
        QObject.__init__(self)
        self.qgis_model_baker_utils = QgisModelBakerUtils()
        self.log = QgsApplication.messageLog()
        self.symbology = SymbologyUtils()
        self.geometry = GeometryUtils()
        self.layer_tree_view = layer_tree_view

        self.__settings_dialog = None
        self._source_handler = None
        self._layers = list()
        self._relations = list()
        self._bags_of_enum = dict()

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
            self.__settings_dialog.db_connection_changed.connect(self.cache_layers_and_relations)
            self.__settings_dialog.db_connection_changed.connect(self.db_connection_changed)

        return self.__settings_dialog

    def get_db_connection(self):
        self.__settings_dialog = self.get_settings_dialog()
        return self.__settings_dialog.get_db_connection()

    def get_source_handler(self):
        if self._source_handler is None:
            self._source_handler = SourceHandler(self)
        return self._source_handler

    def cache_layers_and_relations(self, db, ladm_col_db):
        if ladm_col_db:
            self.status_bar_message_emitted.emit(QCoreApplication.translate("QGISUtils",
                "Extracting relations and domains from the database... This is done only once per session!"), 0)
            QCoreApplication.processEvents()

            with OverrideCursor(Qt.WaitCursor):
                self._layers, self._relations, self._bags_of_enum = self.qgis_model_baker_utils.get_layers_and_relations_info(db)

            self.clear_status_bar_emitted.emit()
        else:
            self.clear_db_cache()

    def clear_db_cache(self):
        self._layers = list()
        self._relations = list()
        self._bags_of_enum = list()

    def get_related_layers(self, layer_names, already_loaded):
        """
        For a given layer we load its domains, all its related layers and the
        domains of those related layers. Additionally, we load its related
        structures and domains to build bags_of_enum widgets.
        """
        related_layers = list()
        for relation in self._relations:
            for layer_name in layer_names:
                if relation[REFERENCING_LAYER] == layer_name:
                    if relation[REFERENCED_LAYER] not in already_loaded and relation[REFERENCED_LAYER] not in layer_names:
                        related_layers.append(relation[REFERENCED_LAYER])

        related_layers_bags_of_enum = list()
        for layer_name in layer_names:
            if layer_name in self._bags_of_enum:
                for k,v in self._bags_of_enum[layer_name].items():
                    if v[2] not in already_loaded and v[2] not in layer_names:
                        related_layers_bags_of_enum.append(v[2]) # domain
                    if v[3] not in already_loaded and v[3] not in layer_names:
                        related_layers_bags_of_enum.append(v[3]) # structure

        related_layers.extend(self.get_related_domains(related_layers, already_loaded))
        return related_layers + related_layers_bags_of_enum

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
        layer = {layer_name: {'name': layer_name, 'geometry': geometry_type, LAYER: None}}
        res_layer = self.get_layers(db, layer, load)
        if res_layer is None:
            return None

        if layer[layer_name]:
            return layer[layer_name][LAYER]
        else:
            return None

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
            ladm_layers = self.get_ladm_layers_from_layer_tree(db)
            for layer_id, layer_info in layers.items():
                layer_obj = None

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
                    # list of layers to load, QGIS Model Baker will set relations
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
                    self.qgis_model_baker_utils.load_layers(all_layers_to_load, db)
                    profiler.end()
                    print("Load layers", profiler.totalTime())
                    profiler.clear()

                    # Now that all layers are loaded, update response dict
                    # and apply post_load_configurations to new layers
                    new_layers = {layer_id: {'name': layers[layer_id]['name'], 'geometry': layers[layer_id]['geometry']} for layer_id, layer_obj in response_layers.items() if layer_obj is None}

                    # Remove layers in two steps:
                    # 1) Remove those spatial layers with more than one geometry
                    #    column loaded because one geometry was requested.
                    ladm_layers = self.get_ladm_layers_from_layer_tree(db)
                    for layer in ladm_layers:
                        layer_name = layer.dataProvider().uri().table()

                        if layer_name in all_layers_to_load and layer.isSpatial():
                            remove_layer = True
                            for layer_id, layer_info in new_layers.items():
                                if layer_info['name'] == layer_name:
                                    if layer_info['geometry'] == layer.geometryType():
                                        remove_layer = False
                                        break
                                    if layer_info['geometry'] is None:
                                        # We allow loading layers that only have
                                        # one geometry column by not specifying
                                        # its geometry (i.e., by using None)
                                        remove_layer = False
                                        break
                            if remove_layer:
                                QgsProject.instance().removeMapLayer(layer)
                                ladm_layers.remove(layer)

                    # 2) Remove related spatial layers with more than one
                    #    geometry column, which we don't prefer (i.e., points)
                    for additional_layer_name in additional_layers_to_load:
                        num_geometry_columns = 0
                        for layer in ladm_layers:
                            if layer.dataProvider().uri().table() == additional_layer_name and layer.isSpatial():
                                num_geometry_columns += 1

                        if num_geometry_columns > 1:
                            QgsProject.instance().removeMapLayer(layer)
                            ladm_layers.remove(layer)

                    profiler.start("post_load")
                    # Apply post-load configs to all just loaded layers
                    requested_layer_names = [v['name'] for k,v in layers.items()]
                    for layer in ladm_layers:
                        layer_name = layer.dataProvider().uri().table()
                        layer_geometry = layer.geometryType()

                        if layer_name in all_layers_to_load:
                            # Discard already loaded layers

                            for layer_id, layer_info in new_layers.items():
                                # This should update response_layers dict with
                                # newly added layer objects
                                if layer_info['name'] == layer_name:
                                    if layer_info['geometry'] is not None and layer_info['geometry'] != layer_geometry:
                                        continue

                                    response_layers[layer_id] = layer
                                    del new_layers[layer_id] # Don't look for this layer anymore
                                    break

                            # Turn off layers loaded as related layers
                            visible = layer_name in requested_layer_names
                            self.post_load_configurations(layer, visible)

                    profiler.end()
                    print("Post load",profiler.totalTime())
                    profiler.clear()
                    self.clear_status_bar_emitted.emit()

        self.map_freeze_requested.emit(False)
        self.map_refresh_requested.emit()
        self.activate_layer_requested.emit(list(response_layers.values())[0])

        # Verifies that the layers have been successfully loaded
        for layer_name in layers:
            if response_layers[layer_name] is None:
                self.message_emitted.emit(QCoreApplication.translate("QGISUtils", "{layer_name} layer couldn't be found... {description}").format(
                        layer_name=layer_name,
                        description=db.get_description()),
                    Qgis.Warning)
                return {}

            # Save reference to layer loaded
            if LAYER in layers[layer_name]:
                layers[layer_name][LAYER] = response_layers[layer_name]

        # response_layers only has data about requested layers. Other layers,
        # i.e., those loaded as related ones, are not included
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
            if db.is_ladm_layer(layer):
                ladm_layers.append(layer)

        return ladm_layers

    def automatic_namespace_local_id_configuration_changed(self, db):
        layers = self.get_ladm_layers_from_layer_tree(db)
        for layer in layers:
            self.set_automatic_fields_namespace_local_id(layer)

    def post_load_configurations(self, layer, visible):
        # Do some post-load work, such as setting styles or
        # setting automatic fields for that layer
        self.configure_missing_relations(layer)
        self.configure_missing_bags_of_enum(layer)
        self.set_display_expressions(layer)
        self.set_layer_variables(layer)
        self.set_custom_widgets(layer)
        self.set_custom_events(layer)
        self.set_automatic_fields(layer)
        self.set_layer_constraints(layer)
        self.set_form_groups(layer)
        if layer.isSpatial():
            self.symbology.set_layer_style_from_qml(layer)
            self.set_layer_visibility(layer, visible)

    def configure_missing_relations(self, layer):
        """
        Relations between newly loaded layers and already loaded layer cannot
        be handled by qgis model baker (which only sets relations between
        loaded layers), so we do it in the Asistente LADM_COL.
        """
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
                referenced_layer = self.get_layer_from_layer_tree(
                    db_relation[REFERENCED_LAYER],
                    layer.dataProvider().uri().schema())
                if referenced_layer is None:
                    # Referenced_layer NOT FOUND in layer tree...
                    continue
                new_rel.setReferencedLayer(referenced_layer.id())
                new_rel.addFieldPair(db_relation[REFERENCING_FIELD],
                    db_relation[REFERENCED_FIELD])
                new_rel.setId(db_relation[RELATION_NAME]) #generateId()
                new_rel.setName(db_relation[RELATION_NAME])

                new_relations.append(new_rel)

        all_qgis_relations = list(QgsProject.instance().relationManager().relations().values())
        all_qgis_relations.extend(new_relations)
        QgsProject.instance().relationManager().setRelations(all_qgis_relations)

    def configure_missing_bags_of_enum(self, layer):
        """
        Bags of enums between newly loaded layers and already loaded layers
        cannot be handled by qgis model baker (which only sets relations
        between loaded layers), so we do it in the Asistente LADM_COL.
        """
        layer_name = layer.dataProvider().uri().table()

        if layer_name in self._bags_of_enum:
            for k,v in self._bags_of_enum[layer_name].items():
                # Check if bag of enum field has already a value relation
                # configured or not
                idx = layer.fields().indexOf(k)
                if layer.editorWidgetSetup(idx).type() == 'ValueRelation':
                    continue

                domain = self.get_layer_from_layer_tree(v[2],
                    layer.dataProvider().uri().schema())
                if domain is not None:
                    cardinality = v[1]
                    domain_table = v[2]
                    key_field = v[4]
                    value_field = v[5]

                    allow_null = cardinality.startswith('0')
                    allow_multi = cardinality.endswith('*')

                    field_widget_config = {
                        'AllowMulti': allow_multi,
                        'UseCompleter': False,
                        'Value': value_field,
                        'OrderByValue': False,
                        'AllowNull': allow_null,
                        'Layer': domain.id(),
                        'FilterExpression': '',
                        'Key': key_field,
                        'NofColumns': 1
                    }
                    setup = QgsEditorWidgetSetup('ValueRelation', field_widget_config)
                    layer.setEditorWidgetSetup(idx, setup)

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
            if layer_name == EXTFILE_TABLE:
                index = layer.fields().indexFromName(EXTFILE_DATA_FIELD)
            elif layer_name == BUILDING_UNIT_TABLE:
                index = layer.fields().indexFromName(NUMBER_OF_FLOORS)

            layer.setEditorWidgetSetup(index, editor_widget_setup)

    def set_custom_events(self, layer):
        if layer.name() == EXTFILE_TABLE:
            self._source_handler = self.get_source_handler()
            self._source_handler.message_with_duration_emitted.connect(self.message_with_duration_emitted)
            self._source_handler.handle_source_upload(layer, EXTFILE_DATA_FIELD)

    def set_layer_constraints(self, layer):
        if layer.name() in LAYER_CONSTRAINTS:
            for field_name, value in LAYER_CONSTRAINTS[layer.name()].items():
                idx = layer.fields().indexOf(field_name)
                layer.setConstraintExpression(
                    idx,
                    value['expression'],
                    value['description'])

                layer.setFieldConstraint(
                    idx,
                    QgsFieldConstraints.ConstraintExpression,
                    QgsFieldConstraints.ConstraintStrengthSoft)

                # We shouldn't make DB constraints flexible, but in case you from the future need it, uncomment
                # layer.setFieldConstraint(
                #     idx,
                #     QgsFieldConstraints.ConstraintUnique,
                #     QgsFieldConstraints.ConstraintStrengthSoft)

    def set_form_groups(self, layer):
        if layer.name() in FORM_GROUPS:
            # Preserve children, clear irc
            irc = layer.editFormConfig().invisibleRootContainer()
            children = list()
            for child in irc.children():
                children.append(child.clone(irc))
            irc.clear()
            aec = children[0] # General Tab

            # Create new General tab
            new_general_tab = QgsAttributeEditorContainer('General', irc)
            new_general_tab.setIsGroupBox(False)
            new_general_tab.setShowLabel(True)
            new_general_tab.setColumnCount(2)

            # Clone General tab elements
            elements = [e.clone(aec) for e in aec.children()]

            # Iterate group definitions
            elements_used = list()
            for group_name, group_def in FORM_GROUPS[layer.name()].items():
                container = QgsAttributeEditorContainer(group_name, new_general_tab)
                container.setIsGroupBox(True)
                container.setShowLabel(group_def['show_label'])
                container.setColumnCount(group_def['column_count'])
                if group_def['visibility_expression'] is None:
                    group_def['visibility_expression'] = "True"
                container.setVisibilityExpression(
                    QgsOptionalExpression(
                        QgsExpression(group_def['visibility_expression'])))

                for e in elements:
                    if e.name() in group_def['attr_list']:
                        container.addChildElement(e)
                        elements_used.append(e)

                group_def['container'] = container

            # Fill new General tab with attributes and groups. It takes order
            # of groups into account from before_attr/after_attr
            for e in elements:
                if e not in elements_used:
                    element_added = False
                    for group_name, group_def in FORM_GROUPS[layer.name()].items():
                        if e.name() == group_def['before_attr']:
                            new_general_tab.addChildElement(group_def['container'])
                            new_general_tab.addChildElement(e)
                            element_added = True
                        elif e.name() == group_def['after_attr']:
                            new_general_tab.addChildElement(e)
                            new_general_tab.addChildElement(group_def['container'])
                            element_added = True
                    if not element_added:
                        new_general_tab.addChildElement(e)

            containers = [ele.name() for ele in new_general_tab.findElements(QgsAttributeEditorElement.AeTypeContainer)]
            for group_name, group_def in FORM_GROUPS[layer.name()].items():
                if group_name not in containers: # Still not added (no before/after attrs)
                    new_general_tab.addChildElement(group_def['container'])

            irc.addChildElement(new_general_tab)

    def configure_automatic_fields(self, layer, list_dicts_field_expression):
        for dict_field_expression in list_dicts_field_expression:
            for field, expression in dict_field_expression.items(): # There should be one key and one value
                index = layer.fields().indexFromName(field)
                default_value = QgsDefaultValue(expression, True) # Calculate on update
                layer.setDefaultValueDefinition(index, default_value)
                QgsApplication.messageLog().logMessage(
                    "Automatic value configured: Layer '{}', field '{}', expression '{}'.".format(
                        layer.name(), field, expression),
                    PLUGIN_NAME, Qgis.Info)

    def reset_automatic_field(self, layer, field):
        self.configure_automatic_fields(layer, [{field: ""}])

    def set_automatic_fields(self, layer):
        layer_name = layer.name()

        self.set_automatic_fields_namespace_local_id(layer)

        if layer.fields().indexFromName(VIDA_UTIL_FIELD) != -1:
            self.configure_automatic_fields(layer, [{VIDA_UTIL_FIELD: "now()"}])

        if layer_name in DICT_AUTOMATIC_VALUES:
            self.configure_automatic_fields(layer, DICT_AUTOMATIC_VALUES[layer_name])

    def set_automatic_fields_namespace_local_id(self, layer):
        layer_name = layer.name()

        ns_enabled, ns_field, ns_value = self.get_namespace_field_and_value(layer_name)
        lid_enabled, lid_field, lid_value = self.get_local_id_field_and_value(layer_name)

        if ns_enabled and ns_field:
            self.configure_automatic_fields(layer, [{ns_field: ns_value}])
        elif not ns_enabled and ns_field:
            self.reset_automatic_field(layer, ns_field)

        if lid_enabled and lid_field:
            self.configure_automatic_fields(layer, [{lid_field: lid_value}])
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
            local_id_value = "$id"
        else:
            local_id_value = None

        return (local_id_enabled, local_id_field, local_id_value)

    def check_if_and_disable_automatic_fields(self, db, layer_name, geometry_type=None):
        """
        Check settings to see if the user wants to calculate automatic values
        when in batch mode. If not, disable automatic fields and return
        expressions so that they can be restored after the batch load.
        """
        settings = QSettings()
        automatic_fields_definition = {}
        if not settings.value('Asistente-LADM_COL/automatic_values/automatic_values_in_batch_mode', True, bool):
            automatic_fields_definition = self.disable_automatic_fields(db, layer_name, geometry_type)

        return automatic_fields_definition

    def disable_automatic_fields(self, db, layer_name, geometry_type=None):
        layer = self.get_layer(db, layer_name, geometry_type, True)
        automatic_fields_definition = {idx: layer.defaultValueDefinition(idx) for idx in layer.attributeList()}

        for field in layer.fields():
            self.reset_automatic_field(layer, field.name())

        return automatic_fields_definition

    def check_if_and_enable_automatic_fields(self, db, automatic_fields_definition, layer_name, geometry_type=None):
        """
        Once the batch load is done, check whether the user wanted to calculate
        automatic values in batch mode or not. If not, restore the expressions
        we saved before running the batch load.
        """
        if automatic_fields_definition:
            settings = QSettings()
            if not settings.value('Asistente-LADM_COL/automatic_values/automatic_values_in_batch_mode', True, bool):
                self.enable_automatic_fields(db,
                                             automatic_fields_definition,
                                             layer_name,
                                             geometry_type)

    def enable_automatic_fields(self, db, automatic_fields_definition, layer_name, geometry_type=None):
        layer = self.get_layer(db, layer_name, geometry_type, True)

        for idx, default_definition in automatic_fields_definition.items():
            layer.setDefaultValueDefinition(idx, default_definition)

    def set_error_group_visibility(self, visible):
        self.set_node_visibility(self.get_error_layers_group(), visible)

    def set_layer_visibility(self, layer, visible):
        node = QgsProject.instance().layerTreeRoot().findLayer(layer.id())
        self.set_node_visibility(node, visible)

    def set_node_visibility(self, node, visible):
        self.set_node_visibility_requested.emit(node, visible)

    @_activate_processing_plugin
    def copy_csv_to_db(self, csv_path, delimiter, longitude, latitude, db, epsg, target_layer_name, elevation=None, decimal_point='.'):
        if not csv_path or not os.path.exists(csv_path):
            self.message_emitted.emit(
                QCoreApplication.translate("QGISUtils",
                                           "No CSV file given or file doesn't exist."),
                Qgis.Warning)
            return False

        # Create QGIS vector layer
        uri = "file:///{}?decimalPoint={}&delimiter={}&xField={}&yField={}&crs=EPSG:{}".format(
              csv_path,
              decimal_point,
              delimiter if delimiter != '\t' else '%5Ct',
              longitude,
              latitude,
              epsg
           )
        csv_layer = QgsVectorLayer(uri, os.path.basename(csv_path), "delimitedtext")

        if elevation:
            z = QgsProperty.fromExpression('\"{}\"'.format(elevation.strip()))
            parameters = {'INPUT': csv_layer,
                          'Z_VALUE': z,
                          'OUTPUT': 'memory:'}
            res = processing.run("qgis:setzvalue", parameters)
            csv_layer = res['OUTPUT']

        if not epsg == DEFAULT_EPSG:
            crs_dest = 'EPSG:{}'.format(DEFAULT_EPSG)
            parameters = {'INPUT': csv_layer,
                          'TARGET_CRS': crs_dest,
                          'OUTPUT': 'memory:'}

            res = processing.run("native:reprojectlayer", parameters)
            csv_layer = res['OUTPUT']

        if not csv_layer.isValid():
            self.message_emitted.emit(
                QCoreApplication.translate("QGISUtils",
                                           "CSV layer not valid!"),
                Qgis.Warning)
            return False

        # Skip checking point overlaps if layer is Survey points
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

        # Improve message for import from csv
        initial_feature_count = target_point_layer.featureCount()
        target_point_layer.dataProvider().addFeatures(new_features)
        QgsProject.instance().addMapLayer(target_point_layer)

        if target_point_layer.featureCount() > initial_feature_count:
            self.zoom_full_requested.emit()
            self.message_emitted.emit(
                QCoreApplication.translate("QGISUtils",
                                           "{} points were added succesfully to '{}'.").format(len(new_features),
                                                                                               target_layer_name),
                Qgis.Info)
        else:
            self.message_emitted.emit(
                QCoreApplication.translate("QGISUtils",
                                           "No point was added to '{}'.").format(target_layer_name),
                Qgis.Warning)
            return False

        return True

    def fill_topology_table_pointbfs(self, db, use_selection=True):

        layers = {
            BOUNDARY_TABLE: {'name': BOUNDARY_TABLE, 'geometry': None, LAYER: None},
            POINT_BOUNDARY_FACE_STRING_TABLE: {'name': POINT_BOUNDARY_FACE_STRING_TABLE, 'geometry': None, LAYER: None},
            BOUNDARY_POINT_TABLE: {'name': BOUNDARY_POINT_TABLE, 'geometry': None, LAYER: None}
        }

        res_layers = self.get_layers(db, layers, load=True)
        if res_layers is None:
            return None

        if use_selection:
            if layers[BOUNDARY_TABLE][LAYER].selectedFeatureCount() == 0:
                if self.get_layer_from_layer_tree(BOUNDARY_TABLE, schema=db.schema) is None:
                    self.message_with_button_load_layer_emitted.emit(
                        QCoreApplication.translate("QGISUtils",
                                                   "First load the layer {} into QGIS and select at least one boundary!").format(BOUNDARY_TABLE),
                        QCoreApplication.translate("QGISUtils", "Load layer {} now").format(BOUNDARY_TABLE),
                        [BOUNDARY_TABLE, None],
                        Qgis.Warning)
                else:
                    reply = QMessageBox.question(None,
                                 QCoreApplication.translate("QGISUtils", "Continue?"),
                                 QCoreApplication.translate("QGISUtils",
                                     "There are no selected boundaries, do you like to fill the '{}' table for all the {} boundaries in the data base?")
                                     .format(POINT_BOUNDARY_FACE_STRING_TABLE,
                                         layers[BOUNDARY_TABLE][LAYER].featureCount()),
                                 QMessageBox.Yes, QMessageBox.No)
                    if reply == QMessageBox.Yes:
                        use_selection = False
                    else:
                        self.message_emitted.emit(
                            QCoreApplication.translate("QGISUtils", "First select at least one boundary!"),
                            Qgis.Warning)
                        return
            else:
                reply = QMessageBox.question(None,
                             QCoreApplication.translate("QGISUtils", "Continue?"),
                             QCoreApplication.translate("QGISUtils",
                                 "There are {selected} boundaries selected, do you like to fill the '{table}' table just for the selected boundaries?\n\nIf you say 'No', the '{table}' table will be filled for all boundaries in the database.")
                                 .format(selected=layers[BOUNDARY_TABLE][LAYER].selectedFeatureCount(),
                                     table=POINT_BOUNDARY_FACE_STRING_TABLE),
                             QMessageBox.Yes, QMessageBox.No)
                if reply == QMessageBox.No:
                    use_selection = False

        bfs_features = layers[POINT_BOUNDARY_FACE_STRING_TABLE][LAYER].getFeatures()

        # Get unique pairs id_boundary-id_boundary_point
        existing_pairs = [(bfs_feature[POINT_BFS_TABLE_BOUNDARY_FIELD], bfs_feature[BFS_TABLE_BOUNDARY_POINT_FIELD]) for bfs_feature in bfs_features]
        existing_pairs = set(existing_pairs)

        id_pairs = self.geometry.get_pair_boundary_boundary_point(layers[BOUNDARY_TABLE][LAYER], layers[BOUNDARY_POINT_TABLE][LAYER], use_selection=use_selection)

        if id_pairs:
            layers[POINT_BOUNDARY_FACE_STRING_TABLE][LAYER].startEditing()
            features = list()
            for id_pair in id_pairs:
                if not id_pair in existing_pairs: # Avoid duplicated pairs in the DB
                    # Create feature
                    feature = QgsVectorLayerUtils().createFeature(layers[POINT_BOUNDARY_FACE_STRING_TABLE][LAYER])
                    feature.setAttribute(POINT_BFS_TABLE_BOUNDARY_FIELD, id_pair[0])
                    feature.setAttribute(BFS_TABLE_BOUNDARY_POINT_FIELD, id_pair[1])
                    features.append(feature)
            layers[POINT_BOUNDARY_FACE_STRING_TABLE][LAYER].addFeatures(features)
            layers[POINT_BOUNDARY_FACE_STRING_TABLE][LAYER].commitChanges()
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
        layers = {
            PLOT_TABLE: {'name': PLOT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            MORE_BOUNDARY_FACE_STRING_TABLE: {'name': MORE_BOUNDARY_FACE_STRING_TABLE, 'geometry': None, LAYER: None},
            LESS_TABLE: {'name': LESS_TABLE, 'geometry': None, LAYER: None},
            BOUNDARY_TABLE: {'name': BOUNDARY_TABLE, 'geometry': None, LAYER: None}
        }

        res_layers = self.get_layers(db, layers, load=True)
        if res_layers is None:
            return None

        if use_selection:
            if layers[PLOT_TABLE][LAYER].selectedFeatureCount() == 0:
                if self.get_layer_from_layer_tree(PLOT_TABLE, schema=db.schema, geometry_type=QgsWkbTypes.PolygonGeometry) is None:
                    self.message_with_button_load_layer_emitted.emit(
                        QCoreApplication.translate("QGISUtils",
                                                   "First load the layer {} into QGIS and select at least one plot!").format(PLOT_TABLE),
                        QCoreApplication.translate("QGISUtils", "Load layer {} now").format(PLOT_TABLE),
                        [PLOT_TABLE, None],
                        Qgis.Warning)
                else:
                    reply = QMessageBox.question(None,
                                 QCoreApplication.translate("QGISUtils", "Continue?"),
                                 QCoreApplication.translate("QGISUtils",
                                      "There are no selected plots, do you like to fill the '{more}' and '{less}' tables for all the {all} plots in the data base?")
                                 .format(more=MORE_BOUNDARY_FACE_STRING_TABLE,
                                         less=LESS_TABLE,
                                         all=layers[PLOT_TABLE][LAYER].featureCount()),
                                 QMessageBox.Yes, QMessageBox.No)
                    if reply == QMessageBox.Yes:
                        use_selection = False
                    else:
                        self.message_emitted.emit(
                            QCoreApplication.translate("QGISUtils", "First select at least one plot!"),
                            Qgis.Warning)
                        return
            else:
                reply = QMessageBox.question(None,
                             QCoreApplication.translate("QGISUtils", "Continue?"),
                             QCoreApplication.translate("QGISUtils",
                                 "There are {selected} plots selected, do you like to fill the '{more}' and '{less}' tables just for the selected plots?\n\nIf you say 'No', the '{more}' and '{less}' tables will be filled for all plots in the database.")
                             .format(selected=layers[PLOT_TABLE][LAYER].selectedFeatureCount(),
                                     more=MORE_BOUNDARY_FACE_STRING_TABLE,
                                     less=LESS_TABLE),
                             QMessageBox.Yes, QMessageBox.No)
                if reply == QMessageBox.No:
                    use_selection = False

        more_bfs_features = layers[MORE_BOUNDARY_FACE_STRING_TABLE][LAYER].getFeatures()
        less_features = layers[LESS_TABLE][LAYER].getFeatures()

        # Get unique pairs id_boundary-id_plot in both tables
        existing_more_pairs = [(more_bfs_feature[MOREBFS_TABLE_PLOT_FIELD], more_bfs_feature[MOREBFS_TABLE_BOUNDARY_FIELD]) for more_bfs_feature in more_bfs_features]
        existing_more_pairs = set(existing_more_pairs)
        existing_less_pairs = [(less_feature[LESS_TABLE_PLOT_FIELD], less_feature[LESS_TABLE_BOUNDARY_FIELD]) for less_feature in less_features]
        existing_less_pairs = set(existing_less_pairs)

        id_more_pairs, id_less_pairs = self.geometry.get_pair_boundary_plot(layers[BOUNDARY_TABLE][LAYER], layers[PLOT_TABLE][LAYER], use_selection=use_selection)

        if id_less_pairs:
            layers[LESS_TABLE][LAYER].startEditing()
            features = list()
            for id_pair in id_less_pairs:
                if not id_pair in existing_less_pairs: # Avoid duplicated pairs in the DB
                    # Create feature
                    feature = QgsVectorLayerUtils().createFeature(layers[LESS_TABLE][LAYER])
                    feature.setAttribute(LESS_TABLE_PLOT_FIELD, id_pair[0])
                    feature.setAttribute(LESS_TABLE_BOUNDARY_FIELD, id_pair[1])
                    features.append(feature)
            layers[LESS_TABLE][LAYER].addFeatures(features)
            layers[LESS_TABLE][LAYER].commitChanges()
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
                QCoreApplication.translate("QGISUtils", "No pairs id_boundary-id_plot found for '{}' table.").format(LESS_TABLE),
                Qgis.Info)

        if id_more_pairs:
            layers[MORE_BOUNDARY_FACE_STRING_TABLE][LAYER].startEditing()
            features = list()
            for id_pair in id_more_pairs:
                if not id_pair in existing_more_pairs: # Avoid duplicated pairs in the DB
                    # Create feature
                    feature = QgsVectorLayerUtils().createFeature(layers[MORE_BOUNDARY_FACE_STRING_TABLE][LAYER])
                    feature.setAttribute(MOREBFS_TABLE_PLOT_FIELD, id_pair[0])
                    feature.setAttribute(MOREBFS_TABLE_BOUNDARY_FIELD, id_pair[1])
                    features.append(feature)
            layers[MORE_BOUNDARY_FACE_STRING_TABLE][LAYER].addFeatures(features)
            layers[MORE_BOUNDARY_FACE_STRING_TABLE][LAYER].commitChanges()
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
                QCoreApplication.translate("QGISUtils", "No pairs id_boundary-id_plot found for '{}' table.").format(MORE_BOUNDARY_FACE_STRING_TABLE),
                Qgis.Info)

    def get_error_layers_group(self):
        """
        Get the topology errors group. If it exists but is placed in another
        position rather than the top, it moves the group to the top.
        """
        root = QgsProject.instance().layerTreeRoot()
        group = root.findGroup(translated_strings.ERROR_LAYER_GROUP)
        if group is None:
            group = root.insertGroup(0, translated_strings.ERROR_LAYER_GROUP)
        elif not self.layer_tree_view.layerTreeModel().node2index(group).row() == 0 or type(group.parent()) is QgsLayerTreeGroup:
            group_clone = group.clone()
            root.insertChildNode(0, group_clone)
            parent = group.parent()
            parent.removeChildNode(group)
            group = group_clone
        return group

    def error_group_exists(self):
        root = QgsProject.instance().layerTreeRoot()
        return root.findGroup(translated_strings.ERROR_LAYER_GROUP) is not None

    def turn_transaction_off(self):
        QgsProject.instance().setAutoTransaction(False)

    @_activate_processing_plugin
    def show_etl_model(self, db, input_layer, ladm_col_layer_name, geometry_type=None, field_mapping=''):
        output = self.get_layer(db, ladm_col_layer_name, geometry_type, load=True)
        if output is None:
            return False

        if output.isEditable():
            self.message_emitted.emit(
                QCoreApplication.translate("QGISUtils",
                    "You need to close the edit session on layer '{}' before using this tool!").format(ladm_col_layer_name),
                Qgis.Warning)
            return False

        model = QgsApplication.processingRegistry().algorithmById("model:ETL-model")
        if model:
            automatic_fields_definition = self.check_if_and_disable_automatic_fields(db, ladm_col_layer_name)

            # Get the mapping we'll use, it might come from stored recent mappings or from the default mapping
            mapping = None
            if field_mapping:
                mapping = self.load_field_mapping(field_mapping)

                if mapping is None: # If the mapping couldn't be parsed for any reason
                    QgsApplication.messageLog().logMessage("Field mapping '{}' was not found and couldn't be loaded. The default mapping is used instead!".format(field_mapping),
                                                           PLUGIN_NAME, Qgis.Warning)

            if mapping is None:
                mapping = get_refactor_fields_mapping(ladm_col_layer_name, self)

            self.activate_layer_requested.emit(input_layer)
            params = {
                'INPUT': input_layer.name(),
                'mapping': mapping,
                'output': output.name()
            }

            start_feature_count = output.featureCount()
            processing.execAlgorithmDialog("model:ETL-model", params)
            finish_feature_count = output.featureCount()

            self.check_if_and_enable_automatic_fields(db,
                                                      automatic_fields_definition,
                                                      ladm_col_layer_name)

            return finish_feature_count > start_feature_count
        else:
            self.message_emitted.emit(
                QCoreApplication.translate("QGISUtils",
                                           "Model ETL-model was not found and cannot be opened!"),
                Qgis.Info)
            return False

    def load_field_mapping(self, field_mapping):
        path_file_field_mapping = os.path.join(FIELD_MAPPING_PATH, '{}.{}'.format(field_mapping, "txt"))

        with open(path_file_field_mapping) as file_field_mapping:
            try:
                mapping = ast.literal_eval(file_field_mapping.read())
            except:
                mapping = None

        return mapping

    @_activate_processing_plugin
    def save_field_mapping(self, ladm_col_layer_name):
        if not os.path.exists(FIELD_MAPPING_PATH):
            os.makedirs(FIELD_MAPPING_PATH)

        log_path =  os.path.join(processing.tools.system.userFolder(), 'processing.log')

        with open(log_path) as log_file: # TODO, review this!!!
            contents = log_file.read().split("ALGORITHM")[-1]
            contents = contents.split('processing.run("model:ETL-model",')[-1]
            params = ast.literal_eval(contents.strip().strip(')'))

        name_field_mapping = "{}_{}.{}".format(ladm_col_layer_name,
                                               datetime.datetime.now().strftime("%Y%m%d_%H_%M_%S"),
                                               "txt")

        txt_field_mapping_path = os.path.join(FIELD_MAPPING_PATH, name_field_mapping)

        QgsApplication.messageLog().logMessage("Field mapping saved: {}".format(name_field_mapping), PLUGIN_NAME, Qgis.Info)

        with open(txt_field_mapping_path, "w+") as file:
            file.write(str(params['mapping']))

    def get_field_mappings_file_names(self, layer_name):
        files = glob.glob(os.path.join(FIELD_MAPPING_PATH, "{}_{}{}".format(layer_name, '[0-9]'*8, "*")))
        files.sort(key=lambda path: os.path.getmtime(path))

        # If there are more files than the expected for the same table, just drop the surplus
        if len(files) > MAXIMUM_FIELD_MAPPING_FILES_PER_TABLE:
            for path in files[0:len(files)-MAXIMUM_FIELD_MAPPING_FILES_PER_TABLE]:
                os.remove(path)

            files = files[len(files) - MAXIMUM_FIELD_MAPPING_FILES_PER_TABLE:]

        files.reverse()

        return [os.path.basename(file).strip(".txt") for file in files]

    def delete_old_field_mapping(self, field_mapping_name):
        file_path = os.path.join(FIELD_MAPPING_PATH, "{}.txt".format(field_mapping_name))
        if os.path.exists(file_path):
            os.remove(file_path)

    def build_boundary(self, db):
        self.turn_transaction_off()
        layer = self.get_layer_from_layer_tree(BOUNDARY_TABLE, db.schema)
        use_selection = True

        if layer is None:
            self.message_with_button_load_layer_emitted.emit(
                QCoreApplication.translate("QGISUtils", "First load the layer {} into QGIS!").format(BOUNDARY_TABLE),
                QCoreApplication.translate("QGISUtils", "Load layer {} now").format(BOUNDARY_TABLE), [BOUNDARY_TABLE, None],Qgis.Warning)
            return
        else:
            if layer.selectedFeatureCount() == 0:
                reply = QMessageBox.question(None,
                                             QCoreApplication.translate("QGISUtils", "Continue?"),
                                             QCoreApplication.translate("QGISUtils",
                                                                        "There are no selected boundaries, do you like to use all the {} boundaries in the data base?").format(layer.featureCount()),
                                             QMessageBox.Yes, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    use_selection = False
                else:
                    self.message_emitted.emit(
                        QCoreApplication.translate("QGISUtils", "First select at least one boundary!"),
                        Qgis.Warning)
                    return

        if use_selection:
            new_boundary_geoms, boundaries_to_del_ids = self.geometry.fix_selected_boundaries(layer)
            num_boundaries = layer.selectedFeatureCount()
        else:
            new_boundary_geoms, boundaries_to_del_ids = self.geometry.fix_boundaries(layer)
            num_boundaries = layer.featureCount()

        if len(new_boundary_geoms)  > 0:

            layer.startEditing()  # Safe, even if layer is already on editing state

            # the boundaries that are to be replaced are removed
            layer.deleteFeatures(boundaries_to_del_ids)

            # Create features based on segment geometries
            new_fix_boundary_features = list()
            for boundary_geom in new_boundary_geoms:
                feature = QgsVectorLayerUtils().createFeature(layer, boundary_geom)
                new_fix_boundary_features.append(feature)

            layer.addFeatures(new_fix_boundary_features)
            self.message_emitted.emit(
                QCoreApplication.translate("QGISUtils",
                                           "{} feature(s) was(were) analyzed generating {} boundary(ies)!").format(num_boundaries, len(new_fix_boundary_features)),
                Qgis.Info)
            self.map_refresh_requested.emit()
        else:
            self.message_emitted.emit(QCoreApplication.translate("QGISUtils", "There are no boundaries to build."), Qgis.Info)

    def fill_right_of_way_relations(self, db):
        layers = {
            ADMINISTRATIVE_SOURCE_TABLE: {'name': ADMINISTRATIVE_SOURCE_TABLE, 'geometry': None, LAYER: None},
            PARCEL_TABLE: {'name': PARCEL_TABLE, 'geometry': None, LAYER: None},
            PLOT_TABLE: {'name': PLOT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            RESTRICTION_TABLE: {'name': RESTRICTION_TABLE, 'geometry': None, LAYER: None},
            RIGHT_OF_WAY_TABLE: {'name': RIGHT_OF_WAY_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            RRR_SOURCE_RELATION_TABLE: {'name': RRR_SOURCE_RELATION_TABLE, 'geometry': None, LAYER: None},
            SURVEY_POINT_TABLE: {'name': SURVEY_POINT_TABLE, 'geometry': None, LAYER: None},
            UEBAUNIT_TABLE: {'name': UEBAUNIT_TABLE, 'geometry': None, LAYER: None}
        }

        # Load layers
        res_layers = self.get_layers(db, layers, load=True)
        if res_layers is None:
            return

        if layers[PLOT_TABLE][LAYER].selectedFeatureCount() == 0 or layers[RIGHT_OF_WAY_TABLE][LAYER].selectedFeatureCount() == 0 or layers[ADMINISTRATIVE_SOURCE_TABLE][LAYER].selectedFeatureCount() == 0:
            if self.get_layer_from_layer_tree(PLOT_TABLE, schema=db.schema, geometry_type=QgsWkbTypes.PolygonGeometry) is None:
                self.message_with_button_load_layer_emitted.emit(
                    QCoreApplication.translate("RightOfWay",
                                               "First load the layer {} into QGIS and select at least one plot!").format(PLOT_TABLE),
                    QCoreApplication.translate("RightOfWay", "Load layer {} now").format(PLOT_TABLE),
                    [PLOT_TABLE, None],
                    Qgis.Warning)
            else:
                self.message_emitted.emit(
                    QCoreApplication.translate("RightOfWay", "Select at least one benefited plot, one right of way and at least one administrative source to create relations!"),
                    Qgis.Warning)
                return
        else:
            ue_baunit_features = layers[UEBAUNIT_TABLE][LAYER].getFeatures()
            # Get unique pairs id_right_of_way-id_parcel
            existing_pairs = [(ue_baunit_feature[UEBAUNIT_TABLE_PARCEL_FIELD], ue_baunit_feature[UEBAUNIT_TABLE_RIGHT_OF_WAY_FIELD]) for ue_baunit_feature in ue_baunit_features]
            existing_pairs = set(existing_pairs)

            plot_ids = [f[ID_FIELD] for f in layers[PLOT_TABLE][LAYER].selectedFeatures()]

            right_of_way_id = layers[RIGHT_OF_WAY_TABLE][LAYER].selectedFeatures()[0].attribute(ID_FIELD)
            id_pairs = list()
            for plot in plot_ids:
                exp = "\"{uebaunit}\" = {plot}".format(uebaunit=UEBAUNIT_TABLE_PLOT_FIELD, plot=plot)
                parcels = layers[UEBAUNIT_TABLE][LAYER].getFeatures(exp)
                for parcel in parcels:
                    id_pair = (parcel.attribute(UEBAUNIT_TABLE_PARCEL_FIELD), right_of_way_id)
                    id_pairs.append(id_pair)

            if len(id_pairs) < len(plot_ids):
                # If any relationship plot-parcel is not found, we don't need to continue
                self.message_emitted.emit(
                    QCoreApplication.translate("RightOfWay", "One or more pairs id_plot-id_parcel weren't found, this is needed to create benefited and restriction relations."),
                    Qgis.Warning)
                return

            if id_pairs:
                new_features = list()
                for id_pair in id_pairs:
                    if not id_pair in existing_pairs:
                        #Create feature
                        new_feature = QgsVectorLayerUtils().createFeature(layers[UEBAUNIT_TABLE][LAYER])
                        new_feature.setAttribute(UEBAUNIT_TABLE_PARCEL_FIELD, id_pair[0])
                        new_feature.setAttribute(UEBAUNIT_TABLE_RIGHT_OF_WAY_FIELD, id_pair[1])
                        self.log.logMessage("Saving RightOfWay-Parcel: {}-{}".format(id_pair[1], id_pair[0]), PLUGIN_NAME, Qgis.Info)
                        new_features.append(new_feature)

                layers[UEBAUNIT_TABLE][LAYER].dataProvider().addFeatures(new_features)
                self.message_emitted.emit(
                    QCoreApplication.translate("RightOfWay",
                                       "{} out of {} records were saved into {}! {} out of {} records already existed in the database.").format(
                        len(new_features),
                        len(id_pairs),
                        UEBAUNIT_TABLE,
                        len(id_pairs) - len(new_features),
                        len(id_pairs)
                        ),
                        Qgis.Info)

            spatial_join_layer = processing.run("qgis:joinattributesbylocation",
                                                {
                                                    'INPUT': layers[PLOT_TABLE][LAYER],
                                                    'JOIN': QgsProcessingFeatureSourceDefinition(layers[RIGHT_OF_WAY_TABLE][LAYER].id(), True),
                                                    'PREDICATE': [0],
                                                    'JOIN_FIELDS': [ID_FIELD, RIGHT_OF_WAY_TABLE_IDENTIFICATOR_FIELD],
                                                    'METHOD': 0,
                                                    'DISCARD_NONMATCHING': True,
                                                    'PREFIX': '',
                                                    'OUTPUT': 'memory:'})['OUTPUT']

            restriction_features = layers[RESTRICTION_TABLE][LAYER].getFeatures()
            existing_restriction_pairs = [(restriction_feature[RESTRICTION_TABLE_PARCEL_FIELD], restriction_feature[RESTRICTION_TABLE_DESCRIPTION_FIELD]) for restriction_feature in restriction_features]
            existing_restriction_pairs = set(existing_restriction_pairs)
            id_pairs_restriction = list()
            plot_ids = spatial_join_layer.getFeatures()

            for plot in plot_ids:
                exp = "\"uebaunit\" = {plot}".format(uebaunit=UEBAUNIT_TABLE_PLOT_FIELD, plot=plot.attribute(ID_FIELD))
                parcels = layers[UEBAUNIT_TABLE][LAYER].getFeatures(exp)
                for parcel in parcels:
                    id_pair_restriction = (parcel.attribute(UEBAUNIT_TABLE_PARCEL_FIELD), "Asociada a la servidumbre {}".format(plot.attribute(RIGHT_OF_WAY_TABLE_IDENTIFICATOR_FIELD)))
                    id_pairs_restriction.append(id_pair_restriction)

            new_restriction_features = list()
            if id_pairs_restriction:
                for id_pair in id_pairs_restriction:
                    if not id_pair in existing_restriction_pairs:
                        #Create feature
                        new_feature = QgsVectorLayerUtils().createFeature(layers[RESTRICTION_TABLE][LAYER])
                        new_feature.setAttribute(RESTRICTION_TABLE_PARCEL_FIELD, id_pair[0])
                        new_feature.setAttribute(RESTRICTION_TABLE_DESCRIPTION_FIELD, id_pair[1])
                        new_feature.setAttribute(TYPE_FIELD, COL_RESTRICTION_TYPE_RIGHT_OF_WAY_VALUE)
                        self.log.logMessage("Saving RightOfWay-Parcel: {}-{}".format(id_pair[1], id_pair[0]), PLUGIN_NAME, Qgis.Info)
                        new_restriction_features.append(new_feature)

                layers[RESTRICTION_TABLE][LAYER].dataProvider().addFeatures(new_restriction_features)
                self.message_emitted.emit(
                    QCoreApplication.translate("RightOfWay",
                                       "{} out of {} records were saved into {}! {} out of {} records already existed in the database.").format(
                        len(new_restriction_features),
                        len(id_pairs_restriction),
                        RESTRICTION_TABLE,
                        len(id_pairs_restriction) - len(new_restriction_features),
                        len(id_pairs_restriction)
                        ),
                        Qgis.Info)

            administrative_source_ids = [f[ID_FIELD] for f in layers[ADMINISTRATIVE_SOURCE_TABLE][LAYER].selectedFeatures()]

            source_relation_features = layers[RRR_SOURCE_RELATION_TABLE][LAYER].getFeatures()

            existing_source_pairs = [(source_relation_feature[RRR_SOURCE_SOURCE_FIELD], source_relation_feature[RRR_SOURCE_RESTRICTION_FIELD]) for source_relation_feature in source_relation_features]
            existing_source_pairs = set(existing_source_pairs)

            rrr_source_relation_pairs = list()

            for administrative_source_id in administrative_source_ids:
                for restriction_feature in new_restriction_features:
                    rrr_source_relation_pair = (administrative_source_id, restriction_feature.attribute(ID_FIELD))
                    rrr_source_relation_pairs.append(rrr_source_relation_pair)

            new_rrr_source_relation_features = list()
            if rrr_source_relation_pairs:
                for id_pair in rrr_source_relation_pairs:
                    if not id_pair in existing_source_pairs:
                        new_feature = QgsVectorLayerUtils().createFeature(layers[RRR_SOURCE_RELATION_TABLE][LAYER])
                        new_feature.setAttribute(RRR_SOURCE_SOURCE_FIELD, id_pair[0])
                        new_feature.setAttribute(RRR_SOURCE_RESTRICTION_FIELD, id_pair[1])
                        self.log.logMessage("Saving Restriction-Source: {}-{}".format(id_pair[1], id_pair[0]), PLUGIN_NAME, Qgis.Info)
                        new_rrr_source_relation_features.append(new_feature)

                layers[RRR_SOURCE_RELATION_TABLE][LAYER].dataProvider().addFeatures(new_rrr_source_relation_features)
                self.message_emitted.emit(
                    QCoreApplication.translate("RightOfWay",
                                       "{} out of {} records were saved into {}! {} out of {} records already existed in the database.").format(
                        len(new_rrr_source_relation_features),
                        len(rrr_source_relation_pairs),
                        RRR_SOURCE_RELATION_TABLE,
                        len(rrr_source_relation_pairs) - len(new_rrr_source_relation_features),
                        len(rrr_source_relation_pairs)
                        ),
                        Qgis.Info)

    def upload_source_files(self, db):
        extfile_layer = self.get_layer(db, EXTFILE_TABLE, None, True)
        if extfile_layer is None:
            return

        field_index = extfile_layer.fields().indexFromName(EXTFILE_DATA_FIELD)
        features = list()

        if extfile_layer.selectedFeatureCount():
            features = extfile_layer.selectedFeatures()
        else:
            features = [f for f in extfile_layer.getFeatures()]

        self._source_handler = self.get_source_handler()
        with OverrideCursor(Qt.WaitCursor):
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
        finally:
            try:
                # s might not exist if socket.create_connection breaks
                s.close()
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

    def suppress_form(self, layer, suppress=True):
        if layer:
            form_config = layer.editFormConfig()
            if suppress:
                form_config.setSuppress(QgsEditFormConfig.SuppressOn)
            else:
                form_config.setSuppress(QgsEditFormConfig.SuppressOff)
            layer.setEditFormConfig(form_config)

    def get_new_feature(self, layer, is_spatial=False):
        self.suppress_form(layer, True)

        if not is_spatial:
            self.action_add_feature_requested.emit()

        new_feature = None
        for i in layer.editBuffer().addedFeatures():
            new_feature = layer.editBuffer().addedFeatures()[i]
            break

        self.suppress_form(layer, False)
        return new_feature

    def active_snapping_all_layers(self, tolerance=12):
        # Configure Snapping
        snapping = QgsProject.instance().snappingConfig()
        snapping.setEnabled(True)
        snapping.setMode(QgsSnappingConfig.AllLayers)
        snapping.setType(QgsSnappingConfig.Vertex)
        snapping.setUnits(QgsTolerance.Pixels)
        snapping.setTolerance(tolerance)
        QgsProject.instance().setSnappingConfig(snapping)

    def active_snapping_layers(self, layers, tolerance=15):
        # Configure Snapping
        snapping = QgsProject.instance().snappingConfig()
        snapping.setEnabled(True)
        snapping.setMode(QgsSnappingConfig.AdvancedConfiguration)

        for layer in layers:
            snapping.setIndividualLayerSettings(layer,
                                                QgsSnappingConfig.IndividualLayerSettings(True,
                                                                                          QgsSnappingConfig.Vertex, tolerance,
                                                                                          QgsTolerance.Pixels))
        QgsProject.instance().setSnappingConfig(snapping)
