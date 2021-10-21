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
from asistente_ladm_col.config.enums import EnumLayerCreationMode, EnumFeatureSelectionType
from asistente_ladm_col.config.general_config import (WIZARD_QSETTINGS,
                                                      WIZARD_QSETTINGS_PATH,
                                                      WIZARD_CREATION_MODE_KEY,
                                                      WIZARD_SELECTED_TYPE_KEY)
from asistente_ladm_col.gui.wizards.controller.single_wizard_controller import SingleWizardController
from asistente_ladm_col.gui.wizards.model.common.wizard_q_settings_manager import WizardQSettingsManager
from asistente_ladm_col.gui.wizards.model.parcel_creator_model import ParcelCreatorModel
from asistente_ladm_col.gui.wizards.view.common.view_args import PickFeaturesSelectedArgs
from asistente_ladm_col.gui.wizards.view.parcel_view import ParcelView


class ParcelController(SingleWizardController):

    def __init__(self, model: ParcelCreatorModel, db, wizard_settings):
        self.__model = model
        SingleWizardController.__init__(self, model, db, wizard_settings)

        self.__model.features_selected.connect(self.features_selected)
        self.__model.map_tool_changed.connect(self.map_tool_changed)
        self.__model.feature_selection_by_expression_changed.connect(self.feature_selection_by_expression_changed)
        # QSetings
        self.__settings_manager = WizardQSettingsManager(self.wizard_config[WIZARD_QSETTINGS][WIZARD_QSETTINGS_PATH])

    def _restore_settings(self):
        settings = self.__settings_manager.get_settings()

        if WIZARD_CREATION_MODE_KEY not in settings or settings[WIZARD_CREATION_MODE_KEY] is None:
            settings[WIZARD_CREATION_MODE_KEY] = EnumLayerCreationMode.MANUALLY

        if WIZARD_SELECTED_TYPE_KEY not in settings:
            settings[WIZARD_SELECTED_TYPE_KEY] = None

        self.__view.restore_settings(settings)

    def _create_view(self):
        self.__view = ParcelView(self, self._get_view_config())
        parcel_types = self.__model.get_type_parcel_conditions()
        self.__view.load_parcel_types(parcel_types)
        return self.__view

    # Called from view
    def next_clicked(self):
        self.__show_number_of_selected_features()

    def pick_features_selected(self, args: PickFeaturesSelectedArgs):
        self.__model.type_of_selected_layer_to_associate = args.selected_type
        if args.feature_selection_type == EnumFeatureSelectionType.SELECTION_ON_MAP:
            self.__view.set_visible(False)  # Make wizard disappear
            self.__model.select_features_on_map()
        elif args.feature_selection_type == EnumFeatureSelectionType.SELECTION_BY_EXPRESSION:
            self.__model.select_features_by_expression()

    def parcel_type_changed(self, parcel_type_ili_code):
        self.__model.parcel_type_ili_code = parcel_type_ili_code

        spatial_units_options_status = self.__model.get_layer_status()
        self.__view.set_spatial_units_options_status(spatial_units_options_status)
        self.__enable_finish_button()

    def feature_selection_by_expression_changed(self):
        self.__show_number_of_selected_features()
        spatial_units_options_status = self.__model.get_layer_status()
        self.__view.set_spatial_units_options_status(spatial_units_options_status)
        self.__enable_finish_button()

    def features_selected(self):
        self.__view.set_visible(True)
        self.__show_number_of_selected_features()
        spatial_units_options_status = self.__model.get_layer_status()
        self.__view.set_spatial_units_options_status(spatial_units_options_status)
        self.__enable_finish_button()

    def __show_number_of_selected_features(self):
        feature_count = self.__model.get_number_of_selected_features()
        self.__view.show_number_of_selected_features(feature_count)

    def __enable_finish_button(self):
        will_enable_finish_button = self.__model.is_each_layer_valid()
        self.__view.enable_finish_button(will_enable_finish_button)
