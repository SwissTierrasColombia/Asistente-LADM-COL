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
import urllib

from qgis.PyQt.QtCore import (QCoreApplication,
                              QObject,
                              QSettings,
                              Qt)
from qgis.PyQt.QtPrintSupport import QPrinter
from qgis.PyQt.QtGui import QValidator
from qgis.PyQt.QtWidgets import (QFileDialog,
                                 QApplication,
                                 QWizard,
                                 QTextEdit)

from asistente_ladm_col.lib.logger import Logger


def selectFileName(line_edit_widget, title, file_filter, parent, folder_setting_key):
    folder = None
    if folder_setting_key:  # Get from settings
        from asistente_ladm_col.app_interface import AppInterface  # Here to avoid circular dependency
        app = AppInterface()
        folder = app.settings.get_setting(folder_setting_key)  # None if key not found
    if not folder:
        folder = line_edit_widget.text()

    filename, matched_filter = QFileDialog.getOpenFileName(parent, title, folder, file_filter)
    line_edit_widget.setText(filename)

    if folder_setting_key and filename:  # Save to settings
        app.settings.set_setting(folder_setting_key, os.path.dirname(filename))


def make_file_selector(widget,
                       title=QCoreApplication.translate("Asistente-LADM-COL", "Open File"),
                       file_filter=QCoreApplication.translate("Asistente-LADM-COL", "Any file(*)"),
                       parent=None,
                       folder_setting_key=None):
    return partial(selectFileName,
                   line_edit_widget=widget,
                   title=title,
                   file_filter=file_filter,
                   parent=parent,
                   folder_setting_key=folder_setting_key)


def selectFileNameToSave(line_edit_widget, title, file_filter, parent, extension, extensions):
    filename, matched_filter = QFileDialog.getSaveFileName(parent, title, line_edit_widget.text(), file_filter)
    extension_valid = False

    if not extensions:
        extensions = [extension]

    if extensions:
        extension_valid = any(filename.endswith(ext) for ext in extensions)

    if not extension_valid and filename:
        filename = filename + extension

    line_edit_widget.setText(filename)


def make_save_file_selector(widget, title=QCoreApplication.translate("QgisModelBaker", "Open File"),
                            file_filter=QCoreApplication.translate("QgisModelBaker", "Any file(*)"), parent=None,
                            extension='', extensions=None):
    return partial(selectFileNameToSave, line_edit_widget=widget, title=title, file_filter=file_filter, parent=parent,
                   extension=extension, extensions=extensions)


def selectFolder(line_edit_widget, title, parent, folder_setting_key=None):
    folder = None
    if folder_setting_key:  # Get from settings
        from asistente_ladm_col.app_interface import AppInterface  # Here to avoid circular dependency
        app = AppInterface()
        folder = app.settings.get_setting(folder_setting_key)  # None if key not found
    if not folder:
        folder = line_edit_widget.text()

    foldername = QFileDialog.getExistingDirectory(parent, title, folder)
    line_edit_widget.setText(foldername)

    if folder_setting_key and foldername:  # Save to settings
        app.settings.set_setting(folder_setting_key, os.path.dirname(foldername))


def make_folder_selector(widget,
                         title=QCoreApplication.translate("Asistente-LADM-COL", "Open Folder"),
                         parent=None,
                         folder_setting_key=None):
    return partial(selectFolder, line_edit_widget=widget, title=title, parent=parent, folder_setting_key=folder_setting_key)


def disable_next_wizard(wizard, with_back=True):
    button_list = [QWizard.HelpButton, QWizard.Stretch, QWizard.FinishButton, QWizard.CancelButton]
    if with_back: button_list.insert(2, QWizard.BackButton)
    wizard.setButtonLayout(button_list)


def enable_next_wizard(wizard, with_back=True):
    button_list = [QWizard.HelpButton, QWizard.Stretch, QWizard.NextButton, QWizard.FinishButton, QWizard.CancelButton]
    if with_back: button_list.insert(2, QWizard.BackButton)
    wizard.setButtonLayout(button_list)


def get_plugin_metadata(plugin_name, key):
    plugin_dir = os.path.dirname(sys.modules[plugin_name].__file__)
    file_path = os.path.join(plugin_dir, 'metadata.txt')
    if os.path.isfile(file_path):
        with open(file_path) as metadata:
            for line in metadata:
                line_array = line.strip().split("=")
                if line_array[0] == key:
                    return line_array[1].strip()

                # Some plugins use : instead of =...
                line_array = line.strip().split(":")
                if line_array[0] == key:
                    return line_array[1].strip()
    return None


