from functools import partial

from qgis.PyQt.QtCore import (QCoreApplication,
                              QObject,
                              QSettings,
                              pyqtSignal)
from qgis.PyQt.QtWidgets import QWizard, QMessageBox
from qgis.core import QgsVectorLayerUtils
from asistente_ladm_col import Logger
from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.config.general_config import WIZARD_UI, WIZARD_FEATURE_NAME, WIZARD_TOOL_NAME, \
    WIZARD_EDITING_LAYER_NAME, WIZARD_LAYERS, WIZARD_READ_ONLY_FIELDS, WIZARD_HELP, WIZARD_HELP_PAGES, WIZARD_HELP1, \
    WIZARD_QSETTINGS, WIZARD_QSETTINGS_LOAD_DATA_TYPE, WIZARD_HELP2, WIZARD_STRINGS
from asistente_ladm_col.config.help_strings import HelpStrings
from asistente_ladm_col.config.translation_strings import TranslatableConfigStrings
from asistente_ladm_col.gui.wizards.wizard_pages.asistente_wizard_page import AsistenteWizardPage
from asistente_ladm_col.gui.wizards.wizard_pages.create_manually import CreateManually
from asistente_ladm_col.gui.wizards.wizard_pages.logic import Logic
from asistente_ladm_col.gui.wizards.wizard_pages.select_features_by_expression_dialog_wrapper import \
    SelectFeatureByExpressionDialogWrapper
from asistente_ladm_col.gui.wizards.wizard_pages.select_features_on_map_wrapper import SelectFeaturesOnMapWrapper
from asistente_ladm_col.gui.wizards.wizard_pages.select_source import SelectSource
from asistente_ladm_col.utils.qt_utils import disable_next_wizard, enable_next_wizard
from asistente_ladm_col.utils.select_map_tool import SelectMapTool
from asistente_ladm_col.utils.utils import show_plugin_help
from qgis.gui import QgsExpressionSelectionDialog


