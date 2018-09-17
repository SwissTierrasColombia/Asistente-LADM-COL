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
from qgis.core import (QgsEditFormConfig, QgsVectorLayerUtils, Qgis,
                       QgsWkbTypes, QgsMapLayerProxyModel)
from qgis.gui import QgsMessageBar
from qgis.PyQt.QtCore import Qt, QPoint, QCoreApplication, QSettings
from qgis.PyQt.QtWidgets import QAction, QWizard

from ..utils import get_ui_class
from ..config.table_mapping_config import (
    PROPERTY_RECORD_CARD_TABLE,
    PARCEL_TABLE,
    PARCEL_PROPERTY_RECORD_CARD_TABLE,
    PPRC_PARCEL_FIELD,
    PPRC_PROPERTY_RECORD_CARD_FIELD)

from ..config.help_strings import HelpStrings

WIZARD_UI = get_ui_class('wiz_create_property_record_card_prc.ui')

class CreatePropertyRecordCardPRCWizard(QWizard, WIZARD_UI):
    def __init__(self, iface, db, qgis_utils, parent=None):
        QWizard.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self._property_record_card_table = None
        self._parcel_layer = None
        self._parcel_property_record_card_table = None
        self._db = db
        self.qgis_utils = qgis_utils
        self.help_strings = HelpStrings()

        self.restore_settings()

        self.rad_create_manually.toggled.connect(self.adjust_page_1_controls)
        self.adjust_page_1_controls()
        self.button(QWizard.FinishButton).clicked.connect(self.finished_dialog)
        self.button(QWizard.HelpButton).clicked.connect(self.show_help)

        self.mMapLayerComboBox.setFilters(QgsMapLayerProxyModel.NoGeometry)

    def adjust_page_1_controls(self):
        if self.rad_refactor.isChecked():
            self.lbl_refactor_source.setEnabled(True)
            self.mMapLayerComboBox.setEnabled(True)
            finish_button_text = QCoreApplication.translate("CreatePropertyRecordCardWizard", "Import")
            self.txt_help_page_1.setHtml(self.help_strings.get_refactor_help_string(PROPERTY_RECORD_CARD_TABLE, False))

        elif self.rad_create_manually.isChecked():
            self.lbl_refactor_source.setEnabled(False)
            self.mMapLayerComboBox.setEnabled(False)
            finish_button_text = QCoreApplication.translate("CreatePropertyRecordCardWizard", "Create")
            self.txt_help_page_1.setHtml(self.help_strings.WIZ_CREATE_PROPERTY_RECORD_CARD_PRC_PAGE_1_OPTION_FORM)

        self.wizardPage1.setButtonText(QWizard.FinishButton,
                                       QCoreApplication.translate("CreatePropertyRecordCardWizard",
                                       finish_button_text))

    def finished_dialog(self):
        self.save_settings()

        if self.rad_refactor.isChecked():
            if self.mMapLayerComboBox.currentLayer() is not None:
                self.qgis_utils.show_etl_model(self._db,
                                               self.mMapLayerComboBox.currentLayer(),
                                               PROPERTY_RECORD_CARD_TABLE)
            else:
                self.iface.messageBar().pushMessage("Asistente LADM_COL",
                    QCoreApplication.translate("CreatePropertyRecordCardWizard",
                                               "Select a source layer to set the field mapping to '{}'.").format(PROPERTY_RECORD_CARD_TABLE),
                    Qgis.Warning)

        elif self.rad_create_manually.isChecked():
            self.prepare_property_record_card_creation()

    def prepare_property_record_card_creation(self):
        # Load layers
        #self._property_record_card_table = self.qgis_utils.get_layer(self._db, PROPERTY_RECORD_CARD_TABLE, load=True)

        # Load layers
        res_layers = self.qgis_utils.get_layers(self._db, {
            PROPERTY_RECORD_CARD_TABLE: {'name': PROPERTY_RECORD_CARD_TABLE, 'geometry': None},
            PARCEL_TABLE: {'name': PARCEL_TABLE, 'geometry': None}}, load=True)

        self._property_record_card_table = res_layers[PROPERTY_RECORD_CARD_TABLE]
        if self._property_record_card_table is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                QCoreApplication.translate("CreatePropertyRecordCardWizard",
                                           "Property record card table couldn't be found... {}").format(self._db.get_description()),
                Qgis.Warning)
            return

        self._parcel_layer = res_layers[PARCEL_TABLE]
        if self._parcel_layer is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                QCoreApplication.translate("CreatePropertyRecordCardWizard",
                                           "Parcel layer couldn't be found... {}").format(self._db.get_description()),
                Qgis.Warning)
            return

        # Don't suppress (i.e., show) feature form
        form_config = self._property_record_card_table.editFormConfig()
        form_config.setSuppress(QgsEditFormConfig.SuppressOff)
        self._property_record_card_table.setEditFormConfig(form_config)

        self.edit_property_record_card()

    def edit_property_record_card(self):
        if self._plot_layer.selectedFeatureCount() == 1:

            # Open Form
            self.iface.layerTreeView().setCurrentLayer(self._property_record_card_table)
            self._property_record_card_table.startEditing()
            self.iface.actionAddFeature().trigger()

            parcel_ids = [f['t_id'] for f in self._parcel_layer.selectedFeatures()]

            self._property_record_card_table.featureAdded.connect(self.call_property_record_card_commit)
            self._property_record_card_table.committedFeaturesAdded.connect(partial(self.finish_propery_record_card, plot_ids))

        elif self._parcel_layer.selectedFeatureCount() == 0:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                QCoreApplication.translate("CreateParcelCadastreWizard",
                                           "Please select one Parcel"),
                Qgis.Warning)
        else: # >1
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                QCoreApplication.translate("CreateParcelCadastreWizard",
                                           "Please select only one Parcel"),
                Qgis.Warning)

    def call_property_record_card_commit(self, fid):
        self._property_record_card_table.featureAdded.disconnect(self.call_property_record_card_commit)
        self.log.logMessage("Propery record card's featureAdded SIGNAL disconnected", PLUGIN_NAME, Qgis.Info)
        res = self._property_record_card_table.commitChanges()

    def finish_parcel(self, parcel_ids, layerId, features):
        if len(features) != 1:
            self.log.logMessage("We should have got only one property record card... We cannot do anything with {} property record cards".format(len(features)), PLUGIN_NAME, Qgis.Warning)
        else:
            fid = features[0].id()
            if not self._property_record_card_table.getFeature(fid).isValid():
                self.log.logMessage("Feature not found in layer Property record card...", PLUGIN_NAME, Qgis.Warning)
            else:
                prc_id = self._property_record_card_table.getFeature(fid)[ID_FIELD]

                # Fill uebaunit table
                new_features = []
                for parcel_id in parcel_ids:
                    new_feature = QgsVectorLayerUtils().createFeature(self._parcel_property_record_card_table)
                    new_feature.setAttribute(PPRC_PARCEL_FIELD, parcel_id)
                    new_feature.setAttribute(PPRC_PROPERTY_RECORD_CARD_FIELD, prc_id)
                    self.log.logMessage("Saving Parcel-Property record card: {}-{}".format(parcel_id, prc_id), PLUGIN_NAME, Qgis.Info)
                    new_features.append(new_feature)

                self._parcel_property_record_card_table.dataProvider().addFeatures(new_features)

                if parcel_ids:
                    self.iface.messageBar().pushMessage("Asistente LADM_COL",
                        QCoreApplication.translate("CreateParcelCadastreWizard",
                                                   "The new property record card (t_id={}) was successfully created and associated with its corresponding Parcel (t_id={})!").format(prc_id, parcel_ids[0]),
                        Qgis.Info)

        self._property_record_card_table.committedFeaturesAdded.disconnect()
        self.log.logMessage("Property record card's committedFeaturesAdded SIGNAL disconnected", PLUGIN_NAME, Qgis.Info)


    def save_settings(self):
        settings = QSettings()
        settings.setValue('Asistente-LADM_COL/wizards/property_record_card_load_data_type', 'create_manually' if self.rad_create_manually.isChecked() else 'refactor')

    def restore_settings(self):
        settings = QSettings()

        load_data_type = settings.value('Asistente-LADM_COL/wizards/property_record_card_load_data_type') or 'create_manually'
        if load_data_type == 'refactor':
            self.rad_refactor.setChecked(True)
        else:
            self.rad_create_manually.setChecked(True)

    def show_help(self):
        self.qgis_utils.show_help("create_property_record_card")
