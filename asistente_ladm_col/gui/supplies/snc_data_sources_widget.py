# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2020-03-19
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
from PyQt5.QtCore import QSettings, QCoreApplication, pyqtSignal
from PyQt5.QtGui import QValidator
from qgis.PyQt.QtWidgets import QWidget

from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.utils.qt_utils import make_file_selector, make_folder_selector, FileValidator, DirValidator, \
    Validators
from asistente_ladm_col.utils.ui import get_ui_class

WIDGET_UI = get_ui_class('supplies/snc_data_source_widget.ui')


class SNCDataSourceWidget(QWidget, WIDGET_UI):

    input_data_changed = pyqtSignal(bool)

    def __init__(self, ):
        QWidget.__init__(self)
        self.setupUi(self)
        self.logger = Logger()

        self.validators = Validators()

        self.restore_settings()

        self.btn_browse_file_predio_bloqueo.clicked.connect(
            make_file_selector(self.txt_file_path_predio_bloqueo, QCoreApplication.translate("SNCDataSourceWidget",
                                                                                             "Select the predio sanción .csv file with SNC data "),
                               QCoreApplication.translate("SNCDataSourceWidget", 'CSV File (*.csv)')))

        self.btn_browse_file_predio.clicked.connect(
            make_file_selector(self.txt_file_path_predio, QCoreApplication.translate("SNCDataSourceWidget",
                                                                                     "Select the predio .csv file with SNC data "),
                               QCoreApplication.translate("SNCDataSourceWidget", 'CSV File (*.csv)')))

        self.btn_browse_file_direccion.clicked.connect(
            make_file_selector(self.txt_file_path_direccion, QCoreApplication.translate("SNCDataSourceWidget",
                                                                                        "Select the dirección .csv file with SNC data "),
                               QCoreApplication.translate("SNCDataSourceWidget", 'CSV File (*.csv)')))

        self.btn_browse_file_uni.clicked.connect(
            make_file_selector(self.txt_file_path_uni, QCoreApplication.translate("SNCDataSourceWidget",
                                                                                  "Select the unidad construcción .csv file with SNC data "),
                               QCoreApplication.translate("SNCDataSourceWidget", 'CSV File (*.csv)')))

        self.btn_browse_file_uni_comp.clicked.connect(
            make_file_selector(self.txt_file_path_uni_comp, QCoreApplication.translate("SNCDataSourceWidget",
                                                                                  "Select the unidad construcción comp .csv file with SNC data "),
                               QCoreApplication.translate("SNCDataSourceWidget", 'CSV File (*.csv)')))

        self.btn_browse_file_persona.clicked.connect(
            make_file_selector(self.txt_file_path_persona, QCoreApplication.translate("SNCDataSourceWidget",
                                                                                      "Select the persona .csv file with SNC data "),
                               QCoreApplication.translate("SNCDataSourceWidget", 'CSV File (*.csv)')))

        self.btn_browse_file_persona_predio.clicked.connect(
            make_file_selector(self.txt_file_path_persona_predio, QCoreApplication.translate("SNCDataSourceWidget",
                                                                                      "Select the persona predio .csv file with SNC data "),
                               QCoreApplication.translate("SNCDataSourceWidget", 'CSV File (*.csv)')))

        self.btn_browse_file_ficha_m.clicked.connect(
            make_file_selector(self.txt_file_path_ficha_m, QCoreApplication.translate("SNCDataSourceWidget",
                                                                                      "Select the ficha matriz .csv file with SNC data "),
                               QCoreApplication.translate("SNCDataSourceWidget", 'CSV File (*.csv)')))

        self.btn_browse_file_ficha_m_predio.clicked.connect(
            make_file_selector(self.txt_file_path_ficha_m_predio, QCoreApplication.translate("SNCDataSourceWidget",
                                                                                             "Select the ficha matriz predio .csv file with SNC data "),
                               QCoreApplication.translate("SNCDataSourceWidget", 'CSV File (*.csv)')))

        self.btn_browse_file_ficha_m_torre.clicked.connect(
            make_file_selector(self.txt_file_path_ficha_m_torre, QCoreApplication.translate("SNCDataSourceWidget",
                                                                                             "Select the ficha matriz torre .csv file with SNC data "),
                               QCoreApplication.translate("SNCDataSourceWidget", 'CSV File (*.csv)')))

        self.btn_browse_file_gdb.clicked.connect(
            make_folder_selector(self.txt_file_path_gdb, title=QCoreApplication.translate(
                "SNCDataSourceWidget", "Open GDB folder"), parent=None))

        file_validator_optional = FileValidator(pattern='*.csv', allow_empty=True)
        file_validator_csv = FileValidator(pattern='*.csv', allow_non_existing=False)
        dir_validator_gdb = DirValidator(pattern='*.gdb', allow_non_existing=False)

        self.txt_file_path_predio_bloqueo.setValidator(file_validator_optional)
        self.txt_file_path_predio.setValidator(file_validator_csv)
        self.txt_file_path_direccion.setValidator(file_validator_csv)
        self.txt_file_path_uni.setValidator(file_validator_csv)
        self.txt_file_path_uni_comp.setValidator(file_validator_csv)
        self.txt_file_path_persona.setValidator(file_validator_csv)
        self.txt_file_path_persona_predio.setValidator(file_validator_csv)
        self.txt_file_path_ficha_m.setValidator(file_validator_optional)
        self.txt_file_path_ficha_m_predio.setValidator(file_validator_optional)
        self.txt_file_path_ficha_m_torre.setValidator(file_validator_optional)
        self.txt_file_path_gdb.setValidator(dir_validator_gdb)

        self.txt_file_path_predio_bloqueo.textChanged.connect(self.validators.validate_line_edits)
        self.txt_file_path_predio.textChanged.connect(self.validators.validate_line_edits)
        self.txt_file_path_direccion.textChanged.connect(self.validators.validate_line_edits)
        self.txt_file_path_uni.textChanged.connect(self.validators.validate_line_edits)
        self.txt_file_path_uni_comp.textChanged.connect(self.validators.validate_line_edits)
        self.txt_file_path_persona.textChanged.connect(self.validators.validate_line_edits)
        self.txt_file_path_persona_predio.textChanged.connect(self.validators.validate_line_edits)
        self.txt_file_path_ficha_m.textChanged.connect(self.validators.validate_line_edits)
        self.txt_file_path_ficha_m_predio.textChanged.connect(self.validators.validate_line_edits)
        self.txt_file_path_ficha_m_torre.textChanged.connect(self.validators.validate_line_edits)
        self.txt_file_path_gdb.textChanged.connect(self.validators.validate_line_edits)

        self.txt_file_path_predio_bloqueo.textChanged.connect(self.emit_input_data_changed)
        self.txt_file_path_predio.textChanged.connect(self.emit_input_data_changed)
        self.txt_file_path_direccion.textChanged.connect(self.emit_input_data_changed)
        self.txt_file_path_uni.textChanged.connect(self.emit_input_data_changed)
        self.txt_file_path_uni_comp.textChanged.connect(self.emit_input_data_changed)
        self.txt_file_path_persona.textChanged.connect(self.emit_input_data_changed)
        self.txt_file_path_persona_predio.textChanged.connect(self.emit_input_data_changed)
        self.txt_file_path_ficha_m.textChanged.connect(self.emit_input_data_changed)
        self.txt_file_path_ficha_m_predio.textChanged.connect(self.emit_input_data_changed)
        self.txt_file_path_ficha_m_torre.textChanged.connect(self.emit_input_data_changed)
        self.txt_file_path_gdb.textChanged.connect(self.emit_input_data_changed)

        # Trigger validations right now
        self.txt_file_path_predio_bloqueo.textChanged.emit(self.txt_file_path_predio_bloqueo.text())
        self.txt_file_path_predio.textChanged.emit(self.txt_file_path_predio.text())
        self.txt_file_path_direccion.textChanged.emit(self.txt_file_path_direccion.text())
        self.txt_file_path_uni.textChanged.emit(self.txt_file_path_uni.text())
        self.txt_file_path_uni_comp.textChanged.emit(self.txt_file_path_uni_comp.text())
        self.txt_file_path_persona.textChanged.emit(self.txt_file_path_persona.text())
        self.txt_file_path_persona_predio.textChanged.emit(self.txt_file_path_persona_predio.text())
        self.txt_file_path_ficha_m.textChanged.emit(self.txt_file_path_ficha_m.text())
        self.txt_file_path_ficha_m_predio.textChanged.emit(self.txt_file_path_ficha_m_predio.text())
        self.txt_file_path_ficha_m_torre.textChanged.emit(self.txt_file_path_ficha_m_torre.text())
        self.txt_file_path_gdb.textChanged.emit(self.txt_file_path_gdb.text())

    def validate_inputs(self):
        state_predio_sancion = self.txt_file_path_predio_bloqueo.validator().validate(self.txt_file_path_predio_bloqueo.text().strip(), 0)[0]
        state_predio = self.txt_file_path_predio.validator().validate(self.txt_file_path_predio.text().strip(), 0)[0]
        state_direccion = self.txt_file_path_direccion.validator().validate(self.txt_file_path_direccion.text().strip(), 0)[0]
        state_uni = self.txt_file_path_uni.validator().validate(self.txt_file_path_uni.text().strip(), 0)[0]
        state_uni_comp = self.txt_file_path_uni_comp.validator().validate(self.txt_file_path_uni_comp.text().strip(), 0)[0]
        state_persona = self.txt_file_path_persona.validator().validate(self.txt_file_path_persona.text().strip(), 0)[0]
        state_persona_predio = self.txt_file_path_persona_predio.validator().validate(self.txt_file_path_persona_predio.text().strip(), 0)[0]
        state_ficha_m = self.txt_file_path_ficha_m.validator().validate(self.txt_file_path_ficha_m.text().strip(), 0)[0]
        state_ficha_m_predio = self.txt_file_path_ficha_m_predio.validator().validate(self.txt_file_path_ficha_m_predio.text().strip(), 0)[0]
        state_ficha_m_torre = self.txt_file_path_ficha_m_torre.validator().validate(self.txt_file_path_ficha_m_torre.text().strip(), 0)[0]
        state_gdb = self.txt_file_path_gdb.validator().validate(self.txt_file_path_gdb.text().strip(), 0)[0]

        if state_predio_sancion == QValidator.Acceptable and \
                state_predio == QValidator.Acceptable and \
                state_direccion == QValidator.Acceptable and \
                state_uni == QValidator.Acceptable and \
                state_persona == QValidator.Acceptable and \
                state_persona_predio == QValidator.Acceptable and \
                state_ficha_m == QValidator.Acceptable and \
                state_ficha_m_predio == QValidator.Acceptable and \
                state_ficha_m_torre == QValidator.Acceptable and \
                state_gdb == QValidator.Acceptable:
            return True
        else:
            return False

    def emit_input_data_changed(self):
        self.input_data_changed.emit(self.validate_inputs())

    def save_settings(self):
        settings = QSettings()
        settings.setValue('Asistente-LADM-COL/etl_snc/predio_bloqueo_path', self.txt_file_path_predio_bloqueo.text())
        settings.setValue('Asistente-LADM-COL/etl_snc/predio_path', self.txt_file_path_predio.text())
        settings.setValue('Asistente-LADM-COL/etl_snc/direccion_path', self.txt_file_path_direccion.text())
        settings.setValue('Asistente-LADM-COL/etl_snc/uni_path', self.txt_file_path_uni.text())
        settings.setValue('Asistente-LADM-COL/etl_snc/uni_comp_path', self.txt_file_path_uni_comp.text())
        settings.setValue('Asistente-LADM-COL/etl_snc/persona_path', self.txt_file_path_persona.text())
        settings.setValue('Asistente-LADM-COL/etl_snc/persona_predio_path', self.txt_file_path_persona_predio.text())
        settings.setValue('Asistente-LADM-COL/etl_snc/ficha_m_path', self.txt_file_path_ficha_m.text())
        settings.setValue('Asistente-LADM-COL/etl_snc/ficha_m_predio_path', self.txt_file_path_ficha_m_predio.text())
        settings.setValue('Asistente-LADM-COL/etl_snc/ficha_m_torre_path', self.txt_file_path_ficha_m_torre.text())
        settings.setValue('Asistente-LADM-COL/etl_snc/gdb_path', self.txt_file_path_gdb.text())

    def restore_settings(self):
        settings = QSettings()
        self.txt_file_path_predio_bloqueo.setText(settings.value('Asistente-LADM-COL/etl_snc/predio_bloqueo_path', ''))
        self.txt_file_path_predio.setText(settings.value('Asistente-LADM-COL/etl_snc/predio_path', ''))
        self.txt_file_path_direccion.setText(settings.value('Asistente-LADM-COL/etl_snc/direccion_path', ''))
        self.txt_file_path_uni.setText(settings.value('Asistente-LADM-COL/etl_snc/uni_path', ''))
        self.txt_file_path_uni_comp.setText(settings.value('Asistente-LADM-COL/etl_snc/uni_comp_path', ''))
        self.txt_file_path_persona.setText(settings.value('Asistente-LADM-COL/etl_snc/persona_path', ''))
        self.txt_file_path_persona_predio.setText(settings.value('Asistente-LADM-COL/etl_snc/persona_predio_path', ''))
        self.txt_file_path_ficha_m.setText(settings.value('Asistente-LADM-COL/etl_snc/ficha_m_path', ''))
        self.txt_file_path_ficha_m_predio.setText(settings.value('Asistente-LADM-COL/etl_snc/ficha_m_predio_path', ''))
        self.txt_file_path_ficha_m_torre.setText(settings.value('Asistente-LADM-COL/etl_snc/ficha_m_torre_path', ''))
        self.txt_file_path_gdb.setText(settings.value('Asistente-LADM-COL/etl_snc/gdb_path', ''))