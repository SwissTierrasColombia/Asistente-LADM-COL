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
from qgis.PyQt.QtCore import pyqtSignal

from asistente_ladm_col.config.general_config import ANT_MAP_REPORT
from asistente_ladm_col.gui.reports.abs_report_factory import AbsReportFactory


class ANTMapReport(AbsReportFactory):
    enable_action_requested = pyqtSignal(str, bool)

    def __init__(self, ladm_data):
        super(ANTMapReport, self).__init__(ladm_data)
        self.report_name = ANT_MAP_REPORT

    def get_layer_geojson(self, db, layer_name, plot_id):
        if layer_name in ('terreno', 'terreno_overview', 'terrenos', 'terrenos_overview'):
            mode = True if layer_name in ('terreno', 'terreno_overview') else False
            overview = True if layer_name in ('terrenos_overview', 'terreno_overview') else False
            return db.get_ant_map_plot_data(plot_id, mode, overview)
        elif layer_name == 'linderos':
            return db.get_ant_map_boundaries(plot_id)
        elif layer_name == 'construcciones':
            return db.get_annex17_building_data(plot_id)
        elif layer_name == 'punto_lindero':
            return db.get_annex17_point_data(plot_id)
        elif layer_name in ('vias', 'vias_overview'):
            overview = False if layer_name == 'vias' else True
            return db.get_ant_map_road_nomenclature(plot_id, overview)
        elif layer_name in ('limite_urbano', 'limite_urbano_overview'):
            overview = False if layer_name == 'limite_urbano' else True
            return db.get_ant_map_urban_limit(plot_id, overview)
        elif layer_name in ('limite_municipio', 'limite_municipio_overview'):
            overview = False if layer_name == 'limite_municipio' else True
            return db.get_ant_map_municipality_boundary(plot_id, overview)
