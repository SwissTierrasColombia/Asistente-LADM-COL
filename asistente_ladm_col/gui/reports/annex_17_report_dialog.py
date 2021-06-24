# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2021-03-18
        git sha              : :%H$
        copyright            : (C) 2021 by Leonardo Cardona (BSF Swissphoto)
        email                : leo dot cardona dot p at gmail dot com
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
                              QSettings,
                              QCoreApplication)
from qgis.PyQt.QtGui import QValidator
from qgis.PyQt.QtWidgets import (QDialog,
                                 QDialogButtonBox)

from asistente_ladm_col.utils.qt_utils import (make_folder_selector,
                                               DirValidator,
                                               Validators)
from asistente_ladm_col.utils import get_ui_class

DIALOG_ANNEX_17_REPORT_UI = get_ui_class('reports/annex_17_map_report_dialog.ui')


class Annex17ReportDialog(QDialog, DIALOG_ANNEX_17_REPORT_UI):
    def __init__(self, report_name):
        QDialog.__init__(self)
        self.setupUi(self)
        self.__validators = Validators()
        self.__report_name = report_name

        self.buttonBox.accepted.disconnect()
        self.buttonBox.accepted.connect(self.accepted)
        self.buttonBox.button(QDialogButtonBox.Ok).setText(QCoreApplication.translate("ReportGenerator", "Generate"))
        self.set_generate_report_button_enabled(False)

        self.btn_browse_file_folder_report.clicked.connect(make_folder_selector(self.txt_file_path_folder_report, title='Output folder', parent=None))
        self.txt_file_path_folder_report.setValidator(DirValidator(pattern=None, allow_empty_dir=True))
        self.txt_file_path_folder_report.textChanged.connect(self.__validators.validate_line_edits)
        self.txt_file_path_folder_report.textChanged.connect(self.input_data_changed)
        self.restore_settings()

        # Result variables
        self.output_folder = ''

    def set_generate_report_button_enabled(self, enable):
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(enable)

    def validate_inputs(self):
        folder_path = self.txt_file_path_folder_report.validator().validate(self.txt_file_path_folder_report.text().strip(), 0)[0]
        return folder_path == QValidator.Acceptable

    def input_data_changed(self):
        self.set_generate_report_button_enabled(self.validate_inputs())

    def accepted(self):
        """
        Set the result variables so that the report generator can get what it needs.
        """
        self.output_folder = self.txt_file_path_folder_report.text().strip()
        self.save_settings()
        self.done(QDialog.Accepted)

    def save_settings(self):
        QSettings().setValue("Asistente-LADM-COL/reports/{}/save_into_dir".format(self.__report_name), self.txt_file_path_folder_report.text().strip())

    def restore_settings(self):
        save_into_dir = QSettings().value("Asistente-LADM-COL/reports/{}/save_into_dir".format(self.__report_name), "")
        self.txt_file_path_folder_report.setText(save_into_dir)
