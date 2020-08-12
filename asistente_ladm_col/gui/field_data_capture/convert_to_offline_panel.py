# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM-COL
                             --------------------
        begin                : 2020-08-11
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
import os

from qgis.PyQt.QtCore import (QCoreApplication,
                              Qt,
                              pyqtSignal)
from qgis.PyQt.QtGui import QBrush
from qgis.PyQt.QtWidgets import (QTableWidgetItem,
                                 QMessageBox,
                                 QFileDialog)
from qgis.gui import QgsPanelWidget

from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.config.enums import EnumLogHandler
from asistente_ladm_col.config.general_config import NOT_ALLOCATED_PARCEL_COLOR
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.utils import get_ui_class

WIDGET_UI = get_ui_class('field_data_capture/convert_to_offline_panel_widget.ui')


class ConvertToOfflinePanelWidget(QgsPanelWidget, WIDGET_UI):
    refresh_parcel_data_clear_selection_requested = pyqtSignal()

    def __init__(self, parent, controller):
        QgsPanelWidget.__init__(self, parent)
        self.setupUi(self)
        self.parent = parent
        self.controller = controller

        self.logger = Logger()
        self.app = AppInterface()

        self.setDockMode(True)
        self.setPanelTitle(QCoreApplication.translate("ConvertToOfflinePanelWidget", "Convert to offline"))
        self.parent.setWindowTitle(QCoreApplication.translate("ConvertToOfflinePanelWidget", "Allocate parcels"))

        self.mQgsFileWidget.lineEdit().setPlaceholderText(QCoreApplication.translate("ConvertToOfflinePanelWidget", "Choose the output folder..."))
        self.mQgsFileWidget.setDefaultRoot(self.app.settings.export_dir_offline_projects)

        self.panelAccepted.connect(self.panel_accepted)
        self.controller.convert_to_offline_progress.connect(self.update_progress)
        self.btn_generate_offline_projects.clicked.connect(self.generate_offline_projects)

    def panel_accepted(self):
        self.refresh_parcel_data_clear_selection_requested.emit()

    def fill_data(self, refresh_parcel_data=False):
        summary_data = self.controller.get_summary_data()

        # TODO: Add widgets and spacers to grid layout

    def fill_row(self, surveyor_name, parcel_count):
        pass

    def generate_offline_projects(self):
        self.logger.clear_message_bar()
        export_dir = self.mQgsFileWidget.filePath()

        if export_dir and os.path.isdir(export_dir):
            self.app.settings.export_dir_offline_projects = export_dir
            self.prb_to_offline.setRange(0, 100)
            self.prb_to_offline.setValue(0)

            res, msg = self.controller.convert_to_offline(export_dir)

            self.logger.success_warning(__name__, res, msg, EnumLogHandler.MESSAGE_BAR)
        else:
            self.logger.warning_msg(__name__, QCoreApplication.translate("ConvertToOfflinePanelWidget", "The output folder is invalid. Choose a valid folder."))

    def update_progress(self, progress):
        self.prb_to_offline.setValue(progress)