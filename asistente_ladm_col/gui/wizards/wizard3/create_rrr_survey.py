from functools import partial

from qgis.PyQt.QtCore import (QCoreApplication,
                              QObject,
                              QSettings,
                              pyqtSignal)
from qgis.PyQt.QtWidgets import QWizard
from qgis.core import QgsMapLayerProxyModel
from qgis.core import QgsVectorLayerUtils
from asistente_ladm_col import Logger
from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.config.general_config import WIZARD_UI, WIZARD_FEATURE_NAME, WIZARD_TOOL_NAME, \
    WIZARD_EDITING_LAYER_NAME, WIZARD_LAYERS, WIZARD_READ_ONLY_FIELDS, WIZARD_HELP, WIZARD_HELP_PAGES, WIZARD_HELP1, \
    WIZARD_QSETTINGS, WIZARD_QSETTINGS_LOAD_DATA_TYPE, WIZARD_MAP_LAYER_PROXY_MODEL, WIZARD_HELP2, WIZARD_STRINGS
from asistente_ladm_col.config.help_strings import HelpStrings
from asistente_ladm_col.config.translation_strings import TranslatableConfigStrings
from asistente_ladm_col.gui.wizards.wizard_pages.asistente_wizard_page import AsistenteWizardPage
from asistente_ladm_col.gui.wizards.wizard_pages.logic import Logic
from asistente_ladm_col.gui.wizards.wizard_pages.select_source import SelectSource
from asistente_ladm_col.utils.qt_utils import disable_next_wizard, enable_next_wizard
from asistente_ladm_col.utils.ui import load_ui
from asistente_ladm_col.utils.utils import show_plugin_help
from qgis.gui import QgsExpressionSelectionDialog


