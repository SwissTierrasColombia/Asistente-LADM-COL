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
import json
import os

from qgis.PyQt.QtCore import (Qt,
                              QObject,
                              pyqtSignal,
                              QCoreApplication,
                              QSettings,
                              QEventLoop,
                              QTextStream,
                              QIODevice,
                              QUrl)
from qgis.PyQt.QtWidgets import (QProgressBar,
                                 QDialog)
from qgis.PyQt.QtNetwork import (QNetworkAccessManager,
                                 QNetworkRequest)
from qgis.core import (Qgis,
                       QgsApplication,
                       QgsEditFormConfig,
                       QgsAttributeEditorContainer,
                       QgsAttributeEditorElement,
                       QgsDefaultValue,
                       QgsEditorWidgetSetup,
                       QgsExpression,
                       QgsExpressionContextUtils,
                       QgsFieldConstraints,
                       QgsLayerTreeGroup,
                       QgsLayerTreeNode,
                       QgsMapLayer,
                       QgsOptionalExpression,
                       QgsProject,
                       QgsTolerance,
                       QgsSnappingConfig,
                       QgsProperty,
                       QgsRelation,
                       QgsVectorLayer)

import processing

from asistente_ladm_col.gui.dialogs.dlg_topological_edition import LayersForTopologicalEditionDialog
from asistente_ladm_col.utils.decorators import _activate_processing_plugin
from asistente_ladm_col.lib.geometry import GeometryUtils
from asistente_ladm_col.utils.qgis_model_baker_utils import QgisModelBakerUtils
from asistente_ladm_col.utils.qt_utils import (OverrideCursor,
                                               ProcessWithStatus)
from asistente_ladm_col.utils.utils import is_connected
from asistente_ladm_col.utils.symbology import SymbologyUtils
from asistente_ladm_col.config.general_config import (DEFAULT_EPSG,
                                                      FIELD_MAPPING_PATH,
                                                      MAXIMUM_FIELD_MAPPING_FILES_PER_TABLE,
                                                      TEST_SERVER,
                                                      DEFAULT_ENDPOINT_SOURCE_SERVICE,
                                                      SOURCE_SERVICE_EXPECTED_ID)
from asistente_ladm_col.config.enums import EnumLayerRegistryType
from asistente_ladm_col.config.transitional_system_config import TransitionalSystemConfig
from asistente_ladm_col.config.layer_config import LayerConfig
from asistente_ladm_col.config.refactor_fields_mappings import RefactorFieldsMappings
from asistente_ladm_col.config.query_names import QueryNames
from asistente_ladm_col.config.ladm_names import LADMNames
from asistente_ladm_col.config.translation_strings import (TranslatableConfigStrings,
                                                           ERROR_LAYER_GROUP)
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.lib.source_handler import SourceHandler


