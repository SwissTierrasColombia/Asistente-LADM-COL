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
from ..config.table_mapping_config import (BOUNDARY_POINT_TABLE,
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
from ..utils import get_ui_class
from ..utils.qt_utils import (enable_next_wizard,
                              disable_next_wizard)
from ..utils.select_map_tool import SelectMapTool

WIZARD_UI = get_ui_class('wiz_create_spatial_source_cadastre.ui')


class CreateSpatialSourceCadastreWizard(QWizard, WIZARD_UI):

    def __init__(self, iface, db, qgis_utils, parent=None):
        QWizard.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self.log = QgsApplication.messageLog()
        self.canvas = self.iface.mapCanvas()
        self.maptool = self.canvas.mapTool()
        self.select_maptool = None

        self._current_layer = None
        self._spatial_source_layer = None
        self._extfile_table = None
        self._plot_layer = None
        self._boundary_layer = None
        self._boundary_point_layer = None
        self._survey_point_layer = None
        self._control_point_layer = None
        self._uesource_table = None
        self._cclsource_table = None
        self._pointsource_table = None
        self._db = db
        self.qgis_utils = qgis_utils
        self.help_strings = HelpStrings()
        self.restore_settings()

        self.rad_boundary_point.setText(BOUNDARY_POINT_TABLE)
        self.rad_survey_point.setText(SURVEY_POINT_TABLE)
        self.rad_control_point.setText(CONTROL_POINT_TABLE)
        self.rad_boundary_point.setChecked(True)

        self.rad_boundary_point.toggled.connect(self.class_of_point_change)
        self.rad_survey_point.toggled.connect(self.class_of_point_change)
        self.rad_control_point.toggled.connect(self.class_of_point_change)

        self.rad_create_manually.toggled.connect(self.adjust_page_1_controls)
        self.adjust_page_1_controls()

        self.button(QWizard.NextButton).clicked.connect(self.adjust_page_2_controls)
        self.button(QWizard.FinishButton).clicked.connect(self.finished_dialog)
        self.button(QWizard.HelpButton).clicked.connect(self.show_help)

        self.mMapLayerComboBox.setFilters(QgsMapLayerProxyModel.NoGeometry)

    def map_tool_changed(self, new_tool, old_tool):
        reply = QMessageBox.question(self,
                                     QCoreApplication.translate("CreateSpatialSourceCadastreWizard", "Stop Spatial Source creation?"),
                                     QCoreApplication.translate("CreateSpatialSourceCadastreWizard","The map tool is about to change. Do you want to stop creating Spatial Source?"),
                                     QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            # Disconnect signal that check if map tool change
            self.canvas.mapToolSet.disconnect(self.map_tool_changed)
            self.close()
        else:
            # Continue creating the Spatial Source
            self.canvas.mapToolSet.disconnect(self.map_tool_changed)
            self.canvas.setMapTool(old_tool)
            self.canvas.mapToolSet.connect(self.map_tool_changed)

    def closeEvent(self, event):
        # Close all open signal when object is destroyed
        sip.delete(self)

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
            finish_button_text = QCoreApplication.translate("CreateSpatialSourceCadastreWizard", "Import")
            self.txt_help_page_1.setHtml(self.help_strings.get_refactor_help_string(SPATIAL_SOURCE_TABLE, False))
            self.wizardPage1.setButtonText(QWizard.FinishButton, finish_button_text)

        elif self.rad_create_manually.isChecked():
            self.lbl_refactor_source.setEnabled(False)
            self.mMapLayerComboBox.setEnabled(False)
            self.lbl_field_mapping.setEnabled(False)
            self.cbo_mapping.setEnabled(False)
            enable_next_wizard(self)
            self.wizardPage1.setFinalPage(False)
            finish_button_text = QCoreApplication.translate("CreateSpatialSourceCadastreWizard", "Create")
            self.txt_help_page_1.setHtml(self.help_strings.WIZ_CREATE_SPATIAL_SOURCE_CADASTRE_PAGE_1_OPTION_FORM)

        self.wizardPage2.setButtonText(QWizard.FinishButton,finish_button_text)

    def adjust_page_2_controls(self):
        self.button(self.FinishButton).setDisabled(True)

        self.txt_help_page_2.setHtml(self.help_strings.WIZ_CREATE_SPATIAL_SOURCE_CADASTRE_PAGE_2)

        # TODO: It is necesary becasuse when I got to back signal map_tool_changed it is not disconnect
        #       Remove when error are fixed
        self.button(QWizard.BackButton).hide()

        # Load layers
        result = self.prepare_spatial_source_creation_layers()

        if result:
            # Check if a previous features are selected
            self.check_selected_features()

            self.btn_plot_map.clicked.connect(partial(self.select_features_on_map, self._plot_layer))
            self.btn_plot_expression.clicked.connect(partial(self.select_features_by_expression, self._plot_layer))

            self.btn_boundary_map.clicked.connect(partial(self.select_features_on_map, self._boundary_layer))
            self.btn_boundary_expression.clicked.connect(partial(self.select_features_by_expression, self._boundary_layer))

            self.btn_point_map.clicked.connect(partial(self.select_features_on_map, self._boundary_point_layer))
            self.btn_point_expression.clicked.connect(partial(self.select_features_by_expression, self._boundary_point_layer))

    def class_of_point_change(self):

        # Disconnect signals
        self.btn_point_map.clicked.disconnect()
        self.btn_point_expression.clicked.disconnect()

        if self.rad_boundary_point.isChecked():
            self.btn_point_map.clicked.connect(partial(self.select_features_on_map, self._boundary_point_layer))
            self.btn_point_expression.clicked.connect(partial(self.select_features_by_expression, self._boundary_point_layer))
        elif self.rad_survey_point.isChecked():
            self.btn_point_map.clicked.connect(partial(self.select_features_on_map, self._survey_point_layer))
            self.btn_point_expression.clicked.connect(partial(self.select_features_by_expression, self._survey_point_layer))
        elif self.rad_control_point.isChecked():
            self.btn_point_map.clicked.connect(partial(self.select_features_on_map, self._control_point_layer))
            self.btn_point_expression.clicked.connect(partial(self.select_features_by_expression, self._control_point_layer))

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
        Dlg_expression_selection = QgsExpressionSelectionDialog(self._current_layer)
        self._current_layer.selectionChanged.connect(self.check_selected_features)
        Dlg_expression_selection.exec()
        self._current_layer.selectionChanged.disconnect(self.check_selected_features)

    def check_selected_features(self):

        # Check selected features in plot layer
        if self._plot_layer.selectedFeatureCount():
            self.lb_plot.setText(QCoreApplication.translate("CreateSpatialSourceCadastreWizard", "Plots: {count} Feature Selected").format(count=self._plot_layer.selectedFeatureCount()))
        else:
            self.lb_plot.setText(QCoreApplication.translate("CreateSpatialSourceCadastreWizard", "Plots: 0 Features Selected"))

        # Check selected features in boundary layer
        if self._boundary_layer.selectedFeatureCount():
            self.lb_boundary.setText(QCoreApplication.translate("CreateSpatialSourceCadastreWizard", "Boundary(ies): {count} Feature Selected").format(count=self._boundary_layer.selectedFeatureCount()))
        else:
            self.lb_boundary.setText(QCoreApplication.translate("CreateSpatialSourceCadastreWizard", "Boundary(ies): 0 Features Selected"))

        # Check selected features in boundary point layer
        if self._boundary_point_layer.selectedFeatureCount():
            self.rad_boundary_point.setText(QCoreApplication.translate("CreateSpatialSourceCadastreWizard", "{table}: {count} Features Selected").format(table=BOUNDARY_POINT_TABLE, count=self._boundary_point_layer.selectedFeatureCount()))
        else:
            self.rad_boundary_point.setText(QCoreApplication.translate("CreateSpatialSourceCadastreWizard", "{table}: 0 Features Selected".format(table=BOUNDARY_POINT_TABLE)))

        # Check selected features in survey point layer
        if self._survey_point_layer.selectedFeatureCount():
            self.rad_survey_point.setText(QCoreApplication.translate("CreateSpatialSourceCadastreWizard", "{table}: {count} Features Selected").format(table=SURVEY_POINT_TABLE, count=self._survey_point_layer.selectedFeatureCount()))
        else:
            self.rad_survey_point.setText(QCoreApplication.translate("CreateSpatialSourceCadastreWizard", "{table}: 0 Features Selected".format(table=SURVEY_POINT_TABLE)))

        # Check selected features in control point layer
        if self._control_point_layer.selectedFeatureCount():
            self.rad_control_point.setText(QCoreApplication.translate("CreateSpatialSourceCadastreWizard", "{table}: {count} Features Selected").format(table=CONTROL_POINT_TABLE, count=self._control_point_layer.selectedFeatureCount()))
        else:
            self.rad_control_point.setText(QCoreApplication.translate("CreateSpatialSourceCadastreWizard", "{table}: 0 Features Selected".format(table=CONTROL_POINT_TABLE)))

        # Verifies that an feature has been selected
        if self._plot_layer.selectedFeatureCount() + self._boundary_layer.selectedFeatureCount() + self._boundary_point_layer.selectedFeatureCount() + self._survey_point_layer.selectedFeatureCount() + self._control_point_layer.selectedFeatureCount():
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
                self.iface.messageBar().pushMessage("Asistente LADM_COL",
                    QCoreApplication.translate("CreateSpatialSourceCadastreWizard",
                                               "Select a source layer to set the field mapping to '{}'.").format(SPATIAL_SOURCE_TABLE),
                    Qgis.Warning)

        elif self.rad_create_manually.isChecked():
            self.prepare_spatial_source_creation()

    def prepare_spatial_source_creation(self):

        result = self.prepare_spatial_source_creation_layers()

        if result:
            # Don't suppress (i.e., show) feature form
            form_config = self._spatial_source_layer.editFormConfig()
            form_config.setSuppress(QgsEditFormConfig.SuppressOff)
            self._spatial_source_layer.setEditFormConfig(form_config)
            self.edit_spatial_source()

    def prepare_spatial_source_creation_layers(self):

        layers_to_load = {
            SPATIAL_SOURCE_TABLE: {'name': SPATIAL_SOURCE_TABLE, 'geometry': None},
            EXTFILE_TABLE: {'name': EXTFILE_TABLE, 'geometry': None},
            PLOT_TABLE: {'name': PLOT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry},
            UESOURCE_TABLE: {'name': UESOURCE_TABLE, 'geometry': None},
            BOUNDARY_TABLE: {'name': BOUNDARY_TABLE, 'geometry': None},
            CCLSOURCE_TABLE: {'name': CCLSOURCE_TABLE, 'geometry': None},
            POINTSOURCE_TABLE: {'name': POINTSOURCE_TABLE, 'geometry': None},
            BOUNDARY_POINT_TABLE: {'name': BOUNDARY_POINT_TABLE, 'geometry': None},
            SURVEY_POINT_TABLE: {'name': SURVEY_POINT_TABLE, 'geometry': None},
            CONTROL_POINT_TABLE: {'name': CONTROL_POINT_TABLE, 'geometry': None}
        }

        # Load layers
        res_layers = self.qgis_utils.get_layers(self._db, layers_to_load, load=True)

        # Get layers into local variables
        self._spatial_source_layer = res_layers[SPATIAL_SOURCE_TABLE]
        if self._spatial_source_layer is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                                QCoreApplication.translate("CreateSpatialSourceCadastreWizard",
                                                                           "Spatial Source layer couldn't be found... {}").format(
                                                    self._db.get_description()),
                                                Qgis.Warning)
            return

        self._extfile_table = res_layers[EXTFILE_TABLE]
        if self._extfile_table is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                                QCoreApplication.translate("CreateSpatialSourceCadastreWizard",
                                                                           "ExtFile table couldn't be found... {}").format(
                                                    self._db.get_description()),
                                                Qgis.Warning)
            return

        self._plot_layer = res_layers[PLOT_TABLE] if PLOT_TABLE in res_layers else None
        if self._plot_layer is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                                QCoreApplication.translate("CreateSpatialSourceCadastreWizard",
                                                                           "Plot layer couldn't be found... {}").format(
                                                    self._db.get_description()),
                                                Qgis.Warning)
            return

        self._uesource_table = res_layers[UESOURCE_TABLE] if UESOURCE_TABLE in res_layers else None
        if self._uesource_table is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                                QCoreApplication.translate("CreateSpatialSourceCadastreWizard",
                                                                           "UESOURCE table couldn't be found... {}").format(
                                                    self._db.get_description()),
                                                Qgis.Warning)
            return

        self._boundary_layer = res_layers[BOUNDARY_TABLE] if BOUNDARY_TABLE in res_layers else None
        if self._boundary_layer is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                                QCoreApplication.translate("CreateSpatialSourceCadastreWizard",
                                                                           "Boundary layer couldn't be found... {}").format(
                                                    self._db.get_description()),
                                                Qgis.Warning)
            return

        self._cclsource_table = res_layers[CCLSOURCE_TABLE] if CCLSOURCE_TABLE in res_layers else None
        if self._cclsource_table is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                                QCoreApplication.translate("CreateSpatialSourceCadastreWizard",
                                                                           "CCLSOURCE table couldn't be found... {}").format(
                                                    self._db.get_description()),
                                                Qgis.Warning)
            return

        self._boundary_point_layer = res_layers[BOUNDARY_POINT_TABLE] if BOUNDARY_POINT_TABLE in res_layers else None
        if self._boundary_point_layer is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                                QCoreApplication.translate("CreateSpatialSourceCadastreWizard",
                                                                           "Boundary Point layer couldn't be found... {}").format(
                                                    self._db.get_description()),
                                                Qgis.Warning)
            return

        self._survey_point_layer = res_layers[SURVEY_POINT_TABLE] if SURVEY_POINT_TABLE in res_layers else None
        if self._survey_point_layer is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                                QCoreApplication.translate("CreateSpatialSourceCadastreWizard",
                                                                           "Survey Point layer couldn't be found... {}").format(
                                                    self._db.get_description()),
                                                Qgis.Warning)
            return

        self._control_point_layer = res_layers[CONTROL_POINT_TABLE] if CONTROL_POINT_TABLE in res_layers else None
        if self._control_point_layer is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                                QCoreApplication.translate("CreateSpatialSourceCadastreWizard",
                                                                           "Control Point layer couldn't be found... {}").format(
                                                    self._db.get_description()),
                                                Qgis.Warning)
            return

        self._pointsource_table = res_layers[POINTSOURCE_TABLE] if POINTSOURCE_TABLE in res_layers else None
        if self._pointsource_table is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                                QCoreApplication.translate("CreateSpatialSourceCadastreWizard",
                                                                           "POINTSOURCE table couldn't be found... {}").format(
                                                    self._db.get_description()),
                                                Qgis.Warning)
            return

        # All layers were successfully loaded
        return True

    def edit_spatial_source(self):
        feature_ids_dict = dict()

        if self._plot_layer is not None:
            if self._plot_layer.selectedFeatureCount() > 0:
                feature_ids_dict[PLOT_TABLE] = [f[ID_FIELD] for f in self._plot_layer.selectedFeatures()]

        if self._boundary_layer is not None:
            if self._boundary_layer.selectedFeatureCount() > 0:
                feature_ids_dict[BOUNDARY_TABLE] = [f[ID_FIELD] for f in self._boundary_layer.selectedFeatures()]

        if self._boundary_point_layer is not None:
            if self._boundary_point_layer.selectedFeatureCount() > 0:
                feature_ids_dict[BOUNDARY_POINT_TABLE] = [f[ID_FIELD] for f in self._boundary_point_layer.selectedFeatures()]

        if self._survey_point_layer is not None:
            if self._survey_point_layer.selectedFeatureCount() > 0:
                feature_ids_dict[SURVEY_POINT_TABLE] = [f[ID_FIELD] for f in self._survey_point_layer.selectedFeatures()]

        if self._control_point_layer is not None:
            if self._control_point_layer.selectedFeatureCount() > 0:
                feature_ids_dict[CONTROL_POINT_TABLE] = [f[ID_FIELD] for f in self._control_point_layer.selectedFeatures()]

        # Open Form
        self.iface.layerTreeView().setCurrentLayer(self._spatial_source_layer)
        self._spatial_source_layer.startEditing()
        self.iface.actionAddFeature().trigger()

        # Create connections to react when a feature is added to buffer and
        # when it gets stored into the DB
        self._spatial_source_layer.featureAdded.connect(self.call_spatial_source_commit)
        self._spatial_source_layer.committedFeaturesAdded.connect(partial(self.finish_spatial_source, feature_ids_dict))

    def call_spatial_source_commit(self, fid):
        self._spatial_source_layer.featureAdded.disconnect(self.call_spatial_source_commit)
        self.log.logMessage("Spatial Source's featureAdded SIGNAL disconnected", PLUGIN_NAME, Qgis.Info)
        res = self._spatial_source_layer.commitChanges()
        if self._extfile_table.isEditable():
            res = self._extfile_table.commitChanges()

    def finish_spatial_source(self, feature_ids_dict, layerId, features):
        if len(features) != 1:
            self.log.logMessage("We should have got only one spatial source... We cannot do anything with {} spatial sources".format(len(features)), PLUGIN_NAME, Qgis.Warning)
        else:
            feature = features[0]
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
                        new_feature = QgsVectorLayerUtils().createFeature(self._uesource_table)
                        new_feature.setAttribute(UESOURCE_TABLE_PLOT_FIELD, plot_id)
                        new_feature.setAttribute(UESOURCE_TABLE_SOURCE_FIELD, spatial_source_id)
                        self.log.logMessage("Saving Plot-SpatialSource: {}-{}".format(plot_id, spatial_source_id), PLUGIN_NAME, Qgis.Info)
                        new_features.append(new_feature)

                    self._uesource_table.dataProvider().addFeatures(new_features)
                    all_new_features.extend(new_feature)


                new_features = list()
                if BOUNDARY_TABLE in feature_ids_dict:
                    # Fill cclsource table
                    for boundary_id in feature_ids_dict[BOUNDARY_TABLE]:
                        new_feature = QgsVectorLayerUtils().createFeature(self._cclsource_table)
                        new_feature.setAttribute(CCLSOURCE_TABLE_BOUNDARY_FIELD, boundary_id)
                        new_feature.setAttribute(CCLSOURCE_TABLE_SOURCE_FIELD, spatial_source_id)
                        self.log.logMessage("Saving Boundary-SpatialSource: {}-{}".format(boundary_id, spatial_source_id), PLUGIN_NAME, Qgis.Info)
                        new_features.append(new_feature)

                    self._cclsource_table.dataProvider().addFeatures(new_features)
                    all_new_features.extend(new_feature)

                new_features = list()
                if BOUNDARY_POINT_TABLE in feature_ids_dict:
                    for boundary_point_id in feature_ids_dict[BOUNDARY_POINT_TABLE]:
                        new_feature = QgsVectorLayerUtils().createFeature(self._pointsource_table)
                        new_feature.setAttribute(POINTSOURCE_TABLE_BOUNDARYPOINT_FIELD, boundary_point_id)
                        new_feature.setAttribute(POINTSOURCE_TABLE_SOURCE_FIELD, spatial_source_id)
                        self.log.logMessage("Saving BoundaryPoint-SpatialSource: {}-{}".format(boundary_point_id, spatial_source_id), PLUGIN_NAME, Qgis.Info)
                        new_features.append(new_feature)

                    self._pointsource_table.dataProvider().addFeatures(new_features)
                    all_new_features.extend(new_feature)

                new_features = list()
                if SURVEY_POINT_TABLE in feature_ids_dict:
                    for survey_point_id in feature_ids_dict[SURVEY_POINT_TABLE]:
                        new_feature = QgsVectorLayerUtils().createFeature(self._pointsource_table)
                        new_feature.setAttribute(POINTSOURCE_TABLE_SURVEYPOINT_FIELD, survey_point_id)
                        new_feature.setAttribute(POINTSOURCE_TABLE_SOURCE_FIELD, spatial_source_id)
                        self.log.logMessage("Saving SurveyPoint-SpatialSource: {}-{}".format(survey_point_id, spatial_source_id), PLUGIN_NAME, Qgis.Info)
                        new_features.append(new_feature)

                    self._pointsource_table.dataProvider().addFeatures(new_features)
                    all_new_features.extend(new_feature)

                new_features = list()
                if CONTROL_POINT_TABLE in feature_ids_dict:
                    for control_point_id in feature_ids_dict[CONTROL_POINT_TABLE]:
                        new_feature = QgsVectorLayerUtils().createFeature(self._pointsource_table)
                        new_feature.setAttribute(POINTSOURCE_TABLE_CONTROLPOINT_FIELD, control_point_id)
                        new_feature.setAttribute(POINTSOURCE_TABLE_SOURCE_FIELD, spatial_source_id)
                        self.log.logMessage("Saving ControlPoint-SpatialSource: {}-{}".format(control_point_id, spatial_source_id), PLUGIN_NAME, Qgis.Info)
                        new_features.append(new_feature)

                    self._pointsource_table.dataProvider().addFeatures(new_features)
                    all_new_features.extend(new_feature)

                if all_new_features:
                    self.iface.messageBar().pushMessage("Asistente LADM_COL",
                        QCoreApplication.translate("CreateSpatialSourceCadastreWizard",
                                                   "The new spatial source (t_id={}) was successfully created and associated with the following features: {}").format(spatial_source_id, feature_ids_dict),
                        Qgis.Info, 30)

        self._spatial_source_layer.committedFeaturesAdded.disconnect()
        self.log.logMessage("Spatial Source's committedFeaturesAdded SIGNAL disconnected", PLUGIN_NAME, Qgis.Info)

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