class CreateSpatialSourceSurveyWizard: #(QWizard):
    update_wizard_is_open_flag = pyqtSignal(bool)

    def __init__(self, iface, db, wizard_settings):
        print('oooo')
        QWizard.__init__(self)
        self.iface = iface
        self._db = db
        self.wizard_config = wizard_settings

        self.logger = Logger()
        self.app = AppInterface()

        self.names = self._db.names
        self.help_strings = HelpStrings()
        self.translatable_config_strings = TranslatableConfigStrings()
        # load_ui(self.wizard_config[WIZARD_UI], self)

        self.WIZARD_FEATURE_NAME = self.wizard_config[WIZARD_FEATURE_NAME]
        self.WIZARD_TOOL_NAME = self.wizard_config[WIZARD_TOOL_NAME]
        self.EDITING_LAYER_NAME = self.wizard_config[WIZARD_EDITING_LAYER_NAME]
        self._layers = self.wizard_config[WIZARD_LAYERS]

        self.logic = Logic(self.app, db, self._layers, wizard_settings)

        self.set_ready_only_field()

        self.wizardPage1 = None
        self.wizardPage2 = None
        self.init_gui()

        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++>>>>> map tool
        self.__init_new_items()

    def __init_new_items(self):
        self.__manual_feature_creator = CreateManually(self.iface, self.app, self.logger,
                                                       self._layers[self.EDITING_LAYER_NAME], self.WIZARD_FEATURE_NAME)

        self.__manual_feature_creator.register_observer(self)

        # map
        self.__feature_selector_on_map = SelectFeaturesOnMapWrapper(self.iface, self.logger)
        self.__feature_selector_on_map.register_observer(self)

        self.__feature_selector_by_expression = SelectFeatureByExpressionDialogWrapper(self.iface)
        self.__feature_selector_by_expression.register_observer(self)

    def set_ready_only_field(self, read_only=True):
        if self._layers[self.EDITING_LAYER_NAME] is not None:
            for field in self.wizard_config[WIZARD_READ_ONLY_FIELDS]:
                # Not validate field that are read only
                self.app.core.set_read_only_field(self._layers[self.EDITING_LAYER_NAME], field, read_only)

    def init_gui(self):
        # it creates the page (select source)
        self.wizardPage1 = SelectSource(self.logic.get_field_mappings_file_names(),
                                          self.logic.get_filters(), self.wizard_config[WIZARD_STRINGS])
        self.wizardPage1.option_changed.connect(self.adjust_page_1_controls)
        self.restore_settings()

        self.button(QWizard.NextButton).clicked.connect(self.adjust_page_2_controls)
        self.button(QWizard.FinishButton).clicked.connect(self.finished_dialog)
        self.button(QWizard.HelpButton).clicked.connect(self.show_help)
        self.rejected.connect(self.close_wizard)

        self.wizardPage2 = AsistenteWizardPage(self.wizard_config[WIZARD_UI])
        self.wizardPage1.controls_changed()

        self.addPage(self.wizardPage1)
        self.addPage(self.wizardPage2)

    # (absWizardFactory)
    def restore_settings(self):
        settings = QSettings()

        load_data_type = settings.value(self.wizard_config[WIZARD_QSETTINGS][WIZARD_QSETTINGS_LOAD_DATA_TYPE]) or 'create_manually'
        if load_data_type == 'refactor':
            self.wizardPage1.enabled_refactor = True
        else:
            self.wizardPage1.enabled_create_manually = True

    def adjust_page_1_controls(self):
        finish_button_text = ''

        if self.wizardPage1.enabled_refactor:
            disable_next_wizard(self)
            self.wizardPage1.setFinalPage(True)
            finish_button_text = QCoreApplication.translate("WizardTranslations", "Import")
            self.wizardPage1.set_help_text(self.help_strings.get_refactor_help_string(self._db, self._layers[self.EDITING_LAYER_NAME]))
            self.wizardPage1.setButtonText(QWizard.FinishButton, finish_button_text)
        elif self.wizardPage1.enabled_create_manually:
            enable_next_wizard(self)
            self.wizardPage1.setFinalPage(False)
            finish_button_text = QCoreApplication.translate("WizardTranslations", "Create")
            self.wizardPage1.set_help_text(self.wizard_config[WIZARD_HELP_PAGES][WIZARD_HELP1])

        self.wizardPage2.setButtonText(QWizard.FinishButton, finish_button_text)

    # (absWizardFactory)
    def show_help(self):
        show_plugin_help(self.wizard_config[WIZARD_HELP])

    def close_wizard(self, message=None, show_message=True):
        if message is None:
            message = QCoreApplication.translate("WizardTranslations", "'{}' tool has been closed.").format(self.WIZARD_TOOL_NAME)
        if show_message:
            self.logger.info_msg(__name__, message)

        # if isinstance(self, SelectFeaturesOnMapWrapper):
        self.__feature_selector_on_map.init_map_tool()

        self.rollback_in_layers_with_empty_editing_buffer()
        self.disconnect_signals()
        self.set_ready_only_field(read_only=False)
        self.update_wizard_is_open_flag.emit(False)
        self.close()

    # (absWizardFactory)
    def rollback_in_layers_with_empty_editing_buffer(self):
        for layer_name in self._layers:
            if self._layers[layer_name] is not None:  # If the layer was removed, this becomes None
                if self._layers[layer_name].isEditable():
                    if not self._layers[layer_name].editBuffer().isModified():
                        self._layers[layer_name].rollBack()

    # (wizardFactory)
    def disconnect_signals(self):
        # if isinstance(self, SelectFeatureByExpressionDialogWrapper):
        self.disconnect_signals_of_feature_selector_buttons()
        self.__feature_selector_on_map.disconnect_signals()
        self.disconnect_signals_will_be_deleted()

        try:
            self._layers[self.EDITING_LAYER_NAME].committedFeaturesAdded.disconnect(self.finish_feature_creation)
        except:
            pass

    # (absWizardFactory)
    def finish_feature_creation(self, layerId, features):
        message = self.post_save(features)

        self._layers[self.EDITING_LAYER_NAME].committedFeaturesAdded.disconnect(self.finish_feature_creation)
        self.logger.info(__name__, "{} committedFeaturesAdded SIGNAL disconnected".format(self.WIZARD_FEATURE_NAME))
        self.close_wizard(message)

    def adjust_page_2_controls(self):
        self.button(self.FinishButton).setDisabled(True)
        self.wizardPage2.txt_help_page_2.setHtml(self.wizard_config[WIZARD_HELP_PAGES][WIZARD_HELP2])
        self.disconnect_signals()

        # Load layers
        result = self.prepare_feature_creation_layers()
        if result is None:
            self.close_wizard(show_message=False)

        # Check if a previous features are selected
        self.check_selected_features()

        # Register select features by expression
        # if isinstance(self, SelectFeatureByExpressionDialogWrapper):
        self.register_select_features_by_expression()

        # Register select features on map
        # if isinstance(self, SelectFeaturesOnMapWrapper):
        self.register_select_feature_on_map()

    def prepare_feature_creation_layers(self):
        # if isinstance(self, SelectFeaturesOnMapWrapper):
        # Add signal to check if a layer was removed
        self.connect_on_removing_layers()

        # All layers were successfully loaded
        return True

    # ------------------------------------------>>>  FINISH DIALOG
    def  finished_dialog(self):
        self.save_settings()

        if self.wizardPage1.enabled_refactor:
            self.__create_from_refactor()
        elif self.wizardPage1.enabled_create_manually:
            self.prepare_feature_creation()

    def __create_from_refactor(self):
        selected_layer = self.wizardPage1.selected_layer
        field_mapping = self.wizardPage1.field_mapping
        editing_layer_name = self.wizard_config[WIZARD_EDITING_LAYER_NAME]

        if selected_layer is not None:
            self.logic.create_from_refactor(selected_layer, editing_layer_name, field_mapping)
        else:
            self.logger.warning_msg(__name__, QCoreApplication.translate("WizardTranslations",
                "Select a source layer to set the field mapping to '{}'.").format(editing_layer_name))

        self.close_wizard()

    def save_settings(self):
        settings = QSettings()
        settings.setValue(self.wizard_config[WIZARD_QSETTINGS][WIZARD_QSETTINGS_LOAD_DATA_TYPE], 'create_manually' if self.wizardPage1.enabled_create_manually else 'refactor')

    # (absWizardFactory)
    def prepare_feature_creation(self):
        if self.prepare_feature_creation_layers():
            self.__manual_feature_creator.create_manually()
        else:
            self.close_wizard(show_message=False)

    # (absWizardFactory)
    def form_rejected(self):
        message = QCoreApplication.translate("WizardTranslations",
                                             "'{}' tool has been closed because you just closed the form.").format(self.WIZARD_TOOL_NAME)
        self.close_wizard(message)

    # (this class)
    def exec_form_advanced(self, layer):
        pass

    # ------------------------------------------>>>  SelectFeaturesOnMapWrapper
    # (map)
    def disconnect_signals_will_be_deleted(self):
        for layer_name in self._layers:
            try:
                self._layers[layer_name].willBeDeleted.disconnect(self.layer_removed)
            except:
                pass

    def map_tool_changed(self):
        message = QCoreApplication.translate("WizardTranslations",
                                             "'{}' tool has been closed because the map tool change.").format(self.WIZARD_TOOL_NAME)
        self.close_wizard(message)

    def connect_on_removing_layers(self):
        for layer_name in self._layers:
            if self._layers[layer_name]:
                # Layer was found, listen to its removal so that we can update the variable properly
                try:
                    self._layers[layer_name].willBeDeleted.disconnect(self.layer_removed)
                except:
                    pass
                self._layers[layer_name].willBeDeleted.connect(self.layer_removed)

    def layer_removed(self):
        message = QCoreApplication.translate("WizardTranslations",
                                             "'{}' tool has been closed because you just removed a required layer.").format(self.WIZARD_TOOL_NAME)
        self.close_wizard(message)

    def features_selected(self):
        self.setVisible(True)  # Make wizard appear
        self.check_selected_features()

    # ------------------------------------------>>> THIS CLASS
    def check_selected_features(self):
        # Check selected features in plot layer
        self.wizardPage2.lb_plot.setText(QCoreApplication.translate("WizardTranslations", "<b>Plot(s)</b>: {count} Feature(s) Selected").format(count=self._layers[self.names.LC_PLOT_T].selectedFeatureCount()))
        # Check selected features in boundary layer
        self.wizardPage2.lb_boundary.setText(QCoreApplication.translate("WizardTranslations", "<b>Boundary(ies)</b>: {count} Feature(s) Selected").format(count=self._layers[self.names.LC_BOUNDARY_T].selectedFeatureCount()))
        # Check selected features in boundary point layer
        self.wizardPage2.lb_boundary_point.setText(QCoreApplication.translate("WizardTranslations", "<b>Boundary</b>: {count} Feature(s) Selected").format(count=self._layers[self.names.LC_BOUNDARY_POINT_T].selectedFeatureCount()))
        # Check selected features in survey point layer
        self.wizardPage2.lb_survey_point.setText(QCoreApplication.translate("WizardTranslations", "<b>Survey</b>: {count} Feature(s) Selected").format(count=self._layers[self.names.LC_SURVEY_POINT_T].selectedFeatureCount()))
        # Check selected features in control point layer
        self.wizardPage2.lb_control_point.setText(QCoreApplication.translate("WizardTranslations", "<b>Control</b>: {count} Feature(s) Selected").format(count=self._layers[self.names.LC_CONTROL_POINT_T].selectedFeatureCount()))

        # Verifies that an feature has been selected
        if self._layers[self.names.LC_PLOT_T].selectedFeatureCount() + self._layers[self.names.LC_BOUNDARY_T].selectedFeatureCount() + self._layers[self.names.LC_BOUNDARY_POINT_T].selectedFeatureCount() + self._layers[self.names.LC_SURVEY_POINT_T].selectedFeatureCount() + self._layers[self.names.LC_CONTROL_POINT_T].selectedFeatureCount() >= 1:
            self.button(self.FinishButton).setDisabled(False)
        else:
            self.button(self.FinishButton).setDisabled(True)

    def disconnect_signals_of_feature_selector_buttons(self):
        signals = [self.wizardPage2.btn_plot_expression.clicked,
                   self.wizardPage2.btn_boundary_expression.clicked,
                   self.wizardPage2.btn_boundary_point_expression.clicked,
                   self.wizardPage2.btn_survey_point_expression.clicked,
                   self.wizardPage2.btn_control_point_expression.clicked,
                   self.wizardPage2.btn_plot_map.clicked,
                   self.wizardPage2.btn_boundary_map.clicked,
                   self.wizardPage2.btn_boundary_point_map.clicked,
                   self.wizardPage2.btn_survey_point_map.clicked,
                   self.wizardPage2.btn_control_point_map.clicked]

        for signal in signals:
            try:
                signal.disconnect()
            except:
                pass

    def register_select_features_by_expression(self):
        self.wizardPage2.btn_plot_expression.clicked.connect(partial(self.__feature_selector_by_expression.select_features_by_expression, self._layers[self.names.LC_PLOT_T]))
        self.wizardPage2.btn_boundary_expression.clicked.connect(partial(self.__feature_selector_by_expression.select_features_by_expression, self._layers[self.names.LC_BOUNDARY_T]))
        self.wizardPage2.btn_boundary_point_expression.clicked.connect(partial(self.__feature_selector_by_expression.select_features_by_expression, self._layers[self.names.LC_BOUNDARY_POINT_T]))
        self.wizardPage2.btn_survey_point_expression.clicked.connect(partial(self.__feature_selector_by_expression.select_features_by_expression, self._layers[self.names.LC_SURVEY_POINT_T]))
        self.wizardPage2.btn_control_point_expression.clicked.connect(partial(self.__feature_selector_by_expression.select_features_by_expression, self._layers[self.names.LC_CONTROL_POINT_T]))

    def register_select_feature_on_map(self):
        self.wizardPage2.btn_plot_map.clicked.connect(self.btn_plot_map_click)
        self.wizardPage2.btn_boundary_map.clicked.connect(self.btn_boundary_map_click)
        self.wizardPage2.btn_boundary_point_map.clicked.connect(self.btn_boundary_point_map_click)
        self.wizardPage2.btn_survey_point_map.clicked.connect(self.btn_survey_point_map_click)
        self.wizardPage2.btn_control_point_map.clicked.connect(self.btn_control_point_map_click)

    def btn_plot_map_click(self):
        self.setVisible(False)  # Make wizard disappear
        self.__feature_selector_on_map.select_features_on_map(self._layers[self.names.LC_PLOT_T])

    def btn_boundary_map_click(self):
        self.setVisible(False)  # Make wizard disappear
        self.__feature_selector_on_map.select_features_on_map(self._layers[self.names.LC_BOUNDARY_T])

    def btn_boundary_point_map_click(self):
        self.setVisible(False)  # Make wizard disappear
        self.__feature_selector_on_map.select_features_on_map(self._layers[self.names.LC_BOUNDARY_POINT_T])

    def btn_survey_point_map_click(self):
        self.setVisible(False)
        self.__feature_selector_on_map.select_features_on_map(self._layers[self.names.LC_SURVEY_POINT_T])

    def btn_control_point_map_click(self):
        self.setVisible(False)
        self.__feature_selector_on_map.select_features_on_map(self._layers[self.names.LC_CONTROL_POINT_T])

    def post_save(self, features):
        message = QCoreApplication.translate("WizardTranslations",
                                             "'{}' tool has been closed because an error occurred while trying to save the data.").format(self.WIZARD_TOOL_NAME)
        if len(features) != 1:
            message = QCoreApplication.translate("WizardTranslations", "'{}' tool has been closed. We should have got only one {} by we have {}").format(self.WIZARD_TOOL_NAME, self.WIZARD_FEATURE_NAME, len(features))
            self.logger.warning(__name__, "We should have got only one {}, but we have {}".format(self.WIZARD_FEATURE_NAME, len(features)))
        else:
            feature = features[0]
            feature_ids_dict = dict()

            if self._layers[self.names.LC_PLOT_T] is not None:
                if self._layers[self.names.LC_PLOT_T].selectedFeatureCount() > 0:
                    feature_ids_dict[self.names.LC_PLOT_T] = [f[self.names.T_ID_F] for f in self._layers[self.names.LC_PLOT_T].selectedFeatures()]

            if self._layers[self.names.LC_BOUNDARY_T] is not None:
                if self._layers[self.names.LC_BOUNDARY_T].selectedFeatureCount() > 0:
                    feature_ids_dict[self.names.LC_BOUNDARY_T] = [f[self.names.T_ID_F] for f in self._layers[self.names.LC_BOUNDARY_T].selectedFeatures()]

            if self._layers[self.names.LC_BOUNDARY_POINT_T] is not None:
                if self._layers[self.names.LC_BOUNDARY_POINT_T].selectedFeatureCount() > 0:
                    feature_ids_dict[self.names.LC_BOUNDARY_POINT_T] = [f[self.names.T_ID_F] for f in self._layers[self.names.LC_BOUNDARY_POINT_T].selectedFeatures()]

            if self._layers[self.names.LC_SURVEY_POINT_T] is not None:
                if self._layers[self.names.LC_SURVEY_POINT_T].selectedFeatureCount() > 0:
                    feature_ids_dict[self.names.LC_SURVEY_POINT_T] = [f[self.names.T_ID_F] for f in self._layers[self.names.LC_SURVEY_POINT_T].selectedFeatures()]

            if self._layers[self.names.LC_CONTROL_POINT_T] is not None:
                if self._layers[self.names.LC_CONTROL_POINT_T].selectedFeatureCount() > 0:
                    feature_ids_dict[self.names.LC_CONTROL_POINT_T] = [f[self.names.T_ID_F] for f in self._layers[self.names.LC_CONTROL_POINT_T].selectedFeatures()]

            if not feature.isValid():
                self.logger.warning(__name__, "Feature not found in layer Spatial Source...")
            else:
                spatial_source_id = feature[self.names.T_ID_F]
                all_new_features = list()

                # Fill association table, depending on the case
                new_features = list()
                if self.names.LC_PLOT_T in feature_ids_dict:
                    # Fill uesource table
                    for plot_id in feature_ids_dict[self.names.LC_PLOT_T]:
                        new_feature = QgsVectorLayerUtils().createFeature(self._layers[self.names.COL_UE_SOURCE_T])
                        new_feature.setAttribute(self.names.COL_UE_SOURCE_T_LC_PLOT_F, plot_id)
                        new_feature.setAttribute(self.names.COL_UE_SOURCE_T_SOURCE_F, spatial_source_id)
                        self.logger.info(__name__, "Saving Plot-SpatialSource: {}-{}".format(plot_id, spatial_source_id))
                        new_features.append(new_feature)

                    self._layers[self.names.COL_UE_SOURCE_T].dataProvider().addFeatures(new_features)
                    all_new_features.extend(new_feature)

                new_features = list()
                if self.names.LC_BOUNDARY_T in feature_ids_dict:
                    # Fill cclsource table
                    for boundary_id in feature_ids_dict[self.names.LC_BOUNDARY_T]:
                        new_feature = QgsVectorLayerUtils().createFeature(self._layers[self.names.COL_CCL_SOURCE_T])

                        # Todo: Update when ili2db issue is solved.
                        # Todo: When an abstract class only implements a concrete class, the name of the attribute is different if two or more classes are implemented.
                        new_feature.setAttribute(self.names.COL_CCL_SOURCE_T_BOUNDARY_F, boundary_id)
                        new_feature.setAttribute(self.names.COL_CCL_SOURCE_T_SOURCE_F, spatial_source_id)
                        self.logger.info(__name__, "Saving Boundary-SpatialSource: {}-{}".format(boundary_id, spatial_source_id))
                        new_features.append(new_feature)

                    self._layers[self.names.COL_CCL_SOURCE_T].dataProvider().addFeatures(new_features)
                    all_new_features.extend(new_feature)

                new_features = list()
                if self.names.LC_BOUNDARY_POINT_T in feature_ids_dict:
                    for boundary_point_id in feature_ids_dict[self.names.LC_BOUNDARY_POINT_T]:
                        new_feature = QgsVectorLayerUtils().createFeature(self._layers[self.names.COL_POINT_SOURCE_T])
                        new_feature.setAttribute(self.names.COL_POINT_SOURCE_T_LC_BOUNDARY_POINT_F, boundary_point_id)
                        new_feature.setAttribute(self.names.COL_POINT_SOURCE_T_SOURCE_F, spatial_source_id)
                        self.logger.info(__name__, "Saving BoundaryPoint-SpatialSource: {}-{}".format(boundary_point_id, spatial_source_id))
                        new_features.append(new_feature)

                    self._layers[self.names.COL_POINT_SOURCE_T].dataProvider().addFeatures(new_features)
                    all_new_features.extend(new_feature)

                new_features = list()
                if self.names.LC_SURVEY_POINT_T in feature_ids_dict:
                    for survey_point_id in feature_ids_dict[self.names.LC_SURVEY_POINT_T]:
                        new_feature = QgsVectorLayerUtils().createFeature(self._layers[self.names.COL_POINT_SOURCE_T])
                        new_feature.setAttribute(self.names.COL_POINT_SOURCE_T_LC_SURVEY_POINT_F, survey_point_id)
                        new_feature.setAttribute(self.names.COL_POINT_SOURCE_T_SOURCE_F, spatial_source_id)
                        self.logger.info(__name__, "Saving SurveyPoint-SpatialSource: {}-{}".format(survey_point_id, spatial_source_id))
                        new_features.append(new_feature)

                    self._layers[self.names.COL_POINT_SOURCE_T].dataProvider().addFeatures(new_features)
                    all_new_features.extend(new_feature)

                new_features = list()
                if self.names.LC_CONTROL_POINT_T in feature_ids_dict:
                    for control_point_id in feature_ids_dict[self.names.LC_CONTROL_POINT_T]:
                        new_feature = QgsVectorLayerUtils().createFeature(self._layers[self.names.COL_POINT_SOURCE_T])
                        new_feature.setAttribute(self.names.COL_POINT_SOURCE_T_LC_CONTROL_POINT_F, control_point_id)
                        new_feature.setAttribute(self.names.COL_POINT_SOURCE_T_SOURCE_F, spatial_source_id)
                        self.logger.info(__name__, "Saving ControlPoint-SpatialSource: {}-{}".format(control_point_id, spatial_source_id))
                        new_features.append(new_feature)

                    self._layers[self.names.COL_POINT_SOURCE_T].dataProvider().addFeatures(new_features)
                    all_new_features.extend(new_feature)

                if all_new_features:
                    message = QCoreApplication.translate("WizardTranslations",
                                                   "The new spatial source (t_id={}) was successfully created and associated with the following features: {}").format(spatial_source_id, feature_ids_dict)
                else:
                    message = QCoreApplication.translate("WizardTranslations",
                                                   "The new spatial source (t_id={}) was successfully created and it wasn't associated with a spatial unit").format(spatial_source_id)

        return message
