"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin           : 2022-01-13
        git sha         : :%H$
        copyright       : (C) 2022 by Germán Carrillo (SwissTierras Colombia)
        email           : gcarrillo@linuxmail.org
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt5.uic import loadUi
from qgis.PyQt.QtCore import (pyqtSignal,
                              QCoreApplication)
from qgis.PyQt.QtWidgets import QWidget
from qgis.gui import QgsPanelWidget

from asistente_ladm_col.gui.transitional_system.tasks_widget import TasksWidget
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.lib.transitional_system.st_session.st_session import STSession
from asistente_ladm_col.utils.ui import (get_ui_class,
                                         get_ui_file_path)

WIDGET_UI = get_ui_class('quality_rules/quality_rules_initial_panel_widget.ui')


class QualityRulesInitialPanelWidget(QgsPanelWidget, WIDGET_UI):
    HOME_WIDGET = "home_widget"
    TASKS_WIDGET = "tasks_widget"

    def __init__(self, parent=None):
        QgsPanelWidget.__init__(self, parent)
        self.setupUi(self)
        self.parent = parent
        self.logger = Logger()

        self.setDockMode(True)
        self.setPanelTitle(QCoreApplication.translate("QualityRulesInitialPanelWidget", "Quality Rules"))

    def show_task_panel(self, task_id):
        """
        Slot called to show the task panel based on a selected task.

        :param task_id: Id of the task that will be used to show the task panel.
        """
        self.parent.show_task_panel(task_id)
