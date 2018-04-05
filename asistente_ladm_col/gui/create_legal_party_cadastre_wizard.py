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
from qgis.core import (QgsEditFormConfig, QgsVectorLayerUtils, Qgis,
                       QgsWkbTypes, QgsMapLayerProxyModel)
from qgis.gui import QgsMessageBar
from qgis.PyQt.QtCore import Qt, QPoint, QCoreApplication, QSettings
from qgis.PyQt.QtWidgets import QAction, QWizard

from ..utils import get_ui_class
from ..config.table_mapping_config import (
    LEGAL_PARTY_TABLE,
    LEGAL_PARTY_TYPE_TABLE
)

from ..config.help_strings import (get_refactor_help_string,
                                   WIZ_CREATE_LEGAL_PARTY_CADASTRE_PAGE_1_OPTION_FORM)

WIZARD_UI = get_ui_class('wiz_create_legal_party_cadastre.ui')

class CreateLegalPartyCadastreWizard(QWizard, WIZARD_UI):
    def __init__(self, iface, db, qgis_utils, parent=None):
        QWizard.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self._legal_party_layer = None
        self._db = db
        self.qgis_utils = qgis_utils

        self.restore_settings()

        self.rad_create_manually.toggled.connect(self.adjust_page_1_controls)
        self.adjust_page_1_controls()
        self.button(QWizard.FinishButton).clicked.connect(self.finished_dialog)

        self.mMapLayerComboBox.setFilters(QgsMapLayerProxyModel.NoGeometry)

    def adjust_page_1_controls(self):
        if self.rad_refactor.isChecked():
            self.lbl_refactor_source.setEnabled(True)
            self.mMapLayerComboBox.setEnabled(True)
            finish_button_text = "Import"
            self.txt_help_page_1.setHtml(get_refactor_help_string(LEGAL_PARTY_TABLE, False))

        elif self.rad_create_manually.isChecked():
            self.lbl_refactor_source.setEnabled(False)
            self.mMapLayerComboBox.setEnabled(False)
            finish_button_text = "Create"
            self.txt_help_page_1.setHtml(WIZ_CREATE_LEGAL_PARTY_CADASTRE_PAGE_1_OPTION_FORM)

        self.wizardPage1.setButtonText(QWizard.FinishButton,
                                       QCoreApplication.translate("CreateLegalPartyCadastreWizard",
                                       finish_button_text))

    def finished_dialog(self):
        self.save_settings()

        if self.rad_refactor.isChecked():
            if self.mMapLayerComboBox.currentLayer() is not None:
                self.qgis_utils.show_etl_model(self._db,
                                               self.mMapLayerComboBox.currentLayer(),
                                               LEGAL_PARTY_TABLE)
            else:
                self.iface.messageBar().pushMessage("Asistente LADM_COL",
                    QCoreApplication.translate("CreateLegalPartyCadastreWizard",
                                               "Select a source layer to set the field mapping to '{}'.").format(LEGAL_PARTY_TABLE),
                    Qgis.Warning)

        elif self.rad_create_manually.isChecked():
            self.prepare_legal_party_creation()

    def prepare_legal_party_creation(self):
        # Load layers
        res_layers = self.qgis_utils.get_layers(self._db, {
            LEGAL_PARTY_TABLE: {'name': LEGAL_PARTY_TABLE, 'geometry': None},
            LEGAL_PARTY_TYPE_TABLE: {'name': LEGAL_PARTY_TYPE_TABLE, 'geometry': None}}, load=True)

        self._legal_party_layer = res_layers[LEGAL_PARTY_TABLE]
        if self._legal_party_layer is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                QCoreApplication.translate("CreateLegalPartyCadastreWizard",
                                           "Legal Party layer couldn't be found..."),
                Qgis.Warning)
            return

        # Configure automatic fields
        self.qgis_utils.set_automatic_fields(self._legal_party_layer, "p")

        # Don't suppress (i.e., show) feature form
        form_config = self._legal_party_layer.editFormConfig()
        form_config.setSuppress(QgsEditFormConfig.SuppressOff)
        self._legal_party_layer.setEditFormConfig(form_config)

        self.edit_legal_party()

    def edit_legal_party(self):
        # Open Form
        self.iface.layerTreeView().setCurrentLayer(self._legal_party_layer)
        self._legal_party_layer.startEditing()
        self.iface.actionAddFeature().trigger()

    def save_settings(self):
        settings = QSettings()
        settings.setValue('Asistente-LADM_COL/wizards/legal_party_load_data_type', 'create_manually' if self.rad_create_manually.isChecked() else 'refactor')

    def restore_settings(self):
        settings = QSettings()

        load_data_type = settings.value('Asistente-LADM_COL/wizards/legal_party_load_data_type') or 'create_manually'
        if load_data_type == 'refactor':
            self.rad_refactor.setChecked(True)
        else:
            self.rad_create_manually.setChecked(True)
