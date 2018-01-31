# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2017-11-14
        git sha              : :%H$
        copyright            : (C) 2017 by Germán Carrillo (BSF Swissphoto)
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
import os

from qgis.core import QgsProject, QgsVectorLayer, QgsSpatialIndex
from qgis.gui import QgsMessageBar
from qgis.PyQt.QtCore import QSettings, QCoreApplication
from qgis.PyQt.QtWidgets import QWizard

from ..utils.qt_utils import make_file_selector
from ..utils import get_ui_class
from ..config.table_mapping_config import (BOUNDARY_POINT_TABLE,
                                           SURVEY_POINT_TABLE)

WIZARD_UI = get_ui_class('wiz_add_points_cadaster.ui')

class PointsSpatialUnitCadasterWizard(QWizard, WIZARD_UI):
    def __init__(self, iface, db, qgis_utils, parent=None):
        QWizard.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self._db = db
        self.qgis_utils = qgis_utils

        # Set connections
        self.btn_browse_file.clicked.connect(
            make_file_selector(self.txt_file_path,
                               file_filter=QCoreApplication.translate("PointsSpatialUnitCadasterWizard",'CSV Comma Separated Value (*.csv)')))
        self.txt_file_path.textChanged.connect(self.fill_long_lat_combos)
        self.txt_delimiter.textChanged.connect(self.fill_long_lat_combos)


        self.restore_settings()

        self.txt_file_path.textChanged.emit(self.txt_file_path.text())

        self.rad_boundary_point.toggled.connect(self.adjust_page_subtitle)
        self.adjust_page_subtitle() # Initialize it
        self.button(QWizard.FinishButton).clicked.connect(self.prepare_copy_csv_points_to_db)

    def adjust_page_subtitle(self):
        if self.rad_boundary_point.isChecked():
            self.wizardPage2.setSubTitle("Configure Data Source for Boundary Points")
        else:
            self.wizardPage2.setSubTitle("Configure Data Source for Survey Points")

    def prepare_copy_csv_points_to_db(self):
        csv_path = self.txt_file_path.text().strip()

        if not csv_path or not os.path.exists(csv_path):
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                QCoreApplication.translate("PointsSpatialUnitCadasterWizard",
                                           "No CSV file given or file doesn't exist."),
                QgsMessageBar.WARNING)
            return

        self.save_settings()

        target_layer = BOUNDARY_POINT_TABLE if self.rad_boundary_point.isChecked() else SURVEY_POINT_TABLE

        res = self.qgis_utils.copy_csv_to_db(csv_path,
                                    self.txt_delimiter.text(),
                                    self.cbo_longitude.currentText(),
                                    self.cbo_latitude.currentText(),
                                    self._db,
                                    target_layer)

    def fill_long_lat_combos(self, text):
        csv_path = self.txt_file_path.text().strip()
        self.cbo_longitude.clear()
        self.cbo_latitude.clear()
        if os.path.exists(csv_path):
            self.button(QWizard.FinishButton).setEnabled(True)

            fields = self.get_fields_from_csv_file(csv_path)
            if not fields:
                self.button(QWizard.FinishButton).setEnabled(False)
                return

            self.cbo_longitude.addItems(fields)
            self.cbo_latitude.addItems(fields)

            # Heuristics to suggest values for x and y
            lowercase_fields = [field for field in fields]
            x_potential_names = ['x', 'lon', 'long', 'longitud', 'longitude', 'este', 'east', 'oeste', 'west']
            y_potential_names = ['y', 'lat', 'latitud', 'latitude', 'norte', 'north']
            for x_potential_name in x_potential_names:
                if x_potential_name in lowercase_fields:
                    self.cbo_longitude.setCurrentText(x_potential_name)
                    break
            for y_potential_name in y_potential_names:
                if y_potential_name in lowercase_fields:
                    self.cbo_latitude.setCurrentText(y_potential_name)
                    break

        else:
            self.button(QWizard.FinishButton).setEnabled(False)


    def get_fields_from_csv_file(self, csv_path):
        if not self.txt_delimiter.text().strip():
            return []

        errorReading = False
        try:
            reader  = open(csv_path, "r")
        except IOError:
            errorReading = True
        line = reader.readline().replace("\n", "")
        reader.close()
        if not line:
            errorReading = True
        else:
            return line.split(self.txt_delimiter.text().strip())

        if errorReading:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                QCoreApplication.translate("PointsSpatialUnitCadasterWizard",
                                           "It was not possible to read field names from the CSV. Check the file and try again."),
                QgsMessageBar.WARNING)
        return []

    def save_settings(self):
        settings = QSettings()
        settings.setValue('Asistente-LADM_COL/add_points_type', 'boundary_point' if self.rad_boundary_point.isChecked() else 'survey_point')
        settings.setValue('Asistente-LADM_COL/add_points_csv_file', self.txt_file_path.text().strip())
        settings.setValue('Asistente-LADM_COL/csv_file_delimiter', self.txt_delimiter.text().strip())

    def restore_settings(self):
        settings = QSettings()
        point_type = settings.value('Asistente-LADM_COL/add_points_type') or 'boundary_point'
        if point_type == 'boundary_point':
            self.rad_boundary_point.setChecked(True)
        else:
            self.rad_survey_point.setChecked(True)
        self.txt_file_path.setText(settings.value('Asistente-LADM_COL/add_points_csv_file'))
        self.txt_delimiter.setText(settings.value('Asistente-LADM_COL/csv_file_delimiter'))
