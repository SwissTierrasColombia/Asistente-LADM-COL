# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-11-07
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
from functools import partial

from qgis.core import QgsApplication

from qgis.PyQt.QtWidgets import (QDialog,
                                 QVBoxLayout,
                                 QRadioButton)

from ...config.help_strings import HelpStrings
from asistente_ladm_col.gui.gui_builder.role_registry import Role_Registry

from ...utils import get_ui_class

DIALOG_UI = get_ui_class('dialogs/dlg_welcome_screen.ui')


class WelcomeScreenDialog(QDialog, DIALOG_UI):
    def __init__(self, qgis_utils, parent):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.qgis_utils = qgis_utils
        self.log = QgsApplication.messageLog()
        self.help_strings = HelpStrings()

        #self.txt_help_page.setHtml(self.help_strings.DLG_WELCOME_SCREEN)
        #self.txt_help_page.anchorClicked.connect(self.save_template)

        self.finished.connect(self.finish_dialog)
        self.buttonBox.helpRequested.connect(self.show_help)

        self.gbx_layout = QVBoxLayout()
        self.roles = Role_Registry()
        self.dict_roles = self.roles.get_roles_info()
        checked = False

        # Initialize radio buttons
        for k,v in self.dict_roles.items():
            radio = QRadioButton(v)
            if not checked:  # Only for the first item
                radio.setChecked(True)
                checked = True
                self.show_description(self.roles.get_role_description(k), checked)  # Initialize help page

            radio.toggled.connect(partial(self.show_description, self.roles.get_role_description(k)))
            self.gbx_layout.addWidget(radio)

        self.gbx_options.setLayout(self.gbx_layout)

    def finish_dialog(self, result):
        if result == 0:
            self.roles.set_active_default_role()
        else:
            self.set_checked_role_active()

    def show_description(self, description, checked):
        if checked:
            self.txt_help_page.setHtml(description)

    def set_checked_role_active(self):
        radio_checked = None
        for i in range(self.gbx_layout.count()):
            radio = self.gbx_layout.itemAt(i).widget()
            if radio.isChecked():
                radio_checked = radio.text()
                break

        for k, v in self.dict_roles.items():
            if v == radio_checked:
                self.roles.set_active_role(k)
                break

    def show_help(self):
        self.qgis_utils.show_help("import_from_excel")