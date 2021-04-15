from qgis.PyQt.QtWidgets import QWizardPage
from qgis.PyQt.QtCore import QCoreApplication

from asistente_ladm_col.config.general_config import CSS_COLOR_INACTIVE_LABEL, CSS_COLOR_OKAY_LABEL
from asistente_ladm_col.gui.wizards.abc.signal_disconnectable import SignalDisconnectableMetaWiz
from asistente_ladm_col.gui.wizards.view.view_enum import EnumTypeOfOption
from asistente_ladm_col.gui.wizards.view.view_params import OptionChangedParams, FeatureSelectedParams
from asistente_ladm_col.utils.ui import load_ui


class ExtAddressSurveyView(QWizardPage, metaclass=SignalDisconnectableMetaWiz):

    def __init__(self, controller, help_texts: dict):
        QWizardPage.__init__(self)
        self.__controller = controller
        load_ui('wizards/wizard_pages/survey/wiz_associate_extaddress_survey.ui', self)

        self.__help_texts = help_texts
        self.__init_gui()

    @property
    def selected_type(self):
        for item_type in self.__controls_by_type:
            if self.__controls_by_type[item_type]["radio"].isChecked():
                return item_type

    @selected_type.setter
    def selected_type(self, value: EnumTypeOfOption):
        self.__controls_by_type[value]["radio"].setChecked(True)

    def set_selected_item_style(self, selected_option_style):
        for item_type in self.__controls_by_type:
            item = self.__controls_by_type[item_type]
            style = CSS_COLOR_INACTIVE_LABEL
            if item["radio"].isChecked():
                style = selected_option_style or CSS_COLOR_OKAY_LABEL
            item["radio"].setStyleSheet(style)
            item["lbl_count"].setStyleSheet(style)

    def set_feature_count(self, feature_count: dict):
        for item_type in self.__controls_by_type:
            self.__controls_by_type[item_type]["lbl_count"].setText(QCoreApplication.translate("WizardTranslations", "{count} Feature(s) Selected").format(count=feature_count[item_type]))

    def connect_signals(self):
        self.__register_radio_toggle()
        self.__register_select_feature_on_map()
        self.__register_select_features_by_expression()

    def disconnect_signals(self):
        signals = [self.btn_plot_expression.clicked,
                   self.btn_building_expression.clicked,
                   self.btn_building_unit_expression.clicked,
                   self.btn_plot_map.clicked,
                   self.btn_building_map.clicked,
                   self.btn_building_unit_map.clicked,
                   self.rad_to_plot.toggled,
                   self.rad_to_building.toggled,
                   self.rad_to_building_unit.toggled]

        for signal in signals:
            try:
                signal.disconnect()
            except:
                pass

    def __init_gui(self):
        self.__init_dict_controls_by_type()
        self.connect_signals()

    def __toggle_radio(self, check):
        if not check:
            return
        # set help text
        self.txt_help_page_2.setHtml(self.__controls_by_type[self.selected_type]["help_text"])

        self.__enable_feature_selector_buttons()

        self.__notify_option_changed()

    def __notify_option_changed(self):
        option_changed_params = OptionChangedParams(self.selected_type)
        self.__controller.option_changed(option_changed_params)

    def __enable_feature_selector_buttons(self):
        for item_type in self.__controls_by_type:
            enable = item_type == self.selected_type
            item = self.__controls_by_type[item_type]
            item["btn_map"].setEnabled(enable)
            item["btn_expression"].setEnabled(enable)

    def __init_dict_controls_by_type(self):
        self.__controls_by_type = dict()

        self.__controls_by_type[EnumTypeOfOption.PLOT] = {
            "radio": self.rad_to_plot,
            "lbl_count": self.lbl_plot_count,
            "btn_map": self.btn_plot_map,
            "btn_expression": self.btn_plot_expression,
            "help_text": self.__help_texts[EnumTypeOfOption.PLOT]}

        self.__controls_by_type[EnumTypeOfOption.BUILDING] = {
            "radio": self.rad_to_building,
            "lbl_count": self.lbl_building_count,
            "btn_map": self.btn_building_map,
            "btn_expression": self.btn_building_expression,
            "help_text": self.__help_texts[EnumTypeOfOption.BUILDING]}

        self.__controls_by_type[EnumTypeOfOption.BUILDING_UNIT] = {
            "radio": self.rad_to_building_unit,
            "lbl_count": self.lbl_building_unit_count,
            "btn_map": self.btn_building_unit_map,
            "btn_expression": self.btn_building_unit_expression,
            "help_text": self.__help_texts[EnumTypeOfOption.BUILDING_UNIT]}

    def __register_radio_toggle(self):
        self.rad_to_plot.toggled.connect(self.__toggle_radio)
        self.rad_to_building.toggled.connect(self.__toggle_radio)
        self.rad_to_building_unit.toggled.connect(self.__toggle_radio)

    def __register_select_features_by_expression(self):
        self.btn_plot_expression.clicked.connect(self.__btn_plot_expression_click)
        self.btn_building_expression.clicked.connect(self.__btn_building_expression_click)
        self.btn_building_unit_expression.clicked.connect(self.__btn_building_unit_expression_click)

    def __register_select_feature_on_map(self):
        self.btn_plot_map.clicked.connect(self.__btn_plot_map_click)
        self.btn_building_map.clicked.connect(self.__btn_building_map_click)
        self.btn_building_unit_map.clicked.connect(self.__btn_building_unit_map_click)

    def __btn_plot_map_click(self):
        feature_selected_params = FeatureSelectedParams(EnumTypeOfOption.PLOT)
        self.__controller.feature_by_map_selected(feature_selected_params)

    def __btn_plot_expression_click(self):
        feature_selected_params = FeatureSelectedParams(EnumTypeOfOption.PLOT)
        self.__controller.feature_by_expression_selected(feature_selected_params)

    def __btn_building_map_click(self):
        feature_selected_params = FeatureSelectedParams(EnumTypeOfOption.BUILDING)
        self.__controller.feature_by_map_selected(feature_selected_params)

    def __btn_building_expression_click(self):
        feature_selected_params = FeatureSelectedParams(EnumTypeOfOption.BUILDING)
        self.__controller.feature_by_expression_selected(feature_selected_params)

    def __btn_building_unit_map_click(self):
        feature_selected_params = FeatureSelectedParams(EnumTypeOfOption.BUILDING_UNIT)
        self.__controller.feature_by_map_selected(feature_selected_params)

    def __btn_building_unit_expression_click(self):
        feature_selected_params = FeatureSelectedParams(EnumTypeOfOption.BUILDING_UNIT)
        self.__controller.feature_by_expression_selected(feature_selected_params)
