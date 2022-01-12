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
from asistente_ladm_col.gui.wizards.model.common.args.model_args import ExecFormAdvancedArgs
from asistente_ladm_col.gui.wizards.model.common.manual_feature_creator import AlphaFeatureCreator
from asistente_ladm_col.gui.wizards.model.common.select_features_by_expression_dialog_wrapper import \
    SelectFeatureByExpressionDialogWrapper
from asistente_ladm_col.gui.wizards.model.common.select_features_on_map_wrapper import SelectFeaturesOnMapWrapper
from asistente_ladm_col.gui.wizards.controller.common.abstract_wizard_controller import (AbstractWizardController,
                                                                                         ProductFactory)
from asistente_ladm_col.gui.wizards.controller.common.wizard_messages_manager import WizardMessagesManager

from asistente_ladm_col.gui.wizards.view.pages.features_selector_view import EnumFeatureSelectionType
from asistente_ladm_col.gui.wizards.model.parcel_creator_model import ParcelCreatorManager
from asistente_ladm_col.gui.wizards.view.common.view_args import PickFeaturesSelectedArgs

from asistente_ladm_col.gui.wizards.view.parcel_view import ParcelView


class ParcelProductFactory(ProductFactory):

    def create_manual_feature_creator(self, iface, app, logger, layer, feature_name):
        return AlphaFeatureCreator(iface, app, logger, layer, feature_name)

    def create_feature_selector_on_map(self, iface, logger, multiple_features=True):
        return SelectFeaturesOnMapWrapper(iface, logger)

    def create_feature_selector_by_expression(self, iface):
        return SelectFeatureByExpressionDialogWrapper(iface)

    def create_wizard_messages_manager(self, wizard_tool_name, editing_layer_name, logger):
        return WizardMessagesManager(wizard_tool_name, editing_layer_name, logger)

    def create_feature_manager(self, db, layers, editing_layer):
        return ParcelCreatorManager(db, layers, editing_layer)


class ParcelController(AbstractWizardController):

    def __init__(self, iface, db, wizard_config, observer):
        AbstractWizardController.__init__(self, iface, db, wizard_config, ParcelProductFactory(), observer)
        self.__manual_feature_creator = None

        self._initialize()

    def _create_feature_selector_by_expression(self):
        self.__feature_selector_by_expression = SelectFeatureByExpressionDialogWrapper(self._iface)
        return self.__feature_selector_by_expression

    # manual feature creator
    def exec_form_advanced(self, args: ExecFormAdvancedArgs):
        # TODO
        self._feature_manager.exec_form_advanced(args)

    def _create_view(self):
        self.__view = ParcelView(self, self._get_view_config())
        parcel_types = self._feature_manager.get_type_parcel_conditions()
        self.__view.load_parcel_types(parcel_types)
        return self.__view

    # methods called from the view
    def next_clicked(self):
        self.__show_number_of_selected_features()
        self.__enable_finish_button()

    def pick_features_selected(self, args: PickFeaturesSelectedArgs):
        layer = self._feature_manager.get_layer_by_type(args.selected_type)

        if args.feature_selection_type == EnumFeatureSelectionType.SELECTION_ON_MAP:
            self.__view.set_visible(False)  # Make wizard disappear
            self._layer_remove_manager.reconnect_signals()
            self._feature_selector_on_map.select_features_on_map(layer)
        elif args.feature_selection_type == EnumFeatureSelectionType.SELECTION_BY_EXPRESSION:
            self._feature_selector_by_expression.select_features_by_expression(layer)

    def parcel_type_changed(self, parcel_type_ili_code):
        self._feature_manager.parcel_type_ili_code = parcel_type_ili_code

        spatial_units_options_status = self._feature_manager.get_layer_status()
        self.__view.set_spatial_units_options_status(spatial_units_options_status)
        self.__enable_finish_button()
    # from view |<-

    def feature_selection_by_expression_changed(self):
        self.__update_spatial_units_status()

    def __update_spatial_units_status(self):
        self.__show_number_of_selected_features()
        spatial_units_options_status = self._feature_manager.get_layer_status()
        self.__view.set_spatial_units_options_status(spatial_units_options_status)
        self.__enable_finish_button()

    # feature selector on map
    def features_selected(self):
        self.__view.set_visible(True)
        self.__update_spatial_units_status()

    def __show_number_of_selected_features(self):
        feature_count = self._feature_manager.get_number_of_selected_features()
        self.__view.show_number_of_selected_features(feature_count)

    def __enable_finish_button(self):
        will_enable_finish_button = self._feature_manager.is_each_layer_valid()
        self.__view.enable_finish_button(will_enable_finish_button)
