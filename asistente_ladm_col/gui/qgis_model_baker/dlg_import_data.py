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
import os
import re

from QgisModelBaker.libili2db import iliimporter
from QgisModelBaker.libili2db.ili2dbconfig import (ImportDataConfiguration,
                                                   BaseConfiguration)
from QgisModelBaker.libili2db.ili2dbutils import color_log_text
from QgisModelBaker.libili2db.ilicache import IliCache
from QgisModelBaker.libili2db.iliimporter import JavaNotFoundError
from qgis.PyQt.QtCore import (Qt,
                              QCoreApplication,
                              QSettings)
from qgis.PyQt.QtGui import (QColor,
                             QValidator,
                             QStandardItemModel,
                             QStandardItem)
from qgis.PyQt.QtWidgets import (QDialog,
                                 QSizePolicy,
                                 QListWidgetItem,
                                 QDialogButtonBox)
from qgis.core import Qgis
from qgis.gui import QgsGui
from qgis.gui import QgsMessageBar

from ...config.general_config import (DEFAULT_EPSG,
                                      DEFAULT_INHERITANCE,
                                      DEFAULT_HIDDEN_MODELS,
                                      SETTINGS_CONNECTION_TAB_INDEX,
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

DIALOG_UI = get_ui_class('qgis_model_baker/dlg_import_data.ui')

class DialogImportData(QDialog, DIALOG_UI):
    def __init__(self, iface, db, qgis_utils):
        QDialog.__init__(self)
        self.setupUi(self)
        QgsGui.instance().enableAutoGeometryRestore(self)
        self.iface = iface
        self.db = db
        self.qgis_utils = qgis_utils
        self.base_configuration = BaseConfiguration()

        self.ilicache = IliCache(self.base_configuration)
        self.ilicache.refresh()

        self.type_combo_box.clear()
        self.type_combo_box.addItem(QCoreApplication.translate("DialogImportData", 'PostgreSQL/PostGIS'), 'ili2pg')
        self.type_combo_box.addItem(QCoreApplication.translate("DialogImportData", 'GeoPackage'), 'ili2gpkg')
        self.type_combo_box.currentIndexChanged.connect(self.type_changed)
        self.type_changed()

        self.xtf_file_browse_button.clicked.connect(
            make_file_selector(self.xtf_file_line_edit, title=QCoreApplication.translate("DialogImportData",'Open Transfer or Catalog File'),
                               file_filter=QCoreApplication.translate("DialogImportData",'Transfer File (*.xtf *.itf);;Catalogue File (*.xml *.xls *.xlsx)')))

        self.validators = Validators()
        self.xtf_file_line_edit.setPlaceholderText(QCoreApplication.translate("DialogImportData", "[Name of the XTF to be created]"))
        fileValidator = FileValidator(pattern=['*.xtf', '*.itf', '*.xml'])
        self.xtf_file_line_edit.setValidator(fileValidator)
        self.xtf_file_line_edit.textChanged.connect(self.update_import_models)
        self.xtf_file_line_edit.textChanged.emit(self.xtf_file_line_edit.text())

        # PG
        self.db_connect_label.setToolTip(self.db.get_display_conn_string())
        self.db_connect_label.setText(self.db.dict_conn_params["database"])
        self.connection_setting_button.clicked.connect(self.show_settings)

        self.connection_setting_button.setText(QCoreApplication.translate("DialogImportData", 'Connection Settings'))

        # GPKG
        self.gpkg_file_line_edit.setPlaceholderText(QCoreApplication.translate("DialogImportData", "[Name of the Geopackage to be created]"))

        self.gpkg_file_browse_button.clicked.connect(
            make_save_file_selector(self.gpkg_file_line_edit, title=QCoreApplication.translate("DialogImportData",'Save in GeoPackage database file'),
                                    file_filter=QCoreApplication.translate("DialogImportData",'GeoPackage Database (*.gpkg)'), extension='.gpkg'))

        gpkgFileValidator = FileValidator(pattern='*.gpkg', allow_non_existing=True)
        self.gpkg_file_line_edit.setValidator(gpkgFileValidator)

        self.gpkgSaveFileValidator = FileValidator(pattern='*.gpkg', allow_non_existing=True)
        self.gpkgOpenFileValidator = FileValidator(pattern='*.gpkg')
        self.gpkg_file_line_edit.textChanged.connect(self.validators.validate_line_edits)
        self.gpkg_file_line_edit.textChanged.emit(self.gpkg_file_line_edit.text())

        # LOG
        self.log_config.setTitle(QCoreApplication.translate("DialogImportData", "Show log"))

        self.bar = QgsMessageBar()
        self.bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.layout().addWidget(self.bar, 0, 0, Qt.AlignTop)

        self.buttonBox.accepted.disconnect()
        self.buttonBox.accepted.connect(self.accepted)
        self.buttonBox.clear()
        self.buttonBox.addButton(QDialogButtonBox.Cancel)
        self.buttonBox.addButton(QCoreApplication.translate("DialogImportData", "Import data"), QDialogButtonBox.AcceptRole)
        self.buttonBox.addButton(QDialogButtonBox.Help)
        self.buttonBox.helpRequested.connect(self.show_help)

    def showEvent(self, event):
        self.update_schema_names_model()
        self.restore_configuration()

    def update_import_models(self):

        message_error = None

        if not self.xtf_file_line_edit.text().strip():
            color = '#ffd356'  # Light orange
            self.import_models_qmodel = QStandardItemModel()
            self.import_models_list_view.setModel(self.import_models_qmodel)
        else:

            if os.path.isfile(self.xtf_file_line_edit.text().strip()):
                color = '#fff'  # White

                self.import_models_qmodel = QStandardItemModel()
                models_name = self.find_models_xtf(self.xtf_file_line_edit.text().strip())

                for model_name in models_name:
                    if not model_name in DEFAULT_HIDDEN_MODELS:
                        item = QStandardItem(model_name)
                        item.setCheckable(False)
                        item.setEditable(False)
                        self.import_models_qmodel.appendRow(item)

                if self.import_models_qmodel.rowCount() > 0:
                    self.import_models_list_view.setModel(self.import_models_qmodel)
                else:
                    message_error = QCoreApplication.translate("DialogImportData",
                                                               "No models were found in the XTF. Is it a valid file?")
                    color = '#ffd356'  # Light orange
                    self.import_models_qmodel = QStandardItemModel()
                    self.import_models_list_view.setModel(self.import_models_qmodel)
            else:
                message_error = QCoreApplication.translate("DialogImportData", "Please set a valid XTF file")
                color = '#ffd356'  # Light orange
                self.import_models_qmodel = QStandardItemModel()
                self.import_models_list_view.setModel(self.import_models_qmodel)
        self.xtf_file_line_edit.setStyleSheet('QLineEdit {{ background-color: {} }}'.format(color))

        if message_error:
            self.txtStdout.setText(message_error)
            self.show_message(message_error, Qgis.Warning)
            self.import_models_list_view.setFocus()
            return

    def find_models_xtf(self, xtf_path):
        models_name = list()
        pattern = re.compile(r'<MODEL[^>]*>(?P<text>[^<]*)</MODEL>')
        with open(xtf_path, 'r') as f:
            for txt in pattern.finditer(f.read()):
                model_tag = str(txt.group(0))
                name = re.findall('NAME="(.*?)"', model_tag, re.IGNORECASE)
                models_name.extend(name)
        return models_name


    def update_schema_names_model(self):
        res, msg = self.db.test_connection()
        schema_names = self.db._schema_names_list()
        self.schema_names_list_widget.clear()

        if schema_names:
            for schema_name in schema_names:
                item = QListWidgetItem(schema_name['schema_name'])
                item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
                item.setCheckState(Qt.Unchecked)
                self.schema_names_list_widget.addItem(item)

            default_item = self.schema_names_list_widget.item(0)
            default_item.setCheckState(Qt.Checked)
        else:
            message_error = "There are no schemata to import into the database. Select another database."
            self.txtStdout.setText(QCoreApplication.translate("DialogImportData", message_error))
            self.show_message(message_error, Qgis.Warning)

        self.schema_names_list_widget.currentRowChanged.connect(self.on_current_row_changed_schema_names)
        self.schema_names_list_widget.itemChanged.connect(self.on_itemchanged_schema_name)

    def on_itemchanged_schema_name(self, selected_item):
        # disconnect signal to do changes in the items
        self.schema_names_list_widget.itemChanged.disconnect(self.on_itemchanged_schema_name)

        for index in range(self.schema_names_list_widget.count()):
            item = self.schema_names_list_widget.item(index)
            item.setCheckState(Qt.Unchecked)
            item.setSelected(False)
            if item == selected_item:
                select_index = index

        item = self.schema_names_list_widget.item(select_index)
        item.setCheckState(Qt.Checked)
        item.setSelected(True)

        # connect signal to check when the items change
        self.schema_names_list_widget.itemChanged.connect(self.on_itemchanged_schema_name)


    def on_current_row_changed_schema_names(self, current_row):
        for index in range(self.schema_names_list_widget.count()):
            item = self.schema_names_list_widget.item(index)
            item.setCheckState(Qt.Unchecked)

        item = self.schema_names_list_widget.item(current_row)
        if item:
            item.setCheckState(Qt.Checked)

    def get_checked_schema(self):
        checked_schema = None
        for index in range(self.schema_names_list_widget.count()):
            item = self.schema_names_list_widget.item(index)
            if item.checkState() == Qt.Checked:
                checked_schema = item.text()
                break
        return checked_schema

    def get_ili_models(self):
        ili_models = list()
        for index in range(self.import_models_qmodel.rowCount()):
            item = self.import_models_qmodel.item(index)
            ili_models.append(item.text())
        return ili_models

    def show_settings(self):
        dlg = self.qgis_utils.get_settings_dialog()
        dlg.tabWidget.setCurrentIndex(SETTINGS_CONNECTION_TAB_INDEX)
        if dlg.exec_():
            self.db = self.qgis_utils.get_db_connection()
            self.db_connect_label.setToolTip(self.db.get_display_conn_string())
            self.db_connect_label.setText(self.db.dict_conn_params["database"])
            self.update_schema_names_model()

    def accepted(self):
        configuration = self.update_configuration()

        if not os.path.isfile(self.xtf_file_line_edit.text().strip()):
            message_error = 'Please set a valid XTF file before importing data. XTF file does not exist'
            self.txtStdout.setText(QCoreApplication.translate("DialogImportData", message_error))
            self.show_message(message_error, Qgis.Warning)
            self.xtf_file_line_edit.setFocus()
            return


        if not self.xtf_file_line_edit.validator().validate(configuration.xtffile, 0)[0] == QValidator.Acceptable:
            message_error = 'Please set a valid XTF before importing data.'
            self.txtStdout.setText(QCoreApplication.translate("DialogImportData", message_error))
            self.show_message(message_error, Qgis.Warning)
            self.xtf_file_line_edit.setFocus()
            return

        if not self.get_ili_models():
            message_error = QCoreApplication.translate("DialogImportData", "The selected XTF file does not have information according to the LADM-COL model to import.")
            self.txtStdout.setText(message_error)
            self.show_message(message_error, Qgis.Warning)
            self.import_models_list_view.setFocus()
            return

        if self.type_combo_box.currentData() == 'ili2gpkg':
            if not configuration.dbfile or self.gpkg_file_line_edit.validator().validate(configuration.dbfile, 0)[0] != QValidator.Acceptable:
                message_error = QCoreApplication.translate("DialogImportData", "Please set a valid database file before creating the project.")
                self.txtStdout.setText(message_error)
                self.show_message(message_error, Qgis.Warning)
                self.gpkg_file_line_edit.setFocus()
                return
            
        with OverrideCursor(Qt.WaitCursor):
            self.progress_bar.show()
            self.progress_bar.setValue(0)

            self.disable()
            self.txtStdout.setTextColor(QColor('#000000'))
            self.txtStdout.clear()

            dataImporter = iliimporter.Importer(dataImport=True)

            dataImporter.tool_name = self.type_combo_box.currentData()
            dataImporter.configuration = configuration

            self.save_configuration(configuration)

            dataImporter.stdout.connect(self.print_info)
            dataImporter.stderr.connect(self.on_stderr)
            dataImporter.process_started.connect(self.on_process_started)
            dataImporter.process_finished.connect(self.on_process_finished)

            self.progress_bar.setValue(25)

            try:
                if dataImporter.run() != iliimporter.Importer.SUCCESS:
                    self.enable()
                    self.progress_bar.hide()
                    self.show_message(QCoreApplication.translate("DialogImportData", "An error occurred when importing the data. For more information see the log..."), Qgis.Warning)
                    return
            except JavaNotFoundError:

                # Set JAVA PATH
                get_java_path_dlg = DialogGetJavaPath()
                get_java_path_dlg.setModal(True)
                if get_java_path_dlg.exec_():
                    configuration = self.update_configuration()

                if not get_java_path_from_qgis_model_baker():
                    message_error_java = QCoreApplication.translate("DialogExportData", "Java could not be found. Please <a href=\"https://java.com/en/download/\">install Java</a> and or <a href=\"#configure\">configure a custom java path</a>. We also support the JAVA_HOME environment variable in case you prefer this.")
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
            self.show_message(QCoreApplication.translate("DialogImportData", "Import of the data was successfully completed"), Qgis.Success)

    def save_configuration(self, configuration):
        settings = QSettings()
        settings.setValue('Asistente-LADM_COL/QgisModelBaker/ili2pg/xtffile_import', configuration.xtffile)
        settings.setValue('Asistente-LADM_COL/QgisModelBaker/importtype', self.type_combo_box.currentData())
        settings.setValue('Asistente-LADM_COL/QgisModelBaker/show_log', not self.log_config.isCollapsed())

        if self.type_combo_box.currentData() == 'ili2gpkg':
            settings.setValue('Asistente-LADM_COL/QgisModelBaker/ili2gpkg/dbfile', configuration.dbfile)

    def restore_configuration(self):
        settings = QSettings()
        self.xtf_file_line_edit.setText(settings.value('Asistente-LADM_COL/QgisModelBaker/ili2pg/xtffile_import'))
        self.type_combo_box.setCurrentIndex(self.type_combo_box.findData(settings.value('Asistente-LADM_COL/QgisModelBaker/importtype', 'ili2pg')))
        self.type_changed()

        # Show log
        value_show_log = settings.value('Asistente-LADM_COL/QgisModelBaker/show_log', False, type=bool)
        self.log_config.setCollapsed(not value_show_log)

        # set model repository
        # if there is no option  by default use online model repository
        self.use_local_models = settings.value('Asistente-LADM_COL/models/custom_model_directories_is_checked', type=bool)
        if self.use_local_models:
            self.custom_model_directories = settings.value('Asistente-LADM_COL/models/custom_models') if settings.value('Asistente-LADM_COL/models/custom_models') else None

    def update_configuration(self):
        """
        Get the configuration that is updated with the user configuration changes on the dialog.
        :return: Configuration
        """
        configuration = ImportDataConfiguration()

        if self.type_combo_box.currentData() == 'ili2pg':
            # PostgreSQL specific options
            configuration.dbhost = self.db.dict_conn_params['host']
            configuration.dbport = self.db.dict_conn_params['port']
            configuration.dbusr = self.db.dict_conn_params['username']
            configuration.database = self.db.dict_conn_params['database']
            configuration.dbschema = self.get_checked_schema()
            configuration.dbpwd = self.db.dict_conn_params['password']
        elif self.type_combo_box.currentData() == 'ili2gpkg':
            configuration.dbfile = self.db.dict_conn_params['dbfile']

        configuration.xtffile = self.xtf_file_line_edit.text().strip()
        configuration.delete_data = False

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
        if self.get_ili_models():
            configuration.ilimodels = ';'.join(self.get_ili_models())

        return configuration

    def print_info(self, text, text_color='#000000', clear=False):
        self.txtStdout.setTextColor(QColor(text_color))
        self.txtStdout.append(text)
        QCoreApplication.processEvents()

    def on_stderr(self, text):
        color_log_text(text, self.txtStdout)
        self.advance_progress_bar_by_text(text)
        QCoreApplication.processEvents()

    def on_process_started(self, command):
        self.disable()
        self.txtStdout.setTextColor(QColor('#000000'))
        self.txtStdout.clear()
        self.txtStdout.setText(command)
        QCoreApplication.processEvents()

    def on_process_finished(self, exit_code, result):
        color = '#004905' if exit_code == 0 else '#aa2222'
        self.txtStdout.setTextColor(QColor(color))
        self.txtStdout.append('Finished ({})'.format(exit_code))
        if result == iliimporter.Importer.SUCCESS:
            self.buttonBox.clear()
            self.buttonBox.setEnabled(True)
            self.buttonBox.addButton(QDialogButtonBox.Close)
        else:
            self.show_message(QCoreApplication.translate("DialogImportData", "Error when importing data"), Qgis.Warning)
            self.enable()

    def advance_progress_bar_by_text(self, text):
        if text.strip() == 'Info: compile models...':
            self.progress_bar.setValue(50)
            QCoreApplication.processEvents()
        elif text.strip() == 'Info: create table structure...':
            self.progress_bar.setValue(75)
            QCoreApplication.processEvents()

    def show_help(self):
        self.qgis_utils.show_help("import_data")

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
        self.bar.pushMessage("Asistente LADM_COL", message, level, duration=0)

    def type_changed(self):
        self.progress_bar.hide()
        if self.type_combo_box.currentData() == 'ili2pg':
            self.pg_config.show()
            self.gpkg_config.hide()
        elif self.type_combo_box.currentData() == 'ili2gpkg':
            self.pg_config.hide()
            self.gpkg_config.show()
