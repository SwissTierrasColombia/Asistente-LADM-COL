# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 15/01/19
        git sha              : :%H$
        copyright            : (C) 2019 by Sergio Ramírez (Incige SAS)
        email                : sergio.ramirez@incige.com
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

import sip
from qgis.PyQt.QtCore import (QCoreApplication,
                              QSettings)
from qgis.PyQt.QtWidgets import (QWizard,
                                 QMessageBox)

from qgis.core import (QgsEditFormConfig,
                       Qgis,
                       QgsMapLayerProxyModel,
                       QgsWkbTypes,
                       QgsApplication,
                       QgsVectorLayerUtils,
                       QgsTolerance,
                       QgsProject,
                       QgsSnappingConfig)
from qgis.gui import QgsExpressionSelectionDialog

from ..config.general_config import (PLUGIN_NAME,
                                     TranslatableConfigStrings,
                                     COLOR_ERROR_LABEL,
                                     COLOR_OKAY_LABEL,
                                     COLOR_INACTIVE_LABEL)
from ..config.help_strings import HelpStrings
from ..config.table_mapping_config import (EXTADDRESS_TABLE,
                                           EXTADDRESS_BUILDING_FIELD,
                                           EXTADDRESS_BUILDING_UNIT_FIELD,
                                           EXTADDRESS_PLOT_FIELD,
                                           BUILDING_TABLE,
                                           BUILDING_UNIT_TABLE,
                                           ID_FIELD,
                                           OID_EXTADDRESS_ID_FIELD,
                                           OID_TABLE,
                                           PLOT_TABLE)
from ..utils import get_ui_class
from ..utils.qt_utils import (enable_next_wizard,
                              disable_next_wizard)
from ..utils.select_map_tool import SelectMapTool

WIZARD_UI = get_ui_class('wiz_associate_extaddress_cadastre.ui')


