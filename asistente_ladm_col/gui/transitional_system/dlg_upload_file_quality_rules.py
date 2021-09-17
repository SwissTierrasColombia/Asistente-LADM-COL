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
from asistente_ladm_col.gui.transitional_system.quality_rules_file_widget import STQualityRulesFileWidget
from asistente_ladm_col.utils.qt_utils import ProcessWithStatus
from asistente_ladm_col.utils.utils import Utils


class STQualityRulesUploadFileDialog(STBaseUploadFileDialog):

    def __init__(self, request_id, other_params, parent=None):
        self._file_widget = STQualityRulesFileWidget()

        STBaseUploadFileDialog.__init__(self, request_id, other_params, parent)

        self.setWindowTitle(QCoreApplication.translate("STQualityRulesUploadFileDialog",
                                                       "Upload quality rules files to Transitional System"))

    def _handle_upload_file(self):
        """
        The PDF is mandatory, whereas the GPKG is optional.
        """
        pdf_file_path = self._file_widget.txt_pdf_file_path.text().strip()
        if not self.txt_comments.toPlainText():
            res = False
            res_msg = QCoreApplication.translate("STQualityRulesUploadFileDialog", "File was not uploaded! Details: Comments are required.")
        elif os.path.isfile(pdf_file_path):
            reports = list()
            reports.append(pdf_file_path)

            gpkg_file_path = self._file_widget.txt_gpkg_file_path.text().strip()

            if gpkg_file_path and not os.path.isfile(gpkg_file_path):
                res = False
                res_msg = QCoreApplication.translate("STQualityRulesUploadFileDialog",
                                                     "The GeoPackage file '{}' does not exist!").format(gpkg_file_path)
            else:
                if gpkg_file_path:
                    reports.append(gpkg_file_path)

                zip_reports_file_path = Utils.compress_files(reports)

                # Prepare upload
                url = self._st_utils.st_config.ST_MANAGER_UPLOAD_FILE_SERVICE_URL.format(self._request_id)
                files = [('files[]', open(zip_reports_file_path, 'rb'))]

                with ProcessWithStatus(QCoreApplication.translate("STQualityRulesUploadFileDialog", "Uploading file to ST server...")):
                    res, res_msg = self._st_utils.upload_files(url,
                                                               self._other_params,
                                                               files,
                                                               self.txt_comments.toPlainText())
        else:
            res = False
            res_msg = QCoreApplication.translate("STQualityRulesUploadFileDialog", "The PDF file '{}' does not exist!").format(pdf_file_path)

        return res, res_msg

    def _get_help_text(self):
        return """
        <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html><head><meta name="qrichtext" content="1" /><style type="text/css">
p, li { white-space: pre-wrap; }
</style></head><body style=" font-family:'Ubuntu'; font-size:11pt; font-weight:400; font-style:normal;">
<p align="justify" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'Noto Sans'; font-size:9pt; color:#545454;">Desde este diálogo puedes subir reportes de reglas de calidad al </span><span style=" font-family:'Noto Sans'; font-size:9pt; font-style:italic; color:#545454;">Sistema de Transición</span><span style=" font-family:'Noto Sans'; font-size:9pt; color:#545454;">. </span></p>
<p align="justify" style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Noto Sans'; font-size:9pt; color:#545454;"><br /></p>
<p align="justify" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'Noto Sans'; font-size:9pt; color:#545454;">En la sección </span><span style=" font-family:'Noto Sans'; font-size:9pt; font-style:italic; color:#545454;">Comentarios</span><span style=" font-family:'Noto Sans'; font-size:9pt; color:#545454;"> se agrega una descripción del (los) archivo(s) a subir.</span></p>
<p align="justify" style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Noto Sans'; font-size:9pt; color:#545454;"><br /></p>
<p align="justify" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'Noto Sans'; font-size:9pt; color:#545454;">Los archivos que se esperan son:</span></p>
<ul style="margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;"><li align="justify" style=" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'Noto Sans'; font-size:9pt; color:#545454;">Un archivo PDF del reporte general de reglas de calidad (obligatorio).</span></li>
<li style=" font-family:'Noto Sans'; font-size:9pt; color:#545454;" align="justify" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">Un archivo GeoPackage que contiene los errores de reglas de calidad (opcional). </li></ul></body></html>"""
