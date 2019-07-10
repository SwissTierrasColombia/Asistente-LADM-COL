# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2018-09-06
        git sha              : :%H$
        copyright            : (C) 2018 by Germán Carrillo
        email                : gcarrillo@linuxmail.com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import (QCoreApplication,
                              QSettings)
from qgis.PyQt.QtWidgets import QWizard
from qgis.core import (QgsApplication,
                       Qgis,
                       QgsMapLayerProxyModel)

from ....config.general_config import (PLUGIN_NAME,
                                       LAYER)
from ....config.help_strings import HelpStrings
from ....config.table_mapping_config import (ID_FIELD,
                                             LEGAL_PARTY_TABLE)
from ....utils import get_ui_class

WIZARD_UI = get_ui_class('wizards/property_record_card/wiz_create_legal_party_prc.ui')


class CreateLegalPartyPRCWizard(QWizard, WIZARD_UI):
    WIZARD_NAME = "CreateLegalPartyWizard"
    WIZARD_TOOL_NAME = QCoreApplication.translate(WIZARD_NAME, "Create legal party")

    def __init__(self, iface, db, qgis_utils, parent=None):
        QWizard.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self.log = QgsApplication.messageLog()
        self._db = db
        self.qgis_utils = qgis_utils
        self.help_strings = HelpStrings()

        self._layers = {
            LEGAL_PARTY_TABLE: {'name': LEGAL_PARTY_TABLE, 'geometry': None, LAYER: None}
        }

        self.restore_settings()
        self.rad_create_manually.toggled.connect(self.adjust_page_1_controls)
        self.adjust_page_1_controls()

        self.button(QWizard.FinishButton).clicked.connect(self.finished_dialog)
        self.button(QWizard.HelpButton).clicked.connect(self.show_help)
        self.rejected.connect(self.close_wizard)
        self.mMapLayerComboBox.setFilters(QgsMapLayerProxyModel.NoGeometry)

    def adjust_page_1_controls(self):
        self.cbo_mapping.clear()
        self.cbo_mapping.addItem("")
        self.cbo_mapping.addItems(self.qgis_utils.get_field_mappings_file_names(LEGAL_PARTY_TABLE))

        if self.rad_refactor.isChecked():
            self.lbl_refactor_source.setEnabled(True)
            self.mMapLayerComboBox.setEnabled(True)
            finish_button_text = QCoreApplication.translate(self.WIZARD_NAME, "Import")
            self.txt_help_page_1.setHtml(self.help_strings.get_refactor_help_string(LEGAL_PARTY_TABLE, False))
            self.lbl_field_mapping.setEnabled(True)
            self.cbo_mapping.setEnabled(True)
        elif self.rad_create_manually.isChecked():
            self.lbl_refactor_source.setEnabled(False)
            self.mMapLayerComboBox.setEnabled(False)
            finish_button_text = QCoreApplication.translate(self.WIZARD_NAME, "Create")
            self.txt_help_page_1.setHtml(self.help_strings.WIZ_CREATE_LEGAL_PARTY_PRC_PAGE_1_OPTION_FORM)
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
                                                               LEGAL_PARTY_TABLE,
                                                               field_mapping=field_mapping)
                if res_etl_model:
                    if field_mapping:
                        self.qgis_utils.delete_old_field_mapping(field_mapping)

                    self.qgis_utils.save_field_mapping(LEGAL_PARTY_TABLE)

            else:
                self.iface.messageBar().pushMessage("Asistente LADM_COL",
                    QCoreApplication.translate(self.WIZARD_NAME,
                                               "Select a source layer to set the field mapping to '{}'.").format(LEGAL_PARTY_TABLE),
                    Qgis.Warning)

        elif self.rad_create_manually.isChecked():
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

        # All layers were successfully loaded
        return True

    def required_layers_are_available(self):
        # Load layers
        self.qgis_utils.get_layers(self._db, self._layers, load=True)
        if not self._layers:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                                QCoreApplication.translate(self.WIZARD_NAME,
                                                                           "'{}' tool has been closed because there was a problem loading the requeries layers.").format(
                                                    self.WIZARD_TOOL_NAME),
                                                Qgis.Warning)
            return False

        # Check if layers any layer is in editing mode
        layers_name = list()
        for layer in self._layers:
            if self._layers[layer]['layer'].isEditable():
                layers_name.append(self._layers[layer]['layer'].name())

        if layers_name:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
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
            self.iface.messageBar().pushMessage("Asistente LADM_COL", message, Qgis.Info)
        self.disconnect_signals()
        self.close()

    def disconnect_signals(self):
        # QGIS APP
        try:
            self._layers[LEGAL_PARTY_TABLE][LAYER].committedFeaturesAdded.disconnect(self.finish_feature_creation)
        except:
            pass

    def edit_feature(self):
        self.iface.layerTreeView().setCurrentLayer(self._layers[LEGAL_PARTY_TABLE][LAYER])
        self._layers[LEGAL_PARTY_TABLE][LAYER].committedFeaturesAdded.connect(self.finish_feature_creation)
        self.open_form(self._layers[LEGAL_PARTY_TABLE][LAYER])

    def finish_feature_creation(self, layerId, features):
        message = QCoreApplication.translate(self.WIZARD_NAME,
                                             "'{}' tool has been closed because an error occurred while trying to save the data.").format(self.WIZARD_TOOL_NAME)
        fid = features[0].id()

        if not self._layers[LEGAL_PARTY_TABLE][LAYER].getFeature(fid).isValid():
            message = QCoreApplication.translate(self.WIZARD_NAME,
                                                 "'{}' tool has been closed. Feature not found in layer {}... It's not posible create a boundary. ").format(self.WIZARD_TOOL_NAME, LEGAL_PARTY_TABLE)
            self.log.logMessage("Feature not found in layer {} ...".format(LEGAL_PARTY_TABLE), PLUGIN_NAME, Qgis.Warning)
        else:
            feature_tid = self._layers[LEGAL_PARTY_TABLE][LAYER].getFeature(fid)[ID_FIELD]
            message = QCoreApplication.translate(self.WIZARD_NAME,
                                                 "The new legal party card (t_id={}) was successfully created ").format(feature_tid)

        self._layers[LEGAL_PARTY_TABLE][LAYER].committedFeaturesAdded.disconnect(self.finish_feature_creation)
        self.log.logMessage("Legal party's committedFeaturesAdded SIGNAL disconnected", PLUGIN_NAME, Qgis.Info)
        self.close_wizard(message)

    def open_form(self, layer):
        if not layer.isEditable():
            layer.startEditing()

        self.exec_form(layer)

    def exec_form(self, layer):
        feature = self.qgis_utils.get_new_feature(layer)
        dialog = self.iface.getFeatureForm(layer, feature)
        dialog.rejected.connect(self.form_rejected)
        dialog.setModal(True)

        if dialog.exec_():
            saved = layer.commitChanges()

            if not saved:
                layer.rollBack()
                self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                                    QCoreApplication.translate(self.WIZARD_NAME,
                                                                               "Error while saving changes. Party could not be created."),
                                                    Qgis.Warning)

                for e in layer.commitErrors():
                    self.log.logMessage("Commit error: {}".format(e), PLUGIN_NAME, Qgis.Warning)

            self.iface.mapCanvas().refresh()
        else:
            layer.rollBack()

    def form_rejected(self):
        message = QCoreApplication.translate(self.WIZARD_NAME,
                                             "'{}' tool has been closed because you just closed the form.").format(self.WIZARD_TOOL_NAME)
        self.close_wizard(message)

    def save_settings(self):
        settings = QSettings()
        settings.setValue('Asistente-LADM_COL/wizards/legal_party_load_data_type', 'create_manually' if self.rad_create_manually.isChecked() else 'refactor')

    def restore_settings(self):
        settings = QSettings()

        load_data_type = settings.value('Asistente-LADM_COL/wizards/legal_party_load_data_type') or 'create_manually'
        if load_data_type == 'refactor':
            self.rad_refactor.setChecked(True)
        else:
            self.rad_create_manually.setChecked(True)

    def show_help(self):
        self.qgis_utils.show_help("create_legal_party")
