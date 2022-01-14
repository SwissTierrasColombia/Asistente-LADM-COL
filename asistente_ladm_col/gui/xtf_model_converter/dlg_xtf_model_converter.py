"""
/***************************************************************************
                              Asistente LADM-COL
                             --------------------
        begin           : 2021-01-29
        git sha         : :%H$
        copyright       : (C) 2021 by Sergio Ramírez (SwissTierras Colombia)
                          (C) 2021 by Germán Carrillo (SwissTierras Colombia)
        email           : seralra96@gmail.com
                          gcarrillo@linuxmail.org
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
from qgis.core import Qgis
from qgis.gui import QgsMessageBar

from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.utils.qt_utils import (FileValidator,
                                               Validators,
                                               make_file_selector,
                                               make_save_file_selector,
                                               ProcessWithStatus)
from asistente_ladm_col.utils import get_ui_class

DIALOG_XTF_MODEL_CONVERTER_UI = get_ui_class('xtf_model_converter/dlg_xtf_model_converter.ui')


class XTFModelConverterDialog(QDialog, DIALOG_XTF_MODEL_CONVERTER_UI):
    on_result = pyqtSignal(bool)  # whether the tool was run successfully or not

    def __init__(self, controller, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self._controller = controller
        self.parent = parent

        self.logger = Logger()
        self.app = AppInterface()
        self.validators = Validators()

        self._dialog_mode = None
        self._running_tool = False        
        self.tool_name = QCoreApplication.translate("XTFModelConverterDialog", "XTF Model Converter")
 
        # Initialize
        self.initialize_progress()

        # Set MessageBar for QDialog
        self.bar = QgsMessageBar()
        self.bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.layout().addWidget(self.bar, 0, 0, Qt.AlignTop)

        # Set connections
        self.buttonBox.accepted.disconnect()
        self.buttonBox.accepted.connect(self.accepted)
        self.buttonBox.button(QDialogButtonBox.Ok).setText(QCoreApplication.translate("XTFModelConverterDialog", "Convert"))
        self.finished.connect(self.finished_slot)

        self.btn_browse_file_source_xtf.clicked.connect(
            make_file_selector(self.txt_source_xtf, QCoreApplication.translate("XTFModelConverterDialog",
                        "Select the INTERLIS Transfer File .xtf file you want to convert"),
                        QCoreApplication.translate("XTFModelConverterDialog", 'Transfer file (*.xtf)')))

        self.btn_browse_file_target_xtf.clicked.connect(
            make_save_file_selector(self.txt_target_xtf, QCoreApplication.translate(
                "XTFModelConverterDialog", "Set the output path of the coverted INTERLIS Transfer File"),
                                    QCoreApplication.translate("XTFModelConverterDialog", 'Transfer file (*.xtf)'),
                                    extension='.xtf'))

        self._controller.progress_changed.connect(self.progress.setValue)

        self.restore_settings()

        # Set validations
        file_validator_xtf_in = FileValidator(pattern='*.xtf', allow_non_existing=False)
        file_validator_xtf_out = FileValidator(pattern='*.xtf', allow_non_existing=True)

        self.txt_source_xtf.setValidator(file_validator_xtf_in)
        self.txt_target_xtf.setValidator(file_validator_xtf_out)

        self.txt_source_xtf.textChanged.connect(self.validators.validate_line_edits)
        self.txt_target_xtf.textChanged.connect(self.validators.validate_line_edits)

        self.txt_source_xtf.textChanged.connect(self.update_model_converters)
        self.txt_source_xtf.textChanged.connect(self.xtf_paths_changed)  # Enable/disable convert button
        self.txt_target_xtf.textChanged.connect(self.xtf_paths_changed)  # Enable/disable convert button
        self.cbo_model_converter.currentIndexChanged.connect(self.selected_converter_changed)  # Need new wizard pages?

        # Trigger validators now
        self.txt_source_xtf.textChanged.emit(self.txt_source_xtf.text())
        self.txt_target_xtf.textChanged.emit(self.txt_target_xtf.text())

    def progress_changed(self, value):
        QCoreApplication.processEvents()  # Listen to cancel from the user
        self.progress.setValue(value)

    def accepted(self):
        self.save_settings()

        self.bar.clearWidgets()  # Remove previous messages
        self.set_gui_controls_enabled(False)
        self.progress.setVisible(True)

        msg = QCoreApplication.translate("XTFModelConverterDialog", "Converting XTF data (this might take a while)...")
        with ProcessWithStatus(msg):
            params = {}
            res, msg = self._controller.convert(self.cbo_model_converter.currentData(),
                                                self.txt_source_xtf.text(),
                                                self.txt_target_xtf.text(),
                                                params)
            self.show_message(msg, Qgis.Success if res else Qgis.Warning)
            self.logger.success_warning(__name__, res, msg)

        self.set_gui_controls_enabled(True)

    def reject(self):
        if self._running_tool:
            reply = QMessageBox.question(self,
                                         QCoreApplication.translate("XTFModelConverterDialog", "Warning"),
                                         QCoreApplication.translate("XTFModelConverterDialog",
                                                                    "The '{}' tool is still running. Do you want to cancel it? If you cancel, the data might be incomplete in the target database.").format(self.tool_name),
                                         QMessageBox.Yes, QMessageBox.No)

            if reply == QMessageBox.Yes:
                self._running_tool = False
                msg = QCoreApplication.translate("XTFModelConverterDialog", "The '{}' tool was cancelled.").format(self.tool_name)
                self.logger.info(__name__, msg)
                self.show_message(msg, Qgis.Info)
        else:
            self.logger.info(__name__, "Dialog closed.")
            self.done(1)

    def finished_slot(self, result):
        self.bar.clearWidgets()

    def xtf_paths_changed(self):
        # Enable/disable 'Convert' button
        state_source_xtf = self.__source_xtf_is_valid()
        state_target_xtf = self.txt_target_xtf.validator().validate(self.txt_target_xtf.text().strip(), 0)[0] == QValidator.Acceptable

        state_converter = self.cbo_model_converter.count() and self.cbo_model_converter.currentData() != "invalid"

        self.set_convert_button_enabled(state_source_xtf and state_converter and state_target_xtf)

    def __source_xtf_is_valid(self):
        return self.txt_source_xtf.validator().validate(self.txt_source_xtf.text().strip(), 0)[0] == QValidator.Acceptable

    def selected_converter_changed(self, index):
        # Ideas for this:
        #   Some converters might need new wizard pages. So this slot should get them from the controller
        #   and pass them to a method that shows them, converting first the single-page wizard into multi-page.
        pass

    def set_convert_button_enabled(self, enable):
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(enable)

    def update_model_converters(self):
        self.cbo_model_converter.clear()

        if self.__source_xtf_is_valid():
            self.cbo_model_converter.setEnabled(True)
            source_xtf = self.txt_source_xtf.text().strip()
            for key, text in self._controller.get_converters(source_xtf).items():
                self.cbo_model_converter.addItem(text, key)

            if not self.cbo_model_converter.count():
                self.cbo_model_converter.addItem(QCoreApplication.translate("XTFModelConverterDialog",
                                                                            "No converter found for the given source XTF"), "invalid")
        else:
            if not self.cbo_model_converter.count():
                self.cbo_model_converter.setEnabled(False)

    def initialize_progress(self):
        self.progress.setValue(0)
        self.progress.setVisible(False)

    def set_gui_controls_enabled(self, enable):
        self.set_convert_button_enabled(enable)
        self.gbx_parameters.setEnabled(enable)

    def save_settings(self):
        settings = QSettings()
        settings.setValue('Asistente-LADM-COL/xtf_model_converter/xtf_in_path', self.txt_source_xtf.text())
        settings.setValue('Asistente-LADM-COL/xtf_model_converter/xtf_out_path', self.txt_target_xtf.text())

        # In the main page (source-target configuration), save if splitter is closed
        self.app.settings.xtf_converter_splitter_collapsed = self.splitter.sizes()[1] == 0
        
    def restore_settings(self):
        settings = QSettings()
        self.txt_source_xtf.setText(settings.value('Asistente-LADM-COL/xtf_model_converter/xtf_in_path', ''))
        self.txt_target_xtf.setText(settings.value('Asistente-LADM-COL/xtf_model_converter/xtf_out_path', ''))

        # If splitter in the main page was closed before, set it as closed again
        if self.app.settings.xtf_converter_splitter_collapsed:
            sizes = self.splitter.sizes()
            self.splitter.setSizes([sizes[0], 0])
        
    def show_message(self, message, level, duration=0):
        self.bar.clearWidgets()  # Remove previous messages before showing a new one
        self.bar.pushMessage(message, level, duration)
