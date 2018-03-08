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

from qgis.core import QgsProject, QgsVectorLayer, Qgis
from qgis.gui import QgsMessageBar
from qgis.PyQt.QtCore import Qt, QSettings
from qgis.PyQt.QtWidgets import QDialog, QSizePolicy, QGridLayout

from ..lib.dbconnector.gpkg_connector import GPKGConnector
from ..lib.dbconnector.pg_connector import PGConnector
from ..utils import get_ui_class
from ..utils.qt_utils import make_file_selector

DIALOG_UI = get_ui_class('dlg_load_layers.ui')

class DialogLoadLayers(QDialog, DIALOG_UI):
    def __init__(self, iface, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self._db = None

        self.cbo_select_predefined_tables.clear()
        self.cbo_select_predefined_tables.addItem(self.tr('Spatial data'), 'spatial_data')
        self.cbo_select_predefined_tables.addItem(self.tr('Legal data'), 'legal_data')
        self.cbo_select_predefined_tables.currentIndexChanged.connect(self.select_predefined_changed)

        # Load layers from the db
        self.load_available_layers()

        # Set connections
        self.buttonBox.accepted.connect(self.accepted)

        # Trigger some default behaviours
        self.restore_settings()

    def load_available_layers(self):
        # Call project generator tabls_info and fill the layer tree
        pass

    def accepted(self):
        print("Accepted!")
        self._db = None # Reset db connection
        self._db = self.get_db_connection()
        self.save_settings()

    def save_settings(self):
        # Save QSettings
        # settings = QSettings(
        pass

    def restore_settings(self):
        # Restore QSettings
        # settings = QSettings()
        pass

    def select_predefined_changed(self):
        pass
