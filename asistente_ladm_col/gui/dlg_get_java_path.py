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
import re
import subprocess
from qgis.PyQt.QtCore import (Qt,
                              QCoreApplication,
                              QSettings)
from qgis.PyQt.QtWidgets import (QDialog,
                                 QSizePolicy,
                                 QDialogButtonBox)
from qgis.core import Qgis
from qgis.gui import QgsMessageBar

from ..config.general_config import JAVA_REQUIRED_VERSION
from ..utils import get_ui_class
from ..utils.qt_utils import (Validators,
                              FileValidator,
                              make_file_selector)

DIALOG_UI = get_ui_class('dlg_get_java_path.ui')


class DialogGetJavaPath(QDialog, DIALOG_UI):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.parent = parent
        self.setupUi(self)
        self.setWindowTitle(QCoreApplication.translate("DialogGetJavaPath", "Get Java Path"))

        self.java_path_line_edit.setPlaceholderText(
            QCoreApplication.translate("DialogGetJavaPath", "[By default %PATH and %JAVA_HOME is searched]"))

        self.java_path_search_button.clicked.connect(
            make_file_selector(self.java_path_line_edit,
                               QCoreApplication.translate("DialogGetJavaPath","Select Java application"),
                               QCoreApplication.translate("DialogGetJavaPath","java (*)")))

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
        self.buttonBox.addButton(QCoreApplication.translate("DialogGetJavaPath", "Set JAVA Path"),QDialogButtonBox.AcceptRole)

    def accepted(self):
        settings = QSettings()

        (is_valid, java_message) = java_path_is_valid(self.java_path_line_edit.text().strip())

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


def java_path_is_valid(java_path):
    """
    Check if java path exist
    :param java_path: (str) java path to validate
    :return: (bool, str)  True if java Path is valid, False in another case
    """
    try:
        procs_message = subprocess.check_output([java_path, '-version'], stderr=subprocess.STDOUT).decode('utf8').lower()
        types_java = ['jre', 'java', 'jdk']

        if procs_message:
            if any(type_java in procs_message for type_java in types_java):
                pattern = '\"(\d+\.\d+).*\"'
                java_version = re.search(pattern, procs_message).groups()[0]

                if java_version:
                    if float(java_version) == JAVA_REQUIRED_VERSION:
                        return (True, QCoreApplication.translate("DialogGetJavaPath", "Java path has been configured correctly."))
                    else:
                        return (False, QCoreApplication.translate("DialogGetJavaPath", "Java version is not valid. Current version is {} and must be greater than {}.").format(java_version, JAVA_REQUIRED_VERSION))

                return (False, QCoreApplication.translate("DialogGetJavaPath", "Java exists but it is not possible to know its version"))
            else:
                return (False, QCoreApplication.translate("DialogGetJavaPath", "Java path is not valid, please select a valid path..."))
        else:
            return (False, QCoreApplication.translate("DialogGetJavaPath", "Java path is not valid, please select a valid path..."))
    except Exception as e:
        return (False, QCoreApplication.translate("DialogGetJavaPath", "Java path is not valid, please select a valid path..."))
