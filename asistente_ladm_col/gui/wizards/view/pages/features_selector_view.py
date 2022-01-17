# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-09-10
        git sha              : :%H$
        copyright            : (C) 2019 by Leo Cardona (BFS Swissphoto)
                               (C) 2021 by Yesid Polanía (BFS Swissphoto)
        email                : leo.cardona.p@gmail.com
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
from abc import (abstractmethod,
                 ABC)
from functools import partial

from qgis.PyQt.QtWidgets import QWizardPage
from qgis.PyQt.QtCore import QCoreApplication

from asistente_ladm_col.config.enums import (EnumRelatableLayers,
                                             EnumFeatureSelectionType)
from asistente_ladm_col.config.general_config import (WIZARD_HELP_PAGES,
                                                      WIZARD_HELP2,
                                                      WIZARD_STRINGS,
                                                      WIZARD_SEL_FEATURES_TITLE,
                                                      CSS_COLOR_INACTIVE_LABEL,
                                                      CSS_COLOR_OKAY_LABEL,
                                                      CSS_COLOR_ERROR_LABEL)
from asistente_ladm_col.config.help_strings import HelpStrings
from asistente_ladm_col.gui.wizards.view.common.view_args import (PickFeaturesSelectedArgs,
                                                                  OptionChangedArgs)
from asistente_ladm_col.utils.ui import load_ui


class FeaturesSelectorView(ABC):

    def __init__(self, controller):
        self.__controller = controller

        self.__qwizard_page = self._create_qwizard_page()
        self.__controls_by_type = self._create_dict_controls_by_type()
        self.connect_signals()

    @abstractmethod
    def _create_qwizard_page(self):
        pass

    @abstractmethod
    def _create_dict_controls_by_type(self):
        pass

    def get_wizard_page(self):
        return self.__qwizard_page

    def show_number_of_selected_features(self, feature_count):
        for layer_type in feature_count:
            if layer_type not in self.__controls_by_type:
                continue
            self.__controls_by_type[layer_type]["lbl_count"].setText(
                QCoreApplication.translate("WizardTranslations", "{count} Feature(s) Selected").format(
                    count=feature_count[layer_type]))

    def __btn_pick_features_click(self, option_type: EnumRelatableLayers, selection_type: EnumFeatureSelectionType):
        feature_selected_args = PickFeaturesSelectedArgs(option_type, selection_type)
        self.__controller.pick_features_selected(feature_selected_args)

    def connect_signals(self):
        for layer_type in self.__controls_by_type:
            for selection_type in self.__controls_by_type[layer_type]["buttons"]:
                self.__controls_by_type[layer_type]["buttons"][selection_type].clicked.connect(
                    partial(self.__btn_pick_features_click, option_type=layer_type, selection_type=selection_type))

    def disconnect_signals(self):
        for layer_type in self.__controls_by_type:
            for selection_type in self.__controls_by_type[layer_type]["buttons"]:
                self.__controls_by_type[layer_type]["buttons"][selection_type].clicked.disconnect()


class PlotSelectorView(FeaturesSelectorView):
    def __init__(self, controller, help_text):
        super().__init__(controller)
        self.__controller = controller
        self.__help_text = help_text
        self.__qwizard_page.txt_help_page_2.setHtml(self.__help_text)

    def _create_qwizard_page(self) -> QWizardPage:
        self.__qwizard_page = QWizardPage()
        ui_path = 'wizards/survey/wiz_create_plot_survey.ui'
        load_ui(ui_path, self.__qwizard_page)
        return self.__qwizard_page

    def _create_dict_controls_by_type(self):
        self.__controls_by_type = dict()

        self.__controls_by_type[EnumRelatableLayers.BOUNDARY] = {
            "lbl": self.__qwizard_page.lbl_boundary,
            "lbl_count": self.__qwizard_page.lbl_boundary_count,
            "buttons": {
                EnumFeatureSelectionType.SELECTION_ON_MAP: self.__qwizard_page.btn_boundary_map,
                EnumFeatureSelectionType.SELECTION_BY_EXPRESSION: self.__qwizard_page.btn_boundary_expression,
                EnumFeatureSelectionType.ALL_FEATURES: self.__qwizard_page.btn_boundary_select_all
            }}
        return self.__controls_by_type


