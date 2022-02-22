"""
/***************************************************************************
                              Asistente LADM-COL
                             --------------------
        begin           : 2020-10-28
        git sha         : :%H$
        copyright       : (C) 2020 by Germán Carrillo (SwissTierras Colombia)
        email           : gcarrillo@linuxmail.org
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt5.QtCore import pyqtSignal
from qgis.PyQt.QtCore import (QObject,
                              QCoreApplication,
                              QSettings)
from qgis.core import (QgsMessageLog,
                       Qgis)

from asistente_ladm_col.config.config_db_supported import ConfigDBsSupported
from asistente_ladm_col.config.general_config import (JAVA_REQUIRED_VERSION,
                                                      DEFAULT_USE_CUSTOM_MODELS,
                                                      DEFAULT_MODELS_DIR,
                                                      CTM12_GPKG_SCRIPT_PATH,
                                                      CTM12_PG_SCRIPT_PATH,
                                                      TOML_FILE_DIR,
                                                      DEFAULT_ILI2DB_DEBUG_MODE)
from asistente_ladm_col.config.ili2db_names import ILI2DBNames
from asistente_ladm_col.lib.dependency.java_dependency import JavaDependency
from asistente_ladm_col.lib.ili import ili2dbvalidator
from asistente_ladm_col.lib.ili import iliimporter
from asistente_ladm_col.lib.ili import iliexporter
from asistente_ladm_col.lib.ili import iliupdater
from asistente_ladm_col.lib.ili.ili2dbconfig import (BaseConfiguration,
                                                     SchemaImportConfiguration,
                                                     ImportDataConfiguration,
                                                     ExportConfiguration,
                                                     UpdateDataConfiguration,
                                                     ValidateDataConfiguration)
from asistente_ladm_col.lib.ili.ili2dbutils import JavaNotFoundError
from asistente_ladm_col.lib.ili.ilicache import IliCache
from asistente_ladm_col.lib.model_registry import LADMColModelRegistry
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.utils.decorators import with_override_cursor


class Ili2DB(QObject):
    """
    Execute ili2db operations via Model Baker API
    """
    stdout = pyqtSignal(str)
    stderr = pyqtSignal(str)
    process_started = pyqtSignal(str)
    process_finished = pyqtSignal(int, int)

    def __init__(self):
        QObject.__init__(self)

        self.logger = Logger()

        self._java_path = ''
        self._java_dependency = JavaDependency()

        self.dbs_supported = ConfigDBsSupported()

        self._base_configuration = None
        self._ilicache = None
        self._log = ''

    def get_full_java_exe_path(self):
        if not self._java_path:
            self._java_path = JavaDependency.get_full_java_exe_path()

        return self._java_path

    def configure_java(self):
        if not self._java_dependency.set_java_home():
            message_java = QCoreApplication.translate("Ili2DB",
                                                      """Configuring Java {}...""").format(JAVA_REQUIRED_VERSION)
            self.logger.status(message_java)
            self._java_dependency.get_java_on_demand(asynchronous=False)

        res = True
        msg = 'Success!'

        java_path = self.get_full_java_exe_path()
        if not java_path:
            res = False
            msg = QCoreApplication.translate("Ili2DB",
                                             "Java {} could not be confiured for you. You can configure the JAVA_HOME environment variable manually, restart QGIS and try again.").format(
                JAVA_REQUIRED_VERSION)

        return res, msg

    def _get_base_configuration(self):
        """
        :return: BaseConfiguration object. If it's already configured, it returns the existing object, so that it can
                 be shared among chained operations (e.g., export DB1-->schema import DB2-->import DB2).
        """
        if not self._base_configuration:
            self._base_configuration = BaseConfiguration()
            self._ilicache = IliCache(self._base_configuration)
            self._ilicache.refresh()

            self._base_configuration.java_path = self.get_full_java_exe_path()  # It is well configured at this point!

            # Check custom model directories
            if QSettings().value('Asistente-LADM-COL/models/custom_model_directories_is_checked', DEFAULT_USE_CUSTOM_MODELS,
                                 type=bool):
                custom_model_directories = QSettings().value('Asistente-LADM-COL/models/custom_models', DEFAULT_MODELS_DIR)
                if not custom_model_directories:
                    self._base_configuration.custom_model_directories_enabled = False
                else:
                    self._base_configuration.custom_model_directories = custom_model_directories
                    self._base_configuration.custom_model_directories_enabled = True

            # Debug mode
            self._base_configuration.debugging_enabled = \
                QSettings().value('Asistente-LADM-COL/models/debug', DEFAULT_ILI2DB_DEBUG_MODE, type=bool)

            self._base_configuration.logfile_path = QSettings().value('Asistente-LADM-COL/models/log_file_path', '')

        return self._base_configuration

    def _get_ili_models(self, db):
        ili_models = list()
        model_names = db.get_models()
        if model_names:
            for model in LADMColModelRegistry().supported_models():
                if not model.hidden() and model.full_name() in model_names:
                    ili_models.append(model.full_name())

        return ili_models

    def get_import_schema_configuration(self, db, ili_models=list(), create_basket_col=False):
        db_factory = self.dbs_supported.get_db_factory(db.engine)

        configuration = SchemaImportConfiguration()
        db_factory.set_ili2db_configuration_params(db.dict_conn_params, configuration)
        configuration.inheritance = ILI2DBNames.DEFAULT_INHERITANCE
        configuration.create_basket_col = create_basket_col
        configuration.create_import_tid = ILI2DBNames.CREATE_IMPORT_TID
        configuration.stroke_arcs = ILI2DBNames.STROKE_ARCS
        configuration.tomlfile = TOML_FILE_DIR

        configuration.base_configuration = self._get_base_configuration()
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

    def get_import_data_configuration(self, db, xtf_path, dataset='', baskets=list(), disable_validation=False):
        db_factory = self.dbs_supported.get_db_factory(db.engine)
        configuration = ImportDataConfiguration()
        db_factory.set_ili2db_configuration_params(db.dict_conn_params, configuration)
        configuration.with_importtid = True
        configuration.xtffile = xtf_path
        configuration.disable_validation = disable_validation
        configuration.dataset = dataset
        configuration.baskets = baskets  # list with basket UUIDs

        configuration.base_configuration = self._get_base_configuration()
        ili_models = self._get_ili_models(db)
        if ili_models:
            configuration.ilimodels = ';'.join(ili_models)

        return configuration

    def get_export_configuration(self, db, xtf_path, dataset='', baskets=list(), disable_validation=False):
        db_factory = self.dbs_supported.get_db_factory(db.engine)
        configuration = ExportConfiguration()
        db_factory.set_ili2db_configuration_params(db.dict_conn_params, configuration)
        configuration.with_exporttid = True
        configuration.xtffile = xtf_path
        configuration.disable_validation = disable_validation
        configuration.dataset = dataset
        configuration.baskets = baskets  # List with basket UUIDs

        configuration.base_configuration = self._get_base_configuration()
        ili_models = self._get_ili_models(db)
        if ili_models:
            configuration.ilimodels = ';'.join(ili_models)

        return configuration

    def get_update_configuration(self, db_factory, db, xtf_path, dataset_name):
        configuration = UpdateDataConfiguration()
        db_factory.set_ili2db_configuration_params(db.dict_conn_params, configuration)

        configuration.base_configuration = self._get_base_configuration()
        ili_models = self._get_ili_models(db)
        if ili_models:
            configuration.ilimodels = ';'.join(ili_models)

        configuration.dataset = dataset_name
        configuration.with_importbid = True
        configuration.with_importtid = True
        configuration.xtffile = xtf_path

        return configuration

    def get_validate_configuration(self, db_factory, db, model_names, xtflog_path, configfile_path):
        configuration = ValidateDataConfiguration()
        db_factory.set_ili2db_configuration_params(db.dict_conn_params, configuration)

        configuration.base_configuration = self._get_base_configuration()
        # Since BaseConfiguration can be shared, avoid a --trace in --validate operation (not supported by ili2db)
        configuration.base_configuration.debugging_enabled = False

        if model_names:
            configuration.ilimodels = ';'.join(model_names)
        if xtflog_path:
            configuration.xtflogfile = xtflog_path
        if configfile_path:
            configuration.configfile = configfile_path

        return configuration

    @with_override_cursor
    def import_schema(self, db, configuration: SchemaImportConfiguration):
        # Check prerequisite
        if not self.get_full_java_exe_path():
            res_java, msg_java = self.configure_java()
            if not res_java:
                return res_java, msg_java

        # Configure command parameters
        db_factory = self.dbs_supported.get_db_factory(db.engine)

        # Configure run
        importer = iliimporter.Importer()
        importer.tool = db_factory.get_model_baker_db_ili_mode()
        importer.process_started.connect(self.on_process_started)
        importer.stderr.connect(self.on_stderr)
        importer.configuration = configuration

        importer.stdout.connect(self.stdout)
        importer.process_finished.connect(self.process_finished)

        # Run!
        res = True
        msg = QCoreApplication.translate("Ili2DB", "Schema import ran successfully!")
        self._log = ''
        self.logger.status(QCoreApplication.translate("Ili2Db", "Creating LADM-COL structure into {}...").format(db.engine.upper()))
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

        self.logger.clear_status()
        return res, msg

    @with_override_cursor
    def import_data(self, db, configuration: ImportDataConfiguration):
        # Check prerequisite
        if not self.get_full_java_exe_path():
            res_java, msg_java = self.configure_java()
            if not res_java:
                return res_java, msg_java

        # Configure command parameters
        db_factory = self.dbs_supported.get_db_factory(db.engine)

        # Configure run
        importer = iliimporter.Importer(dataImport=True)
        importer.tool = db_factory.get_model_baker_db_ili_mode()
        importer.process_started.connect(self.on_process_started)
        importer.stderr.connect(self.on_stderr)
        importer.configuration = configuration

        # Run!
        res = True
        msg = QCoreApplication.translate("Ili2DB", "XTF '{}' imported successfully!").format(configuration.xtffile)
        self._log = ''
        self.logger.status(QCoreApplication.translate("Ili2Db", "Importing XTF into {}...").format(db.engine.upper()))
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

        self.logger.clear_status()
        return res, msg

    @with_override_cursor
    def export(self, db, configuration: ExportConfiguration):
        # Check prerequisite
        if not self.get_full_java_exe_path():
            res_java, msg_java = self.configure_java()
            if not res_java:
                return res_java, msg_java

        # Configure command parameters
        db_factory = self.dbs_supported.get_db_factory(db.engine)

        # Configure run
        exporter = iliexporter.Exporter()
        exporter.tool = db_factory.get_model_baker_db_ili_mode()
        exporter.process_started.connect(self.on_process_started)
        exporter.stderr.connect(self.on_stderr)
        exporter.configuration = configuration

        # Run!
        res = True
        msg = QCoreApplication.translate("Ili2DB", "XTF '{}' exported successfully!").format(configuration.xtffile)
        self._log = ''
        self.logger.status(QCoreApplication.translate("Ili2Db", "Exporting from {} to XTF...").format(db.engine.upper()))
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

        self.logger.clear_status()
        return res, msg

    @with_override_cursor
    def update(self, db, xtf_path, dataset_name):
        # Check prerequisite
        if not self.get_full_java_exe_path():
            res_java, msg_java = self.configure_java()
            if not res_java:
                return res_java, msg_java

        # Configure command parameters
        db_factory = self.dbs_supported.get_db_factory(db.engine)
        configuration = self.get_update_configuration(db_factory, db, xtf_path, dataset_name)

        # Configure run
        updater = iliupdater.Updater()
        updater.tool = db_factory.get_model_baker_db_ili_mode()
        updater.process_started.connect(self.on_process_started)
        updater.stderr.connect(self.on_stderr)
        updater.configuration = configuration

        # Run!
        res = True
        msg = QCoreApplication.translate("Ili2DB", "DB updated successfully from XTF file '{}'!").format(xtf_path)
        self._log = ''
        self.logger.status(QCoreApplication.translate("Ili2Db", "Updating {} DB from XTF '{}'...").format(db.engine.upper(), xtf_path))
        try:
            if updater.run() != iliupdater.Updater.SUCCESS:
                msg = QCoreApplication.translate("Ili2DB",
                                                 "An error occurred when updating the DB from an XTF (check the QGIS log panel).")
                res = False
                QgsMessageLog.logMessage(self._log, QCoreApplication.translate("Ili2DB", "Update DB from XTF"), Qgis.Critical)
            else:
                self.logger.info(__name__, msg)

        except JavaNotFoundError:
            msg = QCoreApplication.translate("Ili2DB",
                                             "Java {} could not be found. You can configure the JAVA_HOME environment variable manually, restart QGIS and try again.").format(
                JAVA_REQUIRED_VERSION)
            res = False

        self.logger.clear_status()
        return res, msg

    @with_override_cursor
    def validate(self, db, model_names=list(), xtflog_path='', configfile_path=''):
        # Check prerequisite
        if not self.get_full_java_exe_path():
            res_java, msg_java = self.configure_java()
            if not res_java:
                return res_java, msg_java

        # Configure command parameters
        db_factory = self.dbs_supported.get_db_factory(db.engine)
        configuration = self.get_validate_configuration(db_factory, db, model_names, xtflog_path, configfile_path)

        # Configure run
        validator = ili2dbvalidator.Ili2DBValidator()
        validator.tool = db_factory.get_model_baker_db_ili_mode()
        validator.process_started.connect(self.on_process_started)
        validator.stderr.connect(self.on_stderr)
        validator.configuration = configuration

        # Run!
        res = True
        msg = QCoreApplication.translate("Ili2DB", "Data successfully validated from DB '{}'!").format(db.get_description_conn_string())
        self._log = ''
        self.logger.status(QCoreApplication.translate("Ili2Db", "Validating data from '{}' DB...").format(db.get_description_conn_string()))
        try:
            res_validation = validator.run()
            if (res_validation != ili2dbvalidator.Ili2DBValidator.SUCCESS
                    and res_validation != ili2dbvalidator.Ili2DBValidator.SUCCESS_WITH_VALIDATION_ERRORS):
                msg = QCoreApplication.translate("Ili2DB",
                                                 "An error occurred when validating data from a DB (check the QGIS log panel).")
                res = False
                QgsMessageLog.logMessage(self._log, QCoreApplication.translate("Ili2DB", "Validate data from DB"),
                                         Qgis.Critical)
            else:
                self.logger.info(__name__, msg)
        except JavaNotFoundError:
            msg = QCoreApplication.translate("Ili2DB",
                                             "Java {} could not be found. You can configure the JAVA_HOME environment variable manually, restart QGIS and try again.").format(
                JAVA_REQUIRED_VERSION)
            res = False

        self.logger.clear_status()
        return res, msg

    def on_process_started(self, command):
        self._log += command + '\n'
        self.process_started.emit(command)

    def on_stderr(self, text):
        self._log += text
        self.stderr.emit(text)
