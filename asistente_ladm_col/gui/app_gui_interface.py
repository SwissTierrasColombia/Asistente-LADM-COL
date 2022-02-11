"""
/***************************************************************************
                              Asistente LADM-COL
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
                              pyqtSlot,
                              pyqtSignal,
                              QCoreApplication)
from qgis.PyQt.QtGui import QColor
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

    def trigger_repaint_on_layer(self, layer):
        layer.triggerRepaint()

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

    def clear_status_bar(self):
        self.iface.statusBarIface().clearMessage()

    def add_indicators(self, node_name, node_type, payload, names):
        """
        Adds all indicators for a node in layer tree. It searches for the proper node and its config.

        :param node_name: Key to get the config and possibly, the node (see payload)
        :param node_type: QgsLayerTreeNode.NodeType
        :param payload: If the node is a LADM layer, we need the layer object, as the name is not enough to disambiguate
                        between layers from different connections
        :param names: DBMappingRegistry instance to read layer names from
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
        indicators_config = LayerTreeIndicatorConfig().get_indicators_config(node_name, node_type, names)
        if not indicators_config:
            self.logger.warning(__name__, "Configuration for indicators not found for node '{}'!".format(node_name))

        # And finally...
        for config in indicators_config:
            self.logger.debug(__name__, "Adding indicator for {} node '{}'...".format(
                'group' if node_type == QgsLayerTreeNode.NodeGroup else 'layer', node_name))
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

    def set_layer_visibility(self, layer, visible):
        node = QgsProject.instance().layerTreeRoot().findLayer(layer.id())
        self.set_node_visibility(node, visible)

    @pyqtSlot()
    def clear_message_bar(self):
        self.iface.messageBar().clearWidgets()

    def zoom_full(self):
        self.iface.zoomFull()

    def zoom_to_active_layer(self):
        self.iface.zoomToActiveLayer()

    def zoom_to_selected(self):
        self.iface.actionZoomToSelected().trigger()

    def zoom_to_feature_ids(self, layer, fids):
        self.iface.mapCanvas().zoomToFeatureIds(layer, fids)

    def zoom_to_extent(self, extent):
        self.iface.mapCanvas().zoomToFeatureExtent(extent)

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
        self.iface.addTabifiedDockWidget(area, dock_widget, raiseTab=True)

    def open_feature_form(self, layer, feature):
        self.iface.openFeatureForm(layer, feature)

    def flash_features(self, layer, fids, flashes=1, duration=500):
        self.iface.mapCanvas().flashFeatureIds(layer,
                                               fids,
                                               QColor(255, 0, 0, 255),
                                               QColor(255, 0, 0, 0),
                                               flashes=flashes,
                                               duration=duration)
