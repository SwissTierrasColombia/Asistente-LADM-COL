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
                              pyqtSignal,
                              QCoreApplication)
from qgis.gui import QgsDockWidget


from asistente_ladm_col.gui.quality_rules.quality_rules_error_results_panel import QualityRulesErrorResultsPanelWidget
from asistente_ladm_col.gui.quality_rules.quality_rules_general_results_panel import QualityRulesGeneralResultsPanelWidget
from asistente_ladm_col.gui.quality_rules.quality_rules_initial_panel import QualityRulesInitialPanelWidget
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.utils import get_ui_class
from asistente_ladm_col.utils.qt_utils import OverrideCursor

DOCKWIDGET_UI = get_ui_class('quality_rules/dockwidget_quality_rules.ui')


class DockWidgetQualityRules(QgsDockWidget, DOCKWIDGET_UI):
    """
    Main UI for the Quality Rules module. It holds other panels.
    """
    trigger_action_emitted = pyqtSignal(str)  # action tag

    def __init__(self, controller, parent):
        super(DockWidgetQualityRules, self).__init__(parent)
        self.setupUi(self)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        self.__controller = controller
        self.__controller.quality_rule_layer_removed.connect(self.__layer_removed)

        self.logger = Logger()

        # Configure panels
        self.__general_results_panel = None
        self.__error_results_panel = None

        self.__main_panel = QualityRulesInitialPanelWidget(controller, self)
        self.widget.setMainPanel(self.__main_panel)

    def __layer_removed(self):
        self.logger.info_msg(__name__, QCoreApplication.translate("DockWidgetQualityRules",
                                                                  "'Quality rules panel' has been initialized because you just removed a required layer."))

        # Go back to initial panel when the user removes QR DB layers
        # Note this closes open signals on panels, reset controller variables
        # and even removes the whole QR DB group!
        self.widget.acceptAllPanels()

    def closeEvent(self, event):
        # Note this closes open signals on panels, reset controller variables
        # and even removes the whole QR DB group!
        self.widget.acceptAllPanels()

        self.close_dock_widget()

    def update_db_connection(self, db, ladm_col_db, db_source):
        self.close_dock_widget()  # The user needs to use the menus again, which will start everything from scratch

    def close_dock_widget(self):
        self.close()  # The user needs to use the menus again, which will start everything from scratch

    def show_general_results_panel(self):
        with OverrideCursor(Qt.WaitCursor):
            self.__delete_general_result_panel()

            self.__general_results_panel = QualityRulesGeneralResultsPanelWidget(self.__controller, self)
            self.__controller.total_progress_changed.connect(self.__general_results_panel.update_total_progress)
            self.__general_results_panel.panelAccepted.connect(self.__controller.reset_vars_for_general_results_panel)
            self.widget.showPanel(self.__general_results_panel)
            self.__controller.validate_qrs()

    def __delete_general_result_panel(self):
        if self.__general_results_panel is not None:
            try:
                self.widget.closePanel(self.__general_results_panel)
            except RuntimeError as e:  # Panel in C++ could be already closed...
                pass

            self.__general_results_panel = None

    def show_error_results_panel(self):
        with OverrideCursor(Qt.WaitCursor):
            if self.__error_results_panel is not None:
                try:
                    self.widget.closePanel(self.__error_results_panel)
                except RuntimeError as e:  # Panel in C++ could be already closed...
                    pass

                self.__error_results_panel = None

            self.__error_results_panel = QualityRulesErrorResultsPanelWidget(self.__controller, self)
            self.__error_results_panel.panelAccepted.connect(self.__controller.reset_vars_for_error_results_panel)
            self.widget.showPanel(self.__error_results_panel)
