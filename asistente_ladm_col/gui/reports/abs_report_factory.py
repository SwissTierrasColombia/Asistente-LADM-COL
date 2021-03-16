# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2018-10-17
        git sha              : :%H$
        copyright            : (C) 2018 by Germán Carrillo (BSF Swissphoto)
                             : (C) 2021 by Leonardo Cardona (BSF Swissphoto)
        email                : gcarrillo@linuxmail.org
                             : leo dot cardona dot p at gmail dot com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""
import functools
import json
import locale
import os
import stat
import tempfile
import time

from qgis.PyQt.QtCore import (Qt,
                              QObject,
                              QCoreApplication,
                              QSettings,
                              QProcess,
                              QEventLoop,
                              pyqtSignal)
from qgis.PyQt.QtWidgets import (QFileDialog,
                                 QProgressBar)
from qgis.core import QgsDataSourceUri

from asistente_ladm_col.config.general_config import (URL_REPORTS_LIBRARIES,
                                                      DEPENDENCY_REPORTS_DIR_NAME)
from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.utils.qt_utils import (normalize_local_url,
                                               OverrideCursor)
from asistente_ladm_col.lib.dependency.report_dependency import ReportDependency
from asistente_ladm_col.lib.dependency.java_dependency import JavaDependency


class AbsReportFactory(QObject):
    LOG_TAB = 'LADM-COL Reports'
    enable_action_requested = pyqtSignal(str, bool)

    def __init__(self, ladm_data):
        QObject.__init__(self)
        self.ladm_data = ladm_data
        self.logger = Logger()
        self.app = AppInterface()
        self.java_dependency = JavaDependency()
        self.java_dependency.download_dependency_completed.connect(self.download_java_complete)

        self.report_dependency = ReportDependency()
        self.report_dependency.download_dependency_completed.connect(self.download_report_complete)
        self.report_name = None

        self.encoding = locale.getlocale()[1]
        # This might be unset
        if not self.encoding:
            self.encoding = 'UTF8'

        self._downloading = False

    def stderr_ready(self, proc):
        text = bytes(proc.readAllStandardError()).decode(self.encoding)
        self.logger.critical(__name__, text, tab=self.LOG_TAB)

    def stdout_ready(self, proc):
        text = bytes(proc.readAllStandardOutput()).decode(self.encoding)
        self.logger.info(__name__, text, tab=self.LOG_TAB)

    def update_yaml_config(self, db, config_path):
        text = ''
        qgs_uri = QgsDataSourceUri(db.uri)

        with open(os.path.join(config_path, 'config_template.yaml')) as f:
            text = f.read()
            text = text.format(
                '{}',
                DB_USER = qgs_uri.username(),
                DB_PASSWORD = qgs_uri.password(),
                DB_HOST = qgs_uri.host(),
                DB_PORT = qgs_uri.port(),
                DB_NAME = qgs_uri.database()
            )
        new_file_path = os.path.join(config_path, self.get_tmp_filename('yaml_config', 'yaml'))

        with open(new_file_path, 'w') as new_yaml:
            new_yaml.write(text)

        return new_file_path

    def create_geojson_file(self, json_data):
        if json_data:
            report_data_dir = self.get_report_data_dir()
            file_name = self.get_tmp_filename('data', 'geojson')
            new_file_path = os.path.join(report_data_dir, file_name)

            with open(new_file_path, 'w') as new_geojson:
                new_geojson.write(json.dumps(json_data))
            return "file://{dirname}/{filename}".format(dirname=os.path.basename(report_data_dir), filename=file_name)
        return None

    def get_layer_geojson(self, db, layer_name, plot_id):
        raise NotImplementedError

    def update_json_data(self, db, json_spec_file, plot_id, tmp_dir):
        json_data = dict()
        with open(json_spec_file) as f:
            json_data = json.load(f)

        json_data['attributes']['id'] = plot_id
        json_data['attributes']['datasetName'] = db.schema
        layers = json_data['attributes']['map']['layers']
        for layer in layers:
            if 'geoJson' in layer:
                result, data = self.get_layer_geojson(db, layer['name'], plot_id)
                if result:
                    layer['geoJson'] = self.create_geojson_file(data)

        overview_layers = json_data['attributes']['overviewMap']['layers']
        for layer in overview_layers:
            if 'geoJson' in layer:
                result, data = self.get_layer_geojson(db, layer['name'], plot_id)
                if result:
                    layer['geoJson'] = self.create_geojson_file(data)

        new_json_file_path = os.path.join(tmp_dir, self.get_tmp_filename('json_data_{}'.format(plot_id), 'json'))
        with open(new_json_file_path, 'w') as new_json:
            new_json.write(json.dumps(json_data))

        return new_json_file_path

    def clean_report_data_dir(self):
        report_data_dir = os.path.join(DEPENDENCY_REPORTS_DIR_NAME, self.report_name, 'data')
        for dirpath, dirnames, filenames in os.walk(report_data_dir):
            for filename in filenames:
                os.unlink(os.path.join(dirpath, filename))

    def get_report_data_dir(self):
        report_data_dir = os.path.join(DEPENDENCY_REPORTS_DIR_NAME, self.report_name, 'data')
        if not os.path.exists(report_data_dir):
            os.makedirs(report_data_dir)
        return report_data_dir

    def get_tmp_dir(self, create_random=True):
        if create_random:
            return tempfile.mkdtemp()

        return tempfile.gettempdir()

    def get_tmp_filename(self, basename, extension='gpkg'):
        return "{}_{}.{}".format(basename, str(time.time()).replace(".",""), extension)

    def generate_report(self, db):
        # Check if mapfish and Jasper are installed, otherwise show where to
        # download them from and return
        if not self.report_dependency.check_if_dependency_is_valid():
            self.report_dependency.download_dependency(URL_REPORTS_LIBRARIES)
            return

        java_home_set = self.java_dependency.set_java_home()
        if not java_home_set:
            self.java_dependency.get_java_on_demand()
            self.logger.info_msg(__name__, QCoreApplication.translate("ReportGenerator",
                                                                         "Java is a prerequisite. Since it was not found, it is being configured..."))
            return

        plot_layer = self.app.core.get_layer(db, db.names.LC_PLOT_T, load=True)
        if not plot_layer:
            return

        selected_plots = plot_layer.selectedFeatures()
        if not selected_plots:
            self.logger.warning_msg(__name__, QCoreApplication.translate("ReportGenerator",
                                    "To generate reports, first select at least a plot!"))
            return

        # Where to store the reports?
        previous_folder = QSettings().value("Asistente-LADM-COL/reports/save_into_dir", ".")
        save_into_folder = QFileDialog.getExistingDirectory(
                        None,
                        QCoreApplication.translate("ReportGenerator", "Select a folder to save the reports to be generated"),
                        previous_folder)
        if not save_into_folder:
            self.logger.warning_msg(__name__, QCoreApplication.translate("ReportGenerator",
                                    "You need to select a folder where to save the reports before continuing."))
            return
        QSettings().setValue("Asistente-LADM-COL/reports/save_into_dir", save_into_folder)

        config_path = os.path.join(DEPENDENCY_REPORTS_DIR_NAME, self.report_name)
        json_spec_file = os.path.join(config_path, 'spec_json_file.json')

        script_name = ''
        if os.name == 'posix':
            script_name = 'print'
        elif os.name == 'nt':
            script_name = 'print.bat'

        script_path = os.path.join(DEPENDENCY_REPORTS_DIR_NAME, 'bin', script_name)
        if not os.path.isfile(script_path):
            self.logger.warning(__name__, "Script file for reports wasn't found! {}".format(script_path))
            return

        self.enable_action_requested.emit(self.report_name, False)

        # Update config file
        yaml_config_path = self.update_yaml_config(db, config_path)
        self.logger.debug(__name__, "Config file for reports: {}".format(yaml_config_path))

        total = len(selected_plots)
        step = 0
        count = 0
        tmp_dir = self.get_tmp_dir()

        # Progress bar setup
        progress = QProgressBar()
        if total == 1:
            progress.setRange(0, 0)
        else:
            progress.setRange(0, 100)
        progress.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.app.gui.create_progress_message_bar(
            QCoreApplication.translate("ReportGenerator", "Generating {} report{}...").format(total, '' if total == 1 else 's'),
            progress)

        polygons_with_holes = []

        with OverrideCursor(Qt.WaitCursor):
            for selected_plot in selected_plots:
                plot_id = selected_plot[db.names.T_ID_F]

                geometry = selected_plot.geometry()
                abstract_geometry = geometry.get()
                if abstract_geometry.ringCount() > 1:
                    polygons_with_holes.append(str(plot_id))
                    self.logger.warning(__name__, QCoreApplication.translate("ReportGenerator",
                        "Skipping Annex 17 for plot with {}={} because it has holes. The reporter module does not support such polygons.").format(db.names.T_ID_F, plot_id))
                    continue

                # Generate data file
                json_file = self.update_json_data(db, json_spec_file, plot_id, tmp_dir)
                self.logger.debug(__name__, "JSON file for reports: {}".format(json_file))

                # Run sh/bat passing config and data files
                proc = QProcess()
                proc.readyReadStandardError.connect(
                    functools.partial(self.stderr_ready, proc=proc))
                proc.readyReadStandardOutput.connect(
                    functools.partial(self.stdout_ready, proc=proc))

                parcel_number = self.ladm_data.get_parcels_related_to_plots(db, [plot_id], db.names.LC_PARCEL_T_PARCEL_NUMBER_F) or ['']
                self.app.gui.activate_layer(plot_layer)  # Previous function changed the selected layer, so, select again plot layer
                file_name = '{}_{}_{}.pdf'.format(self.report_name, plot_id, parcel_number[0])

                current_report_path = os.path.join(save_into_folder, file_name)
                proc.start(script_path, ['-config', yaml_config_path, '-spec', json_file, '-output', current_report_path])

                if not proc.waitForStarted():
                    # Grant execution permissions
                    os.chmod(script_path, stat.S_IXOTH | stat.S_IXGRP | stat.S_IXUSR | stat.S_IRUSR | stat.S_IRGRP)
                    proc.start(script_path, ['-config', yaml_config_path, '-spec', json_file, '-output', current_report_path])

                if not proc.waitForStarted():
                    proc = None
                    self.logger.warning(__name__, "Couldn't execute script to generate report...")
                else:
                    loop = QEventLoop()
                    proc.finished.connect(loop.exit)
                    loop.exec()

                    self.logger.debug(__name__, "{}:{}".format(plot_id, proc.exitCode()))
                    if proc.exitCode() == 0:
                        count += 1

                    step += 1
                    try:
                        progress.setValue(step * 100 / total)
                    except RuntimeError:
                        pass  # progressBar was deleted

        os.remove(yaml_config_path)
        self.clean_report_data_dir()

        self.enable_action_requested.emit(self.report_name, True)
        self.logger.clear_message_bar()

        if total == count:
            if total == 1:
                msg = QCoreApplication.translate("ReportGenerator", "The report <a href='file:///{}'>{}</a> was successfully generated!").format(normalize_local_url(save_into_folder), file_name)
            else:
                msg = QCoreApplication.translate("ReportGenerator", "All reports were successfully generated in folder <a href='file:///{path}'>{path}</a>!").format(path=normalize_local_url(save_into_folder))

            self.logger.success_msg(__name__, msg)
        else:
            details_msg = ''
            if polygons_with_holes:
                details_msg += QCoreApplication.translate("ReportGenerator",
                                                          " The following polygons were skipped because they have holes and are not supported: {}.").format(
                    ", ".join(polygons_with_holes))

            if total == 1:
                msg = QCoreApplication.translate("ReportGenerator", "The report for plot {} couldn't be generated!{} See QGIS log (tab '{}') for details.").format(plot_id, details_msg, self.LOG_TAB)
            else:
                if count == 0:
                    msg = QCoreApplication.translate("ReportGenerator", "No report could be generated!{} See QGIS log (tab '{}') for details.").format(details_msg, self.LOG_TAB)
                else:
                    msg = QCoreApplication.translate("ReportGenerator", "At least one report couldn't be generated!{details_msg} See QGIS log (tab '{log_tab}') for details. Go to <a href='file:///{path}'>{path}</a> to see the reports that were generated.").format(details_msg=details_msg, path=normalize_local_url(save_into_folder), log_tab=self.LOG_TAB)

            self.logger.warning_msg(__name__, msg)

    def download_java_complete(self):
        if self.java_dependency.fetcher_task and not self.java_dependency.fetcher_task.isCanceled():
            if self.java_dependency.check_if_dependency_is_valid():
                self.logger.info_msg(__name__, QCoreApplication.translate("ReportGenerator",
                                                                          "Java was successfully configured!"), 5)
        else:
            self.logger.warning_msg(__name__, QCoreApplication.translate("ReportGenerator",
                                                                         "You have just canceled the Java dependency download."), 5)

    def download_report_complete(self):
        if self.report_dependency.fetcher_task and not self.report_dependency.fetcher_task.isCanceled():
            if self.report_dependency.check_if_dependency_is_valid():
                self.logger.info_msg(__name__, QCoreApplication.translate("ReportGenerator",
                                                                          "Report dependency was successfully configured!"), 5)
        else:
            self.logger.warning_msg(__name__, QCoreApplication.translate("ReportGenerator",
                                                                         "You have just canceled the report dependency download."), 5)
