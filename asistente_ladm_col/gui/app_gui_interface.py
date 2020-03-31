# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2020-03-30
        git sha              : :%H$
        copyright            : (C) 2020 by Germán Carrillo (BSF Swissphoto)
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
from qgis.PyQt.QtCore import (QObject,
                              pyqtSignal,
                              pyqtSlot)
from qgis.PyQt.QtWidgets import QProgressBar
from qgis.core import (Qgis,
                       QgsLayerTreeGroup,
                       QgsLayerTreeNode,
                       QgsMapLayer,
                       QgsProject)

from asistente_ladm_col.config.general_config import PLUGIN_NAME
from asistente_ladm_col.config.translation_strings import (TranslatableConfigStrings,
                                                           ERROR_LAYER_GROUP)
from asistente_ladm_col.lib.logger import Logger


class AppGUIInterface(QObject):
    def __init__(self, iface):
        QObject.__init__(self)
        self.iface = iface

        self.logger = Logger()

        self.translatable_config_strings = TranslatableConfigStrings()

    def trigger_add_feature(self):
        self.iface.actionAddFeature().trigger()

    def trigger_vertex_tool(self):
        self.iface.actionVertexTool().trigger()

    def create_progress_message_bar(self, text, progress):
        progressMessageBar = self.iface.messageBar().createMessage(PLUGIN_NAME, text)
        progressMessageBar.layout().addWidget(progress)
        self.iface.messageBar().pushWidget(progressMessageBar, Qgis.Info)

    def refresh_layer_symbology(self, layer_id):
        self.iface.layerTreeView().refreshLayerSymbology(layer_id)

    def refresh_map(self):
        self.iface.mapCanvas().refresh()

    def freeze_map(self, frozen):
        self.iface.mapCanvas().freeze(frozen)

    def activate_layer(self, layer):
        self.iface.layerTreeView().setCurrentLayer(layer)

    def set_node_visibility(self, node, visible=True):
        # Modes may eventually be layer_id, group_name, layer, group
        if node is not None:
            node.setItemVisibilityChecked(visible)

    def remove_error_group(self):
        group = self.get_error_layers_group()
        parent = group.parent()
        parent.removeChildNode(group)

    def clear_status_bar(self):
        self.iface.statusBarIface().clearMessage()

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
        elif not self.iface.layerTreeView().layerTreeModel().node2index(group).row() == 0 or type(group.parent()) is QgsLayerTreeGroup:
            group_clone = group.clone()
            root.insertChildNode(0, group_clone)
            parent = group.parent()
            parent.removeChildNode(group)
            group = group_clone
        return group

    def set_error_group_visibility(self, visible):
        self.set_node_visibility(self.get_error_layers_group(), visible)

    def set_layer_visibility(self, layer, visible):
        node = QgsProject.instance().layerTreeRoot().findLayer(layer.id())
        self.set_node_visibility(node, visible)

    def error_group_exists(self):
        root = QgsProject.instance().layerTreeRoot()
        translated_strings = self.translatable_config_strings.get_translatable_config_strings()
        return root.findGroup(translated_strings[ERROR_LAYER_GROUP]) is not None

    @pyqtSlot()
    def clear_message_bar(self):
        self.iface.messageBar().clearWidgets()

    def zoom_full(self):
        self.iface.zoom_full()

    def zoom_to_selected(self):
        self.iface.actionZoomToSelected().trigger()

