# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-05-16
        git sha              : :%H$
        copyright            : (C) 2019 by Germán Carrillo (BSF Swissphoto)
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
from qgis.PyQt.QtCore import Qt, pyqtSignal
from qgis.PyQt.QtWidgets import QTableWidgetItem
from qgis.gui import QgsPanelWidget

from asistente_ladm_col.config.table_mapping_config import PARCEL_NUMBER_FIELD
from asistente_ladm_col.utils import get_ui_class

WIDGET_UI = get_ui_class('change_detection/changes_all_parcels_panel_widget.ui')
PARCEL_STATUS = '_PARCEL_STATUS_'
QGIS_ID = "_qgis_id_"
CHANGE_DETECTION_NEW_PARCEL = 'Alta'
CHANGE_DETECTION_PARCEL_CHANGED = 'Cambio'
CHANGE_DETECTION_PARCEL_REMAINS = 'OK'
CHANGE_DETECTION_PARCEL_CHANGED = 'Cambio'

class ChangesAllParcelsPanelWidget(QgsPanelWidget, WIDGET_UI):
    changes_per_parcel_panel_requested = pyqtSignal(str)

    def __init__(self, iface, db, official_db, qgis_utils, ladm_data, parent=None):
        QgsPanelWidget.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self.canvas = iface.mapCanvas()
        self._db = db
        self._official_db = official_db
        self.qgis_utils = qgis_utils
        self.ladm_data = ladm_data

        self.setDockMode(True)

        self.tbl_changes_all_parcels.itemDoubleClicked.connect(self.call_changes_per_parcel_panel)

    def fill_table(self):
        compared_parcels_data = self.get_compared_parcels_data()

        self.tbl_changes_all_parcels.clearContents()
        self.tbl_changes_all_parcels.setRowCount(len(compared_parcels_data))
        self.tbl_changes_all_parcels.setSortingEnabled(False)

        for row, (parcel_number, parcel_attrs) in enumerate(compared_parcels_data.items()):
            item = QTableWidgetItem(parcel_number)
            item.setData(Qt.UserRole, parcel_number)
            self.tbl_changes_all_parcels.setItem(row, 0, item)
            item = QTableWidgetItem(parcel_attrs[PARCEL_STATUS])
            item.setData(Qt.UserRole, parcel_number)
            self.tbl_changes_all_parcels.setItem(row, 1, item)

        self.tbl_changes_all_parcels.setSortingEnabled(True)

        # TODO
        #   On Select: zoom to plots  itemSelectionChanged

    def get_compared_parcels_data(self):
        dict_collected_parcels = self.ladm_data.get_parcel_data_to_compare_changes(self._db, None)
        #print(dict_collected_parcels)
        dict_official_parcels = self.ladm_data.get_parcel_data_to_compare_changes(self._official_db, None)

        dict_compared_parcel_data = dict()

        for collected_parcel_number, collected_attrs in dict_collected_parcels.items():
            dict_attrs_comparison = dict()

            # A parcel number has at least one dict of attributes (i.e., one feature)
            dict_attrs_comparison[PARCEL_NUMBER_FIELD] = collected_parcel_number
            dict_attrs_comparison[QGIS_ID] = [attr[QGIS_ID] for attr in collected_attrs]

            if len(collected_attrs) > 1:
                dict_attrs_comparison[PARCEL_STATUS] = "({})".format(len(collected_attrs))
            else:
                if not collected_parcel_number in dict_official_parcels:
                    dict_attrs_comparison[PARCEL_STATUS] = CHANGE_DETECTION_NEW_PARCEL
                else:
                    official_attrs = dict_official_parcels[collected_parcel_number]

                    del collected_attrs[0][QGIS_ID]
                    del official_attrs[0][QGIS_ID]
                    dict_attrs_comparison[PARCEL_STATUS] = CHANGE_DETECTION_PARCEL_REMAINS if collected_attrs[0] == official_attrs[0] else CHANGE_DETECTION_PARCEL_CHANGED

            dict_compared_parcel_data[collected_parcel_number] = dict_attrs_comparison

        return dict_compared_parcel_data

    def call_changes_per_parcel_panel(self, item):
        parcel_number = item.data(Qt.UserRole)
        self.changes_per_parcel_panel_requested.emit(parcel_number)
