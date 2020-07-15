# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2020-03-30
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
                              QCoreApplication)
from qgis.PyQt.QtWidgets import QDialog

from qgis.core import (QgsLayerTreeNode,
                       QgsProject)

from asistente_ladm_col import Logger
from asistente_ladm_col.config.enums import EnumLayerRegistryType
from asistente_ladm_col.core.app_settings import AppSettings
from asistente_ladm_col.gui.dialogs.dlg_topological_edition import LayersForTopologicalEditionDialog
from asistente_ladm_col.utils.singleton import SingletonQObject


class AppInterface(QObject, metaclass=SingletonQObject):
    def __init__(self):
        QObject.__init__(self)
        self.logger = Logger()
        self.settings = AppSettings()
        self.core = None
        self.gui = None

    def set_core_interface(self, core):
        self.core = core
        self.set_connections()

    def set_gui_interface(self, gui):
        self.gui = gui
        self.set_connections()

    def set_connections(self):
        if self.core and self.gui:
            self.core.action_add_feature_requested.connect(self.gui.trigger_add_feature)
            self.core.action_vertex_tool_requested.connect(self.gui.trigger_vertex_tool)
            self.core.activate_layer_requested.connect(self.gui.activate_layer)
            self.core.map_refresh_requested.connect(self.gui.refresh_map)
            self.core.redraw_all_layers_requested.connect(self.gui.redraw_all_layers)
            self.core.map_freeze_requested.connect(self.gui.freeze_map)
            self.core.zoom_full_requested.connect(self.gui.zoom_full)
            self.core.zoom_to_active_layer_requested.connect(self.gui.zoom_to_active_layer)
            self.core.zoom_to_selected_requested.connect(self.gui.zoom_to_selected)
            self.core.set_node_visibility_requested.connect(self.gui.set_node_visibility)

    def add_indicators(self, db, node_name, node_type):
        """We need to deal with LADM layers in a different way, hence we need a payload to add more info in that case"""
        payload = self._get_node_payload(db, node_name, node_type)
        self.gui.add_indicators(node_name, node_type, payload)

    def _get_node_payload(self, db, node_name, node_type):
        # If the layers is LADM, we need the layer object
        payload = None
        if node_type == QgsLayerTreeNode.NodeLayer:
            ladm_layers = self.core.get_ladm_layers_from_qgis(db, EnumLayerRegistryType.IN_LAYER_TREE)
            if node_name in ladm_layers:
                # We cannot find ladm layers by name (they could be duplicated
                # from other db connections), so, return the layer object
                payload = ladm_layers[node_name]

        return payload

    def enable_topological_editing(self, db):
        # Enable Topological Editing
        QgsProject.instance().setTopologicalEditing(True)

        dlg = LayersForTopologicalEditionDialog(db.names, self.gui.iface.mainWindow())
        if dlg.exec_() == QDialog.Accepted:
            # Load layers selected in the dialog
            layers = dlg.selected_layers_info
            self.core.get_layers(db, layers, load=True)
            if not layers:
                return None

            list_layers = list()
            # Open edit session in all layers
            for layer_name, layer in layers.items():
                layer.startEditing()
                list_layers.append(layer)

            # Activate "Vertex Tool (All Layers)"
            self.gui.activate_layer(list_layers[0])
            self.gui.trigger_vertex_tool()

            self.logger.info_msg(__name__, QCoreApplication.translate("AppCoreInterface",
                "You can start moving nodes in layers {} and {}, simultaneously!").format(
                    ", ".join(layer_name for layer_name in list(layers.keys())[:-1]), list(layers.keys())[-1]), 30)
