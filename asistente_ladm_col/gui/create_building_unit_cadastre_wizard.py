# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 09/05/18
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
from qgis.core import (QgsProject, QgsVectorLayer, QgsEditFormConfig,
                       QgsSnappingConfig, QgsTolerance, QgsFeature, Qgis,
                       QgsMapLayerProxyModel, QgsWkbTypes)
from qgis.PyQt.QtCore import Qt, QPoint, QCoreApplication, QSettings
from qgis.PyQt.QtWidgets import QAction, QWizard

from ..utils import get_ui_class
from ..config.table_mapping_config import (
    BUILDING_UNIT_TABLE,
    SURVEY_POINT_TABLE
)
from ..config.help_strings import HelpStrings

WIZARD_UI = get_ui_class('wiz_create_building_unit_cadastre.ui')

class CreateBuildingUnitCadastreWizard(QWizard, WIZARD_UI):
    def __init__(self, iface, db, qgis_utils, parent=None):
        QWizard.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self._building_unit_layer = None
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
        if self.rad_refactor.isChecked():
            self.lbl_refactor_source.setEnabled(True)
            self.mMapLayerComboBox.setEnabled(True)
            finish_button_text = 'Import'
            self.txt_help_page_1.setHtml(self.help_strings.get_refactor_help_string(BUILDING_UNIT_TABLE, True))

        elif self.rad_digitizing.isChecked():
            self.lbl_refactor_source.setEnabled(False)
            self.mMapLayerComboBox.setEnabled(False)
            finish_button_text = QCoreApplication.translate('CreateBuildingUnitCadastreWizard', 'Start')
            self.txt_help_page_1.setHtml(self.help_strings.WIZ_CREATE_BUILDING_UNIT_CADASTRE_PAGE_1_OPTION_POINTS)

        self.wizardPage1.setButtonText(QWizard.FinishButton,
                                       QCoreApplication.translate('CreateBuildingUnitCadastreWizard',
                                       finish_button_text))

    def finished_dialog(self):
        self.save_settings()

        if self.rad_refactor.isChecked():
            if self.mMapLayerComboBox.currentLayer() is not None:
                self.qgis_utils.show_etl_model(self._db,
                                               self.mMapLayerComboBox.currentLayer(),
                                               BUILDING_UNIT_TABLE,
                                               QgsWkbTypes.PolygonGeometry)
            else:
                self.iface.messageBar().pushMessage('Asistente LADM_COL',
                    QCoreApplication.translate('CreateBuildingUnitCadastreWizard',
                                               "Select a source layer to set the field mapping to '{}'.").format(BUILDING_UNIT_TABLE),
                    Qgis.Warning)

        elif self.rad_digitizing.isChecked():
            self.prepare_building_unit_creation()

    def prepare_building_unit_creation(self):
        # Load layers
        res_layers = self.qgis_utils.get_layers(self._db, {
            BUILDING_UNIT_TABLE: {'name': BUILDING_UNIT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry},
            SURVEY_POINT_TABLE: {'name': SURVEY_POINT_TABLE, 'geometry': None}
        }, load=True)

        self._building_unit_layer = res_layers[BUILDING_UNIT_TABLE]
        self._survey_point_layer = res_layers[SURVEY_POINT_TABLE]

        if self._building_unit_layer is None:
            self.iface.messageBar().pushMessage('Asistente LADM_COL',
                QCoreApplication.translate('CreateBuildingUnitCadastreWizard',
                                           "Building Unit layer couldn't be found... {}").format(self._db.get_description()),
                Qgis.Warning)
            return

        if self._survey_point_layer is None:
            self.iface.messageBar().pushMessage('Asistente LADM_COL',
                QCoreApplication.translate('CreateBuildingUnitCadastreWizard',
                                           "Survey Point layer couldn't be found... {}").format(self._db.get_description()),
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
        form_config = self._building_unit_layer.editFormConfig()
        form_config.setSuppress(QgsEditFormConfig.SuppressOff)
        self._building_unit_layer.setEditFormConfig(form_config)

        # Enable edition mode
        self.iface.layerTreeView().setCurrentLayer(self._building_unit_layer)
        self._building_unit_layer.startEditing()
        self.iface.actionAddFeature().trigger()

        self.iface.messageBar().pushMessage('Asistente LADM_COL',
            QCoreApplication.translate('CreateBuildingUnitCadastreWizard',
                                       'You can now start capturing building units digitizing on the map...'),
            Qgis.Info)

    def save_settings(self):
        settings = QSettings()
        settings.setValue('Asistente-LADM_COL/wizards/building_unit_load_data_type', 'digitizing' if self.rad_digitizing.isChecked() else 'refactor')

    def restore_settings(self):
        settings = QSettings()

        load_data_type = settings.value('Asistente-LADM_COL/wizards/building_unit_load_data_type') or 'digitizing'
        if load_data_type == 'refactor':
            self.rad_refactor.setChecked(True)
        else:
            self.rad_digitizing.setChecked(True)

    def show_help(self):
        self.qgis_utils.show_help("create_building_unit")
