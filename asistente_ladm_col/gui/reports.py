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
    BOUNDARY_POINT_TABLE,
    BOUNDARY_TABLE,
    BUILDING_TABLE,
    BUILDING_UNIT_TABLE,
    PLOT_TABLE
)

class ReportGenerator():
    def __init__(self, db, qgis_utils):
        self.db = db
        self.qgis_utils = qgis_utils
        self.encoding = locale.getlocale()[1]

    def validate_bin_exists(self):
        bin_path = os.path.join(os.path.expanduser('~'), 'Asistente-LADM_COL', 'impresion', 'bin')
        if os.path.exists(bin_path):
            return bin_path
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

    def update_yaml_config(self, tmp_dir):
        text = ''
        with open('/docs/tr/ai/insumos/anexo17/impresion/ANT/config_template.yaml') as f:
            text = f.read()
            text = text.format(
                '{}',
                DB_USER='postgres',
                DB_PASSWORD='postgres',
                DB_HOST='localhost',
                DB_PORT='5432',
                DB_NAME='yamile2'
            )
        new_file_path = os.path.join(tmp_dir, self.get_tmp_filename('yaml_config', 'yaml'))

        with open(new_file_path, 'w') as new_yaml:
            new_yaml.write(text)

        return new_file_path

    def get_layer_geojson(self, layer_name, plot_id):
        if layer_name == 'terreno':
            return self.db.get_annex17_plot_data(plot_id) #{"features":[{"geometry":{"coordinates":[[[[896009.773,1544958.7589],[896176.3346,1544929.0741],[896332.2438,1544904.0326],[896342.8988,1544852.5454],[896345.8979,1544819.5547],[896334.4601,1544784.7153],[896306.2701,1544741.6161],[896307.3808,1544706.7901],[896291.2881,1544677.0181],[896265.8678,1544642.5594],[896260.1954,1544602.9133],[896263.1985,1544568.678],[896274.4086,1544534.4727],[896276.6671,1544529.6294],[896281.1216,1544525.1749],[896303.291,1544473.5619],[896288.3309,1544449.8883],[896286.5521,1544443.2496],[896250.7935,1544402.2281],[896229.4007,1544391.8558],[896212.2175,1544369.0515],[896186.9177,1544352.7036],[896144.4519,1544372.9443],[896111.3606,1544370.3506],[895693.4076,1544396.9691],[895493.1465,1544414.4397],[895401.8673,1544422.4727],[895273.1213,1544434.3874],[895135.8618,1544445.1173],[895025.5441,1544455.3042],[895017.3152,1544494.6591],[895011.2729,1544524.2922],[895008.0272,1544544.1802],[894994.4227,1544583.0971],[894970.1119,1544673.8435],[894953.3767,1544733.0246],[894939.2194,1544779.806],[894935.217,1544794.0575],[894930.5649,1544808.6017],[894893.432,1544924.7552],[894838.7041,1545016.129],[894764.1405,1545102.8648],[894665.6362,1545254.687],[894588.1125,1545353.7931],[894569.8889,1545331.3272],[894520.3255,1545429.6126],[894571.5364,1545488.8855],[894740.2793,1545486.5186],[894798.4863,1545320.3348],[894820.2581,1545259.2353],[894838.1978,1545207.7409],[894848.1695,1545205.57],[894891.7693,1545200.4637],[894935.6368,1545194.383],[894997.8932,1545186.4757],[895051.3722,1545179.7173],[895062.7429,1545178.3633],[895135.3004,1545167.1903],[895174.1847,1544930.4252],[895197.9412,1544767.9276],[895494.1841,1544736.9234],[895679.2655,1544717.9681],[895883.0272,1544699.5062],[895814.6831,1544992.4188],[896009.773,1544958.7589]]]],"type":"MultiPolygon"},"type":"Feature","properties":{"t_id":11692}}],"type":"FeatureCollection"}
        else:
            return self.db.get_annex17_point_data(plot_id) #{"features":[{"geometry":{"coordinates":[894740.2793,1545486.5186],"type":"Point"},"type":"Feature","properties":{"point_number":1}},{"geometry":{"coordinates":[894798.4863,1545320.3348],"type":"Point"},"type":"Feature","properties":{"point_number":2}},{"geometry":{"coordinates":[894820.2581,1545259.2353],"type":"Point"},"type":"Feature","properties":{"point_number":3}},{"geometry":{"coordinates":[894838.1978,1545207.7409],"type":"Point"},"type":"Feature","properties":{"point_number":4}},{"geometry":{"coordinates":[894848.1695,1545205.57],"type":"Point"},"type":"Feature","properties":{"point_number":5}},{"geometry":{"coordinates":[894891.7693,1545200.4637],"type":"Point"},"type":"Feature","properties":{"point_number":6}},{"geometry":{"coordinates":[894935.6368,1545194.383],"type":"Point"},"type":"Feature","properties":{"point_number":7}},{"geometry":{"coordinates":[894997.8932,1545186.4757],"type":"Point"},"type":"Feature","properties":{"point_number":8}},{"geometry":{"coordinates":[895051.3722,1545179.7173],"type":"Point"},"type":"Feature","properties":{"point_number":9}},{"geometry":{"coordinates":[895062.7429,1545178.3633],"type":"Point"},"type":"Feature","properties":{"point_number":10}},{"geometry":{"coordinates":[895135.3004,1545167.1903],"type":"Point"},"type":"Feature","properties":{"point_number":11}},{"geometry":{"coordinates":[895174.1847,1544930.4252],"type":"Point"},"type":"Feature","properties":{"point_number":12}},{"geometry":{"coordinates":[895197.9412,1544767.9276],"type":"Point"},"type":"Feature","properties":{"point_number":13}},{"geometry":{"coordinates":[895494.1841,1544736.9234],"type":"Point"},"type":"Feature","properties":{"point_number":14}},{"geometry":{"coordinates":[895679.2655,1544717.9681],"type":"Point"},"type":"Feature","properties":{"point_number":15}},{"geometry":{"coordinates":[895883.0272,1544699.5062],"type":"Point"},"type":"Feature","properties":{"point_number":16}},{"geometry":{"coordinates":[895814.6831,1544992.4188],"type":"Point"},"type":"Feature","properties":{"point_number":17}},{"geometry":{"coordinates":[896009.773,1544958.7589],"type":"Point"},"type":"Feature","properties":{"point_number":18}},{"geometry":{"coordinates":[896176.3346,1544929.0741],"type":"Point"},"type":"Feature","properties":{"point_number":19}},{"geometry":{"coordinates":[896332.2438,1544904.0326],"type":"Point"},"type":"Feature","properties":{"point_number":20}},{"geometry":{"coordinates":[896342.8988,1544852.5454],"type":"Point"},"type":"Feature","properties":{"point_number":21}},{"geometry":{"coordinates":[896345.8979,1544819.5547],"type":"Point"},"type":"Feature","properties":{"point_number":22}},{"geometry":{"coordinates":[896334.4601,1544784.7153],"type":"Point"},"type":"Feature","properties":{"point_number":23}},{"geometry":{"coordinates":[896306.2701,1544741.6161],"type":"Point"},"type":"Feature","properties":{"point_number":24}},{"geometry":{"coordinates":[896307.3808,1544706.7901],"type":"Point"},"type":"Feature","properties":{"point_number":25}},{"geometry":{"coordinates":[896291.2881,1544677.0181],"type":"Point"},"type":"Feature","properties":{"point_number":26}},{"geometry":{"coordinates":[896265.8678,1544642.5594],"type":"Point"},"type":"Feature","properties":{"point_number":27}},{"geometry":{"coordinates":[896260.1954,1544602.9133],"type":"Point"},"type":"Feature","properties":{"point_number":28}},{"geometry":{"coordinates":[896263.1985,1544568.678],"type":"Point"},"type":"Feature","properties":{"point_number":29}},{"geometry":{"coordinates":[896274.4086,1544534.4727],"type":"Point"},"type":"Feature","properties":{"point_number":30}},{"geometry":{"coordinates":[896276.6671,1544529.6294],"type":"Point"},"type":"Feature","properties":{"point_number":31}},{"geometry":{"coordinates":[896281.1216,1544525.1749],"type":"Point"},"type":"Feature","properties":{"point_number":32}},{"geometry":{"coordinates":[896303.291,1544473.5619],"type":"Point"},"type":"Feature","properties":{"point_number":33}},{"geometry":{"coordinates":[896288.3309,1544449.8883],"type":"Point"},"type":"Feature","properties":{"point_number":34}},{"geometry":{"coordinates":[896286.5521,1544443.2496],"type":"Point"},"type":"Feature","properties":{"point_number":35}},{"geometry":{"coordinates":[896250.7935,1544402.2281],"type":"Point"},"type":"Feature","properties":{"point_number":36}},{"geometry":{"coordinates":[896229.4007,1544391.8558],"type":"Point"},"type":"Feature","properties":{"point_number":37}},{"geometry":{"coordinates":[896212.2175,1544369.0515],"type":"Point"},"type":"Feature","properties":{"point_number":38}},{"geometry":{"coordinates":[896186.9177,1544352.7036],"type":"Point"},"type":"Feature","properties":{"point_number":39}},{"geometry":{"coordinates":[896144.4519,1544372.9443],"type":"Point"},"type":"Feature","properties":{"point_number":40}},{"geometry":{"coordinates":[896111.3606,1544370.3506],"type":"Point"},"type":"Feature","properties":{"point_number":41}},{"geometry":{"coordinates":[895693.4076,1544396.9691],"type":"Point"},"type":"Feature","properties":{"point_number":42}},{"geometry":{"coordinates":[895493.1465,1544414.4397],"type":"Point"},"type":"Feature","properties":{"point_number":43}},{"geometry":{"coordinates":[895401.8673,1544422.4727],"type":"Point"},"type":"Feature","properties":{"point_number":44}},{"geometry":{"coordinates":[895273.1213,1544434.3874],"type":"Point"},"type":"Feature","properties":{"point_number":45}},{"geometry":{"coordinates":[895135.8618,1544445.1173],"type":"Point"},"type":"Feature","properties":{"point_number":46}},{"geometry":{"coordinates":[895025.5441,1544455.3042],"type":"Point"},"type":"Feature","properties":{"point_number":47}},{"geometry":{"coordinates":[895017.3152,1544494.6591],"type":"Point"},"type":"Feature","properties":{"point_number":48}},{"geometry":{"coordinates":[895011.2729,1544524.2922],"type":"Point"},"type":"Feature","properties":{"point_number":49}},{"geometry":{"coordinates":[895008.0272,1544544.1802],"type":"Point"},"type":"Feature","properties":{"point_number":50}},{"geometry":{"coordinates":[894994.4227,1544583.0971],"type":"Point"},"type":"Feature","properties":{"point_number":51}},{"geometry":{"coordinates":[894970.1119,1544673.8435],"type":"Point"},"type":"Feature","properties":{"point_number":52}},{"geometry":{"coordinates":[894953.3767,1544733.0246],"type":"Point"},"type":"Feature","properties":{"point_number":53}},{"geometry":{"coordinates":[894939.2194,1544779.806],"type":"Point"},"type":"Feature","properties":{"point_number":54}},{"geometry":{"coordinates":[894935.217,1544794.0575],"type":"Point"},"type":"Feature","properties":{"point_number":55}},{"geometry":{"coordinates":[894930.5649,1544808.6017],"type":"Point"},"type":"Feature","properties":{"point_number":56}},{"geometry":{"coordinates":[894893.432,1544924.7552],"type":"Point"},"type":"Feature","properties":{"point_number":57}},{"geometry":{"coordinates":[894838.7041,1545016.129],"type":"Point"},"type":"Feature","properties":{"point_number":58}},{"geometry":{"coordinates":[894764.1405,1545102.8648],"type":"Point"},"type":"Feature","properties":{"point_number":59}},{"geometry":{"coordinates":[894665.6362,1545254.687],"type":"Point"},"type":"Feature","properties":{"point_number":60}},{"geometry":{"coordinates":[894588.1125,1545353.7931],"type":"Point"},"type":"Feature","properties":{"point_number":61}},{"geometry":{"coordinates":[894569.8889,1545331.3272],"type":"Point"},"type":"Feature","properties":{"point_number":62}},{"geometry":{"coordinates":[894520.3255,1545429.6126],"type":"Point"},"type":"Feature","properties":{"point_number":63}},{"geometry":{"coordinates":[894571.5364,1545488.8855],"type":"Point"},"type":"Feature","properties":{"point_number":64}}],"type":"FeatureCollection"}

    def update_json_data(self, json_spec_file, plot_id, tmp_dir, schema):
        json_data = dict()
        with open(json_spec_file) as f:
            json_data = json.load(f)

        json_data['attributes']['id'] = plot_id
        json_data['attributes']['datasetName'] = schema # TODO get from DB
        layers = json_data['attributes']['map']['layers']
        for layer in layers:
            layer['geoJson'] = self.get_layer_geojson(layer['name'], plot_id)

        print(json_data)

        new_json_file_path = os.path.join(tmp_dir, self.get_tmp_filename('json_data', 'json'))
        with open(new_json_file_path, 'w') as new_json:
            new_json.write(json.dumps(json_data))

        return new_json_file_path

    def get_tmp_dir(self, create_random=True):
        return "/docs/tr/ai/insumos/anexo17/impresion/ANT/"
        #if create_random:
        #    return tempfile.mkdtemp()

        #return tempfile.gettempdir()

    def get_tmp_filename(self, basename, extension='gpkg'):
        return "{}_{}.{}".format(basename, str(time.time()).replace(".",""), extension)

    def generate_report(self):
        # Check if JAVA is installed, otherwise stop

        # Check if mapfish and Jasper are installed, otherwise show where to
        # download them from and return

        # Run sh/bat passing config and data files

        save_into_folder = '/tmp/output/' # Ask the user
        plot_id = 11692 # Should change inside a for loop
        json_spec_file = '/docs/borrar/spec_json_file.json'
        schema = 'ovejas_ladmcol5'

        bin_path = self.validate_bin_exists()
        if not bin_path:
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
            else:
                tmp_dir = self.get_tmp_dir()

                # Generate data file
                json_file = self.update_json_data(json_spec_file, plot_id, tmp_dir, schema)
                print("JSON FILE:", json_file)

                proc = QProcess()
                proc.readyReadStandardError.connect(
                    functools.partial(self.stderr_ready, proc=proc))
                proc.readyReadStandardOutput.connect(
                    functools.partial(self.stdout_ready, proc=proc))

                # Update config file
                yaml_config_path = self.update_yaml_config(tmp_dir)
                print("CONFIG FILE:", yaml_config_path)
                proc.start(script_path, ['-config', yaml_config_path, '-spec', json_file, '-output', os.path.join(save_into_folder, 'annex_17_{}.pdf'.format(plot_id))])

                if not proc.waitForStarted():
                    proc = None

                loop = QEventLoop()
                proc.finished.connect(loop.exit)
                loop.exec()

                print(proc.exitCode())

                #os.remove(yaml_config_path)
