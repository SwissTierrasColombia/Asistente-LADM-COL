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
                       QgsSnappingConfig, QgsTolerance, QgsFeature)
from qgis.gui import QgsMessageBar
from qgis.PyQt.QtCore import Qt, QPoint, QCoreApplication
from qgis.PyQt.QtWidgets import QAction, QWizard, QToolBar

from ..utils import get_ui_class
from ..config.table_mapping_config import (
    BOUNDARY_TABLE,
    LENGTH_FIELD_BOUNDARY_TABLE,
    VIDA_UTIL_FIELD_BOUNDARY_TABLE
)

WIZARD_UI = get_ui_class('wiz_define_boundaries_cadaster.ui')

class DefineBoundariesCadasterWizard(QWizard, WIZARD_UI):
    def __init__(self, iface, db, qgis_utils, parent=None):
        QWizard.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self._boundary_layer = None
        self._db = db
        self.qgis_utils = qgis_utils

        self.button(QWizard.FinishButton).clicked.connect(self.prepare_boundary_creation)

    def prepare_boundary_creation(self):
        # Load layers
        self._boundary_layer = self.qgis_utils.get_layer(self._db, BOUNDARY_TABLE, load=True)
        if self._boundary_layer is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                QCoreApplication.translate("DefineBoundariesCadasterWizard",
                                           "Boundary layer couldn't be found..."),
                QgsMessageBar.WARNING)
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

        # Suppress feature creation
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
            QCoreApplication.translate("DefineBoundariesCadasterWizard",
                                       "You can now start capturing boundaries clicking on the map..."),
            QgsMessageBar.INFO)
