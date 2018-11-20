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

from qgis.core import (QgsEditFormConfig, QgsVectorLayerUtils, Qgis,
                       QgsWkbTypes, QgsMapLayerProxyModel, QgsApplication)
from qgis.gui import QgsMessageBar
from qgis.PyQt.QtCore import Qt, QPoint, QCoreApplication, QSettings
from qgis.PyQt.QtWidgets import QAction, QWizard

from ..utils import get_ui_class
from ..config.general_config import (
    PLUGIN_NAME,
    FIELD_MAPPING_PATH
)
from ..config.table_mapping_config import (
    BOUNDARY_POINT_TABLE,
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
    UESOURCE_TABLE_SOURCE_FIELD
)
from ..config.help_strings import HelpStrings

WIZARD_UI = get_ui_class('wiz_create_spatial_source_cadastre.ui')

class CreateSpatialSourceCadastreWizard(QWizard, WIZARD_UI):
    def __init__(self, iface, db, qgis_utils, parent=None):
        QWizard.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self.log = QgsApplication.messageLog()
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
        self.points_text = QCoreApplication.translate("CreateSpatialSourceCadastreWizard", "Points")
        self.help_strings = HelpStrings()

        self.restore_settings()

        self.cbo_layer.addItems([PLOT_TABLE,
            BOUNDARY_TABLE,
            self.points_text])
        self.cbo_point_layer.addItems([
            BOUNDARY_POINT_TABLE,
            SURVEY_POINT_TABLE,
            CONTROL_POINT_TABLE])

        self.rad_create_manually.toggled.connect(self.adjust_page_1_controls)
        self.cbo_layer.currentTextChanged.connect(self.adjust_cbo_point_layer)
        self.adjust_page_1_controls()
        self.button(QWizard.FinishButton).clicked.connect(self.finished_dialog)
        self.button(QWizard.HelpButton).clicked.connect(self.show_help)

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
            finish_button_text = QCoreApplication.translate("CreateSpatialSourceCadastreWizard", "Import")
            self.txt_help_page_1.setHtml(self.help_strings.get_refactor_help_string(SPATIAL_SOURCE_TABLE, False))

        elif self.rad_create_manually.isChecked():
            self.cbo_point_layer.setEnabled(self.cbo_layer.currentText() == self.points_text)
            self.lbl_refactor_source.setEnabled(False)
            self.mMapLayerComboBox.setEnabled(False)
            self.lbl_field_mapping.setEnabled(False)
            self.cbo_mapping.setEnabled(False)
            finish_button_text = QCoreApplication.translate("CreateSpatialSourceCadastreWizard", "Create")
            self.txt_help_page_1.setHtml(self.help_strings.WIZ_CREATE_SPATIAL_SOURCE_CADASTRE_PAGE_1_OPTION_FORM)

        self.wizardPage1.setButtonText(QWizard.FinishButton,
                                       QCoreApplication.translate("CreateSpatialSourceCadastreWizard",
                                       finish_button_text))

    def adjust_cbo_point_layer(self):
        self.cbo_point_layer.setEnabled(self.cbo_layer.currentText() == self.points_text)

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
        layers_to_load = {
            SPATIAL_SOURCE_TABLE: {'name': SPATIAL_SOURCE_TABLE, 'geometry': None},
            EXTFILE_TABLE: {'name': EXTFILE_TABLE, 'geometry': None}
        }
        if self.cbo_layer.currentText() == PLOT_TABLE:
            layers_to_load[PLOT_TABLE] = {'name': PLOT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry}
            layers_to_load[UESOURCE_TABLE] = {'name': UESOURCE_TABLE, 'geometry': None}
        elif self.cbo_layer.currentText() == BOUNDARY_TABLE:
            layers_to_load[BOUNDARY_TABLE] = {'name': BOUNDARY_TABLE, 'geometry': None}
            layers_to_load[CCLSOURCE_TABLE] = {'name': CCLSOURCE_TABLE, 'geometry': None}
        elif self.cbo_layer.currentText() == self.points_text:
            layers_to_load[POINTSOURCE_TABLE] = {'name': POINTSOURCE_TABLE, 'geometry': None}
            if BOUNDARY_POINT_TABLE in self.cbo_point_layer.checkedItems():
                layers_to_load[BOUNDARY_POINT_TABLE] = {'name': BOUNDARY_POINT_TABLE, 'geometry': None}
            if SURVEY_POINT_TABLE in self.cbo_point_layer.checkedItems():
                layers_to_load[SURVEY_POINT_TABLE] = {'name': SURVEY_POINT_TABLE, 'geometry': None}
            if CONTROL_POINT_TABLE in self.cbo_point_layer.checkedItems():
                layers_to_load[CONTROL_POINT_TABLE] = {'name': CONTROL_POINT_TABLE, 'geometry': None}

        # Load layers
        res_layers = self.qgis_utils.get_layers(self._db, layers_to_load, load=True)

        # Get layers into local variables
        self._spatial_source_layer = res_layers[SPATIAL_SOURCE_TABLE]
        if self._spatial_source_layer is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                QCoreApplication.translate("CreateSpatialSourceCadastreWizard",
                                           "Spatial Source layer couldn't be found... {}").format(self._db.get_description()),
                Qgis.Warning)
            return

        self._extfile_table = res_layers[EXTFILE_TABLE]
        if self._extfile_table is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                QCoreApplication.translate("CreateSpatialSourceCadastreWizard",
                                           "ExtFile table couldn't be found... {}").format(self._db.get_description()),
                Qgis.Warning)
            return

        if self.cbo_layer.currentText() == PLOT_TABLE:
            self._plot_layer = res_layers[PLOT_TABLE] if PLOT_TABLE in res_layers else None
            if self._plot_layer is None:
                self.iface.messageBar().pushMessage("Asistente LADM_COL",
                    QCoreApplication.translate("CreateSpatialSourceCadastreWizard",
                                               "Plot layer couldn't be found... {}").format(self._db.get_description()),
                    Qgis.Warning)
                return

            self._uesource_table = res_layers[UESOURCE_TABLE] if UESOURCE_TABLE in res_layers else None
            if self._uesource_table is None:
                self.iface.messageBar().pushMessage("Asistente LADM_COL",
                    QCoreApplication.translate("CreateSpatialSourceCadastreWizard",
                                               "UESOURCE table couldn't be found... {}").format(self._db.get_description()),
                    Qgis.Warning)
                return

        if self.cbo_layer.currentText() == BOUNDARY_TABLE:
            self._boundary_layer = res_layers[BOUNDARY_TABLE] if BOUNDARY_TABLE in res_layers else None
            if self._boundary_layer is None:
                self.iface.messageBar().pushMessage("Asistente LADM_COL",
                    QCoreApplication.translate("CreateSpatialSourceCadastreWizard",
                                               "Boundary layer couldn't be found... {}").format(self._db.get_description()),
                    Qgis.Warning)
                return

            self._cclsource_table = res_layers[CCLSOURCE_TABLE] if CCLSOURCE_TABLE in res_layers else None
            if self._cclsource_table is None:
                self.iface.messageBar().pushMessage("Asistente LADM_COL",
                    QCoreApplication.translate("CreateSpatialSourceCadastreWizard",
                                               "CCLSOURCE table couldn't be found... {}").format(self._db.get_description()),
                    Qgis.Warning)
                return

        if self.cbo_layer.currentText() == self.points_text:

            self._boundary_point_layer = res_layers[BOUNDARY_POINT_TABLE] if BOUNDARY_POINT_TABLE in res_layers else None
            if self._boundary_point_layer is None and BOUNDARY_POINT_TABLE in self.cbo_point_layer.checkedItems():
                self.iface.messageBar().pushMessage("Asistente LADM_COL",
                    QCoreApplication.translate("CreateSpatialSourceCadastreWizard",
                                               "Boundary Point layer couldn't be found... {}").format(self._db.get_description()),
                    Qgis.Warning)
                return

            self._survey_point_layer = res_layers[SURVEY_POINT_TABLE] if SURVEY_POINT_TABLE in res_layers else None
            if self._survey_point_layer is None and SURVEY_POINT_TABLE in self.cbo_point_layer.checkedItems():
                self.iface.messageBar().pushMessage("Asistente LADM_COL",
                    QCoreApplication.translate("CreateSpatialSourceCadastreWizard",
                                               "Survey Point layer couldn't be found... {}").format(self._db.get_description()),
                    Qgis.Warning)
                return

            self._control_point_layer = res_layers[CONTROL_POINT_TABLE] if CONTROL_POINT_TABLE in res_layers else None
            if self._control_point_layer is None and CONTROL_POINT_TABLE in self.cbo_point_layer.checkedItems():
                self.iface.messageBar().pushMessage("Asistente LADM_COL",
                    QCoreApplication.translate("CreateSpatialSourceCadastreWizard",
                                               "Control Point layer couldn't be found... {}").format(self._db.get_description()),
                    Qgis.Warning)
                return

            self._pointsource_table = res_layers[POINTSOURCE_TABLE] if POINTSOURCE_TABLE in res_layers else None
            if self._pointsource_table is None:
                self.iface.messageBar().pushMessage("Asistente LADM_COL",
                    QCoreApplication.translate("CreateSpatialSourceCadastreWizard",
                                               "POINTSOURCE table couldn't be found... {}").format(self._db.get_description()),
                    Qgis.Warning)
                return

        # Don't suppress (i.e., show) feature form
        form_config = self._spatial_source_layer.editFormConfig()
        form_config.setSuppress(QgsEditFormConfig.SuppressOff)
        self._spatial_source_layer.setEditFormConfig(form_config)

        self.edit_spatial_source()

    def edit_spatial_source(self):
        feature_ids_dict = dict()

        if self._plot_layer is not None:
            if self._plot_layer.selectedFeatureCount() > 0:
                feature_ids_dict[PLOT_TABLE] = [f[ID_FIELD] for f in self._plot_layer.selectedFeatures()]
            else:
                self.iface.messageBar().pushMessage("Asistente LADM_COL",
                    QCoreApplication.translate("CreateSpatialSourceCadastreWizard",
                                               "Please select at least one Plot"),
                    Qgis.Warning)
                return

        if self._boundary_layer is not None:
            if self._boundary_layer.selectedFeatureCount() > 0:
                feature_ids_dict[BOUNDARY_TABLE] = [f[ID_FIELD] for f in self._boundary_layer.selectedFeatures()]
            else:
                self.iface.messageBar().pushMessage("Asistente LADM_COL",
                    QCoreApplication.translate("CreateSpatialSourceCadastreWizard",
                                               "Please select at least one Boundary"),
                    Qgis.Warning)
                return

        if self._boundary_point_layer is not None:
            if self._boundary_point_layer.selectedFeatureCount() > 0:
                feature_ids_dict[BOUNDARY_POINT_TABLE] = [f[ID_FIELD] for f in self._boundary_point_layer.selectedFeatures()]
            else:
                self.iface.messageBar().pushMessage("Asistente LADM_COL",
                    QCoreApplication.translate("CreateSpatialSourceCadastreWizard",
                                               "Please select at least one Boundary Point"),
                    Qgis.Warning)
                return

        if self._survey_point_layer is not None:
            if self._survey_point_layer.selectedFeatureCount() > 0:
                feature_ids_dict[SURVEY_POINT_TABLE] = [f[ID_FIELD] for f in self._survey_point_layer.selectedFeatures()]
            else:
                self.iface.messageBar().pushMessage("Asistente LADM_COL",
                    QCoreApplication.translate("CreateSpatialSourceCadastreWizard",
                                               "Please select at least one Survey Point"),
                    Qgis.Warning)
                return

        if self._control_point_layer is not None:
            if self._control_point_layer.selectedFeatureCount() > 0:
                feature_ids_dict[CONTROL_POINT_TABLE] = [f[ID_FIELD] for f in self._control_point_layer.selectedFeatures()]
            else:
                self.iface.messageBar().pushMessage("Asistente LADM_COL",
                    QCoreApplication.translate("CreateSpatialSourceCadastreWizard",
                                               "Please select at least one Control Point"),
                    Qgis.Warning)
                return

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

                elif BOUNDARY_TABLE in feature_ids_dict:
                    # Fill cclsource table
                    for boundary_id in feature_ids_dict[BOUNDARY_TABLE]:
                        new_feature = QgsVectorLayerUtils().createFeature(self._cclsource_table)
                        new_feature.setAttribute(CCLSOURCE_TABLE_BOUNDARY_FIELD, boundary_id)
                        new_feature.setAttribute(CCLSOURCE_TABLE_SOURCE_FIELD, spatial_source_id)
                        self.log.logMessage("Saving Boundary-SpatialSource: {}-{}".format(boundary_id, spatial_source_id), PLUGIN_NAME, Qgis.Info)
                        new_features.append(new_feature)

                    self._cclsource_table.dataProvider().addFeatures(new_features)

                else: # Fill pointsource table

                    if BOUNDARY_POINT_TABLE in feature_ids_dict:
                        for boundary_point_id in feature_ids_dict[BOUNDARY_POINT_TABLE]:
                            new_feature = QgsVectorLayerUtils().createFeature(self._pointsource_table)
                            new_feature.setAttribute(POINTSOURCE_TABLE_BOUNDARYPOINT_FIELD, boundary_point_id)
                            new_feature.setAttribute(POINTSOURCE_TABLE_SOURCE_FIELD, spatial_source_id)
                            self.log.logMessage("Saving BoundaryPoint-SpatialSource: {}-{}".format(boundary_point_id, spatial_source_id), PLUGIN_NAME, Qgis.Info)
                            new_features.append(new_feature)

                    if SURVEY_POINT_TABLE in feature_ids_dict:
                        for survey_point_id in feature_ids_dict[SURVEY_POINT_TABLE]:
                            new_feature = QgsVectorLayerUtils().createFeature(self._pointsource_table)
                            new_feature.setAttribute(POINTSOURCE_TABLE_SURVEYPOINT_FIELD, survey_point_id)
                            new_feature.setAttribute(POINTSOURCE_TABLE_SOURCE_FIELD, spatial_source_id)
                            self.log.logMessage("Saving SurveyPoint-SpatialSource: {}-{}".format(survey_point_id, spatial_source_id), PLUGIN_NAME, Qgis.Info)
                            new_features.append(new_feature)

                    if CONTROL_POINT_TABLE in feature_ids_dict:
                        for control_point_id in feature_ids_dict[CONTROL_POINT_TABLE]:
                            new_feature = QgsVectorLayerUtils().createFeature(self._pointsource_table)
                            new_feature.setAttribute(POINTSOURCE_TABLE_CONTROLPOINT_FIELD, control_point_id)
                            new_feature.setAttribute(POINTSOURCE_TABLE_SOURCE_FIELD, spatial_source_id)
                            self.log.logMessage("Saving ControlPoint-SpatialSource: {}-{}".format(control_point_id, spatial_source_id), PLUGIN_NAME, Qgis.Info)
                            new_features.append(new_feature)

                    self._pointsource_table.dataProvider().addFeatures(new_features)

                if new_features:
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
