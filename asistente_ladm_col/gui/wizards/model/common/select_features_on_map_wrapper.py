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
from qgis.PyQt.QtCore import (QCoreApplication,
                              QObject,
                             pyqtSignal)

from asistente_ladm_col.gui.wizards.model.common.args.model_args import MapToolChangedArgs
from asistente_ladm_col.utils.select_map_tool import SelectMapTool


class NullFeatureSelectorOnMap(QObject):
    features_selected = pyqtSignal()
    map_tool_changed = pyqtSignal()

    def __init__(self):
        QObject.__init__(self)
        self.multiple_features = True

    def select_features_on_map(self, layer):
        pass

    def disconnect_signals(self):
        pass

    def init_map_tool(self):
        pass


class SelectFeaturesOnMapWrapper(QObject):
    features_selected = pyqtSignal()
    map_tool_changed = pyqtSignal(MapToolChangedArgs)

    def __init__(self, iface, logger, multiple_features=True):
        QObject.__init__(self)
        self.__iface = iface
        self.__canvas = self.__iface.mapCanvas()
        self.__map_tool = self.__canvas.mapTool()
        self.__select_maptool = None

        self.__logger = logger

        self.multiple_features = multiple_features

    def __map_tool_changed(self, new_tool, old_tool):
        self.__canvas.mapToolSet.disconnect(self.__map_tool_changed)

        args = MapToolChangedArgs()

        self.map_tool_changed.emit(args)

        if not args.change_map_tool:
            self.__canvas.setMapTool(old_tool)
            self.__canvas.mapToolSet.connect(self.__map_tool_changed)

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
        self.features_selected.emit()

        # Disconnect signal that check if map tool change
        # This is necessary before changing the tool to the user's previous selection
        self.__canvas.mapToolSet.disconnect(self.__map_tool_changed)
        self.__canvas.setMapTool(self.__map_tool)

        self.__logger.info(__name__, "Select maptool SIGNAL disconnected")
        self.__select_maptool.features_selected_signal.disconnect(self.__features_selected)
