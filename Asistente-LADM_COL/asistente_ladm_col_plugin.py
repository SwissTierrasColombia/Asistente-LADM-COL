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
from qgis.PyQt.QtWidgets import QAction, QMenu

from .gui.point_spa_uni_cadaster_wizard import PointsSpatialUnitCadasterWizard
#import resources_rc

class AsistenteLADMCOLPlugin(QObject):

    def __init__(self, iface):
        QObject.__init__(self)
        self.iface = iface

    def initGui(self):
        # Set Menus
        icon = QIcon(":/Asistente-LADM_COL/images/icon.png")
        self._menu = QMenu("LAD&M_COL", self.iface.mainWindow().menuBar())
        actions = self.iface.mainWindow().menuBar().actions()
        last_action = actions[-1]
        self.iface.mainWindow().menuBar().insertMenu(last_action, self._menu)

        self._cadaster_menu = QMenu(self.tr("Cadaster"), self._menu)
        self._spatial_unit_cadaster_menu = QMenu(self.tr("Spatial Unit"), self._cadaster_menu)
        self._point_spatial_unit_cadaster_action = QAction(self.tr("Add Points"), self._spatial_unit_cadaster_menu)
        self._boundary_spatial_unit_cadaster_action = QAction(self.tr("Define Boundaries"), self._spatial_unit_cadaster_menu)
        self._spatial_unit_cadaster_menu.addActions([self._point_spatial_unit_cadaster_action,
                                                     self._boundary_spatial_unit_cadaster_action])

        self._party_cadaster_menu = QMenu(self.tr("Party"), self._cadaster_menu)

        self._rrr_cadaster_menu = QMenu(self.tr("RRR"), self._cadaster_menu)
        self._right_rrr_cadaster_action = QAction(self.tr("Right"), self._rrr_cadaster_menu)
        self._restriction_rrr_cadaster_action = QAction(self.tr("Restriction"), self._rrr_cadaster_menu)
        self._responsibility_rrr_cadaster_action = QAction(self.tr("Responsibility"), self._rrr_cadaster_menu)
        self._rrr_cadaster_menu.addActions([self._right_rrr_cadaster_action,
                                            self._restriction_rrr_cadaster_action,
                                            self._responsibility_rrr_cadaster_action])

        self._source_cadaster_menu = QMenu(self.tr("Source"), self._cadaster_menu)

        self._cadaster_menu.addMenu(self._spatial_unit_cadaster_menu)
        self._cadaster_menu.addMenu(self._party_cadaster_menu)
        self._cadaster_menu.addMenu(self._rrr_cadaster_menu)
        self._cadaster_menu.addMenu(self._source_cadaster_menu)

        self._menu.addMenu(self._cadaster_menu)
        self._menu.addSeparator()
        self._help_action = QAction(icon, self.tr("Help"), self.iface.mainWindow())
        self._about_action = QAction(icon, self.tr("About"), self.iface.mainWindow())
        self._menu.addAction(self._help_action)
        self._menu.addAction(self._about_action)

        # Set connections
        self._point_spatial_unit_cadaster_action.triggered.connect(self.show_wiz_point_sp_un_cad)

    def unload(self):
        #self.iface.removePluginDatabaseMenu(self.tr("Asistente LADM_COL"), self._action)
        pass

    def show_wiz_point_sp_un_cad(self):
        wiz = PointsSpatialUnitCadasterWizard(self.iface)
        wiz.exec_()
