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
from qgis.core import Qgis
from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsVectorLayerUtils,
                       QgsGeometry)

from asistente_ladm_col.config.enums import (EnumRelatableLayers,
                                             EnumPlotCreationResult)


class PlotCreatorManager:

    def __init__(self, db, layers, editing_layer, iface, app, logger):
        self.__db = db
        self.__layers = layers

        self.__editing_layer = editing_layer

        self.__iface = iface
        self.__app = app

        # TODO Logger can be moved
        self.__logger = logger

        self.names = db.names

        self.__relatable_layers = dict()
        self.__init_selectable_layer_by_type()

    def __init_selectable_layer_by_type(self):
        self.__relatable_layers[EnumRelatableLayers.BOUNDARY] = self.__layers[self.names.LC_BOUNDARY_T]

    def get_layer_by_type(self, layer_type: EnumRelatableLayers):
        return self.__relatable_layers[layer_type] if layer_type in self.__relatable_layers else None

    def select_all_features(self):
        layer = self.__relatable_layers[EnumRelatableLayers.BOUNDARY]
        layer.selectAll()

    def edit_feature(self) -> EnumPlotCreationResult:
        if self.__layers[self.names.LC_BOUNDARY_T].selectedFeatureCount() == 0:
            return EnumPlotCreationResult.NO_BOUNDARIES_SELECTED

        self.__iface.layerTreeView().setCurrentLayer(self.__editing_layer)
        self.__app.core.active_snapping_all_layers()

        return self.create_plots_from_boundaries()
        # else:
        #   self._logger.warning_msg(__name__, QCoreApplication.translate("WizardTranslations", "First select boundaries!"))

    def create_plots_from_boundaries(self):
        selected_boundaries = self.__layers[self.names.LC_BOUNDARY_T].selectedFeatures()

        boundary_geometries = [f.geometry() for f in selected_boundaries]
        collection = QgsGeometry().polygonize(boundary_geometries)
        features = list()
        for polygon in collection.asGeometryCollection():
            feature = QgsVectorLayerUtils().createFeature(self.__editing_layer, polygon)
            features.append(feature)

        if not features:
            return EnumPlotCreationResult.NO_PLOTS_CREATED

        if not self.__editing_layer.isEditable():
            self.__editing_layer.startEditing()

        self.__editing_layer.addFeatures(features)
        self.__iface.mapCanvas().refresh()

        message = QCoreApplication.translate("WizardTranslations", "{} new plot(s) has(have) been created! To finish the creation of the plots, open its attribute table and fill in the mandatory fields.").format(len(features))
        button_text = QCoreApplication.translate("WizardTranslations", "Open table of attributes")
        level = Qgis.Info
        layer = self.__editing_layer
        filter = '"{}" is Null'.format(self.names.LC_PLOT_T_PLOT_AREA_F)
        self.__logger.message_with_button_open_table_attributes_emitted.emit(message, button_text, level, layer, filter)
        # self.close_wizard(show_message=False)
        return EnumPlotCreationResult.CREATED

    def get_number_of_selected_features(self):
        feature_count = dict()

        for layer in self.__relatable_layers:
            feature_count[layer] = self.__relatable_layers[layer].selectedFeatureCount()

        return feature_count
