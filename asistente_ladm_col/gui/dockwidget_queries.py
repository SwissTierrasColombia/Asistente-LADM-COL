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
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QColor, QIcon, QCursor

from ..config.table_mapping_config import PLOT_TABLE, UEBAUNIT_TABLE, PARCEL_TABLE
from qgis._core import QgsWkbTypes, Qgis, QgsMessageLog
from qgis.gui import QgsDockWidget, QgsMapToolIdentifyFeature

from ..utils import get_ui_class

from ..data.tree_models import TreeModel

DOCKWIDGET_UI = get_ui_class('dockwidget_queries.ui')

class DockWidgetQueries(QgsDockWidget, DOCKWIDGET_UI):
    def __init__(self, iface, db, qgis_utils, parent=None):
        super(DockWidgetQueries, self).__init__(None)
        self.setupUi(self)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.iface = iface
        self._db = db
        self.qgis_utils = qgis_utils

        # self.treeView.selectionModel().selectionChanged.connect(self.treeModel.updateActions)

        self._plot_layer = None
        self._identify_tool = None
        self._identify_neighbours_tool = None

        self.add_options()

        self.btn_identify_plot.setIcon(QIcon(":/Asistente-LADM_COL/resources/images/surveying.png"))
        self.btn_identify_plot_neighbours.setIcon(QIcon(":/Asistente-LADM_COL/resources/images/party.png"))

        # Set connections
        self.btn_query_plot.clicked.connect(self.query_plot)
        self.btn_clear_plot.clicked.connect(self.clear_plot)
        self.btn_identify_plot.clicked.connect(self.identify_plot)
        self.btn_identify_plot_neighbours.clicked.connect(self.identify_plot_neighbours)

    def add_layers(self):
        res_layers = self.qgis_utils.get_layers(self._db, {
            PLOT_TABLE: {'name': PLOT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry},
            PARCEL_TABLE: {'name': PARCEL_TABLE, 'geometry': None},
            UEBAUNIT_TABLE: {'name': UEBAUNIT_TABLE, 'geometry': None}}, load=True)

        self._plot_layer = res_layers[PLOT_TABLE]

        if self._plot_layer is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                                QCoreApplication.translate("DockerWidgetQueries",
                                                                           "Plot layer couldn't be found... {}").format(
                                                    self._db.get_description()),
                                                Qgis.Warning)
            return

    def add_options(self):
        if self._plot_layer == None:
            self.add_layers()

        self.cbo_plot_fields.clear()

        for field in self._plot_layer.fields():
            alias = field.alias()
            if alias is '':
                name = field.name()
                self.cbo_plot_fields.addItem(name, name)
            else:
                self.cbo_plot_fields.addItem(alias, name)

    def query_plot(self):
        option = self.cbo_plot_fields.currentData()
        query = self.txt_plot_query.text()
        if option == 't_id':
            if query != '' and query.isdigit():
                plot_t_id = query
                records = self._db.get_parcels_and_parties_by_plot(plot_t_id)
                print(records)
                self.treeModel = TreeModel(data=records)
                self.treeView.setModel(self.treeModel)
                self.treeView.expandAll()
            else:
                self.iface.messageBar().pushMessage("Asistente LADM_COL",
                    QCoreApplication.translate("DockerWidgetQueries","t_id must be an integer"))


    def clear_plot(self):
        self.txt_plot_query.setText('')


    def identify_plot(self):
        # enable needed layers
        self.add_layers()

        # recover old state of mapCanvas
        self.mapCanvas = self.iface.mapCanvas()
        self.previousTool = self.mapCanvas.mapTool()

        # configure listeners
        if self._identify_tool == None:
            self._identify_tool = CustomMapToolIdentifyFeature(self.mapCanvas, self._plot_layer, self.btn_identify_plot, self.previousTool, self.callback_identify)
        else:
            self._identify_tool.activate()
        self.mapCanvas.setMapTool(self._identify_tool)

        #self._click_point.activate()

        #self.iface.actionSelect().trigger()
        #self.clickeado()

        #self.canvas_clicked.canvasClicked.connect(self.clickeado)

        # activate previous tool
        #currentTool = self.iface.mapCanvas().mapTool()
        #currentTool.activate()

    def callback_identify(self, plot_feature):
        plot_t_id = plot_feature['t_id']
        records = self._db.get_parcels_and_parties_by_plot(plot_t_id)
        print(records)
        self.treeModel = TreeModel(data=records)
        self.treeView.setModel(self.treeModel)
        self.treeView.expandAll()

    def identify_plot_neighbours(self):
        # enable needed layers
        self.add_layers()

        # recover old state of mapCanvas
        self.mapCanvas = self.iface.mapCanvas()
        self.previousTool = self.mapCanvas.mapTool()

        # configure listeners
        if self._identify_neighbours_tool == None:
            self._identify_neighbours_tool = CustomMapToolIdentifyFeature(self.mapCanvas, self._plot_layer, self.btn_identify_plot_neighbours,
                                                               self.previousTool, self.callback_identify_neighbours)
        else:
            self._identify_neighbours_tool.activate()
        self.mapCanvas.setMapTool(self._identify_neighbours_tool)

    def callback_identify_neighbours(self, plot_feature):
        plot_t_id = plot_feature['t_id']
        records = self._db.get_parcels_and_parties_by_plot(plot_t_id)
        print(records)
        self.treeModel = TreeModel(data=records)
        self.treeView.setModel(self.treeModel)
        self.treeView.expandAll()



class CustomMapToolIdentifyFeature(QgsMapToolIdentifyFeature):
    def __init__(self, canvas, vlayer, button, previousTool, callback_identify):
        self.canvas = canvas
        self.vlayer = vlayer
        self.button = button
        self.previousTool = previousTool
        self.callback_identify = callback_identify

        self.button.setCheckable(True)

        QgsMapToolIdentifyFeature.__init__(self, self.canvas, self.vlayer)

        self.featureIdentified.connect(self.featureIdentifiedListener)

    def featureIdentifiedListener(self, feature):
        self.vlayer.selectByIds([feature.id()])
        print(feature.id())
        self.callback_identify(feature)
        self.deactivate()
        self.canvas.unsetMapTool(self) # instead of self.featureIdentified.disconnect(self.featureIdentifiedListener)
        try:
            self.previousTool.activate()
        except AttributeError:
            # if isn't active, doesn't matter
            pass


    def activate(self):
        """
        Overrides parent class.  Set custom cursor and change icon.
        """
        self.canvas.setCursor(QCursor(Qt.PointingHandCursor))
        self.canvas.setSelectionColor(QColor("red"))
        self.button.setChecked(True)

    def deactivate(self):
        """
        Overrides parent class.  Change icon back.
        """
        self.button.setChecked(False)
        self.canvas.mapTool()

