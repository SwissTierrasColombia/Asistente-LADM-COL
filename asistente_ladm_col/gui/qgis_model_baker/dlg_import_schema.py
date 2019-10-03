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
                                 QListWidgetItem,
                                 QSizePolicy,
                                 QDialogButtonBox)
from qgis.core import Qgis
from qgis.gui import QgsMessageBar

from ...config.general_config import (DEFAULT_EPSG,
                                      DEFAULT_INHERITANCE,
                                      DEFAULT_MODEL_NAMES_CHECKED,
                                      SETTINGS_CONNECTION_TAB_INDEX,
                                      TOML_FILE_DIR,
                                      CREATE_BASKET_COL,
                                      CREATE_IMPORT_TID,
                                      STROKE_ARCS)
from ...gui.dialogs.dlg_get_java_path import GetJavaPathDialog
from ...gui.dialogs.dlg_settings import SettingsDialog
from ...utils.qgis_model_baker_utils import get_java_path_from_qgis_model_baker
from ...utils import get_ui_class
from ...utils.qt_utils import (Validators,
                               OverrideCursor)

from ...resources_rc import * # Necessary to show icons
from ...config.config_db_supported import ConfigDbSupported
from ...config.enums import EnumDbActionType
from ...lib.db.db_connector import DBConnector
DIALOG_UI = get_ui_class('qgis_model_baker/dlg_import_schema.ui')


