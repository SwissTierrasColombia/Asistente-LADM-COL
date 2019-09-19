# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-09-10
        git sha              : :%H$
        copyright            : (C) 2017 by Germán Carrillo
                               (C) 2018 by Sergio Ramírez (Incige SAS)
                               (C) 2019 by Leo Cardona
        email                : gcarrillo@linuxmail.com
                               sergio.ramirez@incige.com
                               leo.cardona.p@gmail.com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
 """
from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtWidgets import (QMessageBox,
                                 QPushButton)
from qgis.core import Qgis

from ...config.general_config import (PLUGIN_NAME,
                                      LAYER)
from ...utils.select_map_tool import SelectMapTool


class SelectFeaturesOnMapWizard:
    SELECTION_ON_MAP = True

    def __init__(self):
        self.canvas = self.iface.mapCanvas()
        self.maptool = self.canvas.mapTool()
        self.select_maptool = None

    def map_tool_changed(self, new_tool, old_tool):
        self.canvas.mapToolSet.disconnect(self.map_tool_changed)
        reply = QMessageBox.question(self,
                                     QCoreApplication.translate(self.WIZARD_NAME, "Stop {} creation?").format(self.WIZARD_FEATURE_NAME),
                                     QCoreApplication.translate(self.WIZARD_NAME, "The map tool is about to change. Do you want to stop creating {}?").format(self.WIZARD_FEATURE_NAME),
                                     QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            message = QCoreApplication.translate(self.WIZARD_NAME,
                                                 "'{}' tool has been closed because the map tool change.").format(self.WIZARD_TOOL_NAME)
            self.close_wizard(message)
        else:
            self.canvas.setMapTool(old_tool)
            self.canvas.mapToolSet.connect(self.map_tool_changed)

    def select_features_on_map(self, layer):
        self.iface.setActiveLayer(layer)
        self.setVisible(False)  # Make wizard disappear

        # Enable Select Map Tool
        self.select_maptool = SelectMapTool(self.canvas, layer, multi=True)

        self.canvas.setMapTool(self.select_maptool)
        # Connect signal that check if map tool change
        # This is necessary after select the maptool
        self.canvas.mapToolSet.connect(self.map_tool_changed)

        # Connect signal that check a feature was selected
        self.select_maptool.features_selected_signal.connect(self.features_selected)

    def features_selected(self):
        self.setVisible(True)  # Make wizard appear
        self.check_selected_features()

        # Disconnect signal that check if map tool change
        # This is necessary before changing the tool to the user's previous selection
        self.canvas.mapToolSet.disconnect(self.map_tool_changed)
        self.canvas.setMapTool(self.maptool)

        self.log.logMessage("Select maptool SIGNAL disconnected", PLUGIN_NAME, Qgis.Info)
        self.select_maptool.features_selected_signal.disconnect(self.features_selected)

    def init_map_tool(self):
        try:
            self.canvas.mapToolSet.disconnect(self.map_tool_changed)
        except:
            pass
        self.canvas.setMapTool(self.maptool)

    def validate_remove_layers(self):
        for layer_name in self._layers:
            if self._layers[layer_name][LAYER]:
                # Layer was found, listen to its removal so that we can update the variable properly
                try:
                    self._layers[layer_name][LAYER].willBeDeleted.disconnect(self.layer_removed)
                except:
                    pass
                self._layers[layer_name][LAYER].willBeDeleted.connect(self.layer_removed)

    def layer_removed(self):
        message = QCoreApplication.translate(self.WIZARD_NAME,
                                             "'{}' tool has been closed because you just removed a required layer.").format(self.WIZARD_TOOL_NAME)
        self.close_wizard(message)

    def disconnect_signals_select_features_on_map(self):

        self.disconnect_signals_controls_select_features_on_map()

        try:
            self.canvas.mapToolSet.disconnect(self.map_tool_changed)
        except:
            pass

        for layer_name in self._layers:
            try:
                self._layers[layer_name][LAYER].willBeDeleted.disconnect(self.layer_removed)
            except:
                pass

    def disconnect_signals_controls_select_features_on_map(self):
        raise NotImplementedError

    def save_created_geometry(self):
        message = None
        if self._layers[self.EDITING_LAYER_NAME][LAYER].editBuffer():
            if len(self._layers[self.EDITING_LAYER_NAME][LAYER].editBuffer().addedFeatures()) == 1:
                feature = [value for index, value in self._layers[self.EDITING_LAYER_NAME][LAYER].editBuffer().addedFeatures().items()][0]
                if feature.geometry().isGeosValid():
                    self.exec_form(self._layers[self.EDITING_LAYER_NAME][LAYER])
                else:
                    message = QCoreApplication.translate(self.WIZARD_NAME, "The geometry is invalid. Do you want to return to the edit session?")
            else:
                if len(self._layers[self.EDITING_LAYER_NAME][LAYER].editBuffer().addedFeatures()) == 0:
                    message = QCoreApplication.translate(self.WIZARD_NAME, "No geometry has been created. Do you want to return to the edit session?")
                else:
                    message = QCoreApplication.translate(self.WIZARD_NAME, "Several geometries were created but only one was expected. Do you want to return to the edit session?")

        if message:
            self.show_message_associate_geometry_creation(message)

    def show_message_associate_geometry_creation(self, message):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Question)
        msg.setText(message)
        msg.setWindowTitle(QCoreApplication.translate(self.WIZARD_NAME, "Continue editing?"))
        msg.addButton(QPushButton(QCoreApplication.translate(self.WIZARD_NAME, "Yes")), QMessageBox.YesRole)
        msg.addButton(QPushButton(QCoreApplication.translate(self.WIZARD_NAME, "No, close the wizard")), QMessageBox.NoRole)
        reply = msg.exec_()

        if reply == 1: # 1 close wizard, 0 yes
            # stop edition in close_wizard crash qgis
            if self._layers[self.EDITING_LAYER_NAME][LAYER].isEditable():
                self._layers[self.EDITING_LAYER_NAME][LAYER].rollBack()

            message = QCoreApplication.translate(self.WIZARD_NAME, "'{}' tool has been closed.").format(
                self.WIZARD_TOOL_NAME)
            self.close_wizard(message)
        else:
            # Continue creating geometry
            pass
