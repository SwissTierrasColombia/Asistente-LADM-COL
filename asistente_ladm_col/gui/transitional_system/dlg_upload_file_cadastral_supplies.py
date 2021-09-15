"""
/***************************************************************************
                              Asistente LADM-COL
                             --------------------
        begin           : 2021-09-13
        git sha         : :%H$
        copyright       : (C) 2021 by Germán Carrillo (SwissTierras Colombia)
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

from qgis.PyQt.QtCore import QCoreApplication

from asistente_ladm_col.gui.transitional_system.dlg_base_upload_file import STBaseUploadFileDialog
from asistente_ladm_col.gui.transitional_system.cadastral_supplies_file_widget import STCadastralSuppliesFileWidget
from asistente_ladm_col.utils.qt_utils import ProcessWithStatus
from asistente_ladm_col.utils.utils import Utils


class STCadastralSuppliesUploadFileDialog(STBaseUploadFileDialog):

    def __init__(self, request_id, other_params, parent=None):
        self._file_widget = STCadastralSuppliesFileWidget()

        STBaseUploadFileDialog.__init__(self, request_id, other_params, parent)

        self.setWindowTitle(QCoreApplication.translate("STCadastralSuppliesUploadFileDialog",
                                                       "Upload cadastral supplies files to Transitional System"))

    def _handle_upload_file(self):
        """
        The XTF is mandatory. If report files are sent, XLS is mandatory and GPKG is optional.
        But sending report files is optional.
        """
        xtf_file_path = self._file_widget.txt_xtf_file_path.text().strip()
        if not self.txt_comments.toPlainText():
            res = False
            res_msg = QCoreApplication.translate("STCadastralSuppliesUploadFileDialog", "File was not uploaded! Details: Comments are required.")
        elif os.path.isfile(xtf_file_path):
            zip_xtf_file_path = Utils.compress_files([xtf_file_path])

            xls_file_path = self._file_widget.txt_xls_file_path.text().strip()
            gpkg_file_path = self._file_widget.txt_gpkg_file_path.text().strip()

            if xls_file_path and not os.path.isfile(xls_file_path):
                res = False
                res_msg = QCoreApplication.translate("STCadastralSuppliesUploadFileDialog",
                                                     "The XLSX file '{}' does not exist!").format(xls_file_path)
            elif gpkg_file_path and not os.path.isfile(gpkg_file_path):
                res = False
                res_msg = QCoreApplication.translate("STCadastralSuppliesUploadFileDialog",
                                                     "The GeoPackage file '{}' does not exist!").format(gpkg_file_path)
            elif gpkg_file_path and not xls_file_path:
                res = False
                res_msg = QCoreApplication.translate(
                    "STCadastralSuppliesUploadFileDialog", "If you send a GPKG file, you need to send the corresponding XLS as well!")
            else:
                zip_reports_file_path = None
                if xls_file_path:
                    reports = list()
                    reports.append(xls_file_path)
                    if gpkg_file_path:
                        reports.append(gpkg_file_path)

                    zip_reports_file_path = Utils.compress_files(reports)

                # Prepare upload
                url = self._st_config.ST_PROVIDER_UPLOAD_FILE_SERVICE_URL.format(self._request_id)
                files = [('files[]', open(zip_xtf_file_path, 'rb'))]
                if zip_reports_file_path:  # Optional ZIP file
                    files.append(('extra', open(zip_reports_file_path, 'rb')))

                with ProcessWithStatus(QCoreApplication.translate("STCadastralSuppliesUploadFileDialog", "Uploading file to ST server...")):
                    res, res_msg = self._st_utils.upload_files(url,
                                                               self._other_params,
                                                               files,
                                                               self.txt_comments.toPlainText())
        else:
            res = False
            res_msg = QCoreApplication.translate("STCadastralSuppliesUploadFileDialog", "The XTF file '{}' does not exist!").format(xtf_file_path)

        return res, res_msg

    def _get_help_text(self):
        return """
        <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html><head><meta name="qrichtext" content="1" /><style type="text/css">
p, li { white-space: pre-wrap; }
</style></head><body style=" font-family:'Ubuntu'; font-size:11pt; font-weight:400; font-style:normal;">
<p align="justify" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'Noto Sans'; font-size:9pt; color:#545454;">Desde este diálogo puedes subir archivos de insumos catastrales al </span><span style=" font-family:'Noto Sans'; font-size:9pt; font-style:italic; color:#545454;">Sistema de Transición</span><span style=" font-family:'Noto Sans'; font-size:9pt; color:#545454;">. </span></p>
<p align="justify" style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Noto Sans'; font-size:9pt; color:#545454;"><br /></p>
<p align="justify" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'Noto Sans'; font-size:9pt; color:#545454;">En la sección </span><span style=" font-family:'Noto Sans'; font-size:9pt; font-style:italic; color:#545454;">Comentarios</span><span style=" font-family:'Noto Sans'; font-size:9pt; color:#545454;"> se agrega una descripción del (los) archivo(s) a subir.</span></p>
<p align="justify" style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Noto Sans'; font-size:9pt; color:#545454;"><br /></p>
<p align="justify" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'Noto Sans'; font-size:9pt; color:#545454;">Los archivos que se esperan son:</span></p>
<ul style="margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;"><li align="justify" style=" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'Noto Sans'; font-size:9pt; color:#545454;">Un archivo XTF (obligatorio).</span></li>
<li align="justify" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'Noto Sans'; font-size:9pt; color:#545454;">Un archivo de Excel con el reporte de Omisiones y Comisiones (opcional).</span></li>
<li style=" font-family:'Noto Sans'; font-size:9pt; color:#545454;" align="justify" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">Un archivo GeoPackage con el reporte de Omisiones y Comisiones (opcional y solo posible si se sube también el archivo de Excel). </li></ul></body></html>"""
