# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-11-29
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
from PyQt5.uic import loadUi
from qgis.PyQt.QtCore import (pyqtSignal,
                              QCoreApplication)
from qgis.PyQt.QtWidgets import QWidget
from qgis.gui import QgsPanelWidget

from asistente_ladm_col.gui.transition_system.tasks_widget import TasksWidget
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.lib.transition_system.st_session.st_session import STSession
from asistente_ladm_col.utils.ui import (get_ui_class,
                                         get_ui_file_path)

WIDGET_UI = get_ui_class('transition_system/transition_system_initial_panel_widget.ui')


class TransitionSystemInitialPanelWidget(QgsPanelWidget, WIDGET_UI):
    HOME_WIDGET = "home_widget"
    TASKS_WIDGET = "tasks_widget"
    logout_requested = pyqtSignal()

    def __init__(self, user, parent=None):
        QgsPanelWidget.__init__(self, parent)
        self.setupUi(self)
        self._user = user
        self.parent = parent
        self.logger = Logger()
        self.session = STSession()
        self._current_widget = None

        self.home_widget = loadUi(get_ui_file_path('transition_system/home_widget.ui'), QWidget())
        self.tasks_widget = TasksWidget(user)  # No need to use parent, as the layout will call setParent automatically
        self.tasks_widget.task_panel_requested.connect(self.show_task_panel)

        self.setDockMode(True)
        self.setPanelTitle(QCoreApplication.translate("TransitionSystemInitialPanelWidget", "Transition System"))

        self.btn_home.clicked.connect(self.show_home_widget)
        self.btn_view_tasks.clicked.connect(self.show_tasks_widget)
        self.btn_logout.clicked.connect(self.logout_requested)

        # Now update controls to show an initial state to users
        self._update_user_info()
        self.show_tasks_widget()

    def _update_user_info(self):
        self.lbl_user_info.setText(
            QCoreApplication.translate("TransitionSystemInitialPanelWidget",
                                       "User: {}\nRole: {}".format(self._user.get_name(), self._user.get_role())))

    def fill_data(self):
        pass

    def show_home_widget(self):
        if self._current_widget != self.HOME_WIDGET:
            self.clear_content_widget()

            self.content_layout.addWidget(self.home_widget)
            self.home_widget.setVisible(True)
            self._current_widget = self.HOME_WIDGET

    def show_tasks_widget(self):
        if self._current_widget != self.TASKS_WIDGET:
            self.clear_content_widget()
            self.content_layout.addWidget(self.tasks_widget)
            self.tasks_widget.setVisible(True)
            self._current_widget = self.TASKS_WIDGET

        self.tasks_widget.show_tasks()  # Retrieve tasks from server

    def clear_content_widget(self):
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().setVisible(False)
            #    child.widget().deleteLater()

    def show_task_panel(self, task_id):
        """
        Slot called to show the task panel based on a selected task.

        :param task_id: Id of the task that will be used to show the task panel.
        """
        self.parent.show_task_panel(task_id)