class AssociateExtAddressWizard(QWizard, WIZARD_UI):
    def __init__(self, iface, db, qgis_utils, parent=None):
        QWizard.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self.log = QgsApplication.messageLog()
        self._db = db
        self.qgis_utils = qgis_utils
        self.help_strings = HelpStrings()
        self.translatable_config_strings = TranslatableConfigStrings()

        self.canvas = self.iface.mapCanvas()
        self.maptool = self.canvas.mapTool()
        self.select_maptool = None
        self._extaddress_layer = None
        self._plot_layer = None
        self._building_layer = None
        self._building_unit_layer = None
        self._current_layer = None
        self._extaddress_tid = None

        self.restore_settings()

        self.rad_spatial_unit.toggled.connect(self.adjust_page_1_controls)
        self.adjust_page_1_controls()

        self.button(QWizard.NextButton).clicked.connect(self.adjust_page_2_controls)
        self.button(QWizard.FinishButton).clicked.connect(self.finished_dialog)
        self.button(QWizard.HelpButton).clicked.connect(self.show_help)

        self.mMapLayerComboBox.setFilters(QgsMapLayerProxyModel.PolygonLayer)

    def map_tool_changed(self, new_tool, old_tool):
        self.canvas.mapToolSet.disconnect(self.map_tool_changed)
        reply = QMessageBox.question(self,
                                     QCoreApplication.translate("AssociateExtAddressWizard", "Stop address creation?"),
                                     QCoreApplication.translate("AssociateExtAddressWizard",
                                                                "The map tool is about to change. Do you want to stop creating addresses?"),
                                     QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            # Disconnect signal that check if map tool change
            self.close()
        else:
            # Continue creating the ExtAddress
            self.canvas.setMapTool(old_tool)
            self.canvas.mapToolSet.connect(self.map_tool_changed)

    def closeEvent(self, event):
        # Close all open signal when object is destroyed
        sip.delete(self)

    def adjust_page_1_controls(self):
        self.gbx_page1.setTitle(QCoreApplication.translate("AssociateExtAddressWizard",
                                                           "How would you like to create and associate addresses?"))
        self.cbo_mapping.clear()
        self.cbo_mapping.addItem("")
        self.cbo_mapping.addItems(self.qgis_utils.get_field_mappings_file_names(EXTADDRESS_TABLE))

        if self.rad_refactor.isChecked():
            self.lbl_refactor_source.setEnabled(True)
            self.mMapLayerComboBox.setEnabled(True)
            self.lbl_field_mapping.setEnabled(True)
            self.cbo_mapping.setEnabled(True)
            disable_next_wizard(self)
            self.wizardPage1.setFinalPage(True)
            self.txt_help_page_1.setHtml(self.help_strings.get_refactor_help_string(EXTADDRESS_TABLE, True))
            finish_button_text = QCoreApplication.translate("AssociateExtAddressWizard", "Import")
            self.wizardPage1.setButtonText(QWizard.FinishButton, finish_button_text)

        elif self.rad_spatial_unit.isChecked():
            self.lbl_refactor_source.setEnabled(False)
            self.mMapLayerComboBox.setEnabled(False)
            self.lbl_field_mapping.setEnabled(False)
            self.cbo_mapping.setEnabled(False)
            self.wizardPage1.setFinalPage(False)
            enable_next_wizard(self)
            self.wizardPage1.setFinalPage(False)
            finish_button_text = QCoreApplication.translate("AssociateExtAddressWizard",
                                                            "Associate address with spatial unit")
            self.txt_help_page_1.setHtml(self.help_strings.WIZ_ASSOCIATE_EXTADDRESS_CADASTRE_PAGE_1)

        self.wizardPage2.setButtonText(QWizard.FinishButton, finish_button_text)

    def adjust_page_2_controls(self):
        self.gbx_page2.setTitle(QCoreApplication.translate("AssociateExtAddressWizard",
                                                           "Associate the new address with these spatial unit(s):"))
        self.button(self.FinishButton).setDisabled(True)
        self.disconnect_signals()

        # Load layers
        result = self.prepare_extaddress_creation_layers()

        if result:
            # Check if a previous features are selected
            self.check_selected_features()

            self.btn_plot_map.clicked.connect(partial(self.select_features_on_map, self._plot_layer))
            self.btn_building_map.clicked.connect(partial(self.select_features_on_map, self._building_layer))
            self.btn_building_unit_map.clicked.connect(partial(self.select_features_on_map, self._building_unit_layer))

            self.btn_plot_expression.clicked.connect(partial(self.select_feature_by_expression, self._plot_layer))
            self.btn_building_expression.clicked.connect(partial(self.select_feature_by_expression, self._building_layer))
            self.btn_building_unit_expression.clicked.connect(partial(self.select_feature_by_expression, self._building_unit_layer))

        self.rad_to_plot.toggled.connect(self.toggle_spatial_unit)
        self.rad_to_building.toggled.connect(self.toggle_spatial_unit)
        self.rad_to_building_unit.toggled.connect(self.toggle_spatial_unit)
        self.toggle_spatial_unit()

    def disconnect_signals(self):
        signals = [self.btn_plot_map,
                   self.btn_building_map,
                   self.btn_building_unit_map,
                   self.btn_plot_expression,
                   self.btn_building_expression,
                   self.btn_building_unit_expression,
                   self.canvas.mapToolSet]

        for signal in signals:
            try:
                signal.disconnect()
            except:
                pass

    def toggle_spatial_unit(self):

        self.btn_plot_map.setEnabled(False)
        self.btn_building_map.setEnabled(False)
        self.btn_building_unit_map.setEnabled(False)

        self.btn_plot_expression.setEnabled(False)
        self.btn_building_expression.setEnabled(False)
        self.btn_building_unit_expression.setEnabled(False)

        if self.rad_to_plot.isChecked():
            self.txt_help_page_2.setHtml(self.help_strings.WIZ_ASSOCIATE_EXTADDRESS_CADASTRE_PAGE_2_OPTION_1)
            self._current_layer = self._plot_layer

            self.btn_plot_map.setEnabled(True)
            self.btn_plot_expression.setEnabled(True)

        elif self.rad_to_building.isChecked():
            self.txt_help_page_2.setHtml(self.help_strings.WIZ_ASSOCIATE_EXTADDRESS_CADASTRE_PAGE_2_OPTION_2)
            self._current_layer = self._building_layer

            self.btn_building_map.setEnabled(True)
            self.btn_building_expression.setEnabled(True)

        elif self.rad_to_building_unit.isChecked():
            self.txt_help_page_2.setHtml(self.help_strings.WIZ_ASSOCIATE_EXTADDRESS_CADASTRE_PAGE_2_OPTION_3)
            self._current_layer = self._building_unit_layer

            self.btn_building_unit_map.setEnabled(True)
            self.btn_building_unit_expression.setEnabled(True)

        self.iface.setActiveLayer(self._current_layer)
        self.check_selected_features()

    def prepare_extaddress_creation_layers(self):
        # Load layers
        res_layers = self.qgis_utils.get_layers(self._db, {
            EXTADDRESS_TABLE: {'name': EXTADDRESS_TABLE, 'geometry': QgsWkbTypes.PointGeometry},
            OID_TABLE: {'name': OID_TABLE, 'geometry': None},
            PLOT_TABLE: {'name': PLOT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry},
            BUILDING_TABLE: {'name': BUILDING_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry},
            BUILDING_UNIT_TABLE: {'name': BUILDING_UNIT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry}
        }, load=True)

        self._extaddress_layer = res_layers[EXTADDRESS_TABLE]
        if self._extaddress_layer is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                                QCoreApplication.translate("AssociateExtAddressWizard",
                                                                           "ExtAddress layer couldn't be found... {}").format(
                                                    self._db.get_description()),
                                                Qgis.Warning)
            return

        self._oid_layer = res_layers[OID_TABLE]
        if self._oid_layer is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                                QCoreApplication.translate("AssociateExtAddressWizard",
                                                                           "OID layer couldn't be found... {}").format(
                                                    self._db.get_description()),
                                                Qgis.Warning)
            return

        self._plot_layer = res_layers[PLOT_TABLE]
        if self._plot_layer is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                                QCoreApplication.translate("AssociateExtAddressWizard",
                                                                           "Plot layer couldn't be found... {}").format(
                                                    self._db.get_description()),
                                                Qgis.Warning)
            return

        self._building_layer = res_layers[BUILDING_TABLE]
        if self._building_layer is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                                QCoreApplication.translate("AssociateExtAddressWizard",
                                                                           "Building layer couldn't be found... {}").format(
                                                    self._db.get_description()),
                                                Qgis.Warning)
            return

        self._building_unit_layer = res_layers[BUILDING_UNIT_TABLE]
        if self._building_unit_layer is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                                QCoreApplication.translate("AssociateExtAddressWizard",
                                                                           "Building unit layer couldn't be found... {}").format(
                                                    self._db.get_description()),
                                                Qgis.Warning)
            return

        # All layers were successfully loaded
        return True

    def check_selected_features(self):

        self.rad_to_plot.setText(QCoreApplication.translate("AssociateExtAddressWizard", "Plot(s): {count} Feature(s) Selected").format(count=self._plot_layer.selectedFeatureCount()))
        self.rad_to_building.setText(QCoreApplication.translate("AssociateExtAddressWizard", "Building(s): {count} Feature(s) Selected").format(count=self._building_layer.selectedFeatureCount()))
        self.rad_to_building_unit.setText(QCoreApplication.translate("AssociateExtAddressWizard", "Building unit(s): {count} Feature(s) Selected").format(count=self._building_unit_layer.selectedFeatureCount()))

        if self._current_layer is None:
            if self.iface.activeLayer().name() == PLOT_TABLE:
                self.rad_to_plot.setChecked(True)
                self._current_layer = self._plot_layer
            elif self.iface.activeLayer().name() == BUILDING_TABLE:
                self.rad_to_building.setChecked(True)
                self._current_layer = self._building_layer
            elif self.iface.activeLayer().name() == BUILDING_UNIT_TABLE:
                self.rad_to_building_unit.setChecked(True)
                self._current_layer = self._building_unit_layer
            else:
                # Select layer that have least one feature selected
                # as current layer when current layer is not defined
                if self._plot_layer.selectedFeatureCount():
                    self.rad_to_plot.setChecked(True)
                    self._current_layer = self._plot_layer
                elif self._building_layer.selectedFeatureCount():
                    self.rad_to_building.setChecked(True)
                    self._current_layer = self._building_layer
                elif self._building_unit_layer.selectedFeatureCount():
                    self.rad_to_building_unit.setChecked(True)
                    self._current_layer = self._building_unit_layer
                else:
                    # By default current_layer will be plot layer
                    self.rad_to_plot.setChecked(True)
                    self._current_layer = self._plot_layer

        if self.rad_to_plot.isChecked():
            self.rad_to_building.setStyleSheet(COLOR_INACTIVE_LABEL)
            self.rad_to_building_unit.setStyleSheet(COLOR_INACTIVE_LABEL)

            # Check selected features in plot layer
            if self._plot_layer.selectedFeatureCount() == 1:
                self.rad_to_plot.setStyleSheet(COLOR_OKAY_LABEL)
            elif self._plot_layer.selectedFeatureCount() > 1:
                # the color of the text is changed to highlight when there are more than one feature selected
                self.rad_to_plot.setStyleSheet(COLOR_ERROR_LABEL)
            else:
                # the color of the text is changed to highlight that there is no selection
                self.rad_to_plot.setStyleSheet(COLOR_ERROR_LABEL)

        elif self.rad_to_building.isChecked():
            self.rad_to_plot.setStyleSheet(COLOR_INACTIVE_LABEL)
            self.rad_to_building_unit.setStyleSheet(COLOR_INACTIVE_LABEL)

            # Check selected features in building layer
            if self._building_layer.selectedFeatureCount() == 1:
                self.rad_to_building.setStyleSheet(COLOR_OKAY_LABEL)
            elif self._building_layer.selectedFeatureCount() > 1:
                # the color of the text is changed to highlight when there are more than one feature selected
                self.rad_to_building.setStyleSheet(COLOR_ERROR_LABEL)
            else:
                # the color of the text is changed to highlight that there is no selection
                self.rad_to_building.setStyleSheet(COLOR_ERROR_LABEL)

        elif self.rad_to_building_unit.isChecked():
            self.rad_to_plot.setStyleSheet(COLOR_INACTIVE_LABEL)
            self.rad_to_building.setStyleSheet(COLOR_INACTIVE_LABEL)

            # Check selected features in building unit layer
            if self._building_unit_layer.selectedFeatureCount() == 1:
                self.rad_to_building_unit.setStyleSheet(COLOR_OKAY_LABEL)
            elif self._building_unit_layer.selectedFeatureCount() > 1:
                # the color of the text is changed to highlight when there are more than one features selected
                self.rad_to_building_unit.setStyleSheet(COLOR_ERROR_LABEL)
            else:
                # the color of the text is changed to highlight that there is no selection
                self.rad_to_building_unit.setStyleSheet(COLOR_ERROR_LABEL)

        # Zoom to selected feature
        self.canvas.zoomToSelected(self._current_layer)

        # Condition for enabling the finish button
        if self.rad_to_plot.isChecked() and self._plot_layer.selectedFeatureCount() == 1:
            self.button(self.FinishButton).setDisabled(False)
        elif self.rad_to_building.isChecked() and self._building_layer.selectedFeatureCount() == 1:
            self.button(self.FinishButton).setDisabled(False)
        elif self.rad_to_building_unit.isChecked() and self._building_unit_layer.selectedFeatureCount() == 1:
            self.button(self.FinishButton).setDisabled(False)
        else:
            self.button(self.FinishButton).setDisabled(True)

    def select_features_on_map(self, layer):
        self._current_layer = layer
        self.iface.setActiveLayer(self._current_layer)
        self.setVisible(False)  # Make wizard disappear

        # Enable Select Map Tool
        self.select_maptool = SelectMapTool(self.canvas, self._current_layer, multi=False)

        self.canvas.setMapTool(self.select_maptool)
        # Connect signal that check if map tool change
        # This is necessary after select the maptool
        self.canvas.mapToolSet.connect(self.map_tool_changed)

        # Connect signal that checks a feature was selected
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

    def select_feature_by_expression(self, layer):
        self._current_layer = layer
        self.iface.setActiveLayer(self._current_layer)
        dlg_expression_selection = QgsExpressionSelectionDialog(self._current_layer)
        self._current_layer.selectionChanged.connect(self.check_selected_features)
        dlg_expression_selection.exec()
        self._current_layer.selectionChanged.disconnect(self.check_selected_features)

    def finished_dialog(self):
        self.save_settings()

        if self.rad_refactor.isChecked():
            if self.mMapLayerComboBox.currentLayer() is not None:
                field_mapping = self.cbo_mapping.currentText()
                res_etl_model = self.qgis_utils.show_etl_model(self._db,
                                                               self.mMapLayerComboBox.currentLayer(),
                                                               EXTADDRESS_TABLE,
                                                               field_mapping=field_mapping)

                if res_etl_model:
                    if field_mapping:
                        self.qgis_utils.delete_old_field_mapping(field_mapping)

                    self.qgis_utils.save_field_mapping(EXTADDRESS_TABLE)

            else:
                self.iface.messageBar().pushMessage('Asistente LADM_COL',
                                                    QCoreApplication.translate("AssociateExtAddressWizard",
                                                                               "Select a source layer to set the field mapping to '{}'.").format(
                                                        EXTADDRESS_TABLE),
                                                    Qgis.Warning)

        else:
            self.prepare_extaddress_creation()

    def prepare_extaddress_creation(self):
        result = self.prepare_extaddress_creation_layers()
        if result:
            # Don't suppress (i.e., show) feature form
            form_config = self._extaddress_layer.editFormConfig()
            form_config.setSuppress(QgsEditFormConfig.SuppressOff)
            self._extaddress_layer.setEditFormConfig(form_config)

            # Suppress (i.e., hide) feature form
            form_config = self._oid_layer.editFormConfig()
            form_config.setSuppress(QgsEditFormConfig.SuppressOn)
            self._oid_layer.setEditFormConfig(form_config)

            self.edit_extaddress()

    def edit_extaddress(self):
        if self._current_layer.selectedFeatureCount() == 1:
            # Open Form
            self.iface.layerTreeView().setCurrentLayer(self._extaddress_layer)
            self._extaddress_layer.startEditing()
            self.iface.actionAddFeature().trigger()

            # Configure Snapping
            snapping = QgsProject.instance().snappingConfig()
            snapping.setEnabled(True)
            snapping.setMode(QgsSnappingConfig.AllLayers)
            snapping.setType(QgsSnappingConfig.Vertex)
            snapping.setUnits(QgsTolerance.Pixels)
            snapping.setTolerance(12)
            QgsProject.instance().setSnappingConfig(snapping)

            # Create connections to react when a feature is added to buffer and
            # when it gets stored into the DB
            self._extaddress_layer.featureAdded.connect(self.call_extaddress_commit)

            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                            QCoreApplication.translate("AssociateExtAddressWizard",
                                                                       "Now you can click on the map to locate the new address..."),
                                            Qgis.Info)
        else:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                                QCoreApplication.translate("AssociateExtAddressWizard",
                                                                           "First select a {}.").format(self._current_layer.name()),
                                                Qgis.Warning)

    def call_extaddress_commit(self, fid):
        self._extaddress_tid = self._extaddress_layer.getFeature(fid)[ID_FIELD] # t_id of the new ext_address
        feature_id = self._current_layer.selectedFeatures()[0][ID_FIELD] # Get t_id of feature to associate

        if self._current_layer.name() == PLOT_TABLE:
            plot_field_idx = self._extaddress_layer.getFeature(fid).fieldNameIndex(EXTADDRESS_PLOT_FIELD)
            self._extaddress_layer.changeAttributeValue(fid, plot_field_idx, feature_id)
        elif self._current_layer.name() == BUILDING_TABLE:
            building_field_idx = self._extaddress_layer.getFeature(fid).fieldNameIndex(EXTADDRESS_BUILDING_FIELD)
            self._extaddress_layer.changeAttributeValue(fid, building_field_idx, feature_id)
        elif self._current_layer.name() == BUILDING_UNIT_TABLE:
            building_unit_field_idx = self._extaddress_layer.getFeature(fid).fieldNameIndex(
                EXTADDRESS_BUILDING_UNIT_FIELD)
            self._extaddress_layer.changeAttributeValue(fid, building_unit_field_idx, feature_id)

        self._extaddress_layer.featureAdded.disconnect(self.call_extaddress_commit)
        self.log.logMessage("Extaddress's featureAdded SIGNAL disconnected", PLUGIN_NAME, Qgis.Info)
        res = self._extaddress_layer.commitChanges()
        self._current_layer.removeSelection()
        self.add_oid_feature()

        self.iface.messageBar().pushMessage("Asistente LADM_COL",
            QCoreApplication.translate("AssociateExtAddressWizard",
                "The new address (t_id={}) was successfully created and associated with its corresponding '{}' (t_id={})!").format(
                self._extaddress_tid, self._current_layer.name(), feature_id),
            Qgis.Info)

    def add_oid_feature(self):
        # Add OID record
        self._oid_layer.startEditing()
        feature = QgsVectorLayerUtils().createFeature(self._oid_layer)
        feature.setAttribute(OID_EXTADDRESS_ID_FIELD, self._extaddress_tid)
        self._oid_layer.addFeature(feature)
        self._oid_layer.commitChanges()

    def save_settings(self):
        settings = QSettings()

        load_data_type = 'refactor'
        if self.rad_spatial_unit.isChecked():
            load_data_type = 'to_spatial_unit'

        settings.setValue('Asistente-LADM_COL/wizards/ext_address_load_data_type', load_data_type)

    def restore_settings(self):
        settings = QSettings()

        load_data_type = settings.value('Asistente-LADM_COL/wizards/ext_address_load_data_type', 'to_plot')
        if load_data_type == 'refactor':
            self.rad_refactor.setChecked(True)
        else:
            self.rad_spatial_unit.setChecked(True)

    def show_help(self):
        self.qgis_utils.show_help("associate_ext_address")
