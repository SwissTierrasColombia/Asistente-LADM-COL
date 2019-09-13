# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-09-10
        git sha              : :%H$
        copyright            : (C) 2017 by Germán Carrillo
                               (C) 2018 by Sergio Ramírez (Incige SAS)
                               (C) 2018 by Jorge Useche (Incige SAS)
                               (C) 2018 by Jhon Galindo
                               (C) 2019 by Leo Cardona
        email                : gcarrillo@linuxmail.com
                               sergio.ramirez@incige.com
                               naturalmentejorge@gmail.com
                               jhonsigpjc@gmail.com
                               leo.cardona.p@gmail.com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
 """
from qgis.PyQt.QtCore import (QSettings,
                              QCoreApplication,
                              pyqtSignal)
from qgis.PyQt.QtWidgets import (QWizard,
                                 QPushButton,
                                 QMessageBox)
from qgis.core import (QgsApplication,
                       Qgis,
                       QgsProject)

from ...config.general_config import (PLUGIN_NAME,
                                      LAYER)
from ...config.help_strings import HelpStrings
from ...config.table_mapping_config import ID_FIELD
from ...config.wizards_settings import (WIZARD_HELP_SETTING,
                                        WIZARD_NAME_SETTING,
                                        WIZARD_FEATURE_NAME_SETTING,
                                        WIZARD_EDITING_LAYER_NAME_SETTING,
                                        WIZARD_UI_SETTING,
                                        WIZARD_MAP_LAYER_PROXY_MODEL,
                                        WIZARD_LAYERS_SETTING,
                                        WIZARD_QSETTINGS_SETTING,
                                        WIZARD_HELP_PAGES_SETTING,
                                        WIZARD_HELP_PAGE1,
                                        WIZARD_QSETTINGS_LOAD_DATA_TYPE)
from ...utils.ui import load_ui


class SinglePageSpatialWizardFactory(QWizard):
    set_wizard_is_open_emitted = pyqtSignal(bool)
    set_finalize_geometry_creation_enabled_emitted = pyqtSignal(bool)

    def __init__(self, iface, db, qgis_utils, wizard_settings):
        super(SinglePageSpatialWizardFactory, self).__init__()
        self.iface = iface
        self.log = QgsApplication.messageLog()
        self._db = db
        self.qgis_utils = qgis_utils
        self.wizard_config = wizard_settings
        self.help_strings = HelpStrings()

        load_ui(self.wizard_config[WIZARD_UI_SETTING], self)

        self.WIZARD_NAME = self.wizard_config[WIZARD_NAME_SETTING]
        self.WIZARD_FEATURE_NAME = self.wizard_config[WIZARD_FEATURE_NAME_SETTING]
        self.WIZARD_TOOL_NAME = 'Create {}'.format(self.wizard_config[WIZARD_FEATURE_NAME_SETTING])
        self.EDITING_LAYER_NAME = self.wizard_config[WIZARD_EDITING_LAYER_NAME_SETTING]
        self._layers = self.wizard_config[WIZARD_LAYERS_SETTING]

        self.restore_settings()
        self.rad_create_manually.toggled.connect(self.adjust_page_1_controls)
        self.adjust_page_1_controls()

        self.button(QWizard.FinishButton).clicked.connect(self.finished_dialog)
        self.button(QWizard.HelpButton).clicked.connect(self.show_help)
        self.rejected.connect(self.close_wizard)
        self.mMapLayerComboBox.setFilters(self.wizard_config[WIZARD_MAP_LAYER_PROXY_MODEL])

    def adjust_page_1_controls(self):
        self.cbo_mapping.clear()
        self.cbo_mapping.addItem("")
        self.cbo_mapping.addItems(self.qgis_utils.get_field_mappings_file_names(self.EDITING_LAYER_NAME))

        if self.rad_refactor.isChecked():
            self.lbl_refactor_source.setEnabled(True)
            self.mMapLayerComboBox.setEnabled(True)
            finish_button_text = QCoreApplication.translate(self.WIZARD_NAME, "Import")
            self.txt_help_page_1.setHtml(self.help_strings.get_refactor_help_string(self.EDITING_LAYER_NAME, False))
            self.lbl_field_mapping.setEnabled(True)
            self.cbo_mapping.setEnabled(True)
        elif self.rad_create_manually.isChecked():
            self.lbl_refactor_source.setEnabled(False)
            self.mMapLayerComboBox.setEnabled(False)
            finish_button_text = QCoreApplication.translate(self.WIZARD_NAME, "Create")
            self.txt_help_page_1.setHtml(self.wizard_config[WIZARD_HELP_PAGES_SETTING][WIZARD_HELP_PAGE1])
            self.lbl_field_mapping.setEnabled(False)
            self.cbo_mapping.setEnabled(False)

        self.wizardPage1.setButtonText(QWizard.FinishButton, finish_button_text)

    def finished_dialog(self):
        self.save_settings()

        if self.rad_refactor.isChecked():
            if self.mMapLayerComboBox.currentLayer() is not None:
                field_mapping = self.cbo_mapping.currentText()
                res_etl_model = self.qgis_utils.show_etl_model(self._db,
                                                               self.mMapLayerComboBox.currentLayer(),
                                                               self.EDITING_LAYER_NAME,
                                                               field_mapping=field_mapping)
                if res_etl_model: # Features were added?
                    # If the result of the etl_model is successful and we used a stored recent mapping, we delete the
                    # previous mapping used (we give preference to the latest used mapping)
                    if field_mapping:
                        self.qgis_utils.delete_old_field_mapping(field_mapping)

                    self.qgis_utils.save_field_mapping(self.EDITING_LAYER_NAME)
            else:
                self.qgis_utils.message_emitted.emit(
                    QCoreApplication.translate(self.WIZARD_NAME,
                                               "Select a source layer to set the field mapping to '{}'.").format(
                        self.EDITING_LAYER_NAME),
                    Qgis.Warning)

        elif self.rad_create_manually.isChecked():
            self.set_finalize_geometry_creation_enabled_emitted.emit(True)
            self.prepare_feature_creation()

    def prepare_feature_creation(self):
        result = self.prepare_feature_creation_layers()
        if result:
            self.edit_feature()
        else:
            self.close_wizard(show_message=False)

    def prepare_feature_creation_layers(self):
        is_loaded = self.required_layers_are_available()
        if not is_loaded:
            return False

        # Add signal to check if a layer was removed
        self.validate_remove_layers()

        # All layers were successfully loaded
        return True

    def required_layers_are_available(self):
        # Load layers
        self.qgis_utils.get_layers(self._db, self._layers, load=True)
        if not self._layers:
            self.qgis_utils.message_emitted.emit(
                QCoreApplication.translate(self.WIZARD_NAME,
                                           "'{}' tool has been closed because there was a problem loading the requeries layers.").format(
                    self.WIZARD_TOOL_NAME),
                Qgis.Warning)
            return False

        # Check if any layer is in editing mode
        layers_name = list()
        for layer in self._layers:
            if self._layers[layer][LAYER].isEditable():
                layers_name.append(self._db.get_ladm_layer_name(self._layers[layer][LAYER]))

        if layers_name:
            self.qgis_utils.message_emitted.emit(
                QCoreApplication.translate(self.WIZARD_NAME,
                                           "Wizard cannot be opened until the following layers are not in edit mode '{}'.").format(
                    '; '.join([layer_name for layer_name in layers_name])),
                Qgis.Warning)
            return False

        return True

    def close_wizard(self, message=None, show_message=True):
        if message is None:
            message = QCoreApplication.translate(self.WIZARD_NAME, "'{}' tool has been closed.").format(self.WIZARD_TOOL_NAME)
        if show_message:
            self.qgis_utils.message_emitted.emit(message, Qgis.Info)

        self.set_finalize_geometry_creation_enabled_emitted.emit(False)
        self.disconnect_signals()
        self.set_wizard_is_open_emitted.emit(False)
        self.close()

    def disconnect_signals(self):
        try:
            self._layers[self.EDITING_LAYER_NAME][LAYER].committedFeaturesAdded.disconnect(self.finish_feature_creation)
        except:
            pass

        for layer_name in self._layers:
            try:
                self._layers[layer_name][LAYER].willBeDeleted.disconnect(self.layer_removed)
            except:
                pass

    def edit_feature(self):
        self.iface.layerTreeView().setCurrentLayer(self._layers[self.EDITING_LAYER_NAME][LAYER])
        self._layers[self.EDITING_LAYER_NAME][LAYER].committedFeaturesAdded.connect(self.finish_feature_creation)

        # Disable transactions groups
        QgsProject.instance().setAutoTransaction(False)

        # Activate snapping
        self.qgis_utils.active_snapping_all_layers(tolerance=9)
        self.open_form(self._layers[self.EDITING_LAYER_NAME][LAYER])

        self.qgis_utils.message_emitted.emit(
            QCoreApplication.translate(self.WIZARD_NAME,
                                       "You can now start capturing boundary digitizing on the map..."), Qgis.Info)

    def finish_feature_creation(self, layerId, features):
        message = QCoreApplication.translate(self.WIZARD_NAME,
                                             "'{}' tool has been closed because an error occurred while trying to save the data.").format(self.WIZARD_TOOL_NAME)
        fid = features[0].id()

        if not self._layers[self.EDITING_LAYER_NAME][LAYER].getFeature(fid).isValid():
            message = QCoreApplication.translate(self.WIZARD_NAME,
                                                 "'{}' tool has been closed. Feature not found in layer {}... It's not posible create it. ").format(self.WIZARD_TOOL_NAME, self.EDITING_LAYER_NAME)
            self.log.logMessage("Feature not found in layer {} ...".format(self.EDITING_LAYER_NAME), PLUGIN_NAME, Qgis.Warning)
        else:
            feature_tid = self._layers[self.EDITING_LAYER_NAME][LAYER].getFeature(fid)[ID_FIELD]
            message = QCoreApplication.translate(self.WIZARD_NAME,
                                                 "The new {} (t_id={}) was successfully created ").format(self.WIZARD_FEATURE_NAME, feature_tid)

        self._layers[self.EDITING_LAYER_NAME][LAYER].committedFeaturesAdded.disconnect(self.finish_feature_creation)
        self.log.logMessage("{} committedFeaturesAdded SIGNAL disconnected".format(self.WIZARD_FEATURE_NAME), PLUGIN_NAME, Qgis.Info)
        self.close_wizard(message)

    def open_form(self, layer):
        if not layer.isEditable():
            layer.startEditing()

        self.qgis_utils.suppress_form(layer, True)
        self.iface.actionAddFeature().trigger()

    def exec_form(self, layer):
        self.set_finalize_geometry_creation_enabled_emitted.emit(False)

        for id, added_feature in layer.editBuffer().addedFeatures().items():
            feature = added_feature
            break

        dialog = self.iface.getFeatureForm(layer, feature)
        dialog.rejected.connect(self.form_rejected)
        dialog.setModal(True)

        if dialog.exec_():
            saved = layer.commitChanges()

            if not saved:
                layer.rollBack()
                self.qgis_utils.message_emitted.emit(
                    QCoreApplication.translate(self.WIZARD_NAME,
                                               "Error while saving changes. {} could not be created.").format(self.WIZARD_FEATURE_NAME), Qgis.Warning)
                for e in layer.commitErrors():
                    self.log.logMessage("Commit error: {}".format(e), PLUGIN_NAME, Qgis.Warning)
        else:
            layer.rollBack()
        self.iface.mapCanvas().refresh()

    def form_rejected(self):
        message = QCoreApplication.translate(self.WIZARD_NAME,
                                             "'{}' tool has been closed because you just closed the form.").format(self.WIZARD_TOOL_NAME)
        self.close_wizard(message)

    def save_settings(self):
        settings = QSettings()
        settings.setValue(self.wizard_config[WIZARD_QSETTINGS_SETTING][WIZARD_QSETTINGS_LOAD_DATA_TYPE], 'create_manually' if self.rad_create_manually.isChecked() else 'refactor')

    def restore_settings(self):
        settings = QSettings()

        load_data_type = settings.value(self.wizard_config[WIZARD_QSETTINGS_SETTING][WIZARD_QSETTINGS_LOAD_DATA_TYPE]) or 'create_manually'
        if load_data_type == 'refactor':
            self.rad_refactor.setChecked(True)
        else:
            self.rad_create_manually.setChecked(True)

    def show_help(self):
        self.qgis_utils.show_help(self.wizard_config[WIZARD_HELP_SETTING])

    def validate_remove_layers(self):
        for layer_name in self._layers:
            if self._layers[layer_name][LAYER]:
                # Layer was found, listen to its removal so that we can update the variable properly
                try:
                    self._layers[layer_name][LAYER].willBeDeleted.disconnect(self.layer_removed)
                except:
                    pass
                self._layers[layer_name][LAYER].willBeDeleted.connect(self.layer_removed)

    def layer_removed(self):
        message = QCoreApplication.translate(self.WIZARD_NAME,
                                             "'{}' tool has been closed because you just removed a required layer.").format(self.WIZARD_TOOL_NAME)
        self.close_wizard(message)

    def save_created_geometry(self):
        message = None
        if self._layers[self.EDITING_LAYER_NAME][LAYER].editBuffer():
            if len(self._layers[self.EDITING_LAYER_NAME][LAYER].editBuffer().addedFeatures()) == 1:
                feature = [value for index, value in self._layers[self.EDITING_LAYER_NAME][LAYER].editBuffer().addedFeatures().items()][0]
                if feature.geometry().isGeosValid():
                    self.exec_form(self._layers[self.EDITING_LAYER_NAME][LAYER])
                else:
                    message = QCoreApplication.translate(self.WIZARD_NAME, "The geometry is invalid. Do you want to return to the edit session?")
            else:
                if len(self._layers[self.EDITING_LAYER_NAME][LAYER].editBuffer().addedFeatures()) == 0:
                    message = QCoreApplication.translate(self.WIZARD_NAME, "No geometry has been created. Do you want to return to the edit session?")
                else:
                    message = QCoreApplication.translate(self.WIZARD_NAME, "Several geometries were created but only one was expected. Do you want to return to the edit session?")

        if message:
            self.show_message_associate_geometry_creation(message)

    def show_message_associate_geometry_creation(self, message):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Question)
        msg.setText(message)
        msg.setWindowTitle(QCoreApplication.translate(self.WIZARD_NAME, "Continue editing?"))
        msg.addButton(QPushButton(QCoreApplication.translate(self.WIZARD_NAME, "Yes")), QMessageBox.YesRole)
        msg.addButton(QPushButton(QCoreApplication.translate(self.WIZARD_NAME, "No, close the wizard")), QMessageBox.NoRole)
        reply = msg.exec_()

        if reply == 1: # 1 close wizard, 0 yes
            # stop edition in close_wizard crash qgis
            if self._layers[self.EDITING_LAYER_NAME][LAYER].isEditable():
                self._layers[self.EDITING_LAYER_NAME][LAYER].rollBack()

            message = QCoreApplication.translate(self.WIZARD_NAME, "'{}' tool has been closed.").format(
                self.WIZARD_TOOL_NAME)
            self.close_wizard(message)
        else:
            # Continue creating geometry
            pass
