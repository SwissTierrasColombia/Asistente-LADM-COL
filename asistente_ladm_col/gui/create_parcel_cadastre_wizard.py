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
                              Qt,
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

from ..config.general_config import (PLUGIN_NAME,
                                     CSS_COLOR_ERROR_LABEL,
                                     CSS_COLOR_OKAY_LABEL,
                                     CSS_COLOR_INACTIVE_LABEL)
from ..config.help_strings import HelpStrings
from ..config.table_mapping_config import (BUILDING_TABLE,
                                           BUILDING_UNIT_TABLE,
                                           ID_FIELD,
                                           PARCEL_TABLE,
                                           PARCEL_TYPE_FIELD,
                                           PLOT_TABLE,
                                           UEBAUNIT_TABLE,
                                           UEBAUNIT_TABLE_BUILDING_FIELD,
                                           UEBAUNIT_TABLE_BUILDING_UNIT_FIELD,
                                           UEBAUNIT_TABLE_PARCEL_FIELD,
                                           UEBAUNIT_TABLE_PLOT_FIELD,
                                           CONSTRAINT_TYPES_OF_PARCEL)
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

        self._layers = {
            PLOT_TABLE: {'name': PLOT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry, 'layer': None},
            PARCEL_TABLE: {'name': PARCEL_TABLE, 'geometry': None, 'layer': None},
            BUILDING_TABLE: {'name': BUILDING_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry, 'layer': None},
            BUILDING_UNIT_TABLE: {'name': BUILDING_UNIT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry, 'layer': None},
            UEBAUNIT_TABLE: {'name': UEBAUNIT_TABLE, 'geometry': None, 'layer': None}
        }

        self._spatial_unit_layers = dict()
        self.type_of_parcel_selected = None
        self._db = db
        self.qgis_utils = qgis_utils
        self.help_strings = HelpStrings()

        self.restore_settings()

        self.rad_parcel_from_plot.toggled.connect(self.adjust_page_1_controls)
        self.adjust_page_1_controls()
        self.button(QWizard.NextButton).clicked.connect(self.adjust_page_2_controls)
        self.button(QWizard.FinishButton).clicked.connect(self.finished_dialog)
        self.button(QWizard.HelpButton).clicked.connect(self.show_help)
        self.rejected.connect(self.close_wizard)
        self.mMapLayerComboBox.setFilters(QgsMapLayerProxyModel.NoGeometry)

    def map_tool_changed(self, new_tool, old_tool):
        self.canvas.mapToolSet.disconnect(self.map_tool_changed)
        reply = QMessageBox.question(self,
                                     QCoreApplication.translate("CreateParcelCadastreWizard", "Stop parcel creation?"),
                                     QCoreApplication.translate("CreateParcelCadastreWizard","The map tool is about to change. Do you want to stop creating parcels?"),
                                     QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.close_wizard()
        else:
            # Continue creating the Parcel
            self.canvas.setMapTool(old_tool)
            self.canvas.mapToolSet.connect(self.map_tool_changed)

    def closeEvent(self, event):
        self.close_wizard()

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
        self.button(self.FinishButton).setDisabled(True)
        self.disconnect_signals()

        # Load layers
        result = self.prepare_parcel_creation_layers()

        if result is None:
            # if there was a problem loading the layers
            self.close_wizard()
            return

        if self.cb_parcel_type.count() == 0:
            for parcel_type in CONSTRAINT_TYPES_OF_PARCEL:
                self.cb_parcel_type.addItem(parcel_type)

            # Select previous option saved
            if self.type_of_parcel_selected:
                index = self.cb_parcel_type.findText(self.type_of_parcel_selected)
                if index != -1:
                    self.cb_parcel_type.setCurrentIndex(index)

        self.cb_parcel_type.currentTextChanged.connect(self.validate_type_of_parcel)
        self.cb_parcel_type.currentTextChanged.emit(self.cb_parcel_type.currentText())

        if result:
            # Check if a previous features are selected
            self.check_selected_features()

            self.btn_plot_map.clicked.connect(partial(self.select_features_on_map, self._layers[PLOT_TABLE]['layer']))
            self.btn_building_map.clicked.connect(partial(self.select_features_on_map, self._layers[BUILDING_TABLE]['layer']))
            self.btn_building_unit_map.clicked.connect(partial(self.select_features_on_map, self._layers[BUILDING_UNIT_TABLE]['layer']))

            self.btn_plot_expression.clicked.connect(partial(self.select_features_by_expression, self._layers[PLOT_TABLE]['layer']))
            self.btn_building_expression.clicked.connect(partial(self.select_features_by_expression, self._layers[BUILDING_TABLE]['layer']))
            self.btn_building_unit_expression.clicked.connect(partial(self.select_features_by_expression, self._layers[BUILDING_UNIT_TABLE]['layer']))

    def validate_type_of_parcel(self, parcel_type):
        # Activate all push buttons
        self.btn_plot_map.setEnabled(True)
        self.btn_plot_expression.setEnabled(True)
        self.btn_building_map.setEnabled(True)
        self.btn_building_expression.setEnabled(True)
        self.btn_building_unit_map.setEnabled(True)
        self.btn_building_unit_expression.setEnabled(True)

        # Disable labels/controls depending on parcel_type
        for spatial_unit in CONSTRAINT_TYPES_OF_PARCEL[parcel_type]:
            if CONSTRAINT_TYPES_OF_PARCEL[parcel_type][spatial_unit] == None:
                if spatial_unit == PLOT_TABLE:
                    self.btn_plot_map.setEnabled(False)
                    self.btn_plot_expression.setEnabled(False)
                elif spatial_unit == BUILDING_TABLE:
                    self.btn_building_map.setEnabled(False)
                    self.btn_building_expression.setEnabled(False)
                elif spatial_unit == BUILDING_UNIT_TABLE:
                    self.btn_building_unit_map.setEnabled(False)
                    self.btn_building_unit_expression.setEnabled(False)

        self.update_help_message(parcel_type)
        self.check_selected_features()

    def update_help_message(self, parcel_type):
        msg_parcel_type = self.help_strings.MESSAGE_PARCEL_TYPES[parcel_type]
        msg_help = self.help_strings.WIZ_CREATE_PARCEL_CADASTRE_PAGE_2.format(msg_parcel_type=msg_parcel_type)
        self.txt_help_page_2.setHtml(msg_help)

    def is_constraint_satisfied(self, type):
        result = True
        for spatial_unit in CONSTRAINT_TYPES_OF_PARCEL[type]:
            _layer = self._spatial_unit_layers[spatial_unit]

            if CONSTRAINT_TYPES_OF_PARCEL[type][spatial_unit] == 1 and not _layer.selectedFeatureCount() == 1:
                result = False
            elif CONSTRAINT_TYPES_OF_PARCEL[type][spatial_unit] == '+' and _layer.selectedFeatureCount() < 1:
                result = False

        return result

    def disconnect_signals(self):
        # GUI Wizard
        signals = [self.btn_plot_map.clicked,
                   self.btn_building_map.clicked,
                   self.btn_building_unit_map.clicked,
                   self.btn_plot_expression.clicked,
                   self.btn_building_expression.clicked,
                   self.btn_building_unit_expression.clicked,
                   self.cb_parcel_type.currentTextChanged]
        for signal in signals:
            try:
                signal.disconnect()
            except:
                pass

        # QGIS APP
        try:
            self.canvas.mapToolSet.disconnect(self.map_tool_changed)
        except:
            pass

        try:
            self._layers[PARCEL_TABLE]['layer'].committedFeaturesAdded.disconnect(self.finish_parcel)
        except:
            pass

        layers = [self._layers[PLOT_TABLE]['layer'],
                  self._layers[PARCEL_TABLE]['layer'],
                  self._layers[BUILDING_TABLE]['layer'],
                  self._layers[BUILDING_UNIT_TABLE]['layer'],
                  self._layers[UEBAUNIT_TABLE]['layer']]

        for layer in layers:
            try:
                layer.willBeDeleted.disconnect(self.layer_removed)
            except:
                pass

    def select_features_on_map(self, layer):
        self._current_layer = layer
        self.iface.setActiveLayer(self._current_layer)
        self.setVisible(False)  # Make wizard disappear

        # Enable Select Map Tool
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
        dlg_expression_selection = QgsExpressionSelectionDialog(self._current_layer)
        self._current_layer.selectionChanged.connect(self.check_selected_features)
        dlg_expression_selection.exec()
        self._current_layer.selectionChanged.disconnect(self.check_selected_features)

    def check_selected_features(self):
        self.lb_plot.setText(QCoreApplication.translate("CreateParcelCadastreWizard", "<b>Plot(s)</b>: {count} Feature(s) Selected").format(count=self._layers[PLOT_TABLE]['layer'].selectedFeatureCount()))
        self.lb_plot.setStyleSheet(CSS_COLOR_OKAY_LABEL)  # Default color
        self.lb_building.setText(QCoreApplication.translate("CreateParcelCadastreWizard","<b>Building(s)</b>: {count} Feature(s) Selected").format(count=self._layers[BUILDING_TABLE]['layer'].selectedFeatureCount()))
        self.lb_building.setStyleSheet(CSS_COLOR_OKAY_LABEL)  # Default color
        self.lb_building_unit.setText(QCoreApplication.translate("CreateParcelCadastreWizard","<b>Building unit(s)</b>: {count} Feature(s) Selected").format(count=self._layers[BUILDING_UNIT_TABLE]['layer'].selectedFeatureCount()))
        self.lb_building_unit.setStyleSheet(CSS_COLOR_OKAY_LABEL)  # Default color

        parcel_type = self.cb_parcel_type.currentText()
        for spatial_unit in CONSTRAINT_TYPES_OF_PARCEL[parcel_type]:
            _layer = self._spatial_unit_layers[spatial_unit]

            _color = CSS_COLOR_OKAY_LABEL

            if CONSTRAINT_TYPES_OF_PARCEL[parcel_type][spatial_unit] == 1 and not _layer.selectedFeatureCount() == 1:
                    _color = CSS_COLOR_ERROR_LABEL
            elif CONSTRAINT_TYPES_OF_PARCEL[parcel_type][spatial_unit] == '+' and _layer.selectedFeatureCount() < 1:
                    _color = CSS_COLOR_ERROR_LABEL
            elif CONSTRAINT_TYPES_OF_PARCEL[parcel_type][spatial_unit] == None:
                _color = CSS_COLOR_INACTIVE_LABEL

            if spatial_unit == PLOT_TABLE:
                self.lb_plot.setStyleSheet(_color)
            elif spatial_unit == BUILDING_TABLE:
                self.lb_building.setStyleSheet(_color)
            elif spatial_unit == BUILDING_UNIT_TABLE:
                self.lb_building_unit.setStyleSheet(_color)

        self.button(self.FinishButton).setEnabled(self.is_constraint_satisfied(parcel_type))

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
        if result is None:
            return

        if result:
            # Don't suppress (i.e., show) feature form
            form_config = self._layers[PARCEL_TABLE]['layer'].editFormConfig()
            form_config.setSuppress(QgsEditFormConfig.SuppressOff)
            self._layers[PARCEL_TABLE]['layer'].setEditFormConfig(form_config)
            self.edit_parcel()

    def prepare_parcel_creation_layers(self):
        # Load layers
        res_layers = self.qgis_utils.get_layers(self._db, self._layers, load=True)
        if res_layers is None:
            return

        # Add signal to check if a layer was removed
        self.validate_remove_layers()

        self._spatial_unit_layers = {
            PLOT_TABLE: self._layers[PLOT_TABLE]['layer'],
            BUILDING_TABLE: self._layers[BUILDING_TABLE]['layer'],
            BUILDING_UNIT_TABLE: self._layers[BUILDING_UNIT_TABLE]['layer']
        }

        # All layers were successfully loaded
        return True

    def validate_remove_layers(self):
        for layer_name in self._layers:
            if self._layers[layer_name]['layer']:
                # Layer was found, listen to its removal so that we can update the variable properly
                try:
                    self._layers[layer_name]['layer'].willBeDeleted.disconnect(self.layer_removed)
                except:
                    pass
                self._layers[layer_name]['layer'].willBeDeleted.connect(self.layer_removed)

    def layer_removed(self):
        self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                            QCoreApplication.translate("CreateParcelCadastreWizard",
                                                                       "'Create parcel' tool has been closed because you just removed a required layer."),
                                            Qgis.Info)
        self.close_wizard()

    def close_wizard(self):
        self.init_map_tool()
        self.disconnect_signals()
        self.close()

    def init_map_tool(self):
        try:
            self.canvas.mapToolSet.disconnect(self.map_tool_changed)
        except:
            pass
        self.canvas.setMapTool(self.maptool)

    def edit_parcel(self):
        self.iface.layerTreeView().setCurrentLayer(self._layers[PARCEL_TABLE]['layer'])
        self._layers[PARCEL_TABLE]['layer'].committedFeaturesAdded.connect(self.finish_parcel)
        self.open_form(self._layers[PARCEL_TABLE]['layer'])

    def finish_parcel(self, layerId, features):

        if len(features) != 1:
            self.log.logMessage("We should have got only one predio... We cannot do anything with {} predios".format(len(features)), PLUGIN_NAME, Qgis.Warning)
        else:
            fid = features[0].id()

            if not self._layers[PARCEL_TABLE]['layer'].getFeature(fid).isValid():
                self.log.logMessage("Feature not found in layer Predio...", PLUGIN_NAME, Qgis.Warning)
            else:
                parcel_id = self._layers[PARCEL_TABLE]['layer'].getFeature(fid)[ID_FIELD]

                plot_ids = list()
                building_ids = list()
                building_unit_ids = list()

                # Apply restriction to the selection
                if PLOT_TABLE in CONSTRAINT_TYPES_OF_PARCEL[self.cb_parcel_type.currentText()]:
                    if CONSTRAINT_TYPES_OF_PARCEL[self.cb_parcel_type.currentText()][PLOT_TABLE] is not None:
                        plot_ids = [f[ID_FIELD] for f in self._layers[PLOT_TABLE]['layer'].selectedFeatures()]
                else:
                    plot_ids = [f[ID_FIELD] for f in self._layers[PLOT_TABLE]['layer'].selectedFeatures()]

                if BUILDING_TABLE in CONSTRAINT_TYPES_OF_PARCEL[self.cb_parcel_type.currentText()]:
                    if CONSTRAINT_TYPES_OF_PARCEL[self.cb_parcel_type.currentText()][BUILDING_TABLE] is not None:
                        building_ids = [f[ID_FIELD] for f in self._layers[BUILDING_TABLE]['layer'].selectedFeatures()]
                else:
                    building_ids = [f[ID_FIELD] for f in self._layers[BUILDING_TABLE]['layer'].selectedFeatures()]

                if BUILDING_UNIT_TABLE in CONSTRAINT_TYPES_OF_PARCEL[self.cb_parcel_type.currentText()]:
                    if CONSTRAINT_TYPES_OF_PARCEL[self.cb_parcel_type.currentText()][BUILDING_UNIT_TABLE] is not None:
                        building_unit_ids = [f[ID_FIELD] for f in
                                             self._layers[BUILDING_UNIT_TABLE]['layer'].selectedFeatures()]
                else:
                    building_unit_ids = [f[ID_FIELD] for f in
                                         self._layers[BUILDING_UNIT_TABLE]['layer'].selectedFeatures()]

                # Fill uebaunit table
                new_features = []
                for plot_id in plot_ids:
                    new_feature = QgsVectorLayerUtils().createFeature(self._layers[UEBAUNIT_TABLE]['layer'])
                    new_feature.setAttribute(UEBAUNIT_TABLE_PLOT_FIELD, plot_id)
                    new_feature.setAttribute(UEBAUNIT_TABLE_PARCEL_FIELD, parcel_id)
                    self.log.logMessage("Saving Plot-Parcel: {}-{}".format(plot_id, parcel_id), PLUGIN_NAME, Qgis.Info)
                    new_features.append(new_feature)

                for building_id in building_ids:
                    new_feature = QgsVectorLayerUtils().createFeature(self._layers[UEBAUNIT_TABLE]['layer'])
                    new_feature.setAttribute(UEBAUNIT_TABLE_BUILDING_FIELD, building_id)
                    new_feature.setAttribute(UEBAUNIT_TABLE_PARCEL_FIELD, parcel_id)
                    self.log.logMessage("Saving Building-Parcel: {}-{}".format(building_id, parcel_id), PLUGIN_NAME,
                                        Qgis.Info)
                    new_features.append(new_feature)

                for building_unit_id in building_unit_ids:
                    new_feature = QgsVectorLayerUtils().createFeature(self._layers[UEBAUNIT_TABLE]['layer'])
                    new_feature.setAttribute(UEBAUNIT_TABLE_BUILDING_UNIT_FIELD, building_unit_id)
                    new_feature.setAttribute(UEBAUNIT_TABLE_PARCEL_FIELD, parcel_id)
                    self.log.logMessage("Saving Building Unit-Parcel: {}-{}".format(building_unit_id, parcel_id),
                                        PLUGIN_NAME, Qgis.Info)
                    new_features.append(new_feature)

                self._layers[UEBAUNIT_TABLE]['layer'].dataProvider().addFeatures(new_features)

                if plot_ids and building_ids and building_unit_ids:
                    self.iface.messageBar().pushMessage("Asistente LADM_COL",
                        QCoreApplication.translate("CreateParcelCadastreWizard",
                                                   "The new parcel (t_id={}) was successfully created and associated with its corresponding Plot (t_id={}) and Building(s) (t_id={}) and Building Unit(s) (t_id={})!").format(parcel_id, ", ".join([str(b) for b in plot_ids]), ", ".join([str(b) for b in building_ids]), ", ".join([str(b) for b in building_unit_ids])),
                        Qgis.Info)
                elif plot_ids and building_ids and not building_unit_ids:
                    self.iface.messageBar().pushMessage("Asistente LADM_COL",
                        QCoreApplication.translate("CreateParcelCadastreWizard",
                                                   "The new parcel (t_id={}) was successfully created and associated with its corresponding Plot (t_id={}) and Building(s) (t_id={})!").format(parcel_id, ", ".join([str(b) for b in plot_ids]), ", ".join([str(b) for b in building_ids])),
                        Qgis.Info)
                elif plot_ids and not building_ids and building_unit_ids:
                    self.iface.messageBar().pushMessage("Asistente LADM_COL",
                        QCoreApplication.translate("CreateParcelCadastreWizard",
                                                   "The new parcel (t_id={}) was successfully created and associated with its corresponding Plot (t_id={}) and Building Unit(s) (t_id={})!").format(parcel_id, ", ".join([str(b) for b in plot_ids]), ", ".join([str(b) for b in building_unit_ids])),
                        Qgis.Info)
                elif plot_ids and not building_ids and not building_unit_ids:
                    self.iface.messageBar().pushMessage("Asistente LADM_COL",
                        QCoreApplication.translate("CreateParcelCadastreWizard",
                                                   "The new parcel (t_id={}) was successfully created and associated with its corresponding Plot (t_id={})!").format(parcel_id, ", ".join([str(b) for b in plot_ids])),
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

        self._layers[PARCEL_TABLE]['layer'].committedFeaturesAdded.disconnect(self.finish_parcel)
        self.log.logMessage("Parcel's committedFeaturesAdded SIGNAL disconnected", PLUGIN_NAME, Qgis.Info)
        self.close_wizard()

    def open_form(self, layer):
        if not layer.isEditable():
            layer.startEditing()

        feature = self.qgis_utils.get_new_feature(layer)
        dialog = self.iface.getFeatureForm(layer, feature)
        dialog.rejected.connect(self.form_rejected)
        dialog.setModal(True)

        # TODO: Set custom size of dialog
        # dialog.setFixedSize(1000, 500)
        # dialog.setWindowState(Qt.WindowMaximized)
        # dialog.setWindowState(Qt.WindowFullScreen)

        if dialog.exec_():
            fid = feature.id()

            # assigns the type of parcel before to creating it
            parcel_type_field_idx = layer.getFeature(fid).fieldNameIndex(PARCEL_TYPE_FIELD)
            layer.changeAttributeValue(fid, parcel_type_field_idx, self.cb_parcel_type.currentText())
            saved = layer.commitChanges()

            if not saved:
                layer.rollBack()
                self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                                    QCoreApplication.translate("CreateParcelCadastreWizard",
                                                                               "Error while saving changes. Parcel could not be created."),
                                                    Qgis.Warning)

                for e in layer.commitErrors():
                    self.log.logMessage("Commit error: {}".format(e), PLUGIN_NAME, Qgis.Warning)

            self.iface.mapCanvas().refresh()
        else:
            layer.rollBack()

    def form_rejected(self):
        self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                            QCoreApplication.translate("CreateParcelCadastreWizard",
                                                                       "'Create parcel' tool has been closed because you just closed the form."),
                                            Qgis.Info)
        self.close_wizard()

    def save_settings(self):
        settings = QSettings()
        settings.setValue('Asistente-LADM_COL/wizards/parcel_load_data_type', 'using_plots' if self.rad_parcel_from_plot.isChecked() else 'refactor')
        settings.setValue('Asistente-LADM_COL/wizards/type_of_parcel_selected', self.cb_parcel_type.currentText())

    def restore_settings(self):
        settings = QSettings()

        load_data_type = settings.value('Asistente-LADM_COL/wizards/parcel_load_data_type') or 'using_plots'
        if load_data_type == 'refactor':
            self.rad_refactor.setChecked(True)
        else:
            self.rad_parcel_from_plot.setChecked(True)

        self.type_of_parcel_selected = settings.value('Asistente-LADM_COL/wizards/type_of_parcel_selected')

    def show_help(self):
        self.qgis_utils.show_help("create_parcel")
