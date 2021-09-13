"""
/***************************************************************************
                              Asistente LADM-COL
                             --------------------
        begin           : 2021-09-13
        git sha         : :%H$
        copyright       : (C) 2020 by Germán Carrillo (SwissTierras Colombia)
        email           : gcarrillo@linuxmail.org
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

from asistente_ladm_col.gui.transitional_system.dlg_base_upload_file import STBaseUploadFileDialog
from asistente_ladm_col.utils.qt_utils import (make_file_selector,
                                               ProcessWithStatus)
from asistente_ladm_col.utils.st_utils import STUtils
from asistente_ladm_col.utils.ui import get_ui_class
from asistente_ladm_col.utils.utils import (Utils,
                                            show_plugin_help)

DIALOG_TRANSITION_SYSTEM_UI = get_ui_class('supplies/dlg_upload_file.ui')


class STCadastralSuppliesUploadFileDialog(STBaseUploadFileDialog):

    def __init__(self, request_id, other_params, parent=None):
        STBaseUploadFileDialog.__init__(self, request_id, other_params, parent=None)

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

    def _handle_upload_file(self):
        """
        The XTF is mandatory. If report files are sent, XLS is mandatory and GPKG is optional.
        But sending report files is optional.
        """
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

                # Prepare upload
                url = self.st_config.ST_PROVIDER_UPLOAD_FILE_SERVICE_URL.format(self.request_id)
                files = [('files[]', open(zip_xtf_file_path, 'rb'))]
                if zip_reports_file_path:  # Optional ZIP file
                    files.append(('extra', open(zip_reports_file_path, 'rb')))

                with ProcessWithStatus(QCoreApplication.translate("STUploadFileDialog", "Uploading file to ST server...")):
                    res, res_msg = self.st_utils.upload_files(url,
                                                              self.other_params,
                                                              files,
                                                              self.txt_comments.toPlainText())
        else:
            res = False
            res_msg = QCoreApplication.translate("STUploadFileDialog", "The XTF file '{}' does not exist!").format(xtf_file_path)

        return res, res_msg

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
