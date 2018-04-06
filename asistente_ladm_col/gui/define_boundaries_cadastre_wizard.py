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
from qgis.core import (QgsProject, QgsVectorLayer, QgsEditFormConfig,
                       QgsSnappingConfig, QgsTolerance, QgsFeature, Qgis,
                       QgsMapLayerProxyModel)
from qgis.PyQt.QtCore import Qt, QPoint, QCoreApplication, QSettings
from qgis.PyQt.QtWidgets import QAction, QWizard, QToolBar

from ..utils import get_ui_class
from ..config.table_mapping_config import (
    BOUNDARY_TABLE,
    LENGTH_FIELD_BOUNDARY_TABLE,
    VIDA_UTIL_FIELD_BOUNDARY_TABLE
)
from ..config.help_strings import HelpStrings

WIZARD_UI = get_ui_class('wiz_define_boundaries_cadastre.ui')

class DefineBoundariesCadastreWizard(QWizard, WIZARD_UI):
    def __init__(self, iface, db, qgis_utils, parent=None):
        QWizard.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self._boundary_layer = None
        self._db = db
        self.qgis_utils = qgis_utils
        self.help_strings = HelpStrings()

        self.restore_settings()

        self.rad_digitizing.toggled.connect(self.adjust_page_1_controls)
        self.adjust_page_1_controls()
        self.button(QWizard.FinishButton).clicked.connect(self.finished_dialog)

        self.mMapLayerComboBox.setFilters(QgsMapLayerProxyModel.LineLayer)

    def adjust_page_1_controls(self):
        if self.rad_refactor.isChecked():
            self.lbl_refactor_source.setEnabled(True)
            self.mMapLayerComboBox.setEnabled(True)
            finish_button_text = "Import"
            self.txt_help_page_1.setHtml(self.help_strings.get_refactor_help_string(BOUNDARY_TABLE, False))

        elif self.rad_digitizing.isChecked():
            self.lbl_refactor_source.setEnabled(False)
            self.mMapLayerComboBox.setEnabled(False)
            finish_button_text = "Start"
            self.txt_help_page_1.setHtml(self.help_strings.WIZ_DEFINE_BOUNDARIES_CADASTRE_PAGE_1_OPTION_DIGITIZE)

        self.wizardPage1.setButtonText(QWizard.FinishButton,
                                       QCoreApplication.translate("DefineBoundariesCadastreWizard",
                                       finish_button_text))

    def finished_dialog(self):
        self.save_settings()

        if self.rad_refactor.isChecked():
            if self.mMapLayerComboBox.currentLayer() is not None:
                self.qgis_utils.show_etl_model(self._db,
                                               self.mMapLayerComboBox.currentLayer(),
                                               BOUNDARY_TABLE)
            else:
                self.iface.messageBar().pushMessage("Asistente LADM_COL",
                    QCoreApplication.translate("DefineBoundariesCadastreWizard",
                                               "Select a source layer to set the field mapping to '{}'.").format(BOUNDARY_TABLE),
                    Qgis.Warning)

        elif self.rad_digitizing.isChecked():
            self.prepare_boundary_creation()

    def prepare_boundary_creation(self):
        # Load layers
        self._boundary_layer = self.qgis_utils.get_layer(self._db, BOUNDARY_TABLE, load=True)
        if self._boundary_layer is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                QCoreApplication.translate("DefineBoundariesCadastreWizard",
                                           "Boundary layer couldn't be found... {}").format(self._db.get_description()),
                Qgis.Warning)
            return

        # Disable transactions groups
        QgsProject.instance().setAutoTransaction(False)

        # Configure automatic field longitud
        self.qgis_utils.configureAutomaticField(self._boundary_layer, LENGTH_FIELD_BOUNDARY_TABLE, "$length")
        self.qgis_utils.configureAutomaticField(self._boundary_layer, VIDA_UTIL_FIELD_BOUNDARY_TABLE, "now()")

        # Configure Snapping
        snapping = QgsProject.instance().snappingConfig()
        snapping.setEnabled(True)
        snapping.setMode(QgsSnappingConfig.AllLayers)
        snapping.setType(QgsSnappingConfig.Vertex)
        snapping.setUnits(QgsTolerance.Pixels)
        snapping.setTolerance(9)
        QgsProject.instance().setSnappingConfig(snapping)

        # Suppress feature form
        form_config = self._boundary_layer.editFormConfig()
        form_config.setSuppress(QgsEditFormConfig.SuppressOn)
        self._boundary_layer.setEditFormConfig(form_config)

        # Enable edition mode
        self.iface.layerTreeView().setCurrentLayer(self._boundary_layer)
        self._boundary_layer.startEditing()
        self.iface.actionAddFeature().trigger()

        boundary_toolbar = self.iface.mainWindow().findChild(QToolBar, 'DefineBoundaries')
        boundary_toolbar.setVisible(True)

        self.iface.messageBar().pushMessage("Asistente LADM_COL",
            QCoreApplication.translate("DefineBoundariesCadastreWizard",
                                       "You can now start capturing boundaries clicking on the map..."),
            Qgis.Info)

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
