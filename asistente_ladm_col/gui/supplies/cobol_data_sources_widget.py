# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2020-03-18
        git sha              : :%H$
        copyright            : (C) 2020 by Germán Carrillo (BSF Swissphoto)
                               (C) 2020 by Jhon Galindo (BSF Swissphoto)
        email                : gcarrillo@linuxmail.org
                               jhonsigpjc@gmail.com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QSettings, QCoreApplication, pyqtSignal
from qgis.PyQt.QtGui import QValidator
from qgis.PyQt.QtWidgets import QWidget

from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.utils.qt_utils import (make_file_selector,
                                               make_folder_selector,
                                               FileValidator,
                                               DirValidator,
                                               Validators)
from asistente_ladm_col.utils.ui import get_ui_class

WIDGET_UI = get_ui_class('supplies/cobol_data_source_widget.ui')


class CobolDataSourceWidget(QWidget, WIDGET_UI):

    input_data_changed = pyqtSignal(bool)

    def __init__(self, ):
        QWidget.__init__(self)
        self.setupUi(self)
        self.logger = Logger()
        self.app = AppInterface()

        self.validators = Validators()

        self.restore_settings()

        self.btn_browse_file_blo.clicked.connect(
            make_file_selector(self.txt_file_path_blo, QCoreApplication.translate("CobolDataSourceWidget",
                                                                                  "Select the BLO .lis file with Cobol data "),
                               QCoreApplication.translate("CobolDataSourceWidget", 'lis File (*.lis)'),
                               folder_setting_key=self.app.settings.COBOL_FILES_DIR_KEY))

        self.btn_browse_file_uni.clicked.connect(
            make_file_selector(self.txt_file_path_uni, QCoreApplication.translate("CobolDataSourceWidget",
                                                                                  "Select the UNI .lis file with Cobol data "),
                               QCoreApplication.translate("CobolDataSourceWidget", 'lis File (*.lis)'),
                               folder_setting_key=self.app.settings.COBOL_FILES_DIR_KEY))

        self.btn_browse_file_ter.clicked.connect(
            make_file_selector(self.txt_file_path_ter, QCoreApplication.translate("CobolDataSourceWidget",
                                                                                  "Select the TER .lis file with Cobol data "),
                               QCoreApplication.translate("CobolDataSourceWidget", 'lis File (*.lis)'),
                               folder_setting_key=self.app.settings.COBOL_FILES_DIR_KEY))

        self.btn_browse_file_pro.clicked.connect(
            make_file_selector(self.txt_file_path_pro, QCoreApplication.translate("CobolDataSourceWidget",
                                                                                  "Select the PRO .lis file with Cobol data "),
                               QCoreApplication.translate("CobolDataSourceWidget", 'lis File (*.lis)'),
                               folder_setting_key=self.app.settings.COBOL_FILES_DIR_KEY))

        self.btn_browse_file_gdb.clicked.connect(
            make_folder_selector(self.txt_file_path_gdb, QCoreApplication.translate(
                "CobolDataSourceWidget", "Open GDB folder"), None, self.app.settings.COBOL_FILES_DIR_KEY))

        file_validator_blo = FileValidator(pattern='*.lis', allow_empty=True)
        file_validator_lis = FileValidator(pattern='*.lis', allow_non_existing=False)
        dir_validator_gdb = DirValidator(pattern='*.gdb', allow_non_existing=False)

        self.txt_file_path_blo.setValidator(file_validator_blo)
        self.txt_file_path_uni.setValidator(file_validator_lis)
        self.txt_file_path_ter.setValidator(file_validator_lis)
        self.txt_file_path_pro.setValidator(file_validator_lis)
        self.txt_file_path_gdb.setValidator(dir_validator_gdb)

        self.txt_file_path_blo.textChanged.connect(self.validators.validate_line_edits)
        self.txt_file_path_uni.textChanged.connect(self.validators.validate_line_edits)
        self.txt_file_path_ter.textChanged.connect(self.validators.validate_line_edits)
        self.txt_file_path_pro.textChanged.connect(self.validators.validate_line_edits)
        self.txt_file_path_gdb.textChanged.connect(self.validators.validate_line_edits)

        self.txt_file_path_blo.textChanged.connect(self.emit_input_data_changed)
        self.txt_file_path_uni.textChanged.connect(self.emit_input_data_changed)
        self.txt_file_path_ter.textChanged.connect(self.emit_input_data_changed)
        self.txt_file_path_pro.textChanged.connect(self.emit_input_data_changed)
        self.txt_file_path_gdb.textChanged.connect(self.emit_input_data_changed)

        # Trigger validations right now
        self.txt_file_path_blo.textChanged.emit(self.txt_file_path_blo.text())
        self.txt_file_path_uni.textChanged.emit(self.txt_file_path_uni.text())
        self.txt_file_path_ter.textChanged.emit(self.txt_file_path_ter.text())
        self.txt_file_path_pro.textChanged.emit(self.txt_file_path_pro.text())
        self.txt_file_path_gdb.textChanged.emit(self.txt_file_path_gdb.text())

    def validate_inputs(self):
        state_blo = self.txt_file_path_blo.validator().validate(self.txt_file_path_blo.text().strip(), 0)[0]
        state_ter = self.txt_file_path_ter.validator().validate(self.txt_file_path_ter.text().strip(), 0)[0]
        state_pro = self.txt_file_path_pro.validator().validate(self.txt_file_path_pro.text().strip(), 0)[0]
        state_uni = self.txt_file_path_uni.validator().validate(self.txt_file_path_uni.text().strip(), 0)[0]
        state_gdb = self.txt_file_path_gdb.validator().validate(self.txt_file_path_gdb.text().strip(), 0)[0]

        if state_blo == QValidator.Acceptable and \
                state_ter == QValidator.Acceptable and \
                state_pro == QValidator.Acceptable and \
                state_uni == QValidator.Acceptable and \
                state_gdb == QValidator.Acceptable:
            return True
        else:
            return False

    def emit_input_data_changed(self):
        self.input_data_changed.emit(self.validate_inputs())

    def save_settings(self):
        settings = QSettings()
        settings.setValue('Asistente-LADM-COL/etl_cobol/blo_path', self.txt_file_path_blo.text())
        settings.setValue('Asistente-LADM-COL/etl_cobol/uni_path', self.txt_file_path_uni.text())
        settings.setValue('Asistente-LADM-COL/etl_cobol/ter_path', self.txt_file_path_ter.text())
        settings.setValue('Asistente-LADM-COL/etl_cobol/pro_path', self.txt_file_path_pro.text())
        settings.setValue('Asistente-LADM-COL/etl_cobol/gdb_path', self.txt_file_path_gdb.text())

    def restore_settings(self):
        settings = QSettings()
        self.txt_file_path_blo.setText(settings.value('Asistente-LADM-COL/etl_cobol/blo_path', ''))
        self.txt_file_path_uni.setText(settings.value('Asistente-LADM-COL/etl_cobol/uni_path', ''))
        self.txt_file_path_ter.setText(settings.value('Asistente-LADM-COL/etl_cobol/ter_path', ''))
        self.txt_file_path_pro.setText(settings.value('Asistente-LADM-COL/etl_cobol/pro_path', ''))
        self.txt_file_path_gdb.setText(settings.value('Asistente-LADM-COL/etl_cobol/gdb_path', ''))