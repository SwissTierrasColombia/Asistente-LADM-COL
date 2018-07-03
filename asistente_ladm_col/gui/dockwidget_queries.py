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
from qgis.gui import QgsMessageBar, QgsDockWidget

from ..utils import get_ui_class

#from ..data.qtmodels import TreeViewModel

DOCKWIDGET_UI = get_ui_class('dockwidget_queries.ui')

class DockWidgetQueries(QgsDockWidget, DOCKWIDGET_UI):
    def __init__(self, iface, parent=None):
        super(DockWidgetQueries, self).__init__(None)
        self.setupUi(self)
        self.iface = iface

        #self.layout = QVBoxLayout()
        #self.setLayout(self.layout)

        #self._adminUnitTreeModel = TreeViewModel()


