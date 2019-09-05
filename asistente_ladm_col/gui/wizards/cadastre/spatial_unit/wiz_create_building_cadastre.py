# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 19/04/18
        git sha              : :%H$
        copyright            : (C) 2018 by Jorge Useche (Incige SAS)
        email                : naturalmentejorge@gmail.com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import (QCoreApplication,
                              QSettings)
from qgis.PyQt.QtWidgets import (QWizard,
                                 QToolBar,
                                 QMessageBox)
from qgis.core import (QgsProject,
                       QgsApplication,
                       Qgis,
                       QgsMapLayerProxyModel,
                       QgsWkbTypes)

from .....config.general_config import (PLUGIN_NAME,
                                        TOOLBAR_ID,
                                        TOOLBAR_FINALIZE_GEOMETRY_CREATION,
                                        LAYER)
from .....config.help_strings import HelpStrings
from .....config.table_mapping_config import (BUILDING_TABLE,
                                              ID_FIELD,
                                              SURVEY_POINT_TABLE)
from .....utils import get_ui_class

WIZARD_UI = get_ui_class('wizards/cadastre/spatial_unit/wiz_create_building_cadastre.ui')


class CreateBuildingCadastreWizard(QWizard, WIZARD_UI):
    WIZARD_NAME = "CreateBuildingCadastreWizard"
    WIZARD_TOOL_NAME = QCoreApplication.translate(WIZARD_NAME, "Create building")
    EDITING_LAYER_NAME = ""

    def __init__(self, iface, db, qgis_utils, toolbar, parent=None):
        QWizard.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self.log = QgsApplication.messageLog()
        self._db = db
        self.qgis_utils = qgis_utils
        self.toolbar = toolbar
        self.help_strings = HelpStrings()

        self._layers = {
            BUILDING_TABLE: {'name': BUILDING_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            SURVEY_POINT_TABLE: {'name': SURVEY_POINT_TABLE, 'geometry': None, LAYER: None}
        }

        self.EDITING_LAYER_NAME = BUILDING_TABLE

        self.restore_settings()
        self.rad_digitizing.toggled.connect(self.adjust_page_1_controls)
        self.adjust_page_1_controls()

        self.button(QWizard.FinishButton).clicked.connect(self.finished_dialog)
        self.button(QWizard.HelpButton).clicked.connect(self.show_help)
        self.rejected.connect(self.close_wizard)
        self.mMapLayerComboBox.setFilters(QgsMapLayerProxyModel.PolygonLayer)

    def adjust_page_1_controls(self):
        self.cbo_mapping.clear()
        self.cbo_mapping.addItem("")
        self.cbo_mapping.addItems(self.qgis_utils.get_field_mappings_file_names(BUILDING_TABLE))

        self.toolbar.wiz_geometry_created_requested.connect(self.wiz_geometry_created)

        if self.rad_refactor.isChecked():
            self.lbl_refactor_source.setEnabled(True)
            self.mMapLayerComboBox.setEnabled(True)
            self.lbl_field_mapping.setEnabled(True)
            self.cbo_mapping.setEnabled(True)
            finish_button_text = QCoreApplication.translate(self.WIZARD_NAME, "Import")
            self.txt_help_page_1.setHtml(self.help_strings.get_refactor_help_string(BUILDING_TABLE, True))

        elif self.rad_digitizing.isChecked():
            self.lbl_refactor_source.setEnabled(False)
            self.mMapLayerComboBox.setEnabled(False)
            self.lbl_field_mapping.setEnabled(False)
            self.cbo_mapping.setEnabled(False)
            finish_button_text = QCoreApplication.translate(self.WIZARD_NAME, "Start")
            self.txt_help_page_1.setHtml(self.help_strings.WIZ_CREATE_BUILDING_CADASTRE_PAGE_1_OPTION_POINTS)

        self.wizardPage1.setButtonText(QWizard.FinishButton, finish_button_text)

    def disconnect_signals(self):
        # QGIS APP
        try:
            self._layers[self.EDITING_LAYER_NAME][LAYER].committedFeaturesAdded.disconnect(self.finish_feature_creation)
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
            if self.mMapLayerComboBox.currentLayer() is not None:
                field_mapping = self.cbo_mapping.currentText()
                res_etl_model = self.qgis_utils.show_etl_model(self._db,
                                                               self.mMapLayerComboBox.currentLayer(),
                                                               BUILDING_TABLE,
                                                               QgsWkbTypes.PolygonGeometry,
                                                               field_mapping)

                if res_etl_model:
                    if field_mapping:
                        self.qgis_utils.delete_old_field_mapping(field_mapping)

                    self.qgis_utils.save_field_mapping(BUILDING_TABLE)
            else:
                self.qgis_utils.message_emitted.emit(
                    QCoreApplication.translate(self.WIZARD_NAME,
                                               "Select a source layer to set the field mapping to '{}'.").format(
                        BUILDING_TABLE),
                    Qgis.Warning)

        elif self.rad_digitizing.isChecked():
            self.set_enable_finalize_geometry_creation_action(True)
            self.prepare_feature_creation()

    def prepare_feature_creation(self):
        # layers of interest are loaded
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

        self.set_enable_finalize_geometry_creation_action(False)
        self.disconnect_signals()
        self.close()

    def edit_feature(self):
        self.iface.layerTreeView().setCurrentLayer(self._layers[self.EDITING_LAYER_NAME][LAYER])
        self._layers[self.EDITING_LAYER_NAME][LAYER].committedFeaturesAdded.connect(self.finish_feature_creation)

        # Disable transactions groups
        QgsProject.instance().setAutoTransaction(False)

        # Activate snapping
        self.qgis_utils.active_snapping_all_layers(tolerance=9)
        self.open_form()

        self.qgis_utils.message_emitted.emit(
            QCoreApplication.translate(self.WIZARD_NAME,
                                       "You can now start capturing building digitizing on the map..."),
            Qgis.Info)

    def finish_feature_creation(self, layerId, features):
        message = QCoreApplication.translate(self.WIZARD_NAME,
                                             "'{}' tool has been closed because an error occurred while trying to save the data.").format(self.WIZARD_TOOL_NAME)
        fid = features[0].id()

        if not self._layers[self.EDITING_LAYER_NAME][LAYER].getFeature(fid).isValid():
            message = QCoreApplication.translate(self.WIZARD_NAME,
                                                 "'{}' tool has been closed. Feature not found in layer {}... It's not posible create a building unit. ").format(self.WIZARD_TOOL_NAME, BUILDING_TABLE)
            self.log.logMessage("Feature not found in layer {} ...".format(BUILDING_TABLE), PLUGIN_NAME, Qgis.Warning)
        else:
            feature_tid = self._layers[self.EDITING_LAYER_NAME][LAYER].getFeature(fid)[ID_FIELD]
            message = QCoreApplication.translate(self.WIZARD_NAME, "The new building unit (t_id={}) was successfully created ").format(feature_tid)

        self._layers[self.EDITING_LAYER_NAME][LAYER].committedFeaturesAdded.disconnect(self.finish_feature_creation)
        self.log.logMessage("Building unit's committedFeaturesAdded SIGNAL disconnected", PLUGIN_NAME, Qgis.Info)
        self.close_wizard(message)

    def open_form(self):
        layer = self._layers[self.EDITING_LAYER_NAME][LAYER]
        if not layer.isEditable():
            layer.startEditing()

        self.qgis_utils.suppress_form(layer, True)
        self.iface.actionAddFeature().trigger()

    def exec_form(self):
        self.set_enable_finalize_geometry_creation_action(False)

        layer = self._layers[self.EDITING_LAYER_NAME][LAYER]

        for id, added_feature in layer.editBuffer().addedFeatures().items():
            feature = added_feature
            break

        dialog = self.iface.getFeatureForm(layer, feature)
        dialog.rejected.connect(self.form_rejected)
        dialog.setModal(True)

        if dialog.exec_():
            saved = layer.commitChanges()
            if not saved:
                layer.rollBack()
                self.qgis_utils.message_emitted.emit(
                    QCoreApplication.translate(self.WIZARD_NAME,
                                               "Error while saving changes. Building could not be created."), Qgis.Warning)
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
        settings.setValue('Asistente-LADM_COL/wizards/building_load_data_type', 'digitizing' if self.rad_digitizing.isChecked() else 'refactor')

    def restore_settings(self):
        settings = QSettings()

        load_data_type = settings.value('Asistente-LADM_COL/wizards/building_load_data_type') or 'digitizing'
        if load_data_type == 'refactor':
            self.rad_refactor.setChecked(True)
        else:
            self.rad_digitizing.setChecked(True)

    def show_help(self):
        self.qgis_utils.show_help("create_building")

    def wiz_geometry_created(self):
        message = None
        if self._layers[self.EDITING_LAYER_NAME][LAYER].editBuffer():
            if len(self._layers[self.EDITING_LAYER_NAME][LAYER].editBuffer().addedFeatures()) == 1:
                feature = [value for index, value in self._layers[self.EDITING_LAYER_NAME][LAYER].editBuffer().addedFeatures().items()][0]
                if feature.geometry().isGeosValid():
                    self.exec_form()
                else:
                    message = QCoreApplication.translate(self.WIZARD_NAME, "Geometry is invalid. Do you want to stop creating building?")
            else:
                if len(self._layers[self.EDITING_LAYER_NAME][LAYER].editBuffer().addedFeatures()) == 0:
                    message = QCoreApplication.translate(self.WIZARD_NAME, "Geometry was not created. Do you want to stop creating building?")
                else:
                    message = QCoreApplication.translate(self.WIZARD_NAME, "Many geometries were created but one was expected. Do you want to stop creating building?")

        if message:
            self.show_message_associate_geometry_creation(message)

    def show_message_associate_geometry_creation(self, message):
        reply = QMessageBox.question(self,
                                     QCoreApplication.translate(self.WIZARD_NAME, "Stop building creation?"),
                                     message,
                                     QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            # stop edition in close_wizard crash qgis
            if self._layers[self.EDITING_LAYER_NAME][LAYER].isEditable():
                self._layers[self.EDITING_LAYER_NAME][LAYER].rollBack()

            message = QCoreApplication.translate(self.WIZARD_NAME, "'{}' tool has been closed.").format(
                self.WIZARD_TOOL_NAME)
            self.close_wizard(message)
        else:
            # Continue creating geometry
            pass

    def set_enable_finalize_geometry_creation_action(self, enable):
        finalize_geometry_creation_action = self.get_toolbar_finalize_geometry_creation_action()
        if finalize_geometry_creation_action:
            finalize_geometry_creation_action.setEnabled(enable)

    def get_toolbar_finalize_geometry_creation_action(self):
        for toolbar in self.iface.mainWindow().findChildren(QToolBar, TOOLBAR_ID):
            for action in toolbar.actions():
                if not action.isSeparator():
                    if action.text() == TOOLBAR_FINALIZE_GEOMETRY_CREATION:
                        return action
        return None
