# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2018-06-11
        git sha              : :%H$
        copyright            : (C) 2018 by Germán Carrillo (BSF Swissphoto)
                               (C) 2019 by Leonardo Cardona (BSF Swissphoto)
        email                : gcarrillo@linuxmail.org
                               leocardonapiedrahita@gmail.com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""
from QgisModelBaker.libili2db import iliimporter
from QgisModelBaker.libili2db.ili2dbconfig import (SchemaImportConfiguration,
                                                   BaseConfiguration)
from QgisModelBaker.libili2db.ili2dbutils import color_log_text
from QgisModelBaker.libili2db.ilicache import IliCache
from QgisModelBaker.libili2db.iliimporter import JavaNotFoundError

from qgis.PyQt.QtCore import (Qt,
                              QCoreApplication,
                              QSettings,
                              pyqtSignal)
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtWidgets import (QDialog,
                                 QMessageBox,
                                 QListWidgetItem,
                                 QSizePolicy,
                                 QDialogButtonBox)
from qgis.core import (Qgis,
                       QgsCoordinateReferenceSystem)
from qgis.gui import QgsMessageBar

from asistente_ladm_col.config.general_config import (DEFAULT_EPSG,
                                                      COLLECTED_DB_SOURCE,
                                                      SETTINGS_CONNECTION_TAB_INDEX,
                                                      JAVA_REQUIRED_VERSION,
                                                      TOML_FILE_DIR,
                                                      SETTINGS_MODELS_TAB_INDEX,
                                                      DEFAULT_USE_CUSTOM_MODELS,
                                                      DEFAULT_MODELS_DIR)
from asistente_ladm_col.config.ladm_names import LADMNames
from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.gui.dialogs.dlg_settings import SettingsDialog
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.utils.java_utils import JavaUtils
from asistente_ladm_col.utils import get_ui_class
from asistente_ladm_col.utils.utils import show_plugin_help
from asistente_ladm_col.utils.qt_utils import (Validators,
                                               OverrideCursor)

from asistente_ladm_col.config.config_db_supported import ConfigDBsSupported
from asistente_ladm_col.config.enums import EnumDbActionType

DIALOG_UI = get_ui_class('qgis_model_baker/dlg_import_schema.ui')


