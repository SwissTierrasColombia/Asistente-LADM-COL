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
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QFileSystemModel
from ..config.sql import PREDIO_SQL

from ..config.table_mapping_config import PLOT_TABLE, UEBAUNIT_TABLE, PARCEL_TABLE
from qgis._core import QgsWkbTypes, Qgis
from qgis.gui import QgsDockWidget

from ..utils import get_ui_class, qgis_utils

from ..data.qtmodels import QueryTreeViewModel

DOCKWIDGET_UI = get_ui_class('dockwidget_queries.ui')

class DockWidgetQueries(QgsDockWidget, DOCKWIDGET_UI):
    def __init__(self, iface, db, qgis_utils, parent=None):
        super(DockWidgetQueries, self).__init__(None)
        self.setupUi(self)
        self.iface = iface
        self._db = db
        self.qgis_utils = qgis_utils

        self.setWindowTitle('Search')
        #self.parentmodel = QFileSystemModel()
        #self.parentmodel.setRootPath('')
        # self.treeView.setModel(self.parentmodel) # example

        self.treeModel = QueryTreeViewModel()
        self.treeView.setModel(self.treeModel)
        self.treeModel.agregar()

        self._plot_layer = None

        self.add_options()

        self.add_events()

    def add_events(self):
        self.btn_query.clicked.connect(self.query_terreno)


    def add_options(self):
        self.cbo_plot_fields.clear()
        res_layers = self.qgis_utils.get_layers(self._db, {
            PLOT_TABLE: {'name': PLOT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry},
            PARCEL_TABLE: {'name': PARCEL_TABLE, 'geometry': None},
            UEBAUNIT_TABLE: {'name': UEBAUNIT_TABLE, 'geometry': None}}, load=True)

        self._plot_layer = res_layers[PLOT_TABLE]

        #self.iface._plot_layer = self._plot_layer  # expose for debug purposes
        #self.iface._db = self._db

        if self._plot_layer is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                                QCoreApplication.translate("CreateParcelCadastreWizard",
                                                                           "Plot layer couldn't be found... {}").format(
                                                    self._db.get_description()),
                                                Qgis.Warning)
            return

        for field in self._plot_layer.fields():
            alias = field.alias()
            if alias is '':
                name = field.name()
                self.cbo_plot_fields.addItem(name, name)
            else:
                self.cbo_plot_fields.addItem(alias, name)


    def query_terreno(self):
        t_id_terreno = 677
        print(PREDIO_SQL('test_ladm_col', t_id_terreno))


