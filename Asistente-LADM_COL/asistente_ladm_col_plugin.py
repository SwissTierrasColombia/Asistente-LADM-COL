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
from .gui.define_boundaries_cadaster_wizard import DefineBoundariesCadasterWizard
from .gui.settings_dialog import SettingsDialog
from .utils import qgis_utils

from functools import partial
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
        self._settings_dialog = None

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
        self._settings_action = QAction(icon, self.tr("Settings"), self.iface.mainWindow())
        self._help_action = QAction(icon, self.tr("Help"), self.iface.mainWindow())
        self._about_action = QAction(icon, self.tr("About"), self.iface.mainWindow())
        self._menu.addActions([self._settings_action,
                               self._help_action,
                               self._about_action])

        # Set connections
        self._point_spatial_unit_cadaster_action.triggered.connect(self.show_wiz_point_sp_un_cad)
        self._boundary_spatial_unit_cadaster_action.triggered.connect(self.show_wiz_boundaries_cad)
        self._settings_action.triggered.connect(self.show_settings)

        # Toolbar for Define Boundaries
        self._boundary_explode_action = QAction("Explode...", self.iface.mainWindow())
        self._boundary_explode_action.triggered.connect(qgis_utils.explode_boundaries)
        self._boundary_merge_action = QAction("Merge...", self.iface.mainWindow())
        self._boundary_merge_action.triggered.connect(qgis_utils.merge_boundaries)
        self._fill_point_BFS_action = QAction("Fill Point BFS", self.iface.mainWindow())
        self._fill_point_BFS_action.triggered.connect(partial(qgis_utils.fill_topology_table_pointbfs, self.get_db_connection()))
        self._define_boundary_toolbar = self.iface.addToolBar("Define Boundaries")
        self._define_boundary_toolbar.setObjectName("DefineBoundaries")
        self._define_boundary_toolbar.addActions([self._boundary_explode_action,
                                                  self._boundary_merge_action,
                                                  self._fill_point_BFS_action])
        self._define_boundary_toolbar.setVisible(False)

    def unload(self):
        #self.iface.removePluginDatabaseMenu(self.tr("Asistente LADM_COL"), self._action)
        self.iface.mainWindow().removeToolBar(self._define_boundary_toolbar)
        del self._define_boundary_toolbar

    def show_wiz_point_sp_un_cad(self):
        wiz = PointsSpatialUnitCadasterWizard(self.iface, self.get_db_connection())
        wiz.exec_()

    def show_wiz_boundaries_cad(self):
        wiz = DefineBoundariesCadasterWizard(self.iface, self.get_db_connection())
        wiz.exec_()

    def show_settings(self):
        if self._settings_dialog is None:
            self._settings_dialog = SettingsDialog(self.iface)
        self._settings_dialog.exec_()

    def get_db_connection(self):
        if self._settings_dialog is None:
            self._settings_dialog = SettingsDialog(self.iface)
        return self._settings_dialog.get_db_connection()
