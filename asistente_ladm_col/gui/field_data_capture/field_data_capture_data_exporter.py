# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM-COL
                             --------------------
        begin                : 2020-09-02
        git sha              : :%H$
        copyright            : (C) 2020 by Germán Carrillo (SwissTierras Colombia)
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
import os.path
import shutil

from QgisModelBaker.libili2db.globals import DbIliMode
from qgis.PyQt.QtCore import (QCoreApplication,
                              pyqtSignal,
                              QObject,
                              QSettings,
                              Qt)
from qgis.core import (QgsMessageLog,
                       Qgis,
                       QgsVectorLayer)
import processing

from QgisModelBaker.libili2db.ili2dbutils import JavaNotFoundError
from QgisModelBaker.libili2db import iliexporter, iliimporter
from QgisModelBaker.libili2db.ili2dbconfig import (BaseConfiguration,
                                                   ExportConfiguration,
                                                   SchemaImportConfiguration,
                                                   ImportDataConfiguration)
from QgisModelBaker.libili2db.ilicache import IliCache

from asistente_ladm_col.config.config_db_supported import ConfigDBsSupported
from asistente_ladm_col.config.general_config import (JAVA_REQUIRED_VERSION,
                                                      DEFAULT_USE_CUSTOM_MODELS,
                                                      DEFAULT_MODELS_DIR,
                                                      CTM12_GPKG_SCRIPT_PATH)
from asistente_ladm_col.config.ili2db_names import ILI2DBNames
from asistente_ladm_col.lib.dependency.java_dependency import JavaDependency
from asistente_ladm_col.lib.ladm_col_models import LADMColModelRegistry
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.utils.qt_utils import (OverrideCursor,
                                               ProcessWithStatus)