def remove_readonly(func, path, _):
    """Clear the readonly bit and reattempt the removal"""
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except (TypeError, PermissionError, OSError) as e:
        pass


def normalize_local_url(url):
    """
    Encodes the incoming url to be ready to use when opening files or when loading QGIS delimitedtext layers

    :param url: Local file path
    :return: On Linux it returns the path without the former /, on windows returns the full path. The path returned is
             encoded, so that special characters are passed in '%C3%B3' (-->ó) form.
    """
    url = urllib.parse.quote(url, safe=':/')  # Don't encode : nor / characters
    return url[1:] if url.startswith("/") else url  # Remove the former / if we have a Linux path


class NetworkError(RuntimeError):
    def __init__(self, error_code, msg):
        self.msg = msg
        self.error_code = error_code


def save_pdf_format(settings_path, title, text):
    settings = QSettings()
    new_filename, filter = QFileDialog.getSaveFileName(None,
                                                       QCoreApplication.translate("Asistente-LADM-COL", "Export to PDF"),
                                                       settings.value(settings_path, '.'),
                                                       filter="PDF (*.pdf)")

    if new_filename:
        settings.setValue(settings_path, os.path.dirname(new_filename))
        export_title_text_to_pdf(new_filename, title, text)

        msg = QCoreApplication.translate("Asistente-LADM-COL",
            "Report successfully generated in folder <a href='file:///{normalized_path}'>{path}</a>!").format(
            normalized_path=normalize_local_url(new_filename),
            path=new_filename)
        Logger().success_msg(__name__, msg)


def export_title_text_to_pdf(filepath, title, text):
    filepath = filepath if filepath.lower().endswith(".pdf") else "{}.pdf".format(filepath)

    txt_log = QTextEdit()
    txt_log.setHtml("{}<br>{}".format(title, text))

    printer = QPrinter()
    printer.setPageSize(QPrinter.Letter)
    printer.setOutputFormat(QPrinter.PdfFormat)
    printer.setOutputFileName(filepath)
    txt_log.print(printer)


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
                color = '#ffd356'  # Light orange
        senderObj.setStyleSheet('QLineEdit {{ background-color: {} }}'.format(color))

    def validate_line_edits_lower_case(self, *args, **kwargs):
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
                color = '#ffd356'  # Light orange
        senderObj.setStyleSheet('QLineEdit {{ background-color: {} }}'.format(color))
        senderObj.setText(senderObj.text().strip().lower())


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

        pattern_matches = False
        if type(self.pattern) is str:
            pattern_matches = fnmatch.fnmatch(text, self.pattern)
        elif type(self.pattern) is list:
            pattern_matches = True in (fnmatch.fnmatch(text, pattern) for pattern in self.pattern)
        else:
            raise TypeError('pattern must be str or list, not {}'.format(type(self.pattern)))

        if not text \
                or (not self.allow_non_existing and not os.path.isfile(text)) \
                or not pattern_matches \
                or (self.is_executable and not os.access(text, os.X_OK)):
            return QValidator.Intermediate, text, pos
        else:
            return QValidator.Acceptable, text, pos

class DirValidator(QValidator):
    def __init__(self, pattern=None, parent=None, allow_empty=False, allow_non_existing=False, allow_empty_dir=False):
        QValidator.__init__(self, parent)
        self.pattern = pattern
        self.allow_empty = allow_empty
        self.allow_non_existing = allow_non_existing
        self.allow_empty_dir = allow_empty_dir

    """
    Validator for line edits that hold a dir path
    """
    def validate(self, text, pos):
        if self.allow_empty and not text.strip():
            return QValidator.Acceptable, text, pos

        if self.pattern is not None:
            pattern_matches = False
            if type(self.pattern) is str:
                pattern_matches = fnmatch.fnmatch(text, self.pattern)
            elif type(self.pattern) is list:
                pattern_matches = True in (fnmatch.fnmatch(text, pattern) for pattern in self.pattern)
            else:
                raise TypeError('pattern must be str or list, not {}'.format(type(self.pattern)))
        else:
            pattern_matches = True

        if not text \
                or (not self.allow_non_existing and not os.path.isdir(text)) \
                or not pattern_matches:
            return QValidator.Intermediate, text, pos
        else:
            if not self.allow_empty_dir and not os.listdir(text):
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


class ProcessWithStatus():
    def __init__(self, msg):
        self.msg = msg

    def __enter__(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        Logger().status(self.msg)

    def __exit__(self, exc_type, exc_val, exc_tb):
        QApplication.restoreOverrideCursor()
        Logger().clear_status()
