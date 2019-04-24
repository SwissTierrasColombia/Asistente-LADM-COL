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
import sip
from functools import partial

from qgis.PyQt.QtCore import (QCoreApplication,
                              QSettings)
from qgis.PyQt.QtWidgets import (QWizard,
                                 QMessageBox)
from qgis.core import (QgsEditFormConfig,
                       QgsVectorLayerUtils,
                       Qgis,
                       QgsWkbTypes,
                       QgsMapLayerProxyModel,
                       QgsApplication)
from qgis.gui import QgsExpressionSelectionDialog

from ..config.general_config import PLUGIN_NAME
from ..config.help_strings import HelpStrings
from ..config.table_mapping_config import (BUILDING_TABLE,
                                           BUILDING_UNIT_TABLE,
                                           ID_FIELD,
                                           PARCEL_TABLE,
                                           PLOT_TABLE,
                                           UEBAUNIT_TABLE,
                                           UEBAUNIT_TABLE_BUILDING_FIELD,
                                           UEBAUNIT_TABLE_BUILDING_UNIT_FIELD,
                                           UEBAUNIT_TABLE_PARCEL_FIELD,
                                           UEBAUNIT_TABLE_PLOT_FIELD)
from ..utils import get_ui_class
from ..utils.qt_utils import (enable_next_wizard,
                              disable_next_wizard)
from ..utils.select_map_tool import SelectMapTool

WIZARD_UI = get_ui_class('wiz_create_parcel_cadastre.ui')


