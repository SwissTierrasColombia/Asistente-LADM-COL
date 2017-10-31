# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2017-10-31
        git sha              : :%H$
        copyright            : (C) 2017 by Germán Carrillo (BSF Swissphoto)
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
from qgis.PyQt.QtCore import QObject
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

#import resources_rc

class AsistenteLADMCOLPlugin(QObject):

    def __init__(self, iface):
        QObject.__init__(self)
        self.iface = iface

    def initGui(self):
        icon = QIcon(":/Asistente-LADM_COL/images/icon.png")
        self._action = QAction(icon, self.tr("Asistente LADM_COL"), self.iface.mainWindow())

        self.iface.addPluginToDatabaseMenu(self.tr("Asistente LADM_COL"), self._action)

    def unload(self):
        self.iface.removePluginDatabaseMenu(self.tr("Asistente LADM_COL"), self._action)
        del self._action

    def run(self):
        # TODO
        pass

