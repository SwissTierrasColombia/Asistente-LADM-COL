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
from qgis.core import QgsWkbTypes, Qgis, QgsMessageLog, QgsFeature, QgsFeatureRequest, QgsExpression
from qgis.gui import QgsDockWidget, QgsMapToolIdentifyFeature

from asistente_ladm_col.utils.qt_utils import OverrideCursor
from ..config.table_mapping_config import (PLOT_TABLE,
                                           UEBAUNIT_TABLE,
                                           PARCEL_TABLE,
                                           ID_FIELD,
                                           PARCEL_NUMBER_FIELD,
                                           OFFICIAL_PLOT_TABLE,
                                           OFFICIAL_PARCEL_TABLE)

from ..utils import get_ui_class

from ..data.tree_models import TreeModel

DOCKWIDGET_UI = get_ui_class('dockwidget_changes.ui')

class DockWidgetChanges(QgsDockWidget, DOCKWIDGET_UI):
    def __init__(self, iface, db, official_db, qgis_utils, ladm_data, parent=None):
        super(DockWidgetChanges, self).__init__(None)
        self.setupUi(self)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.iface = iface
        self.canvas = iface.mapCanvas()
        self._db = db
        self._official_db = official_db
        self.qgis_utils = qgis_utils
        self.ladm_data = ladm_data

        # Required layers
        self._plot_layer = None
        self._parcel_layer = None
        self._official_plot_layer = None
        self._official_parcel_layer = None

        self.add_layers()
        self.fill_combos()

        # Set connections
        self.btn_alphanumeric_query.clicked.connect(self.alphanumeric_query)
        self.btn_clear_alphanumeric_query.clicked.connect(self.clear_alphanumeric_query)

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
            self.cbo_parcel_fields.addItem(QCoreApplication.translate("DockWidgetChanges", "Parcel Number"), 'parcel_number')
            self.cbo_parcel_fields.addItem(QCoreApplication.translate("DockWidgetChanges", "Previous Parcel Number"), 'previous_parcel_number')
            self.cbo_parcel_fields.addItem(QCoreApplication.translate("DockWidgetChanges", "Folio de Matrícula Inmobiliaria"), 'fmi')
        else:
            self.add_layers()

    def search_data(self, **kwargs):
        # TODO: use also FMI and previous_parcel_number?
        # TODO: optimize QgsFeatureRequest

        # Get official parcel's t_id and get related plot(s)
        official_parcels = self._official_parcel_layer.getFeatures("{}='{}'".format(PARCEL_NUMBER_FIELD,
                                                                                  kwargs['parcel_number']))
        official_parcel = QgsFeature()
        res = official_parcels.nextFeature(official_parcel)

        if res:
            plot_t_ids = self.ladm_data.get_plots_related_to_parcel(self._official_db,
                                                       official_parcel[ID_FIELD],
                                                       field_name = ID_FIELD,
                                                       plot_layer = self._official_plot_layer,
                                                       uebaunit_table = None)

            self.qgis_utils.map_freeze_requested.emit(True)

            self._official_plot_layer.setSubsetString(
                "\"{}\" IN ('{}')".format(ID_FIELD, "','".join([str(t_id) for t_id in plot_t_ids])))
            self.zoom_to_features(self._official_plot_layer, t_ids=plot_t_ids)
            self.qgis_utils.symbology.set_layer_style_from_qml(self._official_plot_layer)

            # Get parcel's t_id and get related plot(s)
            parcels = self._parcel_layer.getFeatures("{}='{}'".format(PARCEL_NUMBER_FIELD,
                                                                    kwargs['parcel_number']))
            parcel = QgsFeature()
            res = parcels.nextFeature(parcel)
            if res:
                plot_t_ids = self.ladm_data.get_plots_related_to_parcel(self._db,
                                                                        parcel[ID_FIELD],
                                                                        field_name=ID_FIELD,
                                                                        plot_layer=self._plot_layer,
                                                                        uebaunit_table=None)
                self._plot_layer.setSubsetString(
                    "{} IN ('{}')".format(ID_FIELD, "','".join([str(t_id) for t_id in plot_t_ids])))

            self.qgis_utils.activate_layer_requested.emit(self._official_plot_layer)
            self.qgis_utils.map_freeze_requested.emit(False)

            # TODO: Activate swipe tool

    def alphanumeric_query(self):
        """
        Alphanumeric query
        """
        option = self.cbo_parcel_fields.currentData()
        query = self.txt_alphanumeric_query.text().strip()
        if query:
            if option == 'fmi':
                self.search_data(parcel_fmi=query)
            elif option == 'parcel_number':
                self.search_data(parcel_number=query)
            else: # previous_parcel_number
                self.search_data(previous_parcel_number=query)

        else:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                QCoreApplication.translate("DockWidgetChanges", "First enter a query"))

    def clear_alphanumeric_query(self):
        self.txt_alphanumeric_query.setText('')

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

    def zoom_to_features(self, layer, ids=[], t_ids=[]): # TODO move this to a proper utils class
        if t_ids:
            features = self.get_features_from_t_ids(layer, t_ids, True, True)
            for feature in features:
                ids.append(feature.id())

        self.iface.mapCanvas().zoomToFeatureIds(layer, ids)
        self.canvas.flashFeatureIds(layer,
                                    ids,
                                    QColor(255, 0, 0, 255),
                                    QColor(255, 0, 0, 0),
                                    flashes=1,
                                    duration=500)

    def get_features_from_t_ids(self, layer, t_ids, no_attributes=False, no_geometry=False): # TODO move this to a proper utils class
        field_idx = layer.fields().indexFromName(ID_FIELD)
        request = QgsFeatureRequest(QgsExpression("{} IN ('{}')".format(ID_FIELD, "','".join([str(t_id) for t_id in t_ids]))))
        if no_attributes:
            request.setSubsetOfAttributes([field_idx])
        if no_geometry:
            request.setFlags(QgsFeatureRequest.NoGeometry)

        return [feature for feature in layer.getFeatures(request)]