class FieldDataCaptureDataExporter(QObject):
    total_progress_updated = pyqtSignal(int)  # percentage

    def __init__(self, db, basket_dict, export_dir, with_offline_project=False, template_project_path='', raster_layer=None):
        QObject.__init__(self)
        self._db = db
        self._basket_dict = basket_dict  # {t_ili_tids: receiver_name}
        self._export_dir = export_dir

        self._total_steps = len(self._basket_dict)

        # Parameters for the "with offline project" mode
        self._with_offline_project = with_offline_project
        self._template_project_path = template_project_path
        self._raster_layer = raster_layer

        self.logger = Logger()

        self.log = ''
        self.java_dependency = JavaDependency()
        self.java_dependency.download_dependency_completed.connect(self.download_java_complete)

        self._dbs_supported = ConfigDBsSupported()

    def export_baskets(self):
        if self._with_offline_project and not self._template_project_path:
            return {None: (False, QCoreApplication.translate("FieldDataCaptureDataExporter", "No template project was passed, but it is required for generating offline projects!"))}

        self.total_progress_updated.emit(1)  # Let users know we started already

        java_home_set = self.java_dependency.set_java_home()
        if not java_home_set:
            message_java = QCoreApplication.translate("FieldDataCaptureDataExporter", """Configuring Java {}...""").format(
                JAVA_REQUIRED_VERSION)
            self.logger.status(message_java)
            self.java_dependency.get_java_on_demand()
            return

        self.base_configuration = BaseConfiguration()
        self.ilicache = IliCache(self.base_configuration)
        self.ilicache.refresh()

        db_factory = self._dbs_supported.get_db_factory(self._db.engine)
        configuration = ExportConfiguration()
        db_factory.set_ili2db_configuration_params(self._db.dict_conn_params, configuration)
        configuration.with_exporttid = True
        full_java_exe_path = JavaDependency.get_full_java_exe_path()
        if full_java_exe_path:
            self.base_configuration.java_path = full_java_exe_path

        # Check custom model directories
        if QSettings().value('Asistente-LADM-COL/models/custom_model_directories_is_checked', DEFAULT_USE_CUSTOM_MODELS, type=bool):
            custom_model_directories = QSettings().value('Asistente-LADM-COL/models/custom_models', DEFAULT_MODELS_DIR)
            if not custom_model_directories:
                self.base_configuration.custom_model_directories_enabled = False
            else:
                self.base_configuration.custom_model_directories = custom_model_directories
                self.base_configuration.custom_model_directories_enabled = True

        configuration.base_configuration = self.base_configuration
        ili_models = self.get_ili_models()
        if ili_models:
            configuration.ilimodels = ';'.join(ili_models)

        self.exporter = iliexporter.Exporter()
        self.exporter.tool = db_factory.get_model_baker_db_ili_mode()
        self.exporter.process_started.connect(self.on_process_started)
        self.exporter.stderr.connect(self.on_stderr)
        #self.exporter.process_finished.connect(self.on_process_finished)

        res = dict()
        count = 0
        current_progress = 0  # Range 0-100

        with OverrideCursor(Qt.WaitCursor):
            for basket,name in self._basket_dict.items():
                self.log = ''
                configuration.xtffile = os.path.join(self._export_dir, "{}.xtf".format(name))
                configuration.baskets = basket
                self.exporter.configuration = configuration

                try:
                    self.logger.info(__name__, "Exporting data from the capture model to XTF... ({})".format(name))
                    if self.exporter.run() != iliexporter.Exporter.SUCCESS:
                        msg = QCoreApplication.translate("FieldDataCaptureDataExporter", "An error occurred when exporting the data for '{}' (check the QGIS log panel).").format(name)
                        res[basket] = (False, msg)
                        QgsMessageLog.logMessage(self.log, QCoreApplication.translate("FieldDataCaptureDataExporter", "Allocate to coordinators"), Qgis.Critical)
                    else:
                        if self._with_offline_project:
                            self.logger.info(__name__, "Generating offline project for field data capture... ({})".format(name))
                            res[basket] = self.generate_qgis_offline_project(configuration.xtffile, current_progress)
                        else:
                            res[basket] = (True, QCoreApplication.translate("FieldDataCaptureDataExporter", "XTF export for '{}' successful!").format(name))
                except JavaNotFoundError:
                    msg = QCoreApplication.translate("FieldDataCaptureDataExporter", "Java {} could not be found. You can configure the JAVA_HOME environment variable manually, restart QGIS and try again.").format(JAVA_REQUIRED_VERSION)
                    res[basket] = (False, msg)

                count += 1
                current_progress = int(count / self._total_steps * 100)
                self.total_progress_updated.emit(current_progress)

        return res

    def generate_qgis_offline_project(self, xtf_path, current_progress):
        """
        Generates offline projects based on the exported XTF. The QGS project is given by the user and points to a GPKG
        database (built from the exported XTF). Optionally, we might clip a given raster file with the Plot layer
        extent.

        :param xtf_path: Path of the XTF containing data for the offline project
        :param current_progress: Current global progress, used to update the emit a signal with the progress status
        :return: Tuple (whether the project generation was successful, message to describe errors if any)
        """
        step_range = 100 / self._total_steps
        weights = [2, 3, 5, 7, 9] if self._raster_layer else [3, 4, 6, 9]
        def update_progress(step):
            self.total_progress_updated.emit(int(current_progress + weights[step-1] / 10 * step_range))

        base_dir, file_name = os.path.split(xtf_path)
        user_alias, _ = os.path.splitext(file_name)
        offline_dir = os.path.join(base_dir, user_alias)

        # As soon as we start, we've already done the XTF export, so update the progress
        update_progress(1)

        # Create folder
        if os.path.exists(offline_dir):
            try:
                shutil.rmtree(offline_dir)
            except:
                pass
        try:
            os.makedirs(offline_dir)
        except FileExistsError as e:
            pass
        update_progress(2)

        # Run schema import
        gpkg_path = os.path.join(offline_dir, 'data.gpkg')
        res_schema_import = self._run_gpkg_schema_import(gpkg_path, user_alias)
        if not res_schema_import:
            return res_schema_import
        update_progress(3)

        # Run import data
        res_import_data = self._run_gpkg_import_data(gpkg_path, xtf_path, user_alias)
        if not res_import_data:
            return res_import_data
        update_progress(4)

        # Clip raster if any
        if self._raster_layer:
            self.logger.info(__name__, "Clipping raster for the offline project... ({})".format(user_alias))
            # Get extent of the Plot layer
            plot_layer = QgsVectorLayer('{}|layername=terreno'.format(gpkg_path), 'plots', 'ogr')
            if plot_layer.isValid():
                # Extent in this form: 'Xmin,Xmax,Ymin,Ymax [EPSG:9377]'
                # See https://github.com/qgis/QGIS/blob/ccc34c76e714e5f6f87d2a329ca048896eb4c87f/src/gui/qgsextentwidget.cpp#L211
                #extent = plot_layer.extent()
                extent = '4843772.266000000,4844770.188000000,2143021.638000000,2144006.634000000 [EPSG:9377]'

                # Clip raster and put the output in the offline folder
                clipped_raster = os.path.join(offline_dir, 'raster.tif')
                try:
                    processing.run("gdal:cliprasterbyextent", {'INPUT': self._raster_layer,
                                                               'PROJWIN': extent,
                                                               'NODATA': None, 'OPTIONS': 'COMPRESS=JPEG|JPEG_QUALITY=75',
                                                               'DATA_TYPE': 0, 'EXTRA': '', 'OUTPUT': clipped_raster})
                except:
                    pass
            update_progress(5)

        # Copy template project
        project_path = os.path.join(offline_dir, '_qfield.qgs')
        shutil.copyfile(self._template_project_path, project_path)

        return True, QCoreApplication.translate("FieldDataCaptureDataExporter", "Offline project for '{}' was created successfully!").format(user_alias)

    def _run_gpkg_schema_import(self, gpkg_path, user_alias):
        # We don't check any Java stuff because to get here we should have run already the export
        self.log = ''
        db_factory = self._dbs_supported.get_db_factory('gpkg')
        configuration = SchemaImportConfiguration()
        configuration.base_configuration = self.base_configuration

        db_factory.set_ili2db_configuration_params({'dbfile': gpkg_path}, configuration)
        configuration.inheritance = ILI2DBNames.DEFAULT_INHERITANCE
        configuration.create_basket_col = True
        configuration.create_import_tid = ILI2DBNames.CREATE_IMPORT_TID
        configuration.stroke_arcs = ILI2DBNames.STROKE_ARCS

        # EPSG:9377 support for GPKG (Ugly, I know) We need to send known parameters, we'll fix this in the post_script
        configuration.srs_auth = 'EPSG'
        configuration.srs_code = 3116
        configuration.post_script = CTM12_GPKG_SCRIPT_PATH

        ili_models = self.get_ili_models()
        if ili_models:
            configuration.ilimodels = ';'.join(ili_models)

        importer = iliimporter.Importer()
        importer.tool = DbIliMode.ili2gpkg
        importer.configuration = configuration
        importer.stderr.connect(self.on_stderr)
        importer.process_started.connect(self.on_process_started)

        msg_status = QCoreApplication.translate("FieldDataCaptureDataExporter",
                                                "Creating LADM-COL structure in GPKG ({})...").format(user_alias)
        with ProcessWithStatus(msg_status):
            if importer.run() != iliimporter.Importer.SUCCESS:
                msg = QCoreApplication.translate("FieldDataCaptureDataExporter",
                                                 "An error occurred when creating the LADM-COL structure for the offline project for '{}' (check the QGIS log panel).").format(user_alias)
                res = (False, msg)
                QgsMessageLog.logMessage(self.log, QCoreApplication.translate("FieldDataCaptureDataExporter",
                                                                              "Allocate to surveyors"),
                                         Qgis.Critical)
            else:
                res = (True, QCoreApplication.translate("FieldDataCaptureDataExporter",
                                                        "Schema import for '{}' successful!").format(user_alias))

        return res

    def _run_gpkg_import_data(self, gpkg_path, xtf_path, user_alias):
        # We don't check any Java stuff because to get here we should have run already the export
        self.log = ''
        db_factory = self._dbs_supported.get_db_factory('gpkg')
        configuration = ImportDataConfiguration()
        configuration.base_configuration = self.base_configuration

        db_factory.set_ili2db_configuration_params({'dbfile': gpkg_path}, configuration)
        configuration.xtffile = xtf_path
        configuration.with_importtid = True
        # configuration.disable_validation = False

        ili_models = self.get_ili_models()
        if ili_models:
            configuration.ilimodels = ';'.join(ili_models)

        importer = iliimporter.Importer(dataImport=True)
        importer.tool = DbIliMode.ili2gpkg
        importer.configuration = configuration
        importer.stderr.connect(self.on_stderr)
        importer.process_started.connect(self.on_process_started)

        msg_status = QCoreApplication.translate("FieldDataCaptureDataExporter",
                                                "Importing data from XTF to GPKG ({})...").format(user_alias)
        with ProcessWithStatus(msg_status):
            if importer.run() != iliimporter.Importer.SUCCESS:
                msg = QCoreApplication.translate("FieldDataCaptureDataExporter",
                                                 "An error occurred when importing the XTF for the offline project for '{}' (check the QGIS log panel).").format(user_alias)
                res = (False, msg)
                QgsMessageLog.logMessage(self.log, QCoreApplication.translate("FieldDataCaptureDataExporter",
                                                                              "Allocate to surveyors"),
                                         Qgis.Critical)
            else:
                res = (True, QCoreApplication.translate("FieldDataCaptureDataExporter",
                                                        "Import data for '{}' successful!").format(user_alias))

        return res

    def get_ili_models(self):
        ili_models = list()
        model_names = self._db.get_models()
        if model_names:
            for model in LADMColModelRegistry().supported_models():
                if not model.hidden() and model.full_name() in model_names:
                    ili_models.append(model.full_name())

        return ili_models

    def download_java_complete(self):
        self.export_baskets()

    #def on_process_finished(self):
    #    self.run_export()
    #if self._basket_dict:
    #    basket, = self._basket_dict.popitem()

    def on_process_started(self, command):
        self.log += command + '\n'

    def on_stderr(self, text):
        self.log += text
