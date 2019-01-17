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
import functools
import json
import locale
import os
import stat
import shutil
import tempfile
import time
import zipfile

from qgis.PyQt.QtCore import (Qt,
                              QCoreApplication,
                              QSettings,
                              QUrl,
                              QFile,
                              QProcess,
                              QEventLoop,
                              QIODevice)
from qgis.PyQt.QtWidgets import (QFileDialog,
                                 QProgressBar)
from qgis.core import (QgsWkbTypes,
                       QgsDataSourceUri,
                       Qgis,
                       QgsNetworkContentFetcherTask,
                       QgsApplication)

from ..config.general_config import (TEST_SERVER,
                                     PLUGIN_NAME,
                                     REPORTS_REQUIRED_VERSION,
                                     URL_REPORTS_LIBRARIES)
from ..config.table_mapping_config import (ID_FIELD,
                                           PLOT_TABLE)
from ..utils.qt_utils import (OverrideCursor,
                              remove_readonly,
                              normalize_local_url)

class ReportGenerator():
    def __init__(self, qgis_utils):
        self.qgis_utils = qgis_utils
        self.encoding = locale.getlocale()[1]
        # This might be unset
        if not self.encoding:
            self.encoding = 'UTF8'

        self.log = QgsApplication.messageLog()
        self.LOG_TAB = 'Anexo_17'
        self._downloading = False

    def stderr_ready(self, proc):
        text = bytes(proc.readAllStandardError()).decode(self.encoding)
        self.log.logMessage(text, self.LOG_TAB, Qgis.Critical)

    def stdout_ready(self, proc):
        text = bytes(proc.readAllStandardOutput()).decode(self.encoding)
        #print("out", text)
        self.log.logMessage(text, self.LOG_TAB, Qgis.Info)

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

    def get_layer_geojson(self, db, layer_name, plot_id):
        if layer_name == 'terreno':
            return db.get_annex17_plot_data(plot_id, 'only_id')
        elif layer_name == 'terrenos':
            return db.get_annex17_plot_data(plot_id, 'all_but_id')
        elif layer_name == 'terrenos_all':
            return db.get_annex17_plot_data(plot_id, 'all')
        elif layer_name == 'construcciones':
            return db.get_annex17_building_data()
        else:
            return db.get_annex17_point_data(plot_id)

    def update_json_data(self, db, json_spec_file, plot_id, tmp_dir):
        json_data = dict()
        with open(json_spec_file) as f:
            json_data = json.load(f)

        json_data['attributes']['id'] = plot_id
        json_data['attributes']['datasetName'] = db.schema
        layers = json_data['attributes']['map']['layers']
        for layer in layers:
            layer['geoJson'] = self.get_layer_geojson(db, layer['name'], plot_id)

        overview_layers = json_data['attributes']['overviewMap']['layers']
        for layer in overview_layers:
            layer['geoJson'] = self.get_layer_geojson(db, layer['name'], plot_id)

        new_json_file_path = os.path.join(tmp_dir, self.get_tmp_filename('json_data_{}'.format(plot_id), 'json'))
        with open(new_json_file_path, 'w') as new_json:
            new_json.write(json.dumps(json_data))

        return new_json_file_path

    def get_tmp_dir(self, create_random=True):
        if create_random:
            return tempfile.mkdtemp()

        return tempfile.gettempdir()

    def get_tmp_filename(self, basename, extension='gpkg'):
        return "{}_{}.{}".format(basename, str(time.time()).replace(".",""), extension)

    def get_java_path_from_qgis_model_baker(self):
        path = QSettings().value('QgisModelBaker/ili2db/JavaPath')
        java_path = os.path.dirname(os.path.dirname(path or ''))
        return java_path

    def generate_report(self, db, button):
        # Check if mapfish and Jasper are installed, otherwise show where to
        # download them from and return
        base_path = os.path.join(os.path.expanduser('~'), 'Asistente-LADM_COL', 'impresion')
        bin_path = os.path.join(base_path, 'bin')
        if not os.path.exists(bin_path):
            self.qgis_utils.message_with_button_download_report_dependency_emitted.emit(
                QCoreApplication.translate("ReportGenerator",
                   "The dependency library to generate reports is not installed. Click on the button to download and install it."))
            return

        # Check version
        required_version_found = True
        version_path = os.path.join(base_path, 'version')
        if not os.path.exists(version_path):
            required_version_found = False
        else:
            version_found = ''
            with open(version_path) as f:
                version_found = f.read()
            if version_found != REPORTS_REQUIRED_VERSION:
                required_version_found = False

        if not required_version_found:
            self.qgis_utils.message_with_button_remove_report_dependency_emitted.emit(
                QCoreApplication.translate("ReportGenerator",
                    "The dependency library to generate reports was found, but does not match with the version required. Click the button to remove the installed version and try again."))
            return

        # Check if JAVA_HOME path is set, otherwise use path from QGIS Model Baker
        if os.name == 'nt':
            if 'JAVA_HOME' not in os.environ:
                java_path = self.get_java_path_from_qgis_model_baker()
                if not java_path:
                    self.qgis_utils.message_emitted.emit(
                        QCoreApplication.translate("ReportGenerator",
                                                   "Please set JAVA_HOME path in QGIS Model Baker Settings or in Environmental Variables for your OS"),
                        Qgis.Warning)
                    return
                else:
                    os.environ["JAVA_HOME"] = java_path
                    self.log.logMessage("The JAVA_HOME path has been set using QGIS Model Baker Settings for reports.", PLUGIN_NAME, Qgis.Info)

        plot_layer = self.qgis_utils.get_layer(db, PLOT_TABLE, QgsWkbTypes.PolygonGeometry, load=True)
        if plot_layer is None:
            self.qgis_utils.message_emitted.emit(
                QCoreApplication.translate("ReportGenerator",
                                           "Layer 'Plot' not found in DB! {}").format(db.get_description()),
                Qgis.Warning)
            return

        selected_plots = plot_layer.selectedFeatures()
        if not selected_plots:
            self.qgis_utils.message_emitted.emit(
                QCoreApplication.translate("ReportGenerator",
                                           "To generate reports, first select at least a plot!"),
                Qgis.Warning)
            return

        # Where to store the reports?
        previous_folder = QSettings().value("Asistente-LADM_COL/reports/save_into_dir", ".")
        save_into_folder = QFileDialog.getExistingDirectory(
                        None,
                        QCoreApplication.translate("ReportGenerator", "Select a folder to save the reports to be generated"),
                        previous_folder)
        if not save_into_folder:
            self.qgis_utils.message_emitted.emit(
                QCoreApplication.translate("ReportGenerator",
                    "You need to select a folder where to save the reports before continuing."),
                Qgis.Warning)
            return
        QSettings().setValue("Asistente-LADM_COL/reports/save_into_dir", save_into_folder)

        config_path = os.path.join(base_path, 'ANT')
        json_spec_file = os.path.join(config_path, 'spec_json_file.json')

        script_name = ''
        if os.name == 'posix':
            script_name = 'print'
        elif os.name == 'nt':
            script_name = 'print.bat'

        script_path = os.path.join(bin_path, script_name)
        if not os.path.isfile(script_path):
            print("### SCRIPT FILE WASN'T FOUND")
            return

        button.setEnabled(False)

        # Update config file
        yaml_config_path = self.update_yaml_config(db, config_path)
        print("CONFIG FILE:", yaml_config_path)

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
        self.qgis_utils.create_progress_message_bar_emitted.emit(
            QCoreApplication.translate("ReportGenerator", "Generating {} report{}...").format(total, '' if total == 1 else 's'),
            progress)

        for selected_plot in selected_plots:
            plot_id = selected_plot[ID_FIELD]

            # Generate data file
            json_file = self.update_json_data(db, json_spec_file, plot_id, tmp_dir)
            print("JSON FILE:", json_file)

            # Run sh/bat passing config and data files
            proc = QProcess()
            proc.readyReadStandardError.connect(
                functools.partial(self.stderr_ready, proc=proc))
            proc.readyReadStandardOutput.connect(
                functools.partial(self.stdout_ready, proc=proc))

            current_report_path = os.path.join(save_into_folder, 'anexo_17_{}.pdf'.format(plot_id))
            proc.start(script_path, ['-config', yaml_config_path, '-spec', json_file, '-output', current_report_path])

            if not proc.waitForStarted():
                # Grant execution permissions
                os.chmod(script_path, stat.S_IXOTH | stat.S_IXGRP | stat.S_IXUSR | stat.S_IRUSR | stat.S_IRGRP)
                proc.start(script_path, ['-config', yaml_config_path, '-spec', json_file, '-output', current_report_path])

            if not proc.waitForStarted():
                proc = None
                print("### COULDN'T EXECUTE SCRIPT TO GENERATE REPORT...")
            else:
                loop = QEventLoop()
                proc.finished.connect(loop.exit)
                loop.exec()

                print(plot_id, ':', proc.exitCode())
                if proc.exitCode() == 0:
                    count += 1

                step += 1
                progress.setValue(step * 100 / total)

        os.remove(yaml_config_path)
        button.setEnabled(True)
        self.qgis_utils.clear_message_bar_emitted.emit()

        if total == count:
            if total == 1:
                msg = QCoreApplication.translate("ReportGenerator", "The report <a href='file:///{}'>anexo_17_{}.pdf</a> was successfully generated!").format(normalize_local_url(save_into_folder), plot_id)
            else:
                msg = QCoreApplication.translate("ReportGenerator", "All reports were successfully generated in folder <a href='file:///{path}'>{path}</a>!").format(path=normalize_local_url(save_into_folder))

            self.qgis_utils.message_with_duration_emitted.emit(msg, Qgis.Success, 0)
        else:
            if total == 1:
                msg = QCoreApplication.translate("ReportGenerator", "The report for plot {} couldn't be generated! See QGIS log (tab 'Anexo_17') for details.").format(plot_id)
            else:
                if count == 0:
                    msg = QCoreApplication.translate("ReportGenerator", "No report could be generated! See QGIS log (tab 'Anexo_17') for details.")
                else:
                    msg = QCoreApplication.translate("ReportGenerator", "At least one report couldn't be generated! See QGIS log (tab 'Anexo_17') for details. Go to <a href='file:///{path}'>{path}</a> to see the reports that were generated.").format(path=normalize_local_url(save_into_folder))

            self.qgis_utils.message_with_duration_emitted.emit(msg, Qgis.Warning, 0)


    def save_dependency_file(self, fetcher_task):
        if fetcher_task.reply() is not None:
            # Write response to tmp file
            tmp_file = tempfile.mktemp()
            out_file = QFile(tmp_file)
            out_file.open(QIODevice.WriteOnly)
            out_file.write(fetcher_task.reply().readAll())
            out_file.close()

            dependency_base_path = os.path.join(os.path.expanduser('~'), 'Asistente-LADM_COL')
            if not os.path.exists(dependency_base_path):
                os.makedirs(dependency_base_path)

            try:
                with zipfile.ZipFile(tmp_file, "r") as zip_ref:
                    zip_ref.extractall(dependency_base_path)
            except zipfile.BadZipFile as e:
                self.qgis_utils.message_with_duration_emitted.emit(
                    QCoreApplication.translate("ReportGenerator", "There was an error with the download. The downloaded file is invalid."),
                    Qgis.Warning,
                    0)
            except PermissionError as e:
                self.qgis_utils.message_with_duration_emitted.emit(
                    QCoreApplication.translate("ReportGenerator", "Dependencies to generate reports couldn't be installed. Check if it is possible to write into this folder: <a href='file:///{path}'>{path}</a>").format(path=normalize_local_url(os.path.join(dependency_base_path), 'impresion')),
                    Qgis.Warning,
                    0)
            else:
                self.qgis_utils.message_with_duration_emitted.emit(
                    QCoreApplication.translate("ReportGenerator", "The dependency to generate reports is properly installed! Select plots and click again the button in the toolbar to generate reports."),
                    Qgis.Info,
                    0)

            try:
                os.remove(tmp_file)
            except:
                pass

        self._downloading = False

    def download_report_dependency(self):
        self.qgis_utils.clear_message_bar_emitted.emit()
        if not self._downloading: # Already downloading report dependency?
            if self.qgis_utils.is_connected(TEST_SERVER):
                self._downloading = True
                fetcher_task = QgsNetworkContentFetcherTask(QUrl(URL_REPORTS_LIBRARIES))
                fetcher_task.fetched.connect(functools.partial(self.save_dependency_file, fetcher_task))
                QgsApplication.taskManager().addTask(fetcher_task)
            else:
                self.qgis_utils.message_emitted.emit(
                    QCoreApplication.translate("ReportGenerator", "There was a problem connecting to Internet."),
                    Qgis.Warning)
                self._downloading = False

    def remove_report_dependency(self):
        """
        We need to get rid of dependencies when they don't match the version
        that should be installed for this version of the plugin.
        """
        base_path = os.path.join(os.path.expanduser('~'), 'Asistente-LADM_COL', 'impresion')

        # Since folders might contain read only files, we need to delete them
        # using a callback (see https://docs.python.org/3/library/shutil.html#rmtree-example)
        shutil.rmtree(base_path, onerror=remove_readonly)
        self.qgis_utils.clear_message_bar_emitted.emit()

        if os.path.exists(base_path):
            self.qgis_utils.message_with_duration_emitted.emit(
                QCoreApplication.translate("ReportGenerator", "It wasn't possible to remove the dependency folder. You need to remove this folder yourself to generate reports: <a href='file:///{path}'>{path}</a>").format(path=normalize_local_url(base_path)),
                Qgis.Warning,
                0)
