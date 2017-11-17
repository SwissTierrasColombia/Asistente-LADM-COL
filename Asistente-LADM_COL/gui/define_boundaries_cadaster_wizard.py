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
from qgis.PyQt.QtCore import Qt, QPoint
from qgis.PyQt.QtWidgets import QAction, QWizard, QToolBar

from ..utils import qgis_utils, get_ui_class
from ..config.table_mapping_config import LENGTH_FIELD_BOUNDARY_TABLE

WIZARD_UI = get_ui_class('wiz_define_boundaries_cadaster.ui')

class DefineBoundariesCadasterWizard(QWizard, WIZARD_UI):
    def __init__(self, iface, parent=None):
        QWizard.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self._boundary_layer = None

        self.button(QWizard.FinishButton).clicked.connect(self.prepare_boundary_creation)

    def prepare_boundary_creation(self):
        # Load layers
        uri = 'dbname=\'test3\' host=localhost port=5432 user=\'postgres\' password=\'postgres\' sslmode=disable key=\'t_id\' srid=3116 type=LineString checkPrimaryKeyUnicity=\'1\' table="ladm_col_02"."lindero" (geometria) sql='
        self._boundary_layer = QgsVectorLayer(uri, "Lindero", "postgres")
        QgsProject.instance().addMapLayer(self._boundary_layer)

        # Configure automatic field longitud
        qgis_utils.configureAutomaticField(self._boundary_layer, LENGTH_FIELD_BOUNDARY_TABLE, "$length")

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
        self._boundary_layer.startEditing()
        self.iface.actionAddFeature().trigger()

        boundary_toolbar = self.iface.mainWindow().findChild(QToolBar, 'DefineBoundaries')
        boundary_toolbar.setVisible(True)
