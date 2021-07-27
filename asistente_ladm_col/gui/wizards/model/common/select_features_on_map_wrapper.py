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
                               (C) 2021 by Yesid Polanía (BFS Swissphoto)
        email                : gcarrillo@linuxmail.org
                               sergio.ramirez@incige.com
                               leo.cardona.p@gmail.com
                               yesidpol.3@gmail.com
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
from qgis.PyQt.QtWidgets import QMessageBox

from asistente_ladm_col.gui.wizards.signal_disconnectable import SignalDisconnectable
from asistente_ladm_col.utils.select_map_tool import SelectMapTool


class SelectFeaturesOnMapWrapper(SignalDisconnectable):

    def __init__(self, iface, logger, multiple_features=True):
        self.__iface = iface
        self.__canvas = self.__iface.mapCanvas()
        self.__map_tool = self.__canvas.mapTool()
        self.__select_maptool = None

        self.__observer = None
        self.__logger = logger

        self.multiple_features = multiple_features

    def __map_tool_changed(self, new_tool, old_tool):
        self.__canvas.mapToolSet.disconnect(self.__map_tool_changed)

        # TODO parent was removed
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText(QCoreApplication.translate("WizardTranslations", "Do you really want to change the map tool?"))
        msg.setWindowTitle(QCoreApplication.translate("WizardTranslations", "CHANGING MAP TOOL?"))
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.button(QMessageBox.Yes).setText(QCoreApplication.translate("WizardTranslations", "Yes, and close the wizard"))
        msg.button(QMessageBox.No).setText(QCoreApplication.translate("WizardTranslations", "No, continue editing"))
        reply = msg.exec_()

        if reply == QMessageBox.No:
            self.__canvas.setMapTool(old_tool)
            self.__canvas.mapToolSet.connect(self.__map_tool_changed)
        else:
            self.__notify_map_tool_close()

    def select_features_on_map(self, layer):
        self.__iface.setActiveLayer(layer)

        # Enable Select Map Tool
        self.__select_maptool = SelectMapTool(self.__canvas, layer, self.multiple_features)
        self.__canvas.setMapTool(self.__select_maptool)

        # Connect signal that check if map tool change
        # This is necessary after select the maptool
        self.__canvas.mapToolSet.connect(self.__map_tool_changed)

        # Connect signal that check a feature was selected
        self.__select_maptool.features_selected_signal.connect(self.__features_selected)

    def init_map_tool(self):
        self.disconnect_signals()
        self.__canvas.setMapTool(self.__map_tool)

    def disconnect_signals(self):
        try:
            self.__canvas.mapToolSet.disconnect(self.__map_tool_changed)
        except:
            # TODO Specify exception type
            pass

    def __features_selected(self):
        self.__notify_features_selected()

        # Disconnect signal that check if map tool change
        # This is necessary before changing the tool to the user's previous selection
        self.__canvas.mapToolSet.disconnect(self.__map_tool_changed)
        self.__canvas.setMapTool(self.__map_tool)

        self.__logger.info(__name__, "Select maptool SIGNAL disconnected")
        self.__select_maptool.features_selected_signal.disconnect(self.__features_selected)

    def register_observer(self, observer):
        self.__observer = observer

    def __notify_map_tool_close(self):
        if self.__observer:
            self.__observer.map_tool_changed()

    def __notify_features_selected(self):
        if self.__observer:
            self.__observer.features_selected()