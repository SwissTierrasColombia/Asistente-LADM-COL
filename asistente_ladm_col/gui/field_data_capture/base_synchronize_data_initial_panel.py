# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM-COL
                             --------------------
        begin                : 2020-10-22
        git sha              : :%H$
        copyright            : (C) 2020 by Germán Carrillo (SwissTierras Colombia)
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
from qgis.PyQt.QtCore import (QCoreApplication,
                              Qt,
                              pyqtSignal)
from qgis.gui import QgsPanelWidget

from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.config.enums import EnumLogHandler
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.utils import get_ui_class

WIDGET_UI = get_ui_class('field_data_capture/base_synchronize_data_initial_panel_widget.ui')


class BaseSynchronizeDataInitialPanelWidget(QgsPanelWidget, WIDGET_UI):
    def __init__(self, parent, controller, db):
        QgsPanelWidget.__init__(self, parent)
        self.setupUi(self)
        self.parent = parent
        self._controller = controller
        self._db = db

        self.logger = Logger()
        self.app = AppInterface()

        self.setDockMode(True)
        self.setPanelTitle(QCoreApplication.translate("BaseSynchronizeDataInitialPanelWidget", "Synchronize data"))
        self.parent.setWindowTitle(QCoreApplication.translate("BaseSynchronizeDataInitialPanelWidget", "Synchronize data"))

        self.btn_synchronize.clicked.connect(self.synchronize_data)

        self._update_connection_info()

    def _update_connection_info(self):
        db_description = self._db.get_description_conn_string() if self._db else None
        if db_description:
            self.db_connect_label.setText(db_description)
            self.db_connect_label.setToolTip(self._db.get_display_conn_string())
        else:
            self.db_connect_label.setText(QCoreApplication.translate("BaseSynchronizeDataInitialPanelWidget",
                                                                     "The database is not defined!"))
            self.db_connect_label.setToolTip('')

    def close_panel(self):
        # Disconnect signals
        pass

    def synchronize_data(self):
        res, msg = self._controller.synchronize_data(self._db, self.qfw_input_file.filePath().strip())
        self.logger.success_warning(__name__, res, msg, EnumLogHandler.MESSAGE_BAR)
