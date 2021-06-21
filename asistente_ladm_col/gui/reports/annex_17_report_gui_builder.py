from qgis.PyQt.QtCore import (pyqtSignal,
                              QSettings,
                              QCoreApplication)
from qgis.PyQt.QtGui import QValidator
from qgis.PyQt.QtWidgets import (QDialog,
                                 QDialogButtonBox)

from asistente_ladm_col.utils.qt_utils import (make_folder_selector,
                                               DirValidator,
                                               Validators)
from asistente_ladm_col.utils import get_ui_class

DIALOG_ANNEX_17_REPORT_UI = get_ui_class('reports/annex_17_map_report_dialog.ui')


class Annex17ReportGUIBuilder(QDialog, DIALOG_ANNEX_17_REPORT_UI):
    def __init__(self, report_generator):
        QDialog.__init__(self)
        self.setupUi(self)
        self.validators = Validators()
        self.report_generator = report_generator
        self.report_name = self.report_generator.report_name
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
        return folder_path == QValidator.Acceptable

    def input_data_changed(self):
        self.set_generate_report_button_enabled(self.validate_inputs())

    def accepted(self):
        plot_layer = self.report_generator.app.core.get_layer(self.report_generator.db, self.report_generator.db.names.LC_PLOT_T, load=True)
        selected_plots = plot_layer.selectedFeatures()
        if not selected_plots:
            self.logger.warning_msg(__name__, QCoreApplication.translate("ReportGenerator",
                                                                         "To generate reports, first select at least a plot!"))
        save_into_folder = self.txt_file_path_folder_report.text().strip()
        self.save_settings()
        self.close()  # TODO: Close the dialog because canvas shows the progress bar. Dialog should control the progress bar
        self.report_generator.generate_report(plot_layer, selected_plots, save_into_folder)

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
