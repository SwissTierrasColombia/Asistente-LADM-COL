# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-09-10
        git sha              : :%H$
        copyright            : (C) 2017 by Germán Carrillo (BSF Swissphoto)
                               (C) 2018 by Sergio Ramírez (Incige SAS)
                               (C) 2019 by Leo Cardona (BSF Swissphoto)
        email                : gcarrillo@linuxmail.org
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

from asistente_ladm_col.config.general_config import LAYER
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.utils.select_map_tool import SelectMapTool


class SelectFeaturesOnMapWrapper:
    """
    Wrapper class that extends selecting features on the map.
    It is not possible to create an object of this class. This class should be implemented by a wizard.
    """

    def __init__(self):
        self.canvas = self.iface.mapCanvas()
        self.maptool = self.canvas.mapTool()
        self.select_maptool = None
        self.logger = Logger()

    def map_tool_changed(self, new_tool, old_tool):
        self.canvas.mapToolSet.disconnect(self.map_tool_changed)

        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Question)
        msg.setText(QCoreApplication.translate("WizardTranslations", "Do you really want to change the map tool?"))
        msg.setWindowTitle(QCoreApplication.translate("WizardTranslations", "CHANGING MAP TOOL?"))
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.button(QMessageBox.Yes).setText(QCoreApplication.translate("WizardTranslations", "Yes, and close the wizard"))
        msg.button(QMessageBox.No).setText(QCoreApplication.translate("WizardTranslations", "No, continue editing"))
        reply = msg.exec_()

        if reply == QMessageBox.No:
            self.canvas.setMapTool(old_tool)
            self.canvas.mapToolSet.connect(self.map_tool_changed)
        else:
            message = QCoreApplication.translate("WizardTranslations",
                                                 "'{}' tool has been closed because the map tool change.").format(self.WIZARD_TOOL_NAME)
            self.close_wizard(message)

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

        self.logger.info(__name__, "Select maptool SIGNAL disconnected")
        self.select_maptool.features_selected_signal.disconnect(self.features_selected)

    def init_map_tool(self):
        try:
            self.canvas.mapToolSet.disconnect(self.map_tool_changed)
        except:
            pass
        self.canvas.setMapTool(self.maptool)

    def connect_on_removing_layers(self):
        for layer_name in self._layers:
            if self._layers[layer_name][LAYER]:
                # Layer was found, listen to its removal so that we can update the variable properly
                try:
                    self._layers[layer_name][LAYER].willBeDeleted.disconnect(self.layer_removed)
                except:
                    pass
                self._layers[layer_name][LAYER].willBeDeleted.connect(self.layer_removed)

    def layer_removed(self):
        message = QCoreApplication.translate("WizardTranslations",
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

    def register_select_feature_on_map(self):
        raise NotImplementedError
