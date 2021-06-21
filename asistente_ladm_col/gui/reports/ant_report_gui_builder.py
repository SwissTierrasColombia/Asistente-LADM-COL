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


class ANTReportGUIBuilder(QDialog, DIALOG_ANT_REPORT_UI):
    URBAN_ZONE = 'ZONA_URBANA'
    RURAL_ZONE = 'ZONA_RURAL'
    NO_BASEMAP = 'NO_BASEMAP'
    WMS_NAME = 'NAME'
    WMS_URL = 'URL'
    WMS_SUBLAYERS = 'SUBLAYERS'

    def __init__(self, report_generator):
        QDialog.__init__(self)
        self.setupUi(self)
        self.validators = Validators()
        self.report_generator = report_generator
        self.report_name = self.report_generator.report_name
        self.wms_basemaps = dict()
        self.init_gui()

    def init_gui(self):
        self.zone_combobox.clear()
        self.zone_combobox.addItem(QCoreApplication.translate("ReportGenerator", "Urban"), self.URBAN_ZONE)
        self.zone_combobox.addItem(QCoreApplication.translate("ReportGenerator", "Rural"), self.RURAL_ZONE)

        self.register_wms_basemaps()  # List WMS loaded by the user in the map canvas
        self.basemap_combobox.clear()
        self.basemap_combobox.addItem(QCoreApplication.translate("ReportGenerator", "No basemap"), self.NO_BASEMAP)

        for layer_id, wms_params in self.wms_basemaps.items():
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
            if layer.isValid() and layer.providerType() == 'wms':
                basemap = dict()
                basemap[self.WMS_NAME] = layer.name()
                basemap[self.WMS_SUBLAYERS] = layer.subLayers()
                for param in layer.source().split('&'):
                    if param.startswith('url'):
                        basemap[self.WMS_URL] = param.split('=')[1]
                self.wms_basemaps[layer.id()] = basemap

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
