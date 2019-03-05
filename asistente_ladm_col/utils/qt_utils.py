# -*- coding: utf-8 -*-

"""
/***************************************************************************
                              -------------------
        begin                : 2016
        copyright            : (C) 2016 by OPENGIS.ch
        email                : info@opengis.ch
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import fnmatch
import os
import stat
import sys
from functools import partial

from qgis.core import Qgis
import qgis.utils
from qgis.PyQt.QtCore import (QCoreApplication,
                              QObject,
                              QFile,
                              QIODevice,
                              QEventLoop,
                              QUrl,
                              QSettings)
from qgis.PyQt.QtPrintSupport import QPrinter                              
from qgis.PyQt.QtGui import QValidator
from qgis.PyQt.QtNetwork import QNetworkRequest
from qgis.PyQt.QtWidgets import (QFileDialog,
                                 QApplication,
                                 QWizard,
                                 QTextEdit)
from qgis.core import QgsNetworkAccessManager


def selectFileName(line_edit_widget, title, file_filter, parent):
    filename, matched_filter = QFileDialog.getOpenFileName(parent, title, line_edit_widget.text(), file_filter)
    line_edit_widget.setText(filename)


def make_file_selector(widget, title=QCoreApplication.translate('Asistente-LADM_COL', 'Open File'),
                       file_filter=QCoreApplication.translate('Asistente-LADM_COL', 'Any file(*)'), parent=None):
    return partial(selectFileName, line_edit_widget=widget, title=title, file_filter=file_filter, parent=parent)


def selectFileNameToSave(line_edit_widget, title, file_filter, parent, extension):
    filename, matched_filter = QFileDialog.getSaveFileName(parent, title, line_edit_widget.text(), file_filter)
    line_edit_widget.setText(filename if filename.endswith(extension) else (filename + extension if filename else ''))


def make_save_file_selector(widget, title=QCoreApplication.translate('Asistente-LADM_COL', 'Open File'),
                            file_filter=QCoreApplication.translate('Asistente-LADM_COL', 'Any file(*)'), parent=None, extension=''):
    return partial(selectFileNameToSave, line_edit_widget=widget, title=title, file_filter=file_filter, parent=parent, extension=extension)


def selectFolder(line_edit_widget, title, parent):
    foldername = QFileDialog.getExistingDirectory(parent, title, line_edit_widget.text())
    line_edit_widget.setText(foldername)


def make_folder_selector(widget, title=QCoreApplication.translate('Asistente-LADM_COL', 'Open Folder'), parent=None):
    return partial(selectFolder, line_edit_widget=widget, title=title, parent=parent)


def disable_next_wizard(wizard, with_back=True):
    button_list = [QWizard.HelpButton, QWizard.Stretch, QWizard.FinishButton, QWizard.CancelButton]
    if with_back: button_list.insert(2, QWizard.BackButton)
    wizard.setButtonLayout(button_list)


def enable_next_wizard(wizard, with_back=True):
    button_list = [QWizard.HelpButton, QWizard.Stretch, QWizard.NextButton, QWizard.FinishButton, QWizard.CancelButton]
    if with_back: button_list.insert(2, QWizard.BackButton)
    wizard.setButtonLayout(button_list)


def get_plugin_metadata(plugin_name, key):
    plugin_dir = None
    if plugin_name in qgis.utils.plugins:
        plugin_dir = qgis.utils.plugins[plugin_name].plugin_dir
    else:
        plugin_dir = os.path.dirname(sys.modules[plugin_name].__file__)
    file_path = os.path.join(plugin_dir, 'metadata.txt')
    if os.path.isfile(file_path):
        with open(file_path) as metadata:
            for line in metadata:
                line_array = line.strip().split("=")
                if line_array[0] == key:
                    return line_array[1].strip()
    return None


def remove_readonly(func, path, _):
    "Clear the readonly bit and reattempt the removal"
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except (TypeError, PermissionError, OSError) as e:
        pass


def normalize_local_url(url):
    return url[1:] if url.startswith("/") else url



class NetworkError(RuntimeError):
    def __init__(self, error_code, msg):
        self.msg = msg
        self.error_code = error_code

def save_pdf_format(self, settings_path, title, text):
    settings = QSettings()
    new_filename, filter = QFileDialog.getSaveFileName(self,
                                                        QCoreApplication.translate('Asistente-LADM_COL',
                                                                                    'Export to PDF'),
                                                        settings.value(
                                                            settings_path, '.'),
                                                        filter="PDF (*.pdf)")               

    if new_filename:
        settings.setValue(settings_path, os.path.dirname(new_filename))
        new_filename = new_filename if new_filename.lower().endswith(".pdf") else "{}.pdf".format(new_filename)

        txt_log = QTextEdit()
        txt_log.setHtml("{}<br>{}".format(title, text))

        printer = QPrinter()
        printer.setPageSize(QPrinter.Letter)
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName(new_filename)
        txt_log.print(printer)

        msg = QCoreApplication.translate("Asistente-LADM_COL", 
            "All Excel Check report successfully generated in folder <a href='file:///{path}'>{path}</a>!").format(path=normalize_local_url(new_filename))
        self.qgis_utils.message_with_duration_emitted.emit(msg, Qgis.Success, 0)

class Validators(QObject):
    def validate_line_edits(self, *args, **kwargs):
        """
        Validate line edits and set their color to indicate validation state.
        """
        senderObj = self.sender()
        validator = senderObj.validator()
        if validator is None:
            color = '#fff'  # White
        else:
            state = validator.validate(senderObj.text().strip(), 0)[0]
            if state == QValidator.Acceptable:
                color = '#fff'  # White
            elif state == QValidator.Intermediate:
                color = '#ffd356'  # Light orange
            else:
                color = '#f6989d'  # Red
        senderObj.setStyleSheet('QLineEdit {{ background-color: {} }}'.format(color))


class FileValidator(QValidator):
    def __init__(self, pattern='*', is_executable=False, parent=None, allow_empty=False, allow_non_existing=False):
        QValidator.__init__(self, parent)
        self.pattern = pattern
        self.is_executable = is_executable
        self.allow_empty = allow_empty
        self.allow_non_existing = allow_non_existing

    """
    Validator for file line edits
    """

    def validate(self, text, pos):
        if self.allow_empty and not text.strip():
            return QValidator.Acceptable, text, pos

        if not text \
                or (not self.allow_non_existing and not os.path.isfile(text)) \
                or not fnmatch.fnmatch(text, self.pattern) \
                or (self.is_executable and not os.access(text, os.X_OK)):
            return QValidator.Intermediate, text, pos
        else:
            return QValidator.Acceptable, text, pos


class NonEmptyStringValidator(QValidator):
    def __init__(self, parent=None):
        QValidator.__init__(self, parent)

    def validate(self, text, pos):
        if not text.strip():
            return QValidator.Intermediate, text, pos

        return QValidator.Acceptable, text, pos


class OverrideCursor():
    def __init__(self, cursor):
        self.cursor = cursor

    def __enter__(self):
        QApplication.setOverrideCursor(self.cursor)

    def __exit__(self, exc_type, exc_val, exc_tb):
        QApplication.restoreOverrideCursor()
