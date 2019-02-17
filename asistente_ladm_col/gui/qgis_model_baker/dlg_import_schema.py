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
                              QRegExp,
                              QSettings)
from qgis.PyQt.QtGui import (QColor,
                             QValidator,
                             QRegExpValidator)
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
from ...gui.dlg_get_java_path import DialogGetJavaPath
from ...utils.qgis_model_baker_utils import get_java_path_from_qgis_model_baker
from ...utils import get_ui_class
from ...utils.qt_utils import (Validators,
                               FileValidator,
                               make_file_selector,
                               make_save_file_selector,
                               OverrideCursor)
from ...resources_rc import *

DIALOG_UI = get_ui_class('qgis_model_baker/dlg_import_schema.ui')

class DialogImportSchema(QDialog, DIALOG_UI):

    def __init__(self, iface, db, qgis_utils):
        QDialog.__init__(self)
        self.iface = iface
        self.db = db
        self.qgis_utils = qgis_utils
        self.base_configuration = BaseConfiguration()
        self.ilicache = IliCache(self.base_configuration)

        self.setupUi(self)

        self.type_combo_box.clear()
        self.type_combo_box.addItem(QCoreApplication.translate("DialogImportSchema", "PostgreSQL/PostGIS"), 'pg')
        self.type_combo_box.addItem(QCoreApplication.translate("DialogImportSchema", "GeoPackage"), 'gpkg')
        self.type_combo_box.setCurrentIndex(
            self.type_combo_box.findData(QSettings().value('Asistente-LADM_COL/db_connection_source', 'pg')))
        self.type_combo_box.currentIndexChanged.connect(self.type_changed)
        self.type_changed()

        self.schema_name_line_edit.setPlaceholderText(QCoreApplication.translate("DialogImportSchema", "[Name of the schema to be created]"))
        self.validators = Validators()

        # schema name mustn't have special characters
        regex = QRegExp("[a-zA-Z0-9_]+")
        validator = QRegExpValidator(regex)
        self.schema_name_line_edit.setValidator(validator)
        self.schema_name_line_edit.setMaxLength(63)
        self.schema_name_line_edit.textChanged.connect(self.validators.validate_line_edits_lower_case)
        self.schema_name_line_edit.textChanged.emit(self.schema_name_line_edit.text())

        self.update_import_models()
        self.previous_item = QListWidgetItem()

        # PG
        self.db_connect_label.setToolTip(self.db.get_display_conn_string())
        self.connection_setting_button.clicked.connect(self.show_settings)
        self.connection_setting_button.setText(QCoreApplication.translate("DialogImportSchema", "Connection Settings"))
        if self.type_combo_box.currentData() == 'pg':
            self.db_connect_label.setText(self.db.dict_conn_params['database'])

        # GPKG
        self.gpkg_file_line_edit.setPlaceholderText(QCoreApplication.translate("DialogImportSchema", "[Name of the Geopackage to be created]"))
        self.gpkg_file_browse_button.clicked.connect(make_file_selector(self.gpkg_file_line_edit,
                                                                        title=QCoreApplication.translate("DialogImportSchema", "Open GeoPackage database file"),
                                                                        file_filter=QCoreApplication.translate("DialogImportSchema", "GeoPackage Database (*.gpkg)")))

        gpkgFileValidator = FileValidator(pattern='*.gpkg')
        self.gpkg_file_line_edit.setValidator(gpkgFileValidator)

        self.gpkgSaveFileValidator = FileValidator(pattern='*.gpkg', allow_non_existing=True)
        self.gpkgOpenFileValidator = FileValidator(pattern='*.gpkg')
        self.gpkg_file_line_edit.textChanged.connect(self.validators.validate_line_edits)

        # LOG
        self.log_config.setTitle(QCoreApplication.translate("DialogImportSchema", "Show log"))

        self.bar = QgsMessageBar()
        self.bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.layout().addWidget(self.bar, 0, 0, Qt.AlignTop)

        self.buttonBox.accepted.disconnect()
        self.buttonBox.accepted.connect(self.accepted)
        self.buttonBox.clear()
        self.buttonBox.addButton(QDialogButtonBox.Cancel)
        self.buttonBox.addButton(QCoreApplication.translate("DialogImportSchema", "Create LADM-COL structure"), QDialogButtonBox.AcceptRole)
        self.buttonBox.addButton(QDialogButtonBox.Help)
        self.buttonBox.helpRequested.connect(self.show_help)

    def showEvent(self, event):
        self.restore_configuration()

    def update_import_models(self):
        for modelname in DEFAULT_MODEL_NAMES_CHECKED:
            item = QListWidgetItem(modelname)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(DEFAULT_MODEL_NAMES_CHECKED[modelname])
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
        dlg = self.qgis_utils.get_settings_dialog()
        dlg.tabWidget.setCurrentIndex(SETTINGS_CONNECTION_TAB_INDEX)
        if dlg.exec_():
            self.db = self.qgis_utils.get_db_connection()
            self.db_connect_label.setToolTip(self.db.get_display_conn_string())
            self.db_connect_label.setText(self.db.dict_conn_params['database'])

    def accepted(self):
        configuration = self.update_configuration()

        if not self.get_checked_models():
            message_error = QCoreApplication.translate("DialogImportSchema", "Please set a valid model(s) before creating the LADM-COL structure.")
            self.txtStdout.setText(message_error)
            self.show_message(message_error, Qgis.Warning)
            self.import_models_list_widget.setFocus()
            return

        if self.type_combo_box.currentData() == 'pg':
            if not self.schema_name_line_edit.text().strip():
                message_error = QCoreApplication.translate("DialogImportSchema", "Please set a valid schema name before creating the LADM-COL structure.")
                self.txtStdout.setText(message_error)
                self.show_message(message_error, Qgis.Warning)
                self.schema_name_line_edit.setFocus()
                return
        elif self.type_combo_box.currentData() == 'gpkg':
            if not configuration.dbfile or self.gpkg_file_line_edit.validator().validate(configuration.dbfile, 0)[0] != QValidator.Acceptable:
                message_error = QCoreApplication.translate("DialogImportSchema", 'Please set a valid database file before creating the LADM-COL structure.')
                self.txtStdout.setText(message_error)
                self.show_message(message_error, Qgis.Warning)
                self.gpkg_file_line_edit.setFocus()
                return

        configuration.dbschema = self.schema_name_line_edit.text().strip().lower()
        self.save_configuration(configuration)

        with OverrideCursor(Qt.WaitCursor):
            self.progress_bar.show()
            self.progress_bar.setValue(0)

            self.disable()
            self.txtStdout.setTextColor(QColor('#000000'))
            self.txtStdout.clear()

            importer = iliimporter.Importer()

            importer.tool_name = 'ili2pg' if self.type_combo_box.currentData() == 'pg' else 'ili2gpkg'
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
                get_java_path_dlg = DialogGetJavaPath()
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
            self.buttonBox.setEnabled(True)
            self.buttonBox.addButton(QDialogButtonBox.Close)
            self.progress_bar.setValue(100)
            self.print_info(QCoreApplication.translate("DialogImportSchema", "\nDone!"), '#004905')
            self.show_message(QCoreApplication.translate("DialogImportSchema", "Creation of the LADM-COL structure was successfully completed"), Qgis.Success)

    def save_configuration(self, configuration):
        settings = QSettings()
        settings.setValue('Asistente-LADM_COL/QgisModelBaker/show_log', not self.log_config.isCollapsed())
        settings.setValue('Asistente-LADM_COL/db_connection_source', self.type_combo_box.currentData())
        if self.type_combo_box.currentData() == 'gpkg':
            settings.setValue('Asistente-LADM_COL/QgisModelBaker/gpkg/dbfile', configuration.dbfile)

    def restore_configuration(self):
        settings = QSettings()
        self.type_combo_box.setCurrentIndex(self.type_combo_box.findData(settings.value('Asistente-LADM_COL/db_connection_source', 'pg')))
        self.type_changed()

        # Show log
        value_show_log = settings.value('Asistente-LADM_COL/QgisModelBaker/show_log', False, type=bool)
        self.log_config.setCollapsed(not value_show_log)

        # set model repository
        # if there is no option  by default use online model repository
        custom_model_is_checked =  settings.value('Asistente-LADM_COL/models/custom_model_directories_is_checked', type=bool)
        self.use_local_models = custom_model_is_checked
        if self.use_local_models:
            self.custom_model_directories = settings.value('Asistente-LADM_COL/models/custom_models') if settings.value('Asistente-LADM_COL/models/custom_models') else None

    def update_configuration(self):
        configuration = SchemaImportConfiguration()

        if self.type_combo_box.currentData() == 'pg':
            # PostgreSQL specific options
            configuration.tool_name = 'pg'
            configuration.dbhost = self.db.dict_conn_params['host']
            configuration.dbport = self.db.dict_conn_params['port']
            configuration.dbusr = self.db.dict_conn_params['username']
            configuration.database = self.db.dict_conn_params['database']
            configuration.dbschema = self.schema_name_line_edit.text().strip().lower()
            configuration.dbpwd = self.db.dict_conn_params['password']
        elif self.type_combo_box.currentData() == 'gpkg':
            configuration.tool_name = 'gpkg'
            configuration.dbfile = self.db.dict_conn_params['dbfile']

        # set custom toml file
        configuration.tomlfile = TOML_FILE_DIR
        configuration.epsg = DEFAULT_EPSG
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
        self.type_combo_box.setEnabled(False)
        self.pg_config.setEnabled(False)
        self.ili_config.setEnabled(False)
        self.buttonBox.setEnabled(False)

    def enable(self):
        self.type_combo_box.setEnabled(True)
        self.pg_config.setEnabled(True)
        self.ili_config.setEnabled(True)
        self.buttonBox.setEnabled(True)

    def show_message(self, message, level):
        self.bar.pushMessage("Asistente LADM_COL", message, level, duration = 0)

    def type_changed(self):
        self.progress_bar.hide()
        if self.type_combo_box.currentData() == 'pg':
            self.pg_config.show()
            self.gpkg_config.hide()
        elif self.type_combo_box.currentData() == 'gpkg':
            self.pg_config.hide()
            self.gpkg_config.show()
            self.gpkg_file_line_edit.setValidator(self.gpkgSaveFileValidator)
            self.gpkg_file_line_edit.textChanged.emit(self.gpkg_file_line_edit.text())
            try:
                self.gpkg_file_browse_button.clicked.disconnect()
            except:
                pass
            self.gpkg_file_browse_button.clicked.connect(
                make_save_file_selector(
                    self.gpkg_file_line_edit,
                    title=QCoreApplication.translate("DialogImportSchema", "Open GeoPackage database file"),
                    file_filter=QCoreApplication.translate("DialogImportSchema", "GeoPackage Database (*.gpkg)"),
                    extension='.gpkg'))
