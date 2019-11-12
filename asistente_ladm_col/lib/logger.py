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
from qgis.PyQt.QtCore import (pyqtSignal,
                              QObject)
from qgis.core import (QgsApplication,
                       Qgis)

from asistente_ladm_col import PLUGIN_NAME
from asistente_ladm_col.config.enums import (LogHandlerEnum,
                                             LogModeEnum)
from asistente_ladm_col.utils.singleton import SingletonQObject

class Logger(QObject, metaclass=SingletonQObject):
    """
    Point of access to send messages from the plugin to either the GUI or a log.
    Note that messages within a dialog are better handled by the dialog itself.

    Only devs can debug, but users can get a whole log by writing it to a file.
    """
    message_emitted = pyqtSignal(str, int)  # Message, level
    message_with_duration_emitted = pyqtSignal(str, int, int)  # Message, level, duration
    status_bar_message_emitted = pyqtSignal(str, int)  # Message, duration

    def __init__(self):
        QObject.__init__(self)
        self.mode = LogModeEnum.USER  # Default value
        self.log = QgsApplication.messageLog()
        self._file_log = ''

    def set_mode(self, mode):
        self.mode = mode

    def enable_file_log(self, file_path):
        self._file_log = file_path

    def disable_file_log(self):
        self._file_log = ''

    def info(self, module_name, msg, handler=LogHandlerEnum.QGIS_LOG, duration=0):
        self.log_message(module_name, msg, Qgis.Info, handler, duration)

    def warning(self, module_name, msg, handler=LogHandlerEnum.QGIS_LOG, duration=0):
        self.log_message(module_name, msg, Qgis.Warning, handler, duration)

    def error(self, module_name, msg, handler=LogHandlerEnum.QGIS_LOG, duration=0):
        self.log_message(module_name, msg, Qgis.Warning, handler, duration)

    def critical(self, module_name, msg, handler=LogHandlerEnum.QGIS_LOG, duration=0):
        self.log_message(module_name, msg, Qgis.Critical, handler, duration)

    def success(self, module_name, msg, handler=LogHandlerEnum.QGIS_LOG, duration=0):
        self.log_message(module_name, msg, Qgis.Success, handler, duration)

    def debug(self, module_name, msg, handler=LogHandlerEnum.QGIS_LOG, duration=0):
        """
        Here we define messages of a particular run (e.g., showing variable values or potentially long messages)
        """
        if self.mode == LogModeEnum.DEV or self._file_log:
            # Debug messages go for devs and/or for files
            self.log_message(module_name, msg, Qgis.Info, handler, duration)

    def log_message(self, module_name, msg, level, handler=LogHandlerEnum.QGIS_LOG, duration=0):
        module_name = module_name.split(".")[-1]
        if handler == LogHandlerEnum.MESSAGE_BAR:
            self.message_with_duration_emitted.emit(msg, level, duration)
            if self.mode == LogModeEnum.DEV:
                self.log_message(module_name, msg, level, LogHandlerEnum.QGIS_LOG)
        elif handler == LogHandlerEnum.STATUS_BAR:
            self.status_bar_message_emitted.emit(msg, duration)
            if self.mode == LogModeEnum.DEV:
                self.log_message(module_name, msg, level, LogHandlerEnum.QGIS_LOG)
        elif handler == LogHandlerEnum.QGIS_LOG:
            self.log.logMessage(f"[{module_name}] {msg}", PLUGIN_NAME, level, False)

        if self._file_log:
            # Logic to write message to file
            pass

    #def message_with_button... and other methods...
    #    self.log_message(module_name, msg, handler)
