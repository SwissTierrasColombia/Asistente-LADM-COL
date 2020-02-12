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
from qgis.PyQt.QtCore import (Qt,
                              pyqtSignal)
from qgis.gui import QgsDockWidget

from asistente_ladm_col.gui.transition_system.task_panel import TaskPanelWidget
from asistente_ladm_col.gui.transition_system.transition_system_initial_panel import TransitionSystemInitialPanelWidget
from asistente_ladm_col.utils import get_ui_class
from asistente_ladm_col.utils.qt_utils import OverrideCursor

DOCKWIDGET_UI = get_ui_class('transition_system/dockwidget_transition_system.ui')


class DockWidgetTransitionSystem(QgsDockWidget, DOCKWIDGET_UI):
    """
    Main UI for the Transition System in the LADM_COL Assistant. It holds other panels.
    """
    logout_requested = pyqtSignal()
    trigger_action_emitted = pyqtSignal(str)  # action tag

    def __init__(self, user, parent):
        super(DockWidgetTransitionSystem, self).__init__(parent)
        self.setupUi(self)
        self._user = user
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        # Configure panels
        self.task_panel = None

        self.main_panel = TransitionSystemInitialPanelWidget(user, self)
        self.main_panel.logout_requested.connect(self.logout_requested)
        self.widget.setMainPanel(self.main_panel)
        # self.main_panel.fill_data()

    def closeEvent(self, event):
        # closes open signals on panels
        # if self.parcel_panel:
        #     self.parcel_panel.close_panel()

        self.close_dock_widget()

    def update_db_connection(self, db, ladm_col_db):
        #self.close_dock_widget()  # The user needs to use the menus again, which will start everything from scratch
        pass

    def after_logout(self):
        self.close_dock_widget()

    def close_dock_widget(self):
        # try:
        #     self.utils.change_detection_layer_removed.disconnect()  # disconnect layer signals
        # except:
        #     pass

        self.close()  # The user needs to use the menus again, which will start everything from scratch

    def show_task_panel(self, task_id):
        with OverrideCursor(Qt.WaitCursor):
            if self.task_panel is not None:
                try:
                    self.widget.closePanel(self.task_panel)
                except RuntimeError as e:  # Panel in C++ could be already closed...
                    pass

                self.task_panel = None

            self.task_panel = TaskPanelWidget(task_id, self)
            self.task_panel.trigger_action_emitted.connect(self.trigger_action_emitted)
            self.task_panel.call_parent_update_controls.connect(self.update_task_controls)
            self.widget.showPanel(self.task_panel)

    def update_task_controls(self, panel):
        """Called when the task panel is accepted."""
        self.main_panel.tasks_widget.update_controls()  # If task panel is accepted, update "Close Task" button