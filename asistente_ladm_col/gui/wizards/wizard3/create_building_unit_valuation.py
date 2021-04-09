from functools import partial

from qgis.PyQt.QtCore import (QCoreApplication,
                              QObject,
                              QSettings,
                              pyqtSignal)
from qgis.PyQt.QtWidgets import QWizard, QMessageBox
from qgis.core import QgsMapLayerProxyModel, QgsVectorLayerUtils, QgsVectorLayerUtils, QgsGeometry
from asistente_ladm_col import Logger
from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.config.general_config import WIZARD_UI, WIZARD_FEATURE_NAME, WIZARD_TOOL_NAME, \
    WIZARD_EDITING_LAYER_NAME, WIZARD_LAYERS, WIZARD_READ_ONLY_FIELDS, WIZARD_HELP, WIZARD_HELP_PAGES, WIZARD_HELP1, \
    WIZARD_QSETTINGS, WIZARD_QSETTINGS_LOAD_DATA_TYPE, WIZARD_MAP_LAYER_PROXY_MODEL, WIZARD_HELP2, CSS_COLOR_OKAY_LABEL, \
    CSS_COLOR_ERROR_LABEL
from asistente_ladm_col.config.help_strings import HelpStrings
from asistente_ladm_col.config.ladm_names import LADMNames
from asistente_ladm_col.config.translation_strings import TranslatableConfigStrings
from asistente_ladm_col.gui.wizards.wizard_pages.create_manually import CreateManually
from asistente_ladm_col.gui.wizards.wizard_pages.select_features_by_expression_dialog_wrapper import \
    SelectFeatureByExpressionDialogWrapper
from asistente_ladm_col.gui.wizards.wizard_pages.select_features_on_map_wrapper import SelectFeaturesOnMapWrapper
from asistente_ladm_col.utils.qt_utils import disable_next_wizard, enable_next_wizard
from asistente_ladm_col.utils.ui import load_ui
from asistente_ladm_col.utils.utils import show_plugin_help


