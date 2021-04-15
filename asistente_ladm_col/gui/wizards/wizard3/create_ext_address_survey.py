from functools import partial

from qgis.PyQt.QtCore import (QCoreApplication,
                              QObject,
                              QSettings,
                              pyqtSignal)

from qgis.PyQt.QtWidgets import QWizard, QMessageBox
from asistente_ladm_col import Logger
from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.config.general_config import WIZARD_FEATURE_NAME, WIZARD_TOOL_NAME, \
    WIZARD_EDITING_LAYER_NAME, WIZARD_LAYERS, WIZARD_READ_ONLY_FIELDS, WIZARD_HELP, WIZARD_HELP_PAGES, WIZARD_HELP1, \
    WIZARD_QSETTINGS, WIZARD_QSETTINGS_LOAD_DATA_TYPE, DEFAULT_SRS_AUTHID, \
    CSS_COLOR_OKAY_LABEL, CSS_COLOR_ERROR_LABEL, WIZARD_HELP2, WIZARD_HELP3, WIZARD_STRINGS
from asistente_ladm_col.config.help_strings import HelpStrings
from asistente_ladm_col.config.translation_strings import TranslatableConfigStrings
from asistente_ladm_col.gui.wizards.abc.signal_disconnectable import SignalDisconnectableMetaWiz
from asistente_ladm_col.gui.wizards.view.ext_address_survey_view import ExtAddressSurveyView
from asistente_ladm_col.gui.wizards.view.view_enum import EnumTypeOfOption
from asistente_ladm_col.gui.wizards.view.view_params import FeatureSelectedParams, OptionChangedParams
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

        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++>>>>> map interaction expansion
        # TODO Remove?
        self.canvas = self.iface.mapCanvas()
        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++>>>>> SpatialWizardFactory
        self.set_disable_digitize_actions()
        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++>>>>> this class
        self._current_layer = None

        self.__init_new_items()

        self.__selectable_layers_by_type = None
        self.__init_selectable_layer_by_type()

        self.init_gui()

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

    def __init_selectable_layer_by_type(self):
        self.__selectable_layers_by_type = dict()
        self.__selectable_layers_by_type[EnumTypeOfOption.PLOT] = self._layers[self.names.LC_PLOT_T]
        self.__selectable_layers_by_type[EnumTypeOfOption.BUILDING] = self._layers[self.names.LC_BUILDING_T]
        self.__selectable_layers_by_type[EnumTypeOfOption.BUILDING_UNIT] = self._layers[self.names.LC_BUILDING_UNIT_T]

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

        self.wizardPage1.controls_changed()
        self.wizardPage1.layer_changed.connect(self.import_layer_changed)

        self.__init_wizard_page_2()
        self.__initialize_selected_option()
        self.__set_feature_count()

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

        self.setButtonText(QWizard.FinishButton, finish_button_text)

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

    # (this class)
    def adjust_page_2_controls(self):
        self.button(self.FinishButton).setDisabled(True)
        self.__disconnect_signals_no_gui()

        # Load layers
        result = self.prepare_feature_creation_layers()
        if result is None:
            self.close_wizard(show_message=False)

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
    def check_selected_features(self):
        self.__set_feature_count()
        self.__update_selected_feature_info(self.wizardPage2.selected_type)
        self.canvas.zoomToSelected(self._current_layer)

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

    # wizardPage2
    def __init_wizard_page_2(self):
        help_texts = dict()
        help_texts[EnumTypeOfOption.PLOT] = self.wizard_config[WIZARD_HELP_PAGES][WIZARD_HELP1]
        help_texts[EnumTypeOfOption.BUILDING] = self.wizard_config[WIZARD_HELP_PAGES][WIZARD_HELP2]
        help_texts[EnumTypeOfOption.BUILDING_UNIT] = self.wizard_config[WIZARD_HELP_PAGES][WIZARD_HELP3]

        self.wizardPage2 = ExtAddressSurveyView(self, help_texts)

    def feature_by_map_selected(self, feature_selected_params: FeatureSelectedParams):
        self._current_layer = self.__selectable_layers_by_type[feature_selected_params.selected_type]
        self.setVisible(False)  # Make wizard disappear
        self.__feature_selector_on_map.select_features_on_map(self._current_layer)

    def feature_by_expression_selected(self, feature_selected_params: FeatureSelectedParams):
        self._current_layer = self.__selectable_layers_by_type[feature_selected_params.selected_type]
        self.__feature_selector_by_expression.select_features_by_expression(self._current_layer)

    def option_changed(self, option_changed_params: OptionChangedParams):
        self.__update_selected_feature_info(option_changed_params.selected_type)
        self.canvas.zoomToSelected(self._current_layer)

    def __update_selected_feature_info(self, selected_type):
        disable_finish_button = True

        if self.__selectable_layers_by_type[selected_type].selectedFeatureCount() == 1:
            selected_option_style = CSS_COLOR_OKAY_LABEL
            disable_finish_button = False
        elif self._layers[self.names.LC_BUILDING_UNIT_T].selectedFeatureCount() > 1:
            # the color of the text is changed to highlight when there are more than one features selected
            selected_option_style = CSS_COLOR_ERROR_LABEL
        else:
            # the color of the text is changed to highlight that there is no selection
            selected_option_style = CSS_COLOR_ERROR_LABEL
        self.wizardPage2.set_selected_item_style(selected_option_style)
        self.button(self.FinishButton).setDisabled(disable_finish_button)

    def __initialize_selected_option(self):
        is_option_selected = self.__select_option_base_on_active_layer()

        if not is_option_selected:
            is_option_selected = self.__select_option_base_on_layer_with_features()

        if not is_option_selected:
            self.__select_option_default_layer()

    def __set_feature_count(self):
        feature_count = dict()

        for layer in self.__selectable_layers_by_type:
            feature_count[layer] = self.__selectable_layers_by_type[layer].selectedFeatureCount()

        self.wizardPage2.set_feature_count(feature_count)

    # --
    def __select_option_base_on_active_layer(self):
        is_option_selected = False
        for item_type in self.__selectable_layers_by_type:
            if self.__selectable_layers_by_type[item_type] == self.iface.activeLayer():
                self.wizardPage2.selected_type = item_type
                is_option_selected = True
                break
        return is_option_selected

    def __select_option_base_on_layer_with_features(self):
        # Select layer that have least one feature selected
        # as current layer when current layer is not defined
        is_option_selected = False

        for item_type in self.__selectable_layers_by_type:
            if self.__selectable_layers_by_type[item_type].selectedFeatureCount():
                self.wizardPage2.selected_type = item_type
                self._current_layer = self.__selectable_layers_by_type[item_type]
                is_option_selected = True
                break

        return is_option_selected

    def __select_option_default_layer(self):
        # By default current_layer will be plot layer
        self.wizardPage2.selected_type = EnumTypeOfOption.PLOT
        self._current_layer = self._layers[self.names.LC_PLOT_T]