class CreateParcelCadastreWizard(QWizard, WIZARD_UI):

    def __init__(self, iface, db, qgis_utils, parent=None):
        QWizard.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self.log = QgsApplication.messageLog()
        self.canvas = self.iface.mapCanvas()
        self.maptool = self.canvas.mapTool()
        self.select_maptool = None
        self._current_layer = None
        self._plot_layer = None
        self._parcel_layer = None
        self._building_layer = None
        self._building_unit_layer = None
        self._uebaunit_table = None
        self._db = db
        self.qgis_utils = qgis_utils
        self.help_strings = HelpStrings()

        self.restore_settings()

        self.rad_parcel_from_plot.toggled.connect(self.adjust_page_1_controls)
        self.adjust_page_1_controls()
        self.button(QWizard.NextButton).clicked.connect(self.adjust_page_2_controls)
        self.button(QWizard.FinishButton).clicked.connect(self.finished_dialog)
        self.button(QWizard.HelpButton).clicked.connect(self.show_help)

        self.mMapLayerComboBox.setFilters(QgsMapLayerProxyModel.NoGeometry)

    def map_tool_changed(self, new_tool, old_tool):
        reply = QMessageBox.question(self,
                                     QCoreApplication.translate("CreateParcelCadastreWizard", "Stop parcel creation?"),
                                     QCoreApplication.translate("CreateParcelCadastreWizard","The map tool is about to change. Do you want to stop creating parcels?"),
                                     QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            # Disconnect signal that check if map tool change
            self.canvas.mapToolSet.disconnect(self.map_tool_changed)
            self.close()
        else:
            # Continue creating the Parcel
            self.canvas.mapToolSet.disconnect(self.map_tool_changed)
            self.canvas.setMapTool(old_tool)
            self.canvas.mapToolSet.connect(self.map_tool_changed)

    def closeEvent(self, event):
        # Close all open signal when object is destroyed
        sip.delete(self)

    def adjust_page_1_controls(self):

        self.gbx_page1.setTitle(QCoreApplication.translate("CreateParcelCadastreWizard", "How would you like to create parcels?    "))
        self.cbo_mapping.clear()
        self.cbo_mapping.addItem("")
        self.cbo_mapping.addItems(self.qgis_utils.get_field_mappings_file_names(PARCEL_TABLE))

        if self.rad_refactor.isChecked():
            self.lbl_refactor_source.setEnabled(True)
            self.mMapLayerComboBox.setEnabled(True)
            self.lbl_field_mapping.setEnabled(True)
            self.cbo_mapping.setEnabled(True)
            disable_next_wizard(self)
            self.wizardPage1.setFinalPage(True)
            self.txt_help_page_1.setHtml(self.help_strings.get_refactor_help_string(PARCEL_TABLE, False))
            finish_button_text = QCoreApplication.translate("CreateParcelCadastreWizard", "Import")
            self.wizardPage1.setButtonText(QWizard.FinishButton,finish_button_text)
        elif self.rad_parcel_from_plot.isChecked():
            self.lbl_refactor_source.setEnabled(False)
            self.mMapLayerComboBox.setEnabled(False)
            self.lbl_field_mapping.setEnabled(False)
            self.cbo_mapping.setEnabled(False)
            enable_next_wizard(self)
            self.wizardPage1.setFinalPage(False)
            finish_button_text = QCoreApplication.translate("CreateParcelCadastreWizard", "Create")
            self.txt_help_page_1.setHtml(self.help_strings.WIZ_CREATE_PARCEL_CADASTRE_PAGE_1_OPTION_EXISTING_PLOT)

        self.wizardPage2.setButtonText(QWizard.FinishButton,finish_button_text)

    def adjust_page_2_controls(self):

        self.gbx_page2.setTitle(QCoreApplication.translate("CreateParcelCadastreWizard", "What spatial unit do you want to associate the parcel with?    "))
        self.button(self.FinishButton).setDisabled(True)
        self.txt_help_page_2.setHtml(self.help_strings.WIZ_CREATE_PARCEL_CADASTRE_PAGE_2)

        # TODO:
        #  It is necesary becasuse when I got to back signal map_tool_changed it is not disconnect
        #  Remove when error are fixed
        self.button(QWizard.BackButton).hide()

        # Load layers
        result = self.prepare_parcel_creation_layers()

        if result:
            # Check if a previous features are selected
            self.check_selected_features()

            self.btn_plot_map.clicked.connect(partial(self.select_features_on_map, self._plot_layer))
            self.btn_building_map.clicked.connect(partial(self.select_features_on_map, self._building_layer))
            self.btn_building_unit_map.clicked.connect(partial(self.select_features_on_map, self._building_unit_layer))

            self.btn_plot_expression.clicked.connect(partial(self.select_features_by_expression, self._plot_layer))
            self.btn_building_expression.clicked.connect(partial(self.select_features_by_expression, self._building_layer))
            self.btn_building_unit_expression.clicked.connect(partial(self.select_features_by_expression, self._building_unit_layer))

    def select_features_on_map(self, layer):
        self._current_layer = layer
        self.iface.setActiveLayer(self._current_layer)
        self.setVisible(False)  # Make wizard disappear

        # Enable Select Map Tool
        if self._current_layer.name() == PLOT_TABLE:
            self.select_maptool = SelectMapTool(self.canvas, self._current_layer, multi=False)
        else:
            self.select_maptool = SelectMapTool(self.canvas, self._current_layer, multi=True)

        self.canvas.setMapTool(self.select_maptool)
        # Connect signal that check if map tool change
        # This is necessary after select the maptool
        self.canvas.mapToolSet.connect(self.map_tool_changed)

        # Connect signal that check a feature was selected
        self.select_maptool.features_selected_signal.connect(self.features_selected)

    def features_selected(self):
        self.setVisible(True)  # Make wizard appear
        self.check_selected_features()

        # Disconnect signal that check if map tool change
        # This is necessary before changing the tool to the user's previous selection
        self.canvas.mapToolSet.disconnect(self.map_tool_changed)
        self.canvas.setMapTool(self.maptool)

        self.log.logMessage("Select maptool SIGNAL disconnected", PLUGIN_NAME, Qgis.Info)
        self.select_maptool.features_selected_signal.disconnect(self.features_selected)

    def select_features_by_expression(self, layer):
        self._current_layer = layer
        self.iface.setActiveLayer(self._current_layer)
        Dlg_expression_selection = QgsExpressionSelectionDialog(self._current_layer)
        self._current_layer.selectionChanged.connect(self.check_selected_features)
        Dlg_expression_selection.exec()
        self._current_layer.selectionChanged.disconnect(self.check_selected_features)

    def check_selected_features(self):

        # Check selected features in plot layer
        if self._plot_layer.selectedFeatureCount():
            self.lb_plot.setText(QCoreApplication.translate("CreateParcelCadastreWizard", "<b>Plots</b>: {count} Feature Selected").format(count=self._plot_layer.selectedFeatureCount()))
        else:
            self.lb_plot.setText(QCoreApplication.translate("CreateParcelCadastreWizard", "<b>Plots</b>: 0 Features Selected"))

        # Check selected features in building layer
        if self._building_layer.selectedFeatureCount():
            self.lb_building.setText(QCoreApplication.translate("CreateParcelCadastreWizard", "<b>Buildings</b>: {count} Feature Selected").format(count=self._building_layer.selectedFeatureCount()))
        else:
            self.lb_building.setText(QCoreApplication.translate("CreateParcelCadastreWizard", "<b>Buildings</b>: 0 Features Selected"))

        # Check selected features in building unit layer
        if self._building_unit_layer.selectedFeatureCount():
            self.lb_building_unit.setText(QCoreApplication.translate("CreateParcelCadastreWizard", "<b>Building units</b>: {count} Feature Selected").format(count=self._building_unit_layer.selectedFeatureCount()))
        else:
            self.lb_building_unit.setText(QCoreApplication.translate("CreateParcelCadastreWizard", "<b>Building units</b>: 0 Features Selected"))

        if self._plot_layer.selectedFeatureCount() > 1:
            self.button(self.FinishButton).setDisabled(True)
        elif self._plot_layer.selectedFeatureCount() == 0 and self._building_layer.selectedFeatureCount() == 0 and self._building_unit_layer.selectedFeatureCount() == 0:
            self.button(self.FinishButton).setDisabled(True)
        else:
            self.button(self.FinishButton).setDisabled(False)

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

        # layers of interest are loaded
        result = self.prepare_parcel_creation_layers()

        if result:
            # Don't suppress (i.e., show) feature form
            form_config = self._parcel_layer.editFormConfig()
            form_config.setSuppress(QgsEditFormConfig.SuppressOff)
            self._parcel_layer.setEditFormConfig(form_config)
            self.edit_parcel()

    def prepare_parcel_creation_layers(self):
        # Load layers
        res_layers = self.qgis_utils.get_layers(self._db, {
            PLOT_TABLE: {'name': PLOT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry},
            PARCEL_TABLE: {'name': PARCEL_TABLE, 'geometry': None},
            BUILDING_TABLE: {'name': BUILDING_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry},
            BUILDING_UNIT_TABLE: {'name': BUILDING_UNIT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry},
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

        self._building_unit_layer = res_layers[BUILDING_UNIT_TABLE]
        if self._building_unit_layer is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                QCoreApplication.translate("CreateParcelCadastreWizard",
                                           "Building unit layer couldn't be found... {}").format(self._db.get_description()),
                Qgis.Warning)
            return

        self._uebaunit_table = res_layers[UEBAUNIT_TABLE]
        if self._uebaunit_table is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                QCoreApplication.translate("CreateParcelCadastreWizard",
                                           "UEBAUNIT table couldn't be found... {}").format(self._db.get_description()),
                Qgis.Warning)
            return

        # All layers were successfully loaded
        return True


    def edit_parcel(self):
        if self._plot_layer.selectedFeatureCount() == 0 and self._building_layer.selectedFeatureCount() == 0 and self._building_unit_layer.selectedFeatureCount() == 0 :
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                QCoreApplication.translate("CreateParcelCadastreWizard",
                                           "First select at least one Plot, one Building or one Building unit"),
                Qgis.Warning)
            return
        elif self._plot_layer.selectedFeatureCount() > 1:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                QCoreApplication.translate("CreateParcelCadastreWizard",
                                           "First select only one Plot"),
                Qgis.Warning)
            return

        # Open Form
        self.iface.layerTreeView().setCurrentLayer(self._parcel_layer)
        self._parcel_layer.startEditing()
        self.iface.actionAddFeature().trigger()

        ## TODO: Show selection page when all three layers have selections
        plot_ids = [f[ID_FIELD] for f in self._plot_layer.selectedFeatures()]
        building_ids = [f[ID_FIELD] for f in self._building_layer.selectedFeatures()]
        building_unit_ids = [f[ID_FIELD] for f in self._building_unit_layer.selectedFeatures()]

        # Create connections to react when a feature is added to buffer and
        # when it gets stored into the DB
        self._parcel_layer.featureAdded.connect(self.call_parcel_commit)
        self._parcel_layer.committedFeaturesAdded.connect(partial(self.finish_parcel, plot_ids, building_ids, building_unit_ids))

    def call_parcel_commit(self, fid):
        self._parcel_layer.featureAdded.disconnect(self.call_parcel_commit)
        self.log.logMessage("Parcel's featureAdded SIGNAL disconnected", PLUGIN_NAME, Qgis.Info)
        res = self._parcel_layer.commitChanges()

    def finish_parcel(self, plot_ids, building_ids, building_unit_ids, layerId, features):
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
                    self.log.logMessage("Saving Building-Parcel: {}-{}".format(building_id, parcel_id), PLUGIN_NAME,
                                        Qgis.Info)
                    new_features.append(new_feature)

                for building_unit_id in building_unit_ids:
                    new_feature = QgsVectorLayerUtils().createFeature(self._uebaunit_table)
                    new_feature.setAttribute(UEBAUNIT_TABLE_BUILDING_UNIT_FIELD, building_unit_id)
                    new_feature.setAttribute(UEBAUNIT_TABLE_PARCEL_FIELD, parcel_id)
                    self.log.logMessage("Saving Building Unit-Parcel: {}-{}".format(building_unit_id, parcel_id),
                                        PLUGIN_NAME, Qgis.Info)
                    new_features.append(new_feature)

                self._uebaunit_table.dataProvider().addFeatures(new_features)


                if plot_ids and building_ids and building_unit_ids:
                    self.iface.messageBar().pushMessage("Asistente LADM_COL",
                        QCoreApplication.translate("CreateParcelCadastreWizard",
                                                   "The new parcel (t_id={}) was successfully created and associated with its corresponding Plot (t_id={}) and Building(s) (t_id={}) and Building Unit(s) (t_id={})!").format(parcel_id, plot_ids[0], ", ".join([str(b) for b in building_ids]), ", ".join([str(b) for b in building_unit_ids])),
                        Qgis.Info)
                elif plot_ids and building_ids and not building_unit_ids:
                    self.iface.messageBar().pushMessage("Asistente LADM_COL",
                        QCoreApplication.translate("CreateParcelCadastreWizard",
                                                   "The new parcel (t_id={}) was successfully created and associated with its corresponding Plot (t_id={}) and Building(s) (t_id={})!").format(parcel_id, plot_ids[0], ", ".join([str(b) for b in building_ids])),
                        Qgis.Info)
                elif plot_ids and not building_ids and building_unit_ids:
                    self.iface.messageBar().pushMessage("Asistente LADM_COL",
                        QCoreApplication.translate("CreateParcelCadastreWizard",
                                                   "The new parcel (t_id={}) was successfully created and associated with its corresponding Plot (t_id={}) and Building Unit(s) (t_id={})!").format(parcel_id, plot_ids[0], ", ".join([str(b) for b in building_unit_ids])),
                        Qgis.Info)
                elif plot_ids and not building_ids and not building_unit_ids:
                    self.iface.messageBar().pushMessage("Asistente LADM_COL",
                        QCoreApplication.translate("CreateParcelCadastreWizard",
                                                   "The new parcel (t_id={}) was successfully created and associated with its corresponding Plot (t_id={})!").format(parcel_id, plot_ids[0]),
                        Qgis.Info)
                elif not plot_ids and building_ids and not building_unit_ids:
                    self.iface.messageBar().pushMessage("Asistente LADM_COL",
                        QCoreApplication.translate("CreateParcelCadastreWizard",
                                                   "The new parcel (t_id={}) was successfully created and associated with its corresponding Building(s) (t_id={})!").format(parcel_id, ", ".join([str(b) for b in building_ids])),
                        Qgis.Info)
                elif not plot_ids and building_ids and building_unit_ids:
                    self.iface.messageBar().pushMessage("Asistente LADM_COL",
                        QCoreApplication.translate("CreateParcelCadastreWizard",
                                                   "The new parcel (t_id={}) was successfully created and associated with its corresponding Building(s) (t_id={}) and Building Unit(s) (t_id={})!").format(parcel_id, ", ".join([str(b) for b in building_ids]), ", ".join([str(b) for b in building_unit_ids])),
                        Qgis.Info)
                elif not plot_ids and not building_ids and building_unit_ids:
                    self.iface.messageBar().pushMessage("Asistente LADM_COL",
                        QCoreApplication.translate("CreateParcelCadastreWizard",
                                                   "The new parcel (t_id={}) was successfully created and associated with its corresponding Building Unit(s) (t_id={})!").format(parcel_id, ", ".join([str(b) for b in building_unit_ids])),
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
