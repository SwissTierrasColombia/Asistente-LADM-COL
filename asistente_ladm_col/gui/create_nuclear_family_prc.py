# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2018-09-06
        git sha              : :%H$
        copyright            : (C) 2018 by Germán Carrillo
        email                : gcarrillo@linuxmail.com
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
from qgis.PyQt.QtWidgets import QWizard
from qgis.core import (QgsEditFormConfig,
                       Qgis,
                       QgsMapLayerProxyModel)

from ..config.help_strings import HelpStrings
from ..config.table_mapping_config import NUCLEAR_FAMILY_TABLE
from ..utils import get_ui_class

WIZARD_UI = get_ui_class('wiz_create_nuclear_family_prc.ui')

class CreateNuclearFamilyPRCWizard(QWizard, WIZARD_UI):
    def __init__(self, iface, db, qgis_utils, parent=None):
        QWizard.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self._nuclear_family_table = None
        self._db = db
        self.qgis_utils = qgis_utils
        self.help_strings = HelpStrings()

        self.restore_settings()

        self.rad_create_manually.toggled.connect(self.adjust_page_1_controls)
        self.adjust_page_1_controls()
        self.button(QWizard.FinishButton).clicked.connect(self.finished_dialog)
        self.button(QWizard.HelpButton).clicked.connect(self.show_help)

        self.mMapLayerComboBox.setFilters(QgsMapLayerProxyModel.NoGeometry)

    def adjust_page_1_controls(self):
        self.cbo_mapping.clear()
        self.cbo_mapping.addItem("")
        self.cbo_mapping.addItems(self.qgis_utils.get_field_mappings_file_names(NUCLEAR_FAMILY_TABLE))

        if self.rad_refactor.isChecked():
            self.lbl_refactor_source.setEnabled(True)
            self.mMapLayerComboBox.setEnabled(True)
            finish_button_text = QCoreApplication.translate("CreateNuclearFamilyWizard", "Import")
            self.txt_help_page_1.setHtml(self.help_strings.get_refactor_help_string(NUCLEAR_FAMILY_TABLE, False))
            self.lbl_field_mapping.setEnabled(True)
            self.cbo_mapping.setEnabled(True)

        elif self.rad_create_manually.isChecked():
            self.lbl_refactor_source.setEnabled(False)
            self.mMapLayerComboBox.setEnabled(False)
            finish_button_text = QCoreApplication.translate("CreateNuclearFamilyWizard", "Create")
            self.txt_help_page_1.setHtml(self.help_strings.WIZ_CREATE_NUCLEAR_FAMILY_PRC_PAGE_1_OPTION_FORM)
            self.lbl_field_mapping.setEnabled(False)
            self.cbo_mapping.setEnabled(False)

        self.wizardPage1.setButtonText(QWizard.FinishButton,
                                       QCoreApplication.translate("CreateNuclearFamilyWizard",
                                       finish_button_text))

    def finished_dialog(self):
        self.save_settings()

        if self.rad_refactor.isChecked():
            if self.mMapLayerComboBox.currentLayer() is not None:
                field_mapping = self.cbo_mapping.currentText()
                res_etl_model = self.qgis_utils.show_etl_model(self._db,
                                                               self.mMapLayerComboBox.currentLayer(),
                                                               NUCLEAR_FAMILY_TABLE,
                                                               field_mapping=field_mapping)

                if res_etl_model:
                    if field_mapping:
                        self.qgis_utils.delete_old_field_mapping(field_mapping)

                    self.qgis_utils.save_field_mapping(NUCLEAR_FAMILY_TABLE)

            else:
                self.iface.messageBar().pushMessage("Asistente LADM_COL",
                    QCoreApplication.translate("CreateNuclearFamilyWizard",
                                               "Select a source layer to set the field mapping to '{}'.").format(NUCLEAR_FAMILY_TABLE),
                    Qgis.Warning)

        elif self.rad_create_manually.isChecked():
            self.prepare_nuclear_family_creation()

    def prepare_nuclear_family_creation(self):
        # Load layers
        self._nuclear_family_table = self.qgis_utils.get_layer(self._db, NUCLEAR_FAMILY_TABLE, load=True)
        if self._nuclear_family_table is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                QCoreApplication.translate("CreateNuclearFamilyWizard",
                                           "Nuclear family table couldn't be found... {}").format(self._db.get_description()),
                Qgis.Warning)
            return

        # Don't suppress (i.e., show) feature form
        form_config = self._nuclear_family_table.editFormConfig()
        form_config.setSuppress(QgsEditFormConfig.SuppressOff)
        self._nuclear_family_table.setEditFormConfig(form_config)

        self.edit_nuclear_family()

    def edit_nuclear_family(self):
        # Open Form
        self.iface.layerTreeView().setCurrentLayer(self._nuclear_family_table)
        self._nuclear_family_table.startEditing()
        self.iface.actionAddFeature().trigger()

    def save_settings(self):
        settings = QSettings()
        settings.setValue('Asistente-LADM_COL/wizards/nuclear_family_load_data_type', 'create_manually' if self.rad_create_manually.isChecked() else 'refactor')

    def restore_settings(self):
        settings = QSettings()

        load_data_type = settings.value('Asistente-LADM_COL/wizards/nuclear_family_load_data_type') or 'create_manually'
        if load_data_type == 'refactor':
            self.rad_refactor.setChecked(True)
        else:
            self.rad_create_manually.setChecked(True)

    def show_help(self):
        self.qgis_utils.show_help("create_nuclear_family")
