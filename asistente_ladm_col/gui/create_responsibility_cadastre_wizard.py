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
from qgis.gui import QgsExpressionSelectionDialog

from ..config.general_config import PLUGIN_NAME
from ..config.help_strings import HelpStrings
from ..config.table_mapping_config import (ID_FIELD,
                                           RESPONSIBILITY_TABLE,
                                           ADMINISTRATIVE_SOURCE_TABLE,
                                           RRR_SOURCE_RELATION_TABLE,
                                           RRR_SOURCE_RESPONSIBILITY_FIELD,
                                           RRR_SOURCE_SOURCE_FIELD)
from ..utils import get_ui_class
from ..utils.qt_utils import (enable_next_wizard,
                              disable_next_wizard)

WIZARD_UI = get_ui_class('wiz_create_responsibility_cadastre.ui')


class CreateResponsibilityCadastreWizard(QWizard, WIZARD_UI):
    def __init__(self, iface, db, qgis_utils, parent=None):
        QWizard.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self.log = QgsApplication.messageLog()
        self._current_layer = None
        self._responsibility_layer = None
        self._administrative_source_layer = None
        self._rrr_source_relation_layer = None
        self._db = db
        self.qgis_utils = qgis_utils
        self.help_strings = HelpStrings()

        self.restore_settings()

        self.rad_create_manually.toggled.connect(self.adjust_page_1_controls)
        self.adjust_page_1_controls()
        self.button(QWizard.NextButton).clicked.connect(self.adjust_page_2_controls)
        self.button(QWizard.FinishButton).clicked.connect(self.finished_dialog)
        self.button(QWizard.HelpButton).clicked.connect(self.show_help)

        self.mMapLayerComboBox.setFilters(QgsMapLayerProxyModel.NoGeometry)

    def adjust_page_1_controls(self):
        self.cbo_mapping.clear()
        self.cbo_mapping.addItem("")
        self.cbo_mapping.addItems(self.qgis_utils.get_field_mappings_file_names(RESPONSIBILITY_TABLE))

        if self.rad_refactor.isChecked():
            self.lbl_refactor_source.setEnabled(True)
            self.mMapLayerComboBox.setEnabled(True)
            self.lbl_field_mapping.setEnabled(True)
            self.cbo_mapping.setEnabled(True)
            disable_next_wizard(self)
            self.wizardPage1.setFinalPage(True)
            finish_button_text = QCoreApplication.translate("CreateResponsibilityCadastreWizard", "Import")
            self.txt_help_page_1.setHtml(self.help_strings.get_refactor_help_string(RESPONSIBILITY_TABLE, False))
            self.wizardPage1.setButtonText(QWizard.FinishButton, finish_button_text)
        elif self.rad_create_manually.isChecked():
            self.lbl_refactor_source.setEnabled(False)
            self.mMapLayerComboBox.setEnabled(False)
            self.lbl_field_mapping.setEnabled(False)
            self.cbo_mapping.setEnabled(False)
            enable_next_wizard(self)
            self.wizardPage1.setFinalPage(False)
            finish_button_text = QCoreApplication.translate("CreateResponsibilityCadastreWizard", "Create")
            self.txt_help_page_1.setHtml(self.help_strings.WIZ_CREATE_RESPONSIBILITY_CADASTRE_PAGE_1_OPTION_FORM)

        self.wizardPage2.setButtonText(QWizard.FinishButton,finish_button_text)

    def adjust_page_2_controls(self):
        self.button(self.FinishButton).setDisabled(True)
        self.txt_help_page_2.setHtml(self.help_strings.WIZ_CREATE_RESPONSIBILITY_CADASTRE_PAGE_2)

        try:
            self.btn_admin_source_expression.clicked.disconnect()
        except:
            pass

        # Load layers
        result = self.prepare_responsibility_creation_layers()

        if result:
            # Check if previous features are selected
            self.check_selected_features()
            self.btn_admin_source_expression.clicked.connect(partial(self.select_features_by_expression, self._administrative_source_layer))

    def select_features_by_expression(self, layer):
        self._current_layer = layer
        self.iface.setActiveLayer(self._current_layer)
        dlg_expression_selection = QgsExpressionSelectionDialog(self._current_layer)
        self._current_layer.selectionChanged.connect(self.check_selected_features)
        dlg_expression_selection.exec()
        self._current_layer.selectionChanged.disconnect(self.check_selected_features)

    def check_selected_features(self):
        # Check selected features in administrative source layer
        if self._administrative_source_layer.selectedFeatureCount():
            self.lb_admin_source.setText(QCoreApplication.translate("CreateResponsibilityCadastreWizard", "<b>Administrative Source(s)</b>: {count} Feature Selected").format(count=self._administrative_source_layer.selectedFeatureCount()))
        else:
            self.lb_admin_source.setText(QCoreApplication.translate("CreateResponsibilityCadastreWizard", "<b>Administrative Source(s)</b>: 0 Features Selected"))

        if self._administrative_source_layer.selectedFeatureCount() >= 1:
            self.button(self.FinishButton).setDisabled(False)
        else:
            self.button(self.FinishButton).setDisabled(True)

    def finished_dialog(self):
        self.save_settings()

        if self.rad_refactor.isChecked():
            if self.mMapLayerComboBox.currentLayer() is not None:
                field_mapping = self.cbo_mapping.currentText()
                res_etl_model = self.qgis_utils.show_etl_model(self._db,
                                                               self.mMapLayerComboBox.currentLayer(),
                                                               RESPONSIBILITY_TABLE,
                                                               field_mapping=field_mapping)

                if res_etl_model:
                    if field_mapping:
                        self.qgis_utils.delete_old_field_mapping(field_mapping)

                    self.qgis_utils.func_save_field_mapping(RESPONSIBILITY_TABLE)
            else:
                self.iface.messageBar().pushMessage("Asistente LADM_COL",
                    QCoreApplication.translate("CreateResponsibilityCadastreWizard",
                                               "Select a source layer to set the field mapping to '{}'.").format(RESPONSIBILITY_TABLE),
                    Qgis.Warning)

        elif self.rad_create_manually.isChecked():
            self.prepare_responsibility_creation()

    def prepare_responsibility_creation(self):
        result = self.prepare_responsibility_creation_layers()

        if result:
            # Don't suppress (i.e., show) feature form
            form_config = self._responsibility_layer.editFormConfig()
            form_config.setSuppress(QgsEditFormConfig.SuppressOff)
            self._responsibility_layer.setEditFormConfig(form_config)
            self.edit_responsibility()

    def prepare_responsibility_creation_layers(self):
        # Load layers
        # self._responsibility_layer = self.qgis_utils.get_layer(self._db, RESPONSIBILITY_TABLE, None, load=True)

        res_layers = self.qgis_utils.get_layers(self._db, {
            RESPONSIBILITY_TABLE: {'name': RESPONSIBILITY_TABLE, 'geometry': None},
            ADMINISTRATIVE_SOURCE_TABLE: {'name': ADMINISTRATIVE_SOURCE_TABLE, 'geometry': None},
            RRR_SOURCE_RELATION_TABLE: {'name': RRR_SOURCE_RELATION_TABLE, 'geometry': None}}, load=True)

        self._responsibility_layer = res_layers[RESPONSIBILITY_TABLE]
        self._administrative_source_layer = res_layers[ADMINISTRATIVE_SOURCE_TABLE]
        self._rrr_source_relation_layer = res_layers[RRR_SOURCE_RELATION_TABLE]

        if self._responsibility_layer is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                                QCoreApplication.translate("CreateResponsibilityCadastreWizard",
                                                                           "Responsibility layer couldn't be found..."),
                                                Qgis.Warning)
            return

        if self._administrative_source_layer is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                                QCoreApplication.translate("CreateResponsibilityCadastreWizard",
                                                                           "Administrative source layer couldn't be found..."),
                                                Qgis.Warning)
            return

        if self._rrr_source_relation_layer is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                                QCoreApplication.translate("CreateResponsibilityCadastreWizard",
                                                                           "rrr source relation layer couldn't be found..."),
                                                Qgis.Warning)
            return

        # All layers were successfully loaded
        return True

    def edit_responsibility(self):
        if self._administrative_source_layer.selectedFeatureCount() >= 1:
            # Open Form
            self.iface.layerTreeView().setCurrentLayer(self._responsibility_layer)
            self._responsibility_layer.startEditing()
            self.iface.actionAddFeature().trigger()

            administrative_source_ids = [f['t_id'] for f in self._administrative_source_layer.selectedFeatures()]

            # Create connections to react when a feature is added to buffer and
            # when it gets stored into the DB
            self._responsibility_layer.featureAdded.connect(self.call_responsibility_commit)
            self._responsibility_layer.committedFeaturesAdded.connect(partial(self.finish_responsibility, administrative_source_ids))

        else:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                QCoreApplication.translate("CreateResponsibilityCadastreWizard",
                                           "Please select an Administrative source"),
                Qgis.Warning)

    def call_responsibility_commit(self, fid):
        self._responsibility_layer.featureAdded.disconnect(self.call_responsibility_commit)
        self.log.logMessage("Responsibility's featureAdded SIGNAL disconnected", PLUGIN_NAME, Qgis.Info)
        res = self._responsibility_layer.commitChanges()

    def finish_responsibility(self, administrative_source_ids, layerId, features):
        if len(features) != 1:
            self.log.logMessage("We should have got only one Responsibility... We cannot do anything with {} responsibility".format(len(features)), PLUGIN_NAME, Qgis.Warning)
        else:
            fid = features[0].id()
            if not self._responsibility_layer.getFeature(fid).isValid():
                self.log.logMessage("Feature not found in layer Responsibility...", PLUGIN_NAME, Qgis.Warning)
            else:
                responsibility_id = self._responsibility_layer.getFeature(fid)[ID_FIELD]

                # Fill rrrfuente table
                new_features = []
                for administrative_source_id in administrative_source_ids:
                    new_feature = QgsVectorLayerUtils().createFeature(self._rrr_source_relation_layer)
                    new_feature.setAttribute(RRR_SOURCE_SOURCE_FIELD, administrative_source_id)
                    new_feature.setAttribute(RRR_SOURCE_RESPONSIBILITY_FIELD, responsibility_id)
                    self.log.logMessage("Saving Administrative_source-Responsibility: {}-{}".format(administrative_source_id, responsibility_id), PLUGIN_NAME, Qgis.Info)
                    new_features.append(new_feature)

                self._rrr_source_relation_layer.dataProvider().addFeatures(new_features)

                self.iface.messageBar().pushMessage("Asistente LADM_COL",
                    QCoreApplication.translate("CreateResponsibilityCadastreWizard",
                                               "The new responsibility (t_id={}) was successfully created and associated with its corresponding administrative source (t_id={})!").format(responsibility_id, administrative_source_ids[0]),
                    Qgis.Info)

        self._responsibility_layer.committedFeaturesAdded.disconnect()
        self.log.logMessage("Responsibility's committedFeaturesAdded SIGNAL disconnected", PLUGIN_NAME, Qgis.Info)

    def save_settings(self):
        settings = QSettings()
        settings.setValue('Asistente-LADM_COL/wizards/responsibility_load_data_type', 'create_manually' if self.rad_create_manually.isChecked() else 'refactor')

    def restore_settings(self):
        settings = QSettings()

        load_data_type = settings.value('Asistente-LADM_COL/wizards/responsibility_load_data_type') or 'create_manually'
        if load_data_type == 'refactor':
            self.rad_refactor.setChecked(True)
        else:
            self.rad_create_manually.setChecked(True)

    def show_help(self):
        self.qgis_utils.show_help("create_responsibility")
