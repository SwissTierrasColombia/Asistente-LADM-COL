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
from PyQt5.QtCore import Qt

from qgis.gui import QgsDockWidget, QgsMapToolIdentifyFeature

from asistente_ladm_col.gui.change_detection.changes_all_parcels_panel import ChangesAllParcelsPanelWidget
from asistente_ladm_col.gui.change_detection.changes_per_parcel_panel import ChangesPerParcelPanelWidget
from asistente_ladm_col.utils import get_ui_class

DOCKWIDGET_UI = get_ui_class('change_detection/dockwidget_change_detection.ui')

class DockWidgetChangeDetection(QgsDockWidget, DOCKWIDGET_UI):
    def __init__(self, iface, db, official_db, qgis_utils, ladm_data, parent=None):
        super(DockWidgetChangeDetection, self).__init__(None)
        self.setupUi(self)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.iface = iface
        self._db = db
        self._official_db = official_db
        self.qgis_utils = qgis_utils
        self.ladm_data = ladm_data

        self.main_panel = ChangesAllParcelsPanelWidget(self.iface)
        self.widget.setMainPanel(self.main_panel)
        self.parcel_panel = None

    def show_parcel_panel(self, parcel_t_id=None):
        self.parcel_panel = ChangesPerParcelPanelWidget(self.iface, self._db, self._official_db, self.qgis_utils, self.ladm_data)
        self.widget.showPanel(self.parcel_panel)

    def update_db_connection(self, db, ladm_col_db):
        self._db = db
        self.initialize_panels()

        if not ladm_col_db:
            self.setVisible(False)

    def initialize_panels(self):
        pass