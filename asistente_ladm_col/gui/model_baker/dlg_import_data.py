# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2018-06-11
        git sha              : :%H$
        copyright            : (C) 2018 by Germán Carrillo (BSF Swissphoto)
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
from xml.dom import minidom
from xml.parsers.expat import ExpatError

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
                                      DEFAULT_HIDDEN_MODELS)
from ...utils import get_ui_class
from ...utils.qt_utils import (Validators,
                               FileValidator,
                               make_file_selector,
                               make_save_file_selector,
                               OverrideCursor)
from ...resources_rc import *

DIALOG_UI = get_ui_class('model_baker/dlg_import_data.ui')

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
        self.type_combo_box.addItem(QCoreApplication.translate('DialogImportData','Use PostgreSQL/PostGIS'), 'ili2pg')
        self.type_combo_box.addItem(QCoreApplication.translate('DialogImportData','Use GeoPackage)'), 'ili2gpkg')
        self.type_combo_box.currentIndexChanged.connect(self.type_changed)
        self.type_changed()

        self.xtf_file_browse_button.clicked.connect(
            make_file_selector(self.xtf_file_line_edit, title=QCoreApplication.translate('DialogImportData','Open Transfer or Catalog File'),
                               file_filter=QCoreApplication.translate('DialogImportData','Transfer File (*.xtf *.itf);;Catalogue File (*.xml *.xls *.xlsx)')))

        self.validators = Validators()
        self.xtf_file_line_edit.setPlaceholderText(QCoreApplication.translate('DialogImportData', "[Name of the XTF to be created]"))
        fileValidator = FileValidator(pattern=['*.xtf', '*.itf', '*.xml'])
        self.xtf_file_line_edit.setValidator(fileValidator)
        self.xtf_file_line_edit.textChanged.connect(self.update_import_models)
        self.xtf_file_line_edit.textChanged.emit(self.xtf_file_line_edit.text())

        # PG
        self.db_connect_label.setToolTip(self.db.get_uri_without_password())
        self.db_connect_label.setText(self.db.dbname)
        self.connection_setting_button.clicked.connect(self.show_settings)

        self.connection_setting_button.setText(QCoreApplication.translate('DialogImportData', 'Connection Settings'))

        # GPKG
        self.gpkg_file_line_edit.setPlaceholderText(QCoreApplication.translate('DialogImportData', "[Name of the Geopackage to be created]"))

        self.gpkg_file_browse_button.clicked.connect(
            make_save_file_selector(self.gpkg_file_line_edit, title=QCoreApplication.translate('DialogImportData','Save in GeoPackage database file'),
                                    file_filter=QCoreApplication.translate('DialogImportData','GeoPackage Database (*.gpkg)'), extension='.gpkg'))

        gpkgFileValidator = FileValidator(pattern='*.gpkg', allow_non_existing=True)
        self.gpkg_file_line_edit.setValidator(gpkgFileValidator)

        self.gpkgSaveFileValidator = FileValidator(pattern='*.gpkg', allow_non_existing=True)
        self.gpkgOpenFileValidator = FileValidator(pattern='*.gpkg')
        self.gpkg_file_line_edit.textChanged.connect(self.validators.validate_line_edits)
        self.gpkg_file_line_edit.textChanged.emit(self.gpkg_file_line_edit.text())
        self.restore_configuration()

        # LOG
        self.log_config.setTitle(QCoreApplication.translate('DialogImportData', 'Show log'))

        self.bar = QgsMessageBar()
        self.bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.layout().addWidget(self.bar, 0, 0, Qt.AlignTop)

        self.buttonBox.accepted.disconnect()
        self.buttonBox.accepted.connect(self.accepted)
        self.buttonBox.clear()
        self.buttonBox.addButton(QDialogButtonBox.Cancel)
        self.buttonBox.addButton(QCoreApplication.translate('DialogImportData', 'Import data'), QDialogButtonBox.AcceptRole)
        self.buttonBox.addButton(QDialogButtonBox.Help)
        self.buttonBox.helpRequested.connect(self.show_help)

    def showEvent(self, event):
        self.update_schema_names_model()

    def update_import_models(self):

        message_error = None

        if not self.xtf_file_line_edit.text().strip():
            color = '#ffd356'  # Light orange
            self.import_models_qmodel = QStandardItemModel()
            self.import_models_list_view.setModel(self.import_models_qmodel)
        else:

            try:
                mydoc = minidom.parse(self.xtf_file_line_edit.text().strip())
                upper_models = mydoc.getElementsByTagName('MODEL')
                lower_models = mydoc.getElementsByTagName('model')

                models = list()
                models.extend([model for model in upper_models])
                models.extend([model for model in lower_models])

                is_valid_xtf = True if len(models) > 0 else False

            except ExpatError:
                is_valid_xtf = False

            if is_valid_xtf:
                color = '#fff'  # White
                self.import_models_qmodel = QStandardItemModel()
                for model in models:
                    try:
                        u_model_name = model.attributes['NAME'].value
                    except KeyError:
                        # attribute not available
                        u_model_name = None
                        pass

                    try:
                        l_model_name = model.attributes['name'].value
                    except KeyError:
                        # attribute not available
                        l_model_name = None
                        pass

                    if u_model_name or l_model_name:
                        model_name = u_model_name if u_model_name and len(u_model_name) > 0 else l_model_name

                        if not model_name in DEFAULT_HIDDEN_MODELS:
                            item = QStandardItem(model_name)
                            item.setCheckable(False)
                            item.setEditable(False)
                            self.import_models_qmodel.appendRow(item)

                if self.import_models_qmodel.rowCount() > 0:
                    self.import_models_list_view.setModel(self.import_models_qmodel)
                else:
                    message_error = QCoreApplication.translate('DialogImportData', 'The XTF file does not register ili models, please verify')
                    color = '#f6989d'  # Red
                    self.import_models_qmodel = QStandardItemModel()
                    self.import_models_list_view.setModel(self.import_models_qmodel)

            else:
                message_error = QCoreApplication.translate('DialogImportData', 'Please set a valid XTF file')
                color = '#f6989d'  # Red
                self.import_models_qmodel = QStandardItemModel()
                self.import_models_list_view.setModel(self.import_models_qmodel)

        self.xtf_file_line_edit.setStyleSheet('QLineEdit {{ background-color: {} }}'.format(color))

        if message_error:
            self.txtStdout.setText(message_error)
            self.show_message(message_error, Qgis.Warning)
            self.import_models_list_view.setFocus()
            return

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
            message_error = 'There are no schemes to import into the database. Please select another database.'
            self.txtStdout.setText(QCoreApplication.translate('DialogImportData', message_error))
            self.show_message(message_error, Qgis.Warning)
            # try:
            #     self.show_message(message_error, Qgis.Warning)
            # except AttributeError:
            #     pass

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
        self.qgis_utils.get_settings_dialog().exec_()
        self.db = self.qgis_utils.get_db_connection()
        self.db_connect_label.setToolTip(self.db.get_uri_without_password())
        self.db_connect_label.setText(self.db.dbname)
        self.update_schema_names_model()

    def accepted(self):

        configuration = self.updated_configuration()

        if not self.xtf_file_line_edit.validator().validate(configuration.xtffile, 0)[0] == QValidator.Acceptable:
            message_error = 'Please set a valid model before importing data.'
            self.txtStdout.setText(QCoreApplication.translate('DialogImportData',message_error))
            self.show_message(message_error, Qgis.Warning)
            self.xtf_file_line_edit.setFocus()
            return

        if not self.get_ili_models():
            message_error = QCoreApplication.translate('DialogImportData','Please set a valid model(s) before creating the project.')
            self.txtStdout.setText(message_error)
            self.show_message(message_error, Qgis.Warning)
            self.import_models_list_view.setFocus()
            return

        if self.type_combo_box.currentData() == 'ili2gpkg':
            if not configuration.dbfile or self.gpkg_file_line_edit.validator().validate(configuration.dbfile, 0)[0] != QValidator.Acceptable:
                message_error = QCoreApplication.translate("DialogImportData", 'Please set a valid database file before creating the project.')
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
                    self.show_message(QCoreApplication.translate('DialogImportData', 'An error occurred when importing the data'), Qgis.Warning)
                    return
            except JavaNotFoundError:
                self.txtStdout.setTextColor(QColor('#000000'))
                self.txtStdout.clear()
                self.txtStdout.setText(QCoreApplication.translate('DialogImportData','Java could not be found. Please <a href="https://java.com/en/download/">install Java</a> and or <a href="#configure">configure a custom java path</a>. We also support the JAVA_HOME environment variable in case you prefer this.'))
                self.enable()
                self.progress_bar.hide()
                return

            self.buttonBox.clear()
            self.buttonBox.setEnabled(True)
            self.buttonBox.addButton(QDialogButtonBox.Close)
            self.progress_bar.setValue(100)
            self.show_message(QCoreApplication.translate('DialogImportData', 'Import of the data was successfully completed'), Qgis.Success)

    def save_configuration(self, configuration):
        settings = QSettings()
        settings.setValue('Asistente-LADM_COL/QgisModelBaker/ili2pg/xtffile_import', configuration.xtffile)
        settings.setValue('Asistente-LADM_COL/QgisModelBaker/importtype', self.type_combo_box.currentData())

        if self.type_combo_box.currentData() == 'ili2gpkg':
            settings.setValue('Asistente-LADM_COL/QgisModelBaker/ili2gpkg/dbfile', configuration.dbfile)

    def restore_configuration(self):
        settings = QSettings()
        self.xtf_file_line_edit.setText(settings.value('Asistente-LADM_COL/QgisModelBaker/ili2pg/xtffile_import'))
        self.type_combo_box.setCurrentIndex(self.type_combo_box.findData(settings.value('Asistente-LADM_COL/QgisModelBaker/importtype', 'ili2pg')))
        self.type_changed()

        # set model repository
        # if there is no option  by default use online model repository
        custom_model_is_checked =  settings.value('Asistente-LADM_COL/models/custom_model_directories_is_checked') if settings.value('Asistente-LADM_COL/models/custom_model_directories_is_checked') else 0
        self.use_local_models = bool(int(custom_model_is_checked))
        if self.use_local_models:
            self.custom_model_directories = settings.value('Asistente-LADM_COL/models/custom_models') if settings.value('Asistente-LADM_COL/models/custom_models') else None

    def updated_configuration(self):
        """
        Get the configuration that is updated with the user configuration changes on the dialog.
        :return: Configuration
        """
        configuration = ImportDataConfiguration()

        if self.type_combo_box.currentData() == 'ili2pg':
            # PostgreSQL specific options
            configuration.dbhost = self.db.host
            configuration.dbport = self.db.port
            configuration.dbusr = self.db.user
            configuration.database = self.db.dbname
            configuration.dbschema = self.get_checked_schema()
            configuration.dbpwd = self.db.password
        elif self.type_combo_box.currentData() == 'ili2gpkg':
            configuration.dbfile = self.gpkg_file_line_edit.text().strip()

        configuration.xtffile = self.xtf_file_line_edit.text().strip()
        configuration.delete_data = False

        configuration.epsg = DEFAULT_EPSG
        configuration.inheritance = DEFAULT_INHERITANCE
        configuration.create_basket_col = False
        configuration.create_import_tid = False
        configuration.stroke_arcs = True

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

    def print_new_info(self, message_error):
        self.txtStdout.setTextColor(QColor('#000000'))
        self.txtStdout.clear()
        self.txtStdout.setText(message_error)

    def print_info(self, text, text_color='#000000'):
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
            self.show_message(QCoreApplication.translate('DialogImportData', 'Error when importing data'), Qgis.Warning)
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
        self.pg_config.setEnabled(False)
        self.ili_config.setEnabled(False)
        self.buttonBox.setEnabled(False)

    def enable(self):
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