class RrrSelectorView(FeaturesSelectorView):
    def __init__(self, controller, view_config):
        super().__init__(controller)
        self.__controller = controller
        self.__help_text = view_config[WIZARD_HELP_PAGES][WIZARD_HELP2]
        self.__qwizard_page.txt_help_page_2.setHtml(self.__help_text)
        self.__qwizard_page.gbx_page2.setTitle(view_config[WIZARD_STRINGS][WIZARD_SEL_FEATURES_TITLE])

    def _create_qwizard_page(self) -> QWizardPage:
        self.__qwizard_page = QWizardPage()
        ui_path = 'wizards/survey/wiz_create_restriction_survey.ui'
        load_ui(ui_path, self.__qwizard_page)
        return self.__qwizard_page

    def _create_dict_controls_by_type(self):
        self.__controls_by_type = dict()

        self.__controls_by_type[EnumRelatableLayers.ADMINISTRATIVE_SOURCE] = {
            "lbl": self.__qwizard_page.lbl_admin_source,
            "lbl_count": self.__qwizard_page.lbl_admin_source_count,
            "buttons": {
                EnumFeatureSelectionType.SELECTION_BY_EXPRESSION: self.__qwizard_page.btn_expression
            }}
        return self.__controls_by_type


class SpatialSourceFeaturesSelectorView(FeaturesSelectorView):
    def __init__(self, controller, help_text: str):
        super().__init__(controller)
        self.__controller = controller
        self.__help_text = help_text

        self.__qwizard_page.txt_help_page_2.setHtml(self.__help_text)

    def _create_qwizard_page(self) -> QWizardPage:
        self.__qwizard_page = QWizardPage()
        ui_path = 'wizards/survey/wiz_create_spatial_source_survey.ui'
        load_ui(ui_path, self.__qwizard_page)
        return self.__qwizard_page

    def _create_dict_controls_by_type(self):
        self.__controls_by_type = dict()

        self.__controls_by_type[EnumRelatableLayers.PLOT] = {
            "lbl": self.__qwizard_page.lbl_plot,
            "lbl_count": self.__qwizard_page.lbl_plot_count,
            "buttons": {
                EnumFeatureSelectionType.SELECTION_ON_MAP: self.__qwizard_page.btn_plot_map,
                EnumFeatureSelectionType.SELECTION_BY_EXPRESSION: self.__qwizard_page.btn_plot_expression
            }}

        self.__controls_by_type[EnumRelatableLayers.BOUNDARY] = {
            "lbl": self.__qwizard_page.lbl_boundary,
            "lbl_count": self.__qwizard_page.lbl_boundary_count,
            "buttons": {
                EnumFeatureSelectionType.SELECTION_ON_MAP: self.__qwizard_page.btn_boundary_map,
                EnumFeatureSelectionType.SELECTION_BY_EXPRESSION: self.__qwizard_page.btn_boundary_expression
            }}

        self.__controls_by_type[EnumRelatableLayers.BOUNDARY_POINT] = {
            "lbl": self.__qwizard_page.lbl_boundary_point,
            "lbl_count": self.__qwizard_page.lbl_boundary_point_count,
            "buttons": {
                EnumFeatureSelectionType.SELECTION_ON_MAP: self.__qwizard_page.btn_boundary_point_map,
                EnumFeatureSelectionType.SELECTION_BY_EXPRESSION: self.__qwizard_page.btn_boundary_point_expression
            }}

        self.__controls_by_type[EnumRelatableLayers.SURVEY_POINT] = {
            "lbl": self.__qwizard_page.lbl_survey_point,
            "lbl_count": self.__qwizard_page.lbl_survey_point_count,
            "buttons": {
                EnumFeatureSelectionType.SELECTION_ON_MAP: self.__qwizard_page.btn_survey_point_map,
                EnumFeatureSelectionType.SELECTION_BY_EXPRESSION: self.__qwizard_page.btn_survey_point_expression
            }}

        self.__controls_by_type[EnumRelatableLayers.CONTROL_POINT] = {
            "lbl": self.__qwizard_page.lbl_control_point,
            "lbl_count": self.__qwizard_page.lbl_control_point_count,
            "buttons": {
                EnumFeatureSelectionType.SELECTION_ON_MAP: self.__qwizard_page.btn_control_point_map,
                EnumFeatureSelectionType.SELECTION_BY_EXPRESSION: self.__qwizard_page.btn_control_point_expression
            }}
        return self.__controls_by_type


