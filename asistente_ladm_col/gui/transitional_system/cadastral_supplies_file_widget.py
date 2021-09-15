"""
/***************************************************************************
                              Asistente LADM-COL
                             --------------------
        begin           : 2021-09-15
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

from qgis.PyQt.QtWidgets import QWidget
from qgis.PyQt.QtCore import (QCoreApplication,
                              QSettings)

from asistente_ladm_col.utils.qt_utils import make_file_selector
from asistente_ladm_col.utils.ui import get_ui_class

WIDGET_UI = get_ui_class('transitional_system/cadastral_supplies_file_widget.ui')


class STCadastralSuppliesFileWidget(QWidget, WIDGET_UI):

    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)

        self.restore_settings()

        self.btn_browse_xtf_file.clicked.connect(
            make_file_selector(self.txt_xtf_file_path,
                               QCoreApplication.translate("STCadastralSuppliesFileWidget",
                                                          "Select the XTF file you want to upload to the transitional system"),
                               QCoreApplication.translate("STCadastralSuppliesFileWidget",
                                                          "INTERLIS 2 transfer format (*.xtf)")))
        self.btn_browse_xls_file.clicked.connect(
            make_file_selector(self.txt_xls_file_path,
                               QCoreApplication.translate("STCadastralSuppliesFileWidget",
                                                          "Select the XLS file you want to upload to the transitional system"),
                               QCoreApplication.translate("STCadastralSuppliesFileWidget",
                                                          "Excel File (*.xlsx *.xls)")))
        self.btn_browse_gpkg_file.clicked.connect(
            make_file_selector(self.txt_gpkg_file_path,
                               QCoreApplication.translate("STCadastralSuppliesFileWidget",
                                                          "Select the GeoPackage file you want to upload to the transitional system"),
                               QCoreApplication.translate("STCadastralSuppliesFileWidget",
                                                          "GeoPackage Database (*.gpkg)")))

    def save_settings(self):
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
