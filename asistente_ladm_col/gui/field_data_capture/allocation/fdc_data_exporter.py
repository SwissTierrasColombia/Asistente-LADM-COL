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
from QgisModelBaker.libili2db import iliexporter

from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.config.general_config import (JAVA_REQUIRED_VERSION,
                                                      FDC_WILD_CARD_BASKET_ID)
from asistente_ladm_col.config.ladm_names import LADMNames
from asistente_ladm_col.lib.db.gpkg_connector import GPKGConnector
from asistente_ladm_col.lib.ladm_col_models import LADMColModelRegistry
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.lib.qgis_model_baker.ili2db import Ili2DB
from asistente_ladm_col.logic.ladm_col.ladm_data import LADMData
from asistente_ladm_col.utils.utils import get_extent_for_processing


class FieldDataCaptureDataExporter(QObject):
    total_progress_updated = pyqtSignal(int)  # percentage

    def __init__(self, db, total_steps, export_dir, with_offline_project=False, template_project_path='', raster_layer=None):
        QObject.__init__(self)
        self._export_dir = export_dir

        self.app = AppInterface()

        self._total_steps = total_steps

        # Parameters for the "with offline project" mode (i.e., export from coordinator to surveyors)
        self._with_offline_project = with_offline_project
        self._template_project_path = template_project_path
        self._raster_layer = raster_layer

        self._ili2db = Ili2DB()

        # Configure command environment
        self.db_factory = self._ili2db.dbs_supported.get_db_factory(db.engine)
        self.configuration = self._ili2db.get_export_configuration(self.db_factory, db, '')
        self.exporter = iliexporter.Exporter()
        self.exporter.tool = self.db_factory.get_model_baker_db_ili_mode()
        self.exporter.process_started.connect(self.on_process_started)
        self.exporter.stderr.connect(self.on_stderr)

        self.logger = Logger()
        self.log = ''
        self.count = 0
        self.current_progress = 0  # Range 0-100

    def export_basket(self, basket, name):
        """
        :param basket: Basket's t_ili_tid
        :param name: Receiver's name
        :return: Tuple res (bool), msg (string)
        """
        if self._with_offline_project and not self._template_project_path:
            return {None: (False, QCoreApplication.translate("FieldDataCaptureDataExporter",
                    "No template project was passed, but it is required for generating offline projects!"))}

        # Check prerequisite
        if not self._ili2db.get_full_java_exe_path():
            res_java, msg_java = self._ili2db.configure_java()
            if not res_java:
                return {None: (res_java, msg_java)}

        res, msg = False, ''

        self.log = ''
        self.configuration.xtffile = os.path.join(self._export_dir, "{}.xtf".format(name))
        self.configuration.baskets = [basket]
        self.exporter.configuration = self.configuration

        try:
            self.logger.info(__name__, "Exporting data from the capture model to XTF... ({})".format(name))
            if self.exporter.run() != iliexporter.Exporter.SUCCESS:
                res, msg = False, QCoreApplication.translate("FieldDataCaptureDataExporter", "An error occurred when exporting the data for '{}' (check the QGIS log panel).").format(name)
                QgsMessageLog.logMessage(self.log, QCoreApplication.translate("FieldDataCaptureDataExporter", "Allocate to coordinators"), Qgis.Critical)
            else:
                if self._with_offline_project:
                    self.logger.info(__name__, "Generating offline project for field data capture... ({})".format(name))
                    res, msg = self.generate_qgis_offline_project(self.configuration.xtffile)
                else:
                    res, msg = True, QCoreApplication.translate("FieldDataCaptureDataExporter", "XTF export for '{}' successful!").format(name)
        except JavaNotFoundError:
            res, msg = False, QCoreApplication.translate("FieldDataCaptureDataExporter", "Java {} could not be found. You can configure the JAVA_HOME environment variable manually, restart QGIS and try again.").format(JAVA_REQUIRED_VERSION)

        self.count += 1
        self.current_progress = int(self.count / self._total_steps * 100)
        self.total_progress_updated.emit(self.current_progress)

        return res, msg

    def generate_qgis_offline_project(self, xtf_path):
        """
        Generates offline projects based on the exported XTF. The QGS project is given by the user and points to a GPKG
        database (built from the exported XTF). Optionally, we might clip a given raster file with the legacy Plot layer
        extent.

        :param xtf_path: Path of the XTF containing data for the offline project
        :return: Tuple (whether the project generation was successful, message to describe errors if any)
        """
        step_range = 100 / self._total_steps
        weights = [2, 3, 5, 7, 9] if self._raster_layer else [3, 4, 6, 9]

        def update_progress(step):
            self.total_progress_updated.emit(int(self.current_progress + weights[step-1] / 10 * step_range))

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
        db = GPKGConnector(gpkg_path)
        model = LADMColModelRegistry().model(LADMNames.FIELD_DATA_CAPTURE_MODEL_KEY)
        res_schema_import, msg_schema_import = self._ili2db.import_schema(db,
                                                                          [model.full_name()],
                                                                          create_basket_col=True)
        if not res_schema_import:
            return res_schema_import, msg_schema_import
        update_progress(3)

        # Run import data
        res_import_data, msg_import_data = self._ili2db.import_data(db, xtf_path)
        if not res_import_data:
            return res_import_data, msg_import_data
        update_progress(4)

        # Create basket for new features created in the field
        db.test_connection()  # To generate db.names
        LADMData.get_or_create_default_ili2db_basket(db, FDC_WILD_CARD_BASKET_ID)

        # Clip raster if any
        if self._raster_layer:
            plot_layer = self.app.core.get_layer(db, db.names.FDC_LEGACY_PLOT_T, load=False)

            if plot_layer and plot_layer.isValid() and plot_layer.featureCount():
                self.logger.status(QCoreApplication.translate("FieldDataCaptureDataExporter",
                                                              "Clipping raster for '{}'...").format(user_alias))
                extent_str = get_extent_for_processing(plot_layer)
                self.logger.debug(__name__, "...clipping raster to '{}'".format(extent_str))

                # Clip raster and put the output in the offline folder
                clipped_raster = os.path.join(offline_dir, 'raster.tif')
                try:
                    processing.run("gdal:cliprasterbyextent",
                                   {'INPUT': self._raster_layer,
                                    'PROJWIN': extent_str,
                                    'OVERCRS': False, 'NODATA': None,
                                    'OPTIONS': '',  # 'COMPRESS=JPEG|JPEG_QUALITY=75'
                                    'DATA_TYPE': 0,
                                    'EXTRA' : '--config CHECK_DISK_FREE_SPACE NO',
                                    'OUTPUT': clipped_raster})
                except:
                    pass
            update_progress(5)

        db.close_connection()  # Because we are already done with the DB

        # Copy template project
        project_path = os.path.join(offline_dir, '_qfield.qgs')
        shutil.copyfile(self._template_project_path, project_path)
        self.logger.status()  # Clear the status bar

        return True, QCoreApplication.translate("FieldDataCaptureDataExporter",
                                                "Offline project for '{}' was created successfully!").format(user_alias)

    def on_process_started(self, command):
        self.log += command + '\n'

    def on_stderr(self, text):
        self.log += text
