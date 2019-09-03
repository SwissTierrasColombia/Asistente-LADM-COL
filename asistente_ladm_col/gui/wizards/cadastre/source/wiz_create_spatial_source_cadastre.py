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
from qgis.PyQt.QtWidgets import (QWizard,
                                 QMessageBox)
from qgis.core import (QgsVectorLayerUtils,
                       Qgis,
                       QgsWkbTypes,
                       QgsMapLayerProxyModel,
                       QgsApplication)
from qgis.gui import QgsExpressionSelectionDialog

from .....config.general_config import (PLUGIN_NAME, LAYER)
from .....config.help_strings import HelpStrings
from .....config.table_mapping_config import (BOUNDARY_POINT_TABLE,
                                              BOUNDARY_TABLE,
                                              CCLSOURCE_TABLE,
                                              CCLSOURCE_TABLE_BOUNDARY_FIELD,
                                              CCLSOURCE_TABLE_SOURCE_FIELD,
                                              CONTROL_POINT_TABLE,
                                              EXTFILE_TABLE,
                                              ID_FIELD,
                                              PLOT_TABLE,
                                              POINTSOURCE_TABLE,
                                              POINTSOURCE_TABLE_BOUNDARYPOINT_FIELD,
                                              POINTSOURCE_TABLE_SURVEYPOINT_FIELD,
                                              POINTSOURCE_TABLE_CONTROLPOINT_FIELD,
                                              POINTSOURCE_TABLE_SOURCE_FIELD,
                                              SPATIAL_SOURCE_TABLE,
                                              SURVEY_POINT_TABLE,
                                              UESOURCE_TABLE,
                                              UESOURCE_TABLE_PLOT_FIELD,
                                              UESOURCE_TABLE_SOURCE_FIELD)
from .....utils import get_ui_class
from .....utils.qt_utils import (enable_next_wizard,
                                 disable_next_wizard)
from .....utils.select_map_tool import SelectMapTool

WIZARD_UI = get_ui_class('wizards/cadastre/source/wiz_create_spatial_source_cadastre.ui')


