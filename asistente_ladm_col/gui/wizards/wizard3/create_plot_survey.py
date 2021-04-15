from functools import partial
from qgis.core import Qgis
from qgis.PyQt.QtCore import (QCoreApplication,
                              QObject,
                              QSettings,
                              pyqtSignal)
from qgis.PyQt.QtWidgets import QWizard, QMessageBox
from qgis.core import QgsMapLayerProxyModel, QgsVectorLayerUtils, QgsVectorLayerUtils, QgsGeometry
from asistente_ladm_col import Logger
from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.config.general_config import WIZARD_UI, WIZARD_FEATURE_NAME, \
    WIZARD_EDITING_LAYER_NAME, WIZARD_LAYERS, WIZARD_READ_ONLY_FIELDS, WIZARD_HELP, WIZARD_HELP_PAGES, WIZARD_HELP1, \
    WIZARD_QSETTINGS, WIZARD_QSETTINGS_LOAD_DATA_TYPE, WIZARD_HELP2, CSS_COLOR_OKAY_LABEL, \
    CSS_COLOR_ERROR_LABEL, WIZARD_STRINGS, WIZARD_TOOL_NAME
from asistente_ladm_col.config.help_strings import HelpStrings
from asistente_ladm_col.config.translation_strings import TranslatableConfigStrings
from asistente_ladm_col.gui.wizards.view.plot_survey_view import PlotSurveyView
from asistente_ladm_col.gui.wizards.view.view_enum import EnumTypeOfOption
from asistente_ladm_col.gui.wizards.view.view_params import FeatureSelectedParams
from asistente_ladm_col.gui.wizards.wizard_pages.asistente_wizard_page import AsistenteWizardPage
from asistente_ladm_col.gui.wizards.wizard_pages.logic import Logic
from asistente_ladm_col.gui.wizards.wizard_pages.select_features_by_expression_dialog_wrapper import \
    SelectFeatureByExpressionDialogWrapper
from asistente_ladm_col.gui.wizards.wizard_pages.select_features_on_map_wrapper import SelectFeaturesOnMapWrapper
from asistente_ladm_col.gui.wizards.wizard_pages.select_source import SelectSource
from asistente_ladm_col.utils.qt_utils import disable_next_wizard, enable_next_wizard
from asistente_ladm_col.utils.utils import show_plugin_help
from qgis.gui import QgsExpressionSelectionDialog


