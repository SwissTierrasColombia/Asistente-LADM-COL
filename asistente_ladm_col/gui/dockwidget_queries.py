# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2018-03-08
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
from functools import partial

from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QColor, QIcon, QCursor
from PyQt5.QtWidgets import QMenu, QAction, QApplication
from qgis.core import QgsWkbTypes, Qgis, QgsMessageLog
from qgis.gui import QgsDockWidget, QgsMapToolIdentifyFeature

from asistente_ladm_col.utils.qt_utils import OverrideCursor
from ..config.table_mapping_config import PLOT_TABLE, UEBAUNIT_TABLE, PARCEL_TABLE, ID_FIELD

from ..utils import get_ui_class

from ..data.tree_models import TreeModel

DOCKWIDGET_UI = get_ui_class('dockwidget_queries.ui')

class DockWidgetQueries(QgsDockWidget, DOCKWIDGET_UI):
    def __init__(self, iface, db, qgis_utils, parent=None):
        super(DockWidgetQueries, self).__init__(None)
        self.setupUi(self)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.iface = iface
        self.canvas = iface.mapCanvas()
        self._db = db
        self.qgis_utils = qgis_utils
        self.selection_color = None
        self.active_map_tool_before_custom = None

        self.clipboard = QApplication.clipboard()

        # Required layers
        self._plot_layer = None
        self._parcel_layer = None

        self._identify_tool = None

        self.add_layers()
        self.fill_combos()

        self.btn_identify_plot.setIcon(QIcon(":/Asistente-LADM_COL/resources/images/spatial_unit.png"))

        # Set connections
        self.btn_alphanumeric_query.clicked.connect(self.alphanumeric_query)
        self.btn_clear_alphanumeric_query.clicked.connect(self.clear_alphanumeric_query)
        self.btn_identify_plot.clicked.connect(self.btn_plot_toggled)

        # Context menu
        self.treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.show_context_menu)

        # Create maptool
        self.maptool_identify = QgsMapToolIdentifyFeature(self.canvas)

    def add_layers(self):
        res_layers = self.qgis_utils.get_layers(self._db, {
            PLOT_TABLE: {'name': PLOT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry},
            PARCEL_TABLE: {'name': PARCEL_TABLE, 'geometry': None},
            UEBAUNIT_TABLE: {'name': UEBAUNIT_TABLE, 'geometry': None}}, load=True)

        self._plot_layer = res_layers[PLOT_TABLE]
        if self._plot_layer is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                                QCoreApplication.translate("DockWidgetQueries",
                                                                           "Plot layer couldn't be found... {}").format(
                                                    self._db.get_description()),
                                                Qgis.Warning)
        else:
            # Layer was found, listen to its removal so that we can deactivate the custom tool when that occurs
            try:
                self._plot_layer.willBeDeleted.disconnect(self.layer_removed)
            except TypeError as e:
                pass
            self._plot_layer.willBeDeleted.connect(self.layer_removed)

        self._parcel_layer = res_layers[PARCEL_TABLE]
        if self._parcel_layer is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                                QCoreApplication.translate("DockWidgetQueries",
                                                                           "Parcel layer couldn't be found... {}").format(
                                                    self._db.get_description()),
                                                Qgis.Warning)
        else:
            # Layer was found, listen to its removal so that we can update the variable properly
            try:
                self._parcel_layer.willBeDeleted.disconnect(self.parcel_layer_removed)
            except TypeError as e:
                pass
            self._parcel_layer.willBeDeleted.connect(self.parcel_layer_removed)

    def initialize_tool(self):
        self._plot_layer = None
        self.initialize_tools(new_tool=None, old_tool=self.maptool_identify)
        self.btn_plot_toggled()

    def update_db_connection(self, db):
        self._db = db
        self.initialize_tool()

    def layer_removed(self):
        # The required layer was removed, deactivate custom tool
        self.initialize_tool()

    def parcel_layer_removed(self):
        self._parcel_layer = None

    def fill_combos(self):
        self.cbo_parcel_fields.clear()

        if self._parcel_layer is not None:
            self.cbo_parcel_fields.addItem('Número Predial', 'numero_predial')
            self.cbo_parcel_fields.addItem('Número Predial Anterior', 'numero_predial_anterior')
            self.cbo_parcel_fields.addItem('Folio de Matrícula Inmobiliaria', 'fmi')
        else:
            self.add_layers()

    def initialize_tools(self, new_tool, old_tool):
        if self.maptool_identify == old_tool:
            # custom identify was deactivated
            print("Before: custom tool...")
            try:
                self.canvas.mapToolSet.disconnect(self.initialize_tools)
            except TypeError as e:
                pass

            self.canvas.setSelectionColor(self.selection_color) # Original selection color set in QGIS

            self.btn_identify_plot.setChecked(False)
        else:
            # custom identify was activated
            print("Before: A QGIS tool...")

    def btn_plot_toggled(self):
        if self.btn_identify_plot.isChecked():
            self.prepare_identify_plot()
        else:
            # The button was toggled and deactivated, go back to the previous tool
            self.canvas.setMapTool(self.active_map_tool_before_custom)

    def prepare_identify_plot(self):
        """
            Custom Identify tool was activated, prepare everything for identifying plots
        """
        self.active_map_tool_before_custom = self.canvas.mapTool()
        self.selection_color = self.canvas.selectionColor()  # Probably QColor('#ffff00')

        self.btn_identify_plot.setChecked(True)

        self.canvas.mapToolSet.connect(self.initialize_tools)
        self.canvas.setSelectionColor(QColor("red"))

        if self._plot_layer is None:
            self.add_layers()

        self.maptool_identify.setLayer(self._plot_layer)
        cursor = QCursor()
        cursor.setShape(Qt.CrossCursor)
        self.maptool_identify.setCursor(cursor)
        self.canvas.setMapTool(self.maptool_identify)

        try:
            self.maptool_identify.featureIdentified.disconnect()
        except TypeError as e:
            pass
        self.maptool_identify.featureIdentified.connect(self.get_basic_info_by_plot)

    def get_basic_info_by_plot(self, plot_feature):
        plot_t_id = plot_feature[ID_FIELD]
        self.canvas.flashFeatureIds(self._plot_layer,
                                    [plot_feature.id()],
                                    QColor(255, 0, 0, 255),
                                    QColor(255, 0, 0, 0),
                                    flashes=1,
                                    duration=500)

        with OverrideCursor(Qt.WaitCursor):
            self._plot_layer.selectByIds([plot_feature.id()])
            records = self._db.get_igac_basic_info(plot_t_id)
            print(records)
            #data = {"t_id": plot_t_id, "records": records}
            self.treeModel = TreeModel(data=records)
            self.treeView.setModel(self.treeModel)
            self.treeView.expandAll()

    def alphanumeric_query(self):
        """
        Alphanumeric query
        """
        option = self.cbo_parcel_fields.currentData()
        query = self.txt_alphanumeric_query.text().strip()
        if query:
            if option == 'fmi':
                records = self._db.get_igac_basic_info(parcel_fmi=query)
            elif option == 'numero_predial':
                records = self._db.get_igac_basic_info(parcel_number=query)
            else: # previous_parcel_number
                records = self._db.get_igac_basic_info(previous_parcel_number=query)
            #data = {"t_id": query, "records": records}
            #print(records)
            self.treeModel = TreeModel(data=records)
            self.treeView.setModel(self.treeModel)
            self.treeView.expandAll()
        else:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                QCoreApplication.translate("DockWidgetQueries", "First enter a query"))

    def clear_alphanumeric_query(self):
        self.txt_alphanumeric_query.setText('')

    def show_context_menu(self, point):
        index = self.treeView.indexAt(point)

        context_menu = QMenu("Context menu")

        index_data = index.data(Qt.UserRole)
        if "value" in index_data:
            action_copy = QAction("Copy value")
            action_copy.triggered.connect(partial(self.copy_value, index_data["value"]))
            context_menu.addAction(action_copy)

        context_menu.exec_(self.treeView.mapToGlobal(point))

    def copy_value(self, value):
        print("{} copied!".format(value))
        self.clipboard.setText(str(value))