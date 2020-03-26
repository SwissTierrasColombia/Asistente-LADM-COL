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
import stat

from qgis.PyQt.QtCore import (Qt,
                              QSettings,
                              QCoreApplication,
                              QFile)
from qgis.PyQt.QtWidgets import (QWizard,
                                 QFileDialog,
                                 QSizePolicy,
                                 QGridLayout)
from qgis.core import (Qgis,
                       QgsMapLayerProxyModel,
                       QgsCoordinateReferenceSystem,
                       QgsWkbTypes)
from qgis.gui import QgsMessageBar

from asistente_ladm_col.config.general_config import (LAYER,
                                                      DEFAULT_EPSG)
from asistente_ladm_col.config.help_strings import HelpStrings
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.utils import get_ui_class
from asistente_ladm_col.utils.utils import show_plugin_help
from asistente_ladm_col.utils.qt_utils import (make_file_selector,
                                               OverrideCursor,
                                               enable_next_wizard,
                                               disable_next_wizard,
                                               normalize_local_url)

WIZARD_UI = get_ui_class('wizards/operation/wiz_create_points_operation.ui')


class CreatePointsOperationWizard(QWizard, WIZARD_UI):
    WIZARD_NAME = "CreatePointsOperationWizard"
    WIZARD_TOOL_NAME = QCoreApplication.translate(WIZARD_NAME, "Create Point")

    def __init__(self, iface, db, qgis_utils):
        QWizard.__init__(self)
        self.setupUi(self)
        self.iface = iface
        self._db = db
        self.qgis_utils = qgis_utils
        self.logger = Logger()
        self.names = self._db.names
        self.help_strings = HelpStrings()

        self._layers = {
            self.names.OP_BOUNDARY_POINT_T: {'name': self.names.OP_BOUNDARY_POINT_T, 'geometry': None, LAYER: None},
            self.names.OP_SURVEY_POINT_T: {'name': self.names.OP_SURVEY_POINT_T, 'geometry': None, LAYER: None},
            self.names.OP_CONTROL_POINT_T: {'name': self.names.OP_CONTROL_POINT_T, 'geometry': None, LAYER: None}
        }

        self.target_layer = None

        # Auxiliary data to set nonlinear next pages
        self.pages = [self.wizardPage1, self.wizardPage2, self.wizardPage3]
        self.dict_pages_ids = {self.pages[idx] : pid for idx, pid in enumerate(self.pageIds())}

        # Set connections
        self.btn_browse_file.clicked.connect(
            make_file_selector(self.txt_file_path,
                               file_filter=QCoreApplication.translate("WizardTranslations",'CSV File (*.csv *.txt)')))
        self.txt_file_path.textChanged.connect(self.file_path_changed)
        self.crsSelector.crsChanged.connect(self.crs_changed)
        self.crs = QgsCoordinateReferenceSystem()
        self.txt_delimiter.textChanged.connect(self.fill_long_lat_combos)

        self.known_delimiters = [
            {'name': ';', 'value': ';'},
            {'name': ',', 'value': ','},
            {'name': 'tab', 'value': '\t'},
            {'name': 'space', 'value': ' '},
            {'name': '|', 'value': '|'},
            {'name': '~', 'value': '~'},
            {'name': 'Other', 'value': ''}
        ]
        self.cbo_delimiter.addItems([ item['name'] for item in self.known_delimiters ])
        self.cbo_delimiter.currentTextChanged.connect(self.separator_changed)

        self.restore_settings()

        self.txt_file_path.textChanged.emit(self.txt_file_path.text())

        self.rad_boundary_point.toggled.connect(self.point_option_changed)
        self.rad_control_point.toggled.connect(self.point_option_changed)
        self.rad_csv.toggled.connect(self.adjust_page_2_controls)
        self.point_option_changed() # Initialize it
        self.button(QWizard.FinishButton).clicked.connect(self.finished_dialog)
        self.currentIdChanged.connect(self.current_page_changed)

        self.mMapLayerComboBox.setFilters(QgsMapLayerProxyModel.PointLayer)

        self.txt_help_page_2.setHtml(self.help_strings.WIZ_ADD_POINTS_OPERATION_PAGE_2_OPTION_CSV)

        self.wizardPage2.setButtonText(QWizard.FinishButton,
                                       QCoreApplication.translate("WizardTranslations",
                                            "Import"))
        self.txt_help_page_3.setHtml(self.help_strings.WIZ_ADD_POINTS_OPERATION_PAGE_3_OPTION_CSV)
        self.txt_help_page_3.anchorClicked.connect(self.save_template)
        self.button(QWizard.HelpButton).clicked.connect(self.show_help)
        self.rejected.connect(self.close_wizard)

        # Set MessageBar for QWizard
        self.bar = QgsMessageBar()
        self.bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.setLayout(QGridLayout())
        self.layout().addWidget(self.bar, 0, 0, Qt.AlignTop)

    def nextId(self):
        """
        Set navigation order. Should return an integer. -1 is Finish.
        """
        if self.currentId() == self.dict_pages_ids[self.wizardPage1]:
            return self.dict_pages_ids[self.wizardPage2]
        elif self.currentId() == self.dict_pages_ids[self.wizardPage2]:
            if self.rad_csv.isChecked():
                return self.dict_pages_ids[self.wizardPage3]
            elif self.rad_refactor.isChecked():
                return -1
        elif self.currentId() == self.dict_pages_ids[self.wizardPage3]:
            return -1
        else:
            return -1

    def current_page_changed(self, id):
        """
        Reset the Next button. Needed because Next might have been disabled by a
        condition in a another SLOT.
        """
        enable_next_wizard(self)

        if id == self.dict_pages_ids[self.wizardPage2]:
            self.adjust_page_2_controls()
        elif id == self.dict_pages_ids[self.wizardPage3]:
            self.set_buttons_visible(False)
            self.set_buttons_enabled(False)

            QCoreApplication.processEvents()
            self.check_z_in_geometry()
            QCoreApplication.processEvents()
            self.fill_long_lat_combos("")
            QCoreApplication.processEvents()

            self.set_buttons_visible(True)
            self.set_buttons_enabled(True)

    def set_buttons_visible(self, visible):
        self.button(self.BackButton).setVisible(visible)
        self.button(self.FinishButton).setVisible(visible)
        self.button(self.CancelButton).setVisible(visible)

    def set_buttons_enabled(self, enabled):
        self.wizardPage3.setEnabled(enabled)
        self.button(self.BackButton).setEnabled(enabled)
        self.button(self.FinishButton).setEnabled(enabled)
        self.button(self.CancelButton).setEnabled(enabled)

    def check_z_in_geometry(self):
        self.target_layer = self.qgis_utils.get_layer(self._db, self.current_point_name(), load=True)
        if not self.target_layer:
            return

        if not QgsWkbTypes().hasZ(self.target_layer.wkbType()):
            self.labelZ.setEnabled(False)
            self.cbo_elevation.setEnabled(False)
            msg = QCoreApplication.translate("WizardTranslations",
                                             "The current model does not support 3D geometries")
            self.cbo_elevation.setToolTip(msg)
            self.labelZ.setToolTip(msg)
        else:
            self.labelZ.setEnabled(True)
            self.cbo_elevation.setEnabled(True)
            self.labelZ.setToolTip("")
            self.cbo_elevation.setToolTip("")

    def adjust_page_2_controls(self):
        self.cbo_mapping.clear()
        self.cbo_mapping.addItem("")
        self.cbo_mapping.addItems(self.qgis_utils.get_field_mappings_file_names(self.current_point_name()))

        if self.rad_refactor.isChecked():
            self.lbl_refactor_source.setEnabled(True)
            self.mMapLayerComboBox.setEnabled(True)
            self.lbl_field_mapping.setEnabled(True)
            self.cbo_mapping.setEnabled(True)

            disable_next_wizard(self)
            self.wizardPage2.setFinalPage(True)
            self.txt_help_page_2.setHtml(self.help_strings.get_refactor_help_string(self._db, self._layers[self.current_point_name()][LAYER]))

        elif self.rad_csv.isChecked():
            self.lbl_refactor_source.setEnabled(False)
            self.mMapLayerComboBox.setEnabled(False)
            self.lbl_field_mapping.setEnabled(False)
            self.cbo_mapping.setEnabled(False)

            enable_next_wizard(self)
            self.wizardPage2.setFinalPage(False)
            self.txt_help_page_2.setHtml(self.help_strings.WIZ_ADD_POINTS_OPERATION_PAGE_2_OPTION_CSV)

    def point_option_changed(self):
        if self.rad_boundary_point.isChecked():
            self.gbx_page_2.setTitle(QCoreApplication.translate("WizardTranslations", "Load data to Boundary Points..."))
            self.gbx_page_3.setTitle(QCoreApplication.translate("WizardTranslations", "Configure CSV data source for Boundary Points..."))
            self.txt_help_page_1.setHtml(self.help_strings.WIZ_ADD_POINTS_OPERATION_PAGE_1_OPTION_BP)
        elif self.rad_survey_point.isChecked(): # self.rad_survey_point is checked
            self.gbx_page_2.setTitle(QCoreApplication.translate("WizardTranslations", "Load data to Survey Points..."))
            self.gbx_page_3.setTitle(QCoreApplication.translate("WizardTranslations", "Configure CSV data source for Survey Points..."))
            self.txt_help_page_1.setHtml(self.help_strings.WIZ_ADD_POINTS_OPERATION_PAGE_1_OPTION_SP)
        else: # self.rad_control_point is checked
            self.gbx_page_2.setTitle(QCoreApplication.translate("WizardTranslations", "Load data to Control Points..."))
            self.gbx_page_3.setTitle(QCoreApplication.translate("WizardTranslations", "Configure CSV data source for Control Points..."))
            self.txt_help_page_1.setHtml(self.help_strings.WIZ_ADD_POINTS_OPERATION_PAGE_1_OPTION_CP)

    def finished_dialog(self):
        self.save_settings()

        if self.rad_refactor.isChecked():
            output_layer_name = self.current_point_name()

            if self.mMapLayerComboBox.currentLayer() is not None:
                field_mapping = self.cbo_mapping.currentText()
                res_etl_model = self.qgis_utils.show_etl_model(self._db,
                                                               self.mMapLayerComboBox.currentLayer(),
                                                               output_layer_name,
                                                               field_mapping=field_mapping)

                if res_etl_model:
                    if field_mapping:
                        self.qgis_utils.delete_old_field_mapping(field_mapping)

                    self.qgis_utils.save_field_mapping(output_layer_name)

            else:
                self.logger.warning_msg(__name__, QCoreApplication.translate("WizardTranslations",
                    "Select a source layer to set the field mapping to '{}'.").format(output_layer_name))

            self.close_wizard()

        elif self.rad_csv.isChecked():
            self.prepare_copy_csv_points_to_db()

    def close_wizard(self, message=None, show_message=True):
        if message is None:
            message = QCoreApplication.translate("WizardTranslations", "'{}' tool has been closed.").format(self.WIZARD_TOOL_NAME)
        if show_message:
            self.logger.info_msg(__name__, message)
        self.close()

    def current_point_name(self):
        if self.rad_boundary_point.isChecked():
            return self.names.OP_BOUNDARY_POINT_T
        elif self.rad_survey_point.isChecked():
            return self.names.OP_SURVEY_POINT_T
        else:
            return self.names.OP_CONTROL_POINT_T

    def prepare_copy_csv_points_to_db(self):
        csv_path = self.txt_file_path.text().strip()

        if not csv_path or not os.path.exists(csv_path):
            self.logger.warning_msg(__name__, QCoreApplication.translate("WizardTranslations",
                                                                         "No CSV file given or file doesn't exist."))
            return

        target_layer_name = self.current_point_name()

        with OverrideCursor(Qt.WaitCursor):
            csv_layer = self.qgis_utils.csv_to_layer(csv_path,
                                                     self.txt_delimiter.text(),
                                                     self.cbo_longitude.currentText(),
                                                     self.cbo_latitude.currentText(),
                                                     self.epsg,
                                                     self.cbo_elevation.currentText() or None,
                                                     self.detect_decimal_point(csv_path))

            self.qgis_utils.copy_csv_to_db(csv_layer, self._db, target_layer_name)

    def required_layers_are_available(self):
        layers_are_available = self.qgis_utils.required_layers_are_available(self._db, self._layers, self.WIZARD_TOOL_NAME)
        return layers_are_available

    def file_path_changed(self):
        self.autodetect_separator()
        self.fill_long_lat_combos("")
        self.cbo_delimiter.currentTextChanged.connect(self.separator_changed)

    def detect_decimal_point(self, csv_path):
        if os.path.exists(csv_path):
            with open(csv_path) as file:
                file.readline() # headers
                data = file.readline().strip() # 1st line with data

            if data:
                fields = self.get_fields_from_csv_file(csv_path)
                if self.cbo_latitude.currentText() in fields:
                    num_col = data.split(self.cbo_delimiter.currentText())[fields.index(self.cbo_latitude.currentText())]
                    for decimal_point in ['.', ',']:
                        if decimal_point in num_col:
                            return decimal_point

        return '.' # just use the default one

    def autodetect_separator(self):
        csv_path = self.txt_file_path.text().strip()
        if os.path.exists(csv_path):
            with open(csv_path) as file:
                first_line = file.readline()
                for delimiter in self.known_delimiters:
                    if delimiter['value'] == '':
                        continue
                    # if separator works like a column separator in header
                    # number of cols is greater than 1
                    if len(first_line.split(delimiter['value'])) > 1:
                        self.cbo_delimiter.setCurrentText(delimiter['name'])
                        return

    def update_crs_info(self):
        self.crsSelector.setCrs(self.crs)

    def crs_changed(self):
        authid = self.crsSelector.crs().authid()
        self.epsg = int(authid[5:])

    def fill_long_lat_combos(self, text):
        csv_path = self.txt_file_path.text().strip()
        self.cbo_longitude.clear()
        self.cbo_latitude.clear()
        self.cbo_elevation.clear()
        if os.path.exists(csv_path):
            self.button(QWizard.FinishButton).setEnabled(True)

            fields = self.get_fields_from_csv_file(csv_path)
            fields_dict = {field: field.lower() for field in fields}
            if not fields:
                self.button(QWizard.FinishButton).setEnabled(False)
                return

            self.cbo_longitude.addItems(fields)
            self.cbo_latitude.addItems(fields)
            self.cbo_elevation.addItems([""] + fields)

            # Heuristics to suggest values for x, y and z
            x_potential_names = ['x', 'lon', 'long', 'longitud', 'longitude', 'este', 'east', 'oeste', 'west']
            y_potential_names = ['y', 'lat', 'latitud', 'latitude', 'norte', 'north']
            z_potential_names = ['z', 'altura', 'elevacion', 'elevation', 'elevación', 'height']
            for x_potential_name in x_potential_names:
                for k,v in fields_dict.items():
                    if x_potential_name == v:
                        self.cbo_longitude.setCurrentText(k)
                        break
            for y_potential_name in y_potential_names:
                for k, v in fields_dict.items():
                    if y_potential_name == v:
                        self.cbo_latitude.setCurrentText(k)
                        break
            if self.cbo_elevation.isEnabled():
                for z_potential_name in z_potential_names:
                    for k, v in fields_dict.items():
                        if z_potential_name == v:
                            self.cbo_elevation.setCurrentText(k)
                            break

        else:
            self.button(QWizard.FinishButton).setEnabled(False)

    def get_fields_from_csv_file(self, csv_path):
        if not self.txt_delimiter.text():
            return []

        error_reading = False
        try:
            reader  = open(csv_path, "r")
        except IOError:
            error_reading = True
        line = reader.readline().replace("\n", "")
        reader.close()
        if not line:
            error_reading = True
        else:
            return line.split(self.txt_delimiter.text())

        if error_reading:
            self.logger.warning_msg(__name__, QCoreApplication.translate("WizardTranslations",
                "It was not possible to read field names from the CSV. Check the file and try again."))
        return []

    def separator_changed(self, text):
        # first ocurrence
        value = next((x['value'] for x in self.known_delimiters if x['name'] == text), '')
        self.txt_delimiter.setText(value)
        if value == '':
            self.txt_delimiter.setEnabled(True)
        else:
            self.txt_delimiter.setEnabled(False)

    def save_template(self, url):
        link = url.url()
        if self.rad_boundary_point.isChecked():
            if link == '#template':
                self.download_csv_file('template_boundary_points.csv')
            elif link == '#data':
                self.download_csv_file('sample_boundary_points.csv')
        elif self.rad_survey_point.isChecked():
            if link == '#template':
                self.download_csv_file('template_survey_points.csv')
            elif link == '#data':
                self.download_csv_file('sample_survey_points.csv')
        elif self.rad_control_point.isChecked():
            if link == '#template':
                self.download_csv_file('template_control_points.csv')
            elif link == '#data':
                self.download_csv_file('sample_control_points.csv')

    def download_csv_file(self, filename):
        settings = QSettings()
        settings.setValue('Asistente-LADM_COL/wizards/points_csv_file_delimiter', self.txt_delimiter.text().strip())

        new_filename, filter = QFileDialog.getSaveFileName(self,
                                   QCoreApplication.translate("WizardTranslations",
                                                              "Save File"),
                                   os.path.join(settings.value('Asistente-LADM_COL/wizards/points_download_csv_path', '.'), filename),
                                   QCoreApplication.translate("WizardTranslations",
                                                              "CSV File (*.csv *.txt)"))

        if new_filename:
            settings.setValue('Asistente-LADM_COL/wizards/points_download_csv_path', os.path.dirname(new_filename))
            template_file = QFile(":/Asistente-LADM_COL/resources/csv/" + filename)

            if not template_file.exists():
                self.logger.critical(__name__, "CSV doesn't exist! Probably due to a missing 'make' execution to generate resources...")
                msg = QCoreApplication.translate("WizardTranslations", "CSV file not found. Update your plugin. For details see log.")
                self.show_message(msg, Qgis.Warning)
                return

            if os.path.isfile(new_filename):
                self.logger.info(__name__, 'Removing existing file {}...'.format(new_filename))
                os.chmod(new_filename, 0o777)
                os.remove(new_filename)

            if template_file.copy(new_filename):
                os.chmod(new_filename, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
                msg = QCoreApplication.translate("WizardTranslations", """The file <a href="file:///{}">{}</a> was successfully saved!""").format(normalize_local_url(new_filename), os.path.basename(new_filename))
                self.show_message(msg, Qgis.Info)
            else:
                self.logger.warning(__name__, 'There was an error copying the CSV file {}!'.format(new_filename))
                msg = QCoreApplication.translate("WizardTranslations", "The file couldn\'t be saved.")
                self.show_message(msg, Qgis.Warning)

    def show_message(self, message, level):
        self.bar.clearWidgets()  # Remove previous messages before showing a new one
        self.bar.pushMessage(message, level, 10)

    def save_settings(self):
        settings = QSettings()
        point_type = None
        if self.rad_boundary_point.isChecked():
            point_type = 'boundary_point'
        elif self.rad_survey_point.isChecked():
            point_type = 'survey_point'
        else:
            point_type = 'control_point'

        settings.setValue('Asistente-LADM_COL/wizards/points_add_points_type', point_type)
        settings.setValue('Asistente-LADM_COL/wizards/points_load_data_type', 'csv' if self.rad_csv.isChecked() else 'refactor')
        settings.setValue('Asistente-LADM_COL/wizards/points_add_points_csv_file', self.txt_file_path.text().strip())
        settings.setValue('Asistente-LADM_COL/wizards/points_csv_file_delimiter', self.txt_delimiter.text().strip())
        settings.setValue('Asistente-LADM_COL/wizards/points_csv_epsg', self.epsg)

    def restore_settings(self):
        settings = QSettings()
        point_type = settings.value('Asistente-LADM_COL/wizards/points_add_points_type') or 'boundary_point'
        if point_type == 'boundary_point':
            self.rad_boundary_point.setChecked(True)
        elif point_type == 'survey_point':
            self.rad_survey_point.setChecked(True)
        else: # 'control_point'
            self.rad_control_point.setChecked(True)

        load_data_type = settings.value('Asistente-LADM_COL/wizards/points_load_data_type') or 'csv'
        if load_data_type == 'refactor':
            self.rad_refactor.setChecked(True)
        else:
            self.rad_csv.setChecked(True)

        self.txt_file_path.setText(settings.value('Asistente-LADM_COL/wizards/points_add_points_csv_file'))
        self.txt_delimiter.setText(settings.value('Asistente-LADM_COL/wizards/points_csv_file_delimiter'))

        self.crs = QgsCoordinateReferenceSystem(
            settings.value('Asistente-LADM_COL/wizards/points_csv_epsg', DEFAULT_EPSG, int))
        self.update_crs_info()

    def show_help(self):
        show_plugin_help("create_points")
