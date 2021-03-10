# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-08-21
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
import os
import json
from math import ceil, floor

from qgis.core import QgsProject
from qgis.PyQt.QtCore import (pyqtSignal,
                              QSettings,
                              QCoreApplication)
from qgis.PyQt.QtGui import QValidator
from qgis.PyQt.QtWidgets import QDialogButtonBox

from asistente_ladm_col.config.general_config import ANT_MAP_REPORT
from asistente_ladm_col.gui.reports.abs_report_factory import AbsReportFactory
from asistente_ladm_col.utils.ui import load_ui
from asistente_ladm_col.utils.qt_utils import (make_folder_selector,
                                               DirValidator,
                                               Validators)


class ANTMapReport(AbsReportFactory):
    enable_action_requested = pyqtSignal(str, bool)
    URBAN_ZONE = 'ZONA_URBANA'
    RURAL_ZONE = 'ZONA_RURAL'
    NO_BASEMAP = 'NO_BASEMAP'
    WMS_NAME = 'NAME'
    WMS_URL = 'URL'
    WMS_SUBLAYERS = 'SUBLAYERS'

    def __init__(self, db):
        super(ANTMapReport, self).__init__(db)
        self.validators = Validators()
        self.report_name = ANT_MAP_REPORT
        self.report_ui = "reports/ant_map_report_dialog.ui"
        self._wms_basemaps = dict()
        load_ui(self.report_ui, self)
        self.init_gui()

    def init_gui(self):
        self.zone_combobox.clear()
        self.zone_combobox.addItem(QCoreApplication.translate("ReportGenerator", "Urban"), self.URBAN_ZONE)
        self.zone_combobox.addItem(QCoreApplication.translate("ReportGenerator", "Rural"), self.RURAL_ZONE)

        self.register_wms_basemaps()  # List WMS load by the user in the map canvas
        self.basemap_combobox.clear()
        self.basemap_combobox.addItem(QCoreApplication.translate("ReportGenerator", "No basemap"), self.NO_BASEMAP)

        for layer_id, wms_params in self._wms_basemaps.items():
            self.basemap_combobox.addItem(wms_params[self.WMS_NAME], layer_id)

        self.buttonBox.accepted.disconnect()
        self.buttonBox.accepted.connect(self.accepted)
        self.buttonBox.button(QDialogButtonBox.Ok).setText(QCoreApplication.translate("ReportGenerator", "Generate"))
        self.set_generate_report_button_enabled(False)

        self.btn_browse_file_folder_report.clicked.connect(make_folder_selector(self.txt_file_path_folder_report, title='Output folder', parent=None))
        dir_validator_folder = DirValidator(pattern=None, allow_empty_dir=True)
        self.txt_file_path_folder_report.setValidator(dir_validator_folder)
        self.txt_file_path_folder_report.textChanged.connect(self.validators.validate_line_edits)
        self.txt_file_path_folder_report.textChanged.connect(self.input_data_changed)
        self.restore_settings()

    def register_wms_basemaps(self):
        for layer in QgsProject.instance().mapLayers().values():
            if layer.isSpatial() and layer.isValid() and layer.providerType() == 'wms':
                basemap = dict()
                basemap[self.WMS_NAME] = layer.name()
                basemap[self.WMS_SUBLAYERS] = layer.subLayers()
                for param in layer.source().split('&'):
                    if param.startswith('url'):
                        basemap[self.WMS_URL] = param.split('=')[1]
                self._wms_basemaps[layer.id()] = basemap

    def set_generate_report_button_enabled(self, enable):
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(enable)

    def validate_inputs(self):
        folder_path = self.txt_file_path_folder_report.validator().validate(self.txt_file_path_folder_report.text().strip(), 0)[0]

        if folder_path == QValidator.Acceptable:
            return True
        else:
            return False

    def input_data_changed(self):
        self.set_generate_report_button_enabled(self.validate_inputs())

    def accepted(self):
        plot_layer = self.app.core.get_layer(self.db, self.db.names.LC_PLOT_T, load=True)
        selected_plots = plot_layer.selectedFeatures()
        if not selected_plots:
            self.logger.warning_msg(__name__, QCoreApplication.translate("ReportGenerator",
                                                                         "To generate reports, first select at least a plot!"))
        save_into_folder = self.txt_file_path_folder_report.text().strip()
        self.save_settings()
        self.close()  # TODO: Close the dialog because canvas show the progress bar. Dialog should control the progress bar
        self.generate_report(plot_layer, selected_plots, save_into_folder)

    def update_json_data(self, json_spec_file, plot_feature, tmp_dir):
        json_data = dict()
        plot_id = plot_feature[self.db.names.T_ID_F]
        with open(json_spec_file) as f:
            json_data = json.load(f)

        json_data['attributes']['id'] = plot_id
        json_data['attributes']['zone'] = self.zone_combobox.currentData()
        json_data['attributes']['nameWhoElaborated'] = self.text_name_who_elaborated.text().strip()
        json_data['attributes']['licenseWhoElaborated'] = self.text_license_who_elaborated.text().strip()
        json_data['attributes']['nameWhoRevised'] = self.txt_name_who_revised.text().strip()
        json_data['attributes']['licenseWhoRevised'] = self.txt_license_who_revised.text().strip()
        json_data['attributes']['observationsReport'] = self.txt_observations_report.toPlainText()
        json_data['attributes']['datasetName'] = self.db.schema

        layers = json_data['attributes']['map']['layers']
        for layer in layers:
            if 'geoJson' in layer:
                result, data = self.get_layer_geojson(layer['name'], plot_id)
                if result:
                    layer['geoJson'] = self.create_geojson_file(data)

        overview_layers = json_data['attributes']['overviewMap']['layers']
        for layer in overview_layers:
            if 'geoJson' in layer:
                result, data = self.get_layer_geojson(layer['name'], plot_id)
                if result:
                    layer['geoJson'] = self.create_geojson_file(data)

        # WMS layer is added as a base map to be used in the report
        selected_basemap = self.basemap_combobox.currentData()
        if selected_basemap != self.NO_BASEMAP:
            overview_basemap = {
                "baseURL": self._wms_basemaps[selected_basemap][self.WMS_URL],
                "opacity": 1,
                "type": "WMS",
                "layers": self._wms_basemaps[selected_basemap][self.WMS_SUBLAYERS],
                "imageFormat": "image/png",
                "customParams": {
                    "TRANSPARENT": "true"
                }
            }
            overview_layers.append(overview_basemap)

        new_json_file_path = os.path.join(tmp_dir, self.get_tmp_filename('json_data_{}'.format(plot_id), 'json'))
        with open(new_json_file_path, 'w') as new_json:
            new_json.write(json.dumps(json_data))

        return new_json_file_path

    def get_layer_geojson(self, layer_name, plot_id):
        if layer_name in ('terreno', 'terreno_overview', 'terrenos', 'terrenos_overview'):
            mode = True if layer_name in ('terreno', 'terreno_overview') else False
            overview = True if layer_name in ('terrenos_overview', 'terreno_overview') else False
            return self.db.get_ant_map_plot_data(plot_id, mode, overview)
        elif layer_name == 'construcciones':
            return self.db.get_ant_building_data(plot_id)
        elif layer_name == 'punto_lindero':
            return self.db.get_annex17_point_data(plot_id)
        elif layer_name in ('vias', 'vias_overview'):
            overview = False if layer_name == 'vias' else True
            return self.db.get_ant_map_road_nomenclature(plot_id, overview)
        elif layer_name in ('limite_urbano', 'limite_urbano_overview'):
            overview = False if layer_name == 'limite_urbano' else True
            return self.db.get_ant_map_urban_limit(plot_id, overview)
        elif layer_name in ('limite_municipio', 'limite_municipio_overview'):
            overview = False if layer_name == 'limite_municipio' else True
            return self.db.get_ant_map_municipality_boundary(plot_id, overview)

    def save_settings(self):
        QSettings().setValue("Asistente-LADM-COL/reports/{}/save_into_dir".format(self.report_name), self.txt_file_path_folder_report.text().strip())
        QSettings().setValue("Asistente-LADM-COL/reports/{}/zone".format(self.report_name), self.zone_combobox.currentData())
        QSettings().setValue("Asistente-LADM-COL/reports/{}/name_who_elaborated".format(self.report_name), self.text_name_who_elaborated.text().strip())
        QSettings().setValue("Asistente-LADM-COL/reports/{}/license_who_elaborated".format(self.report_name), self.text_license_who_elaborated.text().strip())
        QSettings().setValue("Asistente-LADM-COL/reports/{}/name_who_revised".format(self.report_name), self.txt_name_who_revised.text().strip())
        QSettings().setValue("Asistente-LADM-COL/reports/{}/license_who_revised".format(self.report_name), self.txt_license_who_revised.text().strip())
        QSettings().setValue("Asistente-LADM-COL/reports/{}/observations_report".format(self.report_name), self.txt_observations_report.toPlainText())

    def restore_settings(self):
        save_into_dir = QSettings().value("Asistente-LADM-COL/reports/{}/save_into_dir".format(self.report_name), "")
        self.txt_file_path_folder_report.setText(save_into_dir)

        zone = QSettings().value("Asistente-LADM-COL/reports/{}/zone".format(self.report_name), self.URBAN_ZONE)
        index_zone = self.zone_combobox.findData(zone)
        if index_zone == -1:
            index_zone = self.cbo_db_engine.findData(self.URBAN_ZONE)
        self.zone_combobox.setCurrentIndex(index_zone)

        name_who_elaborated = QSettings().value("Asistente-LADM-COL/reports/{}/name_who_elaborated".format(self.report_name), "")
        self.text_name_who_elaborated.setText(name_who_elaborated)

        license_who_elaborated = QSettings().value("Asistente-LADM-COL/reports/{}/license_who_elaborated".format(self.report_name), "")
        self.text_license_who_elaborated.setText(license_who_elaborated)

        name_who_revised = QSettings().value("Asistente-LADM-COL/reports/{}/name_who_revised".format(self.report_name), "")
        self.txt_name_who_revised.setText(name_who_revised)

        license_who_revised = QSettings().value("Asistente-LADM-COL/reports/{}/license_who_revised".format(self.report_name), "")
        self.txt_license_who_revised.setText(license_who_revised)

        observations_report = QSettings().value("Asistente-LADM-COL/reports/{}/observations_report".format(self.report_name), "")
        self.txt_observations_report.setPlainText(observations_report)
