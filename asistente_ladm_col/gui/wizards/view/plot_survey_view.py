from qgis.PyQt.QtWidgets import QWizardPage
from qgis.PyQt.QtCore import QCoreApplication

from asistente_ladm_col.config.general_config import CSS_COLOR_INACTIVE_LABEL, CSS_COLOR_OKAY_LABEL
from asistente_ladm_col.gui.wizards.abc.signal_disconnectable import SignalDisconnectableMetaWiz
from asistente_ladm_col.gui.wizards.view.view_enum import EnumTypeOfOption
from asistente_ladm_col.gui.wizards.view.view_params import FeatureSelectedParams
from asistente_ladm_col.utils.ui import load_ui


class PlotSurveyView(QWizardPage, metaclass=SignalDisconnectableMetaWiz):

    def __init__(self, controller, help_text: str):
        QWizardPage.__init__(self)
        self.__controller = controller
        load_ui('wizards/wizard_pages/survey/wiz_create_plot_survey.ui', self)

        self.__help_text = help_text
        self.__init_gui()

    def set_feature_count(self, feature_count: dict):
        for item_type in self.__controls_by_type:
            self.__controls_by_type[item_type]["lbl_count"].setText(QCoreApplication.translate("WizardTranslations", "{count} Feature(s) Selected").format(count=feature_count[item_type]))

    def connect_signals(self):
        self.__register_select_feature_on_map()
        self.__register_select_features_by_expression()

    def disconnect_signals(self):
        signals = [self.btn_boundary_expression.clicked,
                   self.btn_boundary_select_all.clicked,
                   self.btn_boundary_map.clicked]

        for signal in signals:
            try:
                signal.disconnect()
            except:
                pass

    def set_selected_item_style(self, selected_option_style):
        for item_type in self.__controls_by_type:
            item = self.__controls_by_type[item_type]

            style = selected_option_style or CSS_COLOR_OKAY_LABEL

            item["lbl"].setStyleSheet(style)
            item["lbl_count"].setStyleSheet(style)

    def __init_gui(self):
        self.txt_help_page_2.setHtml(self.__help_text)
        self.__init_dict_controls_by_type()
        self.connect_signals()

    def __init_dict_controls_by_type(self):
        self.__controls_by_type = dict()

        self.__controls_by_type[EnumTypeOfOption.BOUNDARY] = {
            "lbl": self.lbl_boundary,
            "lbl_count": self.lbl_boundary_count,
            "btn_map": self.btn_boundary_map,
            "btn_expression": self.btn_boundary_expression,
            "btn_select_all": self.btn_boundary_select_all
        }

    def __register_select_features_by_expression(self):
        self.btn_boundary_expression.clicked.connect(self.__btn_boundary_expression_click)
        self.btn_boundary_select_all.clicked.connect(self.__btn_boundary_select_all_click)

    def __register_select_feature_on_map(self):
        self.btn_boundary_map.clicked.connect(self.__btn_boundary_map_click)

    def __btn_boundary_map_click(self):
        feature_selected_params = FeatureSelectedParams(EnumTypeOfOption.BOUNDARY)
        self.__controller.feature_by_map_selected(feature_selected_params)

    def __btn_boundary_expression_click(self):
        feature_selected_params = FeatureSelectedParams(EnumTypeOfOption.BOUNDARY)
        self.__controller.feature_by_expression_selected(feature_selected_params)

    def __btn_boundary_select_all_click(self):
        feature_selected_params = FeatureSelectedParams(EnumTypeOfOption.BOUNDARY)
        self.__controller.all_feature_selected(feature_selected_params)