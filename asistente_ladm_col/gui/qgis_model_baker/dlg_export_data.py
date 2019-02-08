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

from QgisModelBaker.libili2db import iliexporter
from QgisModelBaker.libili2db.ili2dbconfig import (ExportConfiguration,
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
                                 QMessageBox,
                                 QDialogButtonBox)
from qgis.core import Qgis
from qgis.gui import QgsGui
from qgis.gui import QgsMessageBar

from ...config.general_config import (DEFAULT_HIDDEN_MODELS,
                                      SETTINGS_CONNECTION_TAB_INDEX)
from ...utils import get_ui_class
from ...utils.qt_utils import (Validators,
                               FileValidator,
                               make_save_file_selector,
                               make_file_selector,
                               OverrideCursor)
from ...resources_rc import *

DIALOG_UI = get_ui_class('qgis_model_baker/dlg_export_data.ui')

class DialogExportData(QDialog, DIALOG_UI):
    ValidExtensions = ['xtf', 'itf', 'gml', 'xml']
    current_row_schema = 0
    
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
        self.type_combo_box.addItem(QCoreApplication.translate('DialogExportData','PostgreSQL/PostGIS'), 'ili2pg')
        self.type_combo_box.addItem(QCoreApplication.translate('DialogExportData','GeoPackage'), 'ili2gpkg')
        self.type_combo_box.currentIndexChanged.connect(self.type_changed)
        self.type_changed()

        self.xtf_file_browse_button.clicked.connect(
            make_save_file_selector(self.xtf_file_line_edit, title=QCoreApplication.translate('DialogExportData','Save in XTF Transfer File'),
                                    file_filter=QCoreApplication.translate('DialogExportData','XTF Transfer File (*.xtf);;Interlis 1 Transfer File (*.itf);;XML (*.xml);;GML (*.gml)'), extension='.xtf', extensions=['.' + ext for ext in self.ValidExtensions]))
        self.xtf_file_browse_button.clicked.connect(self.xtf_browser_opened_to_true)
        self.xtf_browser_was_opened = False
        
        self.validators = Validators()
        fileValidator = FileValidator(pattern=['*.' + ext for ext in self.ValidExtensions], allow_non_existing=True)
        self.xtf_file_line_edit.setPlaceholderText(QCoreApplication.translate('DialogExportData', "[Name of the XTF to be created]"))
        self.xtf_file_line_edit.setValidator(fileValidator)
        self.xtf_file_line_edit.textChanged.connect(self.validators.validate_line_edits)
        self.xtf_file_line_edit.textChanged.connect(self.xtf_browser_opened_to_false)
        self.xtf_file_line_edit.textChanged.emit(self.xtf_file_line_edit.text())

        # PG
        self.db_connect_label.setToolTip(self.db.get_display_conn_string())
        self.db_connect_label.setText(self.db.dict_conn_params["database"])
        self.connection_setting_button.clicked.connect(self.show_settings)

        self.connection_setting_button.setText(QCoreApplication.translate('DialogExportData', 'Connection Settings'))

        # GPKG
        self.gpkg_file_line_edit.setPlaceholderText(QCoreApplication.translate('DialogExportData', "[Name of the Geopackage to be created]"))
        self.gpkg_file_browse_button.clicked.connect(make_file_selector(self.gpkg_file_line_edit, title=QCoreApplication.translate('DialogExportData','Open GeoPackage database file'),file_filter=QCoreApplication.translate('DialogExportData','GeoPackage Database (*.gpkg)')))
        gpkgFileValidator = FileValidator(pattern='*.gpkg')
        self.gpkg_file_line_edit.setValidator(gpkgFileValidator)
        self.gpkg_file_line_edit.textChanged.connect(self.validators.validate_line_edits)
        self.gpkg_file_line_edit.textChanged.emit(self.gpkg_file_line_edit.text())

        # LOG
        self.log_config.setTitle(QCoreApplication.translate('DialogExportData', 'Show log'))
        self.log_config.setFlat(True)

        self.bar = QgsMessageBar()
        self.bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.layout().addWidget(self.bar, 0, 0, Qt.AlignTop)

        self.buttonBox.accepted.disconnect()
        self.buttonBox.accepted.connect(self.accepted)
        self.buttonBox.clear()
        self.buttonBox.addButton(QDialogButtonBox.Cancel)
        self.buttonBox.addButton(QCoreApplication.translate('DialogExportData', 'Export data'), QDialogButtonBox.AcceptRole)
        self.buttonBox.addButton(QDialogButtonBox.Help)
        self.buttonBox.helpRequested.connect(self.show_help)

    def showEvent(self, event):
        # update after create dialog
        self.update_schema_names_model()
        self.update_model_names(self.get_checked_schema())
        self.restore_configuration()

    def update_schema_names_model(self):
        res, msg = self.db.test_connection()
        schema_names = self.db._schema_names_list()

        if schema_names:
            for schema_name in schema_names:
                item = QListWidgetItem(schema_name['schema_name'])
                item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
                item.setCheckState(Qt.Unchecked)
                self.schema_names_list_widget.addItem(item)

            default_item = self.schema_names_list_widget.item(0)
            default_item.setCheckState(Qt.Checked)
        else:
            self.schema_names_list_widget.clear()
            self.export_models_list_view.setModel(QStandardItemModel())
            message_error = 'There are no schemes to export into the database. Please select another database.'
            self.txtStdout.setText(QCoreApplication.translate('DialogExportData', message_error))
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

        # Update list view with models name info
        schema_name = item.text()
        self.update_model_names(schema_name)

        # connect signal to check when the items change
        self.schema_names_list_widget.itemChanged.connect(self.on_itemchanged_schema_name)

    def on_current_row_changed_schema_names(self, current_row):
        for index in range(self.schema_names_list_widget.count()):
            item = self.schema_names_list_widget.item(index)
            item.setCheckState(Qt.Unchecked)

        item = self.schema_names_list_widget.item(current_row)

        if item:
            item.setCheckState(Qt.Checked)
            # Update list view with models name info
            schema_name = item.text()
            self.update_model_names(schema_name)

    def update_model_names(self, dbschema):
        self.export_models_qmodel = QStandardItemModel()

        db_models = None
        if self.type_combo_box.currentData() == 'ili2gpkg':
            db_models = self.db.get_models()
        elif self.type_combo_box.currentData() == 'ili2pg':
            db_models = self.db.get_models(dbschema) if dbschema else None

        if db_models:
            for db_model in db_models:
                regex = re.compile(r'(?:\{[^\}]*\}|\s)')
                for modelname in regex.split(db_model['modelname']):
                    if modelname and modelname not in DEFAULT_HIDDEN_MODELS:
                        item = QStandardItem(modelname.strip())
                        item.setCheckable(False)
                        item.setEditable(False)
                        self.export_models_qmodel.appendRow(item)

        self.export_models_list_view.setModel(self.export_models_qmodel)

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
        for index in range(self.export_models_qmodel.rowCount()):
            item = self.export_models_qmodel.item(index)
            ili_models.append(item.text())
        return ili_models

    def show_settings(self):
        dlg = self.qgis_utils.get_settings_dialog()
        dlg.tabWidget.setCurrentIndex(SETTINGS_CONNECTION_TAB_INDEX)
        if dlg.exec_():
            self.db = self.qgis_utils.get_db_connection()
            self.db_connect_label.setToolTip(self.db.get_display_conn_string())
            self.db_connect_label.setText(self.db.dict_conn_params['database'])
            self.update_schema_names_model()

    def accepted(self):
        configuration = self.update_configuration()

        if not self.get_checked_schema():
            message_error = QCoreApplication.translate('DialogExportData', 'You need to select a valid schema where to get the data from.')
            self.txtStdout.setText(message_error)
            self.show_message(message_error, Qgis.Warning)
            self.connection_setting_button.setFocus()
            return

        if not self.xtf_file_line_edit.validator().validate(configuration.xtffile, 0)[0] == QValidator.Acceptable:
            message_error = QCoreApplication.translate('DialogExportData', 'Please set a valid XTF file before exporting data.')
            self.txtStdout.setText(message_error)
            self.show_message(message_error, Qgis.Warning)
            self.xtf_file_line_edit.setFocus()
            return

        if not self.get_ili_models():
            message_error = QCoreApplication.translate('DialogExportData','Please set a valid schema to export. This schema does not have information to export.')
            self.txtStdout.setText(message_error)
            self.show_message(message_error, Qgis.Warning)
            self.export_models_list_view.setFocus()
            return
        
        if not configuration.iliexportmodels:
            message_error = QCoreApplication.translate('DialogExportData','Please set a model before exporting data.')
            self.txtStdout.setText(message_error)
            self.show_message(message_error, Qgis.Warning)
            self.export_models_list_view.setFocus()
            return

        if self.type_combo_box.currentData() == 'ili2gpkg':
            if not configuration.dbfile or self.gpkg_file_line_edit.validator().validate(configuration.dbfile, 0)[0] != QValidator.Acceptable:
                message_error = QCoreApplication.translate('DialogExportData', 'Please set an existing database file before creating the project.')
                self.txtStdout.setText(message_error)
                self.show_message(message_error, Qgis.Warning)
                self.gpkg_file_line_edit.setFocus()
                return

        # If xtf browser was opened and the file exists, the user already chose
        # to overwrite the file
        if os.path.isfile(self.xtf_file_line_edit.text().strip()) and not self.xtf_browser_was_opened:
            self.msg = QMessageBox()
            self.msg.setIcon(QMessageBox.Warning)
            self.msg.setText(QCoreApplication.translate('DialogExportData',"{filename} already exists.\nDo you want to replace it?").format(filename=os.path.basename(self.xtf_file_line_edit.text().strip())))
            self.msg.setWindowTitle(QCoreApplication.translate('DialogExportData',"Save in XTF Transfer File"))
            self.msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg_box = self.msg.exec_()
            if msg_box == QMessageBox.No:
                return
            
        with OverrideCursor(Qt.WaitCursor):
            self.progress_bar.show()
            self.progress_bar.setValue(0)

            self.disable()
            self.txtStdout.setTextColor(QColor('#000000'))
            self.txtStdout.clear()

            exporter = iliexporter.Exporter()

            exporter.tool_name = self.type_combo_box.currentData()
            exporter.configuration = configuration

            self.save_configuration(configuration)

            exporter.stdout.connect(self.print_info)
            exporter.stderr.connect(self.on_stderr)
            exporter.process_started.connect(self.on_process_started)
            exporter.process_finished.connect(self.on_process_finished)

            self.progress_bar.setValue(25)

            try:
                if exporter.run() != iliexporter.Exporter.SUCCESS:
                    self.enable()
                    self.progress_bar.hide()
                    self.show_message(QCoreApplication.translate('DialogExportData', 'An error occurred when exporting the data. For more information see the log...'), Qgis.Warning)
                    return
            except JavaNotFoundError:
                self.txtStdout.setTextColor(QColor('#000000'))
                self.txtStdout.clear()
                self.txtStdout.setText(QCoreApplication.translate('DialogExportData','Java could not be found. Please <a href="https://java.com/en/download/">install Java</a> and or <a href="#configure">configure a custom java path</a>. We also support the JAVA_HOME environment variable in case you prefer this.'))
                self.enable()
                self.progress_bar.hide()
                return

            self.buttonBox.clear()
            self.buttonBox.setEnabled(True)
            self.buttonBox.addButton(QDialogButtonBox.Close)
            self.progress_bar.setValue(100)
            self.show_message(QCoreApplication.translate('DialogExportData', 'Export of the data was successfully completed.') , Qgis.Success)

    def save_configuration(self, configuration):
        settings = QSettings()
        settings.setValue('Asistente-LADM_COL/QgisModelBaker/ili2pg/xtffile_export', configuration.xtffile)
        settings.setValue('Asistente-LADM_COL/QgisModelBaker/importtype', self.type_combo_box.currentData())
        settings.setValue('Asistente-LADM_COL/QgisModelBaker/show_log', not self.log_config.isCollapsed())

        if self.type_combo_box.currentData() == 'ili2gpkg':
            settings.setValue('Asistente-LADM_COL/QgisModelBaker/ili2gpkg/dbfile', configuration.dbfile)

    def restore_configuration(self):
        settings = QSettings()
        self.xtf_file_line_edit.setText(settings.value('Asistente-LADM_COL/QgisModelBaker/ili2pg/xtffile_export'))
        self.type_combo_box.setCurrentIndex(self.type_combo_box.findData(settings.value('Asistente-LADM_COL/QgisModelBaker/importtype', 'ili2pg')))
        self.type_changed()

        # Show log
        value_show_log = settings.value('Asistente-LADM_COL/QgisModelBaker/show_log', False, type=bool)
        self.log_config.setCollapsed(not value_show_log)

        # set model repository
        # if there is no option by default use online model repository
        custom_model_is_checked =  settings.value('Asistente-LADM_COL/models/custom_model_directories_is_checked', type=bool)
        if custom_model_is_checked:
            self.custom_model_directories = settings.value('Asistente-LADM_COL/models/custom_models')

    def update_configuration(self):
        """
        Get the configuration that is updated with the user configuration changes on the dialog.
        :return: Configuration
        """
        configuration = ExportConfiguration()

        if self.type_combo_box.currentData() == 'ili2pg':
            # PostgreSQL specific options
            configuration.dbhost = self.db.dict_conn_params["host"]
            configuration.dbport = self.db.dict_conn_params["port"]
            configuration.dbusr = self.db.dict_conn_params["username"]
            configuration.database = self.db.dict_conn_params["database"]
            configuration.dbschema = self.get_checked_schema()
            configuration.dbpwd = self.db.dict_conn_params["password"]
        elif self.type_combo_box.currentData() == 'ili2gpkg':
            configuration.dbfile = self.db.dict_conn_params["dbfile"]

        configuration.xtffile = self.xtf_file_line_edit.text().strip()

        # Check custom model directories
        if QSettings().value('Asistente-LADM_COL/models/custom_model_directories_is_checked', type=bool):
            if self.custom_model_directories is None:
                self.base_configuration.custom_model_directories_enabled = False
            else:
                self.base_configuration.custom_model_directories = self.custom_model_directories
                self.base_configuration.custom_model_directories_enabled = True

        configuration.base_configuration = self.base_configuration
        if self.get_ili_models():
            configuration.iliexportmodels = ';'.join(self.get_ili_models())
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
        self.txtStdout.append(QCoreApplication.translate('DialogExportData','Finished ({})'.format(exit_code)))
        if result == iliexporter.Exporter.SUCCESS:
            self.buttonBox.clear()
            self.buttonBox.setEnabled(True)
            self.buttonBox.addButton(QDialogButtonBox.Close)
        else:
            self.enable()

    def advance_progress_bar_by_text(self, text):
        if text.strip() == 'Info: compile models...':
            self.progress_bar.setValue(50)
            QCoreApplication.processEvents()
        elif text.strip() == 'Info: create table structure...':
            self.progress_bar.setValue(75)
            QCoreApplication.processEvents()

    def show_help(self):
        self.qgis_utils.show_help("export_data")

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

    def xtf_browser_opened_to_true(self):
        """
        Slot. Sets a flag to true to eventually avoid asking a user whether to overwrite a file.
        """
        self.xtf_browser_was_opened = True

    def xtf_browser_opened_to_false(self):
        """
        Slot. Sets a flag to false to eventually ask a user whether to overwrite a file.
        """
        self.xtf_browser_was_opened = False
