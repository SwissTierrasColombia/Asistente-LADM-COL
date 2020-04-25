# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-11-12
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
from qgis.PyQt.QtCore import (pyqtSignal,
                              QObject)
from qgis.core import (QgsApplication,
                       Qgis,
                       QgsVectorLayer)

from asistente_ladm_col.config.enums import (EnumLogHandler,
                                             EnumLogMode)
from asistente_ladm_col.utils.singleton import SingletonQObject

TAB_NAME_FOR_LOGS = "Asistente LADM-COL"

class Logger(QObject, metaclass=SingletonQObject):
    """
    Point of access to send messages from the plugin to either the GUI or a log.
    Note that messages within a dialog are better handled by the dialog itself.

    The mode specifies whether we aim to show logs to users or devs. For the
    former, we hide debug messages, which can be too much. For the latter, we
    show everything into the QGIS log, including those messages that should be
    shown in the Message Bar or Status Bar.

    Log Handlers say where to show the log (see LogHandlerEnum).

    If log should be put into a file, enable_file_log(file_path) should be called.
    When a file log is enabled, we send all log messages to it, even those that
    should be shown in the Message Bar or Status Bar.

    Only devs can debug, but users can get a whole log by writing it to a file.
    """
    clear_message_bar_emitted = pyqtSignal()
    clear_status_bar_emitted = pyqtSignal()
    message_with_duration_emitted = pyqtSignal(str, int, int)  # Message, level, duration
    status_bar_message_emitted = pyqtSignal(str, int)  # Message, duration

    message_with_button_load_layer_emitted = pyqtSignal(str, str, str, int)  # Message, button_text, layer_name, level
    message_with_button_open_table_attributes_emitted = pyqtSignal(str, str, int, QgsVectorLayer, str)  # Message, button_text, level, layer, filter
    message_with_button_download_report_dependency_emitted = pyqtSignal(str)  # Message
    message_with_button_remove_report_dependency_emitted = pyqtSignal(str)  # Message
    message_with_buttons_change_detection_all_and_per_parcel_emitted = pyqtSignal(str)  # Message

    def __init__(self):
        QObject.__init__(self)
        self.mode = EnumLogMode.USER  # Default value
        self.log = QgsApplication.messageLog()
        self._file_log = ''

        self.message_with_button_load_layer_emitted.connect(self._log_load_layer_emitted)
        self.message_with_button_open_table_attributes_emitted.connect(self._log_open_table_attributes_emitted)
        self.message_with_button_download_report_dependency_emitted.connect(self._log_download_report_dependency_emitted)
        self.message_with_button_remove_report_dependency_emitted.connect(self._log_remove_report_emitted)
        self.message_with_buttons_change_detection_all_and_per_parcel_emitted.connect(self._log_change_detection_all_and_per_parcel_emitted)


    def set_mode(self, mode):
        self.mode = mode

    def enable_file_log(self, file_path):
        self._file_log = file_path

    def disable_file_log(self):
        self._file_log = ''

    def info(self, module_name, msg, handler=EnumLogHandler.QGIS_LOG, duration=0, tab=TAB_NAME_FOR_LOGS):
        self.log_message(module_name, msg, Qgis.Info, handler, duration, tab)

    def info_msg(self, module_name, msg, duration=0):
        self.log_message(module_name, msg, Qgis.Info, EnumLogHandler.MESSAGE_BAR, duration)

    def warning(self, module_name, msg, handler=EnumLogHandler.QGIS_LOG, duration=0, tab=TAB_NAME_FOR_LOGS):
        self.log_message(module_name, msg, Qgis.Warning, handler, duration, tab)

    def warning_msg(self, module_name, msg, duration=0):
        self.log_message(module_name, msg, Qgis.Warning, EnumLogHandler.MESSAGE_BAR, duration)

    def error(self, module_name, msg, handler=EnumLogHandler.QGIS_LOG, duration=0, tab=TAB_NAME_FOR_LOGS):
        self.log_message(module_name, msg, Qgis.Warning, handler, duration, tab)

    def error_msg(self, module_name, msg, duration=0):
        self.log_message(module_name, msg, Qgis.Warning, EnumLogHandler.MESSAGE_BAR, duration)

    def critical(self, module_name, msg, handler=EnumLogHandler.QGIS_LOG, duration=0, tab=TAB_NAME_FOR_LOGS):
        self.log_message(module_name, msg, Qgis.Critical, handler, duration, tab)

    def critical_msg(self, module_name, msg, duration=0):
        self.log_message(module_name, msg, Qgis.Critical, EnumLogHandler.MESSAGE_BAR, duration)

    def success(self, module_name, msg, handler=EnumLogHandler.QGIS_LOG, duration=0, tab=TAB_NAME_FOR_LOGS):
        self.log_message(module_name, msg, Qgis.Success, handler, duration, tab)

    def success_msg(self, module_name, msg, duration=0):
        self.log_message(module_name, msg, Qgis.Success, EnumLogHandler.MESSAGE_BAR, duration)

    def clear_message_bar(self):
        self.clear_message_bar_emitted.emit()

    def clear_status(self):
        self.status()

    def status(self, msg=None):
        if msg is None:
            self.clear_status_bar_emitted.emit()
        else:
            self.log_message("status_bar", msg, Qgis.Info, EnumLogHandler.STATUS_BAR, 0)
        QCoreApplication.processEvents()

    def debug(self, module_name, msg, handler=EnumLogHandler.QGIS_LOG, duration=0, tab=TAB_NAME_FOR_LOGS):
        """
        Here we define messages of a particular run (e.g., showing variable values or potentially long messages)
        """
        if self.mode == EnumLogMode.DEV or self._file_log:
            # Debug messages go for devs and/or for files
            self.log_message(module_name, msg, Qgis.Info, handler, duration, tab)

    def info_warning(self, module_name, result, msg, handler=EnumLogHandler.QGIS_LOG, duration=0):
        self.log_message(module_name, msg, Qgis.Info if result else Qgis.Warning, handler, duration)

    def success_warning(self, module_name, result, msg, handler=EnumLogHandler.QGIS_LOG, duration=0):
        self.log_message(module_name, msg, Qgis.Success if result else Qgis.Warning, handler, duration)

    def success_error(self, module_name, result, msg, handler=EnumLogHandler.QGIS_LOG, duration=0):
        self.log_message(module_name, msg, Qgis.Success if result else Qgis.Critical, handler, duration)

    def log_message(self, module_name, msg, level, handler=EnumLogHandler.QGIS_LOG, duration=0, tab=TAB_NAME_FOR_LOGS):
        module_name = module_name.split(".")[-1]
        call_message_log = False
        if handler == EnumLogHandler.MESSAGE_BAR:
            self.message_with_duration_emitted.emit(msg, level, duration)
            if self.mode == EnumLogMode.DEV:
                call_message_log = True
        if handler == EnumLogHandler.STATUS_BAR:
            self.status_bar_message_emitted.emit(msg, duration)
            if self.mode == EnumLogMode.DEV:
                call_message_log = True
        if handler == EnumLogHandler.QGIS_LOG:
            self.log.logMessage(f"[{module_name}] {msg}", tab, level, False)

        if call_message_log:
            self.log_message(module_name, msg, level, EnumLogHandler.QGIS_LOG)

        if self._file_log:
            # Logic to write message to file
            pass

    def _log_load_layer_emitted(self, message, button_text, layer_name, level):
        self.debug("", "A message with button load_layer ({}) was shown!".format(layer_name))

    def _log_open_table_attributes_emitted(self, message, button_text, level, layer, filter):
        self.debug("", "A message with button open_table_attributes ({}) was shown!".format(layer.name()))

    def _log_download_report_dependency_emitted(self, message):
        self.debug("", "A message with button download_report_dependency was shown!")

    def _log_remove_report_emitted(self, message):
        self.debug("", "A message with button remove_report was shown!")

    def _log_change_detection_all_and_per_parcel_emitted(self, message):
        self.debug("", "A message with buttons for change detection all and per parcel was shown!")
