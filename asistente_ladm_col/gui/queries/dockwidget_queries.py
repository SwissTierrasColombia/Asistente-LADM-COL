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
import webbrowser
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
from qgis.PyQt.QtNetwork import (QNetworkRequest, 
                                 QNetworkAccessManager)
from qgis.PyQt.QtWidgets import (QMenu, 
                                 QAction, 
                                 QApplication, 
                                 QLabel)
from qgis.core import (Qgis,
                       QgsFeature,
                       QgsFeatureRequest,
                       QgsExpression,
                       QgsVectorLayer)
from qgis.gui import (QgsDockWidget, 
                      QgsMapToolIdentifyFeature)

from asistente_ladm_col.config.config_db_supported import ConfigDBsSupported
from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.config.layer_config import LayerConfig
from asistente_ladm_col.config.general_config import (TEST_SERVER,
                                                      SUFFIX_GET_THUMBNAIL)

from asistente_ladm_col.utils import get_ui_class
from asistente_ladm_col.utils.utils import is_connected
from asistente_ladm_col.utils.qt_utils import (ProcessWithStatus,
                                               OverrideCursor)

from asistente_ladm_col.logic.ladm_col.tree_models import TreeModel

DOCKWIDGET_UI = get_ui_class('dockwidgets/dockwidget_queries.ui')


