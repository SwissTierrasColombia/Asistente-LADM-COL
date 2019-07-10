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

from PyQt5.QtCore import (QCoreApplication,
                          Qt)
from PyQt5.QtGui import (QColor,
                         QIcon,
                         QCursor)
from PyQt5.QtWidgets import (QMenu,
                             QAction,
                             QApplication)
from qgis.core import (QgsWkbTypes,
                       QgsFeature,
                       QgsFeatureRequest,
                       QgsExpression)
from qgis.gui import (QgsDockWidget,
                      QgsMapToolIdentifyFeature)

from ..config.general_config import LAYER
from ..config.table_mapping_config import (PLOT_TABLE,
                                           UEBAUNIT_TABLE,
                                           PARCEL_TABLE,
                                           ID_FIELD,
                                           DICT_TABLE_PACKAGE,
                                           SPATIAL_UNIT_PACKAGE)

from ..utils import get_ui_class
from ..utils.qt_utils import OverrideCursor

from ..data.tree_models import TreeModel

DOCKWIDGET_UI = get_ui_class('dockwidget_queries.ui')


class DockWidgetQueries(QgsDockWidget, DOCKWIDGET_UI):
    def __init__(self, iface, db, qgis_utils, ladm_data, parent=None):
        super(DockWidgetQueries, self).__init__(None)
        self.setupUi(self)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.iface = iface
        self.canvas = iface.mapCanvas()
        self._db = db
        self.qgis_utils = qgis_utils
        self.ladm_data = ladm_data
        self.selection_color = None
        self.active_map_tool_before_custom = None

        self.clipboard = QApplication.clipboard()

        # Required layers
        self._layers = {
            PLOT_TABLE: {'name': PLOT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            PARCEL_TABLE: {'name': PARCEL_TABLE, 'geometry': None, LAYER: None},
            UEBAUNIT_TABLE: {'name': UEBAUNIT_TABLE, 'geometry': None, LAYER: None}
        }

        self._identify_tool = None

        self.add_layers()
        self.fill_combos()

        self.btn_identify_plot.setIcon(QIcon(":/Asistente-LADM_COL/resources/images/spatial_unit.png"))

        # Set connections
        self.btn_alphanumeric_query.clicked.connect(self.alphanumeric_query)
        self.btn_clear_alphanumeric_query.clicked.connect(self.clear_alphanumeric_query)
        self.btn_identify_plot.clicked.connect(self.btn_plot_toggled)

        # Context menu
        self._set_context_menus()

        # Create maptool
        self.maptool_identify = QgsMapToolIdentifyFeature(self.canvas)

    def _set_context_menus(self):
        self.tree_view_basic.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_view_basic.customContextMenuRequested.connect(self.show_context_menu)

        self.tree_view_legal.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_view_legal.customContextMenuRequested.connect(self.show_context_menu)

        self.tree_view_property_record_card.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_view_property_record_card.customContextMenuRequested.connect(self.show_context_menu)

        self.tree_view_physical.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_view_physical.customContextMenuRequested.connect(self.show_context_menu)

        self.tree_view_economic.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_view_economic.customContextMenuRequested.connect(self.show_context_menu)

    def add_layers(self):
        self.qgis_utils.get_layers(self._db, self._layers, load=True)
        if not self._layers:

            # Restart dictionary It is necessary
            self._layers = {
                PLOT_TABLE: {'name': PLOT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
                PARCEL_TABLE: {'name': PARCEL_TABLE, 'geometry': None, LAYER: None},
                UEBAUNIT_TABLE: {'name': UEBAUNIT_TABLE, 'geometry': None, LAYER: None}
            }

            return None

        # Layer was found, listen to its removal so that we can deactivate the custom tool when that occurs
        try:
            self._layers[PLOT_TABLE][LAYER].willBeDeleted.disconnect(self.layer_removed)
        except TypeError as e:
            pass
        self._layers[PLOT_TABLE][LAYER].willBeDeleted.connect(self.layer_removed)

        # Layer was found, listen to its removal so that we can update the variable properly
        try:
            self._layers[PARCEL_TABLE][LAYER].willBeDeleted.disconnect(self.parcel_layer_removed)
        except TypeError as e:
            pass
        self._layers[PARCEL_TABLE][LAYER].willBeDeleted.connect(self.parcel_layer_removed)

        # Layer was found, listen to its removal so that we can update the variable properly
        try:
            self._layers[UEBAUNIT_TABLE][LAYER].willBeDeleted.disconnect(self.uebaunit_table_removed)
        except TypeError as e:
            pass
        self._layers[UEBAUNIT_TABLE][LAYER].willBeDeleted.connect(self.uebaunit_table_removed)

    def initialize_tool(self):
        self._layers[PLOT_TABLE][LAYER] = None
        self.initialize_tools(new_tool=None, old_tool=self.maptool_identify)
        self.btn_plot_toggled()

    def update_db_connection(self, db, ladm_col_db):
        self._db = db
        self.initialize_tool()

        if not ladm_col_db:
            self.setVisible(False)

    def layer_removed(self):
        # The required layer was removed, deactivate custom tool
        self.initialize_tool()

    def parcel_layer_removed(self):
        self._layers[PARCEL_TABLE][LAYER] = None

    def uebaunit_table_removed(self):
        self._layers[UEBAUNIT_TABLE][LAYER] = None

    def fill_combos(self):
        self.cbo_parcel_fields.clear()

        if self._layers[PARCEL_TABLE][LAYER] is not None:
            self.cbo_parcel_fields.addItem(QCoreApplication.translate("DockWidgetQueries", "Parcel Number"), 'parcel_number')
            self.cbo_parcel_fields.addItem(QCoreApplication.translate("DockWidgetQueries", "Previous Parcel Number"), 'previous_parcel_number')
            self.cbo_parcel_fields.addItem(QCoreApplication.translate("DockWidgetQueries", "Folio de Matrícula Inmobiliaria"), 'fmi')
        else:
            self.add_layers()

    def initialize_tools(self, new_tool, old_tool):
        if self.maptool_identify == old_tool:
            # custom identify was deactivated
            try:
                self.canvas.mapToolSet.disconnect(self.initialize_tools)
            except TypeError as e:
                pass

            if self.selection_color is not None:
                self.canvas.setSelectionColor(self.selection_color) # Original selection color set in QGIS

            self.btn_identify_plot.setChecked(False)
        else:
            # custom identify was activated
            pass

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

        if self._layers[PLOT_TABLE][LAYER] is None:
            self.add_layers()

        self.maptool_identify.setLayer(self._layers[PLOT_TABLE][LAYER])
        cursor = QCursor()
        cursor.setShape(Qt.PointingHandCursor)
        self.maptool_identify.setCursor(cursor)
        self.canvas.setMapTool(self.maptool_identify)

        try:
            self.maptool_identify.featureIdentified.disconnect()
        except TypeError as e:
            pass
        self.maptool_identify.featureIdentified.connect(self.get_info_by_plot)

    def get_info_by_plot(self, plot_feature):
        plot_t_id = plot_feature[ID_FIELD]
        self.canvas.flashFeatureIds(self._layers[PLOT_TABLE][LAYER],
                                    [plot_feature.id()],
                                    QColor(255, 0, 0, 255),
                                    QColor(255, 0, 0, 0),
                                    flashes=1,
                                    duration=500)

        with OverrideCursor(Qt.WaitCursor):
            self._layers[PLOT_TABLE][LAYER].selectByIds([plot_feature.id()])
            if not self.isVisible():
                self.show()

            self.search_data_by_component(plot_t_id=plot_t_id)

    def search_data_by_component(self, **kwargs):
        records = self._db.get_igac_basic_info(**kwargs)
        self.tree_view_basic.setModel(TreeModel(data=records))
        self.tree_view_basic.expandAll()

        records = self._db.get_igac_legal_info(**kwargs)
        self.tree_view_legal.setModel(TreeModel(data=records))
        self.tree_view_legal.expandAll()

        records = self._db.get_igac_property_record_card_info(**kwargs)
        self.tree_view_property_record_card.setModel(TreeModel(data=records))
        self.tree_view_property_record_card.expandAll()

        records = self._db.get_igac_physical_info(**kwargs)
        self.tree_view_physical.setModel(TreeModel(data=records))
        self.tree_view_physical.expandAll()

        records = self._db.get_igac_economic_info(**kwargs)
        self.tree_view_economic.setModel(TreeModel(data=records))
        self.tree_view_economic.expandAll()

    def alphanumeric_query(self):
        """
        Alphanumeric query
        """
        option = self.cbo_parcel_fields.currentData()
        query = self.txt_alphanumeric_query.text().strip()
        if query:
            if option == 'fmi':
                self.search_data_by_component(parcel_fmi=query)
            elif option == 'parcel_number':
                self.search_data_by_component(parcel_number=query)
            else: # previous_parcel_number
                self.search_data_by_component(previous_parcel_number=query)

        else:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                QCoreApplication.translate("DockWidgetQueries", "First enter a query"))

    def clear_alphanumeric_query(self):
        self.txt_alphanumeric_query.setText('')

    def show_context_menu(self, point):
        tree_view = self.sender()
        index = tree_view.indexAt(point)

        context_menu = QMenu("Context menu")

        index_data = index.data(Qt.UserRole)

        if index_data is None:
            return

        if "value" in index_data:
            action_copy = QAction(QCoreApplication.translate("DockWidgetQueries", "Copy value"))
            action_copy.triggered.connect(partial(self.copy_value, index_data["value"]))
            context_menu.addAction(action_copy)
            context_menu.addSeparator()

        # Configure actions for tables/layers
        if "type" in index_data and "id" in index_data:
            table_name = index_data["type"]
            t_id = index_data["id"]
            geometry_type = None
            if table_name in DICT_TABLE_PACKAGE and DICT_TABLE_PACKAGE[table_name] == SPATIAL_UNIT_PACKAGE:
                # Layers in Spatial Unit package have double geometry, we need the polygon one
                geometry_type=QgsWkbTypes.PolygonGeometry

            if table_name == PARCEL_TABLE:
                if self._layers[PARCEL_TABLE][LAYER] is None or self._layers[PLOT_TABLE][LAYER] is None or self._layers[UEBAUNIT_TABLE][LAYER] is None:
                    self.add_layers()
                layer = self._layers[PARCEL_TABLE][LAYER]
                self.iface.layerTreeView().setCurrentLayer(layer)
            else:
                layer = self.qgis_utils.get_layer(self._db, table_name, geometry_type, True)

            if layer is not None:
                if layer.isSpatial():
                    action_zoom_to_feature = QAction(QCoreApplication.translate("DockWidgetQueries", "Zoom to {} with {}={}").format(table_name, ID_FIELD, t_id))
                    action_zoom_to_feature.triggered.connect(partial(self.zoom_to_feature, layer, t_id))
                    context_menu.addAction(action_zoom_to_feature)

                if table_name == PARCEL_TABLE:
                    # We show a handy option to zoom to related plots
                    plot_ids = self.ladm_data.get_plots_related_to_parcel(self._db, t_id, None, self._layers[PLOT_TABLE][LAYER], self._layers[UEBAUNIT_TABLE][LAYER])
                    if plot_ids:
                        action_zoom_to_plots = QAction(QCoreApplication.translate("DockWidgetQueries", "Zoom to related plot(s)"))
                        action_zoom_to_plots.triggered.connect(partial(self.zoom_to_plots, plot_ids))
                        context_menu.addAction(action_zoom_to_plots)

                action_open_feature_form = QAction(QCoreApplication.translate("DockWidgetQueries", "Open form for {} with {}={}").format(table_name, ID_FIELD, t_id))
                action_open_feature_form.triggered.connect(partial(self.open_feature_form, layer, t_id))
                context_menu.addAction(action_open_feature_form)

        if context_menu.actions():
            context_menu.exec_(tree_view.mapToGlobal(point))

    def copy_value(self, value):
        self.clipboard.setText(str(value))

    def zoom_to_feature(self, layer, t_id):
        feature = self.get_feature_from_t_id(layer, t_id)
        self.iface.mapCanvas().zoomToFeatureIds(layer, [feature.id()])
        self.canvas.flashFeatureIds(layer,
                                    [feature.id()],
                                    QColor(255, 0, 0, 255),
                                    QColor(255, 0, 0, 0),
                                    flashes=1,
                                    duration=500)

    def open_feature_form(self, layer, t_id):
        feature = self.get_feature_from_t_id(layer, t_id)
        self.iface.openFeatureForm(layer, feature)

    def get_feature_from_t_id(self, layer, t_id):
        field_idx = layer.fields().indexFromName(ID_FIELD)
        request = QgsFeatureRequest(QgsExpression("{}={}".format(ID_FIELD, t_id))).setSubsetOfAttributes([field_idx])
        request.setFlags(QgsFeatureRequest.NoGeometry)

        iterator = layer.getFeatures(request)
        feature = QgsFeature()
        res = iterator.nextFeature(feature)
        if res:
            return feature

        return None

    def zoom_to_plots(self, plot_ids):
        self.iface.mapCanvas().zoomToFeatureIds(self._layers[PLOT_TABLE][LAYER], plot_ids)
        self.canvas.flashFeatureIds(self._layers[PLOT_TABLE][LAYER],
                                    plot_ids,
                                    QColor(255, 0, 0, 255),
                                    QColor(255, 0, 0, 0),
                                    flashes=1,
                                    duration=500)
