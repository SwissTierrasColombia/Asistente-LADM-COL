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
from qgis.PyQt.QtCore import (pyqtSignal,
                              QSettings,
                              QCoreApplication)
from qgis.PyQt.QtGui import QValidator
from qgis.PyQt.QtWidgets import QDialogButtonBox

from asistente_ladm_col.config.general_config import ANNEX_17_REPORT
from asistente_ladm_col.gui.reports.abs_report_factory import AbsReportFactory
from asistente_ladm_col.utils.qt_utils import (make_folder_selector,
                                               DirValidator,
                                               Validators)
from asistente_ladm_col.utils.ui import load_ui


class Annex17MapReport(AbsReportFactory):
    enable_action_requested = pyqtSignal(str, bool)

    def __init__(self, db):
        super(Annex17MapReport, self).__init__(db)
        self.validators = Validators()
        self.report_name = ANNEX_17_REPORT
        self.report_ui = "reports/annex_17_map_report_dialog.ui"
        load_ui(self.report_ui, self)
        self.init_gui()

    def init_gui(self):
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

    def save_settings(self):
        QSettings().setValue("Asistente-LADM-COL/reports/{}/save_into_dir".format(self.report_name), self.txt_file_path_folder_report.text().strip())

    def restore_settings(self):
        save_into_dir = QSettings().value("Asistente-LADM-COL/reports/{}/save_into_dir".format(self.report_name), "")
        self.txt_file_path_folder_report.setText(save_into_dir)
