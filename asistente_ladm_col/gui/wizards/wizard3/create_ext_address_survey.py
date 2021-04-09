from functools import partial

from qgis.PyQt.QtCore import (QCoreApplication,
                              QObject,
                              QSettings,
                              pyqtSignal)
from qgis.gui import QgsExpressionSelectionDialog

from qgis.PyQt.QtWidgets import QWizard, QMessageBox
from asistente_ladm_col import Logger
from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.config.general_config import WIZARD_UI, WIZARD_FEATURE_NAME, WIZARD_TOOL_NAME, \
    WIZARD_EDITING_LAYER_NAME, WIZARD_LAYERS, WIZARD_READ_ONLY_FIELDS, WIZARD_HELP, WIZARD_HELP_PAGES, WIZARD_HELP1, \
    WIZARD_QSETTINGS, WIZARD_QSETTINGS_LOAD_DATA_TYPE, WIZARD_MAP_LAYER_PROXY_MODEL, DEFAULT_SRS_AUTHID, \
    CSS_COLOR_INACTIVE_LABEL, CSS_COLOR_OKAY_LABEL, CSS_COLOR_ERROR_LABEL, WIZARD_HELP2, WIZARD_HELP3, WIZARD_STRINGS
from asistente_ladm_col.config.help_strings import HelpStrings
from asistente_ladm_col.config.translation_strings import TranslatableConfigStrings
from asistente_ladm_col.gui.wizards.abc.signal_disconnectable import SignalDisconnectableMetaWiz
from asistente_ladm_col.gui.wizards.wizard_pages.asistente_wizard_page import AsistenteWizardPage
from asistente_ladm_col.gui.wizards.wizard_pages.create_manually_spatial import CreateManuallySpatial
from asistente_ladm_col.gui.wizards.wizard_pages.logic import Logic
from asistente_ladm_col.gui.wizards.wizard_pages.select_features_by_expression_dialog_wrapper import \
    SelectFeatureByExpressionDialogWrapper
from asistente_ladm_col.gui.wizards.wizard_pages.select_features_on_map_wrapper import SelectFeaturesOnMapWrapper
from asistente_ladm_col.gui.wizards.wizard_pages.select_source import SelectSource
from asistente_ladm_col.utils.crs_utils import get_crs_authid
from asistente_ladm_col.utils.qt_utils import disable_next_wizard, enable_next_wizard

from asistente_ladm_col.utils.utils import show_plugin_help