class ParcelSelectorView(FeaturesSelectorView):
    def __init__(self, controller, help_text: str):
        super().__init__(controller)
        self.__controller = controller
        self.__help_text = help_text

    def _create_qwizard_page(self) -> QWizardPage:
        self.__qwizard_page = QWizardPage()
        ui_path = 'wizards/survey/wiz_create_parcel_survey.ui'
        load_ui(ui_path, self.__qwizard_page)
        return self.__qwizard_page

    def load_parcel_types(self, parcel_types: dict):
        self.__qwizard_page.cb_parcel_type.clear()
        for key in parcel_types:
            self.__qwizard_page.cb_parcel_type.addItem(parcel_types[key], key)

    def _create_dict_controls_by_type(self):
        self.__controls_by_type = dict()

        self.__controls_by_type[EnumRelatableLayers.PLOT] = {
            "lbl": self.__qwizard_page.lbl_plot,
            "lbl_count": self.__qwizard_page.lbl_plot_count,
            "buttons": {
                EnumFeatureSelectionType.SELECTION_ON_MAP: self.__qwizard_page.btn_plot_map,
                EnumFeatureSelectionType.SELECTION_BY_EXPRESSION: self.__qwizard_page.btn_plot_expression
            }}

        self.__controls_by_type[EnumRelatableLayers.BUILDING] = {
            "lbl": self.__qwizard_page.lbl_building,
            "lbl_count": self.__qwizard_page.lbl_building_count,
            "buttons": {
                EnumFeatureSelectionType.SELECTION_ON_MAP: self.__qwizard_page.btn_building_map,
                EnumFeatureSelectionType.SELECTION_BY_EXPRESSION: self.__qwizard_page.btn_building_expression
            }}

        self.__controls_by_type[EnumRelatableLayers.BUILDING_UNIT] = {
            "lbl": self.__qwizard_page.lbl_building_unit,
            "lbl_count": self.__qwizard_page.lbl_building_unit_count,
            "buttons": {
                EnumFeatureSelectionType.SELECTION_ON_MAP: self.__qwizard_page.btn_building_unit_map,
                EnumFeatureSelectionType.SELECTION_BY_EXPRESSION: self.__qwizard_page.btn_building_unit_expression
            }}

        return self.__controls_by_type

    @property
    def current_parcel_type(self):
        return self.__qwizard_page.cb_parcel_type.currentData()

    @current_parcel_type.setter
    def current_parcel_type(self, value):
        index = self.__qwizard_page.cb_parcel_type.findData(value)
        if index != -1:
            self.__qwizard_page.cb_parcel_type.setCurrentIndex(index)

    # specific parcel
    def connect_signals(self):
        super().connect_signals()
        self.__qwizard_page.cb_parcel_type.currentIndexChanged.connect(self.__option_changed)

    def __option_changed(self, index):
        parcel_type_ili_code = self.__qwizard_page.cb_parcel_type.itemData(index)

        self.__controller.parcel_type_changed(parcel_type_ili_code)

        self.__update_help_message(parcel_type_ili_code)

    def __update_help_message(self, parcel_type):
        help_strings = HelpStrings()
        msg_parcel_type = help_strings.get_message_parcel_type(parcel_type)
        msg_parcel_type = msg_parcel_type.replace(parcel_type, self.__qwizard_page.cb_parcel_type.currentText())

        msg_help = self.__help_text.format(msg_parcel_type=msg_parcel_type)
        self.__qwizard_page.txt_help_page_2.setHtml(msg_help)

    def set_spatial_units_options_status(self, spatial_units_status: dict):
        for item_type in self.__controls_by_type:
            style = CSS_COLOR_INACTIVE_LABEL
            will_active_button = False
            if item_type in spatial_units_status:
                style = CSS_COLOR_OKAY_LABEL if spatial_units_status[item_type] else CSS_COLOR_ERROR_LABEL
                will_active_button = True

            item = self.__controls_by_type[item_type]

            item["lbl"].setStyleSheet(style)
            item["lbl_count"].setStyleSheet(style)

            for button_index in item["buttons"]:
                item["buttons"][button_index].setEnabled(will_active_button)


