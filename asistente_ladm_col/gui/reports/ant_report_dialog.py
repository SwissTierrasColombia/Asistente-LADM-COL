# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2021-03-18
        git sha              : :%H$
        copyright            : (C) 2021 by Leonardo Cardona (BSF Swissphoto)
        email                : leo dot cardona dot p at gmail dot com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.core import QgsProject
from qgis.PyQt.QtCore import (pyqtSignal,
                              QSettings,
                              QCoreApplication)
from qgis.PyQt.QtGui import QValidator
from qgis.PyQt.QtWidgets import (QDialog,
                                 QDialogButtonBox)

from asistente_ladm_col.utils import get_ui_class
from asistente_ladm_col.utils.qt_utils import (make_folder_selector,
                                               DirValidator,
                                               Validators)

DIALOG_ANT_REPORT_UI = get_ui_class('reports/ant_map_report_dialog.ui')


class ANTReportDialog(QDialog, DIALOG_ANT_REPORT_UI):
    URBAN_ZONE = 'ZONA_URBANA'
    RURAL_ZONE = 'ZONA_RURAL'
    NO_BASEMAP = 'NO_BASEMAP'
    WMS_NAME = 'NAME'
    WMS_URL = 'URL'
    WMS_SUBLAYERS = 'SUBLAYERS'
    WMS_PROVIDER = 'wms'

    def __init__(self, report_name):
        QDialog.__init__(self)
        self.setupUi(self)
        self.__validators = Validators()
        self.__report_name = report_name
        self.__wms_basemaps = dict()

        self.zone_combobox.clear()
        self.zone_combobox.addItem(QCoreApplication.translate("ReportGenerator", "Urban"), self.URBAN_ZONE)
        self.zone_combobox.addItem(QCoreApplication.translate("ReportGenerator", "Rural"), self.RURAL_ZONE)

        self.register_wms_basemaps()  # List WMS loaded by the user in the map canvas
        self.basemap_combobox.clear()
        self.basemap_combobox.addItem(QCoreApplication.translate("ReportGenerator", "No basemap"), self.NO_BASEMAP)

        for layer_id, wms_params in self.__wms_basemaps.items():
            self.basemap_combobox.addItem(wms_params[self.WMS_NAME], layer_id)

        self.buttonBox.accepted.disconnect()
        self.buttonBox.accepted.connect(self.accepted)
        self.buttonBox.button(QDialogButtonBox.Ok).setText(QCoreApplication.translate("ReportGenerator", "Generate"))
        self.set_generate_report_button_enabled(False)

        self.btn_browse_file_folder_report.clicked.connect(make_folder_selector(self.txt_file_path_folder_report, title='Output folder', parent=None))
        dir_validator_folder = DirValidator(pattern=None, allow_empty_dir=True)
        self.txt_file_path_folder_report.setValidator(dir_validator_folder)
        self.txt_file_path_folder_report.textChanged.connect(self.__validators.validate_line_edits)
        self.txt_file_path_folder_report.textChanged.connect(self.input_data_changed)
        self.restore_settings()

        # Result variables
        self.output_folder = ''
        self.result_dict = dict()

    def register_wms_basemaps(self):
        for layer in QgsProject.instance().mapLayers().values():
            if layer.providerType() == self.WMS_PROVIDER and layer.isValid():
                basemap = dict()
                basemap[self.WMS_NAME] = layer.name()
                basemap[self.WMS_SUBLAYERS] = layer.subLayers()
                for param in layer.source().split('&'):
                    if param.startswith('url'):
                        basemap[self.WMS_URL] = param.split('=')[1]
                self.__wms_basemaps[layer.id()] = basemap

    def set_generate_report_button_enabled(self, enable):
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(enable)

    def validate_inputs(self):
        folder_path = self.txt_file_path_folder_report.validator().validate(self.txt_file_path_folder_report.text().strip(), 0)[0]
        return folder_path == QValidator.Acceptable

    def input_data_changed(self):
        self.set_generate_report_button_enabled(self.validate_inputs())

    def accepted(self):
        """
        Set the result variables so that the report generator can get what it needs.
        """
        self.output_folder = self.txt_file_path_folder_report.text().strip()
        selected_basemap = self.basemap_combobox.currentData()
        self.result_dict = {
            'zone': self.zone_combobox.currentData(),
            'nameWhoElaborated': self.text_name_who_elaborated.text().strip(),
            'licenseWhoElaborated': self.text_license_who_elaborated.text().strip(),
            'nameWhoRevised': self.txt_name_who_revised.text().strip(),
            'licenseWhoRevised': self.txt_license_who_revised.text().strip(),
            'observationsReport': self.txt_observations_report.toPlainText(),
            self.NO_BASEMAP: selected_basemap == self.NO_BASEMAP,
            self.WMS_URL: self.__wms_basemaps[selected_basemap][self.WMS_URL] if selected_basemap != self.NO_BASEMAP else '',
            self.WMS_SUBLAYERS: self.__wms_basemaps[selected_basemap][self.WMS_SUBLAYERS] if selected_basemap != self.NO_BASEMAP else ''
        }

        self.save_settings()
        self.done(QDialog.Accepted)  # TODO: Close the dialog because canvas shows the progress bar. Dialog should control the progress bar

    def save_settings(self):
        QSettings().setValue("Asistente-LADM-COL/reports/{}/save_into_dir".format(self.__report_name), self.txt_file_path_folder_report.text().strip())
        QSettings().setValue("Asistente-LADM-COL/reports/{}/zone".format(self.__report_name), self.zone_combobox.currentData())
        QSettings().setValue("Asistente-LADM-COL/reports/{}/name_who_elaborated".format(self.__report_name), self.text_name_who_elaborated.text().strip())
        QSettings().setValue("Asistente-LADM-COL/reports/{}/license_who_elaborated".format(self.__report_name), self.text_license_who_elaborated.text().strip())
        QSettings().setValue("Asistente-LADM-COL/reports/{}/name_who_revised".format(self.__report_name), self.txt_name_who_revised.text().strip())
        QSettings().setValue("Asistente-LADM-COL/reports/{}/license_who_revised".format(self.__report_name), self.txt_license_who_revised.text().strip())
        QSettings().setValue("Asistente-LADM-COL/reports/{}/observations_report".format(self.__report_name), self.txt_observations_report.toPlainText())

    def restore_settings(self):
        save_into_dir = QSettings().value("Asistente-LADM-COL/reports/{}/save_into_dir".format(self.__report_name), "")
        self.txt_file_path_folder_report.setText(save_into_dir)

        zone = QSettings().value("Asistente-LADM-COL/reports/{}/zone".format(self.__report_name), self.URBAN_ZONE)
        index_zone = self.zone_combobox.findData(zone)
        if index_zone == -1:
            index_zone = self.cbo_db_engine.findData(self.URBAN_ZONE)
        self.zone_combobox.setCurrentIndex(index_zone)

        name_who_elaborated = QSettings().value("Asistente-LADM-COL/reports/{}/name_who_elaborated".format(self.__report_name), "")
        self.text_name_who_elaborated.setText(name_who_elaborated)

        license_who_elaborated = QSettings().value("Asistente-LADM-COL/reports/{}/license_who_elaborated".format(self.__report_name), "")
        self.text_license_who_elaborated.setText(license_who_elaborated)

        name_who_revised = QSettings().value("Asistente-LADM-COL/reports/{}/name_who_revised".format(self.__report_name), "")
        self.txt_name_who_revised.setText(name_who_revised)

        license_who_revised = QSettings().value("Asistente-LADM-COL/reports/{}/license_who_revised".format(self.__report_name), "")
        self.txt_license_who_revised.setText(license_who_revised)

        observations_report = QSettings().value("Asistente-LADM-COL/reports/{}/observations_report".format(self.__report_name), "")
        self.txt_observations_report.setPlainText(observations_report)
