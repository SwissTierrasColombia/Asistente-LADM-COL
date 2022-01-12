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
from asistente_ladm_col.config.enums import (EnumRelatableLayers,
                                             EnumFeatureSelectionType)
from asistente_ladm_col.config.general_config import (CSS_COLOR_OKAY_LABEL,
                                                      CSS_COLOR_ERROR_LABEL)
from asistente_ladm_col.gui.wizards.view.ext_address_view import ExtAddressView
from asistente_ladm_col.gui.wizards.view.common.view_args import (PickFeaturesSelectedArgs,
                                                                  OptionChangedArgs)
from asistente_ladm_col.gui.wizards.controller.common.abstract_spatial_wizard_controller import \
    AbstractSpatialWizardController
from asistente_ladm_col.gui.wizards.controller.common.abstract_wizard_controller import ProductFactory
from asistente_ladm_col.gui.wizards.controller.common.wizard_messages_manager import WizardMessagesManager
from asistente_ladm_col.gui.wizards.model.common.args.model_args import ExecFormAdvancedArgs
from asistente_ladm_col.gui.wizards.model.common.manual_feature_creator import SpatialFeatureCreator
from asistente_ladm_col.gui.wizards.model.common.select_features_by_expression_dialog_wrapper import \
    SelectFeatureByExpressionDialogWrapper
from asistente_ladm_col.gui.wizards.model.common.select_features_on_map_wrapper import SelectFeaturesOnMapWrapper
from asistente_ladm_col.gui.wizards.model.ext_address_model import ExtAddressManager


class ExtAddressProductFactory(ProductFactory):

    def __init__(self, iface):
        self.__iface = iface

    def create_manual_feature_creator(self, iface, app, logger, layer, feature_name):
        return SpatialFeatureCreator(iface, app, logger, layer, feature_name, 9)

    def create_feature_selector_on_map(self, iface, logger, multiple_features=True):
        return SelectFeaturesOnMapWrapper(iface, logger)

    def create_feature_selector_by_expression(self, iface):
        return SelectFeatureByExpressionDialogWrapper(iface)

    def create_wizard_messages_manager(self, wizard_tool_name, editing_layer_name, logger):
        return WizardMessagesManager(wizard_tool_name, editing_layer_name, logger)

    def create_feature_manager(self, db, layers, editing_layer):
        return ExtAddressManager(db, layers, editing_layer, self.__iface)


class ExtAddressController(AbstractSpatialWizardController):

    def __init__(self, iface, db, wizard_config, observer):
        product_factory = ExtAddressProductFactory(iface)
        AbstractSpatialWizardController.__init__(self, iface, db, wizard_config, product_factory, observer)
        self.__manual_feature_creator = None

        self._initialize()

    def _initialize(self):
        super()._initialize()
        self.__initialize_selected_option()

    def exec_form_advanced(self, args: ExecFormAdvancedArgs):
        self._feature_manager.exec_form_advanced(args)

    def features_selected(self):
        self.__view.set_visible(True)
        self.__show_number_of_selected_features()
        self.__enable_finish_button()
        self.__update_style_of_number_of_selected_features()

    def feature_selection_by_expression_changed(self):
        self.__show_number_of_selected_features()
        self.__enable_finish_button()
        self.__update_style_of_number_of_selected_features()

    def _create_view(self):
        self.__view = ExtAddressView(self, self._get_view_config())
        return self.__view

    def __show_number_of_selected_features(self):
        feature_count = self._feature_manager.get_number_of_selected_features()
        self.__view.show_number_of_selected_features(feature_count)

    # methods called from the view
    def next_clicked(self):
        self.__show_number_of_selected_features()

    def pick_features_selected(self, args: PickFeaturesSelectedArgs):
        layer = self._feature_manager.get_layer_by_type(self._feature_manager.type_of_selected_layer_to_associate)

        if args.feature_selection_type == EnumFeatureSelectionType.SELECTION_ON_MAP:
            self.__view.set_visible(False)  # Make wizard disappear
            self._layer_remove_manager.reconnect_signals()
            self._feature_selector_on_map.select_features_on_map(layer)
        elif args.feature_selection_type == EnumFeatureSelectionType.SELECTION_BY_EXPRESSION:
            self._feature_selector_by_expression.select_features_by_expression(layer)

    def option_changed(self, args: OptionChangedArgs):
        # actualiza el estilo
        # habilita el botón finalizar si hay un feature seleccionado en la capa seleccionada
        self._feature_manager.type_of_selected_layer_to_associate = args.selected_type
        self.__enable_finish_button()
        self.__update_style_of_number_of_selected_features()

    def __initialize_selected_option(self):
        if self.__select_option_base_on_active_layer():
            return

        if self.__select_option_base_on_layer_with_features():
            return

        # By default current_layer will be plot layer
        self.__select_layer_in_view_and_model(EnumRelatableLayers.PLOT)

    def __select_option_base_on_active_layer(self):
        active_layer_type = self._feature_manager.get_active_layer_type()
        is_option_selected = active_layer_type is not None

        if active_layer_type:
            self.__select_layer_in_view_and_model(active_layer_type)

        return is_option_selected

    def __select_layer_in_view_and_model(self, item_type: EnumRelatableLayers):
        self.__view.selected_type = item_type
        self._feature_manager.type_of_selected_layer_to_associate = item_type

    def __select_option_base_on_layer_with_features(self):
        # Select layer that have least one feature selected
        # as current layer when current layer is not defined
        is_option_selected = False
        features_count = self._feature_manager.get_number_of_selected_features()

        for item_type in features_count:
            if features_count[item_type]:
                self.__select_layer_in_view_and_model(item_type)
                is_option_selected = True
                break

        return is_option_selected

    def __update_style_of_number_of_selected_features(self):
        selected_option_style = CSS_COLOR_OKAY_LABEL if self.__get_selected_layer_features_count() == 1 \
            else CSS_COLOR_ERROR_LABEL

        self.__view.set_styles(selected_option_style)

    def __enable_finish_button(self):
        enable_finish_button = self.__get_selected_layer_features_count() == 1
        self.__view.enable_finish_button(enable_finish_button)

    def __get_selected_layer_features_count(self):
        features_count = self._feature_manager.get_number_of_selected_features()
        return features_count[self._feature_manager.type_of_selected_layer_to_associate]
