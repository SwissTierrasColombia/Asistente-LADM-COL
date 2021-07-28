# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-09-10
        git sha              : :%H$
        copyright            : (C) 2017 by Germán Carrillo (BFS Swissphoto)
                               (C) 2019 by Leo Cardona (BFS Swissphoto)
                               (C) 2021 by Yesid Polania (BFS Swissphoto)
        email                : gcarrillo@linuxmail.org
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
from enum import Enum

from qgis.core import Qgis
from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsVectorLayerUtils,
                       QgsGeometry)

from asistente_ladm_col import Logger
from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.config.enums import EnumRelatableLayers, EnumPlotCreationResult
from asistente_ladm_col.config.general_config import (WIZARD_EDITING_LAYER_NAME,
                                                      WIZARD_LAYERS,
                                                      WIZARD_READ_ONLY_FIELDS)
from asistente_ladm_col.gui.wizards.model.common.common_operations import CommonOperationsModel
from asistente_ladm_col.gui.wizards.model.common.refactor_fields_feature_creator import RefactorFieldsFeatureCreator
from asistente_ladm_col.gui.wizards.model.common.feature_selector_manager import FeatureSelectorManager
from asistente_ladm_col.gui.wizards.model.common.layer_remove_signals_manager import LayerRemovedSignalsManager


class PlotModel(FeatureSelectorManager):

    def __init__(self, iface, db, wiz_config):
        self.app = AppInterface()
        self._wizard_config = wiz_config
        self.names = db.names
        self._layers = self._wizard_config[WIZARD_LAYERS]

        self.iface = iface
        self._logger = Logger()

        self._editing_layer_name = self._wizard_config[WIZARD_EDITING_LAYER_NAME]
        self._editing_layer = self._wizard_config[WIZARD_LAYERS][self._editing_layer_name]

        self.__feature_creator_from_refactor = RefactorFieldsFeatureCreator(self.app, db)

        self.__relatable_layers = dict()
        self.__init_selectable_layer_by_type()

        # parent constructor
        FeatureSelectorManager.__init__(self, self.__relatable_layers, self.iface, self._logger)
        self.type_of_selected_layer_to_associate = EnumRelatableLayers.BOUNDARY

        self.__layer_remove_manager = LayerRemovedSignalsManager(self._layers, self)

        self.__common_operations = \
            CommonOperationsModel(self._wizard_config[WIZARD_LAYERS], self._editing_layer_name, self.app,
                                  self._wizard_config[WIZARD_READ_ONLY_FIELDS])

        self.refactor_field_mapping = self.__common_operations.get_field_mappings_file_names()

    def __init_selectable_layer_by_type(self):
        self.__relatable_layers[EnumRelatableLayers.BOUNDARY] = self._layers[self.names.LC_BOUNDARY_T]

    def select_all_features(self):
        layer = self.__relatable_layers[EnumRelatableLayers.BOUNDARY]
        layer.selectAll()

    def create_feature_from_refactor(self, selected_layer, field_mapping):
        self.__feature_creator_from_refactor.create(selected_layer, self._editing_layer_name, field_mapping)

    def set_ready_only_fields(self, read_only):
        self.__common_operations.set_ready_only_field(read_only)

    def edit_feature(self) -> EnumPlotCreationResult:
        if self._layers[self.names.LC_BOUNDARY_T].selectedFeatureCount() == 0:
            return EnumPlotCreationResult.NO_BOUNDARIES_SELECTED

        self.iface.layerTreeView().setCurrentLayer(self._editing_layer)
        self.app.core.active_snapping_all_layers()

        return self.create_plots_from_boundaries()
        # else:
        #   self._logger.warning_msg(__name__, QCoreApplication.translate("WizardTranslations", "First select boundaries!"))

    def create_plots_from_boundaries(self):
        selected_boundaries = self._layers[self.names.LC_BOUNDARY_T].selectedFeatures()

        boundary_geometries = [f.geometry() for f in selected_boundaries]
        collection = QgsGeometry().polygonize(boundary_geometries)
        features = list()
        for polygon in collection.asGeometryCollection():
            feature = QgsVectorLayerUtils().createFeature(self._editing_layer, polygon)
            features.append(feature)

        if not features:
            return EnumPlotCreationResult.NO_PLOTS_CREATED

        if not self._editing_layer.isEditable():
            self._editing_layer.startEditing()

        self._editing_layer.addFeatures(features)
        self.iface.mapCanvas().refresh()

        message = QCoreApplication.translate("WizardTranslations", "{} new plot(s) has(have) been created! To finish the creation of the plots, open its attribute table and fill in the mandatory fields.").format(len(features))
        button_text = QCoreApplication.translate("WizardTranslations", "Open table of attributes")
        level = Qgis.Info
        layer = self._editing_layer
        filter = '"{}" is Null'.format(self.names.LC_PLOT_T_PLOT_AREA_F)
        self._logger.message_with_button_open_table_attributes_emitted.emit(message, button_text, level, layer, filter)
        # self.close_wizard(show_message=False)
        return EnumPlotCreationResult.CREATED

    def dispose(self):
        self.__layer_remove_manager.disconnect_signals()
        self.__common_operations.rollback_in_layers_with_empty_editing_buffer()
        self.__common_operations.set_ready_only_field(False)
        super().dispose()

    # features selectors
    def select_features_on_map(self):
        # TODO is this execution right?
        self.__layer_remove_manager.reconnect_signals()
        super().select_features_on_map()
