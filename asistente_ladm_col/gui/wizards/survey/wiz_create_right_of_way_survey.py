# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-09-10
        git sha              : :%H$
        copyright            : (C) 2017 by Germán Carrillo (BSF Swissphoto)
                               (C) 2018 by Sergio Ramírez (Incige SAS)
                               (C) 2018 by Jorge Useche (Incige SAS)
                               (C) 2018 by Jhon Galindo (Incige SAS)
                               (C) 2019 by Leo Cardona (BSF Swissphoto)
        email                : gcarrillo@linuxmail.org
                               sergio.ramirez@incige.com
                               naturalmentejorge@gmail.com
                               jhonsigpjc@gmail.com
                               leo.cardona.p@gmail.com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""
import processing
from qgis.PyQt.QtCore import (QCoreApplication,
                              QSettings)
from qgis.PyQt.QtWidgets import (QWizard,
                                 QPushButton,
                                 QMessageBox)
from qgis.core import (QgsProject,
                       QgsVectorLayer,
                       QgsVectorLayerUtils,
                       QgsMapLayerProxyModel)

from asistente_ladm_col.config.general_config import (WIZARD_HELP_PAGES,
                                                      WIZARD_QSETTINGS,
                                                      WIZARD_QSETTINGS_LOAD_DATA_TYPE,
                                                      WIZARD_HELP1,
                                                      WIZARD_HELP2,
                                                      WIZARD_MAP_LAYER_PROXY_MODEL, DEFAULT_SRS_AUTHID)
from asistente_ladm_col.config.translation_strings import RIGHT_OF_WAY_LINE_LAYER
from asistente_ladm_col.gui.wizards.select_features_on_map_wrapper import SelectFeaturesOnMapWrapper
from asistente_ladm_col.gui.wizards.single_page_spatial_wizard_factory import SinglePageSpatialWizardFactory
from asistente_ladm_col.utils.crs_utils import get_crs_authid