class CreatePlotSurveyWizard(QWizard):
    update_wizard_is_open_flag = pyqtSignal(bool)

    def __init__(self, iface, db, wizard_settings):
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


        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++>>>>> map tool
        self.logger = Logger()

        self.__init_new_items()

        # TODO Change the name
        self.__selectable_layers_by_type = None
        self.__init_selectable_layer_by_type()
        self.init_gui()

    def __init_new_items(self):
        # map
        self.__feature_selector_on_map = SelectFeaturesOnMapWrapper(self.iface, self.logger)
        self.__feature_selector_on_map.register_observer(self)

        self.__feature_selector_by_expression = SelectFeatureByExpressionDialogWrapper(self.iface)
        self.__feature_selector_by_expression.register_observer(self)

    # TODO Change the name
    def __init_selectable_layer_by_type(self):
        # TODO Change the name
        self.__selectable_layers_by_type = dict()
        self.__selectable_layers_by_type[EnumTypeOfOption.BOUNDARY] = self._layers[self.names.LC_BOUNDARY_T]

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

        self.__init_wizard_page()
        self.wizardPage1.controls_changed()

        self.__set_feature_count()
        self.__update_selected_feature_info(None)

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

    # it was overrided
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

        # unico cambio
        self.setButtonText(QWizard.FinishButton, finish_button_text)

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
        self.wizardPage2.disconnect_signals()
        self.__disconnect_signals_no_gui()

    def __disconnect_signals_no_gui(self):
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
        self.__disconnect_signals_no_gui()

        # Load layers
        result = self.prepare_feature_creation_layers()
        if result is None:
            self.close_wizard(show_message=False)

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
        result = self.prepare_feature_creation_layers()
        if result:
            self.edit_feature()
        else:
            self.close_wizard(show_message=False)

    # sobrecargado
    def edit_feature(self):
        if self._layers[self.names.LC_BOUNDARY_T].selectedFeatureCount() > 0:
            # Open Form
            self.iface.layerTreeView().setCurrentLayer(self._layers[self.EDITING_LAYER_NAME])
            self.app.core.active_snapping_all_layers()
            self.create_plots_from_boundaries()
        else:
            self.logger.warning_msg(__name__, QCoreApplication.translate("WizardTranslations", "First select boundaries!"))

    # No hay open-form
    # ------------------------------------------>>>  SelectFeatureByExpressionDialogWrapper         ACA ACKA ACA
    def select_features_by_expression(self, layer):
        self.iface.setActiveLayer(layer)
        dlg_expression_selection = QgsExpressionSelectionDialog(layer)
        layer.selectionChanged.connect(self.check_selected_features)
        dlg_expression_selection.exec()
        layer.selectionChanged.disconnect(self.check_selected_features)

    # ------------------------------------------>>>  SelectFeaturesOnMapWrapper
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
        self.__set_feature_count()
        self.__update_selected_feature_info(None)

    def create_plots_from_boundaries(self):
        selected_boundaries = self._layers[self.names.LC_BOUNDARY_T].selectedFeatures()

        boundary_geometries = [f.geometry() for f in selected_boundaries]
        collection = QgsGeometry().polygonize(boundary_geometries)
        features = list()
        for polygon in collection.asGeometryCollection():
            feature = QgsVectorLayerUtils().createFeature(self._layers[self.EDITING_LAYER_NAME], polygon)
            features.append(feature)

        if features:
            if not self._layers[self.EDITING_LAYER_NAME].isEditable():
                self._layers[self.EDITING_LAYER_NAME].startEditing()

            self._layers[self.EDITING_LAYER_NAME].addFeatures(features)
            self.iface.mapCanvas().refresh()

            message = QCoreApplication.translate("WizardTranslations", "{} new plot(s) has(have) been created! To finish the creation of the plots, open its attribute table and fill in the mandatory fields.").format(len(features))
            button_text = QCoreApplication.translate("WizardTranslations", "Open table of attributes")
            level = Qgis.Info
            layer = self._layers[self.EDITING_LAYER_NAME]
            filter = '"{}" is Null'.format(self.names.LC_PLOT_T_PLOT_AREA_F)
            self.logger.message_with_button_open_table_attributes_emitted.emit(message, button_text, level, layer, filter)
            self.close_wizard(show_message=False)
        else:
            message = QCoreApplication.translate("WizardTranslations", "No plot could be created. Make sure selected boundaries are closed!")
            self.close_wizard(message)

    def post_save(self, features):
        pass

    # wizardPage2
    def feature_by_map_selected(self, feature_selected_params: FeatureSelectedParams):
        layer = self.__selectable_layers_by_type[feature_selected_params.selected_type]
        self.setVisible(False)  # Make wizard disappear
        self.__feature_selector_on_map.select_features_on_map(layer)

    def feature_by_expression_selected(self, feature_selected_params: FeatureSelectedParams):
        layer = self.__selectable_layers_by_type[feature_selected_params.selected_type]
        self.__feature_selector_by_expression.select_features_by_expression(layer)

    def all_feature_selected(self, feature_selected_params: FeatureSelectedParams):
        layer = self.__selectable_layers_by_type[feature_selected_params.selected_type]
        layer.selectAll()
        self.check_selected_features()

    def __init_wizard_page(self):
        help_text = self.wizard_config[WIZARD_HELP_PAGES][WIZARD_HELP2]
        self.wizardPage2 = PlotSurveyView(self, help_text)

    def __set_feature_count(self):
        feature_count = dict()

        for layer in self.__selectable_layers_by_type:
            feature_count[layer] = self.__selectable_layers_by_type[layer].selectedFeatureCount()

        self.wizardPage2.set_feature_count(feature_count)

    def __update_selected_feature_info(self, selected_type):
        is_any_feature_selected = self.__is_any_feature_selected()

        _color = CSS_COLOR_OKAY_LABEL if is_any_feature_selected else CSS_COLOR_ERROR_LABEL
        self.wizardPage2.set_selected_item_style(_color)
        self.button(self.FinishButton).setDisabled(not is_any_feature_selected)

    def __is_any_feature_selected(self):
        return self._layers[self.names.LC_BOUNDARY_T].selectedFeatureCount() > 0