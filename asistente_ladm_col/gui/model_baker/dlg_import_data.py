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
from qgis.core import Qgis
from qgis.gui import QgsMessageBar

from qgis.PyQt.QtCore import (Qt,
                              QCoreApplication,
                              QSettings)
from qgis.PyQt.QtWidgets import (QDialog,
                                 QSizePolicy,
                                 QDialogButtonBox)
from qgis.PyQt.QtGui import (QColor,
                             QValidator,
                             QStandardItemModel,
                             QStandardItem)
from qgis.gui import QgsGui
from QgisModelBaker.libili2db import iliimporter
from QgisModelBaker.libili2db.ili2dbconfig import (ImportDataConfiguration,
                                                   BaseConfiguration)
from QgisModelBaker.libili2db.ili2dbutils import color_log_text
from QgisModelBaker.libili2db.iliimporter import JavaNotFoundError
from QgisModelBaker.libili2db.ilicache import IliCache

from ...utils.qt_utils import (Validators,
                               FileValidator,
                               make_file_selector,
                               make_save_file_selector,
                               OverrideCursor)

from ...config.general_config import (DEFAULT_EPSG,
                                      DEFAULT_INHERITANCE,
                                      DEFAULT_MODEL_NAMES_CHECKED)
from ...utils import get_ui_class
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
        self.type_combo_box.addItem(QCoreApplication.translate('DialogImportData','Interlis (use PostGIS)'), 'ili2pg')
        self.type_combo_box.addItem(QCoreApplication.translate('DialogImportData','Interlis (use GeoPackage)'), 'ili2gpkg')
        self.type_combo_box.currentIndexChanged.connect(self.type_changed)
        self.type_changed()

        self.update_schema_names_model()
        self.xtf_file_browse_button.clicked.connect(
            make_file_selector(self.xtf_file_line_edit, title=QCoreApplication.translate('DialogImportData','Open Transfer or Catalog File'),
                               file_filter=QCoreApplication.translate('DialogImportData','Transfer File (*.xtf *.itf);;Catalogue File (*.xml *.xls *.xlsx)')))

        self.validators = Validators()
        self.xtf_file_line_edit.setPlaceholderText(QCoreApplication.translate('DialogImportData', "[Name of the XTF to be created]"))
        fileValidator = FileValidator(pattern=['*.xtf', '*.itf', '*.xml'])
        self.xtf_file_line_edit.setValidator(fileValidator)
        self.xtf_file_line_edit.textChanged.connect(self.validators.validate_line_edits)
        self.xtf_file_line_edit.textChanged.emit(self.xtf_file_line_edit.text())

        self.qmodels_ilimodels = QStandardItemModel()
        for modelname in DEFAULT_MODEL_NAMES_CHECKED:
            item = QStandardItem(modelname)
            item.setCheckable(True)
            item.setEditable(False)
            item.setCheckState(DEFAULT_MODEL_NAMES_CHECKED[modelname])
            self.qmodels_ilimodels.appendRow(item)
        self.import_models_list_view.setModel(self.qmodels_ilimodels)

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


    def update_schema_names_model(self):
        res, msg = self.db.test_connection()
        schema_names = self.db._schema_names_list()
        self.schema_names_qmodels = QStandardItemModel()

        for schema_name in schema_names:
            item = QStandardItem(schema_name['schema_name'])
            item.setCheckable(True)
            item.setEditable(False)
            item.setCheckState(Qt.Unchecked)
            self.schema_names_qmodels.appendRow(item)

        default_item = self.schema_names_qmodels.item(0, 0)
        default_item.setCheckState(Qt.Checked)

        self.schema_names_list_view.setModel(self.schema_names_qmodels)
        self.schema_names_list_view.clicked.connect(self.on_click_schema_names)

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def on_click_schema_names(self, index_item):
        for index in range(self.schema_names_qmodels.rowCount()):
            item = self.schema_names_qmodels.item(index)
            item.setCheckState(Qt.Unchecked)
        item = self.schema_names_qmodels.itemFromIndex(index_item)
        item.setCheckState(Qt.Checked)

    def get_checked_schema(self):
        checked_schema = None
        for index in range(self.schema_names_qmodels.rowCount()):
            item = self.schema_names_qmodels.item(index)
            if item.checkState() == Qt.Checked:
                checked_schema = item.text()
                break
        return checked_schema

    def get_checked_models(self):
        checked_models = list()
        for index in range(self.qmodels_ilimodels.rowCount()):
            item = self.qmodels_ilimodels.item(index)
            if item.checkState() == Qt.Checked:
                checked_models.append(item.text())
        return checked_models

    def show_settings(self):
        self.qgis_utils.get_settings_dialog().exec_()
        self.db = self.qgis_utils.get_db_connection()
        self.db_connect_label.setToolTip(self.db.get_uri_without_password())
        self.db_connect_label.setText(self.db.dbname)
        self.update_schema_names_model()

    def accepted(self):

        configuration = self.updated_configuration()

        if not self.xtf_file_line_edit.validator().validate(configuration.xtffile, 0)[0] == QValidator.Acceptable:
            message_error = 'Please set a valid INTERLIS transfer or catalogue file before importing data.'
            self.txtStdout.setText(QCoreApplication.translate('DialogImportData',message_error))
            self.show_message(message_error, Qgis.Critical)
            self.xtf_file_line_edit.setFocus()
            return

        if not self.get_checked_models():
            message_error = QCoreApplication.translate('DialogImportData','Please set a valid INTERLIS model(s) before creating the project.')
            self.txtStdout.setText(message_error)
            self.show_message(message_error, Qgis.Critical)
            self.import_models_list_view.setFocus()
            return

        if self.type_combo_box.currentData() == 'ili2gpkg':
            if not configuration.dbfile or self.gpkg_file_line_edit.validator().validate(configuration.dbfile, 0)[0] != QValidator.Acceptable:
                message_error = QCoreApplication.translate("DialogImportData", 'Please set a valid database file before creating the project.')
                self.txtStdout.setText(message_error)
                self.show_message(message_error, Qgis.Critical)
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
            self.print_info(QCoreApplication.translate('DialogImportData', '\nDone!'), '#004905')

    def save_configuration(self, configuration):
        settings = QSettings()
        settings.setValue('QgisModelBaker/ili2pg/xtffile_import', configuration.xtffile)
        settings.setValue('QgisModelBaker/importtype', self.type_combo_box.currentData())

        if self.type_combo_box.currentData() == 'ili2gpkg':
            settings.setValue('QgisModelBaker/ili2gpkg/dbfile', configuration.dbfile)

    def restore_configuration(self):
        settings = QSettings()
        self.xtf_file_line_edit.setText(settings.value('QgisModelBaker/ili2pg/xtffile_import'))
        self.type_combo_box.setCurrentIndex(self.type_combo_box.findData(settings.value('QgisModelBaker/importtype', 'ili2pg')))
        self.type_changed()

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

        configuration.base_configuration = self.base_configuration
        if self.get_checked_models():
            configuration.ilimodels = ';'.join(self.get_checked_models())

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
            self.show_message(QCoreApplication.translate('DialogImportData', 'Error when importing data'), Qgis.Critical)
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
        if level == Qgis.Warning:
            self.bar.pushMessage(message, Qgis.Info, 10)
        elif level == Qgis.Critical:
            self.bar.pushMessage(message, Qgis.Warning, 10)

    def type_changed(self):
        self.progress_bar.hide()
        if self.type_combo_box.currentData() == 'ili2pg':
            self.pg_config.show()
            self.gpkg_config.hide()
        elif self.type_combo_box.currentData() == 'ili2gpkg':
            self.pg_config.hide()
            self.gpkg_config.show()
