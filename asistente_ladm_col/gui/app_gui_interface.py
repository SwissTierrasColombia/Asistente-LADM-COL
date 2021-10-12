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
import os.path

from qgis.PyQt.QtCore import (QObject,
                              pyqtSlot,
                              pyqtSignal,
                              QCoreApplication,
                              QSettings)
from qgis.PyQt.QtWidgets import (QFileDialog,
                                 QDockWidget)

from qgis.core import (Qgis,
                       QgsLayerTreeGroup,
                       QgsProject,
                       QgsLayerTreeNode,
                       QgsProcessingException,
                       QgsCategorizedSymbolRenderer)
from qgis.gui import QgsLayerTreeViewIndicator
import processing

from asistente_ladm_col.config.general_config import PLUGIN_NAME
from asistente_ladm_col.config.layer_tree_indicator_config import (INDICATOR_TOOLTIP,
                                                                   INDICATOR_ICON,
                                                                   INDICATOR_SLOT,
                                                                   LayerTreeIndicatorConfig)
from asistente_ladm_col.config.translation_strings import (TranslatableConfigStrings,
                                                           ERROR_LAYER_GROUP)
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.lib.processing.custom_processing_feedback import CustomFeedbackWithErrors
from asistente_ladm_col.utils.qgis_model_baker_utils import QgisModelBakerUtils
from asistente_ladm_col.utils.qt_utils import ProcessWithStatus
from asistente_ladm_col.utils.symbology import SymbologyUtils


