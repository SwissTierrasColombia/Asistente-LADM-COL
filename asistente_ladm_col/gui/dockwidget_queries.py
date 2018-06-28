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
import os

from qgis.core import QgsProject, QgsVectorLayer, Qgis, QgsWkbTypes
from qgis.gui import QgsMessageBar, QgsDockWidget
from qgis.PyQt.QtCore import Qt, QSettings, QCoreApplication
from qgis.PyQt.QtGui import QBrush, QFont, QIcon
from qgis.PyQt.QtWidgets import (QAction, QDialog, QTreeWidgetItem, QLineEdit,
                                 QTreeWidgetItemIterator, QComboBox)

from ..utils import get_ui_class

from ..resources_rc import *

DOCKWIDGET_UI = get_ui_class('dockwidget_queries.ui')

class DockWidgetQueries(QgsDockWidget, DOCKWIDGET_UI):
    def __init__(self, iface, parent=None):
        QgsDockWidget.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        #self.iface.addDockWidget(DOCKWIDGET_UI)

