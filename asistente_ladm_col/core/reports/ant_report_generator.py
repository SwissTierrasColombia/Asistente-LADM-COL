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
import os
import json

from qgis.PyQt.QtWidgets import QDialog

from asistente_ladm_col.config.general_config import ANT_MAP_REPORT
from asistente_ladm_col.core.reports.base_report_generator import BaseReportGenerator
from asistente_ladm_col.gui.reports.ant_report_dialog import ANTReportDialog


class ANTReportGenerator(BaseReportGenerator):
    NO_BASEMAP = 'NO_BASEMAP'
    WMS_URL = 'URL'
    WMS_SUBLAYERS = 'SUBLAYERS'

    def __init__(self, db, ladm_data):
        super(ANTReportGenerator, self).__init__(db, ladm_data)
        self.report_name = ANT_MAP_REPORT

        self.__result_dict = dict()  # To store parameters obtained from the dialog and required for the report

    def update_json_data(self, json_spec_file, plot_feature, tmp_dir):
        """
        Overwrite parent method
        """
        json_data = dict()
        plot_id = plot_feature[self.db.names.T_ID_F]
        with open(json_spec_file) as f:
            json_data = json.load(f)

        json_data['attributes']['id'] = plot_id
        json_data['attributes']['zone'] = self.__result_dict['zone']
        json_data['attributes']['nameWhoElaborated'] = self.__result_dict['nameWhoElaborated']
        json_data['attributes']['licenseWhoElaborated'] = self.__result_dict['licenseWhoElaborated']
        json_data['attributes']['nameWhoRevised'] = self.__result_dict['nameWhoRevised']
        json_data['attributes']['licenseWhoRevised'] = self.__result_dict['licenseWhoRevised']
        json_data['attributes']['observationsReport'] = self.__result_dict['observationsReport']
        json_data['attributes']['datasetName'] = self.db.schema

        layers = json_data['attributes']['map']['layers']
        for layer in layers:
            if 'geoJson' in layer:
                result, data = self.get_geojson_layer(layer['name'], plot_id)
                if result:
                    layer['geoJson'] = self.create_geojson_file(data)

        overview_layers = json_data['attributes']['overviewMap']['layers']
        for layer in overview_layers:
            if 'geoJson' in layer:
                result, data = self.get_geojson_layer(layer['name'], plot_id)
                if result:
                    layer['geoJson'] = self.create_geojson_file(data)

        # WMS layer is added as a base map to be used in the report
        if not self.__result_dict[self.NO_BASEMAP]:
            overview_basemap = {
                "baseURL": self.__result_dict[self.WMS_URL],
                "opacity": 1,
                "type": "WMS",
                "layers": self.__result_dict[self.WMS_SUBLAYERS],
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

    def get_geojson_layer(self, layer_name, plot_id):
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

    def run(self):
        dlg = ANTReportDialog(self.report_name)
        res = dlg.exec_()
        if res == QDialog.Accepted:
            self.__result_dict = dlg.result_dict
            self.generate_report(dlg.output_folder)
