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
        email                : gcarrillo@linuxmail.com
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
from qgis.PyQt.QtCore import (QSettings,
                              QCoreApplication,
                              pyqtSignal)
from qgis.PyQt.QtWidgets import QWizard
from qgis.core import (QgsApplication,
                       Qgis)

from asistente_ladm_col.config.general_config import (PLUGIN_NAME,
                                                      TranslatableConfigStrings,
                                                      LAYER,
                                                      WIZARD_NAME,
                                                      WIZARD_FEATURE_NAME, WIZARD_UI,
                                                      WIZARD_EDITING_LAYER_NAME, WIZARD_LAYERS,
                                                      WIZARD_QSETTINGS_LOAD_DATA_TYPE, WIZARD_QSETTINGS,
                                                      WIZARD_HELP, WIZARD_READ_ONLY_FIELDS, WIZARD_TOOL_NAME)
from asistente_ladm_col.config.help_strings import HelpStrings
from asistente_ladm_col.utils.qgis_utils import QGISUtils
from asistente_ladm_col.utils.ui import load_ui


class AbsWizardFactory(QWizard):
    set_wizard_is_open_emitted = pyqtSignal(bool)
    set_finalize_geometry_creation_enabled_emitted = pyqtSignal(bool)

    def __init__(self, iface, db, qgis_utils, wizard_settings):
        super(AbsWizardFactory, self).__init__()
        self.iface = iface
        self.log = QgsApplication.messageLog()
        self._db = db
        self.qgis_utils = qgis_utils
        self.wizard_config = wizard_settings
        self.help_strings = HelpStrings()
        self.translatable_config_strings = TranslatableConfigStrings()

        load_ui(self.wizard_config[WIZARD_UI], self)

        self.WIZARD_NAME = self.wizard_config[WIZARD_NAME]
        self.WIZARD_FEATURE_NAME = self.wizard_config[WIZARD_FEATURE_NAME]
        self.WIZARD_TOOL_NAME = self.wizard_config[WIZARD_TOOL_NAME]
        self.EDITING_LAYER_NAME = self.wizard_config[WIZARD_EDITING_LAYER_NAME]
        self._layers = self.wizard_config[WIZARD_LAYERS]
        self.set_ready_only_field()

        self.init_gui()

    def init_gui(self):
        raise NotImplementedError

    def adjust_page_1_controls(self):
        raise NotImplementedError

    def finished_dialog(self):
        raise NotImplementedError

    def prepare_feature_creation(self):
        result = self.prepare_feature_creation_layers()
        if result:
            self.edit_feature()
        else:
            self.close_wizard(show_message=False)

    def prepare_feature_creation_layers(self):
        raise NotImplementedError

    def close_wizard(self, message=None, show_message=True):
        raise NotImplementedError

    def rollback_in_layers_with_empty_editing_session(self):
        for layer_name in self._layers:
            try:
                if self._layers[layer_name][LAYER]:
                    if self._layers[layer_name][LAYER].isEditable():
                        if not self._layers[layer_name][LAYER].editBuffer().addedFeatures():
                            self._layers[layer_name][LAYER].rollBack()
            except RuntimeError:
                pass # Layer was removed

    def disconnect_signals(self):
        raise NotImplementedError

    def edit_feature(self):
        raise NotImplementedError

    def finish_feature_creation(self, layerId, features):
        message = self.post_save(features)

        self._layers[self.EDITING_LAYER_NAME][LAYER].committedFeaturesAdded.disconnect(self.finish_feature_creation)
        self.log.logMessage("{} committedFeaturesAdded SIGNAL disconnected".format(self.WIZARD_FEATURE_NAME), PLUGIN_NAME, Qgis.Info)
        self.close_wizard(message)

    def post_save(self, features):
        raise NotImplementedError

    def open_form(self, layer):
        raise NotImplementedError

    def exec_form(self, layer):
        feature = self.get_feature_exec_form(layer)
        dialog = self.iface.getFeatureForm(layer, feature)
        dialog.rejected.connect(self.form_rejected)
        dialog.setModal(True)

        if dialog.exec_():
            self.exec_form_advanced(layer)
            saved = layer.commitChanges()

            if not saved:
                layer.rollBack()
                self.qgis_utils.message_emitted.emit(
                    QCoreApplication.translate(self.WIZARD_NAME,
                                               "Error while saving changes. {} could not be created.").format(self.WIZARD_FEATURE_NAME), Qgis.Warning)
                for e in layer.commitErrors():
                    self.log.logMessage("Commit error: {}".format(e), PLUGIN_NAME, Qgis.Warning)
        else:
            layer.rollBack()
        self.iface.mapCanvas().refresh()

    def get_feature_exec_form(self, layer):
        raise NotImplementedError

    def exec_form_advanced(self, layer):
        raise NotImplementedError

    def form_rejected(self):
        message = QCoreApplication.translate(self.WIZARD_NAME,
                                             "'{}' tool has been closed because you just closed the form.").format(self.WIZARD_TOOL_NAME)
        self.close_wizard(message)

    def save_settings(self):
        settings = QSettings()
        settings.setValue(self.wizard_config[WIZARD_QSETTINGS][WIZARD_QSETTINGS_LOAD_DATA_TYPE], 'create_manually' if self.rad_create_manually.isChecked() else 'refactor')

    def restore_settings(self):
        settings = QSettings()

        load_data_type = settings.value(self.wizard_config[WIZARD_QSETTINGS][WIZARD_QSETTINGS_LOAD_DATA_TYPE]) or 'create_manually'
        if load_data_type == 'refactor':
            self.rad_refactor.setChecked(True)
        else:
            self.rad_create_manually.setChecked(True)

    def show_help(self):
        self.qgis_utils.show_help(self.wizard_config[WIZARD_HELP])

    def set_ready_only_field(self, read_only=True):
        if self._layers[self.EDITING_LAYER_NAME][LAYER] is not None:
            for field in self.wizard_config[WIZARD_READ_ONLY_FIELDS]:
                # Not validate field that are read only
                QGISUtils.set_read_only_field(self._layers[self.EDITING_LAYER_NAME][LAYER], field, read_only)
