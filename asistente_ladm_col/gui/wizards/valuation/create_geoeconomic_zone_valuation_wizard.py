# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2018-11-23
        git sha              : :%H$
        copyright            : (C) 2018 by Jhon Galindo
        email                : jhonsigpjc@gmail.com
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
from qgis.core import (QgsProject,
                       QgsApplication,
                       Qgis,
                       QgsMapLayerProxyModel,
                       QgsWkbTypes)

from ....config.general_config import (PLUGIN_NAME,
                                       LAYER)
from ....config.help_strings import HelpStrings
from ....config.table_mapping_config import (ID_FIELD,
                                             VALUATION_GEOECONOMIC_ZONE_TABLE)
from ....utils import get_ui_class

WIZARD_UI = get_ui_class('wizards/valuation/wiz_create_geoeconomic_zone_valuation.ui')


class CreateGeoeconomicZoneValuationWizard(QWizard, WIZARD_UI):
    WIZARD_NAME = "CreateGeoeconomicZoneValuationWizard"
    WIZARD_TOOL_NAME = QCoreApplication.translate(WIZARD_NAME, "Create geoeconomic zone")

    def __init__(self, iface, db, qgis_utils, parent=None):
        QWizard.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self.log = QgsApplication.messageLog()
        self._db = db
        self.qgis_utils = qgis_utils
        self.help_strings = HelpStrings()

        # Necessary to control featureAdded bug (crash QGIS)
        # https://gis.stackexchange.com/a/229949/120426
        self.added_features = None
        self.rollback_changes = False

        self._layers = {
            VALUATION_GEOECONOMIC_ZONE_TABLE: {'name': VALUATION_GEOECONOMIC_ZONE_TABLE, 'geometry': None, LAYER: None}
        }

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
        self.cbo_mapping.addItems(self.qgis_utils.get_field_mappings_file_names(VALUATION_GEOECONOMIC_ZONE_TABLE))

        if self.rad_refactor.isChecked():
            self.lbl_refactor_source.setEnabled(True)
            self.mMapLayerComboBox.setEnabled(True)
            self.lbl_field_mapping.setEnabled(True)
            self.cbo_mapping.setEnabled(True)
            finish_button_text = QCoreApplication.translate(self.WIZARD_NAME, "Import")
            self.txt_help_page_1.setHtml(
                self.help_strings.get_refactor_help_string(VALUATION_GEOECONOMIC_ZONE_TABLE, True))

        elif self.rad_digitizing.isChecked():
            self.lbl_refactor_source.setEnabled(False)
            self.mMapLayerComboBox.setEnabled(False)
            self.lbl_field_mapping.setEnabled(False)
            self.cbo_mapping.setEnabled(False)
            finish_button_text = QCoreApplication.translate(self.WIZARD_NAME, "Start")
            self.txt_help_page_1.setHtml(self.help_strings.WIZ_CREATE_GEOECONOMIC_ZONE_VALUATION_PAGE_1_OPTION_FORM)

        self.wizardPage1.setButtonText(QWizard.FinishButton, finish_button_text)

    def disconnect_signals(self):
        # QGIS APP
        try:
            self._layers[VALUATION_GEOECONOMIC_ZONE_TABLE][LAYER].featureAdded.disconnect()
        except:
            pass

        try:
            self._layers[VALUATION_GEOECONOMIC_ZONE_TABLE][LAYER].editCommandEnded.disconnect(self.confirm_commit)
        except:
            pass

        try:
            self._layers[VALUATION_GEOECONOMIC_ZONE_TABLE][LAYER].committedFeaturesAdded.disconnect(self.finish_feature_creation)
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
                                                               VALUATION_GEOECONOMIC_ZONE_TABLE,
                                                               QgsWkbTypes.PolygonGeometry,
                                                               field_mapping)

                if res_etl_model:
                    if field_mapping:
                        self.qgis_utils.delete_old_field_mapping(field_mapping)

                    self.qgis_utils.save_field_mapping(VALUATION_GEOECONOMIC_ZONE_TABLE)
            else:
                self.iface.messageBar().pushMessage('Asistente LADM_COL',
                                                    QCoreApplication.translate(self.WIZARD_NAME,
                                                                               "Select a source layer to set the field mapping to '{}'.").format(
                                                        VALUATION_GEOECONOMIC_ZONE_TABLE),
                                                    Qgis.Warning)

        elif self.rad_digitizing.isChecked():
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
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                                QCoreApplication.translate(self.WIZARD_NAME,
                                                                           "'{}' tool has been closed because there was a problem loading the requeries layers.").format(self.WIZARD_TOOL_NAME),
                                                Qgis.Warning)
            return False

        # Check if layers any layer is in editing mode
        layers_name = list()
        for layer in self._layers:
            if self._layers[layer]['layer'].isEditable():
                layers_name.append(self._layers[layer]['layer'].name())

        if layers_name:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                                QCoreApplication.translate(self.WIZARD_NAME,
                                                                           "Wizard cannot be opened until the following layers are not in edit mode '{}'.").format(
                                                    '; '.join([layer_name for layer_name in layers_name])),
                                                Qgis.Warning)
            return False

        # Resolve bug associate with undoStack
        for layer_name in self._layers:
            try:
                self._layers[layer_name][LAYER].undoStack().clear()
            except:
                pass

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
                                             "'{}' tool has been closed because you just removed a required layer.").format(
            self.WIZARD_TOOL_NAME)
        self.close_wizard(message)

    def close_wizard(self, message=None, show_message=True):
        if message is None:
            message = QCoreApplication.translate(self.WIZARD_NAME, "'{}' tool has been closed.").format(
                self.WIZARD_TOOL_NAME)
        if show_message:
            self.iface.messageBar().pushMessage("Asistente LADM_COL", message, Qgis.Info)
        self.disconnect_signals()
        self.close()

    def edit_feature(self):
        self.iface.layerTreeView().setCurrentLayer(self._layers[VALUATION_GEOECONOMIC_ZONE_TABLE][LAYER])
        #self._layers[VALUATION_GEOECONOMIC_ZONE_TABLE][LAYER].committedFeaturesAdded.connect(self.finish_feature_creation)

        # Disable transactions groups
        QgsProject.instance().setAutoTransaction(False)

        # Activate snapping
        self.qgis_utils.active_snapping_all_layers(tolerance=9)
        self.open_form(self._layers[VALUATION_GEOECONOMIC_ZONE_TABLE][LAYER])

        self.iface.messageBar().pushMessage('Asistente LADM_COL',
                                            QCoreApplication.translate(self.WIZARD_NAME,
                                                                       "You can now start capturing geoeconomic zone digitizing on the map..."),
                                            Qgis.Info)

    def finish_feature_creation(self, layerId, features):
        message = QCoreApplication.translate(self.WIZARD_NAME,
                                             "'{}' tool has been closed because an error occurred while trying to save the data.").format(
            self.WIZARD_TOOL_NAME)
        fid = features[0].id()

        if not self._layers[VALUATION_GEOECONOMIC_ZONE_TABLE][LAYER].getFeature(fid).isValid():
            message = QCoreApplication.translate(self.WIZARD_NAME,
                                                 "'{}' tool has been closed. Feature not found in layer {}... It's not posible create a geoeconomic zone. ").format(
                self.WIZARD_TOOL_NAME, VALUATION_GEOECONOMIC_ZONE_TABLE)
            self.log.logMessage("Feature not found in layer {} ...".format(VALUATION_GEOECONOMIC_ZONE_TABLE),
                                PLUGIN_NAME, Qgis.Warning)
        else:
            feature_tid = self._layers[VALUATION_GEOECONOMIC_ZONE_TABLE][LAYER].getFeature(fid)[ID_FIELD]
            message = QCoreApplication.translate(self.WIZARD_NAME,
                                                 "The new geoeconomic zone (t_id={}) was successfully created ").format(
                feature_tid)

        self._layers[VALUATION_GEOECONOMIC_ZONE_TABLE][LAYER].committedFeaturesAdded.disconnect(self.finish_feature_creation)
        self.log.logMessage("Geoeconomic zone's committedFeaturesAdded SIGNAL disconnected", PLUGIN_NAME, Qgis.Info)
        self.close_wizard(message)

    def open_form(self, layer):
        if not layer.isEditable():
            layer.startEditing()

        # action add feature
        self.qgis_utils.suppress_form(layer, True)
        self.iface.actionAddFeature().trigger()

        # Shows the form when the feature is created
        layer.featureAdded.connect(partial(self.exec_form, layer))
        #layer.editCommandEnded.connect(self.confirm_commit)

    def exec_form(self, layer, f_id):
        """
        This method only stores featIds in a class variable. It's required to avoid a bug with SLOTS connected to
        featureAdded.
        """
        self.added_features = f_id

        feature = self.qgis_utils.get_new_feature(layer)
        dialog = self.iface.getFeatureForm(layer, feature)
        dialog.setModal(True)

        message = None
        if dialog.exec_():
            self.rollback_changes = False
            message = QCoreApplication.translate(self.WIZARD_NAME, "Geoeconomic zone was created, but no changes have been saved.")
        else:
            self.rollback_changes = True
        self.close_wizard(message)

    def confirm_commit(self):
        layer = self.sender() # Get the layer that has sent the signal

        try:
            layer.featureAdded.disconnect()
            self.log.logMessage("Geoeconomic zone's featureAdded SIGNAL disconnected", PLUGIN_NAME, Qgis.Info)
        except:
            pass

        if not self.rollback_changes:
            saved = layer.commitChanges()

            if not saved:
                layer.rollBack()
                self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                                    QCoreApplication.translate(self.WIZARD_NAME,
                                                                               "Error while saving changes. Parcel could not be created."),
                                                    Qgis.Warning)

                for e in layer.commitErrors():
                    self.log.logMessage("Commit error: {}".format(e), PLUGIN_NAME, Qgis.Warning)
        else:
            layer.rollBack()
            self.form_rejected()

        self.iface.mapCanvas().refresh()
        self.added_features = None

    def form_rejected(self):
        message = QCoreApplication.translate(self.WIZARD_NAME,
                                             "'{}' tool has been closed because you just closed the form.").format(self.WIZARD_TOOL_NAME)
        self.close_wizard(message)

    def save_settings(self):
        settings = QSettings()
        settings.setValue('Asistente-LADM_COL/wizards/geoeconomic_zone_valuation_load_data_type', 'digitizing' if self.rad_digitizing.isChecked() else 'refactor')

    def restore_settings(self):
        settings = QSettings()

        load_data_type = settings.value('Asistente-LADM_COL/wizards/geoeconomic_zone_valuation_load_data_type') or 'digitizing'
        if load_data_type == 'refactor':
            self.rad_refactor.setChecked(True)
        else:
            self.rad_digitizing.setChecked(True)

    def show_help(self):
        self.qgis_utils.show_help("create_geoeconomic_zone_valuation")
