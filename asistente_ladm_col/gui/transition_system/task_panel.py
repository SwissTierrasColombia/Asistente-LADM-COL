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

from qgis.PyQt.QtCore import (Qt,
                              pyqtSignal,
                              QCoreApplication)
from qgis.PyQt.QtGui import (QBrush,
                             QColor)
from qgis.PyQt.QtWidgets import QTreeWidgetItem
from qgis.gui import QgsPanelWidget

from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.config.table_mapping_config import Names
from asistente_ladm_col.lib.transition_system.st_session.st_session import STSession
from ...utils import get_ui_class

WIDGET_UI = get_ui_class('transition_system/transition_system_task_panel_widget.ui')


class TaskPanelWidget(QgsPanelWidget, WIDGET_UI):
    trigger_action_emitted = pyqtSignal(str)  # action tag

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

        self.trw_task_steps.itemDoubleClicked.connect(self.trigger_action)

        self.initialize_gui()

    def initialize_gui(self):
        self.show_task_description()
        self.show_task_steps()

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
        steps = self._task.get_steps()
        self.logger.debug(__name__, "Showing task steps in Task Panel. {} task steps found: {}.".format(
            len(steps), ", ".join([s.get_name() for s in steps])))

        # Create task steps model
        # Set model to view
        for i, step in enumerate(steps):
            children = []
            step_item = QTreeWidgetItem([QCoreApplication.translate("TaskPanelWidget", "Step {}").format(i + 1)])
            step_item.setData(0, Qt.BackgroundRole, QBrush(QColor(219, 219, 219, 255)))
            step_item.setToolTip(0, step.get_description())
            step_item.setCheckState(0, Qt.Checked if step.get_status() else Qt.Unchecked)

            action = step.get_action()
            action_item = QTreeWidgetItem([step.get_name()])
            action_item.setData(0, Qt.UserRole, action)
            step_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            children.append(action_item)

            step_item.addChildren(children)
            step_item.setExpanded(True)
            self.trw_task_steps.addTopLevelItem(step_item)

        for i in range(self.trw_task_steps.topLevelItemCount()):
            self.trw_task_steps.topLevelItem(i).setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable | Qt.ItemIsSelectable)
            self.trw_task_steps.topLevelItem(i).setExpanded(True)

    def trigger_action(self, item, column):
        action = item.data(column, Qt.UserRole)
        if action:
            self.trigger_action_emitted.emit(action)