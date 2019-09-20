# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-02-08
        git sha              : :%H$
        copyright            : (C) 2019 by Leonardo Cardona (BSF Swissphoto)
        email                : leocardonapiedrahita@gmail.com
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
                              QCoreApplication,
                              QSettings)
from qgis.PyQt.QtWidgets import (QDialog,
                                 QSizePolicy,
                                 QDialogButtonBox)
from qgis.core import Qgis
from qgis.gui import QgsMessageBar

from ...utils import get_ui_class
from ...utils.qt_utils import (Validators,
                               FileValidator,
                               make_file_selector)
from ...utils.utils import Utils

DIALOG_UI = get_ui_class('dialogs/dlg_get_java_path.ui')


class GetJavaPathDialog(QDialog, DIALOG_UI):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.parent = parent
        self.setupUi(self)
        self.setWindowTitle(QCoreApplication.translate("GetJavaPathDialog", "Get Java Path"))

        self.java_path_line_edit.setPlaceholderText(
            QCoreApplication.translate("GetJavaPathDialog", "[By default both %PATH and %JAVA_HOME are searched]"))

        self.java_path_search_button.clicked.connect(
            make_file_selector(self.java_path_line_edit,
                               QCoreApplication.translate("GetJavaPathDialog","Select Java application"),
                               QCoreApplication.translate("GetJavaPathDialog","java (*)")))

        self.java_path_line_edit.setValidator(FileValidator(is_executable=True, allow_empty=True))
        self.validators = Validators()
        self.java_path_line_edit.textChanged.connect(self.validators.validate_line_edits)

        self.bar = QgsMessageBar()
        self.bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.layout().addWidget(self.bar, 0, 0, Qt.AlignTop)

        self.buttonBox.accepted.disconnect()
        self.buttonBox.accepted.connect(self.accepted)
        self.buttonBox.clear()
        self.buttonBox.addButton(QDialogButtonBox.Cancel)
        self.buttonBox.addButton(QCoreApplication.translate("GetJavaPathDialog", "Set JAVA Path"),QDialogButtonBox.AcceptRole)

    def accepted(self):
        settings = QSettings()

        (is_valid, java_message) = Utils.java_path_is_valid(self.java_path_line_edit.text().strip())

        if is_valid:
            self.java_path_line_edit.setEnabled(False)
            settings.setValue('QgisModelBaker/ili2db/JavaPath', self.java_path_line_edit.text().strip())

            self.buttonBox.clear()
            self.buttonBox.setEnabled(True)
            self.buttonBox.addButton(QDialogButtonBox.Close)
            self.show_message(java_message, Qgis.Success)

        else:
            self.show_message(java_message, Qgis.Warning)
            return

    def show_message(self, message, level):
        self.bar.pushMessage("Asistente LADM_COL", message, level, duration=0)
