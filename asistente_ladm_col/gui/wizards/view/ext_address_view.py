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
from qgis.PyQt.QtWidgets import QWizard

from asistente_ladm_col.config.general_config import (WIZARD_STRINGS,
                                                      WIZARD_HELP,
                                                      WIZARD_HELP_PAGES,
                                                      WIZARD_HELP2,
                                                      WIZARD_HELP3,
                                                      WIZARD_HELP1)
from asistente_ladm_col.gui.wizards.view.common.select_source import SelectSource
from asistente_ladm_col.gui.wizards.controller.controller_args import CreateFeatureArgs
from asistente_ladm_col.gui.wizards.view.pages.features_selector_view import ExtAddressSelectorView
from asistente_ladm_col.gui.wizards.wizard_constants import (WIZARD_REFACTOR_RECENT_MAPPING_OPTIONS,
                                                             WIZARD_REFACTOR_LAYER_FILTERS,
                                                             WIZARD_FINISH_BUTTON_TEXT,
                                                             WIZARD_SELECT_SOURCE_HELP,
                                                             WIZARD_CREATION_MODE_KEY)
from asistente_ladm_col.gui.wizards.view.common.view_enum import (EnumLayerCreationMode,
                                                                  EnumOptionType)
from asistente_ladm_col.gui.wizards.view.common.view_args import PickFeaturesSelectedArgs
from asistente_ladm_col.utils.qt_utils import (disable_next_wizard,
                                               enable_next_wizard)
from asistente_ladm_col.utils.utils import show_plugin_help


class ExtAddressView:

    def __init__(self, controller, view_config):
        self.__wizard = QWizard()
        self.__controller = controller
        self.__view_config = view_config

        self.__wp_select_source = self._create_select_source()

        help_texts = dict()
        help_texts[EnumOptionType.PLOT] = self.__view_config[WIZARD_HELP_PAGES][WIZARD_HELP1]
        help_texts[EnumOptionType.BUILDING] = self.__view_config[WIZARD_HELP_PAGES][WIZARD_HELP2]
        help_texts[EnumOptionType.BUILDING_UNIT] = self.__view_config[WIZARD_HELP_PAGES][WIZARD_HELP3]
        self.__wp_associated_features_selector = ExtAddressSelectorView(controller, help_texts)
        # -||

        self.__init_gui()

    def _create_select_source(self) -> SelectSource:
        return SelectSource(
            self.__view_config[WIZARD_REFACTOR_RECENT_MAPPING_OPTIONS],
            self.__view_config[WIZARD_REFACTOR_LAYER_FILTERS],
            self.__view_config[WIZARD_STRINGS])

    def close(self):
        self.dispose()
        self.__wizard.close()

    def dispose(self):
        self.__wp_select_source.disconnect_signals()
        self.__wp_associated_features_selector.disconnect_signals()
        self.__wp_select_source.option_changed.disconnect()
        self.__wizard.rejected.disconnect()
        self.__wizard.button(QWizard.FinishButton).clicked.disconnect()

    def exec_(self):
        return self.__wizard.exec_()

    def set_visible(self, visible: bool):
        self.__wizard.setVisible(visible)

    def enable_finish_button(self, enable: bool):
        self.__wizard.button(QWizard.FinishButton).setDisabled(not enable)

    def __init_gui(self):
        self.__wp_select_source.option_changed.connect(self.__option_changed)

        self.__wizard.addPage(self.__wp_select_source.get_wizard_page())

        self.__wizard.addPage(self.__wp_associated_features_selector.get_wizard_page())
        self.__wizard.rejected.connect(self.__view_rejected)
        self.__wizard.button(QWizard.FinishButton).clicked.connect(self.__finish_button_click)
        self.__wp_select_source.connect_signals()

        self.__wizard.button(QWizard.NextButton).clicked.connect(self.__next_button_click)
        self.__wizard.button(QWizard.HelpButton).clicked.connect(self._show_help)

    def __view_rejected(self):
        self.__controller.wizard_rejected()

    def __option_changed(self, e: EnumLayerCreationMode):
        self.__wp_select_source.set_help_text(self.__view_config[WIZARD_SELECT_SOURCE_HELP][e])
        finish_button_text = self.__view_config[WIZARD_FINISH_BUTTON_TEXT][e]

        self.__wizard.setButtonText(QWizard.FinishButton, finish_button_text)

        # new
        self.__wp_select_source.get_wizard_page().setFinalPage(e == EnumLayerCreationMode.REFACTOR)
        if e == EnumLayerCreationMode.REFACTOR:
            disable_next_wizard(self.__wizard)
        else:
            enable_next_wizard(self.__wizard)
        # -||

    def _show_help(self):
        show_plugin_help(self.__view_config[WIZARD_HELP])

    def restore_settings(self, settings: dict):
        self.__wp_select_source.layer_creation_mode = settings[WIZARD_CREATION_MODE_KEY]

    def get_settings(self):
        result = {WIZARD_CREATION_MODE_KEY: self.__wp_select_source.layer_creation_mode}
        return result

    def get_selected_layer_refactor(self):
        return self.__wp_select_source.selected_layer

    def get_field_mapping_refactor(self):
        return self.__wp_select_source.field_mapping

    def __finish_button_click(self):
        e = CreateFeatureArgs(self.__wp_select_source.layer_creation_mode)
        self.__controller.create_feature(e)

    # it is multipage
    def __next_button_click(self):
        self.__controller.next_clicked()

    # wizard page 2
    def show_number_of_selected_features(self, feature_count: dict):
        self.__wp_associated_features_selector.show_number_of_selected_features(feature_count)

    def pick_features_selected(self, arg: PickFeaturesSelectedArgs):
        self.__controller.pick_features_selected(arg)

    def set_styles(self, selected_option_style):
        self.__wp_associated_features_selector.set_styles(selected_option_style)

    @property
    def selected_type(self):
        return self.__wp_associated_features_selector.selected_type

    @selected_type.setter
    def selected_type(self, value: EnumOptionType):
        self.__wp_associated_features_selector.selected_type = value