class DialogImportSchema(QDialog, DIALOG_UI):
    models_have_changed = pyqtSignal(DBConnector, bool)  # dbconn, ladm_col_db
    open_dlg_import_data = pyqtSignal()

    BUTTON_NAME_CREATE_STRUCTURE = QCoreApplication.translate("DialogImportSchema", "Create LADM-COL structure")
    BUTTON_NAME_GO_TO_IMPORT_DATA =  QCoreApplication.translate("DialogImportData", "Go to Import Data...")

    def __init__(self, iface, qgis_utils, conn_manager, selected_models=list()):
        QDialog.__init__(self)
        self.iface = iface
        self.conn_manager = conn_manager
        self.selected_models = selected_models
        self.db = self.conn_manager.get_db_connector_from_source()
        self.qgis_utils = qgis_utils
        self.base_configuration = BaseConfiguration()
        self.ilicache = IliCache(self.base_configuration)
        self._conf_db = ConfigDbSupported()
        self._params = None
        self._current_db = None

        self.setupUi(self)

        self.validators = Validators()

        self.update_import_models()
        self.previous_item = QListWidgetItem()

        self.connection_setting_button.clicked.connect(self.show_settings)
        self.connection_setting_button.setText(QCoreApplication.translate("DialogImportSchema", "Connection Settings"))

        # LOG
        self.log_config.setTitle(QCoreApplication.translate("DialogImportSchema", "Show log"))

        self.bar = QgsMessageBar()
        self.bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.layout().addWidget(self.bar, 0, 0, Qt.AlignTop)

        self.buttonBox.accepted.disconnect()
        self.buttonBox.clicked.connect(self.accepted_import_schema)
        self.buttonBox.clear()
        self.buttonBox.addButton(QDialogButtonBox.Cancel)
        self._accept_button = self.buttonBox.addButton(self.BUTTON_NAME_CREATE_STRUCTURE, QDialogButtonBox.AcceptRole)
        self.buttonBox.addButton(QDialogButtonBox.Help)
        self.buttonBox.helpRequested.connect(self.show_help)

        self.update_connection_info()
        self.restore_configuration()

    def accepted_import_schema(self, button):
        if self.buttonBox.buttonRole(button) == QDialogButtonBox.AcceptRole:
            if button.text() == self.BUTTON_NAME_CREATE_STRUCTURE:
                self.accepted()
            elif button.text() == self.BUTTON_NAME_GO_TO_IMPORT_DATA:
                self.close()  # Close import schema dialog and open import open dialog
                self.open_dlg_import_data.emit()

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
        for modelname, checked in DEFAULT_MODEL_NAMES_CHECKED.items():
            item = QListWidgetItem(modelname)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Checked if modelname in self.selected_models or checked == Qt.Checked else Qt.Unchecked)  # From parameter or by default
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
        dlg = SettingsDialog(qgis_utils=self.qgis_utils, conn_manager=self.conn_manager)

        # Connect signals (DBUtils, QgisUtils)
        dlg.db_connection_changed.connect(self.conn_manager.db_connection_changed)
        dlg.db_connection_changed.connect(self.qgis_utils.cache_layers_and_relations)
        dlg.organization_tools_changed.connect(self.qgis_utils.organization_tools_changed)

        dlg.tabWidget.setCurrentIndex(SETTINGS_CONNECTION_TAB_INDEX)
        dlg.set_action_type(EnumDbActionType.SCHEMA_IMPORT)

        if dlg.exec_():
            self.db = dlg.get_db_connection()
            self.update_connection_info()

    def accepted(self):
        configuration = self.update_configuration()

        if not self.get_checked_models():
            message_error = QCoreApplication.translate("DialogImportSchema", "Please set a valid model(s) before creating the LADM-COL structure.")
            self.txtStdout.setText(message_error)
            self.show_message(message_error, Qgis.Warning)
            self.import_models_list_widget.setFocus()
            return

        self.save_configuration(configuration)

        with OverrideCursor(Qt.WaitCursor):
            self.progress_bar.show()
            self.progress_bar.setValue(0)

            self.disable()
            self.txtStdout.setTextColor(QColor('#000000'))
            self.txtStdout.clear()

            importer = iliimporter.Importer()

            item_db = self._conf_db.get_db_items()[self.db.mode]

            importer.tool = item_db.get_mbaker_db_ili_mode()
            importer.configuration = configuration
            importer.stdout.connect(self.print_info)
            importer.stderr.connect(self.on_stderr)
            importer.process_started.connect(self.on_process_started)
            importer.process_finished.connect(self.on_process_finished)

            try:
                if importer.run() != iliimporter.Importer.SUCCESS:
                    self.enable()
                    self.progress_bar.hide()
                    self.show_message(QCoreApplication.translate("DialogImportSchema", "An error occurred when creating the LADM-COL structure. For more information see the log..."), Qgis.Warning)
                    return
            except JavaNotFoundError:
                # Set JAVA PATH
                get_java_path_dlg = GetJavaPathDialog()
                get_java_path_dlg.setModal(True)
                if get_java_path_dlg.exec_():
                    configuration = self.update_configuration()
                if not get_java_path_from_qgis_model_baker():
                    message_error_java = QCoreApplication.translate("DialogImportSchema",
                                                                    """Java could not be found. You can configure the JAVA_HOME environment variable, restart QGIS and try again.""")
                    self.txtStdout.setTextColor(QColor('#000000'))
                    self.txtStdout.clear()
                    self.txtStdout.setText(message_error_java)
                    self.show_message(message_error_java, Qgis.Warning)
                self.enable()
                self.progress_bar.hide()
                return

            self.buttonBox.clear()

            self.buttonBox.addButton(self.BUTTON_NAME_GO_TO_IMPORT_DATA,
                                     QDialogButtonBox.AcceptRole).setStyleSheet("color: #007208;")

            self.buttonBox.setEnabled(True)
            self.buttonBox.addButton(QDialogButtonBox.Close)
            self.progress_bar.setValue(100)
            self.print_info(QCoreApplication.translate("DialogImportSchema", "\nDone!"), '#004905')
            self.show_message(QCoreApplication.translate("DialogImportSchema", "Creation of the LADM-COL structure was successfully completed"), Qgis.Success)

            self.models_have_changed.emit(self.db, True)

    def save_configuration(self, configuration):
        settings = QSettings()
        settings.setValue('Asistente-LADM_COL/QgisModelBaker/show_log', not self.log_config.isCollapsed())

    def restore_configuration(self):
        settings = QSettings()

        # Show log
        value_show_log = settings.value('Asistente-LADM_COL/QgisModelBaker/show_log', False, type=bool)
        self.log_config.setCollapsed(not value_show_log)

        # set model repository
        # if there is no option  by default use online model repository
        self.use_local_models = settings.value('Asistente-LADM_COL/models/custom_model_directories_is_checked', type=bool)
        if self.use_local_models:
            self.custom_model_directories = settings.value('Asistente-LADM_COL/models/custom_models') if settings.value('Asistente-LADM_COL/models/custom_models') else None

    def update_configuration(self):
        item_db = self._conf_db.get_db_items()[self.db.mode]

        configuration = SchemaImportConfiguration()
        item_db.set_db_configuration_params(self.db.dict_conn_params, configuration)

        # set custom toml file
        configuration.tomlfile = TOML_FILE_DIR
        configuration.epsg = QSettings().value('Asistente-LADM_COL/advanced_settings/epsg', int(DEFAULT_EPSG), int)
        configuration.inheritance = DEFAULT_INHERITANCE
        configuration.create_basket_col = CREATE_BASKET_COL
        configuration.create_import_tid = CREATE_IMPORT_TID
        configuration.stroke_arcs = STROKE_ARCS

        java_path = get_java_path_from_qgis_model_baker()
        if java_path:
            self.base_configuration.java_path = java_path

        # Check custom model directories
        if self.use_local_models:
            if self.custom_model_directories is None:
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

    def show_help(self):
        self.qgis_utils.show_help("import_schema")

    def disable(self):
        self.db_config.setEnabled(False)
        self.ili_config.setEnabled(False)
        self.buttonBox.setEnabled(False)

    def enable(self):
        self.db_config.setEnabled(True)
        self.ili_config.setEnabled(True)
        self.buttonBox.setEnabled(True)

    def show_message(self, message, level):
        self.bar.clearWidgets()  # Remove previous messages before showing a new one
        self.bar.pushMessage("Asistente LADM_COL", message, level, duration = 0)


