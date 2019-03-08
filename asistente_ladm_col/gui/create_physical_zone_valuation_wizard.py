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
from qgis.core import (QgsProject,
                       QgsEditFormConfig,
                       QgsSnappingConfig,
                       QgsTolerance,
                       Qgis,
                       QgsMapLayerProxyModel,
                       QgsWkbTypes)

from ..config.help_strings import HelpStrings
from ..config.table_mapping_config import VALUATION_PHYSICAL_ZONE_TABLE
from ..utils import get_ui_class

WIZARD_UI = get_ui_class('wiz_create_physical_zone_valuation.ui')


class CreatePhysicalZoneValuationWizard(QWizard, WIZARD_UI):
    def __init__(self, iface, db, qgis_utils, parent=None):
        QWizard.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self._physical_zone_valuation = None
        self._db = db
        self.qgis_utils = qgis_utils
        self.help_strings = HelpStrings()

        self.restore_settings()

        self.rad_digitizing.toggled.connect(self.adjust_page_1_controls)
        self.adjust_page_1_controls()
        self.button(QWizard.FinishButton).clicked.connect(self.finished_dialog)
        self.button(QWizard.HelpButton).clicked.connect(self.show_help)

        self.mMapLayerComboBox.setFilters(QgsMapLayerProxyModel.PolygonLayer)

    def adjust_page_1_controls(self):
        self.cbo_mapping.clear()
        self.cbo_mapping.addItem("")
        self.cbo_mapping.addItems(self.qgis_utils.get_field_mappings_file_names(VALUATION_PHYSICAL_ZONE_TABLE))

        if self.rad_refactor.isChecked():
            self.lbl_refactor_source.setEnabled(True)
            self.mMapLayerComboBox.setEnabled(True)
            self.lbl_field_mapping.setEnabled(True)
            self.cbo_mapping.setEnabled(True)
            finish_button_text = 'Import'
            self.txt_help_page_1.setHtml(self.help_strings.get_refactor_help_string(VALUATION_PHYSICAL_ZONE_TABLE, True))

        elif self.rad_digitizing.isChecked():
            self.lbl_refactor_source.setEnabled(False)
            self.mMapLayerComboBox.setEnabled(False)
            self.lbl_field_mapping.setEnabled(False)
            self.cbo_mapping.setEnabled(False)
            finish_button_text = QCoreApplication.translate("CreatePhysicalZoneValuationWizard", "Start")
            self.txt_help_page_1.setHtml(self.help_strings.WIZ_CREATE_PHYSICAL_ZONE_VALUATION_PAGE_1_OPTION_FORM)

        self.wizardPage1.setButtonText(QWizard.FinishButton,
                                       QCoreApplication.translate("CreatePhysicalZoneValuationWizard",
                                       finish_button_text))

    def finished_dialog(self):
        self.save_settings()

        if self.rad_refactor.isChecked():
            if self.mMapLayerComboBox.currentLayer() is not None:
                field_mapping = self.cbo_mapping.currentText()
                res_etl_model = self.qgis_utils.show_etl_model(self._db,
                                                               self.mMapLayerComboBox.currentLayer(),
                                                               VALUATION_PHYSICAL_ZONE_TABLE,
                                                               QgsWkbTypes.PolygonGeometry,
                                                               field_mapping)

                if res_etl_model:
                    if field_mapping:
                        self.qgis_utils.delete_old_field_mapping(field_mapping)

                    self.qgis_utils.save_field_mapping(VALUATION_PHYSICAL_ZONE_TABLE)
            else:
                self.iface.messageBar().pushMessage('Asistente LADM_COL',
                    QCoreApplication.translate("CreatePhysicalZoneValuationWizard",
                                               "Select a source layer to set the field mapping to '{}'.").format(VALUATION_PHYSICAL_ZONE_TABLE),
                    Qgis.Warning)

        elif self.rad_digitizing.isChecked():
            self.prepare_building_unit_creation()

    def prepare_building_unit_creation(self):
        # Load layers
        res_layers = self.qgis_utils.get_layers(self._db, {
            VALUATION_PHYSICAL_ZONE_TABLE: {'name': VALUATION_PHYSICAL_ZONE_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry}
        }, load=True)

        self._physical_zone_valuation = res_layers[VALUATION_PHYSICAL_ZONE_TABLE]

        if self._physical_zone_valuation is None:
            self.iface.messageBar().pushMessage('Asistente LADM_COL',
                QCoreApplication.translate("CreatePhysicalZoneValuationWizard",
                                           "Physical zone valuation layer couldn't be found... {}").format(self._db.get_description()),
                Qgis.Warning)
            return

        # Disable transactions groups
        QgsProject.instance().setAutoTransaction(False)

        # Configure Snapping
        snapping = QgsProject.instance().snappingConfig()
        snapping.setEnabled(True)
        snapping.setMode(QgsSnappingConfig.AllLayers)
        snapping.setType(QgsSnappingConfig.Vertex)
        snapping.setUnits(QgsTolerance.Pixels)
        snapping.setTolerance(9)
        QgsProject.instance().setSnappingConfig(snapping)

        # Don't suppress feature form
        form_config = self._physical_zone_valuation.editFormConfig()
        form_config.setSuppress(QgsEditFormConfig.SuppressOff)
        self._physical_zone_valuation.setEditFormConfig(form_config)

        # Enable edition mode
        self.iface.layerTreeView().setCurrentLayer(self._physical_zone_valuation)
        self._physical_zone_valuation.startEditing()
        self.iface.actionAddFeature().trigger()

        self.iface.messageBar().pushMessage('Asistente LADM_COL',
            QCoreApplication.translate("CreatePhysicalZoneValuationWizard",
                                       "You can now start capturing physical zones digitizing on the map..."),
            Qgis.Info)

    def save_settings(self):
        settings = QSettings()
        settings.setValue('Asistente-LADM_COL/wizards/physical_zone_valuation_load_data_type', 'digitizing' if self.rad_digitizing.isChecked() else 'refactor')

    def restore_settings(self):
        settings = QSettings()

        load_data_type = settings.value('Asistente-LADM_COL/wizards/physical_zone_valuation_load_data_type') or 'digitizing'
        if load_data_type == 'refactor':
            self.rad_refactor.setChecked(True)
        else:
            self.rad_digitizing.setChecked(True)

    def show_help(self):
        self.qgis_utils.show_help("create_physical_zone_valuation")
