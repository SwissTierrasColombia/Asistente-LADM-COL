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
from qgis.core import QgsWkbTypes, QgsFeatureRequest, QgsExpression, QgsApplication
from qgis.PyQt.QtCore import Qt, pyqtSignal, QCoreApplication
from qgis.PyQt.QtWidgets import QTableWidgetItem, QMenu, QAction

from asistente_ladm_col.config.general_config import (PARCEL_STATUS_DISPLAY,
                                                      PARCEL_STATUS,
                                                      STATUS_COLORS, SOURCE_DB, COLLECTED_DB_SOURCE,
                                                      CHANGE_DETECTION_MISSING_PARCEL, CHANGE_DETECTION_NEW_PARCEL,
                                                      OFFICIAL_DB_SOURCE)
from asistente_ladm_col.config.table_mapping_config import (PLOT_TABLE,
                                                            PARCEL_TABLE,
                                                            UEBAUNIT_TABLE,
                                                            ID_FIELD, PARCEL_NUMBER_FIELD)
from asistente_ladm_col.utils import get_ui_class

WIDGET_UI = get_ui_class('change_detection/changes_all_parcels_panel_widget.ui')


class ChangesAllParcelsPanelWidget(QgsPanelWidget, WIDGET_UI):
    changes_per_parcel_panel_requested = pyqtSignal(str)

    def __init__(self, parent, utils, filter_parcels=dict()):
        QgsPanelWidget.__init__(self, parent)
        self.setupUi(self)
        self.parent = parent
        self.utils = utils

        self.setDockMode(True)

        self.tbl_changes_all_parcels.setColumnWidth(0, 270)

        self.tbl_changes_all_parcels.itemDoubleClicked.connect(self.call_changes_per_parcel_panel)
        self.btn_select_all_listed_parcels.clicked.connect(partial(self.select_related_plots_listed, True))

        self.tbl_changes_all_parcels.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tbl_changes_all_parcels.customContextMenuRequested.connect(self.show_context_menu)

        # Remove selection in plot layers
        self.utils._layers[PLOT_TABLE]['layer'].removeSelection()
        self.utils._official_layers[PLOT_TABLE]['layer'].removeSelection()

        self.fill_table(filter_parcels)

    def fill_table(self, filter_parcels=dict()):
        if not filter_parcels or (filter_parcels and filter_parcels[SOURCE_DB] == COLLECTED_DB_SOURCE):
            inverse = False
        else:
            inverse = True  # Take the official db as base db

        compared_parcels_data = self.utils.get_compared_parcels_data(inverse)

        self.tbl_changes_all_parcels.clearContents()
        self.tbl_changes_all_parcels.setRowCount(len(filter_parcels[PARCEL_NUMBER_FIELD]) if filter_parcels else len(compared_parcels_data))
        self.tbl_changes_all_parcels.setSortingEnabled(False)

        row = 0
        for parcel_number, parcel_attrs in compared_parcels_data.items():
            if not filter_parcels or (filter_parcels and parcel_number in filter_parcels[PARCEL_NUMBER_FIELD]):
                item = QTableWidgetItem(parcel_number) if parcel_number else QTableWidgetItem(QgsApplication.nullRepresentation())
                item.setData(Qt.UserRole, {ID_FIELD: parcel_attrs[ID_FIELD], 'inverse': inverse})
                self.tbl_changes_all_parcels.setItem(row, 0, item)

                status = parcel_attrs[PARCEL_STATUS]
                status_display = parcel_attrs[PARCEL_STATUS_DISPLAY]
                if filter_parcels:
                    # If we are on the official DB, "new" parcels are "missing" parcels from the collected db perspective
                    if filter_parcels[SOURCE_DB] == OFFICIAL_DB_SOURCE and parcel_attrs[PARCEL_STATUS_DISPLAY] == CHANGE_DETECTION_NEW_PARCEL:
                        status_display = CHANGE_DETECTION_MISSING_PARCEL
                        status = CHANGE_DETECTION_MISSING_PARCEL
                    
                item = QTableWidgetItem(status_display)
                item.setData(Qt.UserRole, {ID_FIELD: parcel_attrs[ID_FIELD], 'inverse': inverse})
                self.tbl_changes_all_parcels.setItem(row, 1, item)
                color = STATUS_COLORS[status]
                self.tbl_changes_all_parcels.item(row, 1).setBackground(color)

                row += 1

        self.tbl_changes_all_parcels.setSortingEnabled(True)

        # Zoom and flash features
        if filter_parcels:
            plot_layer = None
            if filter_parcels[SOURCE_DB] == COLLECTED_DB_SOURCE:
                plot_layer = self.utils._layers[PLOT_TABLE]['layer']
            else:
                plot_layer = self.utils._official_layers[PLOT_TABLE]['layer']

            plot_ids = self.utils.ladm_data.get_plots_related_to_parcels(self.utils._db if filter_parcels[SOURCE_DB] == COLLECTED_DB_SOURCE else self.utils._official_db,
                          filter_parcels[ID_FIELD],
                          None, # Get QGIS plot ids
                          plot_layer,
                          self.utils._layers[UEBAUNIT_TABLE]['layer'] if filter_parcels[SOURCE_DB] == COLLECTED_DB_SOURCE else self.utils._official_layers[UEBAUNIT_TABLE]['layer'])
            self.parent.request_zoom_to_features(plot_layer, ids=plot_ids, duration=3000)

            # plot_layer.select(plot_ids)
        else:
            self.utils.qgis_utils.activate_layer_requested.emit(self.utils._layers[PLOT_TABLE]['layer'])
            self.utils.iface.zoomToActiveLayer()

        self.select_related_plots_listed(False)

    def show_context_menu(self, point):
        table_widget = self.sender()
        item = table_widget.itemAt(point)

        context_menu = QMenu("Context menu")

        parcels_t_ids = item.data(Qt.UserRole)[ID_FIELD]

        if parcels_t_ids is None:
            return

        res_layers = self.utils.qgis_utils.get_layers(self.utils._db, {
            PLOT_TABLE: {'name': PLOT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry},
            PARCEL_TABLE: {'name': PARCEL_TABLE, 'geometry': None},
            UEBAUNIT_TABLE: {'name': UEBAUNIT_TABLE, 'geometry': None}}, load=True)

        plot_layer = res_layers[PLOT_TABLE]
        plot_layer.setSubsetString("")

        plot_ids = self.utils.ladm_data.get_plots_related_to_parcels(self.utils._db, parcels_t_ids, field_name=None, plot_layer=plot_layer, uebaunit_table=res_layers[UEBAUNIT_TABLE])

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

    def select_related_plots_listed(self, zoom_to_selected=True):
        parcels_t_ids_collected = list()
        parcels_t_ids_official = list()

        for row in range(self.tbl_changes_all_parcels.rowCount()):
            item = self.tbl_changes_all_parcels.item(row, 0)
            if item.data(Qt.UserRole)['inverse']:
                parcels_t_ids_official.extend(item.data(Qt.UserRole)[ID_FIELD])
            else:
                parcels_t_ids_collected.extend(item.data(Qt.UserRole)[ID_FIELD])

        if parcels_t_ids_collected:
            self.select_related_plots(parcels_t_ids_collected, False)

        if parcels_t_ids_official:
            self.select_related_plots(parcels_t_ids_official, True)

        if zoom_to_selected:
            plot_layer = self.utils._layers[PLOT_TABLE]['layer']
            if plot_layer.selectedFeatureIds():
                self.utils.iface.mapCanvas().zoomToFeatureIds(plot_layer, plot_layer.selectedFeatureIds())
            else:  # Bajas
                plot_layer = self.utils._official_layers[PLOT_TABLE]['layer']
                self.utils.iface.mapCanvas().zoomToFeatureIds(plot_layer, plot_layer.selectedFeatureIds())

    def select_related_plots(self, parcels_t_ids, inverse):
        plot_layer = self.utils._official_layers[PLOT_TABLE]['layer'] if inverse else self.utils._layers[PLOT_TABLE]['layer']
        uebaunit_table = self.utils._official_layers[UEBAUNIT_TABLE]['layer'] if inverse else self.utils._layers[UEBAUNIT_TABLE]['layer']
        plot_ids = self.utils.ladm_data.get_plots_related_to_parcels(self.utils._official_db if inverse else self.utils._db,
                                                                     parcels_t_ids,
                                                                     field_name=None,  # Get QGIS ids
                                                                     plot_layer=plot_layer,
                                                                     uebaunit_table=uebaunit_table)

        #self.parent.request_zoom_to_features(plot_layer, ids=plot_ids, duration=3000)
        plot_layer.select(plot_ids)
