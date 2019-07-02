# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 06/09/18
        git sha              : :%H$
        copyright            : (C) 2018 by Sergio Ramírez (Incige SAS)
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

from qgis.PyQt.QtCore import (QCoreApplication,
                              QSettings)
from qgis.PyQt.QtWidgets import QWizard
from qgis.core import (Qgis,
                       QgsApplication,
                       QgsMapLayerProxyModel,
                       QgsProject,
                       QgsVectorLayer,
                       QgsWkbTypes,
                       QgsVectorLayerUtils)

import processing
from .....config.general_config import (TranslatableConfigStrings,
                                        LAYER,
                                        DEFAULT_EPSG,
                                        PLUGIN_NAME)
from .....config.help_strings import HelpStrings
from .....config.table_mapping_config import (ID_FIELD,
                                              PLOT_TABLE,
                                              RIGHT_OF_WAY_TABLE,
                                              SURVEY_POINT_TABLE)
from .....utils import get_ui_class

WIZARD_UI = get_ui_class('wiz_create_right_of_way_cadastre.ui')


class CreateRightOfWayCadastreWizard(QWizard, WIZARD_UI):
    WIZARD_CREATES_SPATIAL_FEATURE = True
    WIZARD_NAME = "CreateRightOfWayCadastreWizard"
    WIZARD_TOOL_NAME = QCoreApplication.translate(WIZARD_NAME, "Create Right of way")

    def __init__(self, iface, db, qgis_utils, parent=None):
        QWizard.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self.log = QgsApplication.messageLog()
        self._db = db
        self.qgis_utils = qgis_utils
        self.help_strings = HelpStrings()
        self.translatable_config_strings = TranslatableConfigStrings()

        self.type_geometry_creation = None
        self.addedFeatures = None

        self._layers = {
            PLOT_TABLE: {'name': PLOT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            RIGHT_OF_WAY_TABLE: {'name': RIGHT_OF_WAY_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            SURVEY_POINT_TABLE: {'name': SURVEY_POINT_TABLE, 'geometry': None, LAYER: None}
        }

        self.restore_settings()
        self.rad_digitizing.toggled.connect(self.adjust_page_1_controls)
        self.rad_digitizing_line.toggled.connect(self.adjust_page_1_controls)
        self.adjust_page_1_controls()

        self.button(QWizard.FinishButton).clicked.connect(self.finished_dialog)
        self.button(QWizard.HelpButton).clicked.connect(self.show_help)
        self.width_line_edit.setValue(1.0)
        self.rejected.connect(self.close_wizard)
        self.mMapLayerComboBox.setFilters(QgsMapLayerProxyModel.PolygonLayer)

    def adjust_page_1_controls(self):
        self.cbo_mapping.clear()
        self.cbo_mapping.addItem("")
        self.cbo_mapping.addItems(self.qgis_utils.get_field_mappings_file_names(RIGHT_OF_WAY_TABLE))

        if self.rad_refactor.isChecked():
            self.lbl_width.setEnabled(False)
            self.width_line_edit.setEnabled(False)
            self.lbl_refactor_source.setEnabled(True)
            self.mMapLayerComboBox.setEnabled(True)
            self.lbl_field_mapping.setEnabled(True)
            self.cbo_mapping.setEnabled(True)
            finish_button_text = QCoreApplication.translate(self.WIZARD_NAME, "Import")
            self.txt_help_page_1.setHtml(self.help_strings.get_refactor_help_string(RIGHT_OF_WAY_TABLE, True))

        elif self.rad_digitizing.isChecked():
            self.lbl_refactor_source.setEnabled(False)
            self.mMapLayerComboBox.setEnabled(False)
            self.lbl_width.setEnabled(False)
            self.width_line_edit.setEnabled(False)
            self.lbl_field_mapping.setEnabled(False)
            self.cbo_mapping.setEnabled(False)
            finish_button_text = QCoreApplication.translate(self.WIZARD_NAME, "Start")
            self.txt_help_page_1.setHtml(self.help_strings.WIZ_CREATE_RIGHT_OF_WAY_CADASTRE_PAGE_1_OPTION_POINTS)

        elif self.rad_digitizing_line.isChecked():
            self.width_line_edit.setEnabled(True)
            self.lbl_width.setEnabled(True)
            self.lbl_refactor_source.setEnabled(False)
            self.mMapLayerComboBox.setEnabled(False)
            self.lbl_field_mapping.setEnabled(False)
            self.cbo_mapping.setEnabled(False)
            finish_button_text = QCoreApplication.translate(self.WIZARD_NAME, "Start")
            self.txt_help_page_1.setHtml(self.help_strings.WIZ_CREATE_RIGHT_OF_WAY_CADASTRE_PAGE_1_OPTION2_POINTS)

        self.wizardPage1.setButtonText(QWizard.FinishButton, finish_button_text)

    def disconnect_signals(self):
        # QGIS APP
        try:
            self._layers[RIGHT_OF_WAY_TABLE][LAYER].featureAdded.disconnect()
        except:
            pass

        try:
            self._layers[RIGHT_OF_WAY_TABLE][LAYER].committedFeaturesAdded.disconnect(self.finish_feature_creation)
        except:
            pass

        for layer_name in self._layers:
            try:
                self._layers[layer_name][LAYER].willBeDeleted.disconnect(self.layer_removed)
            except:
                pass

    def finished_dialog(self):
        self.save_settings()

        if self.rad_refactor.isChecked():
            self.type_geometry_creation = None
            if self.mMapLayerComboBox.currentLayer() is not None:
                field_mapping = self.cbo_mapping.currentText()
                res_etl_model = self.qgis_utils.show_etl_model(self._db,
                                               self.mMapLayerComboBox.currentLayer(),
                                               RIGHT_OF_WAY_TABLE,
                                               field_mapping=field_mapping)

                if res_etl_model:
                    if field_mapping:
                        self.qgis_utils.delete_old_field_mapping(field_mapping)

                    self.qgis_utils.save_field_mapping(RIGHT_OF_WAY_TABLE)

            else:
                self.iface.messageBar().pushMessage('Asistente LADM_COL',
                    QCoreApplication.translate(self.WIZARD_NAME,
                                               "Select a source layer to set the field mapping to '{}'.").format(RIGHT_OF_WAY_TABLE),
                    Qgis.Warning)

        elif self.rad_digitizing.isChecked():
            self.type_geometry_creation = "digitizing_polygon"
            self.prepare_feature_creation()
        elif self.rad_digitizing_line.isChecked():
            self.type_geometry_creation = "digitizing_line"
            self.prepare_feature_creation()

    def prepare_feature_creation(self):
        result = self.prepare_feature_creation_layers()
        if result is None:
            return
        self.edit_feature()

    def prepare_feature_creation_layers(self):
        # Load layers
        res_layers = self.qgis_utils.get_layers(self._db, self._layers, load=True)
        if res_layers is None:
            return

        # Add signal to check if a layer was removed
        self.validate_remove_layers()

        # All layers were successfully loaded
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

    def close_wizard(self, message=None):
        if message is None:
            message = QCoreApplication.translate(self.WIZARD_NAME, "'{}' tool has been closed.").format(self.WIZARD_TOOL_NAME)
        self.iface.messageBar().pushMessage("Asistente LADM_COL", message, Qgis.Info)

        self.disconnect_signals()
        self.close()

    def edit_feature(self):

        # Disable transactions groups and configure Snapping
        QgsProject.instance().setAutoTransaction(False)
        self.qgis_utils.active_snapping_all_layers(tolerance=9)

        layer = None
        if self.type_geometry_creation == "digitizing_polygon":
            layer = self._layers[RIGHT_OF_WAY_TABLE][LAYER]
        elif self.type_geometry_creation == "digitizing_line":
            # Add Memory line layer
            layer = QgsVectorLayer("MultiLineString?crs=EPSG:{}".format(DEFAULT_EPSG), self.translatable_config_strings.RIGHT_OF_WAY_LINE_LAYER, "memory")
            QgsProject.instance().addMapLayer(layer, True)
        else:
            return

        if layer:
            self.iface.layerTreeView().setCurrentLayer(layer)
            self._layers[RIGHT_OF_WAY_TABLE][LAYER].committedFeaturesAdded.connect(self.finish_feature_creation)
            self.open_form(layer)

    def store_features_ids(self, featId):
        """
        This method only stores featIds in a class variable. It's required to avoid a bug with SLOTS connected to
        featureAdded.
        """
        self.addedFeatures = featId

    def update_attributes_after_adding(self):
        layer = self.sender()  # Get the layer that has sent the signal
        layer.featureAdded.disconnect(self.store_features_ids)
        self.log.logMessage("RigthOfWayLine's featureAdded SIGNAL disconnected", PLUGIN_NAME, Qgis.Info)
        res = layer.commitChanges()
        QgsProject.instance().removeMapLayer(layer)
        self.addedFeatures = None

    def finish_feature_creation(self, layerId, features):
        message = QCoreApplication.translate(self.WIZARD_NAME,
                                             "'{}' tool has been closed because an error occurred while trying to save the data.").format(
            self.WIZARD_TOOL_NAME)
        fid = features[0].id()

        if not self._layers[RIGHT_OF_WAY_TABLE][LAYER].getFeature(fid).isValid():
            message = QCoreApplication.translate(self.WIZARD_NAME,
                                                 "'{}' tool has been closed. Feature not found in layer {}... It's not posible create a right of way. ").format(
                self.WIZARD_TOOL_NAME, RIGHT_OF_WAY_TABLE)
            self.log.logMessage("Feature not found in layer {} ...".format(RIGHT_OF_WAY_TABLE), PLUGIN_NAME,
                                Qgis.Warning)
        else:
            feature_tid = self._layers[RIGHT_OF_WAY_TABLE][LAYER].getFeature(fid)[ID_FIELD]
            message = QCoreApplication.translate(self.WIZARD_NAME,
                                                 "The new right of way (t_id={}) was successfully created ").format(
                feature_tid)

        self._layers[RIGHT_OF_WAY_TABLE][LAYER].committedFeaturesAdded.disconnect(self.finish_feature_creation)
        self.log.logMessage("Right of way's committedFeaturesAdded SIGNAL disconnected", PLUGIN_NAME, Qgis.Info)
        self.close_wizard(message)

    def open_form(self, layer):
        if not layer.isEditable():
            layer.startEditing()

        if self.WIZARD_CREATES_SPATIAL_FEATURE:
            self.iface.messageBar().pushMessage('Asistente LADM_COL',
                                           QCoreApplication.translate(self.WIZARD_NAME,
                                                                      "You can now start capturing right of ways digitizing on the map..."),
                                           Qgis.Info)

            # action add ExtAddress feature
            self.qgis_utils.suppress_form(layer, True)
            self.iface.actionAddFeature().trigger()

            # Shows the form when the feature is created
            layer.featureAdded.connect(partial(self.exec_form, layer))

        else:
            self.exec_form(layer)

    def exec_form(self, layer):
        try:
            # Disconnect signal to prevent add features
            layer.featureAdded.disconnect()
            self.log.logMessage("Feature added SIGNAL disconnected", PLUGIN_NAME, Qgis.Info)
        except:
            pass

        if self.type_geometry_creation == "digitizing_polygon":
            feature = self.qgis_utils.get_new_feature(layer, self.WIZARD_CREATES_SPATIAL_FEATURE)
        elif self.type_geometry_creation == "digitizing_line":

            # Get temporal right of way geometry
            feature = self.get_feature_with_buffer_right_of_way(layer)
            layer.commitChanges()

            # Remove temporal layer and set right of way as layer
            QgsProject.instance().removeMapLayer(layer)
            layer = self._layers[RIGHT_OF_WAY_TABLE][LAYER]

            # Add temporal geometry create
            if not layer.isEditable():
                layer.startEditing()

            self.qgis_utils.suppress_form(layer, True)
            layer.addFeature(feature)

        dialog = self.iface.getFeatureForm(layer, feature)
        dialog.rejected.connect(self.form_rejected)
        dialog.setModal(True)

        if dialog.exec_():
            saved = layer.commitChanges()

            if not saved:
                layer.rollBack()
                self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                                    QCoreApplication.translate(self.WIZARD_NAME,
                                                                               "Error while saving changes. ExtAddress could not be created."),
                                                    Qgis.Warning)
                for e in layer.commitErrors():
                    self.log.logMessage("Commit error: {}".format(e), PLUGIN_NAME, Qgis.Warning)

            self.iface.mapCanvas().refresh()
        else:
            # TODO: implement when the bug is removed
            # When feature form is cancel QGIS close sudenlly
            #layer.editBuffer().rollBack()
            # layer.rollBack()
            pass

    def get_feature_with_buffer_right_of_way(self, layer):
        params = {'INPUT': layer,
                  'DISTANCE': self.width_line_edit.value(),
                  'SEGMENTS': 5,
                  'END_CAP_STYLE': 1,  # Flat
                  'JOIN_STYLE': 2,
                  'MITER_LIMIT': 2,
                  'DISSOLVE': False,
                  'OUTPUT': 'memory:'}
        buffered_right_of_way_layer = processing.run("native:buffer", params)['OUTPUT']
        buffer_geometry = buffered_right_of_way_layer.getFeature(1).geometry()
        feature = QgsVectorLayerUtils().createFeature(self._layers[RIGHT_OF_WAY_TABLE][LAYER], buffer_geometry)
        return feature

    def form_rejected(self):
        message = QCoreApplication.translate(self.WIZARD_NAME,
                                             "'{}' tool has been closed because you just closed the form.").format(self.WIZARD_TOOL_NAME)
        self.close_wizard(message)

    def save_settings(self):
        settings = QSettings()

        load_data_type = 'refactor'
        if self.rad_digitizing.isChecked():
            load_data_type = 'digitizing'
        elif self.rad_digitizing_line.isChecked():
            load_data_type = 'digitizing_line'

        settings.setValue('Asistente-LADM_COL/wizards/right_of_way_load_data_type', load_data_type)

    def restore_settings(self):
        settings = QSettings()

        load_data_type = settings.value('Asistente-LADM_COL/wizards/right_of_way_load_data_type') or 'digitizing_line'
        if load_data_type == 'refactor':
            self.rad_refactor.setChecked(True)
        elif load_data_type == 'digitizing':
            self.rad_digitizing.setChecked(True)
        else:
            self.rad_digitizing_line.setChecked(True)

    def show_help(self):
        self.qgis_utils.show_help("create_right_of_way")
