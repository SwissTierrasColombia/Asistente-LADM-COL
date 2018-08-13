# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2018-06-11
        git sha              : :%H$
        copyright            : (C) 2018 by Germán Carrillo (BSF Swissphoto)
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
import os

from qgis.core import QgsWkbTypes
from qgis.PyQt.QtCore import Qt, QSettings, QCoreApplication
from qgis.PyQt.QtGui import QBrush, QFont, QIcon, QColor
from qgis.PyQt.QtWidgets import (
    QDialog,
    QListWidgetItem,
    QDialogButtonBox
)
from ..config.table_mapping_config import (
    BOUNDARY_TABLE,
    BOUNDARY_POINT_TABLE,
    BUILDING_TABLE,
    BUILDING_UNIT_TABLE,
    PLOT_TABLE,
    SURVEY_POINT_TABLE
)
from ..utils import get_ui_class

from ..resources_rc import *

DIALOG_UI = get_ui_class('dlg_topological_edition.ui')

class LayersForTopologicalEdition(QDialog, DIALOG_UI):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.selected_layers_info = dict()

        self.lst_plots.clear()
        self.lst_buildings.clear()

        self.plots = {
            BOUNDARY_POINT_TABLE: {'name': BOUNDARY_POINT_TABLE, 'geometry': None},
            BOUNDARY_TABLE: {'name': BOUNDARY_TABLE, 'geometry': None},
            PLOT_TABLE: {'name': PLOT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry}
        }

        self.buildings = {
            SURVEY_POINT_TABLE: {'name': SURVEY_POINT_TABLE, 'geometry': None},
            BUILDING_TABLE: {'name': BUILDING_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry},
            BUILDING_UNIT_TABLE: {'name': BUILDING_UNIT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry}
        }

        icons = {
            BOUNDARY_POINT_TABLE: QIcon(":/Asistente-LADM_COL/resources/images/points.png"),
            BOUNDARY_TABLE: QIcon(":/Asistente-LADM_COL/resources/images/lines.png"),
            PLOT_TABLE: QIcon(":/Asistente-LADM_COL/resources/images/polygons.png"),
            SURVEY_POINT_TABLE: QIcon(":/Asistente-LADM_COL/resources/images/points.png"),
            BUILDING_TABLE: QIcon(":/Asistente-LADM_COL/resources/images/polygons.png"),
            BUILDING_UNIT_TABLE: QIcon(":/Asistente-LADM_COL/resources/images/polygons.png")
        }

        for k, v in self.plots.items():
            item = QListWidgetItem()
            item.setData(Qt.DecorationRole, icons[k])
            item.setText(k)
            self.lst_plots.addItem(item)

        for k, v in self.buildings.items():
            item = QListWidgetItem()
            item.setData(Qt.DecorationRole, icons[k])
            item.setText(k)
            self.lst_buildings.addItem(item)

        # Set connections
        self.buttonBox.accepted.connect(self.accepted)
        self.rad_plots.toggled.connect(self.update_controls)
        self.lst_plots.itemSelectionChanged.connect(self.update_controls)
        self.lst_buildings.itemSelectionChanged.connect(self.update_controls)

        self.update_controls() # Initialize GUI state

    def update_controls(self):
        checked = self.rad_plots.isChecked()
        self.lst_plots.setEnabled(checked)
        self.lst_buildings.setEnabled(not checked)
        if checked:
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(len(self.lst_plots.selectedItems()) > 1)
            self.lst_buildings.clearSelection()
        else:
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(len(self.lst_buildings.selectedItems()) > 1)
            self.lst_plots.clearSelection()

    def accepted(self):
        if self.rad_plots.isChecked():
            items = self.lst_plots.selectedItems()
            self.selected_layers_info = {i.text(): self.plots[i.text()] for i in items}
        else:
            items = self.lst_buildings.selectedItems()
            self.selected_layers_info = {i.text(): self.buildings[i.text()] for i in items}

        self.done(1)

    def rejected(self):
        pass
