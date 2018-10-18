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
import os
import locale
import functools
import shutil
import zipfile
import json
import stat
import tempfile
import time

from qgis.core import (QgsGeometry, QgsLineString, QgsDefaultValue, QgsProject,
                       QgsWkbTypes, QgsVectorLayerUtils, QgsDataSourceUri, Qgis,
                       QgsSpatialIndex, QgsVectorLayer, QgsMultiLineString,
                       QgsField,
                       QgsMapLayer,
                       QgsPointXY, QgsNetworkContentFetcherTask,
                       QgsMultiPoint, QgsMultiLineString, QgsGeometryCollection,
                       QgsApplication, QgsProcessingFeedback, QgsRelation,
                       QgsExpressionContextUtils, QgsEditorWidgetSetup,
                       QgsLayerTreeGroup, QgsApplication)
from qgis.PyQt.QtCore import (
    Qt,
    QObject,
    pyqtSignal,
    QCoreApplication,
    QVariant,
    QSettings,
    QLocale,
    QUrl,
    QFile,
    QProcess,
    QEventLoop,
    QIODevice
)
from qgis.PyQt.QtWidgets import QDialog, QFileDialog

from ..utils.qt_utils import OverrideCursor
from ..utils.symbology import SymbologyUtils
from ..utils.geometry import GeometryUtils
from .dlg_topological_edition import LayersForTopologicalEdition

from ..config.general_config import TEST_SERVER
from ..config.table_mapping_config import (
    ID_FIELD,
    PLOT_TABLE
)

