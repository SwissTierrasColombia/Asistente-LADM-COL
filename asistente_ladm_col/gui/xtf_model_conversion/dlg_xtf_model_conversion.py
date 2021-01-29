# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2021-01-29
        git sha              : :%H$
        copyright            : (C) 2021 by Sergio Ramírez (SwissTierras Colombia)
        email                : seralra96@gmail.com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtWidgets import (QDialog,
                                 QMessageBox,
                                 QDialogButtonBox,
                                 QSizePolicy)
from qgis.PyQt.QtCore import (Qt,
                              QSettings,
                              QCoreApplication,
                              pyqtSignal)
from qgis.PyQt.QtGui import QValidator
from qgis.core import (Qgis,
                       QgsProject,
                       QgsVectorLayer)
from qgis.gui import QgsMessageBar

from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.utils.qt_utils import (FileValidator,
                                               DirValidator,
                                               NonEmptyStringValidator,
                                               Validators,
                                               normalize_local_url,
                                               make_file_selector,
                                               make_folder_selector)
from asistente_ladm_col.utils import get_ui_class
from asistente_ladm_col.lib.processing.custom_processing_feedback import CustomFeedback

DIALOG_LOG_EXCEL_UI = get_ui_class('xtf_model_conversion/dlg_xtf_model_conversion.ui')


class XtfModelConversionDialog(QDialog, DIALOG_LOG_EXCEL_UI):
    on_result = pyqtSignal(bool)  # whether the tool was run successfully or not

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.parent = parent

        self.logger = Logger()
        self.app = AppInterface()
        self.validators = Validators()

        self._dialog_mode = None
        self._running_tool = False        
        self.tool_name = QCoreApplication.translate("XtfModelConversionDialog", "XTF Model Conversion")
 
        # Initialize
        self.initialize_feedback()

        # Set MessageBar for QDialog
        self.bar = QgsMessageBar()
        self.bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.layout().addWidget(self.bar, 0, 0, Qt.AlignTop)

        # Set connections
        self.buttonBox.accepted.disconnect()
        self.buttonBox.accepted.connect(self.accepted)
        self.buttonBox.button(QDialogButtonBox.Ok).setText(QCoreApplication.translate("XtfModelConversionDialog", "Convert"))
        self.finished.connect(self.finished_slot)

        self.btn_browse_file_xtf_in.clicked.connect(
            make_file_selector(self.txt_file_path_xtf_in, QCoreApplication.translate("XtfModelConversionDialog",
                        "Select the INTERLIS Transfer File .xtf file you want to convert"),
                        QCoreApplication.translate("XtfModelConversionDialog", 'XTF File (*.xtf)')))

        self.btn_browse_file_xtf_out.clicked.connect(
                make_file_selector(self.txt_file_path_xtf_out, QCoreApplication.translate(
                "XtfModelConversionDialog", "Set the INTERLIS Transfer File .xtf to export"),
                        QCoreApplication.translate("XtfModelConversionDialog", 'XTF File (*.xtf)')))

        # Set validations
        file_validator_xtf_in = FileValidator(pattern='*.xtf', allow_non_existing=False)
        file_validator_xtf_out = FileValidator(pattern='*.xtf', allow_non_existing=True)
        non_empty_validator_name = NonEmptyStringValidator()

        self.txt_file_path_xtf_in.setValidator(file_validator_xtf_in)
        self.txt_file_path_xtf_out.setValidator(file_validator_xtf_out)

        self.txt_file_path_xtf_in.textChanged.connect(self.validators.validate_line_edits)
        self.txt_file_path_xtf_out.textChanged.connect(self.validators.validate_line_edits)
        
        self.txt_file_path_xtf_in.textChanged.connect(self.input_data_changed)
        self.txt_file_path_xtf_out.textChanged.connect(self.input_data_changed)

    def progress_configuration(self, base, num_process):
        """
        :param base: Where to start counting from
        :param num_process: Number of steps
        """
        self.progress_base = base
        self.progress_maximum = 100 * num_process
        self.progress.setMaximum(self.progress_maximum)

    def progress_changed(self):
        QCoreApplication.processEvents()  # Listen to cancel from the user
        self.progress.setValue(self.progress_base + self.custom_feedback.progress())

    def reject(self):
        if self._running_tool:
            reply = QMessageBox.question(self,
                                         QCoreApplication.translate("XtfModelConversionDialog", "Warning"),
                                         QCoreApplication.translate("XtfModelConversionDialog",
                                                                    "The '{}' tool is still running. Do you want to cancel it? If you cancel, the data might be incomplete in the target database.").format(self.tool_name),
                                         QMessageBox.Yes, QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.custom_feedback.cancel()
                self._running_tool = False
                msg = QCoreApplication.translate("XtfModelConversionDialog", "The '{}' tool was cancelled.").format(self.tool_name)
                self.logger.info(__name__, msg)
                self.show_message(msg, Qgis.Info)
        else:
            self.logger.info(__name__, "Dialog closed.")
            self.done(1)

    def finished_slot(self, result):
        self.bar.clearWidgets()

    def input_data_changed(self):
        self.set_import_button_enabled(self.validate_inputs())

    def set_import_button_enabled(self, enable):
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(enable)

    def validate_inputs(self):
        raise NotImplementedError

    def validate_common_inputs(self):
        return self.txt_file_path_gdb.validator().validate(self.txt_file_path_gdb.text().strip(), 0)[0] == QValidator.Acceptable

    def initialize_feedback(self):
        self.progress.setValue(0)
        self.progress.setVisible(False)
        self.custom_feedback = CustomFeedback()
        self.custom_feedback.progressChanged.connect(self.progress_changed)
        self.set_gui_controls_enabled(True)

    def set_gui_controls_enabled(self, enable):
        if self.buttonBox.button(QDialogButtonBox.Ok) is not None:  # It's None if the tool finished successfully
            self.set_import_button_enabled(enable)

    def save_settings(self, system):
        settings = QSettings()
        settings.setValue('Asistente-LADM-COL/xtf_model_conversion_{}/xtf_in_path'.format(system), self.txt_file_path_xtf_in.text())
        settings.setValue('Asistente-LADM-COL/xtf_model_conversion_{}/xtf_out_path'.format(system), self.txt_file_path_xtf_out.text())
        
    def restore_settings(self, system):
        settings = QSettings()
        self.txt_file_path_xtf_in.setText(settings.value('Asistente-LADM-COL/xtf_model_conversion_{}/xtf_in_path'.format(system), ''))
        self.txt_file_path_xtf_out.setText(settings.value('Asistente-LADM-COL/xtf_model_conversion_{}/xtf_out_path'.format(system), ''))
        
    def show_message(self, message, level):
        self.bar.clearWidgets()  # Remove previous messages before showing a new one
        self.bar.pushMessage(message, level, 15)