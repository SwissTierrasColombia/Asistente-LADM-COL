# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-08-21
        git sha              : :%H$
        copyright            : (C) 2019 by Leonardo Cardona (BSF Swissphoto)
        email                : leo dot cardona dot p at gmail dot com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtWidgets import (QDialog,
                                 QDialogButtonBox)
from qgis.PyQt.QtWidgets import QTableWidgetItem
from qgis.core import (QgsFeatureRequest,
                       QgsExpression)

from ...config.table_mapping_config import (PARCEL_NUMBER_FIELD,
                                            NUPRE_FIELD,
                                            FMI_FIELD,
                                            ID_FIELD,
                                            PARCEL_TABLE,
                                            PLOT_TABLE,
                                            UEBAUNIT_TABLE)
from ...config.general_config import LAYER
from ...utils import get_ui_class

DIALOG_UI = get_ui_class('change_detection/dlg_select_duplicate_parcel_change_detection.ui')


class SelectDuplicateParcelDialog(QDialog, DIALOG_UI):
    def __init__(self, utils, parcels_t_ids, parent):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.utils = utils
        self.parcels_t_ids = parcels_t_ids
        self.parent = parent
        self.parcel_t_id = None
        self.parcel_number = None

        self.fill_table()

        self.tbl_changes_parcels.itemSelectionChanged.connect(self.react_after_new_selection)

        # Remove selection in plot layers
        self.utils._layers[PLOT_TABLE][LAYER].removeSelection()
        self.utils._official_layers[PLOT_TABLE][LAYER].removeSelection()

        self.select_button_name = QCoreApplication.translate("SelectParcelDialog", "Show details for selected parcel")
        self.zoom_to_all_button_name = QCoreApplication.translate("SelectParcelDialog", "Zoom to all listed parcels")
        self.buttonBox.accepted.disconnect()
        self.buttonBox.clicked.connect(self.button_box_clicked)
        self.buttonBox.clear()
        self.buttonBox.addButton(QDialogButtonBox.Cancel)
        self.buttonBox.addButton(self.zoom_to_all_button_name, QDialogButtonBox.AcceptRole)
        self.buttonBox.addButton(self.select_button_name, QDialogButtonBox.AcceptRole)

        self.set_controls_enabled()

    def fill_table(self):
        self.tbl_changes_parcels.clearContents()
        self.tbl_changes_parcels.setRowCount(len(self.parcels_t_ids))

        request = QgsFeatureRequest(QgsExpression('"{}" in ({})'.format(ID_FIELD, ",".join(str(t_id) for t_id in self.parcels_t_ids))))
        request.setFlags(QgsFeatureRequest.NoGeometry)
        request.setSubsetOfAttributes([ID_FIELD,
                                       NUPRE_FIELD,
                                       FMI_FIELD,
                                       PARCEL_NUMBER_FIELD],
                                      self.utils._layers[PARCEL_TABLE][LAYER].fields())  # NOTE: this adds a new flag
        parcels = self.utils._layers[PARCEL_TABLE][LAYER].getFeatures(request)

        if parcels:
            row = 0
            for parcel in parcels:
                self.tbl_changes_parcels.setItem(row, 0, QTableWidgetItem(str(parcel[ID_FIELD])))
                self.tbl_changes_parcels.setItem(row, 1, QTableWidgetItem(str(parcel[NUPRE_FIELD])))
                self.tbl_changes_parcels.setItem(row, 2, QTableWidgetItem(str(parcel[FMI_FIELD])))
                self.tbl_changes_parcels.setItem(row, 3, QTableWidgetItem(str(parcel[PARCEL_NUMBER_FIELD])))
                row += 1

    def react_after_new_selection(self):
        """
        A new selection was made, we will react depending on what the new selection is.
        """
        selected_rows = [item.row() for item in self.tbl_changes_parcels.selectedItems()]
        if len(set(selected_rows)) == 1:  # Single row selected
            item = self.tbl_changes_parcels.selectedItems()[0]
            parcel_t_id = int(self.tbl_changes_parcels.item(item.row(), 0).text())  # parcel t_id
            self.zoom_to_parcels([parcel_t_id])

        self.set_controls_enabled()


    def zoom_to_parcels(self, parcels_t_ids):
        self.utils._layers[PLOT_TABLE][LAYER].removeSelection()
        plot_ids = self.utils.ladm_data.get_plots_related_to_parcels(self.utils._db,
                                                                     parcels_t_ids,
                                                                     field_name=None,
                                                                     plot_layer=self.utils._layers[PLOT_TABLE][LAYER],
                                                                     uebaunit_table=self.utils._layers[UEBAUNIT_TABLE][LAYER])

        self.parent.zoom_to_features_requested.emit(self.utils._layers[PLOT_TABLE][LAYER], plot_ids, list(), 500)

    def set_controls_enabled(self):
        for button in self.buttonBox.buttons():
            if button.text() == self.select_button_name:
                button.setEnabled(bool(self.tbl_changes_parcels.selectedItems()))
                break

    def accepted(self):
        selected_row = self.tbl_changes_parcels.currentRow()
        self.parcel_t_id = self.tbl_changes_parcels.item(selected_row, 0).text()
        self.parcel_number = self.tbl_changes_parcels.item(selected_row, 3).text()
        self.close()

    def button_box_clicked(self, button):
        if self.buttonBox.buttonRole(button) == QDialogButtonBox.AcceptRole:
            if button.text() == self.select_button_name:
                self.accepted()
            elif button.text() == self.zoom_to_all_button_name:
                # Zoom to all plots
                self.zoom_to_parcels(self.parcels_t_ids)
                self.tbl_changes_parcels.clearSelection()

    def reject(self):
        self.done(0)