class DialogImportSchema(QDialog, DIALOG_UI):
    open_dlg_import_data = pyqtSignal(dict)  # dict with key-value params
    on_result = pyqtSignal(bool)  # whether the tool was run successfully or not

    BUTTON_NAME_CREATE_STRUCTURE = QCoreApplication.translate("DialogImportSchema", "Create LADM-COL structure")
    BUTTON_NAME_GO_TO_IMPORT_DATA =  QCoreApplication.translate("DialogImportData", "Go to Import Data...")

    def __init__(self, iface, conn_manager, context, selected_models=list(), link_to_import_data=True):
        QDialog.__init__(self)
        self.iface = iface
        self.conn_manager = conn_manager
        self.selected_models = selected_models
        self.link_to_import_data = link_to_import_data
        self.logger = Logger()
        self.app = AppInterface()

        self.java_utils = JavaUtils()
        self.java_utils.download_java_completed.connect(self.download_java_complete)
        self.java_utils.download_java_progress_changed.connect(self.download_java_progress_change)

        self.db_source = context.get_db_sources()[0]
        self.db = self.conn_manager.get_db_connector_from_source(self.db_source)
        self.base_configuration = BaseConfiguration()
        self.ilicache = IliCache(self.base_configuration)
        self._dbs_supported = ConfigDBsSupported()
        self._running_tool = False

        # There may be two cases where we need to emit a db_connection_changed from the Schema Import dialog:
        #   1) Connection Settings was opened and the DB conn was changed.
        #   2) Connection Settings was never opened but the Schema Import ran successfully, in a way that new models may
        #      convert a db/schema LADM-COL compliant.
        self._db_was_changed = False  # To postpone calling refresh gui until we close this dialog instead of settings

        # Similarly, we could call a refresh on layers and relations cache in two cases:
        #   1) If the SI dialog was called for the COLLECTED source: opening Connection Settings and changing the DB
        #      connection.
        #   2) Not opening the Connection Settings, but running a successful Schema Import on the COLLECTED DB, which
        #      invalidates the cache as models change.
        self._schedule_layers_and_relations_refresh = False

        self.setupUi(self)

        self.validators = Validators()

        self.update_import_models()
        self.previous_item = QListWidgetItem()

        self.connection_setting_button.clicked.connect(self.show_settings)
        self.connection_setting_button.setText(QCoreApplication.translate("DialogImportSchema", "Connection Settings"))

        # CRS Setting
        self.epsg = DEFAULT_EPSG
        self.crsSelector.crsChanged.connect(self.crs_changed)

        # LOG
        self.log_config.setTitle(QCoreApplication.translate("DialogImportSchema", "Show log"))

        self.buttonBox.accepted.disconnect()
        self.buttonBox.clicked.connect(self.accepted_import_schema)
        self.buttonBox.clear()
        self.buttonBox.addButton(QDialogButtonBox.Cancel)
        self._accept_button = self.buttonBox.addButton(self.BUTTON_NAME_CREATE_STRUCTURE, QDialogButtonBox.AcceptRole)
        self.buttonBox.addButton(QDialogButtonBox.Help)
        self.buttonBox.helpRequested.connect(self.show_help)

        self.import_models_list_widget.setDisabled(bool(selected_models))  # If we got models from params, disable panel

        self.update_connection_info()
        self.restore_configuration()

        self.bar = QgsMessageBar()
        self.bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.layout().addWidget(self.bar, 0, 0, Qt.AlignTop)

    def accepted_import_schema(self, button):
        if self.buttonBox.buttonRole(button) == QDialogButtonBox.AcceptRole:
            if button.text() == self.BUTTON_NAME_CREATE_STRUCTURE:
                self.accepted()
            elif button.text() == self.BUTTON_NAME_GO_TO_IMPORT_DATA:
                self.close()  # Close import schema dialog and open import open dialog
                self.open_dlg_import_data.emit({"db_source": self.db_source})

    def reject(self):
        if self._running_tool:
            QMessageBox.information(self,
                                    QCoreApplication.translate("DialogImportSchema", "Warning"),
                                    QCoreApplication.translate("DialogImportSchema", "The Import Schema tool is still running. Please wait until it finishes."))
        else:
            self.close_dialog()

    def close_dialog(self):
        """
        We use this method to be safe when emitting the db_connection_changed, otherwise we could trigger slots that
        unload the plugin, destroying dialogs and thus, leading to crashes.
        """
        if self._schedule_layers_and_relations_refresh:
            self.conn_manager.db_connection_changed.connect(self.app.core.cache_layers_and_relations)

        if self._db_was_changed:
            self.conn_manager.db_connection_changed.emit(self.db, self.db.test_connection()[0], self.db_source)

        if self._schedule_layers_and_relations_refresh:
            self.conn_manager.db_connection_changed.disconnect(self.app.core.cache_layers_and_relations)

        self.logger.info(__name__, "Dialog closed.")
        self.done(QDialog.Accepted)

    def update_connection_info(self):
        db_description = self.db.get_description_conn_string()
        if db_description:
            self.db_connect_label.setText(db_description)
            self.db_connect_label.setToolTip(self.db.get_display_conn_string())
            self._accept_button.setEnabled(True)
        else:
            self.db_connect_label.setText(QCoreApplication.translate("DialogImportSchema", "The database is not defined!"))
            self.db_connect_label.setToolTip('')
            self._accept_button.setEnabled(False)

    def update_import_models(self):
        for modelname, checked in LADMNames.DEFAULT_MODEL_NAMES_CHECKED.items():
            item = QListWidgetItem(modelname)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            if self.selected_models:  # From parameters
                item.setCheckState(Qt.Checked if modelname in self.selected_models else Qt.Unchecked)
            else:  # By default
                item.setCheckState(Qt.Checked if checked == Qt.Checked else Qt.Unchecked)
            self.import_models_list_widget.addItem(item)

        self.import_models_list_widget.itemClicked.connect(self.on_item_clicked_import_model)
        self.import_models_list_widget.itemChanged.connect(self.on_itemchanged_import_model)

    def on_item_clicked_import_model(self, item):
        # disconnect signal to do changes in the items
        self.import_models_list_widget.itemChanged.disconnect(self.on_itemchanged_import_model)
        if self.previous_item.text() != item.text():
            if item.checkState() == Qt.Checked:
                item.setCheckState(Qt.Unchecked)
            else:
                item.setCheckState(Qt.Checked)
        # connect signal to check when the items change
        self.import_models_list_widget.itemChanged.connect(self.on_itemchanged_import_model)
        self.previous_item = item

    def on_itemchanged_import_model(self, item):
        if self.previous_item.text() != item.text():
            item.setSelected(True)
        self.previous_item = item

    def get_checked_models(self):
        checked_models = list()
        for index in range(self.import_models_list_widget.count()):
            item = self.import_models_list_widget.item(index)
            if item.checkState() == Qt.Checked:
                checked_models.append(item.text())
        return checked_models

    def show_settings(self):
        # We only need those tabs related to Model Baker/ili2db operations
        dlg = SettingsDialog(self.conn_manager)
        dlg.set_db_source(self.db_source)
        dlg.set_tab_pages_list([SETTINGS_CONNECTION_TAB_INDEX, SETTINGS_MODELS_TAB_INDEX])

        # Connect signals (DBUtils, Core)
        dlg.db_connection_changed.connect(self.db_connection_changed)
        if self.db_source == COLLECTED_DB_SOURCE:
            self._schedule_layers_and_relations_refresh = True

        dlg.set_action_type(EnumDbActionType.SCHEMA_IMPORT)

        if dlg.exec_():
            self.db = dlg.get_db_connection()
            self.update_connection_info()

    def db_connection_changed(self, db, ladm_col_db, db_source):
        # We dismiss parameters here, after all, we already have the db, and the ladm_col_db may change from this moment
        # until we close the import schema dialog
        self._db_was_changed = True
        self.clear_messages()  # Clean GUI messages if db connection changed

    def accepted(self):
        self._running_tool = True
        self.txtStdout.clear()
        self.progress_bar.setValue(0)
        self.bar.clearWidgets()

        java_home_set = self.java_utils.set_java_home()
        if not java_home_set:
            message_java = QCoreApplication.translate("DialogImportSchema", """Configuring Java {}...""").format(JAVA_REQUIRED_VERSION)
            self.txtStdout.setTextColor(QColor('#000000'))
            self.txtStdout.clear()
            self.txtStdout.setText(message_java)
            self.java_utils.get_java_on_demand()
            self.disable()
            return

        configuration = self.update_configuration()

        if not self.get_checked_models():
            self._running_tool = False
            message_error = QCoreApplication.translate("DialogImportSchema", "You should select a valid model(s) before creating the LADM-COL structure.")
            self.txtStdout.setText(message_error)
            self.show_message(message_error, Qgis.Warning)
            self.import_models_list_widget.setFocus()
            return

        self.save_configuration(configuration)

        with OverrideCursor(Qt.WaitCursor):
            self.progress_bar.show()
            self.disable()
            self.txtStdout.setTextColor(QColor('#000000'))
            self.txtStdout.clear()

            importer = iliimporter.Importer()

            db_factory = self._dbs_supported.get_db_factory(self.db.engine)

            importer.tool = db_factory.get_model_baker_db_ili_mode()
            importer.configuration = configuration
            importer.stdout.connect(self.print_info)
            importer.stderr.connect(self.on_stderr)
            importer.process_started.connect(self.on_process_started)
            importer.process_finished.connect(self.on_process_finished)

            try:
                if importer.run() != iliimporter.Importer.SUCCESS:
                    self._running_tool = False
                    self.show_message(QCoreApplication.translate("DialogImportSchema", "An error occurred when creating the LADM-COL structure. For more information see the log..."), Qgis.Warning)
                    self.on_result.emit(False)  # Inform other classes that the execution was not successful
                    return
            except JavaNotFoundError:
                self._running_tool = False
                message_error_java = QCoreApplication.translate("DialogImportSchema", "Java {} could not be found. You can configure the JAVA_HOME environment variable manually, restart QGIS and try again.").format(JAVA_REQUIRED_VERSION)
                self.txtStdout.setTextColor(QColor('#000000'))
                self.txtStdout.clear()
                self.txtStdout.setText(message_error_java)
                self.show_message(message_error_java, Qgis.Warning)
                return

            self._running_tool = False
            self.buttonBox.clear()
            if self.link_to_import_data:
                self.buttonBox.addButton(self.BUTTON_NAME_GO_TO_IMPORT_DATA,
                                         QDialogButtonBox.AcceptRole).setStyleSheet("color: #007208;")
            self.buttonBox.setEnabled(True)
            self.buttonBox.addButton(QDialogButtonBox.Close)
            self.progress_bar.setValue(100)
            self.print_info(QCoreApplication.translate("DialogImportSchema", "\nDone!"), '#004905')
            self.show_message(QCoreApplication.translate("DialogImportSchema", "LADM-COL structure was successfully created!"), Qgis.Success)
            self.on_result.emit(True)  # Inform other classes that the execution was successful
            self._db_was_changed = True  # Schema could become LADM compliant after a schema import

            if self.db_source == COLLECTED_DB_SOURCE:
                self.logger.info(__name__, "Schedule a call to refresh db relations cache since a Schema Import was run on the current 'collected' DB.")
                self._schedule_layers_and_relations_refresh = True

    def download_java_complete(self):
        self.accepted()

    def download_java_progress_change(self, progress):
        self.progress_bar.setValue(progress/2)
        if (progress % 20) == 0:
            self.txtStdout.append('...')

    def save_configuration(self, configuration):
        settings = QSettings()
        settings.setValue('Asistente-LADM-COL/QgisModelBaker/show_log', not self.log_config.isCollapsed())
        settings.setValue('Asistente-LADM-COL/QgisModelBaker/epsg', self.epsg)

    def restore_configuration(self):
        settings = QSettings()

        # CRS
        crs = QgsCoordinateReferenceSystem(settings.value('Asistente-LADM-COL/QgisModelBaker/epsg', int(DEFAULT_EPSG), int))
        self.crsSelector.setCrs(crs)
        self.crs_changed()

        # Show log
        value_show_log = settings.value('Asistente-LADM-COL/QgisModelBaker/show_log', False, type=bool)
        self.log_config.setCollapsed(not value_show_log)

        # set model repository
        # if there is no option  by default use online model repository
        self.use_local_models = settings.value('Asistente-LADM-COL/models/custom_model_directories_is_checked', DEFAULT_USE_CUSTOM_MODELS, type=bool)
        if self.use_local_models:
            self.custom_model_directories = settings.value('Asistente-LADM-COL/models/custom_models', DEFAULT_MODELS_DIR)

    def crs_changed(self):
        if self.crsSelector.crs().authid()[:5] != 'EPSG:':
            self.crs_label.setStyleSheet('color: orange')
            self.crs_label.setToolTip(QCoreApplication.translate("DialogImportSchema", "Please select an EPSG Coordinate Reference System"))
            self.epsg = int(DEFAULT_EPSG)
        else:
            self.crs_label.setStyleSheet('')
            self.crs_label.setToolTip(QCoreApplication.translate("DialogImportSchema", "Coordinate Reference System"))
            authid = self.crsSelector.crs().authid()
            self.epsg = int(authid[5:])

    def update_configuration(self):
        db_factory = self._dbs_supported.get_db_factory(self.db.engine)

        configuration = SchemaImportConfiguration()
        db_factory.set_ili2db_configuration_params(self.db.dict_conn_params, configuration)

        # set custom toml file
        configuration.tomlfile = TOML_FILE_DIR
        configuration.epsg = self.epsg
        configuration.inheritance = LADMNames.DEFAULT_INHERITANCE
        configuration.create_basket_col = LADMNames.CREATE_BASKET_COL
        configuration.create_import_tid = LADMNames.CREATE_IMPORT_TID
        configuration.stroke_arcs = LADMNames.STROKE_ARCS

        full_java_exe_path = JavaUtils.get_full_java_exe_path()
        if full_java_exe_path:
            self.base_configuration.java_path = full_java_exe_path

        # User could have changed the default values
        self.use_local_models = QSettings().value('Asistente-LADM-COL/models/custom_model_directories_is_checked', DEFAULT_USE_CUSTOM_MODELS, type=bool)
        self.custom_model_directories = QSettings().value('Asistente-LADM-COL/models/custom_models', DEFAULT_MODELS_DIR)

        # Check custom model directories
        if self.use_local_models:
            if not self.custom_model_directories:
                self.base_configuration.custom_model_directories_enabled = False
            else:
                self.base_configuration.custom_model_directories = self.custom_model_directories
                self.base_configuration.custom_model_directories_enabled = True

        configuration.base_configuration = self.base_configuration
        if self.get_checked_models():
            configuration.ilimodels = ';'.join(self.get_checked_models())

        return configuration

    def print_info(self, text, text_color='#000000', clear=False):
        self.txtStdout.setTextColor(QColor(text_color))
        self.txtStdout.append(text)
        QCoreApplication.processEvents()

    def on_stderr(self, text):
        color_log_text(text, self.txtStdout)
        self.advance_progress_bar_by_text(text)

    def on_process_started(self, command):
        self.txtStdout.setText(command)
        QCoreApplication.processEvents()

    def on_process_finished(self, exit_code, result):
        if exit_code == 0:
            color = '#004905'
            message = QCoreApplication.translate("DialogImportSchema", "Model(s) successfully imported into the database!")
        else:
            color = '#aa2222'
            message = QCoreApplication.translate("DialogImportSchema", "Finished with errors!")

            # Open log
            if self.log_config.isCollapsed():
                self.log_config.setCollapsed(False)

        self.txtStdout.setTextColor(QColor(color))
        self.txtStdout.append(message)

    def advance_progress_bar_by_text(self, text):
        if text.strip() == 'Info: compile models…':
            self.progress_bar.setValue(20)
            QCoreApplication.processEvents()
        elif text.strip() == 'Info: create table structure…':
            self.progress_bar.setValue(70)
            QCoreApplication.processEvents()

    def clear_messages(self):
        self.bar.clearWidgets()  # Remove previous messages before showing a new one
        self.txtStdout.clear()  # Clear previous log messages
        self.progress_bar.setValue(0)  # Initialize progress bar

    def show_help(self):
        show_plugin_help("import_schema")

    def disable(self):
        self.db_config.setEnabled(False)
        self.ili_config.setEnabled(False)
        self.buttonBox.setEnabled(False)

    def enable(self):
        self.db_config.setEnabled(True)
        self.ili_config.setEnabled(True)
        self.buttonBox.setEnabled(True)

    def show_message(self, message, level):
        if level == Qgis.Warning:
            self.enable()

        self.bar.clearWidgets()  # Remove previous messages before showing a new one
        self.bar.pushMessage("Asistente LADM-COL", message, level, duration = 0)