class CreateExtAddressSurveyWizard(QWizard, metaclass=SignalDisconnectableMetaWiz):
    update_wizard_is_open_flag = pyqtSignal(bool)
    set_finalize_geometry_creation_enabled_emitted = pyqtSignal(bool)

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

        self.WIZARD_FEATURE_NAME = self.wizard_config[WIZARD_FEATURE_NAME]
        self.WIZARD_TOOL_NAME = self.wizard_config[WIZARD_TOOL_NAME]
        self.EDITING_LAYER_NAME = self.wizard_config[WIZARD_EDITING_LAYER_NAME]
        self._layers = self.wizard_config[WIZARD_LAYERS]

        self.logic = Logic(self.app, db, self._layers, wizard_settings)

        self.set_ready_only_field()

        self.wizardPage1 = None
        self.wizardPage2 = None
        self.init_gui()

        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++>>>>> map interaction expansion
        # TODO Remove?
        self.canvas = self.iface.mapCanvas()
        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++>>>>> SpatialWizardFactory
        self.set_disable_digitize_actions()
        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++>>>>> map tool
        self.logger = Logger()
        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++>>>>> this class
        self._current_layer = None

        self.__init_new_items()

    def __init_new_items(self):
        self.__manual_feature_creator = \
            CreateManuallySpatial(self.iface, self.app, self.logger,
                                  self._layers[self.EDITING_LAYER_NAME],
                                  self.WIZARD_FEATURE_NAME)

        self.__manual_feature_creator.register_observer(self)

        # map
        self.__feature_selector_on_map = SelectFeaturesOnMapWrapper(self.iface, self.logger, False)
        self.__feature_selector_on_map.register_observer(self)

        self.__feature_selector_by_expression = SelectFeatureByExpressionDialogWrapper(self.iface)
        self.__feature_selector_by_expression.register_observer(self)

    # (absWizardFactory)
    def set_ready_only_field(self, read_only=True):
        if self._layers[self.EDITING_LAYER_NAME] is not None:
            for field in self.wizard_config[WIZARD_READ_ONLY_FIELDS]:
                # Not validate field that are read only
                self.app.core.set_read_only_field(self._layers[self.EDITING_LAYER_NAME], field, read_only)

    # (multiPageSpatialWizard)
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
        self.wizardPage1.layer_changed.connect(self.import_layer_changed)

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

    # (multiPageSpatialWizard)
    def adjust_page_1_controls(self):
        finish_button_text = ''

        if self.wizardPage1.enabled_refactor:
            disable_next_wizard(self)
            self.wizardPage1.setFinalPage(True)
            finish_button_text = QCoreApplication.translate("WizardTranslations", "Import")
            self.wizardPage1.set_help_text(self.help_strings.get_refactor_help_string(self._db, self._layers[self.EDITING_LAYER_NAME]))
            self.wizardPage1.setButtonText(QWizard.FinishButton, finish_button_text)
            self.import_layer_changed(self.wizardPage1.selected_layer)
        elif self.wizardPage1.enabled_create_manually:
            self.wizardPage1.setFinalPage(False)
            enable_next_wizard(self)
            self.wizardPage1.setFinalPage(False)
            self.wizardPage1.lbl_refactor_source.setStyleSheet('')
            finish_button_text = QCoreApplication.translate("WizardTranslations", "Create")
            self.wizardPage1.set_help_text(self.wizard_config[WIZARD_HELP_PAGES][WIZARD_HELP1])

        self.wizardPage2.setButtonText(QWizard.FinishButton, finish_button_text)

    # (absWizardFactory)
    def show_help(self):
        show_plugin_help(self.wizard_config[WIZARD_HELP])

    # (spatial_wizard_Factory)
    def close_wizard(self, message=None, show_message=True):
        if message is None:
            message = QCoreApplication.translate("WizardTranslations", "'{}' tool has been closed.").format(self.WIZARD_TOOL_NAME)
        if show_message:
            self.logger.info_msg(__name__, message)

        self.__feature_selector_on_map.init_map_tool()

        self.rollback_in_layers_with_empty_editing_buffer()
        self.set_finalize_geometry_creation_enabled_emitted.emit(False)
        self.disconnect_signals()
        self.set_ready_only_field(read_only=False)
        self.set_disable_digitize_actions(visible=True)
        self.update_wizard_is_open_flag.emit(False)
        self.close()

    # (absWizardFactory)
    def rollback_in_layers_with_empty_editing_buffer(self):
        for layer_name in self._layers:
            if self._layers[layer_name] is not None:  # If the layer was removed, this becomes None
                if self._layers[layer_name].isEditable():
                    if not self._layers[layer_name].editBuffer().isModified():
                        self._layers[layer_name].rollBack()

    # (spatialWizardFactory)
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

    # (this class)
    def adjust_page_2_controls(self):
        self.button(self.FinishButton).setDisabled(True)
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

        self.wizardPage2.rad_to_plot.toggled.connect(self.toggle_spatial_unit)
        self.wizardPage2.rad_to_building.toggled.connect(self.toggle_spatial_unit)
        self.wizardPage2.rad_to_building_unit.toggled.connect(self.toggle_spatial_unit)
        self.toggle_spatial_unit()

    # (spatialWizardFactory)
    def prepare_feature_creation_layers(self):
        self.connect_on_removing_layers()

        # All layers were successfully loaded
        return True

    # (MapInteractionExpansion)
    def connect_on_removing_layers(self):
        for layer_name in self._layers:
            if self._layers[layer_name]:
                # Layer was found, listen to its removal so that we can update the variable properly
                try:
                    self._layers[layer_name].willBeDeleted.disconnect(self.layer_removed)
                except:
                    pass
                self._layers[layer_name].willBeDeleted.connect(self.layer_removed)

    # ------------------------------------------>>>  FINISH DIALOG
    # (spatialWizardFactory)
    def finished_dialog(self):
        self.save_settings()

        if self.wizardPage1.enabled_refactor:
            self.__create_from_refactor()
        elif self.wizardPage1.enabled_create_manually:
            self.set_finalize_geometry_creation_enabled_emitted.emit(True)
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

    # (absWizardFactory)
    def save_settings(self):
        settings = QSettings()
        settings.setValue(self.wizard_config[WIZARD_QSETTINGS][WIZARD_QSETTINGS_LOAD_DATA_TYPE], 'create_manually' if self.wizardPage1.enabled_create_manually else 'refactor')

    # (absWizardFactory)
    def prepare_feature_creation(self):
        self.connect_on_removing_layers()

        if self._current_layer.selectedFeatureCount() != 1:
            self.logger.warning_msg(__name__,
                QCoreApplication.translate("WizardTranslations",
                                           "First select a {}.").format(self._db.get_ladm_layer_name(self._current_layer)), Qgis.Warning)
            return

        self.__manual_feature_creator.create_manually()

    # (absWizardFactory)
    def form_rejected(self):
        message = QCoreApplication.translate("WizardTranslations", "'{}' tool has been closed because you just closed the form.").format(self.WIZARD_TOOL_NAME)
        self.close_wizard(message)

    def dialog_succeed(self, dialog_succeed_params):
        layer = dialog_succeed_params["layer"]

        for f in layer.editBuffer().addedFeatures():
            feature = layer.editBuffer().addedFeatures()[f]
            break

        spatial_unit_field_idx = None
        if feature:
            # Get t_id of spatial unit to associate
            feature_id = self._current_layer.selectedFeatures()[0][self.names.T_ID_F]
            fid = feature.id()

            if self._db.get_ladm_layer_name(self._current_layer) == self.names.LC_PLOT_T:
                spatial_unit_field_idx = layer.getFeature(fid).fieldNameIndex(self.names.EXT_ADDRESS_S_LC_PLOT_F)
            elif self._db.get_ladm_layer_name(self._current_layer) == self.names.LC_BUILDING_T:
                spatial_unit_field_idx = layer.getFeature(fid).fieldNameIndex(self.names.EXT_ADDRESS_S_LC_BUILDING_F)
            elif self._db.get_ladm_layer_name(self._current_layer) == self.names.LC_BUILDING_UNIT_T:
                spatial_unit_field_idx = layer.getFeature(fid).fieldNameIndex(self.names.EXT_ADDRESS_S_LC_BUILDING_UNIT_F)

        if spatial_unit_field_idx:
            # assign the relation with the spatial unit
            layer.changeAttributeValue(fid, spatial_unit_field_idx, feature_id)
        else:
            # if the field of the spatial unit does not exist
            layer.rollBack()
            message = QCoreApplication.translate("WizardTranslations",
                                                 "'{}' tool has been closed because when try to create {} it was not possible to associate a space unit.").format(self.WIZARD_TOOL_NAME, self.EDITING_LAYER_NAME)
            self.close_wizard(message)

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

    # map
    def features_selected(self):
        self.setVisible(True)  # Make wizard appear
        self.check_selected_features()

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++>>>>> map interaction expansion
    # (map interaction expansion)
    def set_disable_digitize_actions(self, visible=False):
        self.iface.actionToggleEditing().setVisible(visible)

        self.iface.actionSaveActiveLayerEdits().setVisible(visible)
        self.iface.actionSaveAllEdits().setVisible(visible)
        self.iface.actionSaveEdits().setVisible(visible)

        self.iface.actionAllEdits().setVisible(visible)
        self.iface.actionCancelAllEdits().setVisible(visible)
        self.iface.actionCancelEdits().setVisible(visible)

        self.iface.actionRollbackAllEdits().setVisible(visible)
        self.iface.actionRollbackEdits().setVisible(visible)

    def layer_removed(self):
        message = QCoreApplication.translate("WizardTranslations",
                                             "'{}' tool has been closed because you just removed a required layer.").format(self.WIZARD_TOOL_NAME)
        self.close_wizard(message)

    def save_created_geometry(self):
        self.__manual_feature_creator.save_created_geometry()

    def show_message_associate_geometry_creation(self, message, layer):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Question)
        msg.setText(message)
        msg.setWindowTitle(QCoreApplication.translate("WizardTranslations", "Continue editing?"))
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.button(QMessageBox.No).setText(QCoreApplication.translate("WizardTranslations", "No, close the wizard"))
        reply = msg.exec_()

        if reply == QMessageBox.No:
            # stop edition in close_wizard crash qgis
            if layer.isEditable():
                layer.rollBack()

            message = QCoreApplication.translate("WizardTranslations", "'{}' tool has been closed.").format(
                self.WIZARD_TOOL_NAME)
            self.close_wizard(message)
        else:
            # Continue creating geometry
            pass

    # ----------------------------------++++++++++++++++++++++++++++++++++++++++++++-------->>> THIS CLASS
    def toggle_spatial_unit(self):

        self.wizardPage2.btn_plot_map.setEnabled(False)
        self.wizardPage2.btn_building_map.setEnabled(False)
        self.wizardPage2.btn_building_unit_map.setEnabled(False)

        self.wizardPage2.btn_plot_expression.setEnabled(False)
        self.wizardPage2.btn_building_expression.setEnabled(False)
        self.wizardPage2.btn_building_unit_expression.setEnabled(False)

        if self.wizardPage2.rad_to_plot.isChecked():
            self.wizardPage2.txt_help_page_2.setHtml(self.wizard_config[WIZARD_HELP_PAGES][WIZARD_HELP1])
            self._current_layer = self._layers[self.names.LC_PLOT_T]

            self.wizardPage2.btn_plot_map.setEnabled(True)
            self.wizardPage2.btn_plot_expression.setEnabled(True)

        elif self.wizardPage2.rad_to_building.isChecked():
            self.wizardPage2.txt_help_page_2.setHtml(self.wizard_config[WIZARD_HELP_PAGES][WIZARD_HELP2])
            self.wizardPage2._current_layer = self._layers[self.names.LC_BUILDING_T]

            self.wizardPage2.btn_building_map.setEnabled(True)
            self.wizardPage2.btn_building_expression.setEnabled(True)

        elif self.wizardPage2.rad_to_building_unit.isChecked():
            self.wizardPage2.txt_help_page_2.setHtml(self.wizard_config[WIZARD_HELP_PAGES][WIZARD_HELP3])
            self._current_layer = self._layers[self.names.LC_BUILDING_UNIT_T]

            self.wizardPage2.btn_building_unit_map.setEnabled(True)
            self.wizardPage2.btn_building_unit_expression.setEnabled(True)

        self.iface.setActiveLayer(self._current_layer)
        self.check_selected_features()

    def check_selected_features(self):
        self.wizardPage2.rad_to_plot.setText(QCoreApplication.translate("WizardTranslations", "Plot(s): {count} Feature(s) Selected").format(count=self._layers[self.names.LC_PLOT_T].selectedFeatureCount()))
        self.wizardPage2.rad_to_building.setText(QCoreApplication.translate("WizardTranslations", "Building(s): {count} Feature(s) Selected").format(count=self._layers[self.names.LC_BUILDING_T].selectedFeatureCount()))
        self.wizardPage2.rad_to_building_unit.setText(QCoreApplication.translate("WizardTranslations", "Building unit(s): {count} Feature(s) Selected").format(count=self._layers[self.names.LC_BUILDING_UNIT_T].selectedFeatureCount()))

        if self._current_layer is None:
            if self._db.get_ladm_layer_name(self.iface.activeLayer()) == self.names.LC_PLOT_T:
                self.wizardPage2.rad_to_plot.setChecked(True)
                self._current_layer = self._layers[self.names.LC_PLOT_T]
            elif self._db.get_ladm_layer_name(self.iface.activeLayer()) == self.names.LC_BUILDING_T:
                self.wizardPage2.rad_to_building.setChecked(True)
                self._current_layer = self._layers[self.names.LC_BUILDING_T]
            elif self._db.get_ladm_layer_name(self.iface.activeLayer()) == self.names.LC_BUILDING_UNIT_T:
                self.wizardPage2.rad_to_building_unit.setChecked(True)
                self._current_layer = self._layers[self.names.LC_BUILDING_UNIT_T]
            else:
                # Select layer that have least one feature selected
                # as current layer when current layer is not defined
                if self._layers[self.names.LC_PLOT_T].selectedFeatureCount():
                    self.wizardPage2.rad_to_plot.setChecked(True)
                    self._current_layer = self._layers[self.names.LC_PLOT_T]
                elif self._layers[self.names.LC_BUILDING_T].selectedFeatureCount():
                    self.wizardPage2.rad_to_building.setChecked(True)
                    self._current_layer = self._layers[self.names.LC_BUILDING_T]
                elif self._layers[self.names.LC_BUILDING_UNIT_T].selectedFeatureCount():
                    self.wizardPage2.rad_to_building_unit.setChecked(True)
                    self._current_layer = self._layers[self.names.LC_BUILDING_UNIT_T]
                else:
                    # By default current_layer will be plot layer
                    self.wizardPage2.rad_to_plot.setChecked(True)
                    self._current_layer = self._layers[self.names.LC_PLOT_T]

        if self.wizardPage2.rad_to_plot.isChecked():
            self.wizardPage2.rad_to_building.setStyleSheet(CSS_COLOR_INACTIVE_LABEL)
            self.wizardPage2.rad_to_building_unit.setStyleSheet(CSS_COLOR_INACTIVE_LABEL)

            # Check selected features in plot layer
            if self._layers[self.names.LC_PLOT_T].selectedFeatureCount() == 1:
                self.wizardPage2.rad_to_plot.setStyleSheet(CSS_COLOR_OKAY_LABEL)
            elif self._layers[self.names.LC_PLOT_T].selectedFeatureCount() > 1:
                # the color of the text is changed to highlight when there are more than one feature selected
                self.wizardPage2.rad_to_plot.setStyleSheet(CSS_COLOR_ERROR_LABEL)
            else:
                # the color of the text is changed to highlight that there is no selection
                self.wizardPage2.rad_to_plot.setStyleSheet(CSS_COLOR_ERROR_LABEL)

        elif self.wizardPage2.rad_to_building.isChecked():
            self.wizardPage2.rad_to_plot.setStyleSheet(CSS_COLOR_INACTIVE_LABEL)
            self.wizardPage2.rad_to_building_unit.setStyleSheet(CSS_COLOR_INACTIVE_LABEL)

            # Check selected features in building layer
            if self._layers[self.names.LC_BUILDING_T].selectedFeatureCount() == 1:
                self.wizardPage2.rad_to_building.setStyleSheet(CSS_COLOR_OKAY_LABEL)
            elif self._layers[self.names.LC_BUILDING_T].selectedFeatureCount() > 1:
                # the color of the text is changed to highlight when there are more than one feature selected
                self.wizardPage2.rad_to_building.setStyleSheet(CSS_COLOR_ERROR_LABEL)
            else:
                # the color of the text is changed to highlight that there is no selection
                self.wizardPage2.rad_to_building.setStyleSheet(CSS_COLOR_ERROR_LABEL)

        elif self.wizardPage2.rad_to_building_unit.isChecked():
            self.wizardPage2.rad_to_plot.setStyleSheet(CSS_COLOR_INACTIVE_LABEL)
            self.wizardPage2.rad_to_building.setStyleSheet(CSS_COLOR_INACTIVE_LABEL)

            # Check selected features in building unit layer
            if self._layers[self.names.LC_BUILDING_UNIT_T].selectedFeatureCount() == 1:
                self.wizardPage2.rad_to_building_unit.setStyleSheet(CSS_COLOR_OKAY_LABEL)
            elif self._layers[self.names.LC_BUILDING_UNIT_T].selectedFeatureCount() > 1:
                # the color of the text is changed to highlight when there are more than one features selected
                self.wizardPage2.rad_to_building_unit.setStyleSheet(CSS_COLOR_ERROR_LABEL)
            else:
                # the color of the text is changed to highlight that there is no selection
                self.wizardPage2.rad_to_building_unit.setStyleSheet(CSS_COLOR_ERROR_LABEL)

        # Zoom to selected feature
        self.canvas.zoomToSelected(self._current_layer)

        # Condition for enabling the finish button
        if self.wizardPage2.rad_to_plot.isChecked() and self._layers[self.names.LC_PLOT_T].selectedFeatureCount() == 1:
            self.button(self.FinishButton).setDisabled(False)
        elif self.wizardPage2.rad_to_building.isChecked() and self._layers[self.names.LC_BUILDING_T].selectedFeatureCount() == 1:
            self.button(self.FinishButton).setDisabled(False)
        elif self.wizardPage2.rad_to_building_unit.isChecked() and self._layers[self.names.LC_BUILDING_UNIT_T].selectedFeatureCount() == 1:
            self.button(self.FinishButton).setDisabled(False)
        else:
            self.button(self.FinishButton).setDisabled(True)

    def disconnect_signals_of_feature_selector_buttons(self):
        signals = [self.wizardPage2.btn_plot_expression.clicked,
                   self.wizardPage2.btn_building_expression.clicked,
                   self.wizardPage2.btn_building_unit_expression.clicked,
                   self.wizardPage2.btn_plot_map.clicked,
                   self.wizardPage2.btn_building_map.clicked,
                   self.wizardPage2.btn_building_unit_map.clicked]

        for signal in signals:
            try:
                signal.disconnect()
            except:
                pass

    def register_select_features_by_expression(self):
        self.wizardPage2.btn_plot_expression.clicked.connect(partial(self.__feature_selector_by_expression.select_features_by_expression, self._layers[self.names.LC_PLOT_T]))
        self.wizardPage2.btn_building_expression.clicked.connect(partial(self.__feature_selector_by_expression.select_features_by_expression, self._layers[self.names.LC_BUILDING_T]))
        self.wizardPage2.btn_building_unit_expression.clicked.connect(partial(self.__feature_selector_by_expression.select_features_by_expression, self._layers[self.names.LC_BUILDING_UNIT_T]))

    def register_select_feature_on_map(self):
        self.wizardPage2.btn_plot_map.clicked.connect(self.btn_plot_map_click)
        self.wizardPage2.btn_building_map.clicked.connect(self.btn_building_map_click)
        self.wizardPage2.btn_building_unit_map.clicked.connect(self.btn_building_unit_map_click)

    def __call_feature_on_map_selector(self, layer):
        self.setVisible(False)  # Make wizard disappear
        self._current_layer = layer
        self.__feature_selector_on_map.select_features_on_map(layer)

    def btn_plot_map_click(self):
        self.__call_feature_on_map_selector(self._layers[self.names.LC_PLOT_T])

    def btn_building_map_click(self):
        self.__call_feature_on_map_selector(self._layers[self.names.LC_BUILDING_T])

    def btn_building_unit_map_click(self):
        self.__call_feature_on_map_selector(self._layers[self.names.LC_BUILDING_UNIT_T])

    def post_save(self, features):
        message = QCoreApplication.translate("WizardTranslations",
                                             "'{}' tool has been closed because an error occurred while trying to save the data.").format(self.WIZARD_TOOL_NAME)
        if len(features) != 1:
            message = QCoreApplication.translate("WizardTranslations", "'{}' tool has been closed. We should have got only one {} by we have {}").format(self.WIZARD_TOOL_NAME, self.WIZARD_FEATURE_NAME, len(features))
            self.logger.warning(__name__, "We should have got only one {}, but we have {}".format(self.WIZARD_FEATURE_NAME, len(features)))
        else:
            fid = features[0].id()

            if not self._layers[self.EDITING_LAYER_NAME].getFeature(fid).isValid():
                message = QCoreApplication.translate("WizardTranslations",
                                                     "'{}' tool has been closed. Feature not found in layer {}... It's not posible create it. ").format(self.WIZARD_TOOL_NAME, self.EDITING_LAYER_NAME)
                self.logger.warning(__name__, "Feature not found in layer {} ...".format(self.EDITING_LAYER_NAME))
            else:
                extaddress_tid = self._layers[self.EDITING_LAYER_NAME].getFeature(fid)[self.names.T_ID_F]
                message = QCoreApplication.translate("WizardTranslations",
                                                     "The new {} (t_id={}) was successfully created ").format(self.WIZARD_FEATURE_NAME, extaddress_tid)
        return message

    # (spatialWizardFactory)
    def import_layer_changed(self, layer):
        if layer:
            crs = get_crs_authid(layer.crs())
            if crs != DEFAULT_SRS_AUTHID:
                self.wizardPage1.lbl_refactor_source.setStyleSheet('color: orange')
                self.wizardPage1.lbl_refactor_source.setToolTip(QCoreApplication.translate("WizardTranslations",
                                                                               "This layer will be reprojected for you to '{}' (Colombian National Origin),<br>before attempting to import it into LADM-COL.").format(
                    DEFAULT_SRS_AUTHID))
            else:
                self.wizardPage1.lbl_refactor_source.setStyleSheet('')
                self.wizardPage1.lbl_refactor_source.setToolTip('')

    def feature_for_dialog_getting(self, feature_params):
        pass

    def geometry_finalized(self, finalized_geometry_params):
        is_geometry_finalized = finalized_geometry_params["finalized"]
        self.set_finalize_geometry_creation_enabled_emitted.emit(is_geometry_finalized)

    def invalid_geometry(self, invalid_geometry_params):
        layer = invalid_geometry_params['layer']
        message = QCoreApplication.translate("WizardTranslations", "The geometry is invalid. Do you want to return to the edit session?")

        self.show_message_associate_geometry_creation(message, layer)

    def zero_or_many_features_added(self, zero_or_many_features_added_params):
        features_amount = zero_or_many_features_added_params['len_features_added']
        layer = zero_or_many_features_added_params['layer']

        if features_amount == 0:
            message = QCoreApplication.translate("WizardTranslations",
                                                 "No geometry has been created. Do you want to return to the edit session?")
        else:
            message = QCoreApplication.translate("WizardTranslations",
                                                 "Several geometries were created but only one was expected. Do you want to return to the edit session?")

        self.show_message_associate_geometry_creation(message, layer)
