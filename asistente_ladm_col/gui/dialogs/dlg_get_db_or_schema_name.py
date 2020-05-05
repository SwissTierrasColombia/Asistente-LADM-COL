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
                              QRegExp,
                              pyqtSignal)
from qgis.PyQt.QtGui import QRegExpValidator
from qgis.PyQt.QtWidgets import (QDialog,
                                 QSizePolicy,
                                 QDialogButtonBox)
from qgis.core import Qgis
from qgis.gui import QgsMessageBar

from ...utils import get_ui_class
from ...utils.qt_utils import (Validators,
                               OverrideCursor)

DIALOG_UI = get_ui_class('dialogs/dlg_get_db_or_schema_name.ui')


class GetDBOrSchemaNameDialog(QDialog, DIALOG_UI):
    db_or_schema_created = pyqtSignal(str)

    def __init__(self, db_connector, uri, type, parent=None):
        """
        Constructor
        :param db: database connection instance
        :param type: type of parameter to capture (database or schema)
        :param parent: parent of dialog
        """
        QDialog.__init__(self, parent)

        self.type = type
        self.db_connector = db_connector
        self.uri = uri
        self.parent = parent
        self.setupUi(self)

        if self.type == 'database':
            self.message_label.setText(QCoreApplication.translate("GetDBOrSchemaNameDialog", "Enter the name of the database:"))
            self.parameter_line_edit.setPlaceholderText(QCoreApplication.translate("GetDBOrSchemaNameDialog", "[Name of the database to be created]"))
        else:
            self.message_label.setText(QCoreApplication.translate("GetDBOrSchemaNameDialog", "Enter the name of the schema:"))
            self.parameter_line_edit.setPlaceholderText(QCoreApplication.translate("GetDBOrSchemaNameDialog", "[Name of the schema to be created]"))

        self.setWindowTitle(QCoreApplication.translate("GetDBOrSchemaNameDialog", "Create {type}").format(type=self.type))
        self.validators = Validators()

        # schema name mustn't have special characters
        regex = QRegExp("[a-zA-Z0-9_]+")
        validator = QRegExpValidator(regex)
        self.parameter_line_edit.setValidator(validator)
        self.parameter_line_edit.setMaxLength(63)
        self.parameter_line_edit.textChanged.connect(self.validators.validate_line_edits_lower_case)
        self.parameter_line_edit.textChanged.emit(self.parameter_line_edit.log_quality_validation_text())

        self.bar = QgsMessageBar()
        self.bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.layout().addWidget(self.bar, 0, 0, Qt.AlignTop)

        self.buttonBox.accepted.disconnect()
        self.buttonBox.accepted.connect(self.accepted)
        self.buttonBox.clear()
        self.buttonBox.addButton(QDialogButtonBox.Cancel)
        self.buttonBox.addButton(QCoreApplication.translate("GetDBOrSchemaNameDialog", "Create {type}").format(type=self.type), QDialogButtonBox.AcceptRole)

    def accepted(self):
        parameter_value = self.parameter_line_edit.log_quality_validation_text().strip()
        if not parameter_value:
            if self.type == 'database':
                self.show_message(QCoreApplication.translate("GetDBOrSchemaNameDialog", "The name of the database cannot be empty."), Qgis.Warning)
            else:
                self.show_message(QCoreApplication.translate("GetDBOrSchemaNameDialog", "The name of the schema cannot be empty."), Qgis.Warning)
            return

        tmp_db_conn = self.db_connector
        self.buttonBox.setEnabled(False)
        self.parameter_line_edit.setEnabled(False)

        with OverrideCursor(Qt.WaitCursor):
            if self.type == 'database':
                db_name = parameter_value
                result = tmp_db_conn.create_database(self.uri, db_name)
            elif self.type == 'schema':
                schema_name = parameter_value
                result = tmp_db_conn.create_schema(self.uri, schema_name)

        if result[0]:
            self.buttonBox.clear()
            self.buttonBox.setEnabled(True)
            self.buttonBox.addButton(QDialogButtonBox.Close)
            self.show_message(result[1], Qgis.Success)

            # signal updating the list of databases or schemas
            self.db_or_schema_created.emit(parameter_value)
        else:
            self.show_message(result[1], Qgis.Warning)
            self.buttonBox.setEnabled(True)
            self.parameter_line_edit.setEnabled(True)

    def show_message(self, message, level):
        self.bar.clearWidgets()  # Remove previous messages before showing a new one
        self.bar.pushMessage("Asistente LADM_COL", message, level, duration=0)
