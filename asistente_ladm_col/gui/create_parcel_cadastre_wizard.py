# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2017-12-09
        git sha              : :%H$
        copyright            : (C) 2017 by Germán Carrillo (BSF Swissphoto)
        email                : gcarrillo@linuxmail.org
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
                       QgsWkbTypes,
                       QgsMapLayerProxyModel,
                       QgsApplication)

from ..config.general_config import PLUGIN_NAME, FIELD_MAPPING_PATH
from ..config.help_strings import HelpStrings
from ..config.table_mapping_config import (BUILDING_TABLE,
                                           ID_FIELD,
                                           PARCEL_TABLE,
                                           PLOT_TABLE,
                                           UEBAUNIT_TABLE,
                                           UEBAUNIT_TABLE_BUILDING_FIELD,
                                           UEBAUNIT_TABLE_PARCEL_FIELD,
                                           UEBAUNIT_TABLE_PLOT_FIELD)
from ..utils import get_ui_class

WIZARD_UI = get_ui_class('wiz_create_parcel_cadastre.ui')


class CreateParcelCadastreWizard(QWizard, WIZARD_UI):
    def __init__(self, iface, db, qgis_utils, parent=None):
        QWizard.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self.log = QgsApplication.messageLog()
        self._plot_layer = None
        self._parcel_layer = None
        self._building_layer = None
        self._uebaunit_table = None
        self._db = db
        self.qgis_utils = qgis_utils
        self.help_strings = HelpStrings()

        self.restore_settings()

        self.rad_parcel_from_plot.toggled.connect(self.adjust_page_1_controls)
        self.adjust_page_1_controls()
        self.button(QWizard.FinishButton).clicked.connect(self.finished_dialog)
        self.button(QWizard.HelpButton).clicked.connect(self.show_help)

        self.mMapLayerComboBox.setFilters(QgsMapLayerProxyModel.NoGeometry)

    def adjust_page_1_controls(self):
        self.cbo_mapping.clear()
        self.cbo_mapping.addItem("")
        self.cbo_mapping.addItems(self.qgis_utils.get_field_mappings_file_names(PARCEL_TABLE))

        if self.rad_refactor.isChecked():
            self.lbl_refactor_source.setEnabled(True)
            self.mMapLayerComboBox.setEnabled(True)
            self.lbl_field_mapping.setEnabled(True)
            self.cbo_mapping.setEnabled(True)
            finish_button_text = QCoreApplication.translate("CreateParcelCadastreWizard", "Import")
            self.txt_help_page_1.setHtml(self.help_strings.get_refactor_help_string(PARCEL_TABLE, False))

        elif self.rad_parcel_from_plot.isChecked():
            self.lbl_refactor_source.setEnabled(False)
            self.mMapLayerComboBox.setEnabled(False)
            self.lbl_field_mapping.setEnabled(False)
            self.cbo_mapping.setEnabled(False)
            finish_button_text = QCoreApplication.translate("CreateParcelCadastreWizard", "Create")
            self.txt_help_page_1.setHtml(self.help_strings.WIZ_CREATE_PARCEL_CADASTRE_PAGE_1_OPTION_EXISTING_PLOT)

        self.wizardPage1.setButtonText(QWizard.FinishButton,
                                       QCoreApplication.translate("CreateParcelCadastreWizard",
                                       finish_button_text))

    def finished_dialog(self):
        self.save_settings()

        if self.rad_refactor.isChecked():
            if self.mMapLayerComboBox.currentLayer() is not None:
                field_mapping = self.cbo_mapping.currentText()
                res_etl_model = self.qgis_utils.show_etl_model(self._db,
                                                               self.mMapLayerComboBox.currentLayer(),
                                                               PARCEL_TABLE,
                                                               field_mapping=field_mapping)

                if res_etl_model:
                    if field_mapping:
                        self.qgis_utils.delete_old_field_mapping(field_mapping)

                    self.qgis_utils.save_field_mapping(PARCEL_TABLE)
            else:
                self.iface.messageBar().pushMessage("Asistente LADM_COL",
                    QCoreApplication.translate("CreateParcelCadastreWizard",
                                               "Select a source layer to set the field mapping to '{}'.").format(PARCEL_TABLE),
                    Qgis.Warning)

        elif self.rad_parcel_from_plot.isChecked():
            self.prepare_parcel_creation()

    def prepare_parcel_creation(self):
        # Load layers
        res_layers = self.qgis_utils.get_layers(self._db, {
            PLOT_TABLE: {'name': PLOT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry},
            PARCEL_TABLE: {'name': PARCEL_TABLE, 'geometry': None},
            BUILDING_TABLE: {'name': BUILDING_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry},
            UEBAUNIT_TABLE: {'name': UEBAUNIT_TABLE, 'geometry': None}}, load=True)

        self._plot_layer = res_layers[PLOT_TABLE]
        if self._plot_layer is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                QCoreApplication.translate("CreateParcelCadastreWizard",
                                           "Plot layer couldn't be found... {}").format(self._db.get_description()),
                Qgis.Warning)
            return

        self._parcel_layer = res_layers[PARCEL_TABLE]
        if self._parcel_layer is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                QCoreApplication.translate("CreateParcelCadastreWizard",
                                           "Parcel layer couldn't be found... {}").format(self._db.get_description()),
                Qgis.Warning)
            return

        self._building_layer = res_layers[BUILDING_TABLE]
        if self._building_layer is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                QCoreApplication.translate("CreateParcelCadastreWizard",
                                           "Building layer couldn't be found... {}").format(self._db.get_description()),
                Qgis.Warning)
            return

        self._uebaunit_table = res_layers[UEBAUNIT_TABLE]
        if self._uebaunit_table is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                QCoreApplication.translate("CreateParcelCadastreWizard",
                                           "UEBAUNIT table couldn't be found... {}").format(self._db.get_description()),
                Qgis.Warning)
            return

        # Don't suppress (i.e., show) feature form
        form_config = self._parcel_layer.editFormConfig()
        form_config.setSuppress(QgsEditFormConfig.SuppressOff)
        self._parcel_layer.setEditFormConfig(form_config)

        self.edit_parcel()

    def edit_parcel(self):
        if self._plot_layer.selectedFeatureCount() == 1 or self._building_layer.selectedFeatureCount() > 0:
            # Open Form
            self.iface.layerTreeView().setCurrentLayer(self._parcel_layer)
            self._parcel_layer.startEditing()
            self.iface.actionAddFeature().trigger()

            plot_ids = [f['t_id'] for f in self._plot_layer.selectedFeatures()]
            building_ids = [f['t_id'] for f in self._building_layer.selectedFeatures()]

            # Create connections to react when a feature is added to buffer and
            # when it gets stored into the DB
            self._parcel_layer.featureAdded.connect(self.call_parcel_commit)
            self._parcel_layer.committedFeaturesAdded.connect(partial(self.finish_parcel, plot_ids, building_ids))

        elif self._plot_layer.selectedFeatureCount() == 0 and self._building_layer.selectedFeatureCount() == 0:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                QCoreApplication.translate("CreateParcelCadastreWizard",
                                           "Please select one Plot or at least one Building"),
                Qgis.Warning)
        else: # >1
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                QCoreApplication.translate("CreateParcelCadastreWizard",
                                           "Please select only one Plot"),
                Qgis.Warning)

    def call_parcel_commit(self, fid):
        self._parcel_layer.featureAdded.disconnect(self.call_parcel_commit)
        self.log.logMessage("Parcel's featureAdded SIGNAL disconnected", PLUGIN_NAME, Qgis.Info)
        res = self._parcel_layer.commitChanges()

    def finish_parcel(self, plot_ids, building_ids, layerId, features):
        if len(features) != 1:
            self.log.logMessage("We should have got only one predio... We cannot do anything with {} predios".format(len(features)), PLUGIN_NAME, Qgis.Warning)
        else:
            fid = features[0].id()
            if not self._parcel_layer.getFeature(fid).isValid():
                self.log.logMessage("Feature not found in layer Predio...", PLUGIN_NAME, Qgis.Warning)
            else:
                parcel_id = self._parcel_layer.getFeature(fid)[ID_FIELD]

                # Fill uebaunit table
                new_features = []
                for plot_id in plot_ids:
                    new_feature = QgsVectorLayerUtils().createFeature(self._uebaunit_table)
                    new_feature.setAttribute(UEBAUNIT_TABLE_PLOT_FIELD, plot_id)
                    new_feature.setAttribute(UEBAUNIT_TABLE_PARCEL_FIELD, parcel_id)
                    self.log.logMessage("Saving Plot-Parcel: {}-{}".format(plot_id, parcel_id), PLUGIN_NAME, Qgis.Info)
                    new_features.append(new_feature)

                for building_id in building_ids:
                    new_feature = QgsVectorLayerUtils().createFeature(self._uebaunit_table)
                    new_feature.setAttribute(UEBAUNIT_TABLE_BUILDING_FIELD, building_id)
                    new_feature.setAttribute(UEBAUNIT_TABLE_PARCEL_FIELD, parcel_id)
                    self.log.logMessage("Saving Building-Parcel: {}-{}".format(building_id, parcel_id), PLUGIN_NAME, Qgis.Info)
                    new_features.append(new_feature)

                self._uebaunit_table.dataProvider().addFeatures(new_features)

                if plot_ids and building_ids:
                    self.iface.messageBar().pushMessage("Asistente LADM_COL",
                        QCoreApplication.translate("CreateParcelCadastreWizard",
                                                   "The new parcel (t_id={}) was successfully created and associated with its corresponding Plot (t_id={}) and Building(s) (t_id={})!").format(parcel_id, plot_ids[0], ", ".join([str(b) for b in building_ids])),
                        Qgis.Info)
                elif plot_ids and not building_ids:
                    self.iface.messageBar().pushMessage("Asistente LADM_COL",
                        QCoreApplication.translate("CreateParcelCadastreWizard",
                                                   "The new parcel (t_id={}) was successfully created and associated with its corresponding Plot (t_id={})!").format(parcel_id, plot_ids[0]),
                        Qgis.Info)
                elif not plot_ids and building_ids:
                    self.iface.messageBar().pushMessage("Asistente LADM_COL",
                        QCoreApplication.translate("CreateParcelCadastreWizard",
                                                   "The new parcel (t_id={}) was successfully created and associated with its corresponding Building(s) (t_id={})!").format(parcel_id, ", ".join([str(b) for b in building_ids])),
                        Qgis.Info)

        self._parcel_layer.committedFeaturesAdded.disconnect()
        self.log.logMessage("Parcel's committedFeaturesAdded SIGNAL disconnected", PLUGIN_NAME, Qgis.Info)

    def save_settings(self):
        settings = QSettings()
        settings.setValue('Asistente-LADM_COL/wizards/parcel_load_data_type', 'using_plots' if self.rad_parcel_from_plot.isChecked() else 'refactor')

    def restore_settings(self):
        settings = QSettings()

        load_data_type = settings.value('Asistente-LADM_COL/wizards/parcel_load_data_type') or 'using_plots'
        if load_data_type == 'refactor':
            self.rad_refactor.setChecked(True)
        else:
            self.rad_parcel_from_plot.setChecked(True)

    def show_help(self):
        self.qgis_utils.show_help("create_parcel")
