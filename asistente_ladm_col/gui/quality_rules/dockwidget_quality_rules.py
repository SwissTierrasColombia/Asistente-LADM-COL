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
from qgis.PyQt.QtCore import (Qt,
                              pyqtSignal)
from qgis.gui import QgsDockWidget

from asistente_ladm_col.gui.quality_rules.quality_rules_initial_panel import QualityRulesInitialPanelWidget
from asistente_ladm_col.utils import get_ui_class
from asistente_ladm_col.utils.qt_utils import OverrideCursor

DOCKWIDGET_UI = get_ui_class('quality_rules/dockwidget_quality_rules.ui')


class DockWidgetQualityRules(QgsDockWidget, DOCKWIDGET_UI):
    """
    Main UI for the Quality Rules module. It holds other panels.
    """
    trigger_action_emitted = pyqtSignal(str)  # action tag

    def __init__(self, db, parent):
        super(DockWidgetQualityRules, self).__init__(parent)
        self.setupUi(self)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        self.__db = db

        # Configure panels
        self.task_panel = None

        self.main_panel = QualityRulesInitialPanelWidget(self)
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
            self.task_panel.panelAccepted.connect(self.reload_tasks)
            self.widget.showPanel(self.task_panel)
