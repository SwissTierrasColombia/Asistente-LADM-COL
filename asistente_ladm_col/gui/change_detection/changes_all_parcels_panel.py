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
from functools import partial

from qgis.gui import QgsPanelWidget
from qgis.core import QgsWkbTypes, QgsFeatureRequest, QgsExpression
from qgis.PyQt.QtCore import Qt, pyqtSignal, QCoreApplication
from qgis.PyQt.QtWidgets import QTableWidgetItem, QMenu, QAction

from asistente_ladm_col.config.general_config import (PARCEL_STATUS_DISPLAY,
                                                      PARCEL_STATUS,
                                                      STATUS_COLORS)
from asistente_ladm_col.config.table_mapping_config import (PLOT_TABLE,
                                                            PARCEL_TABLE,
                                                            UEBAUNIT_TABLE,
                                                            ID_FIELD)
from asistente_ladm_col.utils import get_ui_class

WIDGET_UI = get_ui_class('change_detection/changes_all_parcels_panel_widget.ui')


class ChangesAllParcelsPanelWidget(QgsPanelWidget, WIDGET_UI):
    changes_per_parcel_panel_requested = pyqtSignal(str)

    def __init__(self, parent, utils, filter_parcels=list()):
        QgsPanelWidget.__init__(self, parent)
        self.setupUi(self)
        self.parent = parent
        self.utils = utils

        self.setDockMode(True)

        self.tbl_changes_all_parcels.setColumnWidth(0, 270)

        self.tbl_changes_all_parcels.itemDoubleClicked.connect(self.call_changes_per_parcel_panel)

        self.tbl_changes_all_parcels.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tbl_changes_all_parcels.customContextMenuRequested.connect(self.show_context_menu)

        self.fill_table(filter_parcels)

    def fill_table(self, filter_parcels=list()):
        compared_parcels_data = self.utils.get_compared_parcels_data(self.utils._db, self.utils._official_db)

        self.tbl_changes_all_parcels.clearContents()
        self.tbl_changes_all_parcels.setRowCount(len(filter_parcels) or len(compared_parcels_data))
        self.tbl_changes_all_parcels.setSortingEnabled(False)

        row = 0
        for parcel_number, parcel_attrs in compared_parcels_data.items():
            if not filter_parcels or (filter_parcels and parcel_number in filter_parcels):
                item = QTableWidgetItem(parcel_number)
                item.setData(Qt.UserRole, parcel_attrs[ID_FIELD])
                self.tbl_changes_all_parcels.setItem(row, 0, item)

                item = QTableWidgetItem(parcel_attrs[PARCEL_STATUS_DISPLAY])
                item.setData(Qt.UserRole, parcel_attrs[ID_FIELD])
                self.tbl_changes_all_parcels.setItem(row, 1, item)
                color = STATUS_COLORS[parcel_attrs[PARCEL_STATUS]]
                self.tbl_changes_all_parcels.item(row, 1).setBackground(color)

                row += 1

        self.tbl_changes_all_parcels.setSortingEnabled(True)

    def show_context_menu(self, point):
        table_widget = self.sender()
        item = table_widget.itemAt(point)

        context_menu = QMenu("Context menu")

        parcels_t_ids = item.data(Qt.UserRole)

        if parcels_t_ids is None:
            return

        res_layers=self.utils.qgis_utils.get_layers(self._db, {
            PLOT_TABLE: {'name': PLOT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry},
            PARCEL_TABLE: {'name': PARCEL_TABLE, 'geometry': None},
            UEBAUNIT_TABLE: {'name': UEBAUNIT_TABLE, 'geometry': None}}, load=True)

        plot_layer = res_layers[PLOT_TABLE]
        plot_layer.setSubsetString("")

        plot_ids = self.utils.ladm_data.get_plots_related_to_parcels(self._db, parcels_t_ids, field_name=None, plot_layer=plot_layer, uebaunit_table=res_layers[UEBAUNIT_TABLE])

        if plot_ids:
            action_zoom = QAction(QCoreApplication.translate("ChangesAllParcelsPanelWidget", "Zoom to related plots"))
            action_zoom.triggered.connect(partial(self.parent.request_zoom_to_features, plot_layer, plot_ids, list()))
            context_menu.addAction(action_zoom)

        action_view_changes = QAction(QCoreApplication.translate("ChangesAllParcelsPanelWidget", "View changes for this parcel number"))
        action_view_changes.triggered.connect(partial(self.call_changes_per_parcel_panel, item))
        context_menu.addAction(action_view_changes)

        if context_menu.actions():
            context_menu.exec_(table_widget.mapToGlobal(point))

    def call_changes_per_parcel_panel(self, item):
        parcel_number = self.tbl_changes_all_parcels.item(item.row(), 0).text()
        self.changes_per_parcel_panel_requested.emit(parcel_number)