class CreateRightOfWaySurveyWizard(SinglePageSpatialWizardFactory):
    def __init__(self, iface, db, wizard_settings):
        super(CreateRightOfWaySurveyWizard, self).__init__(iface, db, wizard_settings)
        self.type_geometry_creation = None
        self.temporal_layer = None

    #############################################################################
    # Override methods
    #############################################################################
    def init_gui(self):
        self.mMapLayerComboBox.setFilters(QgsMapLayerProxyModel.Filter(self.wizard_config[WIZARD_MAP_LAYER_PROXY_MODEL]))
        self.mMapLayerComboBox.layerChanged.connect(self.import_layer_changed)

        self.restore_settings()
        self.rad_create_manually.toggled.connect(self.adjust_page_1_controls)
        self.rad_digitizing_line.toggled.connect(self.adjust_page_1_controls)
        self.adjust_page_1_controls()

        self.button(QWizard.FinishButton).clicked.connect(self.finished_dialog)
        self.button(QWizard.HelpButton).clicked.connect(self.show_help)
        self.width_line_edit.setValue(1.0)
        self.rejected.connect(self.close_wizard)

    def adjust_page_1_controls(self):
        self.cbo_mapping.clear()
        self.cbo_mapping.addItem("")
        self.cbo_mapping.addItems(self.app.core.get_field_mappings_file_names(self.EDITING_LAYER_NAME))

        if self.rad_refactor.isChecked():
            self.lbl_width.setEnabled(False)
            self.width_line_edit.setEnabled(False)
            self.lbl_refactor_source.setEnabled(True)
            self.mMapLayerComboBox.setEnabled(True)
            self.lbl_field_mapping.setEnabled(True)
            self.cbo_mapping.setEnabled(True)
            self.import_layer_changed(self.mMapLayerComboBox.currentLayer())
            finish_button_text = QCoreApplication.translate("WizardTranslations", "Import")
            self.txt_help_page_1.setHtml(self.help_strings.get_refactor_help_string(self._db, self._layers[self.EDITING_LAYER_NAME]))
        elif self.rad_create_manually.isChecked():
            self.lbl_refactor_source.setEnabled(False)
            self.mMapLayerComboBox.setEnabled(False)
            self.lbl_width.setEnabled(False)
            self.width_line_edit.setEnabled(False)
            self.lbl_field_mapping.setEnabled(False)
            self.cbo_mapping.setEnabled(False)
            finish_button_text = QCoreApplication.translate("WizardTranslations", "Create")
            self.txt_help_page_1.setHtml(self.wizard_config[WIZARD_HELP_PAGES][WIZARD_HELP1])
            self.lbl_refactor_source.setStyleSheet('')
        elif self.rad_digitizing_line.isChecked():
            self.width_line_edit.setEnabled(True)
            self.lbl_width.setEnabled(True)
            self.lbl_refactor_source.setEnabled(False)
            self.mMapLayerComboBox.setEnabled(False)
            self.lbl_field_mapping.setEnabled(False)
            self.cbo_mapping.setEnabled(False)
            finish_button_text = QCoreApplication.translate("WizardTranslations", "Create")
            self.txt_help_page_1.setHtml(self.wizard_config[WIZARD_HELP_PAGES][WIZARD_HELP2])
            self.lbl_refactor_source.setStyleSheet('')

        self.wizardPage1.setButtonText(QWizard.FinishButton, finish_button_text)

    def finished_dialog(self):
        self.save_settings()

        if self.rad_refactor.isChecked():
            self.type_geometry_creation = None
            if self.mMapLayerComboBox.currentLayer() is not None:
                field_mapping = self.cbo_mapping.currentText()
                res_etl_model = self.app.core.show_etl_model(self._db,
                                                             self.mMapLayerComboBox.currentLayer(),
                                                             self.EDITING_LAYER_NAME,
                                                             field_mapping=field_mapping)
                if res_etl_model: # Features were added?
                    self.app.gui.redraw_all_layers()  # Redraw all layers to show imported data

                    # If the result of the etl_model is successful and we used a stored recent mapping, we delete the
                    # previous mapping used (we give preference to the latest used mapping)
                    if field_mapping:
                        self.app.core.delete_old_field_mapping(field_mapping)

                    self.app.core.save_field_mapping(self.EDITING_LAYER_NAME)

            else:
                self.logger.warning_msg(__name__, QCoreApplication.translate("WizardTranslations",
                    "Select a source layer to set the field mapping to '{}'.").format(self.EDITING_LAYER_NAME))

            self.close_wizard()

        elif self.rad_create_manually.isChecked():
            self.set_finalize_geometry_creation_enabled_emitted.emit(True)
            self.type_geometry_creation = "digitizing_polygon"
            self.prepare_feature_creation()
        elif self.rad_digitizing_line.isChecked():
            self.set_finalize_geometry_creation_enabled_emitted.emit(True)
            self.type_geometry_creation = "digitizing_line"
            self.prepare_feature_creation()

    def close_wizard(self, message=None, show_message=True):
        if message is None:
            message = QCoreApplication.translate("WizardTranslations", "'{}' tool has been closed.").format(self.WIZARD_TOOL_NAME)
        if show_message:
            self.logger.info_msg(__name__, message)

        if isinstance(self, SelectFeaturesOnMapWrapper):
            self.init_map_tool()

        self.rollback_in_layers_with_empty_editing_buffer()
        self.remove_temporal_layer()
        self.set_finalize_geometry_creation_enabled_emitted.emit(False)
        self.disconnect_signals()
        self.update_wizard_is_open_flag.emit(False)
        self.close()

    def remove_temporal_layer(self):
        if self.temporal_layer:
            self.temporal_layer.rollBack()
            QgsProject.instance().removeMapLayer(self.temporal_layer)

    def edit_feature(self):

        translated_strings = self.translatable_config_strings.get_translatable_config_strings()

        layer = None
        if self.type_geometry_creation == "digitizing_polygon":
            layer = self._layers[self.EDITING_LAYER_NAME]
        elif self.type_geometry_creation == "digitizing_line":
            # Add Memory line layer
            self.temporal_layer = QgsVectorLayer("MultiLineString?crs={}".format(get_crs_authid(self._layers[self.EDITING_LAYER_NAME].sourceCrs())), translated_strings[RIGHT_OF_WAY_LINE_LAYER], "memory")
            layer = self.temporal_layer
            QgsProject.instance().addMapLayer(self.temporal_layer, True)
        else:
            return

        if layer:
            self.iface.layerTreeView().setCurrentLayer(layer)
            self._layers[self.EDITING_LAYER_NAME].committedFeaturesAdded.connect(self.finish_feature_creation)

            # Disable transactions groups
            QgsProject.instance().setAutoTransaction(False)

            # Activate snapping
            self.app.core.active_snapping_all_layers(tolerance=9)
            self.open_form(layer)

            self.logger.info_msg(__name__, QCoreApplication.translate("WizardTranslations",
                "You can now start capturing {} digitizing on the map...").format(self.WIZARD_FEATURE_NAME))

    def post_save(self, features):
        message = QCoreApplication.translate("WizardTranslations",
                                             "'{}' tool has been closed because an error occurred while trying to save the data.").format(self.WIZARD_TOOL_NAME)
        fid = features[0].id()

        if not self._layers[self.EDITING_LAYER_NAME].getFeature(fid).isValid():
            message = QCoreApplication.translate("WizardTranslations", "'{}' tool has been closed. Feature not found in layer {}... It's not posible create a {}. ").format(self.WIZARD_TOOL_NAME, self.EDITING_LAYER_NAME, self.WIZARD_FEATURE_NAME)
            self.logger.warning(__name__, "Feature not found in layer {} ...".format(self.EDITING_LAYER_NAME))
        else:
            feature_tid = self._layers[self.EDITING_LAYER_NAME].getFeature(fid)[self.names.T_ID_F]
            message = QCoreApplication.translate("WizardTranslations", "The new {} (t_id={}) was successfully created ").format(self.WIZARD_FEATURE_NAME, feature_tid)

        return message

    def exec_form(self, layer):
        self.set_finalize_geometry_creation_enabled_emitted.emit(False)
        feature = None
        if self.type_geometry_creation == "digitizing_polygon":
            for id, added_feature in layer.editBuffer().addedFeatures().items():
                feature = added_feature
                break
        elif self.type_geometry_creation == "digitizing_line":
            # Get temporal right of way geometry
            feature = self.get_feature_with_buffer_right_of_way(layer)
            layer.commitChanges()

            # Change target layer (temporal by db layer)
            layer = self._layers[self.EDITING_LAYER_NAME]

            # Add temporal geometry create
            if not layer.isEditable():
                layer.startEditing()

            self.app.core.suppress_form(layer, True)
            layer.addFeature(feature)

        dialog = self.iface.getFeatureForm(layer, feature)
        dialog.rejected.connect(self.form_rejected)
        dialog.setModal(True)

        if dialog.exec_():
            self.exec_form_advanced(layer)
            saved = layer.commitChanges()

            if not saved:
                layer.rollBack()
                self.logger.warning_msg(__name__, QCoreApplication.translate("WizardTranslations",
                    "Error while saving changes. {} could not be created.").format(self.WIZARD_FEATURE_NAME))
                for e in layer.commitErrors():
                    self.logger.warning(__name__, "Commit error: {}".format(e))
        else:
            layer.rollBack()
        self.iface.mapCanvas().refresh()

    def get_feature_with_buffer_right_of_way(self, layer):
        params = {'INPUT': layer,
                  'DISTANCE': self.width_line_edit.value(),
                  'SEGMENTS': 5,
                  'END_CAP_STYLE': 1,  # Flat
                  'JOIN_STYLE': 2,
                  'MITER_LIMIT': 2,
                  'DISSOLVE': False,
                  'OUTPUT': 'TEMPORARY_OUTPUT'}
        buffered_right_of_way_layer = processing.run("native:buffer", params)['OUTPUT']
        buffer_geometry = buffered_right_of_way_layer.getFeature(1).geometry()
        feature = QgsVectorLayerUtils().createFeature(self._layers[self.EDITING_LAYER_NAME], buffer_geometry)
        return feature

    def import_layer_changed(self, layer):
        if layer:
            crs = get_crs_authid(layer.crs())
            if crs != DEFAULT_SRS_AUTHID:
                self.lbl_refactor_source.setStyleSheet('color: orange')
                self.lbl_refactor_source.setToolTip(QCoreApplication.translate("WizardTranslations",
                                                                   "This layer will be reprojected for you to '{}' (Colombian National Origin),<br>before attempting to import it into LADM-COL.").format(
                    DEFAULT_SRS_AUTHID))
            else:
                self.lbl_refactor_source.setStyleSheet('')
                self.lbl_refactor_source.setToolTip('')

    def save_settings(self):
        settings = QSettings()

        load_data_type = 'refactor'
        if self.rad_create_manually.isChecked():
            load_data_type = 'create_manually'
        elif self.rad_digitizing_line.isChecked():
            load_data_type = 'digitizing_line'

        settings.setValue(self.wizard_config[WIZARD_QSETTINGS][WIZARD_QSETTINGS_LOAD_DATA_TYPE], load_data_type)

    def restore_settings(self):
        settings = QSettings()

        load_data_type = settings.value(self.wizard_config[WIZARD_QSETTINGS][WIZARD_QSETTINGS_LOAD_DATA_TYPE]) or 'digitizing_line'
        if load_data_type == 'refactor':
            self.rad_refactor.setChecked(True)
        elif load_data_type == 'create_manually':
            self.rad_create_manually.setChecked(True)
        else:
            self.rad_digitizing_line.setChecked(True)

    def save_created_geometry(self):
        layer = None
        if self.type_geometry_creation == "digitizing_polygon":
            layer = self._layers[self.EDITING_LAYER_NAME]
        elif self.type_geometry_creation == "digitizing_line":
            try:
                if self.temporal_layer:
                    layer = self.temporal_layer
                else:
                    layer = self._layers[self.EDITING_LAYER_NAME]
            except:
                layer = self._layers[self.EDITING_LAYER_NAME]

        message = None
        if layer.editBuffer():
            if len(layer.editBuffer().addedFeatures()) == 1:
                feature = [value for index, value in layer.editBuffer().addedFeatures().items()][0]
                if feature.geometry().isGeosValid():
                    self.exec_form(layer)
                else:
                    message = QCoreApplication.translate("WizardTranslations", "Geometry is invalid. Do you want to return to the editing session?")
            else:
                if len(layer.editBuffer().addedFeatures()) == 0:
                    message = QCoreApplication.translate("WizardTranslations", "Geometry was not created. Do you want to return to the editing session?")
                else:
                    message = QCoreApplication.translate("WizardTranslations", "Many geometries were created but one was expected. Do you want to return to the editing session?")

        if message:
            self.show_message_associate_geometry_creation(message)

    def show_message_associate_geometry_creation(self, message):
        layer = None
        if self.type_geometry_creation == "digitizing_polygon":
            layer = self._layers[self.EDITING_LAYER_NAME]
        elif self.type_geometry_creation == "digitizing_line":
            layer = self.temporal_layer

        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Question)
        msg.setText(message)
        msg.setWindowTitle(QCoreApplication.translate("WizardTranslations", "Continue editing?"))
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.button(QMessageBox.No).setText(QCoreApplication.translate("WizardTranslations", "No, close the wizard"))
        reply = msg.exec_()

        if reply == QMessageBox.No:
            # stop edition in close_wizard crash qgis
            if layer.isEditable():
                layer.rollBack()

            message = QCoreApplication.translate("WizardTranslations", "'{}' tool has been closed.").format(
                self.WIZARD_TOOL_NAME)
            self.close_wizard(message)
        else:
            # Continue creating geometry
            pass
