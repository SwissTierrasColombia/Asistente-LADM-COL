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
from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtWidgets import (QDialog,
                                 QVBoxLayout,
                                 QRadioButton)

from asistente_ladm_col.config.enums import LogHandlerEnum
from asistente_ladm_col.lib.logger import Logger
from ...config.help_strings import HelpStrings
from asistente_ladm_col.lib.st_session.st_session import STSession

from ...utils import get_ui_class

DIALOG_UI = get_ui_class('dialogs/dlg_login_st.ui')


class LoginSTDialog(QDialog, DIALOG_UI):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.session = STSession()

        self.logger = Logger()
        self.help_strings = HelpStrings()

        #self.txt_help_page.setHtml(self.help_strings.DLG_WELCOME_SCREEN)
        #self.txt_help_page.anchorClicked.connect(self.save_template)

        self.buttonBox.accepted.connect(self.login)
        self.buttonBox.helpRequested.connect(self.show_help)

    def login(self):
        res = self.session.login(self.txt_login_user.text(), self.txt_login_password.text())
        if res:
            self.logger.info(__name__, QCoreApplication.translate("LoginSTDialog", "User logged in successfully!"), LogHandlerEnum.MESSAGE_BAR)
        else:
            self.logger.warning(__name__, QCoreApplication.translate("LoginSTDialog", "User could not access the Transition System. Try again!"), LogHandlerEnum.MESSAGE_BAR)

    def show_help(self):
        self.qgis_utils.show_help("import_from_excel")