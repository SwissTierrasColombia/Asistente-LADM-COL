"""
/***************************************************************************
                              Asistente LADM-COL
                             --------------------
        begin           : 2021-09-15
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
from qgis.PyQt.QtWidgets import QWidget
from qgis.PyQt.QtCore import (QCoreApplication,
                              QSettings)

from asistente_ladm_col.utils.qt_utils import make_file_selector
from asistente_ladm_col.utils.ui import get_ui_class

WIDGET_UI = get_ui_class('transitional_system/quality_rules_file_widget.ui')


class STQualityRulesFileWidget(QWidget, WIDGET_UI):

    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)

        self.restore_settings()

        self.btn_browse_pdf_file.clicked.connect(
            make_file_selector(self.txt_pdf_file_path,
                               QCoreApplication.translate("STQualityRulesFileWidget",
                                                          "Select the PDF report file you want to upload to the transitional system"),
                               QCoreApplication.translate("STQualityRulesFileWidget",
                                                          "Portable Document Format (*.pdf)")))
        self.btn_browse_gpkg_file.clicked.connect(
            make_file_selector(self.txt_gpkg_file_path,
                               QCoreApplication.translate("STQualityRulesFileWidget",
                                                          "Select the GeoPackage file you want to upload to the transitional system"),
                               QCoreApplication.translate("STQualityRulesFileWidget",
                                                          "GeoPackage Database (*.gpkg)")))

    def save_settings(self):
        settings = QSettings()
        settings.setValue('Asistente-LADM-COL/transitional_system/quality_rules/pdf_path',
                          self.txt_pdf_file_path.text().strip())
        settings.setValue('Asistente-LADM-COL/transitional_system/quality_rules/gpkg_path',
                          self.txt_gpkg_file_path.text().strip())

    def restore_settings(self):
        settings = QSettings()
        self.txt_pdf_file_path.setText(settings.value('Asistente-LADM-COL/transitional_system/quality_rules/pdf_path', ''))
        self.txt_gpkg_file_path.setText(settings.value('Asistente-LADM-COL/transitional_system/quality_rules/gpkg_path', ''))
