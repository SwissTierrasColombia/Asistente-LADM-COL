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
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtCore import Qt, pyqtSignal, QCoreApplication
from qgis.PyQt.QtWidgets import QTableWidgetItem, QMenu, QAction

from asistente_ladm_col.config.table_mapping_config import PARCEL_NUMBER_FIELD, PLOT_TABLE, PARCEL_TABLE, \
    UEBAUNIT_TABLE, ID_FIELD
from asistente_ladm_col.utils import get_ui_class

WIDGET_UI = get_ui_class('change_detection/changes_all_parcels_panel_widget.ui')
PARCEL_STATUS = '_PARCEL_STATUS_'
CHANGE_DETECTION_NEW_PARCEL = 'Alta'
CHANGE_DETECTION_PARCEL_CHANGED = 'Cambio'
CHANGE_DETECTION_PARCEL_REMAINS = 'OK'
CHANGE_DETECTION_SEVERAL_PARCELS = 'several'
STATUS_COLORS = {CHANGE_DETECTION_NEW_PARCEL: Qt.red,
                 CHANGE_DETECTION_PARCEL_CHANGED: Qt.red,
                 CHANGE_DETECTION_PARCEL_REMAINS: Qt.green,
                 CHANGE_DETECTION_SEVERAL_PARCELS: Qt.yellow}

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

        self.tbl_changes_all_parcels.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tbl_changes_all_parcels.customContextMenuRequested.connect(self.show_context_menu)

    def fill_table(self):
        compared_parcels_data = self.get_compared_parcels_data()

        self.tbl_changes_all_parcels.clearContents()
        self.tbl_changes_all_parcels.setRowCount(len(compared_parcels_data))
        self.tbl_changes_all_parcels.setSortingEnabled(False)

        for row, (parcel_number, parcel_attrs) in enumerate(compared_parcels_data.items()):
            item = QTableWidgetItem(parcel_number)
            item.setData(Qt.UserRole, parcel_attrs[ID_FIELD])
            self.tbl_changes_all_parcels.setItem(row, 0, item)

            item = QTableWidgetItem(parcel_attrs[PARCEL_STATUS])
            item.setData(Qt.UserRole, parcel_attrs[ID_FIELD])
            self.tbl_changes_all_parcels.setItem(row, 1, item)
            color = STATUS_COLORS[parcel_attrs[PARCEL_STATUS] if parcel_attrs[PARCEL_STATUS] in STATUS_COLORS else CHANGE_DETECTION_SEVERAL_PARCELS]
            self.tbl_changes_all_parcels.item(row, 1).setBackground(color)

        self.tbl_changes_all_parcels.setSortingEnabled(True)

    def get_compared_parcels_data(self):
        dict_collected_parcels = self.ladm_data.get_parcel_data_to_compare_changes(self._db, None)
        dict_official_parcels = self.ladm_data.get_parcel_data_to_compare_changes(self._official_db, None)

        dict_compared_parcel_data = dict()

        for collected_parcel_number, collected_attrs in dict_collected_parcels.items():
            dict_attrs_comparison = dict()

            # A parcel number has at least one dict of attributes (i.e., one feature)
            dict_attrs_comparison[PARCEL_NUMBER_FIELD] = collected_parcel_number
            dict_attrs_comparison[ID_FIELD] = [attr[ID_FIELD] for attr in collected_attrs]

            if len(collected_attrs) > 1:
                dict_attrs_comparison[PARCEL_STATUS] = "({})".format(len(collected_attrs))
            else:
                if not collected_parcel_number in dict_official_parcels:
                    dict_attrs_comparison[PARCEL_STATUS] = CHANGE_DETECTION_NEW_PARCEL
                else:
                    official_attrs = dict_official_parcels[collected_parcel_number]

                    del collected_attrs[0][ID_FIELD]
                    del official_attrs[0][ID_FIELD]
                    dict_attrs_comparison[PARCEL_STATUS] = CHANGE_DETECTION_PARCEL_REMAINS if collected_attrs[0] == official_attrs[0] else CHANGE_DETECTION_PARCEL_CHANGED

            dict_compared_parcel_data[collected_parcel_number] = dict_attrs_comparison

        return dict_compared_parcel_data

    def call_changes_per_parcel_panel(self, item):
        parcel_number = self.tbl_changes_all_parcels.item(item.row(), 0).text()
        self.changes_per_parcel_panel_requested.emit(parcel_number)

    def show_context_menu(self, point):
        table_widget = self.sender()
        item = table_widget.itemAt(point)

        context_menu = QMenu("Context menu")

        parcels_t_ids = item.data(Qt.UserRole)

        if parcels_t_ids is None:
            return

        res_layers=self.qgis_utils.get_layers(self._db, {
            PLOT_TABLE: {'name': PLOT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry},
            PARCEL_TABLE: {'name': PARCEL_TABLE, 'geometry': None},
            UEBAUNIT_TABLE: {'name': UEBAUNIT_TABLE, 'geometry': None}}, load=True, emit_map_freeze=False)

        plot_layer = res_layers[PLOT_TABLE]
        plot_layer.setSubsetString("")

        plot_ids = self.ladm_data.get_plots_related_to_parcels(self._db, parcels_t_ids, field_name=None, plot_layer=plot_layer, uebaunit_table=res_layers[UEBAUNIT_TABLE])

        if plot_ids:
            action_zoom = QAction(QCoreApplication.translate("ChangesAllParcelsPanelWidget", "Zoom to related plots"))
            action_zoom.triggered.connect(partial(self.zoom_to_features, plot_layer, plot_ids))
            context_menu.addAction(action_zoom)

        action_view_changes = QAction(QCoreApplication.translate("ChangesAllParcelsPanelWidget", "View changes for this parcel number"))
        action_view_changes.triggered.connect(partial(self.call_changes_per_parcel_panel, item))
        context_menu.addAction(action_view_changes)

        if context_menu.actions():
            context_menu.exec_(table_widget.mapToGlobal(point))

    def zoom_to_features(self, layer, ids=[], t_ids=[]):  # TODO move this to a proper utils class
        if t_ids:
            features = self.ladm_data.get_features_from_t_ids(layer, t_ids, True, True)
            for feature in features:
                ids.append(feature.id())

        self.iface.mapCanvas().zoomToFeatureIds(layer, ids)
        self.canvas.flashFeatureIds(layer,
                                    ids,
                                    QColor(255, 0, 0, 255),
                                    QColor(255, 0, 0, 0),
                                    flashes=1,
                                    duration=500)