class CreateBuildingUnitValuationWizard(QWizard):
    update_wizard_is_open_flag = pyqtSignal(bool)

    def __init__(self, iface, db, wizard_settings):
        print('aoeaoe')
        QWizard.__init__(self)
        self.iface = iface
        self._db = db
        self.wizard_config = wizard_settings

        self.logger = Logger()
        self.app = AppInterface()

        self.names = self._db.names
        self.help_strings = HelpStrings()
        self.translatable_config_strings = TranslatableConfigStrings()
        load_ui(self.wizard_config[WIZARD_UI], self)

        self.WIZARD_FEATURE_NAME = self.wizard_config[WIZARD_FEATURE_NAME]
        self.WIZARD_TOOL_NAME = self.wizard_config[WIZARD_TOOL_NAME]
        self.EDITING_LAYER_NAME = self.wizard_config[WIZARD_EDITING_LAYER_NAME]
        self._layers = self.wizard_config[WIZARD_LAYERS]
        self.set_ready_only_field()

        self.init_gui()

        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++>>>>> map tool
        self.logger = Logger()

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

    # (absWizardFactory)
    def set_ready_only_field(self, read_only=True):
        if self._layers[self.EDITING_LAYER_NAME] is not None:
            for field in self.wizard_config[WIZARD_READ_ONLY_FIELDS]:
                # Not validate field that are read only
                self.app.core.set_read_only_field(self._layers[self.EDITING_LAYER_NAME], field, read_only)

    # (multiPageWizardFactory)
    def init_gui(self):
        self.restore_settings()
        self.rad_create_manually.toggled.connect(self.adjust_page_1_controls)
        self.adjust_page_1_controls()

        self.button(QWizard.NextButton).clicked.connect(self.adjust_page_2_controls)
        self.button(QWizard.FinishButton).clicked.connect(self.finished_dialog)
        self.button(QWizard.HelpButton).clicked.connect(self.show_help)
        self.rejected.connect(self.close_wizard)
        self.mMapLayerComboBox.setFilters(QgsMapLayerProxyModel.Filter(self.wizard_config[WIZARD_MAP_LAYER_PROXY_MODEL]))

    # (absWizardFactory)
    def restore_settings(self):
        settings = QSettings()

        load_data_type = settings.value(self.wizard_config[WIZARD_QSETTINGS][WIZARD_QSETTINGS_LOAD_DATA_TYPE]) or 'create_manually'
        if load_data_type == 'refactor':
            self.rad_refactor.setChecked(True)
        else:
            self.rad_create_manually.setChecked(True)

    # (multiPageWizardFactory)
    def adjust_page_1_controls(self):
        self.cbo_mapping.clear()
        self.cbo_mapping.addItem("")
        self.cbo_mapping.addItems(self.app.core.get_field_mappings_file_names(self.EDITING_LAYER_NAME))

        if self.rad_refactor.isChecked():
            self.lbl_refactor_source.setEnabled(True)
            self.mMapLayerComboBox.setEnabled(True)
            self.lbl_field_mapping.setEnabled(True)
            self.cbo_mapping.setEnabled(True)
            disable_next_wizard(self)
            self.wizardPage1.setFinalPage(True)
            finish_button_text = QCoreApplication.translate("WizardTranslations", "Import")
            self.txt_help_page_1.setHtml(self.help_strings.get_refactor_help_string(self._db, self._layers[self.EDITING_LAYER_NAME]))
            self.wizardPage1.setButtonText(QWizard.FinishButton, finish_button_text)
        elif self.rad_create_manually.isChecked():
            self.lbl_refactor_source.setEnabled(False)
            self.mMapLayerComboBox.setEnabled(False)
            self.lbl_field_mapping.setEnabled(False)
            self.cbo_mapping.setEnabled(False)
            enable_next_wizard(self)
            self.wizardPage1.setFinalPage(False)
            finish_button_text = QCoreApplication.translate("WizardTranslations", "Create")
            self.txt_help_page_1.setHtml(self.wizard_config[WIZARD_HELP_PAGES][WIZARD_HELP1])

        self.wizardPage2.setButtonText(QWizard.FinishButton, finish_button_text)

    # (absWizardFactory)
    def show_help(self):
        show_plugin_help(self.wizard_config[WIZARD_HELP])

    # (wizardFactory)
    def close_wizard(self, message=None, show_message=True):
        if message is None:
            message = QCoreApplication.translate("WizardTranslations", "'{}' tool has been closed.").format(self.WIZARD_TOOL_NAME)
        if show_message:
            self.logger.info_msg(__name__, message)

        #if isinstance(self, SelectFeaturesOnMapWrapper):
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

    # (multiPageWizardFactory)
    def adjust_page_2_controls(self):
        self.button(self.FinishButton).setDisabled(True)
        self.txt_help_page_2.setHtml(self.wizard_config[WIZARD_HELP_PAGES][WIZARD_HELP2])
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

    # (wizardFactory)
    def prepare_feature_creation_layers(self):
        # Add signal to check if a layer was removed
        self.connect_on_removing_layers()

        # All layers were successfully loaded
        return True

    # ------------------------------------------>>>  FINISH DIALOG
    # (wizard factory)
    def  finished_dialog(self):
        self.save_settings()

        if self.rad_refactor.isChecked():
            if self.mMapLayerComboBox.currentLayer() is not None:
                field_mapping = self.cbo_mapping.currentText()
                res_etl_model = self.app.core.show_etl_model(self._db,
                                                               self.mMapLayerComboBox.currentLayer(),
                                                               self.EDITING_LAYER_NAME,
                                                               field_mapping=field_mapping)
                if res_etl_model: # Features were added?
                    self.app.gui.redraw_all_layers()  # Redraw all layers to show imported data

                    # If the result of the etl_model is successful and we used a stored recent mapping, we delete the
                    # previous mapping used (we give preference to the latest used mapping)
                    if field_mapping:
                        self.app.core.delete_old_field_mapping(field_mapping)

                    self.app.core.save_field_mapping(self.EDITING_LAYER_NAME)
            else:
                self.logger.warning_msg(__name__, QCoreApplication.translate("WizardTranslations",
                    "Select a source layer to set the field mapping to '{}'.").format(self.EDITING_LAYER_NAME))

            self.close_wizard()

        elif self.rad_create_manually.isChecked():
            self.prepare_feature_creation()

    # (absWizardFactory)
    def save_settings(self):
        settings = QSettings()
        settings.setValue(self.wizard_config[WIZARD_QSETTINGS][WIZARD_QSETTINGS_LOAD_DATA_TYPE], 'create_manually' if self.rad_create_manually.isChecked() else 'refactor')

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

    # (map)
    def map_tool_changed(self, new_tool, old_tool):
        message = QCoreApplication.translate("WizardTranslations",
                                             "'{}' tool has been closed because the map tool change.").format(self.WIZARD_TOOL_NAME)
        self.close_wizard(message)

    # (map)
    def connect_on_removing_layers(self):
        for layer_name in self._layers:
            if self._layers[layer_name]:
                # Layer was found, listen to its removal so that we can update the variable properly
                try:
                    self._layers[layer_name].willBeDeleted.disconnect(self.layer_removed)
                except:
                    pass
                self._layers[layer_name].willBeDeleted.connect(self.layer_removed)

    # (map)
    def layer_removed(self):
        message = QCoreApplication.translate("WizardTranslations",
                                             "'{}' tool has been closed because you just removed a required layer.").format(self.WIZARD_TOOL_NAME)
        self.close_wizard(message)

    # map
    def features_selected(self):
        self.setVisible(True)  # Make wizard appear
        self.check_selected_features()

    # ------------------------------------------>>> THIS CLASS
    def check_selected_features(self):
        _count = self._layers[self.names.LC_BUILDING_UNIT_T].selectedFeatureCount()
        self.lb_info.setText(QCoreApplication.translate("WizardTranslations", "<b>Building unit(s)</b>: {count} Feature(s) Selected").format(count=_count))
        self.lb_info.setStyleSheet(CSS_COLOR_OKAY_LABEL)  # Default color

        if _count != 1:
            _color = CSS_COLOR_ERROR_LABEL
            self.lb_info.setStyleSheet(_color)
        self.button(self.FinishButton).setEnabled(_count == 1)

    def disconnect_signals_of_feature_selector_buttons(self):
        signals = [self.wizardPage2.btn_expression.clicked, self.wizardPage2.btn_map.clicked]

        for signal in signals:
            try:
                signal.disconnect()
            except:
                pass

    def register_select_features_by_expression(self):
        self.wizardPage2.btn_expression.clicked.connect(partial(self.__feature_selector_by_expression.select_features_by_expression, self._layers[self.names.LC_BUILDING_UNIT_T]))

    def register_select_feature_on_map(self):
        self.wizardPage2.btn_map.clicked.connect(self.btn_map_click)

    def btn_map_click(self):
        self.setVisible(False)  # Make wizard disappear
        self.__feature_selector_on_map.select_features_on_map(self._layers[self.names.LC_BUILDING_UNIT_T])

    def post_save(self, features):
        message = QCoreApplication.translate("WizardTranslations",
                                             "'{}' tool has been closed because an error occurred while trying to save the data.").format(self.WIZARD_TOOL_NAME)
        if len(features) != 1:
            message = QCoreApplication.translate("WizardTranslations", "'{}' tool has been closed. We should have got only one {} by we have {}").format(self.WIZARD_TOOL_NAME, self.WIZARD_FEATURE_NAME, len(features))
            self.logger.warning(__name__, "We should have got only one {}, but we have {}".format(self.WIZARD_FEATURE_NAME, len(features)))
        else:
            fid = features[0].id()
            building_unit_ids = [f[self.names.T_ID_F] for f in self._layers[self.names.LC_BUILDING_UNIT_T].selectedFeatures()]

            if not self._layers[self.EDITING_LAYER_NAME].getFeature(fid).isValid():
                self.logger.warning(__name__, "Feature not found in layer {}...".format(self.EDITING_LAYER_NAME))
            else:
                building_unit_valuation_id = self._layers[self.EDITING_LAYER_NAME].getFeature(fid)[self.names.T_ID_F]

                # Fill avaluounidadconstruccion table
                new_features = []
                for building_unit_id in building_unit_ids:
                    new_feature = QgsVectorLayerUtils().createFeature(self._layers[LADMNames.AVALUOUNIDADCONSTRUCCION_TABLE])
                    new_feature.setAttribute(LADMNames.AVALUOUNIDADCONSTRUCCION_TABLE_BUILDING_UNIT_FIELD, building_unit_id)
                    new_feature.setAttribute(LADMNames.AVALUOUNIDADCONSTRUCCION_TABLE_BUILDING_UNIT_VALUATION_FIELD, building_unit_valuation_id)
                    self.logger.info(__name__, "Saving Building unit-Building unit valuation: {}-{}".format(building_unit_id, building_unit_valuation_id))
                    new_features.append(new_feature)

                self._layers[LADMNames.AVALUOUNIDADCONSTRUCCION_TABLE].dataProvider().addFeatures(new_features)
                if building_unit_ids:
                    message = QCoreApplication.translate("WizardTranslations", "The new {} (t_id={}) was successfully created and associated with its corresponding building unit (t_id={})!").format(self.WIZARD_FEATURE_NAME, building_unit_valuation_id, building_unit_ids[0])

        return message
