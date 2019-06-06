# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2017-11-14
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
                              QSettings)
from qgis.PyQt.QtWidgets import QWizard
from qgis.core import (QgsProject,
                       Qgis,
                       QgsApplication,
                       QgsMapLayerProxyModel,
                       QgsWkbTypes)

from .....config.general_config import PLUGIN_NAME
from .....config.help_strings import HelpStrings
from .....config.table_mapping_config import (BOUNDARY_TABLE,
                                              ID_FIELD,
                                              BOUNDARY_POINT_TABLE)
from .....utils import get_ui_class

WIZARD_UI = get_ui_class('wiz_create_boundaries_cadastre.ui')


class CreateBoundariesCadastreWizard(QWizard, WIZARD_UI):
    WIZARD_CREATES_SPATIAL_FEATURE = True
    WIZARD_NAME = "CreateBoundariesCadastreWizard"
    WIZARD_TOOL_NAME = QCoreApplication.translate(WIZARD_NAME, "Create boundary")

    def __init__(self, iface, db, qgis_utils, parent=None):
        QWizard.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self.log = QgsApplication.messageLog()
        self._db = db
        self.qgis_utils = qgis_utils
        self.help_strings = HelpStrings()

        self._layers = {
            BOUNDARY_TABLE: {'name': BOUNDARY_TABLE, 'geometry': QgsWkbTypes.LineGeometry, 'layer': None},
            BOUNDARY_POINT_TABLE: {'name': BOUNDARY_POINT_TABLE, 'geometry': QgsWkbTypes.PointGeometry, 'layer': None}
        }

        self.restore_settings()
        self.rad_digitizing.toggled.connect(self.adjust_page_1_controls)
        self.adjust_page_1_controls()

        self.button(QWizard.FinishButton).clicked.connect(self.finished_dialog)
        self.button(QWizard.HelpButton).clicked.connect(self.show_help)
        self.rejected.connect(self.close_wizard)
        self.mMapLayerComboBox.setFilters(QgsMapLayerProxyModel.LineLayer)

    def adjust_page_1_controls(self):
        self.cbo_mapping.clear()
        self.cbo_mapping.addItem("")
        self.cbo_mapping.addItems(self.qgis_utils.get_field_mappings_file_names(BOUNDARY_TABLE))

        if self.rad_refactor.isChecked():
            self.lbl_refactor_source.setEnabled(True)
            self.mMapLayerComboBox.setEnabled(True)
            self.lbl_field_mapping.setEnabled(True)
            self.cbo_mapping.setEnabled(True)
            finish_button_text = QCoreApplication.translate(self.WIZARD_NAME, "Import")
            self.txt_help_page_1.setHtml(self.help_strings.get_refactor_help_string(BOUNDARY_TABLE, False))

        elif self.rad_digitizing.isChecked():
            self.lbl_refactor_source.setEnabled(False)
            self.mMapLayerComboBox.setEnabled(False)
            self.lbl_field_mapping.setEnabled(False)
            self.cbo_mapping.setEnabled(False)
            finish_button_text = QCoreApplication.translate(self.WIZARD_NAME, "Start")
            self.txt_help_page_1.setHtml(self.help_strings.WIZ_DEFINE_BOUNDARIES_CADASTRE_PAGE_1_OPTION_DIGITIZE)

        self.wizardPage1.setButtonText(QWizard.FinishButton,
                                       QCoreApplication.translate(self.WIZARD_NAME,
                                       finish_button_text))

    def disconnect_signals(self):
        # QGIS APP
        try:
            self._layers[BOUNDARY_TABLE]['layer'].featureAdded.disconnect()
        except:
            pass

        try:
            self._layers[BOUNDARY_TABLE]['layer'].committedFeaturesAdded.disconnect(self.finish_feature_creation)
        except:
            pass

        layers = [self._layers[BOUNDARY_TABLE]['layer'],
                  self._layers[BOUNDARY_POINT_TABLE]['layer']]

        for layer in layers:
            try:
                layer.willBeDeleted.disconnect(self.layer_removed)
            except:
                pass

    def finished_dialog(self):
        self.save_settings()

        if self.rad_refactor.isChecked():
            if self.mMapLayerComboBox.currentLayer() is not None:
                field_mapping = self.cbo_mapping.currentText()
                res_etl_model = self.qgis_utils.show_etl_model(self._db,
                                                               self.mMapLayerComboBox.currentLayer(),
                                                               BOUNDARY_TABLE,
                                                               field_mapping=field_mapping)

                if res_etl_model:
                    # If the result of the etl_model is successful and we used a stored recent mapping, we delete the
                    # previous mapping used (we give preference to the latest used mapping)
                    if field_mapping:
                        self.qgis_utils.delete_old_field_mapping(field_mapping)

                    self.qgis_utils.save_field_mapping(BOUNDARY_TABLE)
            else:
                self.iface.messageBar().pushMessage("Asistente LADM_COL",
                    QCoreApplication.translate(self.WIZARD_NAME,
                                               "Select a source layer to set the field mapping to '{}'.").format(BOUNDARY_TABLE),
                    Qgis.Warning)

        elif self.rad_digitizing.isChecked():
            self.prepare_feature_creation()

    def prepare_feature_creation(self):
        # layers of interest are loaded
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
            if self._layers[layer_name]['layer']:
                # Layer was found, listen to its removal so that we can update the variable properly
                try:
                    self._layers[layer_name]['layer'].willBeDeleted.disconnect(self.layer_removed)
                except:
                    pass
                self._layers[layer_name]['layer'].willBeDeleted.connect(self.layer_removed)

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
        self.iface.layerTreeView().setCurrentLayer(self._layers[BOUNDARY_TABLE]['layer'])
        self._layers[BOUNDARY_TABLE]['layer'].committedFeaturesAdded.connect(self.finish_feature_creation)

        # Disable transactions groups
        QgsProject.instance().setAutoTransaction(False)

        # Activate snapping
        self.qgis_utils.active_snapping_layers([self._layers[BOUNDARY_POINT_TABLE]['layer'],
                                                self._layers[BOUNDARY_TABLE]['layer']])
        self.open_form(self._layers[BOUNDARY_TABLE]['layer'])

    def finish_feature_creation(self, layerId, features):
        message = QCoreApplication.translate(self.WIZARD_NAME,
                                             "'{}' tool has been closed because an error occurred while trying to save the data.").format(self.WIZARD_TOOL_NAME)
        fid = features[0].id()

        if not self._layers[BOUNDARY_TABLE]['layer'].getFeature(fid).isValid():
            message = QCoreApplication.translate(self.WIZARD_NAME,
                                                 "'{}' tool has been closed. Feature not found in layer {}... It's not posible create a boundary. ").format(self.WIZARD_TOOL_NAME, BOUNDARY_TABLE)
            self.log.logMessage("Feature not found in layer {} ...".format(BOUNDARY_TABLE), PLUGIN_NAME, Qgis.Warning)
        else:
            feature_tid = self._layers[BOUNDARY_TABLE]['layer'].getFeature(fid)[ID_FIELD]
            message = QCoreApplication.translate(self.WIZARD_NAME, "The new boundary (t_id={}) was successfully created ").format(feature_tid)

        self._layers[BOUNDARY_TABLE]['layer'].committedFeaturesAdded.disconnect(self.finish_feature_creation)
        self.log.logMessage("Boundary's committedFeaturesAdded SIGNAL disconnected", PLUGIN_NAME, Qgis.Info)
        self.close_wizard(message)

    def open_form(self, layer):
        if not layer.isEditable():
            layer.startEditing()

        if self.WIZARD_CREATES_SPATIAL_FEATURE:
            # action add feature
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

        feature = self.qgis_utils.get_new_feature(layer)
        dialog = self.iface.getFeatureForm(layer, feature)
        dialog.rejected.connect(self.form_rejected)
        dialog.setModal(True)

        if dialog.exec_():
            saved = layer.commitChanges()

            if not saved:
                layer.rollBack()
                self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                                    QCoreApplication.translate(self.WIZARD_NAME,
                                                                               "Error while saving changes. Parcel could not be created."),
                                                    Qgis.Warning)

                for e in layer.commitErrors():
                    self.log.logMessage("Commit error: {}".format(e), PLUGIN_NAME, Qgis.Warning)

            self.iface.mapCanvas().refresh()
        else:
            # TODO: implement when the bug is removed
            # When feature form is cancel QGIS close sudenlly
            # self.iface.actionRollbackEdits().trigger()
            # layer.rollBack(True)
            pass

    def form_rejected(self):
        message = QCoreApplication.translate(self.WIZARD_NAME,
                                             "'{}' tool has been closed because you just closed the form.").format(self.WIZARD_TOOL_NAME)
        self.close_wizard(message)

    def save_settings(self):
        settings = QSettings()
        settings.setValue('Asistente-LADM_COL/wizards/boundary_load_data_type', 'digitizing' if self.rad_digitizing.isChecked() else 'refactor')

    def restore_settings(self):
        settings = QSettings()

        load_data_type = settings.value('Asistente-LADM_COL/wizards/boundary_load_data_type') or 'digitizing'
        if load_data_type == 'refactor':
            self.rad_refactor.setChecked(True)
        else:
            self.rad_digitizing.setChecked(True)

    def show_help(self):
        self.qgis_utils.show_help("create_boundaries")
