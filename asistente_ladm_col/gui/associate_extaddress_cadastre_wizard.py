# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 15/01/19
        git sha              : :%H$
        copyright            : (C) 2019 by Sergio Ramírez (Incige SAS)
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
from qgis.core import (QgsProject, QgsVectorLayer, QgsEditFormConfig,
                       QgsSnappingConfig, QgsTolerance, QgsFeature, Qgis,
                       QgsMapLayerProxyModel, QgsWkbTypes, QgsApplication,
                       QgsProcessingException, QgsProcessingFeedback,
                       QgsVectorLayerUtils)

from qgis.PyQt.QtCore import Qt, QPoint, QCoreApplication, QSettings
from qgis.PyQt.QtWidgets import QAction, QWizard

import processing
from ..utils import get_ui_class
from ..config.table_mapping_config import EXTADDRESS_TABLE
from ..config.general_config import (
    DEFAULT_EPSG,
    PLUGIN_NAME,
    TranslatableConfigStrings
)
from ..config.help_strings import HelpStrings
from .right_of_way import RightOfWay

WIZARD_UI = get_ui_class('wiz_associate_ext_address_cadastre.ui')

class AssociateExtAddressWizard(QWizard, WIZARD_UI):

    def __init__(self, iface, db, qgis_utils, parent=None):
        QWizard.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self.log = QgsApplication.messageLog()
        self._db = db
        self.qgis_utils = qgis_utils
        self.help_strings = HelpStrings()
        self.translatable_config_strings = TranslatableConfigStrings()

        self.restore_settings()

        self.rad_to_plot.toggled.connect(self.adjust_page_1_controls)
        self.rad_to_building.toggled.connect(self.adjust_page_1_controls)
        self.rad_to_building_unit.toggled.connect(self.adjust_page_1_controls)
        self.adjust_page_1_controls()
        self.button(QWizard.FinishButton).clicked.connect(self.finished_dialog)
        self.button(QWizard.HelpButton).clicked.connect(self.show_help)

        self.mMapLayerComboBox.setFilters(QgsMapLayerProxyModel.PolygonLayer)

    def adjust_page_1_controls(self):
        self.cbo_mapping.clear()
        self.cbo_mapping.addItem("")
        self.cbo_mapping.addItems(self.qgis_utils.get_field_mappings_file_names(EXTADDRESS_TABLE))

        if self.rad_refactor.isChecked():
            self.lbl_refactor_source.setEnabled(True)
            self.mMapLayerComboBox.setEnabled(True)
            self.lbl_field_mapping.setEnabled(True)
            self.cbo_mapping.setEnabled(True)
            finish_button_text = QCoreApplication.translate("AssociateExtAddressWizard", "Import")
            self.txt_help_page_1.setHtml(self.help_strings.get_refactor_help_string(EXTADDRESS_TABLE, True))

        elif self.rad_to_plot.isChecked():
            self.lbl_refactor_source.setEnabled(False)
            self.mMapLayerComboBox.setEnabled(False)
            self.lbl_field_mapping.setEnabled(False)
            self.cbo_mapping.setEnabled(False)
            finish_button_text = QCoreApplication.translate("AssociateExtAddressWizard", "Select Plot")
            self.txt_help_page_1.setHtml(self.help_strings.WIZ_ASSOCIATE_EXTADDRESS_CADASTRE_PAGE_1_OPTION_POINTS)

        elif self.rad_to_building.isChecked():
            self.lbl_refactor_source.setEnabled(False)
            self.mMapLayerComboBox.setEnabled(False)
            self.lbl_field_mapping.setEnabled(False)
            self.cbo_mapping.setEnabled(False)
            finish_button_text = QCoreApplication.translate("AssociateExtAddressWizard", "Select Building")
            self.txt_help_page_1.setHtml(self.help_strings.WIZ_ASSOCIATE_EXTADDRESS_CADASTRE_PAGE_1_OPTION2_POINTS)

        elif self.rad_to_building_unit.isChecked():
            self.lbl_refactor_source.setEnabled(False)
            self.mMapLayerComboBox.setEnabled(False)
            self.lbl_field_mapping.setEnabled(False)
            self.cbo_mapping.setEnabled(False)
            finish_button_text = QCoreApplication.translate("AssociateExtAddressWizard", "Select Building Unit")
            self.txt_help_page_1.setHtml(self.help_strings.WIZ_ASSOCIATE_EXTADDRESS_CADASTRE_PAGE_1_OPTION3_POINTS)

        self.wizardPage1.setButtonText(QWizard.FinishButton,
                                       QCoreApplication.translate('AssociateExtAddressWizard',
                                       finish_button_text))

    def finished_dialog(self):
        self.save_settings()

        if self.rad_refactor.isChecked():
            if self.mMapLayerComboBox.currentLayer() is not None:
                field_mapping = self.cbo_mapping.currentText()
                res_etl_model = self.qgis_utils.show_etl_model(self._db,
                                               self.mMapLayerComboBox.currentLayer(),
                                               EXTADDRESS_TABLE,
                                               field_mapping=field_mapping)

                if res_etl_model:
                    if field_mapping:
                        self.qgis_utils.delete_old_field_mapping(field_mapping)

                    self.qgis_utils.save_field_mapping(EXTADDRESS_TABLE)

            else:
                self.iface.messageBar().pushMessage('Asistente LADM_COL',
                    QCoreApplication.translate("AssociateExtAddressWizard",
                                               "Select a source layer to set the field mapping to '{}'.").format(EXTADDRESS_TABLE),
                    Qgis.Warning)

        elif self.rad_to_plot.isChecked():
            pass
        elif self.rad_to_building.isChecked():
            pass
        elif self.rad_to_building_unit.isChecked():
            pass

    def save_settings(self):
        settings = QSettings()

        load_data_type = 'refactor'
        if self.rad_to_plot.isChecked():
            load_data_type = 'to_plot'
        elif self.rad_to_building.isChecked():
            load_data_type = 'to_building'
        elif self.rad_to_building_unit.isChecked():
            load_data_type = 'to_building_unit'

        settings.setValue('Asistente-LADM_COL/wizards/ext_address_load_data_type', load_data_type)

    def restore_settings(self):
        settings = QSettings()

        load_data_type = settings.value('Asistente-LADM_COL/wizards/ext_address_load_data_type') or 'to_plot'
        if load_data_type == 'refactor':
            self.rad_refactor.setChecked(True)
        elif load_data_type == 'to_plot':
            self.rad_to_plot.setChecked(True)
        elif load_data_type == 'to_building':
            self.rad_to_building.setChecked(True)
        else:
            self.rad_to_building_unit.setChecked(True)

    def show_help(self):
        self.qgis_utils.show_help("associate_ext_address")
