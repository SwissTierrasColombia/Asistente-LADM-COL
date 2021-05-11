# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2020-02-11
        git sha              : :%H$
        copyright            : (C) 2020 by Germán Carrillo (Swissphoto BSF)
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
import os.path

from qgis.core import Qgis
from qgis.PyQt.QtWidgets import (QDialog,
                                 QSizePolicy,
                                 QDialogButtonBox)
from qgis.PyQt.QtCore import (Qt,
                              QCoreApplication,
                              QSettings,
                              pyqtSignal)
from qgis.gui import QgsMessageBar

from asistente_ladm_col.utils.qt_utils import (make_file_selector,
                                               ProcessWithStatus)
from asistente_ladm_col.utils.st_utils import STUtils
from asistente_ladm_col.utils.ui import get_ui_class
from asistente_ladm_col.utils.utils import (Utils,
                                            show_plugin_help)

DIALOG_TRANSITION_SYSTEM_UI = get_ui_class('supplies/dlg_upload_file.ui')


class STUploadFileDialog(QDialog, DIALOG_TRANSITION_SYSTEM_UI):
    on_result = pyqtSignal(bool)  # whether the tool was run successfully or not

    def __init__(self, request_id, supply_type, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        self.request_id = request_id
        self.supply_type = supply_type
        self.st_utils = STUtils()

        self.buttonBox.accepted.disconnect()
        self.buttonBox.accepted.connect(self.upload_file)
        self.buttonBox.helpRequested.connect(self.show_help)

        self.restore_settings()  # To update file paths, which will be used as basis in FileDialogs

        self.btn_browse_xtf_file.clicked.connect(
            make_file_selector(self.txt_xtf_file_path,
                               QCoreApplication.translate("STUploadFileDialog",
                                                          "Select the XTF file you want to upload to the transitional system"),
                               QCoreApplication.translate("STUploadFileDialog",
                                                          "INTERLIS 2 transfer format (*.xtf)")))
        self.btn_browse_xls_file.clicked.connect(
            make_file_selector(self.txt_xls_file_path,
                               QCoreApplication.translate("STUploadFileDialog",
                                                          "Select the XLS file you want to upload to the transitional system"),
                               QCoreApplication.translate("STUploadFileDialog",
                                                          "Excel File (*.xlsx *.xls)")))
        self.btn_browse_gpkg_file.clicked.connect(
            make_file_selector(self.txt_gpkg_file_path,
                               QCoreApplication.translate("STUploadFileDialog",
                                                          "Select the GeoPackage file you want to upload to the transitional system"),
                               QCoreApplication.translate("STUploadFileDialog",
                                                          "GeoPackage Database (*.gpkg)")))

        self.initialize_progress()

        self.bar = QgsMessageBar()
        self.bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.layout().addWidget(self.bar, 0, 0, Qt.AlignTop)

    def upload_file(self):
        """
        The XTF is mandatory. If report files are sent, XLS is mandatory and GPKG is optional. But sending report files
        is optional.
        """
        self.bar.clearWidgets()
        self.start_progress()
        self.enable_controls(False)

        xtf_file_path = self.txt_xtf_file_path.text().strip()
        if not self.txt_comments.toPlainText():
            res = False
            res_msg = QCoreApplication.translate("STUploadFileDialog", "File was not uploaded! Details: Comments are required.")
        elif os.path.isfile(xtf_file_path):
            zip_xtf_file_path = Utils.compress_files([xtf_file_path])

            xls_file_path = self.txt_xls_file_path.text().strip()
            gpkg_file_path = self.txt_gpkg_file_path.text().strip()

            if xls_file_path and not os.path.isfile(xls_file_path):
                res = False
                res_msg = QCoreApplication.translate("STUploadFileDialog",
                                                     "The XLSX file '{}' does not exist!").format(xls_file_path)
            elif gpkg_file_path and not os.path.isfile(gpkg_file_path):
                res = False
                res_msg = QCoreApplication.translate("STUploadFileDialog",
                                                     "The GeoPackage file '{}' does not exist!").format(gpkg_file_path)
            elif gpkg_file_path and not xls_file_path:
                res = False
                res_msg = QCoreApplication.translate(
                    "STUploadFileDialog", "If you send a GPKG file, you need to send the corresponding XLS as well!")
            else:
                zip_reports_file_path = None
                if xls_file_path:
                    reports = list()
                    reports.append(xls_file_path)
                    if gpkg_file_path:
                        reports.append(gpkg_file_path)

                    zip_reports_file_path = Utils.compress_files(reports)

                with ProcessWithStatus(QCoreApplication.translate("STUploadFileDialog", "Uploading file to ST server...")):
                    res, res_msg = self.st_utils.upload_files(self.request_id,
                                                              self.supply_type,
                                                              zip_xtf_file_path,
                                                              zip_reports_file_path,
                                                              self.txt_comments.toPlainText())
        else:
            res = False
            res_msg = QCoreApplication.translate("STUploadFileDialog", "The XTF file '{}' does not exist!").format(xtf_file_path)

        self.show_message(res_msg, Qgis.Success if res else Qgis.Warning)

        self.initialize_progress()

        if res:
            self.store_settings()
        else:
            self.enable_controls(True)  # Prepare next run

        self.on_result.emit(res)  # Inform other classes if the execution was successful

        return  # Do not close dialog

    def show_message(self, message, level):
        self.bar.clearWidgets()  # Remove previous messages before showing a new one
        self.bar.pushMessage(message, level, 0)

    def store_settings(self):
        settings = QSettings()
        settings.setValue('Asistente-LADM-COL/QgisModelBaker/ili2pg/xtffile_export',
                          self.txt_xtf_file_path.text().strip())

    def restore_settings(self):
        settings = QSettings()
        self.txt_xtf_file_path.setText(settings.value('Asistente-LADM-COL/QgisModelBaker/ili2pg/xtffile_export'))

        folder_path = settings.value('Asistente-LADM-COL/missing_supplies_snc/folder_path')
        file_names = settings.value('Asistente-LADM-COL/missing_supplies_snc/file_names')
        xls_path = os.path.join(folder_path, "{}.xlsx".format(file_names))
        gpkg_path = os.path.join(folder_path, "{}.gpkg".format(file_names))

        self.txt_xls_file_path.setText(xls_path if folder_path and file_names else '')
        self.txt_gpkg_file_path.setText(gpkg_path if folder_path and file_names else '')

    def start_progress(self):
        self.progress.setVisible(True)
        self.progress.setRange(0, 0)

    def initialize_progress(self):
        self.progress.setVisible(False)

    def enable_controls(self, enable):
        self.gbx_page_1.setEnabled(enable)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(enable)

    def show_help(self):
        show_plugin_help('transitional_system_upload_file')