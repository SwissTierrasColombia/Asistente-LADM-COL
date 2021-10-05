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
from qgis.PyQt.QtWidgets import QDialog

from asistente_ladm_col.config.general_config import ANNEX_17_REPORT
from asistente_ladm_col.core.reports.base_report_generator import BaseReportGenerator
from asistente_ladm_col.gui.reports.annex_17_report_dialog import Annex17ReportDialog


class Annex17ReportGenerator(BaseReportGenerator):

    def __init__(self, db, ladm_data):
        super(Annex17ReportGenerator, self).__init__(db, ladm_data)
        self.report_name = ANNEX_17_REPORT

    def get_file_name(self, plot_id):
        parcel_number = self.ladm_data.get_parcels_related_to_plots(self.db, [plot_id], self.db.names.LC_PARCEL_T_PARCEL_NUMBER_F) or ['']
        return '{}_{}_{}.pdf'.format(self.report_name, plot_id, parcel_number[0])

    def get_geojson_layer(self, layer_name, plot_id):
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
        dlg = Annex17ReportDialog(self.report_name)
        res = dlg.exec_()
        if res == QDialog.Accepted:
            # We have validated
            self.generate_report(dlg.output_folder)

    def _spatial_layers_to_validate(self):
        return {
            self.db.names.LC_PLOT_T: None,
            self.db.names.LC_BUILDING_T: None,
            self.db.names.LC_BOUNDARY_T: None,
            self.db.names.LC_BOUNDARY_POINT_T: None
        }