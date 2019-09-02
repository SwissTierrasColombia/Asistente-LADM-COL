# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-02-08
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

DIALOG_UI = get_ui_class('change_detection/dlg_select_parcel_change_detection.ui')


class SelectParcelDialog(QDialog, DIALOG_UI):
    def __init__(self, parent, utils, data, dock):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.utils = utils
        self.data = data
        self.dock = dock
        self.parcel_id = None
        self.parcel_number = None

        self.fill_table()
        self.tbl_changes_parcels.itemClicked.connect(self.zoom_to_parcel)
        self.tbl_changes_parcels.itemDoubleClicked.connect(self.zoom_to_parcel)

        # Remove selection in plot layers
        self.utils._layers[PLOT_TABLE][LAYER].removeSelection()
        self.utils._official_layers[PLOT_TABLE][LAYER].removeSelection()

        self.select_button_name = QCoreApplication.translate("SelectParcelDialog", "Select")
        self.zoom_to_all_button_name = QCoreApplication.translate("SelectParcelDialog", "Zoom to all")
        self.buttonBox.accepted.disconnect()
        self.buttonBox.clicked.connect(self.button_box_clicked)
        self.buttonBox.clear()
        self.buttonBox.addButton(QDialogButtonBox.Cancel)
        self.buttonBox.addButton(self.zoom_to_all_button_name, QDialogButtonBox.AcceptRole)
        self.buttonBox.addButton(self.select_button_name, QDialogButtonBox.AcceptRole)

    def fill_table(self):
        self.tbl_changes_parcels.clearContents()
        self.tbl_changes_parcels.setRowCount(len(self.data))

        request = QgsFeatureRequest(QgsExpression('"{}" in ({})'.format(ID_FIELD, ",".join(str(t_id) for t_id in self.data))))
        field_idx = self.utils._layers[PARCEL_TABLE][LAYER].fields().indexFromName(ID_FIELD)
        request.setSubsetOfAttributes([field_idx])
        request.setFlags(QgsFeatureRequest.NoGeometry)
        parcels = self.utils._layers[PARCEL_TABLE][LAYER].getFeatures(request)

        if parcels:
            row = 0
            for parcel in parcels:
                self.tbl_changes_parcels.setItem(row, 0, QTableWidgetItem(str(parcel[ID_FIELD])))
                self.tbl_changes_parcels.setItem(row, 1, QTableWidgetItem(str(parcel[NUPRE_FIELD])))
                self.tbl_changes_parcels.setItem(row, 2, QTableWidgetItem(str(parcel[FMI_FIELD])))
                self.tbl_changes_parcels.setItem(row, 3, QTableWidgetItem(str(parcel[PARCEL_NUMBER_FIELD])))
                row += 1

    def zoom_to_parcel(self, item):
        row = item.row()
        self.lb_message.setText("")
        parcels_id = [int(self.tbl_changes_parcels.item(row, 0).text())]  # t_id of parcel
        self.zoom_to_parcels(parcels_id)

    def zoom_to_parcels(self, parcels_id):
        plot_ids = self.utils.ladm_data.get_plots_related_to_parcels(self.utils._db,
                                                                     parcels_id,
                                                                     field_name=ID_FIELD,
                                                                     plot_layer=self.utils._layers[PLOT_TABLE][LAYER],
                                                                     uebaunit_table=self.utils._layers[UEBAUNIT_TABLE][LAYER])

        self.utils._layers[PLOT_TABLE][LAYER].removeSelection()
        exp_select_plots = "{} IN ({})".format(ID_FIELD, ",".join([str(plot_id) for plot_id in plot_ids]))
        self.utils._layers[PLOT_TABLE][LAYER].selectByExpression(exp_select_plots)
        self.dock.request_zoom_to_features(self.utils._layers[PLOT_TABLE][LAYER], t_ids=plot_ids)

    def accepted(self):
        if len(self.tbl_changes_parcels.selectedItems()):
            self.lb_message.setText("")
            selected_row = self.tbl_changes_parcels.currentRow()
            self.parcel_id = self.tbl_changes_parcels.item(selected_row, 0).text()
            self.parcel_number = self.tbl_changes_parcels.item(selected_row, 3).text()
            self.close()
        else:
            self.lb_message.setText(QCoreApplication.translate("SelectParcelDialog", "You should select one parcel..."))
            self.lb_message.setStyleSheet('color:#FF0000')

    def button_box_clicked(self, button):
        if self.buttonBox.buttonRole(button) == QDialogButtonBox.AcceptRole:
            if button.text() == self.select_button_name:
                self.accepted()
            elif button.text() == self.zoom_to_all_button_name:
                # Zoom to all plots
                self.zoom_to_parcels(self.data)
                self.tbl_changes_parcels.clearSelection()
                self.lb_message.setText("")

    def reject(self):
        self.done(0)