class DockWidgetQueries(QgsDockWidget, DOCKWIDGET_UI):

    zoom_to_features_requested = pyqtSignal(QgsVectorLayer, list, dict, int)  # layer, ids, t_ids, duration

    def __init__(self, iface, db, ladm_data, parent=None):
        super(DockWidgetQueries, self).__init__(None)
        self.setupUi(self)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.iface = iface
        self._db = db
        self.ladm_data = ladm_data
        self.logger = Logger()

        self.app = AppInterface()

        self.canvas = iface.mapCanvas()
        self.active_map_tool_before_custom = None
        self.names = self._db.names

        self._ladm_queries = ConfigDBsSupported().get_db_factory(self._db.engine).get_ladm_queries()

        self.clipboard = QApplication.clipboard()

        # Required layers
        self.restart_dict_of_layers()

        self._identify_tool = None

        self.add_layers()
        self.fill_combos()

        self.btn_identify_plot.setIcon(QIcon(":/Asistente-LADM-COL/resources/images/spatial_unit.png"))

        # Set connections
        self.btn_alphanumeric_query.clicked.connect(self.alphanumeric_query)
        self.cbo_parcel_fields.currentIndexChanged.connect(self.search_field_updated)
        self.btn_identify_plot.clicked.connect(self.btn_plot_toggled)

        # Context menu
        self._set_context_menus()

        # Create maptool
        self.maptool_identify = QgsMapToolIdentifyFeature(self.canvas)

        self.initialize_field_values_line_edit()

    def search_field_updated(self, index=None):
        self.initialize_field_values_line_edit()

    def initialize_field_values_line_edit(self):
        self.txt_alphanumeric_query.setLayer(self._layers[self.names.OP_PARCEL_T])
        idx = self._layers[self.names.OP_PARCEL_T].fields().indexOf(self.cbo_parcel_fields.currentData())
        self.txt_alphanumeric_query.setAttributeIndex(idx)

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

    def restart_dict_of_layers(self):
        self._layers = {
            self.names.OP_PLOT_T: None,
            self.names.OP_PARCEL_T: None,
            self.names.COL_UE_BAUNIT_T: None
        }

    def add_layers(self):
        self.app.core.get_layers(self._db, self._layers, load=True)
        if not self._layers:
            self.restart_dict_of_layers()  # Let it ready for the next call
            return None

        # Layer was found, listen to its removal so that we can deactivate the custom tool when that occurs
        try:
            self._layers[self.names.OP_PLOT_T].willBeDeleted.disconnect(self.layer_removed)
        except TypeError as e:
            pass
        self._layers[self.names.OP_PLOT_T].willBeDeleted.connect(self.layer_removed)

        # Layer was found, listen to its removal so that we can update the variable properly
        try:
            self._layers[self.names.OP_PARCEL_T].willBeDeleted.disconnect(self.parcel_layer_removed)
        except TypeError as e:
            pass
        self._layers[self.names.OP_PARCEL_T].willBeDeleted.connect(self.parcel_layer_removed)

        # Layer was found, listen to its removal so that we can update the variable properly
        try:
            self._layers[self.names.COL_UE_BAUNIT_T].willBeDeleted.disconnect(self.uebaunit_table_removed)
        except TypeError as e:
            pass
        self._layers[self.names.COL_UE_BAUNIT_T].willBeDeleted.connect(self.uebaunit_table_removed)

    def initialize_tool(self):
        self._layers[self.names.OP_PLOT_T] = None
        self.initialize_tools(new_tool=None, old_tool=self.maptool_identify)
        self.btn_plot_toggled()

    def update_db_connection(self, db, ladm_col_db, db_source):
        self.close_dock_widget()

    def close_dock_widget(self):

        try:
            self._layers[self.names.OP_PLOT_T].willBeDeleted.disconnect(self.layer_removed)
        except:
            pass

        try:
            self._layers[self.names.OP_PARCEL_T].willBeDeleted.disconnect(self.parcel_layer_removed)
        except:
            pass

        self.initialize_tool()
        self.close()  # The user needs to use the menus again, which will start everything from scratch

    def layer_removed(self):
        # The required layer was removed, deactivate custom tool and close dockwidget
        self.close_dock_widget()

    def parcel_layer_removed(self):
        self._layers[self.names.OP_PARCEL_T] = None

    def uebaunit_table_removed(self):
        self._layers[self.names.COL_UE_BAUNIT_T] = None

    def fill_combos(self):
        self.cbo_parcel_fields.clear()

        self.cbo_parcel_fields.addItem(QCoreApplication.translate("DockWidgetQueries", "Parcel Number"), self.names.OP_PARCEL_T_PARCEL_NUMBER_F)
        self.cbo_parcel_fields.addItem(QCoreApplication.translate("DockWidgetQueries", "Previous Parcel Number"), self.names.OP_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F)
        self.cbo_parcel_fields.addItem(QCoreApplication.translate("DockWidgetQueries", "Folio de Matrícula Inmobiliaria"), self.names.OP_PARCEL_T_FMI_F)

    def initialize_tools(self, new_tool, old_tool):
        if self.maptool_identify == old_tool:
            # custom identify was deactivated
            try:
                self.canvas.mapToolSet.disconnect(self.initialize_tools)
            except TypeError as e:
                pass
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

        self.btn_identify_plot.setChecked(True)

        self.canvas.mapToolSet.connect(self.initialize_tools)

        if self._layers[self.names.OP_PLOT_T] is None:
            self.add_layers()

        self.maptool_identify.setLayer(self._layers[self.names.OP_PLOT_T])
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
        plot_t_id = plot_feature[self.names.T_ID_F]
        self.canvas.flashFeatureIds(self._layers[self.names.OP_PLOT_T],
                                    [plot_feature.id()],
                                    QColor(255, 0, 0, 255),
                                    QColor(255, 0, 0, 0),
                                    flashes=1,
                                    duration=500)

        with OverrideCursor(Qt.WaitCursor):
            if not self.isVisible():
                self.show()

            self.search_data_by_component(plot_t_ids=[plot_t_id], zoom_and_select=False)
            self._layers[self.names.OP_PLOT_T].selectByIds([plot_feature.id()])

    def search_data_by_component(self, **kwargs):
        self._layers[self.names.OP_PLOT_T].removeSelection()

        # Read zoom_and_select parameter and remove it from kwargs
        bZoom = False
        if 'zoom_and_select' in kwargs:
            bZoom = kwargs['zoom_and_select']
            del kwargs['zoom_and_select']

        records = self._ladm_queries.get_igac_basic_info(self._db, **kwargs)
        self.setup_tree_view(self.tree_view_basic, records)

        if bZoom:
            # Zoom to resulting plots
            plot_t_ids = self.get_plot_t_ids_from_basic_info(records)
            if plot_t_ids:
                features = self.ladm_data.get_features_from_t_ids(self._layers[self.names.OP_PLOT_T], self.names.T_ID_F, plot_t_ids, True, True)
                plot_ids = [feature.id() for feature in features]
                self.zoom_to_features_requested.emit(self._layers[self.names.OP_PLOT_T], plot_ids, dict(), 500)
                self._layers[self.names.OP_PLOT_T].selectByIds(plot_ids)

        records = self._ladm_queries.get_igac_legal_info(self._db, **kwargs)
        self.setup_tree_view(self.tree_view_legal, records)

        records = self._ladm_queries.get_igac_property_record_card_info(self._db, **kwargs)
        self.setup_tree_view(self.tree_view_property_record_card, records)

        records = self._ladm_queries.get_igac_physical_info(self._db, **kwargs)
        self.setup_tree_view(self.tree_view_physical, records)

        records = self._ladm_queries.get_igac_economic_info(self._db, **kwargs)
        self.setup_tree_view(self.tree_view_economic, records)

    def setup_tree_view(self, tree_view, records):
        """
        Configure result tree views

        :param tree_view:
        :return:
        """
        tree_view.setModel(TreeModel(self.names, data=records))
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

        :param model:
        :return:
        """
        model = tree_view.model()
        for idx in model.getPixmapIndexList():
            url = model.data(idx, Qt.UserRole)['url']
            res, image = self.download_image("{}{}".format(url, SUFFIX_GET_THUMBNAIL))
            if res:
                pixmap = QPixmap()
                pixmap.loadFromData(image)
                label = QLabel()
                label.setPixmap(pixmap)
                tree_view.setIndexWidget(idx, label)

    def get_plot_t_ids_from_basic_info(self, records):
        res = []
        if records:
            if self.names.OP_PLOT_T in records:
                for element in records[self.names.OP_PLOT_T]:
                    res.append(element['id'])

        return res

    def alphanumeric_query(self):
        """
        Alphanumeric query
        """
        option = self.cbo_parcel_fields.currentData()
        query = self.txt_alphanumeric_query.value()
        if query:
            if option == self.names.OP_PARCEL_T_FMI_F:
                self.search_data_by_component(parcel_fmi=query, zoom_and_select=True)
            elif option == self.names.OP_PARCEL_T_PARCEL_NUMBER_F:
                self.search_data_by_component(parcel_number=query, zoom_and_select=True)
            else: # previous_parcel_number
                self.search_data_by_component(previous_parcel_number=query, zoom_and_select=True)
        else:
            self.iface.messageBar().pushMessage("Asistente LADM-COL",
                QCoreApplication.translate("DockWidgetQueries", "First enter a query"))

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

        if "url" in index_data:
            action_open_url = QAction(QCoreApplication.translate("DockWidgetQueries", "Open URL"))
            action_open_url.triggered.connect(partial(self.open_url, index_data["url"]))
            context_menu.addAction(action_open_url)
            context_menu.addSeparator()

        # Configure actions for tables/layers
        if "type" in index_data and "id" in index_data:
            table_name = index_data["type"]
            table_package = LayerConfig.get_dict_table_package(self.names)
            t_id = index_data["id"]

            if table_name == self.names.OP_PARCEL_T:
                if self._layers[self.names.OP_PARCEL_T] is None or self._layers[self.names.OP_PLOT_T] is None or self._layers[self.names.COL_UE_BAUNIT_T] is None:
                    self.add_layers()
                layer = self._layers[self.names.OP_PARCEL_T]
                self.iface.layerTreeView().setCurrentLayer(layer)
            else:
                layer = self.app.core.get_layer(self._db, table_name, True)

            if layer is not None:
                if layer.isSpatial():
                    action_zoom_to_feature = QAction(QCoreApplication.translate("DockWidgetQueries", "Zoom to {} with {}={}").format(table_name, self.names.T_ID_F, t_id))
                    action_zoom_to_feature.triggered.connect(partial(self.zoom_to_feature, layer, t_id))
                    context_menu.addAction(action_zoom_to_feature)

                if table_name == self.names.OP_PARCEL_T:
                    # We show a handy option to zoom to related plots
                    plot_ids = self.ladm_data.get_plots_related_to_parcels(self._db, [t_id], None, self._layers[self.names.OP_PLOT_T], self._layers[self.names.COL_UE_BAUNIT_T])
                    if plot_ids:
                        action_zoom_to_plots = QAction(QCoreApplication.translate("DockWidgetQueries", "Zoom to related plot(s)"))
                        action_zoom_to_plots.triggered.connect(partial(self.zoom_to_plots, plot_ids))
                        context_menu.addAction(action_zoom_to_plots)

                action_open_feature_form = QAction(QCoreApplication.translate("DockWidgetQueries", "Open form for {} with {}={}").format(table_name, self.names.T_ID_F, t_id))
                action_open_feature_form.triggered.connect(partial(self.open_feature_form, layer, t_id))
                context_menu.addAction(action_open_feature_form)

        if context_menu.actions():
            context_menu.exec_(tree_view.mapToGlobal(point))

    def copy_value(self, value):
        self.clipboard.setText(str(value))

    def open_url(self, url):
        webbrowser.open(url)

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
        field_idx = layer.fields().indexFromName(self.names.T_ID_F)
        request = QgsFeatureRequest(QgsExpression("{}={}".format(self.names.T_ID_F, t_id)))
        request.setFlags(QgsFeatureRequest.NoGeometry)

        iterator = layer.getFeatures(request)
        feature = QgsFeature()
        res = iterator.nextFeature(feature)
        if res:
            return feature

        return None

    def zoom_to_plots(self, plot_ids):
        self.iface.mapCanvas().zoomToFeatureIds(self._layers[self.names.OP_PLOT_T], plot_ids)
        self.canvas.flashFeatureIds(self._layers[self.names.OP_PLOT_T],
                                    plot_ids,
                                    QColor(255, 0, 0, 255),
                                    QColor(255, 0, 0, 0),
                                    flashes=1,
                                    duration=500)

    def closeEvent(self, event):
        try:
            self.canvas.mapToolSet.disconnect(self.initialize_tools)
        except TypeError as e:
            pass
        self.canvas.setMapTool(self.active_map_tool_before_custom)

    def download_image(self, url):
        res = False
        img = None
        msg = {'text': '', 'level': Qgis.Warning}
        if url:
            self.logger.info(__name__, "Downloading file from {}".format(url))
            msg = "Downloading image from document repository (this might take a while)..."
            with ProcessWithStatus(msg):
                if is_connected(TEST_SERVER):

                    nam = QNetworkAccessManager()
                    request = QNetworkRequest(QUrl(url))
                    reply = nam.get(request)

                    loop = QEventLoop()
                    reply.finished.connect(loop.quit)
                    loop.exec_()

                    status = reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)
                    if status == 200:
                        res = True
                        img = reply.readAll()
                    else:
                        res = False
                        msg['text'] = QCoreApplication.translate("SettingsDialog",
                            "There was a problem connecting to the server. The server might be down or the service cannot be reached at the given URL.")
                else:
                    res = False
                    msg['text'] = QCoreApplication.translate("SettingsDialog",
                        "There was a problem connecting to Internet.")

        else:
            res = False
            msg['text'] = QCoreApplication.translate("SettingsDialog", "Not valid URL")

        if not res:
            self.logger.log_message(__name__, msg['text'], msg['level'])
        return (res, img)
