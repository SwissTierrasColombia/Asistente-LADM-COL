# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2018-11-23
        git sha              : :%H$
        copyright            : (C) 2018 by Jhon Galindo
        email                : jhonsigpjc@gmail.com
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
                       Qgis,
                       QgsVectorLayerUtils,
                       QgsWkbTypes,
                       QgsMapLayerProxyModel,
                       QgsApplication)

from ..config.general_config import PLUGIN_NAME
from ..config.help_strings import HelpStrings
from ..config.table_mapping_config import (AVALUOUNIDADCONSTRUCCION_TABLE,
                                           AVALUOUNIDADCONSTRUCCION_TABLE_BUILDING_UNIT_VALUATION_FIELD,
                                           AVALUOUNIDADCONSTRUCCION_TABLE_BUILDING_UNIT_FIELD,
                                           BUILDING_UNIT_TABLE,
                                           ID_FIELD,
                                           VALUATION_BUILDING_UNIT_TABLE)
from ..utils import get_ui_class

WIZARD_UI = get_ui_class('wiz_create_building_unit_valuation.ui')

class CreateBuildingUnitValuationWizard(QWizard, WIZARD_UI):
    def __init__(self, iface, db, qgis_utils, parent=None):
        QWizard.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self.log = QgsApplication.messageLog()
        self._building_unit_valuation = None
        self._building_unit_layer = None
        self._avaluounidadconstruccion_table = None
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
        self.cbo_mapping.addItems(self.qgis_utils.get_field_mappings_file_names(VALUATION_BUILDING_UNIT_TABLE))

        if self.rad_refactor.isChecked():
            self.lbl_refactor_source.setEnabled(True)
            self.mMapLayerComboBox.setEnabled(True)
            self.lbl_field_mapping.setEnabled(True)
            self.cbo_mapping.setEnabled(True)
            finish_button_text = QCoreApplication.translate("CreateBuildingUnitValuationWizard", "Import")
            self.txt_help_page_1.setHtml(self.help_strings.get_refactor_help_string(VALUATION_BUILDING_UNIT_TABLE, False))

        elif self.rad_create_manually.isChecked():
            self.lbl_refactor_source.setEnabled(False)
            self.mMapLayerComboBox.setEnabled(False)
            self.lbl_field_mapping.setEnabled(False)
            self.cbo_mapping.setEnabled(False)
            finish_button_text = QCoreApplication.translate("CreateBuildingUnitValuationWizard", "Create")
            self.txt_help_page_1.setHtml(self.help_strings.WIZ_CREATE_BUILDING_UNIT_VALUATION_PAGE_1_OPTION_FORM)

        self.wizardPage1.setButtonText(QWizard.FinishButton,
                                       QCoreApplication.translate("CreateBuildingUnitValuationWizard",
                                       finish_button_text))

    def finished_dialog(self):
        self.save_settings()

        if self.rad_refactor.isChecked():
            if self.mMapLayerComboBox.currentLayer() is not None:
                field_mapping = self.cbo_mapping.currentText()
                res_etl_model = self.qgis_utils.show_etl_model(self._db,
                                                               self.mMapLayerComboBox.currentLayer(),
                                                               VALUATION_BUILDING_UNIT_TABLE,
                                                               field_mapping=field_mapping)

                if res_etl_model:
                    if field_mapping:
                        self.qgis_utils.delete_old_field_mapping(field_mapping)

                    self.qgis_utils.save_field_mapping(VALUATION_BUILDING_UNIT_TABLE)

            else:
                self.iface.messageBar().pushMessage("Asistente LADM_COL",
                    QCoreApplication.translate("CreateBuildingUnitValuationWizard",
                                               "Select a source layer to set the field mapping to '{}'.").format(VALUATION_BUILDING_UNIT_TABLE),
                    Qgis.Warning)

        elif self.rad_create_manually.isChecked():
            self.prepare_building_unit_valuation_creation()

    def prepare_building_unit_valuation_creation(self):
        # Load layers
        res_layers = self.qgis_utils.get_layers(self._db, {
            VALUATION_BUILDING_UNIT_TABLE: {'name': VALUATION_BUILDING_UNIT_TABLE, 'geometry': None},
            BUILDING_UNIT_TABLE: {'name': BUILDING_UNIT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry},
            AVALUOUNIDADCONSTRUCCION_TABLE: {'name': AVALUOUNIDADCONSTRUCCION_TABLE, 'geometry': None}}, load=True)

        self._avaluounidadconstruccion_table = res_layers[AVALUOUNIDADCONSTRUCCION_TABLE]
        if self._avaluounidadconstruccion_table is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                QCoreApplication.translate("CreateBuildingUnitValuationWizard",
                                           "avaluounidadconstruccion table couldn't be found... {}").format(
                                            self._db.get_description()),
                                                Qgis.Warning)
            return

        self._building_unit_layer = res_layers[BUILDING_UNIT_TABLE]
        if self._building_unit_layer is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                QCoreApplication.translate("CreateBuildingUnitValuationWizard",
                                           "Building Unit table couldn't be found... {}").format(
                                            self._db.get_description()),
                                                Qgis.Warning)
            return

        self._building_unit_valuation = res_layers[VALUATION_BUILDING_UNIT_TABLE]
        if self._building_unit_valuation is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                QCoreApplication.translate("CreateBuildingUnitValuationWizard",
                                           "building unit table couldn't be found... {}").format(
                                            self._db.get_description()),
                Qgis.Warning)
            return

        # Don't suppress (i.e., show) feature form
        form_config = self._building_unit_valuation.editFormConfig()
        form_config.setSuppress(QgsEditFormConfig.SuppressOff)
        self._building_unit_valuation.setEditFormConfig(form_config)

        self.edit_building_unit_valuation()

    def edit_building_unit_valuation(self):

        if self._building_unit_layer.selectedFeatureCount() == 1:
            # Open Form
            self.iface.layerTreeView().setCurrentLayer(self._building_unit_valuation)
            self._building_unit_valuation.startEditing()
            self.iface.actionAddFeature().trigger()

            building_unit_ids = [f['t_id'] for f in self._building_unit_layer.selectedFeatures()]

            # Create connections to react when a feature is added to buffer and
            # when it gets stored into the DB
            self._building_unit_valuation.featureAdded.connect(self.call_building_unit_valuation_commit)
            self._building_unit_valuation.committedFeaturesAdded.connect(partial(self.finish_building_unit_valuation, building_unit_ids))

        elif self._building_unit_layer.selectedFeatureCount() == 0 or self._building_unit_layer.selectedFeatureCount() > 1:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                QCoreApplication.translate("CreateBuildingUnitValuationWizard",
                                           "Please select one building unit"),
                Qgis.Warning)

    def call_building_unit_valuation_commit(self, fid):
        self._building_unit_valuation.featureAdded.disconnect(self.call_building_unit_valuation_commit)
        self.log.logMessage("building unit valuation's featureAdded SIGNAL disconnected", PLUGIN_NAME, Qgis.Info)
        res = self._building_unit_valuation.commitChanges()

    def finish_building_unit_valuation(self, building_unit_ids, layerId, features):
        if len(features) != 1:
            self.log.logMessage("We should have got only one building unit... We cannot do anything with {} building units".format(len(features)), PLUGIN_NAME, Qgis.Warning)
        else:
            fid = features[0].id()
            if not self._building_unit_valuation.getFeature(fid).isValid():
                self.log.logMessage("Feature not found in layer building unit...", PLUGIN_NAME, Qgis.Warning)
            else:
                building_unit_valuation_id = self._building_unit_valuation.getFeature(fid)[ID_FIELD]

                # Fill avaluounidadconstruccion table
                new_features = []
                for building_unit_id in building_unit_ids:
                    new_feature = QgsVectorLayerUtils().createFeature(self._avaluounidadconstruccion_table)
                    new_feature.setAttribute(AVALUOUNIDADCONSTRUCCION_TABLE_BUILDING_UNIT_FIELD, building_unit_id)
                    new_feature.setAttribute(AVALUOUNIDADCONSTRUCCION_TABLE_BUILDING_UNIT_VALUATION_FIELD, building_unit_valuation_id)
                    self.log.logMessage("Saving Building unit-Building unit valuation: {}-{}".format(building_unit_id, building_unit_valuation_id), PLUGIN_NAME, Qgis.Info)
                    new_features.append(new_feature)

                self._avaluounidadconstruccion_table.dataProvider().addFeatures(new_features)

                if building_unit_ids:
                    self.iface.messageBar().pushMessage("Asistente LADM_COL",
                        QCoreApplication.translate("CreateBuildingUnitValuationWizard",
                                                   "The new building unit valuation (t_id={}) was successfully created and associated with its corresponding building unit (t_id={})!").format(building_unit_valuation_id, building_unit_ids[0]),
                        Qgis.Info)


        self._building_unit_valuation.committedFeaturesAdded.disconnect()
        self.log.logMessage("Building unit valuation's committedFeaturesAdded SIGNAL disconnected", PLUGIN_NAME, Qgis.Info)

    def save_settings(self):
        settings = QSettings()
        settings.setValue('Asistente-LADM_COL/wizards/valuation_building_unit_load_data_type', 'create_manually' if self.rad_create_manually.isChecked() else 'refactor')

    def restore_settings(self):
        settings = QSettings()

        load_data_type = settings.value('Asistente-LADM_COL/wizards/valuation_building_unit_load_data_type') or 'create_manually'
        if load_data_type == 'refactor':
            self.rad_refactor.setChecked(True)
        else:
            self.rad_create_manually.setChecked(True)

    def show_help(self):
        self.qgis_utils.show_help("create_building_unit_valuation")