class CreateRRRSurveyWizard(QWizard):

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
        # al no cargar la parte visual, se requiere cargar la segunda página
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

    # (absWizardFactory)
    def set_ready_only_field(self, read_only=True):
        if self._layers[self.EDITING_LAYER_NAME] is not None:
            for field in self.wizard_config[WIZARD_READ_ONLY_FIELDS]:
                # Not validate field that are read only
                self.app.core.set_read_only_field(self._layers[self.EDITING_LAYER_NAME], field, read_only)

    # (multiPageWizardFactory)
    def init_gui(self):
        # it creates the page (select source)
        self.wizardPage1 = SelectSource(self.logic.get_field_mappings_file_names(),
                                          self.logic.get_filters(), self.wizard_config[WIZARD_STRINGS])
        self.wizardPage1.option_changed.connect(self.adjust_page_1_controls)

        self.button(QWizard.NextButton).clicked.connect(self.adjust_page_2_controls)
        self.button(QWizard.FinishButton).clicked.connect(self.finished_dialog)
        self.button(QWizard.HelpButton).clicked.connect(self.show_help)
        self.rejected.connect(self.close_wizard)

        self.wizardPage2 = AsistenteWizardPage(self.wizard_config[WIZARD_UI])

        self.addPage(self.wizardPage1)
        self.addPage(self.wizardPage2)
        self.restore_settings()
        self.wizardPage1.controls_changed()

    # (absWizardFactory)
    def restore_settings(self):
        settings = QSettings()

        load_data_type = settings.value(self.wizard_config[WIZARD_QSETTINGS][WIZARD_QSETTINGS_LOAD_DATA_TYPE]) or 'create_manually'
        if load_data_type == 'refactor':
            self.wizardPage1.enabled_refactor = True
        else:
            self.wizardPage1.enabled_create_manually = True

    # (multiPageWizardFactory)
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

    # 2 init_gui   MODIFICADO !!!
    def close_wizard(self, message=None, show_message=True):
        if message is None:
            message = QCoreApplication.translate("WizardTranslations", "'{}' tool has been closed.").format(self.WIZARD_TOOL_NAME)
        if show_message:
            self.logger.info_msg(__name__, message)

        # if isinstance(self, SelectFeaturesOnMapWrapper):
        #    self.init_map_tool()

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

    # 3 close_wizard
    def disconnect_signals(self):
        # if isinstance(self, SelectFeatureByExpressionDialogWrapper):
        self.disconnect_signals_select_features_by_expression()

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

    # 2 init_gui ----- metodo create_rrr
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

    # 3 adjust_page_2_controls
    def prepare_feature_creation_layers(self):
        #   if isinstance of SelectFeaturesOnMapWrapper
        # Add signal to check if a layer was removed
        #  self.connect_on_removing_layers()

        # All layers were successfully loaded
        return True

    # ------------------------------------------>>>  FINISH DIALOG
    # (wizard factory)
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
        settings.setValue(self.wizard_config[WIZARD_QSETTINGS][WIZARD_QSETTINGS_LOAD_DATA_TYPE],
                          'create_manually' if self.wizardPage1.enabled_create_manually else 'refactor')

    # (absWizardFactory)
    def prepare_feature_creation(self):
        result = self.prepare_feature_creation_layers()
        if result:
            self.edit_feature()
        else:
            self.close_wizard(show_message=False)

    def edit_feature(self):
        # selecciona la capa
        self.iface.layerTreeView().setCurrentLayer(self._layers[self.EDITING_LAYER_NAME])
        # agrega el evento
        self._layers[self.EDITING_LAYER_NAME].committedFeaturesAdded.connect(self.finish_feature_creation)
        self.open_form(self._layers[self.EDITING_LAYER_NAME])

    # (wizardFactory)
    def open_form(self, layer):
        if not layer.isEditable():
            layer.startEditing()

        self.exec_form(layer)

    # (absWizardFactory)
    def exec_form(self, layer):
        feature = self.get_feature_exec_form(layer)
        dialog = self.iface.getFeatureForm(layer, feature)
        dialog.rejected.connect(self.form_rejected)
        dialog.setModal(True)

        if dialog.exec_():
            self.exec_form_advanced(layer)
            saved = layer.commitChanges()

            if not saved:
                layer.rollBack()
                self.logger.warning_msg(__name__, QCoreApplication.translate("WizardTranslations",
                    "Error while saving changes. {} could not be created.").format(self.WIZARD_FEATURE_NAME))
                for e in layer.commitErrors():
                    self.logger.warning(__name__, "Commit error: {}".format(e))
        else:
            layer.rollBack()
        self.iface.mapCanvas().refresh()

    # (wizard factory)
    def get_feature_exec_form(self, layer):
        return self.app.core.get_new_feature(layer)

    # (absWizardFactory)
    def form_rejected(self):
        message = QCoreApplication.translate("WizardTranslations",
                                             "'{}' tool has been closed because you just closed the form.").format(self.WIZARD_TOOL_NAME)
        self.close_wizard(message)

    # (this class)
    def exec_form_advanced(self, layer):
        pass

    # ------------------------------------------>>>  SelectFeatureByExpressionDialogWrapper
    def select_features_by_expression(self, layer):
        self.iface.setActiveLayer(layer)
        dlg_expression_selection = QgsExpressionSelectionDialog(layer)
        layer.selectionChanged.connect(self.check_selected_features)
        dlg_expression_selection.exec()
        layer.selectionChanged.disconnect(self.check_selected_features)

    # ------------------------------------------>>> THIS CLASS
    def check_selected_features(self):
        # Check selected features in administrative source layer
        if self._layers[self.names.LC_ADMINISTRATIVE_SOURCE_T].selectedFeatureCount():
            self.wizardPage2.lb_admin_source.setText(QCoreApplication.translate("WizardTranslations", "<b>Administrative Source(s)</b>: {count} Feature Selected").format(count=self._layers[self.names.LC_ADMINISTRATIVE_SOURCE_T].selectedFeatureCount()))
            self.button(self.FinishButton).setDisabled(False)
        else:
            self.wizardPage2.lb_admin_source.setText(QCoreApplication.translate("WizardTranslations", "<b>Administrative Source(s)</b>: 0 Features Selected"))
            self.button(self.FinishButton).setDisabled(True)

    def disconnect_signals_select_features_by_expression(self):
        signals = [self.wizardPage2.btn_expression.clicked]

        for signal in signals:
            try:
                signal.disconnect()
            except:
                pass

    def register_select_features_by_expression(self):
        self.wizardPage2.btn_expression.clicked.connect(partial(self.select_features_by_expression, self._layers[self.names.LC_ADMINISTRATIVE_SOURCE_T]))

    def post_save(self, features):
        message = QCoreApplication.translate("WizardTranslations",
                                             "'{}' tool has been closed because an error occurred while trying to save the data.").format(self.WIZARD_TOOL_NAME)

        if len(features) != 1:
            message = QCoreApplication.translate("WizardTranslations", "'{}' tool has been closed. We should have got only one {} by we have {}").format(self.WIZARD_TOOL_NAME, self.WIZARD_FEATURE_NAME, len(features))
            self.logger.warning(__name__, "We should have got only one {}, but we have {}".format(self.WIZARD_FEATURE_NAME, len(features)))
        else:
            fid = features[0].id()
            administrative_source_ids = [f[self.names.T_ID_F] for f in self._layers[self.names.LC_ADMINISTRATIVE_SOURCE_T].selectedFeatures()]

            if not self._layers[self.EDITING_LAYER_NAME].getFeature(fid).isValid():
                self.logger.warning(__name__, "Feature not found in layer {}...".format(self.EDITING_LAYER_NAME))
            else:
                # feature_rrr_id: generic name used for represent id for right, restriction
                feature_rrr_id = self._layers[self.EDITING_LAYER_NAME].getFeature(fid)[self.names.T_ID_F]

                # Fill rrrfuente table
                new_features = []
                for administrative_source_id in administrative_source_ids:
                    new_feature = QgsVectorLayerUtils().createFeature(self._layers[self.names.COL_RRR_SOURCE_T])

                    new_feature.setAttribute(self.names.COL_RRR_SOURCE_T_SOURCE_F, administrative_source_id)
                    if self.EDITING_LAYER_NAME == self.names.LC_RIGHT_T:
                        new_feature.setAttribute(self.names.COL_RRR_SOURCE_T_LC_RIGHT_F, feature_rrr_id)
                    elif self.EDITING_LAYER_NAME == self.names.LC_RESTRICTION_T:
                        new_feature.setAttribute(self.names.COL_RRR_SOURCE_T_LC_RESTRICTION_F, feature_rrr_id)

                    self.logger.info(__name__, "Saving Administrative_source-{}: {}-{}".format(self.WIZARD_FEATURE_NAME, administrative_source_id, feature_rrr_id))
                    new_features.append(new_feature)

                self._layers[self.names.COL_RRR_SOURCE_T].dataProvider().addFeatures(new_features)
                message = QCoreApplication.translate("WizardTranslations","The new {} (t_id={}) was successfully created and associated with its corresponding administrative source (t_id={})!").format(self.WIZARD_FEATURE_NAME, feature_rrr_id, ", ".join([str(b) for b in administrative_source_ids]))

        return message
