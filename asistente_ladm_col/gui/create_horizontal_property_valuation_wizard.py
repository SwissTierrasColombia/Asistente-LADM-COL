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
from qgis.PyQt.QtCore import (QCoreApplication,
                              QSettings)
from qgis.PyQt.QtWidgets import QWizard
from qgis.core import (QgsEditFormConfig,
                       Qgis,
                       QgsMapLayerProxyModel)

from ..config.help_strings import HelpStrings
from ..config.table_mapping_config import VALUATION_HORIZONTAL_PROPERTY_TABLE
from ..utils import get_ui_class

WIZARD_UI = get_ui_class('wiz_create_horizontal_property_valuation.ui')

class CreateHorizontalPropertyValuationWizard(QWizard, WIZARD_UI):
    def __init__(self, iface, db, qgis_utils, parent=None):
        QWizard.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self._horizontal_property_valuation = None
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
        if self.rad_refactor.isChecked():
            self.lbl_refactor_source.setEnabled(True)
            self.mMapLayerComboBox.setEnabled(True)
            finish_button_text = QCoreApplication.translate("CreateHorizontalPropertyValuationWizard", "Import")
            self.txt_help_page_1.setHtml(self.help_strings.get_refactor_help_string(VALUATION_HORIZONTAL_PROPERTY_TABLE, False))

        elif self.rad_create_manually.isChecked():
            self.lbl_refactor_source.setEnabled(False)
            self.mMapLayerComboBox.setEnabled(False)
            finish_button_text = QCoreApplication.translate("CreateHorizontalPropertyValuationWizard", "Create")
            self.txt_help_page_1.setHtml(self.help_strings.WIZ_CREATE_HORIZONTAL_PROPERTY_VALUATION_PAGE_1_OPTION_FORM)

        self.wizardPage1.setButtonText(QWizard.FinishButton,
                                       QCoreApplication.translate("CreateHorizontalPropertyValuationWizard",
                                       finish_button_text))

    def finished_dialog(self):
        self.save_settings()

        if self.rad_refactor.isChecked():
            if self.mMapLayerComboBox.currentLayer() is not None:
                self.qgis_utils.show_etl_model(self._db,
                                               self.mMapLayerComboBox.currentLayer(),
                                               VALUATION_HORIZONTAL_PROPERTY_TABLE)
            else:
                self.iface.messageBar().pushMessage("Asistente LADM_COL",
                    QCoreApplication.translate("CreateHorizontalPropertyValuationWizard",
                                               "Horizontal property valuation table couldn't be found... {}").format(
                        self._db.get_description()),
                    Qgis.Warning)

        elif self.rad_create_manually.isChecked():
            self.prepare_horizontal_property_valuation_creation()

    def prepare_horizontal_property_valuation_creation(self):
        # Load layers
        self._horizontal_property_valuation = self.qgis_utils.get_layer(self._db, VALUATION_HORIZONTAL_PROPERTY_TABLE, load=True)
        if self._horizontal_property_valuation is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                QCoreApplication.translate("CreateLegalPartyWizard",
                                           "Legal party table couldn't be found... {}").format(self._db.get_description()),
                Qgis.Warning)
            return

        # Don't suppress (i.e., show) feature form
        form_config = self._horizontal_property_valuation.editFormConfig()
        form_config.setSuppress(QgsEditFormConfig.SuppressOff)
        self._horizontal_property_valuation.setEditFormConfig(form_config)

        self.edit_horizontal_property_valuation()

    def edit_horizontal_property_valuation(self):
        # Open Form
        self.iface.layerTreeView().setCurrentLayer(self._horizontal_property_valuation)
        self._horizontal_property_valuation.startEditing()
        self.iface.actionAddFeature().trigger()

    def save_settings(self):
        settings = QSettings()
        settings.setValue('Asistente-LADM_COL/wizards/valuation_horizontal_property_load_data_type', 'create_manually' if self.rad_create_manually.isChecked() else 'refactor')

    def restore_settings(self):
        settings = QSettings()

        load_data_type = settings.value('Asistente-LADM_COL/wizards/valuation_horizontal_property_load_data_type') or 'create_manually'
        if load_data_type == 'refactor':
            self.rad_refactor.setChecked(True)
        else:
            self.rad_create_manually.setChecked(True)

    def show_help(self):
        self.qgis_utils.show_help("create_horizontal_property_valuation")