# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2021-05-21
        git sha              : :%H$
        copyright            : (C) 2021 by Yesid Polanía (BFS Swissphoto)
        email                : yesidpol.3@gmail.com
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
                             pyqtSignal)

from asistente_ladm_col.gui.wizards.model.common.abstract_qobject_meta import AbstractQObjectMeta
from asistente_ladm_col.gui.wizards.model.common.select_features_by_expression_dialog_wrapper import \
    SelectFeatureByExpressionDialogWrapper
from asistente_ladm_col.gui.wizards.model.common.select_features_on_map_wrapper import SelectFeaturesOnMapWrapper


class FeatureSelectorManager(QObject, metaclass=AbstractQObjectMeta):
    features_selected = pyqtSignal()
    map_tool_changed = pyqtSignal()
    feature_selection_by_expression_changed = pyqtSignal()

    def __init__(self, relatable_layers, iface, logger):
        QObject.__init__(self)
        self.__iface = iface
        self._logger = logger
        self.__features_on_map_observer_list = list()
        self.__feature_selector_by_expression_observers = list()

        self.__feature_selector_on_map = SelectFeaturesOnMapWrapper(self.__iface, self._logger)
        self.__feature_selector_on_map.features_selected.connect(self.features_selected)
        self.__feature_selector_on_map.map_tool_changed.connect(self.map_tool_changed)

        self.__feature_selector_by_expression = SelectFeatureByExpressionDialogWrapper(self.__iface)
        self.__feature_selector_by_expression.feature_selection_by_expression_changed.connect(
            self.feature_selection_by_expression_changed)

        self.__relatable_layers = relatable_layers

        self.type_of_selected_layer_to_associate = None

    def select_features_on_map(self):
        # TODO Exception if layer does not exist
        layer = self.__relatable_layers[self.type_of_selected_layer_to_associate]
        self.__feature_selector_on_map.select_features_on_map(layer)

    def select_features_by_expression(self):
        # TODO Check if layer exists in self._layers
        layer = self.__relatable_layers[self.type_of_selected_layer_to_associate]
        self.__feature_selector_by_expression.select_features_by_expression(layer)

    def dispose(self):
        self.__feature_selector_on_map.init_map_tool()
        self.__feature_selector_on_map.disconnect_signals()

    def get_number_of_selected_features(self):
        feature_count = dict()

        for layer in self.__relatable_layers:
            feature_count[layer] = self.__relatable_layers[layer].selectedFeatureCount()

        return feature_count
