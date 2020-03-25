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

from asistente_ladm_col.config.enums import EnumSTTaskStatus
from asistente_ladm_col.config.transitional_system_config import TransitionalSystemConfig
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.lib.transitional_system.st_session.st_session import STSession
from asistente_ladm_col.utils.ui import get_ui_class, get_ui_file_path

WIDGET_UI = get_ui_class('transitional_system/tasks_widget.ui')


class TasksWidget(QWidget, WIDGET_UI):
    task_panel_requested = pyqtSignal(int)  # Selected task_id

    def __init__(self, user):
        QWidget.__init__(self)
        self.setupUi(self)
        self.logger = Logger()
        self.session = STSession()
        self._user = user
        self.st_config = TransitionalSystemConfig()

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
                enable = task.get_status() == EnumSTTaskStatus.STARTED.value and task.steps_complete()

        self.btn_close_task.setEnabled(enable)

        for index in range(self.lvw_tasks.count()):
            # Update every single task item with a proper style
            item = self.lvw_tasks.item(index)
            self.set_task_item_style(self.lvw_tasks.itemWidget(item), item.isSelected())

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
        widget_item = loadUi(get_ui_file_path('transitional_system/task_widget_item.ui'), QWidget())
        widget_item.lbl_name.setText(task.get_name())
        widget_item.lbl_description.setText(task.get_description())
        widget_item.lbl_status.setText(task.get_status())
        widget_item.lbl_created_at.setText(QCoreApplication.translate("TaskPanelWidget", "Created at: {}").format(task.get_creation_date()))
        widget_item.lbl_deadline.setText(QCoreApplication.translate("TaskPanelWidget", "Deadline: {}").format(task.get_deadline()))

        self.set_task_item_style(widget_item)
        item = QListWidgetItem(self.lvw_tasks)
        self.lvw_tasks.setItemWidget(item, widget_item)
        item.setSizeHint(QSize(widget_item.width(), widget_item.height()))
        item.setData(Qt.UserRole, task.get_id())
        self.lvw_tasks.addItem(item)

    def set_task_item_style(self, widget, selected=False):
        title_text = self.st_config.TASK_TITLE_TEXT_CSS
        normal_text = self.st_config.TASK_NORMAL_TEXT_CSS
        date_text = self.st_config.TASK_DATE_TEXT_CSS
        if widget.lbl_status.text() == EnumSTTaskStatus.ASSIGNED.value:
            status_text = self.st_config.TASK_ASSIGNED_STATUS_TEXT_CSS
        elif widget.lbl_status.text() == EnumSTTaskStatus.STARTED.value:
            status_text = self.st_config.TASK_STARTED_STATUS_SELECTED_TEXT_CSS if selected else self.st_config.TASK_STARTED_STATUS_TEXT_CSS

        if selected:
            title_text = self.st_config.TASK_TITLE_SELECTED_TEXT_CSS
            normal_text = self.st_config.TASK_NORMAL_SELECTED_TEXT_CSS
            date_text = self.st_config.TASK_DATE_SELECTED_TEXT_CSS

        widget.lbl_name.setStyleSheet(title_text)
        widget.lbl_description.setStyleSheet(normal_text)
        widget.lbl_status.setStyleSheet(status_text)
        widget.lbl_created_at.setStyleSheet(date_text)
        widget.lbl_deadline.setStyleSheet(date_text)

    def clear_task_widget(self):
        self.lvw_tasks.clear()