class CreateSpatialSourceCadastreWizard(QWizard, WIZARD_UI):
    WIZARD_NAME = "CreateSpatialSourceCadastreWizard"
    WIZARD_TOOL_NAME = QCoreApplication.translate(WIZARD_NAME, "Create Spatial Source")

    def __init__(self, iface, db, qgis_utils, parent=None):
        QWizard.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self.log = QgsApplication.messageLog()
        self._db = db
        self.qgis_utils = qgis_utils
        self.help_strings = HelpStrings()

        self.canvas = self.iface.mapCanvas()
        self.maptool = self.canvas.mapTool()
        self.select_maptool = None

        self._layers = {
            SPATIAL_SOURCE_TABLE: {'name': SPATIAL_SOURCE_TABLE, 'geometry': None, LAYER: None},
            EXTFILE_TABLE: {'name': EXTFILE_TABLE, 'geometry': None, LAYER: None},
            PLOT_TABLE: {'name': PLOT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            UESOURCE_TABLE: {'name': UESOURCE_TABLE, 'geometry': None, LAYER: None},
            BOUNDARY_TABLE: {'name': BOUNDARY_TABLE, 'geometry': None, LAYER: None},
            CCLSOURCE_TABLE: {'name': CCLSOURCE_TABLE, 'geometry': None, LAYER: None},
            POINTSOURCE_TABLE: {'name': POINTSOURCE_TABLE, 'geometry': None, LAYER: None},
            BOUNDARY_POINT_TABLE: {'name': BOUNDARY_POINT_TABLE, 'geometry': None, LAYER: None},
            SURVEY_POINT_TABLE: {'name': SURVEY_POINT_TABLE, 'geometry': None, LAYER: None},
            CONTROL_POINT_TABLE: {'name': CONTROL_POINT_TABLE, 'geometry': None, LAYER: None}
        }

        self.restore_settings()
        self.rad_create_manually.toggled.connect(self.adjust_page_1_controls)
        self.adjust_page_1_controls()

        self.button(QWizard.NextButton).clicked.connect(self.adjust_page_2_controls)
        self.button(QWizard.FinishButton).clicked.connect(self.finished_dialog)
        self.button(QWizard.HelpButton).clicked.connect(self.show_help)
        self.rejected.connect(self.close_wizard)
        self.mMapLayerComboBox.setFilters(QgsMapLayerProxyModel.NoGeometry)

    def adjust_page_1_controls(self):
        self.cbo_mapping.clear()
        self.cbo_mapping.addItem("")
        self.cbo_mapping.addItems(self.qgis_utils.get_field_mappings_file_names(SPATIAL_SOURCE_TABLE))

        if self.rad_refactor.isChecked():
            self.lbl_refactor_source.setEnabled(True)
            self.mMapLayerComboBox.setEnabled(True)
            self.lbl_field_mapping.setEnabled(True)
            self.cbo_mapping.setEnabled(True)
            disable_next_wizard(self)
            self.wizardPage1.setFinalPage(True)
            finish_button_text = QCoreApplication.translate(self.WIZARD_NAME, "Import")
            self.txt_help_page_1.setHtml(self.help_strings.get_refactor_help_string(SPATIAL_SOURCE_TABLE, False))
            self.wizardPage1.setButtonText(QWizard.FinishButton, finish_button_text)
        elif self.rad_create_manually.isChecked():
            self.lbl_refactor_source.setEnabled(False)
            self.mMapLayerComboBox.setEnabled(False)
            self.lbl_field_mapping.setEnabled(False)
            self.cbo_mapping.setEnabled(False)
            enable_next_wizard(self)
            self.wizardPage1.setFinalPage(False)
            finish_button_text = QCoreApplication.translate(self.WIZARD_NAME, "Create")
            self.txt_help_page_1.setHtml(self.help_strings.WIZ_CREATE_SPATIAL_SOURCE_CADASTRE_PAGE_1_OPTION_FORM)

        self.wizardPage2.setButtonText(QWizard.FinishButton,finish_button_text)

    def adjust_page_2_controls(self):
        self.button(self.FinishButton).setDisabled(True)
        self.txt_help_page_2.setHtml(self.help_strings.WIZ_CREATE_SPATIAL_SOURCE_CADASTRE_PAGE_2)
        self.disconnect_signals()

        # Load layers
        result = self.prepare_feature_creation_layers()
        if result is None:
            self.close_wizard(show_message=False)

        # Check if a previous features are selected
        self.check_selected_features()

        self.btn_plot_map.clicked.connect(partial(self.select_features_on_map, self._layers[PLOT_TABLE][LAYER]))
        self.btn_plot_expression.clicked.connect(partial(self.select_features_by_expression, self._layers[PLOT_TABLE][LAYER]))

        self.btn_boundary_map.clicked.connect(partial(self.select_features_on_map, self._layers[BOUNDARY_TABLE][LAYER]))
        self.btn_boundary_expression.clicked.connect(partial(self.select_features_by_expression, self._layers[BOUNDARY_TABLE][LAYER]))

        self.btn_boundary_point_map.clicked.connect(partial(self.select_features_on_map, self._layers[BOUNDARY_POINT_TABLE][LAYER]))
        self.btn_boundary_point_expression.clicked.connect(partial(self.select_features_by_expression, self._layers[BOUNDARY_POINT_TABLE][LAYER]))

        self.btn_survey_point_map.clicked.connect(partial(self.select_features_on_map, self._layers[SURVEY_POINT_TABLE][LAYER]))
        self.btn_survey_point_expression.clicked.connect(partial(self.select_features_by_expression, self._layers[SURVEY_POINT_TABLE][LAYER]))

        self.btn_control_point_map.clicked.connect(partial(self.select_features_on_map, self._layers[CONTROL_POINT_TABLE][LAYER]))
        self.btn_control_point_expression.clicked.connect(partial(self.select_features_by_expression, self._layers[CONTROL_POINT_TABLE][LAYER]))

    def disconnect_signals(self):
        # GUI Wizard
        signals = [self.btn_plot_map.clicked,
                   self.btn_plot_expression.clicked,
                   self.btn_boundary_map.clicked,
                   self.btn_boundary_expression.clicked,
                   self.btn_boundary_point_map.clicked,
                   self.btn_boundary_point_expression.clicked,
                   self.btn_survey_point_map.clicked,
                   self.btn_survey_point_expression.clicked,
                   self.btn_control_point_map.clicked,
                   self.btn_control_point_expression.clicked,
                   self.canvas.mapToolSet]
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
            self._layers[SPATIAL_SOURCE_TABLE][LAYER].committedFeaturesAdded.disconnect(self.finish_feature_creation)
        except:
            pass

        for layer_name in self._layers:
            try:
                self._layers[layer_name][LAYER].willBeDeleted.disconnect(self.layer_removed)
            except:
                pass

    def map_tool_changed(self, new_tool, old_tool):
        self.canvas.mapToolSet.disconnect(self.map_tool_changed)
        reply = QMessageBox.question(self,
                                     QCoreApplication.translate(self.WIZARD_NAME, "Stop Spatial Source creation?"),
                                     QCoreApplication.translate(self.WIZARD_NAME,"The map tool is about to change. Do you want to stop creating Spatial Source?"),
                                     QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            message = QCoreApplication.translate(self.WIZARD_NAME,
                                                 "'{}' tool has been closed because the map tool change.").format(self.WIZARD_TOOL_NAME)
            self.close_wizard(message)
        else:
            # Continue creating the Spatial Source
            self.canvas.setMapTool(old_tool)
            self.canvas.mapToolSet.connect(self.map_tool_changed)

    def select_features_on_map(self, layer):
        self.iface.setActiveLayer(layer)
        self.setVisible(False)  # Make wizard disappear

        # Enable Select Map Tool
        self.select_maptool = SelectMapTool(self.canvas, layer, multi=True)

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
        self.iface.setActiveLayer(layer)
        dlg_expression_selection = QgsExpressionSelectionDialog(layer)
        layer.selectionChanged.connect(self.check_selected_features)
        dlg_expression_selection.exec()
        layer.selectionChanged.disconnect(self.check_selected_features)

    def check_selected_features(self):
        # Check selected features in plot layer
        self.lb_plot.setText(QCoreApplication.translate(self.WIZARD_NAME, "<b>Plot(s)</b>: {count} Feature(s) Selected").format(count=self._layers[PLOT_TABLE][LAYER].selectedFeatureCount()))
        # Check selected features in boundary layer
        self.lb_boundary.setText(QCoreApplication.translate(self.WIZARD_NAME, "<b>Boundary(ies)</b>: {count} Feature(s) Selected").format(count=self._layers[BOUNDARY_TABLE][LAYER].selectedFeatureCount()))
        # Check selected features in boundary point layer
        self.lb_boundary_point.setText(QCoreApplication.translate(self.WIZARD_NAME, "<b>Boundary</b>: {count} Feature(s) Selected").format(count=self._layers[BOUNDARY_POINT_TABLE][LAYER].selectedFeatureCount()))
        # Check selected features in survey point layer
        self.lb_survey_point.setText(QCoreApplication.translate(self.WIZARD_NAME, "<b>Survey</b>: {count} Feature(s) Selected").format(count=self._layers[SURVEY_POINT_TABLE][LAYER].selectedFeatureCount()))
        # Check selected features in control point layer
        self.lb_control_point.setText(QCoreApplication.translate(self.WIZARD_NAME, "<b>Control</b>: {count} Feature(s) Selected").format(count=self._layers[CONTROL_POINT_TABLE][LAYER].selectedFeatureCount()))

        # Verifies that an feature has been selected
        if self._layers[PLOT_TABLE][LAYER].selectedFeatureCount() + self._layers[BOUNDARY_TABLE][LAYER].selectedFeatureCount() + self._layers[BOUNDARY_POINT_TABLE][LAYER].selectedFeatureCount() + self._layers[SURVEY_POINT_TABLE][LAYER].selectedFeatureCount() + self._layers[CONTROL_POINT_TABLE][LAYER].selectedFeatureCount() >= 1:
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
                                                               SPATIAL_SOURCE_TABLE,
                                                               field_mapping=field_mapping)

                if res_etl_model:
                    if field_mapping:
                        self.qgis_utils.delete_old_field_mapping(field_mapping)

                    self.qgis_utils.save_field_mapping(SPATIAL_SOURCE_TABLE)
            else:
                self.qgis_utils.message_emitted.emit(
                    QCoreApplication.translate(self.WIZARD_NAME,
                                               "Select a source layer to set the field mapping to '{}'.").format(
                        SPATIAL_SOURCE_TABLE),
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

        # Check if layers any layer is in editing mode
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

    def close_wizard(self, message=None, show_message=True):
        if message is None:
            message = QCoreApplication.translate(self.WIZARD_NAME, "'{}' tool has been closed.").format(self.WIZARD_TOOL_NAME)
        if show_message:
            self.qgis_utils.message_emitted.emit(message, Qgis.Info)
        self.init_map_tool()
        self.disconnect_signals()
        self.close()

    def init_map_tool(self):
        try:
            self.canvas.mapToolSet.disconnect(self.map_tool_changed)
        except:
            pass
        self.canvas.setMapTool(self.maptool)

    def edit_feature(self):
        self.iface.layerTreeView().setCurrentLayer(self._layers[SPATIAL_SOURCE_TABLE][LAYER])
        self._layers[SPATIAL_SOURCE_TABLE][LAYER].committedFeaturesAdded.connect(self.finish_feature_creation)
        self.open_form(self._layers[SPATIAL_SOURCE_TABLE][LAYER])

    def finish_feature_creation(self, layerId, features):
        message = QCoreApplication.translate(self.WIZARD_NAME,
                                             "'{}' tool has been closed because an error occurred while trying to save the data.").format(self.WIZARD_TOOL_NAME)

        if len(features) != 1:
            message = QCoreApplication.translate(self.WIZARD_NAME,
                                                 "'{}' tool has been closed. We should have got only one spatial source... We cannot do anything with {} spatial sources").format(self.WIZARD_TOOL_NAME, len(features))
            self.log.logMessage("We should have got only one spatial source... We cannot do anything with {} spatial sources".format(len(features)), PLUGIN_NAME, Qgis.Warning)
        else:

            feature = features[0]
            feature_ids_dict = dict()

            if self._layers[PLOT_TABLE][LAYER] is not None:
                if self._layers[PLOT_TABLE][LAYER].selectedFeatureCount() > 0:
                    feature_ids_dict[PLOT_TABLE] = [f[ID_FIELD] for f in self._layers[PLOT_TABLE][LAYER].selectedFeatures()]

            if self._layers[BOUNDARY_TABLE][LAYER] is not None:
                if self._layers[BOUNDARY_TABLE][LAYER].selectedFeatureCount() > 0:
                    feature_ids_dict[BOUNDARY_TABLE] = [f[ID_FIELD] for f in self._layers[BOUNDARY_TABLE][LAYER].selectedFeatures()]

            if self._layers[BOUNDARY_POINT_TABLE][LAYER] is not None:
                if self._layers[BOUNDARY_POINT_TABLE][LAYER].selectedFeatureCount() > 0:
                    feature_ids_dict[BOUNDARY_POINT_TABLE] = [f[ID_FIELD] for f in self._layers[BOUNDARY_POINT_TABLE][LAYER].selectedFeatures()]

            if self._layers[SURVEY_POINT_TABLE][LAYER] is not None:
                if self._layers[SURVEY_POINT_TABLE][LAYER].selectedFeatureCount() > 0:
                    feature_ids_dict[SURVEY_POINT_TABLE] = [f[ID_FIELD] for f in self._layers[SURVEY_POINT_TABLE][LAYER].selectedFeatures()]

            if self._layers[CONTROL_POINT_TABLE][LAYER] is not None:
                if self._layers[CONTROL_POINT_TABLE][LAYER].selectedFeatureCount() > 0:
                    feature_ids_dict[CONTROL_POINT_TABLE] = [f[ID_FIELD] for f in self._layers[CONTROL_POINT_TABLE][LAYER].selectedFeatures()]

            if not feature.isValid():
                self.log.logMessage("Feature not found in layer Spatial Source...", PLUGIN_NAME, Qgis.Warning)
            else:
                spatial_source_id = feature[ID_FIELD]
                all_new_features = list()

                # Fill association table, depending on the case
                new_features = list()
                if PLOT_TABLE in feature_ids_dict:
                    # Fill uesource table
                    for plot_id in feature_ids_dict[PLOT_TABLE]:
                        new_feature = QgsVectorLayerUtils().createFeature(self._layers[UESOURCE_TABLE][LAYER])
                        new_feature.setAttribute(UESOURCE_TABLE_PLOT_FIELD, plot_id)
                        new_feature.setAttribute(UESOURCE_TABLE_SOURCE_FIELD, spatial_source_id)
                        self.log.logMessage("Saving Plot-SpatialSource: {}-{}".format(plot_id, spatial_source_id), PLUGIN_NAME, Qgis.Info)
                        new_features.append(new_feature)

                    self._layers[UESOURCE_TABLE][LAYER].dataProvider().addFeatures(new_features)
                    all_new_features.extend(new_feature)

                new_features = list()
                if BOUNDARY_TABLE in feature_ids_dict:
                    # Fill cclsource table
                    for boundary_id in feature_ids_dict[BOUNDARY_TABLE]:
                        new_feature = QgsVectorLayerUtils().createFeature(self._layers[CCLSOURCE_TABLE][LAYER])
                        new_feature.setAttribute(CCLSOURCE_TABLE_BOUNDARY_FIELD, boundary_id)
                        new_feature.setAttribute(CCLSOURCE_TABLE_SOURCE_FIELD, spatial_source_id)
                        self.log.logMessage("Saving Boundary-SpatialSource: {}-{}".format(boundary_id, spatial_source_id), PLUGIN_NAME, Qgis.Info)
                        new_features.append(new_feature)

                    self._layers[CCLSOURCE_TABLE][LAYER].dataProvider().addFeatures(new_features)
                    all_new_features.extend(new_feature)

                new_features = list()
                if BOUNDARY_POINT_TABLE in feature_ids_dict:
                    for boundary_point_id in feature_ids_dict[BOUNDARY_POINT_TABLE]:
                        new_feature = QgsVectorLayerUtils().createFeature(self._layers[POINTSOURCE_TABLE][LAYER])
                        new_feature.setAttribute(POINTSOURCE_TABLE_BOUNDARYPOINT_FIELD, boundary_point_id)
                        new_feature.setAttribute(POINTSOURCE_TABLE_SOURCE_FIELD, spatial_source_id)
                        self.log.logMessage("Saving BoundaryPoint-SpatialSource: {}-{}".format(boundary_point_id, spatial_source_id), PLUGIN_NAME, Qgis.Info)
                        new_features.append(new_feature)

                    self._layers[POINTSOURCE_TABLE][LAYER].dataProvider().addFeatures(new_features)
                    all_new_features.extend(new_feature)

                new_features = list()
                if SURVEY_POINT_TABLE in feature_ids_dict:
                    for survey_point_id in feature_ids_dict[SURVEY_POINT_TABLE]:
                        new_feature = QgsVectorLayerUtils().createFeature(self._layers[POINTSOURCE_TABLE][LAYER])
                        new_feature.setAttribute(POINTSOURCE_TABLE_SURVEYPOINT_FIELD, survey_point_id)
                        new_feature.setAttribute(POINTSOURCE_TABLE_SOURCE_FIELD, spatial_source_id)
                        self.log.logMessage("Saving SurveyPoint-SpatialSource: {}-{}".format(survey_point_id, spatial_source_id), PLUGIN_NAME, Qgis.Info)
                        new_features.append(new_feature)

                    self._layers[POINTSOURCE_TABLE][LAYER].dataProvider().addFeatures(new_features)
                    all_new_features.extend(new_feature)

                new_features = list()
                if CONTROL_POINT_TABLE in feature_ids_dict:
                    for control_point_id in feature_ids_dict[CONTROL_POINT_TABLE]:
                        new_feature = QgsVectorLayerUtils().createFeature(self._layers[POINTSOURCE_TABLE][LAYER])
                        new_feature.setAttribute(POINTSOURCE_TABLE_CONTROLPOINT_FIELD, control_point_id)
                        new_feature.setAttribute(POINTSOURCE_TABLE_SOURCE_FIELD, spatial_source_id)
                        self.log.logMessage("Saving ControlPoint-SpatialSource: {}-{}".format(control_point_id, spatial_source_id), PLUGIN_NAME, Qgis.Info)
                        new_features.append(new_feature)

                    self._layers[POINTSOURCE_TABLE][LAYER].dataProvider().addFeatures(new_features)
                    all_new_features.extend(new_feature)

                if all_new_features:
                    message = QCoreApplication.translate(self.WIZARD_NAME,
                                                   "The new spatial source (t_id={}) was successfully created and associated with the following features: {}").format(spatial_source_id, feature_ids_dict)
                else:
                    message = QCoreApplication.translate(self.WIZARD_NAME,
                                                   "The new spatial source (t_id={}) was successfully created and it wasn't associated with a spatial unit").format(spatial_source_id)

        self._layers[SPATIAL_SOURCE_TABLE][LAYER].committedFeaturesAdded.disconnect()
        self.log.logMessage("Spatial Source's committedFeaturesAdded SIGNAL disconnected", PLUGIN_NAME, Qgis.Info)
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

            if self._layers[EXTFILE_TABLE][LAYER].isEditable():
                res = self._layers[EXTFILE_TABLE][LAYER].commitChanges()

            if not saved:
                layer.rollBack()
                self.qgis_utils.message_emitted.emit(
                    QCoreApplication.translate(self.WIZARD_NAME,
                                               "Error while saving changes. Spatial Source could not be created."),
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
        settings.setValue('Asistente-LADM_COL/wizards/spatial_source_load_data_type', 'create_manually' if self.rad_create_manually.isChecked() else 'refactor')

    def restore_settings(self):
        settings = QSettings()

        load_data_type = settings.value('Asistente-LADM_COL/wizards/spatial_source_load_data_type') or 'create_manually'
        if load_data_type == 'refactor':
            self.rad_refactor.setChecked(True)
        else:
            self.rad_create_manually.setChecked(True)

    def show_help(self):
        self.qgis_utils.show_help("create_spatial_source")
