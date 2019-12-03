# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-12-03
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
from functools import partial

from qgis.PyQt.QtCore import (Qt,
                              pyqtSignal,
                              QCoreApplication)
from qgis.PyQt.QtWidgets import (QTableWidgetItem,
                                 QMenu,
                                 QAction)
from qgis.core import (QgsWkbTypes,
                       NULL,
                       QgsApplication)
from qgis.gui import QgsPanelWidget

from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.config.table_mapping_config import Names
from asistente_ladm_col.lib.st_session.st_session import STSession
from ...utils import get_ui_class
from ...utils.qt_utils import OverrideCursor

WIDGET_UI = get_ui_class('transition_system/transition_system_task_panel_widget.ui')


class TaskPanelWidget(QgsPanelWidget, WIDGET_UI):
    def __init__(self, task_id, parent):
        QgsPanelWidget.__init__(self, parent)
        self.setupUi(self)
        self.session = STSession()
        self._task = self.session.task_manager.get_task(task_id)
        self.parent = parent
        self.logger = Logger()
        self.names = Names()

        self.setDockMode(True)
        self.setPanelTitle(QCoreApplication.translate("TaskPanelWidget", "Task details"))

        self.initialize_gui()

    def initialize_gui(self):
        self.initialize_description()
        self.update_view()

    def initialize_description(self):
        if self._task is not None:
            self.logger.debug(__name__, "Setting task description in Task Panel...")
            self.lbl_name.setText(self._task.get_name())
            self.lbl_description.setText(self._task.get_description())
            self.lbl_created_at.setText("Created at: {}".format(self._task.get_creation_date()))
            self.lbl_started_at.setText("Started at: {}".format(self._task.get_started_date()))
            self.lbl_deadline.setText("Deadline: {}".format(self._task.get_deadline()))
            self.lbl_status.setText(self._task.get_status())

    def update_view(self):
        pass