# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM-COL
                             --------------------
        begin                : 2020-10-28
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
from functools import partial

from qgis.PyQt.QtCore import (QObject,
                              QCoreApplication,
                              QSettings)
from qgis.core import (QgsMessageLog,
                       Qgis)

from QgisModelBaker.libili2db import iliexporter, iliimporter
from QgisModelBaker.libili2db.ili2dbconfig import (BaseConfiguration,
                                                   ExportConfiguration,
                                                   SchemaImportConfiguration,
                                                   ImportDataConfiguration)
from QgisModelBaker.libili2db.ilicache import IliCache
from QgisModelBaker.libili2db.ili2dbutils import JavaNotFoundError

from asistente_ladm_col.config.config_db_supported import ConfigDBsSupported
from asistente_ladm_col.config.general_config import (JAVA_REQUIRED_VERSION,
                                                      DEFAULT_USE_CUSTOM_MODELS,
                                                      DEFAULT_MODELS_DIR, CTM12_GPKG_SCRIPT_PATH, CTM12_PG_SCRIPT_PATH)
from asistente_ladm_col.config.ili2db_names import ILI2DBNames
from asistente_ladm_col.lib.dependency.java_dependency import JavaDependency
from asistente_ladm_col.lib.ladm_col_models import LADMColModelRegistry
from asistente_ladm_col.lib.logger import Logger


