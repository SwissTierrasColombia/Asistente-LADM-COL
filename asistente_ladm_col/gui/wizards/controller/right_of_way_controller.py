# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-09-10
        git sha              : :%H$
        copyright            : (C) 2017 by Germán Carrillo (BSF Swissphoto)
                               (C) 2018 by Sergio Ramírez (Incige SAS)
                               (C) 2018 by Jorge Useche (Incige SAS)
                               (C) 2018 by Jhon Galindo (Incige SAS)
                               (C) 2019 by Leo Cardona (BSF Swissphoto)
                               (C) 2021 by Yesid Polania (BSF Swissphoto)
        email                : gcarrillo@linuxmail.org
                               sergio.ramirez@incige.com
                               naturalmentejorge@gmail.com
                               jhonsigpjc@gmail.com
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
from qgis.core import QgsProject
from asistente_ladm_col.config.enums import EnumLayerCreationMode
from asistente_ladm_col.config.general_config import (WIZARD_HELP_PAGES,
                                                      WIZARD_HELP2,
                                                      WIZARD_FINISH_BUTTON_TEXT,
                                                      WIZARD_SELECT_SOURCE_HELP)
from asistente_ladm_col.gui.wizards.controller.common.abstract_spatial_wizard_controller import \
    AbstractSpatialWizardController
from asistente_ladm_col.gui.wizards.controller.common.abstract_wizard_controller import ProductFactory
from asistente_ladm_col.gui.wizards.controller.common.wizard_messages_manager import WizardMessagesManager
from asistente_ladm_col.gui.wizards.controller.controller_args import CreateFeatureArgs
from asistente_ladm_col.gui.wizards.model.common.args.model_args import ValidFeaturesDigitizedArgs
from asistente_ladm_col.gui.wizards.model.common.layer_remove_signals_manager import LayerRemovedSignalsManager
from asistente_ladm_col.gui.wizards.model.common.manual_feature_creator import SpatialFeatureCreator
from asistente_ladm_col.gui.wizards.model.common.select_features_by_expression_dialog_wrapper import \
    NullSelectorByExpression
from asistente_ladm_col.gui.wizards.model.common.select_features_on_map_wrapper import NullFeatureSelectorOnMap
from asistente_ladm_col.gui.wizards.model.right_of_way_model import RightOfWayManager
from asistente_ladm_col.gui.wizards.view.right_of_way_view import RightOfWayView


class RightOfWayProductFactory(ProductFactory):

    def create_feature_manager(self, db, layers, editing_layer):
        return RightOfWayManager(db, layers, editing_layer)

    def create_manual_feature_creator(self, iface, app, logger, layer, feature_name):
        return SpatialFeatureCreator(iface, app, logger, layer, feature_name, 9)

    def create_feature_selector_on_map(self, iface, logger, multiple_features=True):
        return NullFeatureSelectorOnMap()

    def create_feature_selector_by_expression(self, iface):
        return NullSelectorByExpression()

    def create_wizard_messages_manager(self, wizard_tool_name, editing_layer_name, logger):
        return WizardMessagesManager(wizard_tool_name, editing_layer_name, logger)


class RightOfWayController(AbstractSpatialWizardController):

    def __init__(self, iface, db, wizard_config, observer):
        AbstractSpatialWizardController.__init__(self, iface, db, wizard_config, RightOfWayProductFactory(), observer)
        self.__manual_feature_creator = None

        self._initialize()

    def _initialize(self):
        super()._initialize()
        self.__temporal_layer = {"memory_line_layer": None}
        self._feature_manager.app = self._app
        self.digitizing_polygon = None
        self.__layer_removed_signal_manager = None

    def _create_view(self):
        self.__view = RightOfWayView(self, self._get_view_config())
        return self.__view

    def create_feature(self, args: CreateFeatureArgs):
        if args.layer_creation_mode == EnumLayerCreationMode.MANUALLY:
            self.digitizing_polygon = True

        if args.layer_creation_mode == EnumLayerCreationMode.DIGITIZING_LINE:
            self._feature_manager.width_line = self.__view.get_with_line_edit()
            self.digitizing_polygon = False

        # TODO this implicit execute create_manually
        super().create_feature(args)

    def _create_manually(self):
        if not self.digitizing_polygon:
            self.__add_memory_line_layer()
        else:
            self._manual_feature_creator.editing_layer = None

        super()._create_manually()

    def _get_view_config(self):
        view_config = super()._get_view_config()
        view_config[WIZARD_FINISH_BUTTON_TEXT][EnumLayerCreationMode.DIGITIZING_LINE] = \
            view_config[WIZARD_FINISH_BUTTON_TEXT][EnumLayerCreationMode.MANUALLY]
        view_config[WIZARD_SELECT_SOURCE_HELP][EnumLayerCreationMode.DIGITIZING_LINE] = \
            self._wizard_config[WIZARD_HELP_PAGES][WIZARD_HELP2]

        return view_config

    def valid_features_digitized(self, args: ValidFeaturesDigitizedArgs):
        self.enable_save_geometry_button.emit(False)

        if not self.digitizing_polygon:
            new_feature = self._feature_manager.get_feature_with_buffer_right_of_way(args.layer, self._editing_layer)
            args.feature = new_feature
            self._feature_manager.add_tmp_feature_to_layer(self._editing_layer, new_feature)

    def dispose(self):
        super().dispose()

        if self.__layer_removed_signal_manager:
            self.__layer_removed_signal_manager.disconnect_signals()

        if self.__temporal_layer["memory_line_layer"]:
            self.rollback_layer(self.__temporal_layer["memory_line_layer"])

            QgsProject.instance().removeMapLayer(self.__temporal_layer["memory_line_layer"])

        self._manual_feature_creator.editing_layer = None

    def __add_memory_line_layer(self):
        temporal_layer = self._feature_manager.get_memory_line_layer(self._editing_layer)

        QgsProject.instance().addMapLayer(temporal_layer, True)

        self._manual_feature_creator.editing_layer = temporal_layer
        self.__temporal_layer["memory_line_layer"] = temporal_layer

        self.__register_tmp_layer_into_layer_removed_signal_manager()

    def __register_tmp_layer_into_layer_removed_signal_manager(self):
        self.__layer_removed_signal_manager = LayerRemovedSignalsManager(self.__temporal_layer)
        self.__layer_removed_signal_manager.layer_removed.connect(self.layer_removed)

        self.__layer_removed_signal_manager.connect_signals()

