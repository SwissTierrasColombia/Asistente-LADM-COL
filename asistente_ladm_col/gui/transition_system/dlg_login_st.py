# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-11-20
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
                              QCoreApplication)
from qgis.PyQt.QtWidgets import (QDialog,
                                 QVBoxLayout,
                                 QRadioButton,
                                 QSizePolicy)
from qgis.core import Qgis
from qgis.gui import QgsMessageBar

from asistente_ladm_col.config.enums import LogHandlerEnum
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.config.help_strings import HelpStrings
from asistente_ladm_col.lib.transition_system.st_session.st_session import STSession
from asistente_ladm_col.utils.qt_utils import ProcessWithStatus

from asistente_ladm_col.utils import get_ui_class

DIALOG_UI = get_ui_class('transition_system/dlg_login_st.ui')


class LoginSTDialog(QDialog, DIALOG_UI):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.session = STSession()

        self.logger = Logger()
        self.help_strings = HelpStrings()

        #self.txt_help_page.setHtml(self.help_strings.DLG_WELCOME_SCREEN)
        #self.txt_help_page.anchorClicked.connect(self.save_template)

        self.buttonBox.accepted.disconnect()
        self.buttonBox.accepted.connect(self.login)
        self.buttonBox.helpRequested.connect(self.show_help)

        self.bar = QgsMessageBar()
        self.bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.layout().addWidget(self.bar, 0, 0, Qt.AlignTop)

    def login(self):
        msg = self.logger.status(QCoreApplication.translate("LoginSTDialog", "Connecting to login service..."))
        with ProcessWithStatus(msg):
            res, msg = self.session.login(self.txt_login_user.text(), self.txt_login_password.text())

        if res:
            self.logger.info(__name__, msg, LogHandlerEnum.MESSAGE_BAR, 15)
            self.close()
        else:
            self.show_message(msg, Qgis.Warning, 0)

    def show_message(self, message, level, duration=15):
        self.bar.clearWidgets()  # Remove previous messages before showing a new one
        self.bar.pushMessage(message, level, duration)

    def show_help(self):
        self.qgis_utils.show_help("import_from_excel")