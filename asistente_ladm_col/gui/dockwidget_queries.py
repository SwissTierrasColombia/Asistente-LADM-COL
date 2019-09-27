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
                              QEventLoop, 
                              QTextStream, 
                              QIODevice)
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
from qgis.core import (QgsWkbTypes,
                       Qgis,
                       QgsMessageLog,
                       QgsFeature,
                       QgsFeatureRequest,
                       QgsExpression,
                       QgsVectorLayer,
                       QgsApplication)
from qgis.gui import (QgsDockWidget, 
                      QgsMapToolIdentifyFeature)

from asistente_ladm_col.config.general_config import TEST_SERVER, PLUGIN_NAME, LAYER, SUFFIX_GET_THUMBNAIL
from ..config.table_mapping_config import (DICT_TABLE_PACKAGE,
                                           SPATIAL_UNIT_PACKAGE,
                                           PARCEL_NUMBER_FIELD,
                                           PARCEL_NUMBER_BEFORE_FIELD,
                                           FMI_FIELD,
                                           ID_FIELD,
                                           PARCEL_TABLE,
                                           PLOT_TABLE,
                                           UEBAUNIT_TABLE)

from ..utils import get_ui_class
from ..utils.qt_utils import OverrideCursor

from ..data.tree_models import TreeModel

DOCKWIDGET_UI = get_ui_class('dockwidgets/dockwidget_queries.ui')


class DockWidgetQueries(QgsDockWidget, DOCKWIDGET_UI):

    zoom_to_features_requested = pyqtSignal(QgsVectorLayer, list, list, int)  # layer, ids, t_ids, duration

    def __init__(self, iface, db, qgis_utils, ladm_data, parent=None):
        super(DockWidgetQueries, self).__init__(None)
        self.setupUi(self)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.iface = iface
        self.log = QgsApplication.messageLog()
        self.canvas = iface.mapCanvas()
        self._db = db
        self.qgis_utils = qgis_utils
        self.ladm_data = ladm_data
        self.active_map_tool_before_custom = None

        self.clipboard = QApplication.clipboard()

        # Required layers
        self.restart_dict_of_layers()

        self._identify_tool = None

        self.add_layers()
        self.fill_combos()

        self.btn_identify_plot.setIcon(QIcon(":/Asistente-LADM_COL/resources/images/spatial_unit.png"))

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
        self.txt_alphanumeric_query.setLayer(self._layers[PARCEL_TABLE][LAYER])
        idx = self._layers[PARCEL_TABLE][LAYER].fields().indexOf(self.cbo_parcel_fields.currentData())
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
            PLOT_TABLE: {'name': PLOT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            PARCEL_TABLE: {'name': PARCEL_TABLE, 'geometry': None, LAYER: None},
            UEBAUNIT_TABLE: {'name': UEBAUNIT_TABLE, 'geometry': None, LAYER: None}
        }

    def add_layers(self):
        self.qgis_utils.get_layers(self._db, self._layers, load=True)
        if not self._layers:
            self.restart_dict_of_layers()  # Let it ready for the next call
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

        self.cbo_parcel_fields.addItem(QCoreApplication.translate("DockWidgetQueries", "Parcel Number"), PARCEL_NUMBER_FIELD)
        self.cbo_parcel_fields.addItem(QCoreApplication.translate("DockWidgetQueries", "Previous Parcel Number"), PARCEL_NUMBER_BEFORE_FIELD)
        self.cbo_parcel_fields.addItem(QCoreApplication.translate("DockWidgetQueries", "Folio de Matrícula Inmobiliaria"), FMI_FIELD)

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
            if not self.isVisible():
                self.show()

            self.search_data_by_component(plot_t_id=plot_t_id, zoom_and_select=False)
            self._layers[PLOT_TABLE][LAYER].selectByIds([plot_feature.id()])

    def search_data_by_component(self, **kwargs):
        self._layers[PLOT_TABLE][LAYER].removeSelection()

        # Read zoom_and_select parameter and remove it from kwargs
        bZoom = False
        if 'zoom_and_select' in kwargs:
            bZoom = kwargs['zoom_and_select']
            del kwargs['zoom_and_select']

        records = self._db.get_igac_basic_info(**kwargs)
        self.setup_tree_view(self.tree_view_basic, records)

        if bZoom:
            # Zoom to resulting plots
            plot_t_ids = self.get_plot_t_ids_from_basic_info(records)
            if plot_t_ids:
                features = self.ladm_data.get_features_from_t_ids(self._layers[PLOT_TABLE][LAYER], plot_t_ids, True, True)
                plot_ids = [feature.id() for feature in features]
                self.zoom_to_features_requested.emit(self._layers[PLOT_TABLE][LAYER], plot_ids, list(), 500)
                self._layers[PLOT_TABLE][LAYER].selectByIds(plot_ids)

        records = self._db.get_igac_legal_info(**kwargs)
        self.setup_tree_view(self.tree_view_legal, records)

        records = self._db.get_igac_property_record_card_info(**kwargs)
        self.setup_tree_view(self.tree_view_property_record_card, records)

        records = self._db.get_igac_physical_info(**kwargs)
        self.setup_tree_view(self.tree_view_physical, records)

        records = self._db.get_igac_economic_info(**kwargs)
        self.setup_tree_view(self.tree_view_economic, records)

    def setup_tree_view(self, tree_view, records):
        """
        Configure result tree views

        :param tree_view:
        :return:
        """
        tree_view.setModel(TreeModel(data=records))
        tree_view.expandAll()
        self.add_thumbnails_to_tree_view(tree_view)

    def add_thumbnails_to_tree_view(self, tree_view):
        """
        Gets a list of model indexes corresponding to extFiles objects to show a preview

        :param model:
        :return:
        """
        model = tree_view.model()
        indexes = model.getPixmapIndexList()
        for idx in indexes:
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
            for record in records:
                if PLOT_TABLE in record:
                    for element in record[PLOT_TABLE]:
                        res.append(element['id'])

        return res

    def alphanumeric_query(self):
        """
        Alphanumeric query
        """
        option = self.cbo_parcel_fields.currentData()
        query = self.txt_alphanumeric_query.value()
        if query:
            if option == FMI_FIELD:
                self.search_data_by_component(parcel_fmi=query, zoom_and_select=True)
            elif option == PARCEL_NUMBER_FIELD:
                self.search_data_by_component(parcel_number=query, zoom_and_select=True)
            else: # previous_parcel_number
                self.search_data_by_component(previous_parcel_number=query, zoom_and_select=True)
        else:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
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
                    plot_ids = self.ladm_data.get_plots_related_to_parcels(self._db, [t_id], None, self._layers[PLOT_TABLE][LAYER], self._layers[UEBAUNIT_TABLE][LAYER])
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
        field_idx = layer.fields().indexFromName(ID_FIELD)
        request = QgsFeatureRequest(QgsExpression("{}={}".format(ID_FIELD, t_id)))
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
            self.log.logMessage("Downloading file from {}".format(url), PLUGIN_NAME, Qgis.Info)
            with OverrideCursor(Qt.WaitCursor):
                self.qgis_utils.status_bar_message_emitted.emit("Downloading image from document repository (this might take a while)...", 0)
                QCoreApplication.processEvents()
                if self.qgis_utils.is_connected(TEST_SERVER):

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

                self.qgis_utils.clear_status_bar_emitted.emit()
        else:
            res = False
            msg['text'] = QCoreApplication.translate("SettingsDialog", "Not valid URL")

        if not res:
            self.log.logMessage(msg['text'], PLUGIN_NAME, msg['level'])
        return (res, img)
