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
from qgis.PyQt.QtCore import (pyqtSignal,
                              QCoreApplication)
from qgis.core import Qgis
from qgis.gui import QgsPanelWidget

from asistente_ladm_col.config.enums import LogHandlerEnum
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.config.table_mapping_config import Names
from asistente_ladm_col.lib.st_session.st_session import STSession
from asistente_ladm_col.utils import get_ui_class

WIDGET_UI = get_ui_class('transition_system/transition_system_initial_panel_widget.ui')


class TransitionSystemInitialPanelWidget(QgsPanelWidget, WIDGET_UI):

    all_parcels_panel_requested = pyqtSignal(str)

    def __init__(self, user, parent=None):
        QgsPanelWidget.__init__(self, parent)
        self.setupUi(self)
        self._user = user
        self.logger = Logger()
        self.names = Names()
        self.session = STSession()

        self.setDockMode(True)
        self.setPanelTitle(QCoreApplication.translate("TransitionSystemInitialPanelWidget", "Transition System"))

        self.btn_logout.clicked.connect(self.logout)

        self._update_user_info()

    def _update_user_info(self):
        self.lbl_user_info.setText(
            QCoreApplication.translate("TransitionSystemInitialPanelWidget",
                                       "User: {}\nRole: {}".format(self._user.get_name(), self._user.get_role())))

    def fill_data(self):
        pass

    def logout(self):
        logged_out, msg = self.session.logout()
        self.logger.log_message(__name__, msg, Qgis.Info if logged_out else Qgis.Warning, LogHandlerEnum.MESSAGE_BAR)