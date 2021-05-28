# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM-COL
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

from qgis.PyQt.QtCore import (QCoreApplication,
                              Qt, 
                              pyqtSignal, 
                              QUrl, 
                              QEventLoop)
from qgis.PyQt.QtGui import (QColor, 
                             QIcon, 
                             QCursor, 
                             QPixmap)
from qgis.PyQt.QtWidgets import (QMenu, 
                                 QAction, 
                                 QApplication, 
                                 QLabel)
from qgis.gui import (QgsDockWidget, 
                      QgsMapToolIdentifyFeature)

from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.config.general_config import SUFFIX_GET_THUMBNAIL

from asistente_ladm_col.utils import get_ui_class
from asistente_ladm_col.utils.qt_utils import OverrideCursor


DOCKWIDGET_UI = get_ui_class('dockwidgets/dockwidget_queries.ui')


class DockWidgetQueries(QgsDockWidget, DOCKWIDGET_UI):

    def __init__(self, iface, controller, parent=None):
        super(DockWidgetQueries, self).__init__(None)
        self.setupUi(self)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.iface = iface
        self._controller = controller

        self.logger = Logger()
        self.app = AppInterface()

        self.canvas = iface.mapCanvas()
        self.active_map_tool_before_custom = None

        self._identify_tool = None

        self._fill_combos()

        self.btn_identify_plot.setIcon(QIcon(":/Asistente-LADM-COL/resources/images/spatial_unit.png"))

        # Set connections
        self._controller.close_view_requested.connect(self._close_dock_widget)

        self.btn_alphanumeric_query.clicked.connect(self._alphanumeric_query)
        self.cbo_parcel_fields.currentIndexChanged.connect(self._search_field_updated)
        self.btn_identify_plot.clicked.connect(self._btn_plot_toggled)
        self.btn_query_informality.clicked.connect(self._query_informality)
        self.btn_next_informal_parcel.clicked.connect(self._query_next_informal_parcel)
        self.btn_previous_informal_parcel.clicked.connect(self._query_previous_informal_parcel)

        # Context menu
        self._set_context_menus()

        # Create maptool
        self.maptool_identify = QgsMapToolIdentifyFeature(self.canvas)

        self._initialize_field_values_line_edit()
        self._update_informal_controls()

    def _search_field_updated(self, index=None):
        self._initialize_field_values_line_edit()

    def _initialize_field_values_line_edit(self):
        self.txt_alphanumeric_query.setLayer(self._controller.parcel_layer())
        idx = self._controller.parcel_layer().fields().indexOf(self.cbo_parcel_fields.currentData())
        self.txt_alphanumeric_query.setAttributeIndex(idx)

    def _set_context_menus(self):
        self.tree_view_basic.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_view_basic.customContextMenuRequested.connect(self._show_context_menu)

        self.tree_view_legal.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_view_legal.customContextMenuRequested.connect(self._show_context_menu)

        self.tree_view_property_record_card.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_view_property_record_card.customContextMenuRequested.connect(self._show_context_menu)

        self.tree_view_physical.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_view_physical.customContextMenuRequested.connect(self._show_context_menu)

        self.tree_view_economic.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_view_economic.customContextMenuRequested.connect(self._show_context_menu)

    def _close_dock_widget(self):
        # Deactivate custom tool and close dockwidget
        self._controller.disconnect_plot_layer()
        self._controller.disconnect_parcel_layer()

        self._initialize_tools(new_tool=None, old_tool=self.maptool_identify)
        self._btn_plot_toggled()
        self.close()  # The user needs to use the menus again, which will start everything from scratch

    def _fill_combos(self):
        self.cbo_parcel_fields.clear()
        self.cbo_parcel_fields.addItem(QCoreApplication.translate("DockWidgetQueries", "Parcel Number"), self._controller.parcel_number_name())
        self.cbo_parcel_fields.addItem(QCoreApplication.translate("DockWidgetQueries", "Previous Parcel Number"), self._controller.previous_parcel_number_name())
        self.cbo_parcel_fields.addItem(QCoreApplication.translate("DockWidgetQueries", "Folio de Matrícula Inmobiliaria"), self._controller.fmi_name())

    def _initialize_tools(self, new_tool, old_tool):
        if self.maptool_identify == old_tool:
            # custom identify was deactivated
            try:
                self.canvas.mapToolSet.disconnect(self._initialize_tools)
            except TypeError as e:
                pass
            self.btn_identify_plot.setChecked(False)
        else:
            # custom identify was activated
            pass

    def _btn_plot_toggled(self):
        if self.btn_identify_plot.isChecked():
            self._prepare_identify_plot()
        else:
            # The button was toggled and deactivated, go back to the previous tool
            self.canvas.setMapTool(self.active_map_tool_before_custom)

    def _prepare_identify_plot(self):
        """
        Custom Identify tool was activated, prepare everything for identifying plots
        """
        self.active_map_tool_before_custom = self.canvas.mapTool()
        self.btn_identify_plot.setChecked(True)

        self.canvas.mapToolSet.connect(self._initialize_tools)

        self.maptool_identify.setLayer(self._controller.plot_layer())
        cursor = QCursor()
        cursor.setShape(Qt.PointingHandCursor)
        self.maptool_identify.setCursor(cursor)
        self.canvas.setMapTool(self.maptool_identify)

        try:
            self.maptool_identify.featureIdentified.disconnect()
        except TypeError as e:
            pass
        self.maptool_identify.featureIdentified.connect(self._search_data_by_plot)

    def _search_data_by_plot(self, plot_feature):
        plot_t_id = plot_feature[self._controller.t_id_name()]
        self.canvas.flashFeatureIds(self._controller.plot_layer(),
                                    [plot_feature.id()],
                                    QColor(255, 0, 0, 255),
                                    QColor(255, 0, 0, 0),
                                    flashes=1,
                                    duration=500)

        with OverrideCursor(Qt.WaitCursor):
            if not self.isVisible():
                self.show()

            self._search_data_by_component(plot_t_ids=[plot_t_id], zoom_and_select=False)
            self._controller.plot_layer().selectByIds([plot_feature.id()])

    def _search_data_by_component(self, **kwargs):
        """
        Perform the searches by component and fill tree views

        :param kwargs: A dict with search criteria.
        """
        self._controller.plot_layer().removeSelection()

        # Read zoom_and_select parameter and remove it from kwargs
        bZoom = False
        if 'zoom_and_select' in kwargs:
            bZoom = kwargs['zoom_and_select']
            del kwargs['zoom_and_select']

        records = self._controller.search_data_basic_info(**kwargs)
        if bZoom:
            self._controller.zoom_to_resulting_plots(records)

        self._setup_tree_view(self.tree_view_basic, records)

        records = self._controller.search_data_legal_info(**kwargs)
        self._setup_tree_view(self.tree_view_legal, records)

        records = self._controller.search_data_property_record_card_info(**kwargs)
        self._setup_tree_view(self.tree_view_property_record_card, records)

        records = self._controller.search_data_physical_info(**kwargs)
        self._setup_tree_view(self.tree_view_physical, records)

        records = self._controller.search_data_economic_info(**kwargs)
        self._setup_tree_view(self.tree_view_economic, records)

    def _setup_tree_view(self, tree_view, records):
        """
        Configure result tree views

        :param tree_view: Tree view to be updated
        :param records: List of dicts. A dict per plot: {id: 21, attributes: {...}}
        """
        tree_view.setModel(self._controller.create_model(records))
        self._collapse_tree_view_items(tree_view)
        self._add_thumbnails_to_tree_view(tree_view)

    def _collapse_tree_view_items(self, tree_view):
        """
        Collapse tree view items based on a property
        """
        tree_view.expandAll()
        for idx in tree_view.model().getCollapseIndexList():
            tree_view.collapse(idx)

    def _add_thumbnails_to_tree_view(self, tree_view):
        """
        Gets a list of model indexes corresponding to extFiles objects to show a preview
        """
        model = tree_view.model()
        for idx in model.getPixmapIndexList():
            url = model.data(idx, Qt.UserRole)['url']
            res, image = self._controller.download_image("{}{}".format(url, SUFFIX_GET_THUMBNAIL))
            if res:
                pixmap = QPixmap()
                pixmap.loadFromData(image)
                label = QLabel()
                label.setPixmap(pixmap)
                tree_view.setIndexWidget(idx, label)

    def _alphanumeric_query(self):
        option = self.cbo_parcel_fields.currentData()
        query = self.txt_alphanumeric_query.value()
        if query:
            if option == self._controller.fmi_name():
                self._search_data_by_component(parcel_fmi=query, zoom_and_select=True)
            elif option == self._controller.parcel_number_name():
                self._search_data_by_component(parcel_number=query, zoom_and_select=True)
            else: # previous_parcel_number
                self._search_data_by_component(previous_parcel_number=query, zoom_and_select=True)
        else:
            self.logger.info_msg(__name__, QCoreApplication.translate("DockWidgetQueries", "First enter a query"))

    def _show_context_menu(self, point):
        tree_view = self.sender()
        index = tree_view.indexAt(point)

        context_menu = QMenu("Context menu")

        index_data = index.data(Qt.UserRole)

        if index_data is None:
            return

        if "value" in index_data:
            action_copy = QAction(QCoreApplication.translate("DockWidgetQueries", "Copy value"))
            action_copy.triggered.connect(partial(self._controller.copy_value, index_data["value"]))
            context_menu.addAction(action_copy)
            context_menu.addSeparator()

        if "url" in index_data:
            action_open_url = QAction(QCoreApplication.translate("DockWidgetQueries", "Open URL"))
            action_open_url.triggered.connect(partial(self._controller.open_url, index_data["url"]))
            context_menu.addAction(action_open_url)
            context_menu.addSeparator()

        # Configure actions for tables/layers
        if "type" in index_data and "id" in index_data:
            table_name = index_data["type"]
            t_id = index_data["id"]

            if table_name == self._controller.parcel_layer_name():
                layer = self._controller.parcel_layer()
                self.app.core.activate_layer_requested.emit(layer)
            else:
                layer = self._controller.get_layer(table_name)

            if layer is not None:
                if layer.isSpatial():
                    action_zoom_to_feature = QAction(QCoreApplication.translate("DockWidgetQueries", "Zoom to {} with {}={}").format(table_name, self._controller.t_id_name(), t_id))
                    action_zoom_to_feature.triggered.connect(partial(self._controller.zoom_to_feature, layer, t_id))
                    context_menu.addAction(action_zoom_to_feature)

                if table_name == self._controller.parcel_layer_name():
                    # We show a handy option to zoom to related plots
                    plot_ids = self._controller.get_plots_related_to_parcel(t_id)
                    if plot_ids:
                        action_zoom_to_plots = QAction(QCoreApplication.translate("DockWidgetQueries", "Zoom to related plot(s)"))
                        action_zoom_to_plots.triggered.connect(partial(self._controller.zoom_to_plots, plot_ids))
                        context_menu.addAction(action_zoom_to_plots)

                action_open_feature_form = QAction(QCoreApplication.translate("DockWidgetQueries", "Open form for {} with {}={}").format(table_name, self._controller.t_id_name(), t_id))
                action_open_feature_form.triggered.connect(partial(self._controller.open_feature_form, layer, t_id))
                context_menu.addAction(action_open_feature_form)

        if context_menu.actions():
            context_menu.exec_(tree_view.mapToGlobal(point))

    def _query_informality(self):
        first_parcel_number, current, total = self._controller.query_informal_parcels()
        self._search_data_by_component(parcel_number=first_parcel_number, zoom_and_select=True)
        self._update_informal_controls(first_parcel_number, current, total)

        if not total:
            self.logger.info_msg(__name__,
                                 QCoreApplication.translate("DockWidgetQueries",
                                                            "There are no informal parcels in this database!"))

    def _update_informal_controls(self, parcel_number='', current=0, total=0):
        """
        Update controls (reset labels, enable buttons if we have informality)
        """
        self._update_informal_labels(parcel_number, current, total)
        self.btn_query_informality.setText(
            QCoreApplication.translate("DockWidgetQueries", "Restart") if current else QCoreApplication.translate("DockWidgetQueries", "Start"))

        enable = total > 1  # At least 2 to enable buttons that traverse the parcels
        self.btn_next_informal_parcel.setEnabled(enable)
        self.btn_previous_informal_parcel.setEnabled(enable)

    def _update_informal_labels(self, parcel_number='', current=0, total=0):
        self.lbl_informal_parcel_number.setText(parcel_number)
        out_of = ''
        if current and total:
            out_of = QCoreApplication.translate("DockWidgetQueries", "{} out of {}").format(current, total)
        self.lbl_informal_out_of_total.setText(out_of)

    def _query_next_informal_parcel(self):
        parcel_number, current, total = self._controller.get_next_informal_parcel()
        self._search_data_by_component(parcel_number=parcel_number, zoom_and_select=True)
        self._update_informal_controls(parcel_number, current, total)

    def _query_previous_informal_parcel(self):
        parcel_number, current, total = self._controller.get_previous_informal_parcel()
        self._search_data_by_component(parcel_number=parcel_number, zoom_and_select=True)
        self._update_informal_controls(parcel_number, current, total)

    def closeEvent(self, event):
        try:
            self.canvas.mapToolSet.disconnect(self._initialize_tools)
        except TypeError as e:
            pass
        self.canvas.setMapTool(self.active_map_tool_before_custom)
