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
import qgis

from qgis.PyQt.QtGui import QColor, QMouseEvent
from qgis.PyQt.QtCore import QCoreApplication, Qt, QEvent, QPoint
from qgis.core import (QgsWkbTypes,
                       Qgis,
                       QgsMessageLog,
                       QgsFeature,
                       QgsFeatureRequest,
                       QgsExpression,
                       QgsRectangle)

from qgis.gui import QgsPanelWidget

from asistente_ladm_col.config.general_config import MAP_SWIPE_TOOL_PLUGIN_NAME
from asistente_ladm_col.config.table_mapping_config import (PLOT_TABLE,
                                                            PARCEL_TABLE,
                                                            UEBAUNIT_TABLE,
                                                            OFFICIAL_PLOT_TABLE,
                                                            OFFICIAL_PARCEL_TABLE,
                                                            PARCEL_NUMBER_FIELD,
                                                            PARCEL_NUMBER_BEFORE_FIELD,
                                                            FMI_FIELD,
                                                            ID_FIELD)
from asistente_ladm_col.utils import get_ui_class

WIDGET_UI = get_ui_class('change_detection/changes_per_parcel_panel_widget.ui')

class ChangesPerParcelPanelWidget(QgsPanelWidget, WIDGET_UI):
    def __init__(self, iface, db, official_db, qgis_utils, ladm_data, parcel_number=None):
        QgsPanelWidget.__init__(self, None)
        self.setupUi(self)
        self.iface = iface
        self.canvas = iface.mapCanvas()
        self._db = db
        self._official_db = official_db
        self.qgis_utils = qgis_utils
        self.ladm_data = ladm_data

        self.setDockMode(True)

        self.map_swipe_tool = qgis.utils.plugins[MAP_SWIPE_TOOL_PLUGIN_NAME]

        # Required layers
        self._plot_layer = None
        self._parcel_layer = None
        self._official_plot_layer = None
        self._official_parcel_layer = None

        self._current_official_substring = ""
        self._current_substring = ""

        self.add_layers()
        self.fill_combos()

        # Set connections
        self.btn_alphanumeric_query.clicked.connect(self.alphanumeric_query)
        self.chk_show_all_plots.toggled.connect(self.show_all_plots)
        self.cbo_parcel_fields.currentIndexChanged.connect(self.field_search_updated)

        self.initialize_field_values_line_edit()

        if parcel_number is not None:
            self.txt_alphanumeric_query.setValue(parcel_number)
            self.search_data(parcel_number= parcel_number)

    def add_layers(self):
        self.qgis_utils.map_freeze_requested.emit(True)

        # Load layers from the new BD
        res_layers = self.qgis_utils.get_layers(self._db, {
            PLOT_TABLE: {'name': PLOT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry},
            PARCEL_TABLE: {'name': PARCEL_TABLE, 'geometry': None},
            UEBAUNIT_TABLE: {'name': UEBAUNIT_TABLE, 'geometry': None}}, load=True, emit_map_freeze=False)

        self._plot_layer = res_layers[PLOT_TABLE]
        if self._plot_layer is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                                QCoreApplication.translate("DockWidgetChanges",
                                                                           "Plot layer couldn't be found... {}").format(
                                                    self._db.get_description()),
                                                Qgis.Warning)
            return
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
                                                QCoreApplication.translate("DockWidgetChanges",
                                                                           "Parcel layer couldn't be found... {}").format(
                                                    self._db.get_description()),
                                                Qgis.Warning)
            return
        else:
            # Layer was found, listen to its removal so that we can update the variable properly
            try:
                self._parcel_layer.willBeDeleted.disconnect(self.layer_removed)
            except TypeError as e:
                pass
            self._parcel_layer.willBeDeleted.connect(self.layer_removed)

        # Now load official layers
        res_layers = self.qgis_utils.get_layers(self._official_db, {
            PLOT_TABLE: {'name': PLOT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry},
            PARCEL_TABLE: {'name': PARCEL_TABLE, 'geometry': None}}, load=True, emit_map_freeze=False)

        self._official_plot_layer = res_layers[PLOT_TABLE]
        if self._official_plot_layer is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                                QCoreApplication.translate("DockWidgetChanges",
                                                                           "Plot layer couldn't be found... {}").format(
                                                    self._db.get_description()),
                                                Qgis.Warning)
            return
        else:
            self._official_plot_layer.setName(OFFICIAL_PLOT_TABLE)
            self.qgis_utils.symbology.set_layer_style_from_qml(self._official_plot_layer)

            # Layer was found, listen to its removal so that we can deactivate the custom tool when that occurs
            try:
                self._official_plot_layer.willBeDeleted.disconnect(self.layer_removed)
            except TypeError as e:
                pass
            self._official_plot_layer.willBeDeleted.connect(self.layer_removed)

        self._official_parcel_layer = res_layers[PARCEL_TABLE]
        if self._official_parcel_layer is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                                QCoreApplication.translate("DockWidgetChanges",
                                                                           "Parcel layer couldn't be found... {}").format(
                                                    self._db.get_description()),
                                                Qgis.Warning)
            return
        else:
            self._official_parcel_layer.setName(OFFICIAL_PARCEL_TABLE)
            # Layer was found, listen to its removal so that we can update the variable properly
            try:
                self._official_parcel_layer.willBeDeleted.disconnect(self.layer_removed)
            except TypeError as e:
                pass
            self._official_parcel_layer.willBeDeleted.connect(self.layer_removed)

        self.qgis_utils.map_freeze_requested.emit(False)

    def field_search_updated(self, index=None):
        self.initialize_field_values_line_edit()

    def initialize_field_values_line_edit(self):
        self.txt_alphanumeric_query.setLayer(self._official_parcel_layer)
        idx = self._official_parcel_layer.fields().indexOf(self.cbo_parcel_fields.currentData())
        self.txt_alphanumeric_query.setAttributeIndex(idx)

    def initialize_layers(self):
        self._plot_layer = None
        self._parcel_layer = None
        self._official_plot_layer = None
        self._official_parcel_layer = None

    def update_db_connection(self, db, ladm_col_db):
        self._db = db
        self.initialize_layers()

        if not ladm_col_db:
            self.setVisible(False)

    def layer_removed(self):
        # A required layer was removed, initialize variables so that next time we reload the layers
        self.initialize_layers()

    def fill_combos(self):
        self.cbo_parcel_fields.clear()

        if self._official_parcel_layer is not None:
            self.cbo_parcel_fields.addItem(QCoreApplication.translate("DockWidgetChanges", "Parcel Number"), PARCEL_NUMBER_FIELD)
            self.cbo_parcel_fields.addItem(QCoreApplication.translate("DockWidgetChanges", "Previous Parcel Number"), PARCEL_NUMBER_BEFORE_FIELD)
            self.cbo_parcel_fields.addItem(QCoreApplication.translate("DockWidgetChanges", "Folio de Matrícula Inmobiliaria"), FMI_FIELD)
        else:
            self.add_layers()

    def search_data(self, **kwargs):
        # TODO: use also FMI and previous_parcel_number?
        # TODO: optimize QgsFeatureRequest

        self.chk_show_all_plots.setEnabled(False)
        self.chk_show_all_plots.setChecked(False)

        # Get official parcel's t_id and get related plot(s)
        official_parcels = self._official_parcel_layer.getFeatures("{}='{}'".format(PARCEL_NUMBER_FIELD,
                                                                                  kwargs['parcel_number']))
        official_parcel = QgsFeature()
        res = official_parcels.nextFeature(official_parcel)

        if res:
            official_plot_t_ids = self.ladm_data.get_plots_related_to_parcels(self._official_db,
                                                                              [official_parcel[ID_FIELD]],
                                                                              field_name = ID_FIELD,
                                                                              plot_layer = self._official_plot_layer,
                                                                              uebaunit_table = None)
            if official_plot_t_ids:
                self.qgis_utils.map_freeze_requested.emit(True)

                self._current_official_substring = "\"{}\" IN ('{}')".format(ID_FIELD, "','".join([str(t_id) for t_id in official_plot_t_ids]))
                self._official_plot_layer.setSubsetString(self._current_official_substring)
                self.zoom_to_features(self._official_plot_layer, t_ids=official_plot_t_ids)

                # Get parcel's t_id and get related plot(s)
                parcels = self._parcel_layer.getFeatures("{}='{}'".format(PARCEL_NUMBER_FIELD,
                                                                        kwargs['parcel_number']))
                parcel = QgsFeature()
                res = parcels.nextFeature(parcel)
                if res:
                    plot_t_ids = self.ladm_data.get_plots_related_to_parcels(self._db,
                                                                             [parcel[ID_FIELD]],
                                                                             field_name=ID_FIELD,
                                                                             plot_layer=self._plot_layer,
                                                                             uebaunit_table=None)
                    self._current_substring = "{} IN ('{}')".format(ID_FIELD, "','".join([str(t_id) for t_id in plot_t_ids]))
                    self._plot_layer.setSubsetString(self._current_substring)

                self.qgis_utils.activate_layer_requested.emit(self._official_plot_layer)
                self.qgis_utils.map_freeze_requested.emit(False)

                # Activate Swipe Tool and send mouse event
                self.activate_mapswipe_tool()

                if res: # plot_t_ids found
                    plots = self.get_features_from_t_ids(self._plot_layer, plot_t_ids, True)
                    plots_extent = QgsRectangle()
                    for plot in plots:
                        plots_extent.combineExtentWith(plot.geometry().boundingBox())

                    print(plots_extent)
                    coord_x = plots_extent.xMaximum() - (plots_extent.xMaximum() - plots_extent.xMinimum()) / 9
                    coord_y = plots_extent.yMaximum() - (plots_extent.yMaximum() - plots_extent.yMinimum()) / 2

                    coord_transform = self.iface.mapCanvas().getCoordinateTransform()
                    map_point = coord_transform.transform(coord_x, coord_y)
                    widget_point = map_point.toQPointF().toPoint()
                    global_point = self.canvas.mapToGlobal(widget_point)

                    print(coord_x, coord_y, global_point)
                    #cursor = self.iface.mainWindow().cursor()
                    #cursor.setPos(global_point.x(), global_point.y())

                    self.canvas.mousePressEvent(QMouseEvent(QEvent.MouseButtonPress, global_point, Qt.LeftButton, Qt.LeftButton, Qt.NoModifier))
                    # mc.mouseMoveEvent(QMouseEvent(QEvent.MouseMove, gp, Qt.NoButton, Qt.LeftButton, Qt.NoModifier))
                    self.canvas.mouseMoveEvent(QMouseEvent(QEvent.MouseMove, widget_point + QPoint(1,0), Qt.NoButton, Qt.LeftButton, Qt.NoModifier))
                    # QApplication.processEvents()
                    self.canvas.mouseReleaseEvent(QMouseEvent(QEvent.MouseButtonRelease, widget_point + QPoint(1,0), Qt.LeftButton, Qt.LeftButton, Qt.NoModifier))
                    # QApplication.processEvents()

                    # Once the query is done, activate the checkbox to alternate all plots/only selected plot
                    self.chk_show_all_plots.setEnabled(True)

    def alphanumeric_query(self):
        """
        Alphanumeric query
        """
        option = self.cbo_parcel_fields.currentData()
        query = self.txt_alphanumeric_query.value()
        if query:
            if option == FMI_FIELD:
                self.search_data(parcel_fmi=query)
            elif option == PARCEL_NUMBER_FIELD:
                self.search_data(parcel_number=query)
            else: # previous_parcel_number
                self.search_data(previous_parcel_number=query)

        else:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                QCoreApplication.translate("DockWidgetChanges", "First enter a query"))

    def show_all_plots(self, state):
        self._official_plot_layer.setSubsetString(self._current_official_substring if not state else "")
        self._plot_layer.setSubsetString(self._current_substring if not state else "")

    def activate_mapswipe_tool(self):
        self.map_swipe_tool.run(True)
        self.iface.messageBar().clearWidgets()

    def deactivate_mapswipe_tool(self):
        self.map_swipe_tool.run(False)
        self.qgis_utils.set_layer_visibility(self._official_plot_layer, True)

    # def zoom_to_feature(self, layer, t_id):
    #     feature = self.get_feature_from_t_id(layer, t_id)
    #     self.iface.mapCanvas().zoomToFeatureIds(layer, [feature.id()])
    #     self.canvas.flashFeatureIds(layer,
    #                                 [feature.id()],
    #                                 QColor(255, 0, 0, 255),
    #                                 QColor(255, 0, 0, 0),
    #                                 flashes=1,
    #                                 duration=500)

    # plot_ids = self.ladm_data.get_plots_related_to_parcel(self._db, t_id, None, self._plot_layer, self._uebaunit_table)
    # if plot_ids:
    #     action_zoom_to_plots = QAction(QCoreApplication.translate("DockWidgetQueries", "Zoom to related plot(s)"))
    #     action_zoom_to_plots.triggered.connect(partial(self.zoom_to_plots, plot_ids))

    # def open_feature_form(self, layer, t_id):
    #     feature = self.get_feature_from_t_id(layer, t_id)
    #     self.iface.openFeatureForm(layer, feature)
    #

    # def zoom_to_plots(self, plot_ids):
    #     self.iface.mapCanvas().zoomToFeatureIds(self._plot_layer, plot_ids)
    #     self.canvas.flashFeatureIds(self._plot_layer,
    #                                 plot_ids,
    #                                 QColor(255, 0, 0, 255),
    #                                 QColor(255, 0, 0, 0),
    #                                 flashes=1,
    #                                 duration=500)

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
