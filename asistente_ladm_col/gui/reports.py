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
import json
import tempfile
import time

from qgis.core import (QgsGeometry, QgsLineString, QgsDefaultValue, QgsProject,
                       QgsWkbTypes, QgsVectorLayerUtils, QgsDataSourceUri, Qgis,
                       QgsSpatialIndex, QgsVectorLayer, QgsMultiLineString,
                       QgsField,
                       QgsMapLayer,
                       QgsPointXY,
                       QgsMultiPoint, QgsMultiLineString, QgsGeometryCollection,
                       QgsApplication, QgsProcessingFeedback, QgsRelation,
                       QgsExpressionContextUtils, QgsEditorWidgetSetup,
                       QgsLayerTreeGroup)
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
    QEventLoop
)
from qgis.PyQt.QtWidgets import QDialog

from ..utils.qt_utils import OverrideCursor
from ..utils.symbology import SymbologyUtils
from ..utils.geometry import GeometryUtils
from .dlg_topological_edition import LayersForTopologicalEdition

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

    def generate_report(self):
        # Check if JAVA is installed, otherwise stop

        # Check if mapfish and Jasper are installed, otherwise show where to
        # download them from and return

        # Run sh/bat passing config and data files

        save_into_folder = '/tmp/output/' # Ask the user

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

        base_path = os.path.join(os.path.expanduser('~'), 'Asistente-LADM_COL', 'impresion')
        bin_path = os.path.join(base_path, 'bin')
        config_path = os.path.join(base_path, 'ANT')
        json_spec_file = os.path.join(config_path, 'spec_json_file.json')

        if not self.validate_bin_exists(bin_path):
            # RETURN!
            print("### BIN PATH WASN'T FOUND")
        else:
            script_name = ''
            if os.name == 'posix':
                script_name = 'print'
            elif os.name == 'nt':
                script_name = 'print.bat'

            script_path = os.path.join(bin_path, script_name)
            if not os.path.isfile(script_path):
                # RETURN!
                print("### SCRIPT FILE WASN'T FOUND")

        # Update config file
        yaml_config_path = self.update_yaml_config(config_path)
        print("CONFIG FILE:", yaml_config_path)

        for selected_plot in selected_plots:
            plot_id = selected_plot[ID_FIELD]

            tmp_dir = self.get_tmp_dir()

            # Generate data file
            json_file = self.update_json_data(json_spec_file, plot_id, tmp_dir)
            print("JSON FILE:", json_file)

            proc = QProcess()
            proc.readyReadStandardError.connect(
                functools.partial(self.stderr_ready, proc=proc))
            proc.readyReadStandardOutput.connect(
                functools.partial(self.stdout_ready, proc=proc))

            proc.start(script_path, ['-config', yaml_config_path, '-spec', json_file, '-output', os.path.join(save_into_folder, 'annex_17_{}.pdf'.format(plot_id))])

            if not proc.waitForStarted():
                proc = None

            loop = QEventLoop()
            proc.finished.connect(loop.exit)
            loop.exec()

            print(plot_id, ':', proc.exitCode())

        #os.remove(yaml_config_path)
