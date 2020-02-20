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
import json

from qgis.PyQt.QtCore import (Qt,
                              pyqtSignal,
                              QCoreApplication,
                              QSettings)
from qgis.PyQt.QtGui import QBrush
from qgis.PyQt.QtWidgets import (QTreeWidgetItem,
                                 QMessageBox,
                                 QDialog)
from qgis.gui import QgsPanelWidget

from asistente_ladm_col.config.enums import STTaskStatusEnum
from asistente_ladm_col.config.general_config import (CHECKED_COLOR,
                                                      UNCHECKED_COLOR,
                                                      GRAY_COLOR)
from asistente_ladm_col.config.task_steps_config import (SLOT_NAME,
                                                         SLOT_PARAMS)
from asistente_ladm_col.gui.transitional_system.dlg_cancel_task import STCancelTaskDialog
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.lib.transitional_system.st_session.st_session import STSession
from asistente_ladm_col.utils import get_ui_class

WIDGET_UI = get_ui_class('transitional_system/transitional_system_task_panel_widget.ui')


class TaskPanelWidget(QgsPanelWidget, WIDGET_UI):
    trigger_action_emitted = pyqtSignal(str)  # action tag

    def __init__(self, task_id, parent):
        QgsPanelWidget.__init__(self, parent)
        self.setupUi(self)
        self.session = STSession()
        self._task = self.session.task_manager.get_task(task_id)
        self.parent = parent
        self.logger = Logger()

        self.setDockMode(True)
        self.setPanelTitle(QCoreApplication.translate("TaskPanelWidget", "Task details"))

        self.trw_task_steps.itemDoubleClicked.connect(self.trigger_action)
        self.trw_task_steps.itemChanged.connect(self.update_step_controls)
        self.session.task_manager.task_started.connect(self.update_task)
        self.session.task_manager.task_canceled.connect(self.acceptPanel)
        self.session.task_manager.task_closed.connect(self.acceptPanel)

        self.btn_start_task.clicked.connect(self.start_task)
        self.btn_cancel_task.clicked.connect(self.cancel_task)
        self.btn_close_task.clicked.connect(self.close_task)

        self.initialize_gui()

    def initialize_gui(self):
        self.show_task_description()
        self.show_task_steps()
        self.update_controls()

    def show_task_description(self):
        if self._task is not None:
            self.logger.debug(__name__, "Setting task description in Task Panel...")
            self.lbl_name.setText(self._task.get_name())
            self.lbl_description.setText(self._task.get_description())
            self.lbl_created_at.setText(QCoreApplication.translate("TaskPanelWidget", "Created at: {}").format(self._task.get_creation_date()))
            self.lbl_started_at.setText(QCoreApplication.translate("TaskPanelWidget", "Started at: {}").format(self._task.get_started_date()))
            self.lbl_deadline.setText(QCoreApplication.translate("TaskPanelWidget", "Deadline: {}").format(self._task.get_deadline()))
            self.lbl_status.setText(self._task.get_status())

    def show_task_steps(self):
        self.trw_task_steps.clear()
        steps = self._task.get_steps()
        self.logger.debug(__name__, "Showing task steps in Task Panel. {} task steps found: {}.".format(
            len(steps), ", ".join([s.get_name() for s in steps])))

        for i, step in enumerate(steps):
            children = []
            step_item = QTreeWidgetItem([QCoreApplication.translate("TaskPanelWidget", "Step {}").format(i + 1)])
            step_item.setData(0, Qt.BackgroundRole, QBrush(GRAY_COLOR))
            step_item.setToolTip(0, step.get_name())
            step_item.setCheckState(0, Qt.Checked if step.get_status() else Qt.Unchecked)

            action_item = QTreeWidgetItem([step.get_name()])
            action_item.setData(0, Qt.UserRole, step.get_id())
            action_item.setToolTip(0, step.get_description())
            step_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            children.append(action_item)

            step_item.addChildren(children)
            self.trw_task_steps.addTopLevelItem(step_item)

        for i in range(self.trw_task_steps.topLevelItemCount()):
            self.trw_task_steps.topLevelItem(i).setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable | Qt.ItemIsSelectable)
            self.trw_task_steps.topLevelItem(i).setExpanded(True)

    def trigger_action(self, item, column):
        step_id = item.data(column, Qt.UserRole)
        step = self._task.get_step(step_id)
        if step:
            slot = step.get_custom_action_slot()
            if slot:  # Custom action call
                self.logger.info(__name__, "Executing step action with custom parameters...")
                slot[SLOT_NAME](**slot[SLOT_PARAMS])
            else:  # Default action call
                self.logger.info(__name__, "Executing default action...")
                self.trigger_action_emitted.emit(step.get_action_tag())

    def set_item_style(self, item, column):
        color = CHECKED_COLOR if item.checkState(column) == Qt.Checked else UNCHECKED_COLOR
        item.setData(column, Qt.BackgroundRole, QBrush(color))

        for index in range(item.childCount()):
            color = GRAY_COLOR if item.checkState(column) == Qt.Checked else Qt.black
            item.child(index).setData(column, Qt.ForegroundRole, QBrush(color))

    def update_step_controls(self, item, column):
        if item.childCount():  # Only do this for parents
            self.trw_task_steps.blockSignals(True)
            self.set_item_style(item, column)
            self.save_task_steps_status(column)
            self.trw_task_steps.blockSignals(False)

        self.update_close_control()

    def update_controls(self):
        # Steps panel
        self.trw_task_steps.setEnabled(self._task.get_status() == STTaskStatusEnum.STARTED.value)

        # Start task button
        self.btn_start_task.setEnabled(self._task.get_status() == STTaskStatusEnum.ASSIGNED.value)

        # Cancel task button
        self.btn_cancel_task.setEnabled(self._task.get_status() == STTaskStatusEnum.STARTED.value)

        self.update_close_control()

    def update_close_control(self):
        # Can we close the task?
        self.btn_close_task.setEnabled(self._task.get_status() == STTaskStatusEnum.STARTED.value and self.steps_complete())
        if self._task.get_status() == STTaskStatusEnum.STARTED.value and self.steps_complete():
            self.btn_close_task.setToolTip("")
        elif self._task.get_status() != STTaskStatusEnum.STARTED.value and self.steps_complete():
            self.btn_close_task.setToolTip(
                QCoreApplication.translate("TaskPanelWidget", "The task is not started yet, hence, it cannot be closed."))
        else:  # The remaining 2 cases: steps incomplete (whether the task is started or not)
            self.btn_close_task.setToolTip(
                QCoreApplication.translate("TaskPanelWidget", "You should complete the steps before closing the task."))

    def steps_complete(self):
        """
        :return: boolean --> Can we close the task
        """
        return self._task.steps_complete()

    def save_task_steps_status(self, column):
        steps_status = dict()
        for i in range(self.trw_task_steps.topLevelItemCount()):
            steps_status[i+1] = self.trw_task_steps.topLevelItem(i).checkState(column) == Qt.Checked

        # Don't save if not necessary
        status = QSettings().value("Asistente-LADM_COL/transitional_system/tasks/{}/step_status".format(self._task.get_id()), "{}")
        if status != json.dumps(steps_status):
            self._task.save_steps_status(steps_status)

    def start_task(self):
        self.session.task_manager.start_task(self.session.get_logged_st_user(), self._task.get_id())
        self.update_controls()

    def cancel_task(self):
        reply = QMessageBox.question(self,
                                     QCoreApplication.translate("TaskPanelWidget", "Confirm"),
                                     QCoreApplication.translate("TaskPanelWidget",
                                                                "Are you sure you want to cancel the task '{}'?").format(
                                         self._task.get_name()),
                                     QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            dlg = STCancelTaskDialog()
            res = dlg.exec_()
            if res == QDialog.Accepted:
                if dlg.comments:
                    self.session.task_manager.cancel_task(self.session.get_logged_st_user(),
                                                          self._task.get_id(),
                                                          dlg.comments)
            else:
                self.logger.warning_msg(__name__,
                                        QCoreApplication.translate("TaskPanelWidget", "The task was not canceled."))

    def close_task(self):
        reply = QMessageBox.question(self,
                                     QCoreApplication.translate("TaskPanelWidget", "Confirm"),
                                     QCoreApplication.translate("TaskPanelWidget",
                                                                "Are you sure you want to close the task '{}'?").format(
                                         self._task.get_name()),
                                     QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.session.task_manager.close_task(self.session.get_logged_st_user(), self._task.get_id())

    def update_task(self, task_id):
        """A task changed in the Task Manager, so, update the base task for the panel and update the panel itself"""
        self._task = self.session.task_manager.get_task(task_id)
        self.initialize_gui()