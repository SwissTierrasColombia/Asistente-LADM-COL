from qgis.PyQt.QtWidgets import QWizardPage
from qgis.PyQt.QtCore import QCoreApplication

from asistente_ladm_col.gui.wizards.abc.signal_disconnectable import SignalDisconnectableMetaWiz
from asistente_ladm_col.gui.wizards.view.view_enum import EnumTypeOfOption
from asistente_ladm_col.gui.wizards.view.view_params import FeatureSelectedParams
from asistente_ladm_col.utils.ui import load_ui


class SpatialSourceSurveyView(QWizardPage, metaclass=SignalDisconnectableMetaWiz):

    def __init__(self, controller, help_text: str):
        QWizardPage.__init__(self)
        self.__controller = controller
        load_ui('wizards/wizard_pages/survey/wiz_create_spatial_source_survey.ui', self)

        self.__help_text = help_text
        self.__init_gui()

    def set_feature_count(self, feature_count: dict):
        for item_type in self.__controls_by_type:
            self.__controls_by_type[item_type]["lbl_count"].setText(QCoreApplication.translate("WizardTranslations", "{count} Feature(s) Selected").format(count=feature_count[item_type]))

    def connect_signals(self):
        self.__register_select_feature_on_map()
        self.__register_select_features_by_expression()

    def disconnect_signals(self):
        signals = [self.btn_plot_expression.clicked,
                   self.btn_boundary_expression.clicked,
                   self.btn_boundary_point_expression.clicked,
                   self.btn_survey_point_expression.clicked,
                   self.btn_control_point_expression.clicked,
                   self.btn_plot_map.clicked,
                   self.btn_boundary_map.clicked,
                   self.btn_boundary_point_map.clicked,
                   self.btn_survey_point_map.clicked,
                   self.btn_control_point_map.clicked]

        for signal in signals:
            try:
                signal.disconnect()
            except:
                pass

    def __init_gui(self):
        self.txt_help_page_2.setHtml(self.__help_text)
        self.__init_dict_controls_by_type()
        self.connect_signals()

    def __init_dict_controls_by_type(self):
        self.__controls_by_type = dict()

        self.__controls_by_type[EnumTypeOfOption.PLOT] = {
            "lbl": self.lbl_plot,
            "lbl_count": self.lbl_plot_count,
            "btn_map": self.btn_plot_map,
            "btn_expression": self.btn_plot_expression}

        self.__controls_by_type[EnumTypeOfOption.BOUNDARY] = {
            "lbl": self.lbl_boundary,
            "lbl_count": self.lbl_boundary_count,
            "btn_map": self.btn_boundary_map,
            "btn_expression": self.btn_boundary_expression}

        self.__controls_by_type[EnumTypeOfOption.BOUNDARY_POINT] = {
            "lbl": self.lbl_boundary_point,
            "lbl_count": self.lbl_boundary_point_count,
            "btn_map": self.btn_boundary_point_map,
            "btn_expression": self.btn_boundary_point_expression}

        self.__controls_by_type[EnumTypeOfOption.SURVEY_POINT] = {
            "lbl": self.lbl_survey_point,
            "lbl_count": self.lbl_survey_point_count,
            "btn_map": self.btn_survey_point_map,
            "btn_expression": self.btn_survey_point_expression}

        self.__controls_by_type[EnumTypeOfOption.CONTROL_POINT] = {
            "lbl": self.lbl_control_point,
            "lbl_count": self.lbl_control_point_count,
            "btn_map": self.btn_control_point_map,
            "btn_expression": self.btn_control_point_expression}

    def __register_select_features_by_expression(self):
        self.btn_plot_expression.clicked.connect(self.__btn_plot_expression_click)
        self.btn_boundary_expression.clicked.connect(self.__btn_boundary_expression_click)
        self.btn_boundary_point_expression.clicked.connect(self.__btn_boundary_point_expression_click)
        self.btn_survey_point_expression.clicked.connect(self.__btn_survey_point_expression_click)
        self.btn_control_point_expression.clicked.connect(self.__btn_control_point_expression_click)

    def __register_select_feature_on_map(self):
        self.btn_plot_map.clicked.connect(self.__btn_plot_map_click)
        self.btn_boundary_map.clicked.connect(self.__btn_boundary_map_click)
        self.btn_boundary_point_map.clicked.connect(self.__btn_boundary_point_map_click)
        self.btn_survey_point_map.clicked.connect(self.__btn_survey_point_map_click)
        self.btn_control_point_map.clicked.connect(self.__btn_control_point_map_click)

    def __btn_plot_map_click(self):
        feature_selected_params = FeatureSelectedParams(EnumTypeOfOption.PLOT)
        self.__controller.feature_by_map_selected(feature_selected_params)

    def __btn_plot_expression_click(self):
        feature_selected_params = FeatureSelectedParams(EnumTypeOfOption.PLOT)
        self.__controller.feature_by_expression_selected(feature_selected_params)

    def __btn_boundary_map_click(self):
        feature_selected_params = FeatureSelectedParams(EnumTypeOfOption.BOUNDARY)
        self.__controller.feature_by_map_selected(feature_selected_params)

    def __btn_boundary_expression_click(self):
        feature_selected_params = FeatureSelectedParams(EnumTypeOfOption.BOUNDARY)
        self.__controller.feature_by_expression_selected(feature_selected_params)

    def __btn_boundary_point_map_click(self):
        feature_selected_params = FeatureSelectedParams(EnumTypeOfOption.BOUNDARY_POINT)
        self.__controller.feature_by_map_selected(feature_selected_params)

    def __btn_boundary_point_expression_click(self):
        feature_selected_params = FeatureSelectedParams(EnumTypeOfOption.BOUNDARY_POINT)
        self.__controller.feature_by_expression_selected(feature_selected_params)

    def __btn_survey_point_map_click(self):
        feature_selected_params = FeatureSelectedParams(EnumTypeOfOption.SURVEY_POINT)
        self.__controller.feature_by_map_selected(feature_selected_params)

    def __btn_survey_point_expression_click(self):
        feature_selected_params = FeatureSelectedParams(EnumTypeOfOption.SURVEY_POINT)
        self.__controller.feature_by_expression_selected(feature_selected_params)

    def __btn_control_point_map_click(self):
        feature_selected_params = FeatureSelectedParams(EnumTypeOfOption.CONTROL_POINT)
        self.__controller.feature_by_map_selected(feature_selected_params)

    def __btn_control_point_expression_click(self):
        feature_selected_params = FeatureSelectedParams(EnumTypeOfOption.CONTROL_POINT)
        self.__controller.feature_by_expression_selected(feature_selected_params)