class ReportGenerator():
    def __init__(self, db, qgis_utils):
        self.db = db
        self.qgis_utils = qgis_utils
        self.encoding = locale.getlocale()[1]

    def validate_bin_exists(self, path):
        if os.path.exists(path):
            return True
        else:
            print("Prerequisite wasn't found")
            return False

    def stderr_ready(self, proc):
        text = bytes(proc.readAllStandardError()).decode(self.encoding)
    #    if not self.__done_pattern:
    #        if self.dataImport:
    #            self.__done_pattern = re.compile(r"Info: \.\.\.import done")
    #        else:
    #            self.__done_pattern = re.compile(r"Info: \.\.\.done")
    #    if self.__done_pattern.search(text):
    #        self.__result = Importer.SUCCESS
        print("err", text)

    def stdout_ready(self, proc):
        text = bytes(proc.readAllStandardOutput()).decode(self.encoding)
        print("out", text)

    def update_yaml_config(self, config_path):
        text = ''
        qgs_uri = QgsDataSourceUri(self.db.uri)

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

    def get_layer_geojson(self, layer_name, plot_id):
        if layer_name == 'terreno':
            return self.db.get_annex17_plot_data(plot_id)
        else:
            return self.db.get_annex17_point_data(plot_id)

    def update_json_data(self, json_spec_file, plot_id, tmp_dir):
        json_data = dict()
        with open(json_spec_file) as f:
            json_data = json.load(f)

        json_data['attributes']['id'] = plot_id
        json_data['attributes']['datasetName'] = self.db.schema
        layers = json_data['attributes']['map']['layers']
        for layer in layers:
            layer['geoJson'] = self.get_layer_geojson(layer['name'], plot_id)

        #print(json_data)

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

    def generate_report(self, button):
        # Check if JAVA is installed, otherwise stop

        # Check if mapfish and Jasper are installed, otherwise show where to
        # download them from and return
        base_path = os.path.join(os.path.expanduser('~'), 'Asistente-LADM_COL', 'impresion')
        bin_path = os.path.join(base_path, 'bin')
        if not self.validate_bin_exists(bin_path):
            self.qgis_utils.message_with_button_download_report_dependency_emitted.emit(
                QCoreApplication.translate("ReportGenerator",
                   "The dependency library to generate reports is not installed. Click on the button to download and install it."))
            return

        plot_layer = self.qgis_utils.get_layer(self.db, PLOT_TABLE, QgsWkbTypes.PolygonGeometry, load=True)
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
        yaml_config_path = self.update_yaml_config(config_path)
        print("CONFIG FILE:", yaml_config_path)

        for selected_plot in selected_plots:
            plot_id = selected_plot[ID_FIELD]

            tmp_dir = self.get_tmp_dir()

            # Generate data file
            json_file = self.update_json_data(json_spec_file, plot_id, tmp_dir)
            print("JSON FILE:", json_file)

            # Run sh/bat passing config and data files
            proc = QProcess()
            proc.readyReadStandardError.connect(
                functools.partial(self.stderr_ready, proc=proc))
            proc.readyReadStandardOutput.connect(
                functools.partial(self.stdout_ready, proc=proc))

            proc.start(script_path, ['-config', yaml_config_path, '-spec', json_file, '-output', os.path.join(save_into_folder, 'annex_17_{}.pdf'.format(plot_id))])

            if not proc.waitForStarted():
                # Grant execution permissions
                os.chmod(script_path, stat.S_IXOTH | stat.S_IXGRP | stat.S_IXUSR | stat.S_IRUSR | stat.S_IRGRP)
                proc.start(script_path, ['-config', yaml_config_path, '-spec', json_file, '-output', os.path.join(save_into_folder, 'annex_17_{}.pdf'.format(plot_id))])

            if not proc.waitForStarted():
                proc = None
                print("### COULDN'T EXECUTE SCRIPT TO GENERATE REPORT...")
            else:
                loop = QEventLoop()
                proc.finished.connect(loop.exit)
                loop.exec()

                print(plot_id, ':', proc.exitCode())

        os.remove(yaml_config_path)
        button.setEnabled(True)

    def save_dependency_file(self, fetcher_task):
        if fetcher_task.reply() is not None:
            tmp_file = tempfile.mktemp()
            out_file = QFile(tmp_file)
            out_file.open(QIODevice.WriteOnly)
            out_file.write(fetcher_task.reply().readAll())
            out_file.close()

            dependency_base_path = os.path.join(os.path.expanduser('~'), 'Asistente-LADM_COL')
            if not os.path.exists(dependency_base_path):
                os.makedirs(dependency_base_path)

            print(dependency_base_path)

            try:
                with zipfile.ZipFile(tmp_file, "r") as zip_ref:
                    zip_ref.extractall(dependency_base_path)

            except zipfile.BadZipFile as e:
                self.qgis_utils.message_emitted.emit(
                    QCoreApplication.translate("ReportGenerator", "There was an error with the download. The downloaded file is invalid."),
                    Qgis.Warning)
            else:
                self.qgis_utils.message_emitted.emit(
                    QCoreApplication.translate("ReportGenerator", "The dependency to generate reports is properly installed! Select plots and click again in the button to generate reports in the toolbar."),
                    Qgis.Info)

            try:
                os.remove(tmp_file)
            except:
                pass

    def download_report_dependency(self):
        if self.qgis_utils.is_connected(TEST_SERVER):
            #self.btn_download_help.setEnabled(False)
            #url = 'http://downloads.tuxfamily.org/tuxgis/tmp/impresion.zip'
            #url = 'http://downloads.tuxfamily.org/tuxgis/tmp/borrar/impresion.zip'
            url = 'https://owncloud.proadmintierra.info/owncloud/index.php/s/mrUcc2ugGJoB8pk/download'
            fetcher_task = QgsNetworkContentFetcherTask(QUrl(url))
            # fetcher_task.taskCompleted.connect(self.enable_download_button)
            fetcher_task.fetched.connect(functools.partial(self.save_dependency_file, fetcher_task))
            QgsApplication.taskManager().addTask(fetcher_task)
        else:
            self.qgis_utils.message_emitted.emit(
                QCoreApplication.translate("AboutDialog", "There was a problem connecting to Internet."),
                Qgis.Warning)
