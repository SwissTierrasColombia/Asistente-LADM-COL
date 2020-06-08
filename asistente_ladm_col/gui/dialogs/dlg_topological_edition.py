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

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import (QDialog,
                                 QListWidgetItem,
                                 QDialogButtonBox)

from asistente_ladm_col.utils import get_ui_class

DIALOG_UI = get_ui_class('dialogs/dlg_topological_edition.ui')


class LayersForTopologicalEditionDialog(QDialog, DIALOG_UI):
    def __init__(self, names, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.names = names
        self.selected_layers_info = dict()

        self.lst_plots.clear()
        self.lst_buildings.clear()

        self.plots = {
            self.names.OP_BOUNDARY_POINT_T: None,
            self.names.OP_BOUNDARY_T: None,
            self.names.OP_PLOT_T: None
        }

        self.buildings = {
            self.names.OP_SURVEY_POINT_T: None,
            self.names.OP_BUILDING_T: None,
            self.names.OP_BUILDING_UNIT_T: None
        }

        icons = {
            self.names.OP_BOUNDARY_POINT_T: QIcon(":/Asistente-LADM-COL/resources/images/points.png"),
            self.names.OP_BOUNDARY_T: QIcon(":/Asistente-LADM-COL/resources/images/lines.png"),
            self.names.OP_PLOT_T: QIcon(":/Asistente-LADM-COL/resources/images/polygons.png"),
            self.names.OP_SURVEY_POINT_T: QIcon(":/Asistente-LADM-COL/resources/images/points.png"),
            self.names.OP_BUILDING_T: QIcon(":/Asistente-LADM-COL/resources/images/polygons.png"),
            self.names.OP_BUILDING_UNIT_T: QIcon(":/Asistente-LADM-COL/resources/images/polygons.png")
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
