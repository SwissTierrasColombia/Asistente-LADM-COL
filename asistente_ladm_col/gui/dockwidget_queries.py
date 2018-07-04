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
from ..config.table_mapping_config import PLOT_TABLE
from qgis._core import QgsWkbTypes, Qgis
from qgis.gui import QgsMessageBar, QgsDockWidget

from ..utils import get_ui_class, qgis_utils

from ..data.qtmodels import TreeViewModel

DOCKWIDGET_UI = get_ui_class('dockwidget_queries.ui')

class DockWidgetQueries(QgsDockWidget, DOCKWIDGET_UI):
    def __init__(self, iface, db, qgis_utils, parent=None):
        super(DockWidgetQueries, self).__init__(None)
        self.setupUi(self)
        self.iface = iface
        self._db = db
        self.qgis_utils = qgis_utils

        self.setWindowTitle('Search')
        self.parentmodel = QFileSystemModel()
        self.parentmodel.setRootPath('')
        self.treeModel = TreeViewModel(self.parentmodel)
        #self.treeView.setModel(self.treeModel)
        self.treeView.setModel(self.parentmodel) # example

        self._plot_layer = None

        self.add_options()

    def add_options(self):
        self.cbo_plot_fields
        self.cbo_plot_fields.clear()
        res_layers = self.qgis_utils.get_layers(self._db, {
            PLOT_TABLE: {'name': PLOT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry}
        })

        self._plot_layer = res_layers[PLOT_TABLE]
        if self._plot_layer is None:
            QgsMessageBar.pushWarning("OJO, llenar eso con conexión a base de datos?")
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                                QCoreApplication.translate("CreateParcelCadastreWizard",
                                                                           "Plot layer couldn't be found... {}").format(
                                                    self._db.get_description()),
                                                Qgis.Warning)
            return
        self.iface._plot_layer = self._plot_layer # expose for debug purposes

        for field in self._plot_layer.fields():
            alias = field.alias()
            if alias is '':
                name = field.name()
                self.cbo_plot_fields.addItem(name, name)
            else:
                self.cbo_plot_fields.addItem(alias, name)
