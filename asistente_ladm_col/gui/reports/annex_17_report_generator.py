# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2018-10-17
        git sha              : :%H$
        copyright            : (C) 2018 by Germán Carrillo (BSF Swissphoto)
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
from asistente_ladm_col.config.general_config import ANNEX_17_REPORT
from asistente_ladm_col.gui.reports.abs_report_factory import AbsReportFactory
from asistente_ladm_col.gui.reports.annex_17_report_gui_builder import Annex17ReportGUIBuilder


class Annex17ReportGenerator(AbsReportFactory):

    def __init__(self, db, ladm_data):
        super(Annex17ReportGenerator, self).__init__(db, ladm_data)
        self.report_name = ANNEX_17_REPORT
        self.gui_builder = Annex17ReportGUIBuilder(self)

    def get_layer_geojson(self, layer_name, plot_id):
        if layer_name in ('terreno', 'terreno_overview', 'terrenos', 'terrenos_overview'):
            # True if you want the selected plot and False if you want the plots surrounding the selected plot
            mode = True if layer_name in ('terreno', 'terreno_overview') else False
            overview = True if layer_name in ('terrenos_overview', 'terreno_overview') else False
            return self.db.get_annex17_plot_data(plot_id, mode, overview)
        elif layer_name == 'construcciones':
            return self.db.get_annex17_building_data(plot_id)
        elif layer_name == 'punto_lindero':
            return self.db.get_annex17_point_data(plot_id)

    def run(self):
        self.gui_builder.exec_()