class AppGUIInterface(QObject):
    add_indicators_requested = pyqtSignal(str, QgsLayerTreeNode.NodeType)  # node name, node type

    def __init__(self, iface):
        QObject.__init__(self)
        self.iface = iface

        self.logger = Logger()

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

    def redraw_all_layers(self):
        self.iface.mapCanvas().redrawAllLayers()

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

    def add_error_layer(self, db, error_layer):
        group = self.get_error_layers_group()

        # Check if layer is loaded and remove it
        layers = group.findLayers()
        for layer in layers:
            if layer.name() == error_layer.name():
                group.removeLayer(layer.layer())
                break

        added_layer = QgsProject.instance().addMapLayer(error_layer, False)
        index = QgisModelBakerUtils().get_suggested_index_for_layer(added_layer, group)
        added_layer = group.insertLayer(index, added_layer).layer()
        if added_layer.isSpatial():
            # db connection is none because we are using a memory layer
            SymbologyUtils().set_layer_style_from_qml(db, added_layer, is_error_layer=True)

            if isinstance(added_layer.renderer(), QgsCategorizedSymbolRenderer):
                # Remove empty style categories as they just make difficult to understand validation errors
                unique_values = added_layer.uniqueValues(added_layer.fields().indexOf(QCoreApplication.translate("QualityRule", "codigo_error")))
                renderer = added_layer.renderer()
                for cat in reversed(renderer.categories()):  # To be safe while removing categories
                    if cat.value() not in unique_values:
                        renderer.deleteCategory(renderer.categoryIndexForValue(cat.value()))

                added_layer.setRenderer(added_layer.renderer().clone())

        return added_layer

    def get_error_layers_group(self):
        """
        Get the topology errors group. If it exists but is placed in another
        position rather than the top, it moves the group to the top.
        """
        root = QgsProject.instance().layerTreeRoot()
        translated_strings = TranslatableConfigStrings.get_translatable_config_strings()
        group = root.findGroup(translated_strings[ERROR_LAYER_GROUP])
        if group is None:
            group = root.insertGroup(0, translated_strings[ERROR_LAYER_GROUP])
            self.add_indicators_requested.emit(translated_strings[ERROR_LAYER_GROUP], QgsLayerTreeNode.NodeGroup)
        elif not self.iface.layerTreeView().layerTreeModel().node2index(group).row() == 0 or type(group.parent()) is QgsLayerTreeGroup:
            group_clone = group.clone()
            root.insertChildNode(0, group_clone)
            parent = group.parent()
            parent.removeChildNode(group)
            group = group_clone
        return group

    def add_indicators(self, node_name, node_type, payload):
        """
        Adds all indicators for a node in layer tree. It searches for the proper node and its config.

        :param node_name: Key to get the config and possibly, the node (see payload)
        :param node_type: QgsLayerTreeNode.NodeType
        :param payload: If the node is a LADM layer, we need the layer object, as the name is not enough to disambiguate
                        between layers from different connections
        """
        # First get the node
        node = None
        root = QgsProject.instance().layerTreeRoot()
        if node_type == QgsLayerTreeNode.NodeGroup:
            node = root.findGroup(node_name)
        elif node_type == QgsLayerTreeNode.NodeLayer:
            if payload:
                node = root.findLayer(payload)  # Search by QgsMapLayer
            else:  # Get the first layer matching the node name
                layers = QgsProject.instance().mapLayersByName(node_name)
                if layers:
                    node = root.findLayer(layers[0])

        if not node:
            self.logger.warning(__name__, "Node not found for adding indicators! ({}, {})".format(node_name, node_type))
            return  # No node, no party

        # Then, get the config
        indicators_config = LayerTreeIndicatorConfig().get_indicators_config(node_name, node_type)
        if not indicators_config:
            self.logger.warning(__name__, "Configuration for indicators not found for node '{}'!".format(node_name))

        # And finally...
        for config in indicators_config:
            self.add_indicator(node, config)

    def add_indicator(self, node, config):
        """
        Adds a single indicator for the node, based on a config dict

        :param node: Layer tree node
        :param config: Dictionary with required data to set the indicator
        """
        indicator = QgsLayerTreeViewIndicator(self.iface.layerTreeView())
        indicator.setToolTip(config[INDICATOR_TOOLTIP])
        indicator.setIcon(config[INDICATOR_ICON])
        indicator.clicked.connect(config[INDICATOR_SLOT])
        self.iface.layerTreeView().addIndicator(node, indicator)

    def export_error_group(self):
        """Exports the error group to GeoPackage"""
        group = self.get_error_layers_group()
        if group:
            layers = group.findLayerIds()
            if not layers:
                self.logger.warning_msg(__name__, QCoreApplication.translate("AppGUIInterface",
                                                                             "There are no error layers to export!"))
                return

            settings = QSettings()
            settings_path = "Asistente-LADM-COL/quality_rules/save_path"
            filename, matched_filter = QFileDialog.getSaveFileName(self.iface.mainWindow(),
                                           QCoreApplication.translate("AppGUIInterface", "Where do you want to save your GeoPackage?"),
                                           settings.value(settings_path, '.'),
                                           QCoreApplication.translate("AppGUIInterface", "GeoPackage (*.gpkg)"))

            if filename:
                settings.setValue(settings_path, os.path.dirname(filename))
                if not filename.endswith(".gpkg") and filename:
                    filename = filename + ".gpkg"

                feedback = CustomFeedbackWithErrors()
                try:
                    msg = QCoreApplication.translate("AppGUIInterface", "Exporting quality errors to GeoPackage...")
                    with ProcessWithStatus(msg):
                        processing.run("native:package", {
                            'LAYERS': layers,
                            'OUTPUT': filename,
                            'OVERWRITE': False,
                            'SAVE_STYLES': True},
                                       feedback=feedback)
                except QgsProcessingException as e:
                    self.logger.warning_msg(__name__, QCoreApplication.translate("AppGUIInterface",
                                                                                 "The quality errors could not be exported. Details: {}".format(feedback.msg)))
                    return

                self.logger.success_msg(__name__, QCoreApplication.translate("AppGUIInterface",
                                    "The quality errors have been exported to GeoPackage!"))
            else:
                self.logger.warning_msg(__name__, QCoreApplication.translate("AppGUIInterface",
                                             "Export to GeoPackage was cancelled. No output file was selected."), 5)
        else:
            self.logger.warning_msg(__name__, QCoreApplication.translate("AppGUIInterface",
                                             "There is no quality error group to export!"), 5)

    def set_error_group_visibility(self, visible):
        self.set_node_visibility(self.get_error_layers_group(), visible)

    def set_layer_visibility(self, layer, visible):
        node = QgsProject.instance().layerTreeRoot().findLayer(layer.id())
        self.set_node_visibility(node, visible)

    def error_group_exists(self):
        root = QgsProject.instance().layerTreeRoot()
        translated_strings = TranslatableConfigStrings.get_translatable_config_strings()
        return root.findGroup(translated_strings[ERROR_LAYER_GROUP]) is not None

    @pyqtSlot()
    def clear_message_bar(self):
        self.iface.messageBar().clearWidgets()

    def zoom_full(self):
        self.iface.zoomFull()

    def zoom_to_active_layer(self):
        self.iface.zoomToActiveLayer()

    def zoom_to_selected(self):
        self.iface.actionZoomToSelected().trigger()

    def show_message(self, msg, level, duration=5):
        self.clear_message_bar()  # Remove previous messages before showing a new one
        self.iface.messageBar().pushMessage("Asistente LADM-COL", msg, level, duration)

    def show_status_bar_message(self, msg, duration):
        self.iface.statusBarIface().showMessage(msg, duration)

    def add_tabified_dock_widget(self, area, dock_widget):
        """
        Adds the dock_widget to the given area, making sure it is tabified if other dock widgets exist.
        :param area: Value of the Qt.DockWidgetArea enum
        :param dock_widget: QDockWidget object
        """
        if Qgis.QGIS_VERSION_INT >= 31300:  # Use native addTabifiedDockWidget
            self.iface.addTabifiedDockWidget(area, dock_widget, raiseTab=True)
        else:  # Use plugin's addTabifiedDockWidget, which does not raise the new tab
            dock_widgets = list()
            for dw in self.iface.mainWindow().findChildren(QDockWidget):
                if dw.isVisible() and self.iface.mainWindow().dockWidgetArea(dw) == area:
                    dock_widgets.append(dw)

            self.iface.mainWindow().addDockWidget(area, dock_widget)  # We add the dock widget, then attempt to tabify
            if dock_widgets:
                self.logger.debug(__name__, "Tabifying dock widget {}...".format(dock_widget.windowTitle()))
                self.iface.mainWindow().tabifyDockWidget(dock_widgets[0], dock_widget)  # No way to prefer one Dock Widget