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

from qgis.PyQt.QtCore import (Qt,
                              QCoreApplication)
from qgis.PyQt.QtWidgets import (QDialog,
                                 QListWidgetItem,
                                 QDialogButtonBox)
from asistente_ladm_col.utils import get_ui_class

DIALOG_UI = get_ui_class('dialogs/dlg_topological_edition.ui')


class LayersForTopologicalEditionDialog(QDialog, DIALOG_UI):
    def __init__(self, names, models, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.names = names
        self.selected_layers_info = list()

        self.tab_survey_idx = 0
        self.tab_fdc_idx = 1
        self.tab_widget.setTabText(self.tab_survey_idx, QCoreApplication.translate("LayersForTopologicalEditionDialog", "Survey"))
        self.tab_widget.setTabText(self.tab_fdc_idx, QCoreApplication.translate("LayersForTopologicalEditionDialog", "Field Data Capture"))

        self.lst_plots.clear()
        self.lst_buildings.clear()
        self.lst_fdc_plots.clear()
        self.lst_fdc_buildings.clear()

        # Get lists of layers and dict of icons depending on the models available in the DB
        from asistente_ladm_col.config.layer_config import LayerConfig
        self.plots, self.buildings, self.fdc_plots, self.fdc_buildings, icons = LayerConfig.get_topological_edition_configuration(names, models)

        for layer_name in self.plots:
            item = QListWidgetItem()
            item.setData(Qt.DecorationRole, icons[layer_name])
            item.setText(layer_name)
            self.lst_plots.addItem(item)

        for layer_name in self.buildings:
            item = QListWidgetItem()
            item.setData(Qt.DecorationRole, icons[layer_name])
            item.setText(layer_name)
            self.lst_buildings.addItem(item)

        for layer_name in self.fdc_plots:
            item = QListWidgetItem()
            item.setData(Qt.DecorationRole, icons[layer_name])
            item.setText(layer_name)
            self.lst_fdc_plots.addItem(item)

        for layer_name in self.fdc_buildings:
            item = QListWidgetItem()
            item.setData(Qt.DecorationRole, icons[layer_name])
            item.setText(layer_name)
            self.lst_fdc_buildings.addItem(item)

        # Set connections
        self.buttonBox.accepted.connect(self.accepted)
        self.rad_plots.toggled.connect(self.update_controls)
        self.rad_fdc_plots.toggled.connect(self.update_controls)
        self.lst_plots.itemSelectionChanged.connect(self.update_controls)
        self.lst_buildings.itemSelectionChanged.connect(self.update_controls)
        self.lst_fdc_plots.itemSelectionChanged.connect(self.update_controls)
        self.lst_fdc_buildings.itemSelectionChanged.connect(self.update_controls)

        self.tab_widget.setCurrentIndex(self.tab_fdc_idx if bool(self.fdc_plots) else self.tab_survey_idx)
        self.update_controls() # Initialize GUI state

    def update_controls(self):
        # Tabs
        self.tab_widget.setTabEnabled(self.tab_survey_idx, bool(self.plots))
        self.tab_widget.setTabEnabled(self.tab_fdc_idx, bool(self.fdc_plots))

        # Inner widgets
        if self.tab_widget.currentIndex() == self.tab_survey_idx:  # Survey model tab enabled
            self.update_inner_controls(self.rad_plots, self.lst_plots, self.lst_buildings)
        else:  # Field data capture model tab enabled
            self.update_inner_controls(self.rad_fdc_plots, self.lst_fdc_plots, self.lst_fdc_buildings)

    def update_inner_controls(self, rad_plots, lst_plots, lst_buildings):
        checked = rad_plots.isChecked()
        lst_plots.setEnabled(checked)
        lst_buildings.setEnabled(not checked)
        if checked:
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(len(lst_plots.selectedItems()) > 1)
            lst_buildings.clearSelection()
        else:
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(len(lst_buildings.selectedItems()) > 1)
            lst_plots.clearSelection()

    def accepted(self):
        if self.tab_widget.currentIndex() == self.tab_survey_idx:  # Survey model tab enabled
            self.get_selected_layer_names(self.rad_plots,
                                         self.lst_plots,
                                         self.lst_buildings)
        else:  # Field data capture model tab enabled
            self.get_selected_layer_names(self.rad_fdc_plots,
                                         self.lst_fdc_plots,
                                         self.lst_fdc_buildings)

        self.done(1)

    def get_selected_layer_names(self, rad_plots, lst_plots, lst_buildings):
        if rad_plots.isChecked():
            self.selected_layers_info = [i.text() for i in lst_plots.selectedItems()]
        else:
            self.selected_layers_info = [i.text() for i in lst_buildings.selectedItems()]

    def rejected(self):
        pass
