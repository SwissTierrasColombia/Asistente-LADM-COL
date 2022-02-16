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

from qgis.PyQt.QtCore import (QCoreApplication,
                              pyqtSignal,
                              QObject,
                              QSettings,
                              Qt)
from qgis.core import (QgsMessageLog,
                       Qgis)

from asistente_ladm_col.lib.ili.ili2dbutils import JavaNotFoundError
from asistente_ladm_col.lib.ili import iliexporter
from asistente_ladm_col.lib.ili.ili2dbconfig import (BaseConfiguration,
                                                   ExportConfiguration)
from asistente_ladm_col.lib.ili.ilicache import IliCache

from asistente_ladm_col.config.config_db_supported import ConfigDBsSupported
from asistente_ladm_col.config.general_config import (JAVA_REQUIRED_VERSION,
                                                      DEFAULT_USE_CUSTOM_MODELS,
                                                      DEFAULT_MODELS_DIR)
from asistente_ladm_col.lib.dependency.java_dependency import JavaDependency
from asistente_ladm_col.lib.model_registry import LADMColModelRegistry
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.utils.qt_utils import OverrideCursor


class BasketExporter(QObject):
    total_progress_updated = pyqtSignal(int)  # percentage

    def __init__(self, db, basket_dict, export_dir):
        QObject.__init__(self)
        self._db = db
        self._basket_dict = basket_dict  # {t_ili_tids: receiver_name}
        self._export_dir = export_dir
        self.logger = Logger()

        self.log = ''
        self.java_dependency = JavaDependency()
        self.java_dependency.download_dependency_completed.connect(self.download_java_complete)

        self._dbs_supported = ConfigDBsSupported()

    def export_baskets(self):
        java_home_set = self.java_dependency.set_java_home()
        if not java_home_set:
            message_java = QCoreApplication.translate("BasketExporter", """Configuring Java {}...""").format(
                JAVA_REQUIRED_VERSION)
            self.logger.status(message_java)
            self.java_dependency.get_java_on_demand()
            return

        self.base_configuration = BaseConfiguration()
        self.ilicache = IliCache(self.base_configuration)
        self.ilicache.refresh()

        db_factory = self._dbs_supported.get_db_factory(self._db.engine)
        self.configuration = ExportConfiguration()
        db_factory.set_ili2db_configuration_params(self._db.dict_conn_params, self.configuration)
        self.configuration.with_exporttid = True
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

        self.configuration.base_configuration = self.base_configuration
        if self.get_ili_models():
            self.configuration.ilimodels = ';'.join(self.get_ili_models())

        self.exporter = iliexporter.Exporter()
        self.exporter.tool = db_factory.get_model_baker_db_ili_mode()
        self.exporter.process_started.connect(self.on_process_started)
        self.exporter.stderr.connect(self.on_stderr)
        #self.exporter.process_finished.connect(self.on_process_finished)

        res = dict()
        count = 0
        total = len(self._basket_dict)

        with OverrideCursor(Qt.WaitCursor):
            for basket,name in self._basket_dict.items():
                self.log = ''
                self.configuration.xtffile = os.path.join(self._export_dir, "{}.xtf".format(name))
                self.configuration.baskets = basket
                self.exporter.configuration = self.configuration

                try:
                    if self.exporter.run() != iliexporter.Exporter.SUCCESS:
                        msg = QCoreApplication.translate("BasketExporter", "An error occurred when exporting the data for '{}' (check the QGIS log panel).").format(name)
                        res[basket] = (False, msg)
                        QgsMessageLog.logMessage(self.log, QCoreApplication.translate("BasketExporter", "Allocate to coordinators"), Qgis.Critical)
                    else:
                        res[basket] = (True, QCoreApplication.translate("BasketExporter", "XTF export for '{}' successful!").format(name) )
                except JavaNotFoundError:
                    msg = QCoreApplication.translate("BasketExporter", "Java {} could not be found. You can configure the JAVA_HOME environment variable manually, restart QGIS and try again.").format(JAVA_REQUIRED_VERSION)
                    res[basket] = (False, msg)

                count += 1
                self.total_progress_updated.emit(count/total*100)

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