class Ili2DB(QObject):
    """
    Execute ili2db operations via Model Baker API
    """
    def __init__(self):
        QObject.__init__(self)

        self.logger = Logger()

        self._java_path = ''
        self._java_dependency = JavaDependency()

        self._dbs_supported = ConfigDBsSupported()

        self._base_configuration = None
        self._ilicache = None
        self._log = ''

    def _get_full_java_exe_path(self):
        if not self._java_path:
            self._java_path = JavaDependency.get_full_java_exe_path()

        return self._java_path

    def _configure_java(self, function_to_call, function_params):
        if not self._java_dependency.set_java_home():
            message_java = QCoreApplication.translate("Ili2DB",
                                                      """Configuring Java {}...""").format(JAVA_REQUIRED_VERSION)
            self.logger.status(message_java)
            self._java_dependency.download_dependency_completed.connect(partial(self.download_java_complete,
                                                                                function_to_call,
                                                                                function_params))
            self._java_dependency.get_java_on_demand()
            return

        java_path = self._get_full_java_exe_path()
        if java_path:
            # Now that we've configured Java properly, let's call again the function that was originally called
            function_to_call(**function_params)
        else:
            self.logger.critical_msg(__name__, QCoreApplication.translate("Ili2DB",
                                             "Java {} could not be confiured for you. You can configure the JAVA_HOME environment variable manually, restart QGIS and try again.").format(
                JAVA_REQUIRED_VERSION))

    def download_java_complete(self, function_to_call, function_params):
        # Now that we got Java, set the java home
        self._configure_java(function_to_call, function_params)

    def _get_base_configuration(self):
        """
        :return: BaseConfiguration object. If it's already configured, it returns the existing object, so that it can
                 be shared among chained operations (e.g., export DB1-->schema import DB2-->import DB2).
        """
        if not self._base_configuration:
            self._base_configuration = BaseConfiguration()
            self._ilicache = IliCache(self._base_configuration)
            self._ilicache.refresh()

            self._base_configuration.java_path = self._get_full_java_exe_path()  # It is well configured at this point!

            # Check custom model directories
            if QSettings().value('Asistente-LADM-COL/models/custom_model_directories_is_checked', DEFAULT_USE_CUSTOM_MODELS,
                                 type=bool):
                custom_model_directories = QSettings().value('Asistente-LADM-COL/models/custom_models', DEFAULT_MODELS_DIR)
                if not custom_model_directories:
                    self._base_configuration.custom_model_directories_enabled = False
                else:
                    self._base_configuration.custom_model_directories = custom_model_directories
                    self._base_configuration.custom_model_directories_enabled = True

        return self._base_configuration

    def _get_ili_models(self, db):
        ili_models = list()
        model_names = db.get_models()
        if model_names:
            for model in LADMColModelRegistry().supported_models():
                if not model.hidden() and model.full_name() in model_names:
                    ili_models.append(model.full_name())

        return ili_models

    def get_import_schema_configuration(self, db_factory, db, create_basket_col=False):
        configuration = SchemaImportConfiguration()
        db_factory.set_ili2db_configuration_params(db.dict_conn_params, configuration)
        configuration.inheritance = ILI2DBNames.DEFAULT_INHERITANCE
        configuration.create_basket_col = create_basket_col
        configuration.create_import_tid = ILI2DBNames.CREATE_IMPORT_TID
        configuration.stroke_arcs = ILI2DBNames.STROKE_ARCS

        configuration.base_configuration = self._get_base_configuration()
        ili_models = self._get_ili_models(db)
        if ili_models:
            configuration.ilimodels = ';'.join(ili_models)

        if db.engine == 'gpkg':
            # EPSG:9377 support for GPKG (Ugly, I know) We need to send known parameters, we'll fix this in the post_script
            configuration.srs_auth = 'EPSG'
            configuration.srs_code = 3116
            configuration.post_script = CTM12_GPKG_SCRIPT_PATH
        elif db.engine == 'pg':
            configuration.srs_auth = 'EPSG'
            configuration.srs_code = 9377
            configuration.pre_script = CTM12_PG_SCRIPT_PATH

        return configuration

    def get_import_data_configuration(self, db_factory, db, xtf_path, dataset='', baskets=list(), disable_validation=False):
        configuration = ImportDataConfiguration()
        db_factory.set_ili2db_configuration_params(db.dict_conn_params, configuration)
        configuration.with_importtid = True
        configuration.xtffile = xtf_path
        configuration.disable_validation = disable_validation
        configuration.dataset = dataset
        configuration.baskets = baskets[0] if baskets else ''  # list with basket UUIDs

        configuration.base_configuration = self._get_base_configuration()
        ili_models = self._get_ili_models(db)
        if ili_models:
            configuration.ilimodels = ';'.join(ili_models)

        return configuration

    def get_export_configuration(self, db_factory, db, xtf_path, dataset='', baskets=list(), disable_validation=False):
        configuration = ExportConfiguration()
        db_factory.set_ili2db_configuration_params(db.dict_conn_params, configuration)
        configuration.with_exporttid = True
        configuration.xtffile = xtf_path
        configuration.disable_validation = disable_validation
        configuration.dataset = dataset
        configuration.baskets = baskets[0] if baskets else ''  # List with basket UUIDs

        configuration.base_configuration = self._get_base_configuration()
        ili_models = self._get_ili_models(db)
        if ili_models:
            configuration.ilimodels = ';'.join(ili_models)

        return configuration

    def import_schema(self, db, create_basket_col=False):
        # Check prerequisite
        if not self._get_full_java_exe_path():
            self._configure_java(self.import_schema, {'db': db, 'create_basket_col': create_basket_col})
            return  # Current function will be called again when JAVA has been downloaded

        # Configure command parameters
        db_factory = self._dbs_supported.get_db_factory(db.engine)
        configuration = self.get_import_schema_configuration(db_factory, db, create_basket_col)

        # Configure run
        importer = iliimporter.Importer()
        importer.tool = db_factory.get_model_baker_db_ili_mode()
        importer.process_started.connect(self.on_process_started)
        importer.stderr.connect(self.on_stderr)
        importer.configuration = configuration

        # Run!
        res = True
        msg = QCoreApplication.translate("Ili2DB", "Schema import ran successfully!")
        self._log = ''
        try:
            if importer.run() != iliimporter.Importer.SUCCESS:
                msg = QCoreApplication.translate("Ili2DB",
                                                 "An error occurred when importing a schema into a DB (check the QGIS log panel).")
                res = False
                QgsMessageLog.logMessage(self._log, QCoreApplication.translate("Ili2DB", "DB Schema Import"), Qgis.Critical)

        except JavaNotFoundError:
            msg = QCoreApplication.translate("Ili2DB",
                                             "Java {} could not be found. You can configure the JAVA_HOME environment variable manually, restart QGIS and try again.").format(
                JAVA_REQUIRED_VERSION)
            res = False

        return res, msg

    def import_data(self, db, xtf_path, dataset='', baskets=list(), disable_validation=False):
        # Check prerequisite
        if not self._get_full_java_exe_path():
            self._configure_java(self.import_schema, {'db': db,
                                                      'xtf_path': xtf_path,
                                                      'dataset': dataset,
                                                      'baskets': baskets,
                                                      'disable_validation': disable_validation})
            return  # Current function will be called again when JAVA has been downloaded

        # Configure command parameters
        db_factory = self._dbs_supported.get_db_factory(db.engine)
        configuration = self.get_import_data_configuration(db_factory, db, xtf_path, dataset, baskets, disable_validation)

        # Configure run
        importer = iliimporter.Importer(dataImport=True)
        importer.tool = db_factory.get_model_baker_db_ili_mode()
        importer.process_started.connect(self.on_process_started)
        importer.stderr.connect(self.on_stderr)
        importer.configuration = configuration

        # Run!
        res = True
        msg = QCoreApplication.translate("Ili2DB", "XTF '{}' imported successfully!").format(xtf_path)
        self._log = ''
        try:
            if importer.run() != iliimporter.Importer.SUCCESS:
                msg = QCoreApplication.translate("Ili2DB",
                                                 "An error occurred when importing from XTF (check the QGIS log panel).")
                res = False
                QgsMessageLog.logMessage(self._log, QCoreApplication.translate("Ili2DB", "Import from XTF"),
                                         Qgis.Critical)

        except JavaNotFoundError:
            msg = QCoreApplication.translate("Ili2DB",
                                             "Java {} could not be found. You can configure the JAVA_HOME environment variable manually, restart QGIS and try again.").format(
                JAVA_REQUIRED_VERSION)
            res = False

        return res, msg

    def export(self, db, xtf_path, dataset='', baskets=list(), disable_validation=False):
        # Check prerequisite
        if not self._get_full_java_exe_path():
            self._configure_java(self.export, {'db': db,
                                               'xtf_path': xtf_path,
                                               'dataset': dataset,
                                               'baskets': baskets,
                                               'disable_validation': disable_validation})
            return  # Current function will be called again when JAVA has been downloaded

        # Configure command parameters
        db_factory = self._dbs_supported.get_db_factory(db.engine)
        configuration = self.get_export_configuration(db_factory, db, xtf_path, dataset, baskets, disable_validation)

        # Configure run
        exporter = iliexporter.Exporter()
        exporter.tool = db_factory.get_model_baker_db_ili_mode()
        exporter.process_started.connect(self.on_process_started)
        exporter.stderr.connect(self.on_stderr)
        exporter.configuration = configuration

        # Run!
        res = True
        msg = QCoreApplication.translate("Ili2DB", "XTF '{}' exported successfully!").format(xtf_path)
        self._log = ''
        try:
            if exporter.run() != iliexporter.Exporter.SUCCESS:
                msg = QCoreApplication.translate("Ili2DB",
                                                 "An error occurred when exporting data to XTF (check the QGIS log panel).")
                res = False
                QgsMessageLog.logMessage(self._log, QCoreApplication.translate("Ili2DB", "Export to XTF"), Qgis.Critical)
            else:
                self.logger.info(__name__, msg)

        except JavaNotFoundError:
            msg = QCoreApplication.translate("Ili2DB",
                                             "Java {} could not be found. You can configure the JAVA_HOME environment variable manually, restart QGIS and try again.").format(
                JAVA_REQUIRED_VERSION)
            res = False

        return res, msg

    def update(self, db, xtf_path, dataset_name):
        # Check prerequisite
        # Configure command parameters
        # Configure run
        # Run!
        pass

    def on_process_started(self, command):
        self._log += command + '\n'

    def on_stderr(self, text):
        self._log += text
