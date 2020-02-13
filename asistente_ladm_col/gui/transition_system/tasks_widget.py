# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-12-02
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
from qgis.PyQt.QtCore import (Qt,
                              QCoreApplication,
                              QSize,
                              pyqtSignal)
from qgis.PyQt.QtWidgets import (QWidget,
                                 QListWidgetItem,
                                 QMessageBox)

from asistente_ladm_col.config.enums import STTaskStatusEnum
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.lib.transition_system.st_session.st_session import STSession
from asistente_ladm_col.lib.transition_system.task_manager.tasks_model import TasksModel
from asistente_ladm_col.utils.ui import get_ui_class, get_ui_file_path

WIDGET_UI = get_ui_class('transition_system/tasks_widget.ui')


class TasksWidget(QWidget, WIDGET_UI):
    task_panel_requested = pyqtSignal(int)  # Selected task_id

    def __init__(self, user):
        QWidget.__init__(self)
        self.setupUi(self)
        self.logger = Logger()
        self.session = STSession()
        self._user = user

        self.lvw_tasks.itemSelectionChanged.connect(self.update_controls)
        self.lvw_tasks.itemDoubleClicked.connect(self.call_task_panel)
        self.btn_view_task.clicked.connect(self.view_task)
        self.btn_close_task.clicked.connect(self.close_task)

        self.update_controls()  # Initialize controls

    def show_tasks(self):
        self.clear_task_widget()
        tasks = self._get_user_tasks()
        self.update_task_count_label(len(tasks))
        for k, task in tasks.items():
            self.add_task_widget_item_to_view(task)

    def _get_user_tasks(self):
        return self.session.task_manager.get_tasks(self._user)

    def update_controls(self):
        selected_items = self.lvw_tasks.selectedItems()
        enable = len(selected_items) == 1
        self.btn_view_task.setEnabled(enable)

        if enable:
            # Enable Close Task button?
            task = self.session.task_manager.get_task(selected_items[0].data(Qt.UserRole))
            if task:
                enable = task.get_status() == STTaskStatusEnum.STARTED.value and task.steps_complete()

        self.btn_close_task.setEnabled(enable)

    def update_task_count_label(self, count):
        self.lbl_task_count.setText(QCoreApplication.translate("TasksWidget",
               "{} pending task{}").format(count, "s" if count>1 else ""))

    def view_task(self):
        items = self.lvw_tasks.selectedItems()
        if items:
            self.call_task_panel(items[0])

    def call_task_panel(self, item):
        task_id = item.data(Qt.UserRole)
        self.logger.info(__name__, "View task (id:{})".format(task_id))
        self.task_panel_requested.emit(task_id)

    def close_task(self):
        items = self.lvw_tasks.selectedItems()
        if items:
            reply = QMessageBox.question(self,
                                         QCoreApplication.translate("TaskPanelWidget", "Confirm"),
                                         QCoreApplication.translate("TaskPanelWidget",
                                                                    "Are you sure you want to close the task '{}'?").format(
                                             self._task.get_name()),
                                         QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                task_id = items[0].data(Qt.UserRole)
                self.session.task_manager.close_task(self._user, task_id)

    def add_task_widget_item_to_view(self, task):
        widget_item = loadUi(get_ui_file_path('transition_system/task_widget_item.ui'), QWidget())
        widget_item.lbl_name.setText(task.get_name())
        widget_item.lbl_description.setText(task.get_description())
        widget_item.lbl_status.setText(task.get_status())
        widget_item.lbl_created_at.setText("Created at: {}".format(task.get_creation_date()))
        widget_item.lbl_deadline.setText("Deadline: {}".format(task.get_deadline()))
        item = QListWidgetItem(self.lvw_tasks)
        self.lvw_tasks.setItemWidget(item, widget_item)
        item.setSizeHint(QSize(widget_item.width(), widget_item.height()))
        item.setData(Qt.UserRole, task.id())
        self.lvw_tasks.addItem(item)

    def clear_task_widget(self):
        self.lvw_tasks.clear()
