# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-02-21
        git sha              : :%H$
        copyright            : (C) 2019 by Yesid Polanía (BSF Swissphoto)
        email                : yesidpol.3@gmail.com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""

from qgis.PyQt.QtCore import (QCoreApplication,
                              pyqtSignal)
from qgis.core import Qgis
from ...config.enums import EnumDbActionType
from ...utils.qt_utils import (make_save_file_selector,
                               make_file_selector)
from .db_config_panel import DBConfigPanel
from ...utils import get_ui_class

WIDGET_UI = get_ui_class('dialogs/settings_gpkg.ui')


class GPKGConfigPanel(DBConfigPanel, WIDGET_UI):
    notify_message_requested = pyqtSignal(str, Qgis.MessageLevel)

    def __init__(self, parent):
        DBConfigPanel.__init__(self, parent)
        self.setupUi(self)

        self.action = None
        self.set_action(EnumDbActionType.CONFIG)

    def read_connection_parameters(self):
        dict_conn = dict()
        dict_conn['dbfile'] = self.txt_file.log_quality_validation_text().strip()

        return dict_conn

    def write_connection_parameters(self, dict_conn):
        self.txt_file.setText(dict_conn['dbfile'] if 'dbfile' in dict_conn else '')

    def get_keys_connection_parameters(self):
        return list(self.read_connection_parameters().keys())

    def set_action(self, action):
        self.action = action
        try:
            self.btn_file_browse.clicked.disconnect()
        except TypeError:
            pass

        if action == EnumDbActionType.SCHEMA_IMPORT:
            # TODO DialogImportSchema?
            file_selector = make_save_file_selector(
                                self.txt_file,
                                title=QCoreApplication.translate("DialogImportSchema", "Create GeoPackage database file"),
                                file_filter=QCoreApplication.translate("DialogImportSchema", "GeoPackage Database (*.gpkg)"),
                                extension='.gpkg')

        else:
            # TODO DialogExportData?
            file_selector = make_file_selector(self.txt_file,
                                title=QCoreApplication.translate("DialogExportData", "Open GeoPackage database file"),
                                file_filter=QCoreApplication.translate("DialogExportData","GeoPackage Database (*.gpkg)"))

        self.btn_file_browse.clicked.connect(file_selector)

    def state_changed(self):
        result = True

        if self.state:
            result = self.state['dbfile'] != self.txt_file.log_quality_validation_text().strip()

        return result
