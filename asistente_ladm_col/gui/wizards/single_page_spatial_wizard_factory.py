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
from qgis.PyQt.QtCore import (QCoreApplication,
                              pyqtSignal)
from qgis.PyQt.QtWidgets import QWizard
from qgis.core import QgsMapLayerProxyModel

from asistente_ladm_col.config.general_config import (WIZARD_HELP_PAGES,
                                                      WIZARD_HELP1,
                                                      WIZARD_MAP_LAYER_PROXY_MODEL)
from asistente_ladm_col.gui.wizards.spatial_wizard_factory import SpatialWizardFactory


class SinglePageSpatialWizardFactory(SpatialWizardFactory):
    update_wizard_is_open_flag = pyqtSignal(bool)
    set_finalize_geometry_creation_enabled_emitted = pyqtSignal(bool)

    def __init__(self, iface, db, wizard_settings):
        super(SinglePageSpatialWizardFactory, self).__init__(iface, db, wizard_settings)

    def init_gui(self):
        self.mMapLayerComboBox.setFilters(QgsMapLayerProxyModel.Filter(self.wizard_config[WIZARD_MAP_LAYER_PROXY_MODEL]))
        self.mMapLayerComboBox.layerChanged.connect(self.import_layer_changed)

        self.restore_settings()
        self.rad_create_manually.toggled.connect(self.adjust_page_1_controls)
        self.adjust_page_1_controls()

        self.button(QWizard.FinishButton).clicked.connect(self.finished_dialog)
        self.button(QWizard.HelpButton).clicked.connect(self.show_help)
        self.rejected.connect(self.close_wizard)

    def adjust_page_1_controls(self):
        self.cbo_mapping.clear()
        self.cbo_mapping.addItem("")
        self.cbo_mapping.addItems(self.app.core.get_field_mappings_file_names(self.EDITING_LAYER_NAME))

        if self.rad_refactor.isChecked():
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
            self.lbl_field_mapping.setEnabled(False)
            self.cbo_mapping.setEnabled(False)
            self.lbl_refactor_source.setStyleSheet('')
            finish_button_text = QCoreApplication.translate("WizardTranslations", "Create")
            self.txt_help_page_1.setHtml(self.wizard_config[WIZARD_HELP_PAGES][WIZARD_HELP1])

        self.wizardPage1.setButtonText(QWizard.FinishButton, finish_button_text)

    def post_save(self, features):
        message = QCoreApplication.translate("WizardTranslations",
                                             "'{}' tool has been closed because an error occurred while trying to save the data.").format(self.WIZARD_TOOL_NAME)
        fid = features[0].id()

        if not self._layers[self.EDITING_LAYER_NAME].getFeature(fid).isValid():
            message = QCoreApplication.translate("WizardTranslations",
                                                 "'{}' tool has been closed. Feature not found in layer {}... It's not posible create it.").format(self.WIZARD_TOOL_NAME, self.EDITING_LAYER_NAME)
            self.logger.warning(__name__, "Feature not found in layer {} ...".format(self.EDITING_LAYER_NAME))
        else:
            feature_tid = self._layers[self.EDITING_LAYER_NAME].getFeature(fid)[self.names.T_ID_F]
            message = QCoreApplication.translate("WizardTranslations",
                                                 "The new {} (t_id={}) was successfully created!").format(self.WIZARD_FEATURE_NAME, feature_tid)
        return message

    def exec_form_advanced(self, layer):
        pass