class ExtAddressSelectorView(FeaturesSelectorView):
    def __init__(self, controller, help_text):
        super().__init__(controller)
        self.__controller = controller
        self.__help_texts = help_text

    def _create_qwizard_page(self) -> QWizardPage:
        self.__qwizard_page = QWizardPage()
        ui_path = 'wizards/survey/wiz_associate_extaddress_survey.ui'
        load_ui(ui_path, self.__qwizard_page)
        return self.__qwizard_page

    def _create_dict_controls_by_type(self):
        self.__controls_by_type = dict()

        self.__controls_by_type[EnumRelatableLayers.PLOT] = {
            "radio": self.__qwizard_page.rad_to_plot,
            "lbl_count": self.__qwizard_page.lbl_plot_count,
            "buttons": {
                EnumFeatureSelectionType.SELECTION_ON_MAP: self.__qwizard_page.btn_plot_map,
                EnumFeatureSelectionType.SELECTION_BY_EXPRESSION: self.__qwizard_page.btn_plot_expression
            }}

        self.__controls_by_type[EnumRelatableLayers.BUILDING] = {
            "radio": self.__qwizard_page.rad_to_building,
            "lbl_count": self.__qwizard_page.lbl_building_count,
            "buttons": {
                EnumFeatureSelectionType.SELECTION_ON_MAP: self.__qwizard_page.btn_building_map,
                EnumFeatureSelectionType.SELECTION_BY_EXPRESSION: self.__qwizard_page.btn_building_expression
            }}

        self.__controls_by_type[EnumRelatableLayers.BUILDING_UNIT] = {
            "radio": self.__qwizard_page.rad_to_building_unit,
            "lbl_count": self.__qwizard_page.lbl_building_unit_count,
            "buttons": {
                EnumFeatureSelectionType.SELECTION_ON_MAP: self.__qwizard_page.btn_building_unit_map,
                EnumFeatureSelectionType.SELECTION_BY_EXPRESSION: self.__qwizard_page.btn_building_unit_expression
            }}

        return self.__controls_by_type

    # specific ext_address
    def connect_signals(self):
        super().connect_signals()
        for layer_type in self.__controls_by_type:
            self.__controls_by_type[layer_type]["radio"].toggled.connect(self.__toggle_radio)

    def disconnect_signals(self):
        super().disconnect_signals()
        for layer_type in self.__controls_by_type:
            self.__controls_by_type[layer_type]["radio"].toggled.disconnect()

    @property
    def selected_type(self):
        for item_type in self.__controls_by_type:
            if self.__controls_by_type[item_type]["radio"].isChecked():
                return item_type

    @selected_type.setter
    def selected_type(self, value: EnumRelatableLayers):
        self.__controls_by_type[value]["radio"].setChecked(True)

    def __toggle_radio(self, check):
        if not check:
            return
        # set help text
        self.__qwizard_page.txt_help_page_2.setHtml(self.__help_texts[self.selected_type])

        self.__enable_feature_selector_buttons()
        self.__notify_option_changed()

    def set_styles(self, selected_option_style):
        for item_type in self.__controls_by_type:
            item = self.__controls_by_type[item_type]
            style = CSS_COLOR_INACTIVE_LABEL
            if item["radio"].isChecked():
                style = selected_option_style or CSS_COLOR_OKAY_LABEL
            item["radio"].setStyleSheet(style)
            item["lbl_count"].setStyleSheet(style)

    def __enable_feature_selector_buttons(self):
        for item_type in self.__controls_by_type:
            enable = item_type == self.selected_type
            item = self.__controls_by_type[item_type]
            item["buttons"][EnumFeatureSelectionType.SELECTION_ON_MAP].setEnabled(enable)
            item["buttons"][EnumFeatureSelectionType.SELECTION_BY_EXPRESSION].setEnabled(enable)

    def __notify_option_changed(self):
        option_changed_args = OptionChangedArgs(self.selected_type)
        self.__controller.option_changed(option_changed_args)