class QGISUtils(QObject):
    action_add_feature_requested = pyqtSignal()
    action_vertex_tool_requested = pyqtSignal()
    activate_layer_requested = pyqtSignal(QgsMapLayer)
    create_progress_message_bar_emitted = pyqtSignal(str, QProgressBar)
    remove_error_group_requested = pyqtSignal()
    layer_symbology_changed = pyqtSignal(str) # layer id
    map_refresh_requested = pyqtSignal()
    map_freeze_requested = pyqtSignal(bool)
    set_node_visibility_requested = pyqtSignal(QgsLayerTreeNode, bool)
    zoom_full_requested = pyqtSignal()
    zoom_to_selected_requested = pyqtSignal()

    def __init__(self, layer_tree_view=None):
        QObject.__init__(self)
        self.layer_tree_view = layer_tree_view
        self.logger = Logger()
        self.qgis_model_baker_utils = QgisModelBakerUtils()
        self.symbology = SymbologyUtils()
        self.geometry = GeometryUtils()
        self.translatable_config_strings = TranslatableConfigStrings()
        self.refactor_fields = RefactorFieldsMappings()

        self._source_handler = None
        self._layers = list()
        self._relations = list()
        self._bags_of_enum = dict()

    def get_source_handler(self):
        if self._source_handler is None:
            self._source_handler = SourceHandler(self)
        return self._source_handler

    def cache_layers_and_relations(self, db, ladm_col_db, db_source):
        self.logger.debug(__name__, "Cache layers and relations called (LADM-COL DB: {})".format(ladm_col_db))
        if ladm_col_db:
            msg = QCoreApplication.translate("QGISUtils",
                "Extracting relations and domains from the database... This is done only once per session!")
            with ProcessWithStatus(msg):
                self._layers, self._relations, self._bags_of_enum = self.qgis_model_baker_utils.get_layers_and_relations_info(db)
        else:
            self.clear_db_cache()

    def clear_db_cache(self):
        self._layers = list()
        self._relations = list()
        self._bags_of_enum = list()

    def get_related_layers(self, layer_names, ladm_layers):
        """
        For a given layer we load its domains, all its related layers and the
        domains of those related layers. Additionally, we load its related
        structures and domains to build bags_of_enum widgets.

        :param layer_names: list of layer names from which we want to obtain related layers
        :param ladm_layers: dict of ladm_layers currently loaded
        """
        already_loaded = list(ladm_layers.keys())  # List of loaded ladm layer names
        related_layers = list()
        for relation in self._relations:  # Takes into account both domains and not-domain layers
            for layer_name in layer_names:
                if relation[QueryNames.REFERENCING_LAYER] == layer_name:
                    if relation[QueryNames.REFERENCED_LAYER] not in already_loaded and relation[QueryNames.REFERENCED_LAYER] not in layer_names:
                        related_layers.append(relation[QueryNames.REFERENCED_LAYER])

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
            for layer_name in layer_names:
                if relation[QueryNames.REFERENCING_LAYER] == layer_name:
                    if relation[QueryNames.REFERENCED_LAYER] not in already_loaded:
                        related_domains.append(relation[QueryNames.REFERENCED_LAYER])

        return related_domains

    def get_layer(self, db, layer_name, load=False, emit_map_freeze=True, layer_modifiers=dict()):
        # Handy function to get a single layer
        layer = {layer_name: None}
        self.get_layers(db, layer, load, emit_map_freeze, layer_modifiers=layer_modifiers)
        if not layer:
            return None

        return layer[layer_name]

    def get_layers(self, db, layers, load=False, emit_map_freeze=True, layer_modifiers=dict()):
        """
        Load LADM-COL layers to QGIS.

        :param db: db connection instance
        :param layers: parameter passed by reference, i.e., it will be updated {layer_name : None}
            layer_name: layer name as it is stored in the db
            layer: key to store the QgsVectorLayer object.
            The whole dict will be None if any of the requested layers is not found. A message will inform which layer
            wasn't found.
        :param load: Whether to load layer in the layer tree/map canvas or not (if not, it'll only be added to registry)
        :param emit_map_freeze: False can be used for subsequent calls to get_layers (e.g., from differente dbs), where
        one could be interested in handling the map_freeze from the outside
        :param layer_modifiers: is a dict that it have properties that modify the layer properties
        like prefix_layer_name, suffix_layer_name, symbology_group
        """
        if emit_map_freeze:
            self.map_freeze_requested.emit(True)

        with OverrideCursor(Qt.WaitCursor):
            if not load:
                # We don't need the layers to be loaded (to layer tree), so, check if the layer is in QGIS and use it or
                # if not found just add it to the registry! Note: for layers added to registry we don't load related
                # tables nor domains!
                ladm_layers = self.get_ladm_layers_from_qgis(db)
                for layer_name in layers.keys():
                    layers[layer_name] = ladm_layers[layer_name] if layer_name in ladm_layers else self.load_layer_to_registry(db, layer_name)

            else:  # We want to load the layers
                # First, use already loaded layers
                ladm_layers = self.get_ladm_layers_from_qgis(db, EnumLayerRegistryType.IN_LAYER_TREE)
                for layer_name in layers.keys():
                    layers[layer_name] = ladm_layers[layer_name] if layer_name in ladm_layers else None

                # Let's load the remaining layers
                layers_to_load = [layer_name for layer_name,layer in layers.items() if layer is None]

                if layers_to_load:
                    # Get related layers from cached relations and add them to
                    # list of layers to load, QGIS Model Baker will set relations
                    additional_layers_to_load = self.get_related_layers(layers_to_load, ladm_layers)
                    all_layers_to_load = list(set(layers_to_load + additional_layers_to_load))

                    # Required layers that are only in registry are removed, we reload them to get everything configured
                    self.remove_registry_layers(db, all_layers_to_load)

                    self.logger.status(QCoreApplication.translate("QGISUtils", "Loading LADM_COL layers to QGIS and configuring their relations and forms..."))
                    self.qgis_model_baker_utils.load_layers(db, all_layers_to_load)
                    ladm_layers = self.get_ladm_layers_from_qgis(db, EnumLayerRegistryType.IN_LAYER_TREE)  # Update

                    # Now that all layers are loaded, update response dict
                    # and apply post_load_configurations to all new layers
                    for layer_name, layer in ladm_layers.items():
                        if layer_name in all_layers_to_load:  # Discard already loaded layers
                            if layer_name in layers_to_load:
                                layers[layer_name] = layer  # If originally requested, store layer object in dict

                            # Turn off layers loaded as related layers
                            layer_modifiers[LayerConfig.VISIBLE_LAYER_MODIFIERS] = layer_name in layers_to_load
                            self.post_load_configurations(db, layer, layer_name, layer_modifiers=layer_modifiers)

                    self.logger.clear_status()

        if emit_map_freeze:
            self.map_freeze_requested.emit(False)

        if load:
            self.map_refresh_requested.emit()
            self.activate_layer_requested.emit(list(layers.values())[0])

        # Verifies that the layers have been successfully loaded
        layer_not_loaded = False
        for layer_name, layer in layers.items():
            if layer is None:
                layer_not_loaded = True
                self.logger.warning_msg(__name__, QCoreApplication.translate("QGISUtils",
                    "{layer_name} layer couldn't be found... {description}").format(
                        layer_name=layer_name,
                        description=db.get_display_conn_string()))

        if layer_not_loaded:  # If it is not possible to obtain the requested layers we make the variable layers None
            layers = None

    def remove_registry_layers(self, db, layer_names):
        """
        :param db: DB connection
        :param layer_names: list of layer names from which registry layers should be removed
        """
        registry_layers = self.get_ladm_layers_from_qgis(db, EnumLayerRegistryType.ONLY_IN_REGISTRY)
        QgsProject.instance().removeMapLayers([layer.id() for layer_name,layer in registry_layers.items() if layer_name in layer_names])

    def load_layer_to_registry(self, db, layer_name):
        """ Load layer to registry, not to tree view/map canvas """
        layers = self.qgis_model_baker_utils.get_required_layers_without_load([layer_name], db)
        return layers[0] if layers else None

    @staticmethod
    def get_ladm_layer_from_qgis(db, layer_name, registry_type=None):
        """
        :param db: DB connection
        :param layer_name: layer name
        :param registry_type: None if no filter should be applied (i.e., layer can be only in registry or also in tree
                              view), otherwise, value of EnumLayerRegistryType to filter only registry layers or
                              tree view (and therefore also in registry).
        :return: QgsVectorLayer
        """
        for k, layer in QgsProject.instance().mapLayers().items():
            name = db.get_ladm_layer_name(layer, validate_is_ladm=True)  # get layer name from provider

            if name and name == layer_name:
                in_layer_tree = QgsProject.instance().layerTreeRoot().findLayer(layer) if registry_type else None

                if not registry_type or (registry_type == EnumLayerRegistryType.IN_LAYER_TREE and in_layer_tree) or \
                        (registry_type == EnumLayerRegistryType.ONLY_IN_REGISTRY and not in_layer_tree):
                    return layer

        return None

    @staticmethod
    def get_ladm_layers_from_qgis(db, registry_type=None):
        """
        Note that this method only gets ladm layers from the db connection. Even if you have layers from several db's
        loaded in QGIS, this method will filter only those that correspond to the db passed.

        :param db: DB connection
        :param registry_type: None if no filter should be applied (i.e., layer can be only in registry or also in tree
                              view), otherwise, value of EnumLayerRegistryType to filter only registry layers or
                              tree view (and therefore also in registry).
        :return: dict where key is ladm layer name and value is QgsVectorLayer
        """
        ladm_layers = dict()
        for k, layer in QgsProject.instance().mapLayers().items():
            name = db.get_ladm_layer_name(layer, validate_is_ladm=True)  # get layer name from provider

            if name:  # If no ladm_layer, name is None
                in_layer_tree = QgsProject.instance().layerTreeRoot().findLayer(layer) if registry_type else None

                if not registry_type or (registry_type == EnumLayerRegistryType.IN_LAYER_TREE and in_layer_tree) or \
                        (registry_type == EnumLayerRegistryType.ONLY_IN_REGISTRY and not in_layer_tree):
                    ladm_layers[name] = layer

        return ladm_layers

    def required_layers_are_available(self, db, layers, tool_name):
        msg = QCoreApplication.translate("AsistenteLADMCOLPlugin",
                "'{}' tool has been closed because there was a problem loading the requeries layers.").format(tool_name)

        if None in layers:
            self.logger.warning_msg(__name__, msg)
            return False

        # Load layers
        self.get_layers(db, layers, load=True)
        if not layers or layers is None:
            self.logger.warning_msg(__name__, msg)
            return False

        # Check if any layer is in editing mode
        layers_name = list()
        for layer_name, layer in layers.items():
            if layer is not None and layer.isEditable():
                layers_name.append(layer_name)

        if layers_name:
            self.logger.warning_msg(__name__, QCoreApplication.translate("AsistenteLADMCOLPlugin",
                "'{}' cannot be opened until the following layers are not in edit mode '{}'.").format(
                    tool_name,
                    '; '.join(layers_name)))
            return False

        return True

    def automatic_namespace_local_id_configuration_changed(self, db):
        for layer_name, layer in self.get_ladm_layers_from_qgis(db).items():
            self.set_automatic_fields_namespace_local_id(db, layer_name, layer)

    def post_load_configurations(self, db, layer, layer_name, layer_modifiers=dict()):
        # TODO: Just call this method once after get_layers (IMPORTANT!)
        # Do some post-load work, such as setting styles or setting automatic fields for that layer
        self.configure_missing_relations(db, layer, layer_name)
        self.configure_missing_bags_of_enum(db, layer, layer_name)
        self.set_display_expressions(db, layer, layer_name)
        self.set_layer_variables(db, layer, layer_name)
        self.set_custom_widgets(db, layer, layer_name)
        self.set_custom_read_only_fiels(db, layer, layer_name)
        self.set_custom_events(db, layer, layer_name)
        self.set_automatic_fields(db, layer, layer_name)
        self.set_layer_constraints(db, layer, layer_name)
        self.set_form_groups(db, layer, layer_name)
        self.set_custom_layer_name(db, layer, layer_modifiers=layer_modifiers)

        if layer.isSpatial():
            self.symbology.set_layer_style_from_qml(db, layer, layer_modifiers=layer_modifiers)

            visible = False
            if LayerConfig.VISIBLE_LAYER_MODIFIERS in layer_modifiers:
                visible = layer_modifiers[LayerConfig.VISIBLE_LAYER_MODIFIERS]
            self.set_layer_visibility(layer, visible)

    def set_custom_layer_name(self, db, layer, layer_modifiers=dict()):
        if db is None:
            return

        full_layer_name = ''
        layer_name = layer.name()

        if LayerConfig.PREFIX_LAYER_MODIFIERS in layer_modifiers:
            if layer_modifiers[LayerConfig.PREFIX_LAYER_MODIFIERS]:
                full_layer_name = layer_modifiers[LayerConfig.PREFIX_LAYER_MODIFIERS]

        full_layer_name += layer_name

        if LayerConfig.SUFFIX_LAYER_MODIFIERS in layer_modifiers:
            if layer_modifiers[LayerConfig.SUFFIX_LAYER_MODIFIERS]:
                full_layer_name += layer_modifiers[LayerConfig.SUFFIX_LAYER_MODIFIERS]

        if full_layer_name and full_layer_name != layer_name:
            layer.setName(full_layer_name)

    def configure_missing_relations(self, db, layer, layer_name):
        """
        Relations between newly loaded layers and already loaded layer cannot
        be handled by QGIS Model Baker (which only sets relations between
        loaded layers), so we do it in the Asistente LADM_COL!
        """
        db_relations = list()
        for relation in self._relations:
            if relation[QueryNames.REFERENCING_LAYER] == layer_name:
                db_relations.append(relation)

        # Get already existent QGIS relations where this layer is the referencing layer
        qgis_relations = QgsProject.instance().relationManager().referencingRelations(layer)
        qgis_rels = list()
        for qgis_relation in qgis_relations:
            qgis_rel = dict()
            referenced_layer = qgis_relation.referencedLayer()
            qgis_rel[QueryNames.REFERENCED_LAYER] = db.get_ladm_layer_name(referenced_layer)
            qgis_rel[QueryNames.REFERENCED_FIELD] = referenced_layer.fields()[qgis_relation.referencedFields()[0]].name()
            qgis_rel[QueryNames.REFERENCING_FIELD] = layer.fields()[qgis_relation.referencingFields()[0]].name()
            qgis_rels.append(qgis_rel)

        new_relations = list()
        # Compare relations and configure what is missing
        for db_relation in db_relations:
            found = False
            for qgis_rel in qgis_rels:
                # We known that referencing_layer already matches, so don't check
                if qgis_rel[QueryNames.REFERENCED_LAYER] == db_relation[QueryNames.REFERENCED_LAYER] and \
                        qgis_rel[QueryNames.REFERENCING_FIELD] == db_relation[QueryNames.REFERENCING_FIELD] and \
                        qgis_rel[QueryNames.REFERENCED_FIELD] == db_relation[QueryNames.REFERENCED_FIELD]:
                    found = True
                    break

            if not found:
                # This relation is not configured in QGIS, let's do it!
                new_rel = QgsRelation()
                new_rel.setReferencingLayer(layer.id())
                referenced_layer = self.get_ladm_layer_from_qgis(db, db_relation[QueryNames.REFERENCED_LAYER])
                if referenced_layer is None:
                    continue  # Referenced_layer NOT FOUND in layer tree...
                new_rel.setReferencedLayer(referenced_layer.id())
                new_rel.addFieldPair(db_relation[QueryNames.REFERENCING_FIELD],
                    db_relation[QueryNames.REFERENCED_FIELD])
                new_rel.setId(db_relation[QueryNames.RELATION_NAME_MODEL_BAKER])
                new_rel.setName(db_relation[QueryNames.RELATION_NAME_MODEL_BAKER])

                new_relations.append(new_rel)

        all_qgis_relations = list(QgsProject.instance().relationManager().relations().values())
        all_qgis_relations.extend(new_relations)
        QgsProject.instance().relationManager().setRelations(all_qgis_relations)

    def configure_missing_bags_of_enum(self, db, layer, layer_name):
        """
        Bags of enums between newly loaded layers and already loaded layers
        cannot be handled by qgis model baker (which only sets relations
        between loaded layers), so we do it in the Asistente LADM_COL.
        """
        if layer_name in self._bags_of_enum:
            for k,v in self._bags_of_enum[layer_name].items():
                # Check if bag of enum field has already a value relation
                # configured or not
                idx = layer.fields().indexOf(k)
                if layer.editorWidgetSetup(idx).type() == 'ValueRelation':
                    continue

                domain = self.get_ladm_layer_from_qgis(db, v[2])
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

    def set_display_expressions(self, db, layer, layer_name):
        dict_display_expressions = LayerConfig.get_dict_display_expressions(db.names)
        if layer_name in dict_display_expressions:
            layer.setDisplayExpression(dict_display_expressions[layer_name])

    def set_layer_variables(self, db, layer, layer_name):
        layer_variables = LayerConfig.get_layer_variables(db.names)
        if layer_name in layer_variables:
            for variable, value in layer_variables[layer_name].items():
                QgsExpressionContextUtils.setLayerVariable(layer, variable, value)

    def set_custom_widgets(self, db, layer, layer_name):
        custom_widget_configuration = LayerConfig.get_custom_widget_configuration(db.names)
        if layer_name in custom_widget_configuration:
            editor_widget_setup = QgsEditorWidgetSetup(custom_widget_configuration[layer_name]['type'],
                                                       custom_widget_configuration[layer_name]['config'])
            if layer_name == db.names.EXT_ARCHIVE_S:
                index = layer.fields().indexFromName(db.names.EXT_ARCHIVE_S_DATA_F)
            elif layer_name == db.names.OP_BUILDING_UNIT_T:
                index = layer.fields().indexFromName(db.names.OP_BUILDING_UNIT_T_TOTAL_FLOORS_F)

            layer.setEditorWidgetSetup(index, editor_widget_setup)

    def set_custom_read_only_fiels(self, db, layer, layer_name):
        custom_read_only_fields = LayerConfig.get_custom_read_only_fields(db.names)
        if layer_name in custom_read_only_fields:
            for field in custom_read_only_fields[layer_name]:
                self.set_read_only_field(layer, field)

    @staticmethod
    def set_read_only_field(layer, field, read_only=True):
        field_idx = layer.fields().indexFromName(field)
        if layer.fields().exists(field_idx):
            formConfig = layer.editFormConfig()
            formConfig.setReadOnly(field_idx, read_only)
            layer.setEditFormConfig(formConfig)

    def set_custom_events(self, db, layer, layer_name):
        if layer_name == db.names.EXT_ARCHIVE_S:
            self._source_handler = self.get_source_handler()
            self._source_handler.handle_source_upload(db, layer, db.names.EXT_ARCHIVE_S_DATA_F)

    def set_layer_constraints(self, db, layer, layer_name):
        layer_constraints = LayerConfig.get_layer_constraints(db.names)
        if layer_name in layer_constraints:
            for field_name, value in layer_constraints[layer_name].items():
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

    def set_form_groups(self, db, layer, layer_name):
        if layer_name in LADMNames.FORM_GROUPS:
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
            for group_name, group_def in LADMNames.FORM_GROUPS[layer_name].items():
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
                    for group_name, group_def in LADMNames.FORM_GROUPS[layer_name].items():
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
            for group_name, group_def in LADMNames.FORM_GROUPS[layer_name].items():
                if group_name not in containers: # Still not added (no before/after attrs)
                    new_general_tab.addChildElement(group_def['container'])

            irc.addChildElement(new_general_tab)

    def configure_automatic_fields(self, db, layer, list_dicts_field_expression):
        for dict_field_expression in list_dicts_field_expression:
            for field, expression in dict_field_expression.items(): # There should be one key and one value
                index = layer.fields().indexFromName(field)
                default_value = QgsDefaultValue(expression, True) # Calculate on update
                layer.setDefaultValueDefinition(index, default_value)
                self.logger.info(__name__, "Automatic value configured: Layer '{}', field '{}', expression '{}'.".format(
                    layer.name(), field, expression))

    def reset_automatic_field(self, db, layer, field):
        self.configure_automatic_fields(db, layer, [{field: ""}])

    def set_automatic_fields(self, db, layer, layer_name):
        self.set_automatic_fields_namespace_local_id(db, layer_name, layer)

        if layer.fields().indexFromName(db.names.VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F) != -1:
            self.configure_automatic_fields(db, layer, [{db.names.VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F: "now()"}])

        dict_automatic_values = LayerConfig.get_dict_automatic_values(db.names)
        if layer_name in dict_automatic_values:
            self.configure_automatic_fields(db, layer, dict_automatic_values[layer_name])

    def set_automatic_fields_namespace_local_id(self, db, layer_name, layer):
        ns_enabled, ns_field, ns_value = self.get_namespace_field_and_value(db.names, layer_name)
        lid_enabled, lid_field, lid_value = self.get_local_id_field_and_value(db.names, layer_name)

        if ns_enabled and ns_field:
            self.configure_automatic_fields(db, layer, [{ns_field: ns_value}])
        elif not ns_enabled and ns_field:
            self.reset_automatic_field(db, layer, ns_field)

        if lid_enabled and lid_field:
            self.configure_automatic_fields(db, layer, [{lid_field: lid_value}])
        elif not lid_enabled and lid_field:
            self.reset_automatic_field(db, layer, lid_field)

    def get_namespace_field_and_value(self, names, layer_name):
        namespace_enabled = QSettings().value('Asistente-LADM_COL/automatic_values/namespace_enabled', True, bool)
        namespace_field = names.OID_T_NAMESPACE_F

        if namespace_field is not None:
            namespace = str(QSettings().value('Asistente-LADM_COL/automatic_values/namespace_prefix', ""))
            namespace_value = "'{}{}{}'".format(namespace, "_" if namespace else "", layer_name).upper()
        else:
            namespace_value = None

        return (namespace_enabled, namespace_field, namespace_value)

    def get_local_id_field_and_value(self, names, layer_name):
        local_id_enabled = QSettings().value('Asistente-LADM_COL/automatic_values/local_id_enabled', True, bool)
        local_id_field = names.OID_T_LOCAL_ID_F

        if local_id_field is not None:
            # TODO: Update expression to update local_id incrementally
            #local_id_value = "to_string(layer_property(@layer_name, 'feature_count') + @row_number)"
            local_id_value = "$id"
        else:
            local_id_value = None

        return (local_id_enabled, local_id_field, local_id_value)

    def check_if_and_disable_automatic_fields(self, db, layer_name):
        """
        Check settings to see if the user wants to calculate automatic values
        when in batch mode. If not, disable automatic fields and return
        expressions so that they can be restored after the batch load.
        """
        settings = QSettings()
        automatic_fields_definition = {}
        if not settings.value('Asistente-LADM_COL/automatic_values/automatic_values_in_batch_mode', True, bool):
            automatic_fields_definition = self.disable_automatic_fields(db, layer_name)

        return automatic_fields_definition

    def disable_automatic_fields(self, db, layer_name):
        layer = self.get_layer(db, layer_name, True)
        automatic_fields_definition = {idx: layer.defaultValueDefinition(idx) for idx in layer.attributeList()}

        for field in layer.fields():
            self.reset_automatic_field(db, layer, field.name())

        return automatic_fields_definition

    def check_if_and_enable_automatic_fields(self, db, automatic_fields_definition, layer_name):
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
                                             layer_name)

    def enable_automatic_fields(self, db, automatic_fields_definition, layer_name):
        layer = self.get_layer(db, layer_name, True)

        for idx, default_definition in automatic_fields_definition.items():
            layer.setDefaultValueDefinition(idx, default_definition)

    def set_error_group_visibility(self, visible):
        self.set_node_visibility(self.get_error_layers_group(), visible)

    def set_layer_visibility(self, layer, visible):
        node = QgsProject.instance().layerTreeRoot().findLayer(layer.id())
        self.set_node_visibility(node, visible)

    def set_node_visibility(self, node, visible):
        self.set_node_visibility_requested.emit(node, visible)

    def csv_to_layer(self, csv_path, delimiter, longitude, latitude, epsg, elevation=None, decimal_point='.'):
        if not csv_path or not os.path.exists(csv_path):
            self.logger.warning_msg(__name__, QCoreApplication.translate("QGISUtils",
                                                                         "No CSV file given or file doesn't exist."))
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
            self.logger.warning_msg(__name__, QCoreApplication.translate("QGISUtils",
                                                                         "CSV layer not valid!"))
            return False

        # Necessary export to have edit capabilities in the dataprovider
        csv_layer.selectAll()
        csv_layer_export = processing.run("native:saveselectedfeatures", {'INPUT': csv_layer, 'OUTPUT': 'memory:'})['OUTPUT']
        csv_layer.removeSelection()

        return csv_layer_export

    @_activate_processing_plugin
    def copy_csv_to_db(self, csv_layer, db, target_layer_name):
        QgsProject.instance().addMapLayer(csv_layer)

        if not csv_layer or not csv_layer.isValid():
            return

        # Skip checking point overlaps if layer is Survey points
        if target_layer_name != db.names.OP_SURVEY_POINT_T:
            overlapping = self.geometry.get_overlapping_points(csv_layer) # List of lists of ids
            overlapping = [id for items in overlapping for id in items] # Build a flat list of ids

            if overlapping:
                self.logger.warning_msg(__name__, QCoreApplication.translate("QGISUtils",
                    "There are overlapping points, we cannot import them into the DB! See selected points."))
                csv_layer.selectByIds(overlapping)
                self.zoom_to_selected_requested.emit()
                return False

        target_point_layer = self.get_layer(db, target_layer_name, load=True)
        initial_feature_count = target_point_layer.featureCount()

        if not target_point_layer:
            return False

        self.run_etl_model_in_backgroud_mode(db, csv_layer, target_layer_name)
        QgsProject.instance().removeMapLayer(csv_layer)

        features_added = target_point_layer.featureCount() > initial_feature_count
        new_features = target_point_layer.featureCount() - initial_feature_count

        if features_added:
            self.zoom_full_requested.emit()
            self.logger.info_msg(__name__, QCoreApplication.translate("QGISUtils",
                "{} points were added succesfully to '{}'.").format(new_features, target_layer_name))
        else:
            self.logger.warning_msg(__name__, QCoreApplication.translate("QGISUtils",
                "No point was added to '{}'.").format(target_layer_name))
            return False

        return True

    def get_ladm_layers_in_edit_mode_with_edit_buffer_is_modified(self, db):
        layers = list()
        for layer in QgsProject.instance().mapLayers().values():
            if db.is_ladm_layer(layer):
                if layer.isEditable():
                    if layer.editBuffer().isModified():
                        layers.append(layer)
        return layers

    def get_error_layers_group(self):
        """
        Get the topology errors group. If it exists but is placed in another
        position rather than the top, it moves the group to the top.
        """
        root = QgsProject.instance().layerTreeRoot()
        translated_strings = self.translatable_config_strings.get_translatable_config_strings()
        group = root.findGroup(translated_strings[ERROR_LAYER_GROUP])
        if group is None:
            group = root.insertGroup(0, translated_strings[ERROR_LAYER_GROUP])
        elif not self.layer_tree_view.layerTreeModel().node2index(group).row() == 0 or type(group.parent()) is QgsLayerTreeGroup:
            group_clone = group.clone()
            root.insertChildNode(0, group_clone)
            parent = group.parent()
            parent.removeChildNode(group)
            group = group_clone
        return group

    def error_group_exists(self):
        root = QgsProject.instance().layerTreeRoot()
        translated_strings = self.translatable_config_strings.get_translatable_config_strings()
        return root.findGroup(translated_strings[ERROR_LAYER_GROUP]) is not None

    @_activate_processing_plugin
    def run_etl_model_in_backgroud_mode(self, db, input_layer, ladm_col_layer_name):
        output_layer = self.get_layer(db, ladm_col_layer_name, load=True)
        start_feature_count = output_layer.featureCount()

        if not output_layer:
            return False

        if output_layer.isEditable():
            self.logger.warning_msg(__name__, QCoreApplication.translate("QGISUtils",
                "You need to close the edit session on layer '{}' before using this tool!").format(ladm_col_layer_name))
            return False

        model = QgsApplication.processingRegistry().algorithmById("model:ETL-model")
        if model:
            automatic_fields_definition = self.check_if_and_disable_automatic_fields(db, ladm_col_layer_name)
            field_mapping = self.refactor_fields.get_refactor_fields_mapping_resolve_domains(db.names, ladm_col_layer_name, self)
            self.activate_layer_requested.emit(input_layer)

            res = processing.run("model:ETL-model", {'INPUT': input_layer, 'mapping': field_mapping, 'output': output_layer})

            self.check_if_and_enable_automatic_fields(db, automatic_fields_definition, ladm_col_layer_name)
            finish_feature_count = output_layer.featureCount()

            return finish_feature_count > start_feature_count
        else:
            self.logger.info_msg(__name__, QCoreApplication.translate("QGISUtils",
                "Model ETL-model was not found and cannot be opened!"))
            return False

    @_activate_processing_plugin
    def show_etl_model(self, db, input_layer, ladm_col_layer_name, field_mapping=''):
        output = self.get_layer(db, ladm_col_layer_name, load=True)
        if not output:
            return False

        if output.isEditable():
            self.logger.warning_msg(__name__, QCoreApplication.translate("QGISUtils",
                "You need to close the edit session on layer '{}' before using this tool!").format(ladm_col_layer_name))
            return False

        model = QgsApplication.processingRegistry().algorithmById("model:ETL-model")
        if model:
            automatic_fields_definition = self.check_if_and_disable_automatic_fields(db, ladm_col_layer_name)

            # Get the mapping we'll use, it might come from stored recent mappings or from the default mapping
            mapping = None
            if field_mapping:
                mapping = self.load_field_mapping(field_mapping)

                if mapping is None: # If the mapping couldn't be parsed for any reason
                    self.logger.warning(__name__, "Field mapping '{}' was not found and couldn't be loaded. The default mapping is used instead!".format(field_mapping))

            if mapping is None:
                mapping = self.refactor_fields.get_refactor_fields_mapping(db.names, ladm_col_layer_name, self)

            self.activate_layer_requested.emit(input_layer)
            params = {
                'INPUT': input_layer.name(),
                'mapping': mapping,
                'output': output.name()
            }

            start_feature_count = output.featureCount()
            dlg = processing.createAlgorithmDialog("model:ETL-model", params)
            dlg.setModal(True)
            res = dlg.exec_()
            finish_feature_count = output.featureCount()

            self.check_if_and_enable_automatic_fields(db,
                                                      automatic_fields_definition,
                                                      ladm_col_layer_name)

            return finish_feature_count > start_feature_count
        else:
            self.logger.info_msg(__name__, QCoreApplication.translate("QGISUtils",
                "Model ETL-model was not found and cannot be opened!"))
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
        self.logger.info(__name__, "Field mapping saved: {}".format(name_field_mapping))

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

    def is_transitional_system_service_valid(self, url=None):
        res = False
        msg = {'text': '', 'level': Qgis.Warning}
        st_config = TransitionalSystemConfig()
        if url is None:
            url = st_config.get_domain()

        if url:
            with ProcessWithStatus("Checking Transitional System service availability (this might take a while)..."):
                if is_connected(TEST_SERVER):

                    nam = QNetworkAccessManager()
                    request = QNetworkRequest(QUrl(url))
                    reply = nam.get(request)

                    loop = QEventLoop()
                    reply.finished.connect(loop.quit)
                    loop.exec_()

                    allData = reply.readAll()
                    status = reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)
                    if status == 401:
                        try:
                            data = json.loads(str(allData, 'utf-8'))

                            if 'error' in data and data['error'] == st_config.ST_EXPECTED_RESPONSE:
                                res = True
                                msg['text'] = QCoreApplication.translate("SettingsDialog",
                                    "The tested service is valid to connect with Transitional System!")
                                msg['level'] = Qgis.Info
                            else:
                                res = False
                                msg['text'] = QCoreApplication.translate("SettingsDialog",
                                    "Response from the tested service is not as expected.")
                        except:
                            res = False
                            msg['text'] = QCoreApplication.translate("SettingsDialog",
                                "Response from the tested service is not as expected.")
                    else:
                        res = False
                        msg['text'] = QCoreApplication.translate("SettingsDialog",
                            "There was a problem connecting to the server. The server might be down or the service cannot be reached at the given URL.")
                else:
                    res = False
                    msg['text'] = QCoreApplication.translate("SettingsDialog",
                        "There was a problem connecting to Internet.")
        else:
            res = False
            msg['text'] = QCoreApplication.translate("SettingsDialog", "Not valid service URL to test!")

        return (res, msg)

    def is_source_service_valid(self, url=None):
        res = False
        msg = {'text': '', 'level': Qgis.Warning}
        if url is None:
            url = QSettings().value('Asistente-LADM_COL/sources/service_endpoint', DEFAULT_ENDPOINT_SOURCE_SERVICE)

        if url:
            with ProcessWithStatus("Checking source service availability (this might take a while)..."):
                if is_connected(TEST_SERVER):

                    nam = QNetworkAccessManager()
                    request = QNetworkRequest(QUrl(url))
                    reply = nam.get(request)

                    loop = QEventLoop()
                    reply.finished.connect(loop.quit)
                    loop.exec_()

                    allData = reply.readAll()
                    response = QTextStream(allData, QIODevice.ReadOnly)
                    status = reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)
                    if status == 200:
                        try:
                            data = json.loads(response.readAll())
                            if 'id' in data and data['id'] == SOURCE_SERVICE_EXPECTED_ID:
                                res = True
                                msg['text'] = QCoreApplication.translate("SettingsDialog",
                                    "The tested service is valid to upload files!")
                                msg['level'] = Qgis.Info
                            else:
                                res = False
                                msg['text'] = QCoreApplication.translate("SettingsDialog",
                                    "The tested upload service is not compatible: no valid 'id' found in response.")
                        except json.decoder.JSONDecodeError as e:
                            res = False
                            msg['text'] = QCoreApplication.translate("SettingsDialog",
                                "Response from the tested service is not compatible: not valid JSON found.")
                    else:
                        res = False
                        msg['text'] = QCoreApplication.translate("SettingsDialog",
                            "There was a problem connecting to the server. The server might be down or the service cannot be reached at the given URL.")
                else:
                    res = False
                    msg['text'] = QCoreApplication.translate("SettingsDialog",
                        "There was a problem connecting to Internet.")
        else:
            res = False
            msg['text'] = QCoreApplication.translate("SettingsDialog", "Not valid service URL to test!")

        return (res, msg)

    def upload_source_files(self, db):
        extfile_layer = self.get_layer(db, db.names.EXT_ARCHIVE_S, True)
        if not extfile_layer:
            return

        field_index = extfile_layer.fields().indexFromName(db.names.EXT_ARCHIVE_S_DATA_F)
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

    def enable_topological_editing(self, db):
        # Enable Topological Editing
        QgsProject.instance().setTopologicalEditing(True)

        dlg = LayersForTopologicalEditionDialog(db.names)
        if dlg.exec_() == QDialog.Accepted:
            # Load layers selected in the dialog

            layers = dlg.selected_layers_info
            self.get_layers(db, layers, load=True)
            if not layers:
                return None

            list_layers = list()
            # Open edit session in all layers
            for layer_name, layer in layers.items():
                layer.startEditing()
                list_layers.append(layer)

            # Activate "Vertex Tool (All Layers)"
            self.activate_layer_requested.emit(list_layers[0])
            self.action_vertex_tool_requested.emit()

            self.logger.info_msg(__name__, QCoreApplication.translate("QGISUtils",
                "You can start moving nodes in layers {} and {}, simultaneously!").format(
                    ", ".join(layer_name for layer_name in list(layers.keys())[:-1]), list(layers.keys())[-1]), 30)
