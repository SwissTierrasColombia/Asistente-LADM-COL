# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2018-03-06
        git sha              : :%H$
        copyright            : (C) 2018 by Sergio Ramírez (Incige SAS)
        email                : seralra96@gmail.com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""
from functools import partial

from qgis.PyQt.QtCore import (QCoreApplication,
                              QSettings)
from qgis.PyQt.QtWidgets import QWizard
from qgis.core import (QgsEditFormConfig,
                       QgsVectorLayerUtils,
                       Qgis,
                       QgsMapLayerProxyModel,
                       QgsApplication)

from ..config.general_config import (PLUGIN_NAME,
                                     FIELD_MAPPING_PATH)
from ..config.help_strings import HelpStrings
from ..config.table_mapping_config import (ID_FIELD,
                                           RIGHT_TABLE,
                                           ADMINISTRATIVE_SOURCE_TABLE,
                                           RRR_SOURCE_RELATION_TABLE,
                                           RRR_SOURCE_RIGHT_FIELD,
                                           RRR_SOURCE_SOURCE_FIELD)
from ..utils import get_ui_class

WIZARD_UI = get_ui_class('wiz_create_right_cadastre.ui')


class CreateRightCadastreWizard(QWizard, WIZARD_UI):
    def __init__(self, iface, db, qgis_utils, parent=None):
        QWizard.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self.log = QgsApplication.messageLog()
        self._right_layer = None
        self._administrative_source_layer = None
        self._rrr_source_relation_layer = None
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
        self.cbo_mapping.clear()
        self.cbo_mapping.addItem("")
        self.cbo_mapping.addItems(self.qgis_utils.get_field_mappings_file_names(RIGHT_TABLE))

        if self.rad_refactor.isChecked():
            self.lbl_refactor_source.setEnabled(True)
            self.mMapLayerComboBox.setEnabled(True)
            self.lbl_field_mapping.setEnabled(True)
            self.cbo_mapping.setEnabled(True)
            finish_button_text = QCoreApplication.translate("CreateRightCadastreWizard", "Import")
            self.txt_help_page_1.setHtml(self.help_strings.get_refactor_help_string(RIGHT_TABLE, False))

        elif self.rad_create_manually.isChecked():
            self.lbl_refactor_source.setEnabled(False)
            self.mMapLayerComboBox.setEnabled(False)
            self.lbl_field_mapping.setEnabled(False)
            self.cbo_mapping.setEnabled(False)
            finish_button_text = QCoreApplication.translate("CreateRightCadastreWizard", "Create")
            self.txt_help_page_1.setHtml(self.help_strings.WIZ_CREATE_RIGHT_CADASTRE_PAGE_1_OPTION_FORM)

        self.wizardPage1.setButtonText(QWizard.FinishButton,
                                       QCoreApplication.translate("CreaterRightCadastreWizard",
                                       finish_button_text))

    def finished_dialog(self):
        self.save_settings()

        if self.rad_refactor.isChecked():
            if self.mMapLayerComboBox.currentLayer() is not None:
                field_mapping = self.cbo_mapping.currentText()
                res_etl_model = self.qgis_utils.show_etl_model(self._db,
                                                               self.mMapLayerComboBox.currentLayer(),
                                                               RIGHT_TABLE,
                                                               field_mapping=field_mapping)

                if res_etl_model:
                    if field_mapping:
                        self.qgis_utils.delete_old_field_mapping(field_mapping)

                    self.qgis_utils.save_field_mapping(RIGHT_TABLE)
            else:
                self.iface.messageBar().pushMessage("Asistente LADM_COL",
                    QCoreApplication.translate("CreateRightCadastreWizard",
                                               "Select a source layer to set the field mapping to '{}'.").format(RIGHT_TABLE),
                    Qgis.Warning)

        elif self.rad_create_manually.isChecked():
            self.prepare_right_creation()

    def prepare_right_creation(self):
        # Load layers
        #self._right_layer = self.qgis_utils.get_layer(self._db, RIGHT_TABLE, None, load=True)

        res_layers = self.qgis_utils.get_layers(self._db, {
            RIGHT_TABLE: {'name': RIGHT_TABLE, 'geometry': None},
            ADMINISTRATIVE_SOURCE_TABLE: {'name': ADMINISTRATIVE_SOURCE_TABLE, 'geometry': None},
            RRR_SOURCE_RELATION_TABLE: {'name': RRR_SOURCE_RELATION_TABLE, 'geometry': None}}, load=True)

        self._right_layer = res_layers[RIGHT_TABLE]
        self._administrative_source_layer = res_layers[ADMINISTRATIVE_SOURCE_TABLE]
        self._rrr_source_relation_layer =  res_layers[RRR_SOURCE_RELATION_TABLE]

        if self._right_layer is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                QCoreApplication.translate("CreateRightCadastreWizard",
                                           "Right layer couldn't be found..."),
                Qgis.Warning)
            return

        if self._administrative_source_layer is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                QCoreApplication.translate("CreateRightCadastreWizard",
                                           "Administrative source layer couldn't be found..."),
                Qgis.Warning)
            return

        if self._rrr_source_relation_layer is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                QCoreApplication.translate("CreateRightCadastreWizard",
                                           "rrr source relation layer couldn't be found..."),
                Qgis.Warning)
            return

        # Don't suppress (i.e., show) feature form
        form_config = self._right_layer.editFormConfig()
        form_config.setSuppress(QgsEditFormConfig.SuppressOff)
        self._right_layer.setEditFormConfig(form_config)

        self.edit_right()

    def edit_right(self):
        if self._administrative_source_layer.selectedFeatureCount() >= 1:
            # Open Form
            self.iface.layerTreeView().setCurrentLayer(self._right_layer)
            self._right_layer.startEditing()
            self.iface.actionAddFeature().trigger()

            administrative_source_ids = [f['t_id'] for f in self._administrative_source_layer.selectedFeatures()]

            # Create connections to react when a feature is added to buffer and
            # when it gets stored into the DB
            self._right_layer.featureAdded.connect(self.call_right_commit)
            self._right_layer.committedFeaturesAdded.connect(partial(self.finish_right, administrative_source_ids))

        else:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                QCoreApplication.translate("CreateRightCadastreWizard",
                                           "Please select an Administrative source"),
                Qgis.Warning)

    def call_right_commit(self, fid):
        self._right_layer.featureAdded.disconnect(self.call_right_commit)
        self.log.logMessage("Right's featureAdded SIGNAL disconnected", PLUGIN_NAME, Qgis.Info)
        res = self._right_layer.commitChanges()

    def finish_right(self, administrative_source_ids, layerId, features):
        if len(features) != 1:
            self.log.logMessage("We should have got only one right... We cannot do anything with {} rights".format(len(features)), PLUGIN_NAME, Qgis.Warning)
        else:
            fid = features[0].id()
            if not self._right_layer.getFeature(fid).isValid():
                self.log.logMessage("Feature not found in layer Right...", PLUGIN_NAME, Qgis.Warning)
            else:
                right_id = self._right_layer.getFeature(fid)[ID_FIELD]

                # Fill rrrfuente table
                new_features = []
                for administrative_source_id in administrative_source_ids:
                    new_feature = QgsVectorLayerUtils().createFeature(self._rrr_source_relation_layer)
                    new_feature.setAttribute(RRR_SOURCE_SOURCE_FIELD, administrative_source_id)
                    new_feature.setAttribute(RRR_SOURCE_RIGHT_FIELD, right_id)
                    self.log.logMessage("Saving Administrative_source-Right: {}-{}".format(administrative_source_id, right_id), PLUGIN_NAME, Qgis.Info)
                    new_features.append(new_feature)

                self._rrr_source_relation_layer.dataProvider().addFeatures(new_features)

                self.iface.messageBar().pushMessage("Asistente LADM_COL",
                    QCoreApplication.translate("CreateRightCadastreWizard",
                                               "The new right (t_id={}) was successfully created and associated with its corresponding administrative source (t_id={})!").format(right_id, administrative_source_ids[0]),
                    Qgis.Info)

        self._right_layer.committedFeaturesAdded.disconnect()
        self.log.logMessage("Right's committedFeaturesAdded SIGNAL disconnected", PLUGIN_NAME, Qgis.Info)

    def save_settings(self):
        settings = QSettings()
        settings.setValue('Asistente-LADM_COL/wizards/right_load_data_type', 'create_manually' if self.rad_create_manually.isChecked() else 'refactor')

    def restore_settings(self):
        settings = QSettings()

        load_data_type = settings.value('Asistente-LADM_COL/wizards/right_load_data_type') or 'create_manually'
        if load_data_type == 'refactor':
            self.rad_refactor.setChecked(True)
        else:
            self.rad_create_manually.setChecked(True)

    def show_help(self):
        self.qgis_utils.show_help("create_right")
