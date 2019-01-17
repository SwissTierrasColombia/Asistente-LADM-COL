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

from QgisModelBaker.libili2db import iliimporter
from QgisModelBaker.libili2db.ili2dbconfig import (SchemaImportConfiguration,
                                                   BaseConfiguration)
from QgisModelBaker.libili2db.ili2dbutils import color_log_text
from QgisModelBaker.libili2db.iliimporter import JavaNotFoundError
from QgisModelBaker.libili2db.ilicache import IliCache

from ...utils.qt_utils import (Validators,
                               NonEmptyStringValidator,
                               FileValidator,
                               make_file_selector,
                               make_save_file_selector,
                               OverrideCursor)

from ...config.general_config import (DEFAULT_EPSG,
                                      DEFAULT_INHERITANCE,
                                      DEFAULT_MODEL_NAMES_CHECKED)

from ...lib.dbconnector.pg_connector import PGConnector
from ...utils import get_ui_class
from ...resources_rc import *

DIALOG_UI = get_ui_class('dlg_import_schema.ui')

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
        self.type_combo_box.addItem(QCoreApplication.translate('DialogImportSchema','Interlis (use PostGIS)'), 'ili2pg')
        self.type_combo_box.addItem(QCoreApplication.translate('DialogImportSchema','Interlis (use GeoPackage)'), 'ili2gpkg')
        self.type_combo_box.currentIndexChanged.connect(self.type_changed)
        self.type_changed()

        self.schema_name_line_edit.setPlaceholderText(QCoreApplication.translate('DialogImportSchema', "[Name of the schema to be created]"))
        self.validators = Validators()
        nonEmptyValidator = NonEmptyStringValidator()
        self.schema_name_line_edit.setValidator(nonEmptyValidator)
        self.schema_name_line_edit.textChanged.connect(self.validators.validate_line_edits)
        self.schema_name_line_edit.textChanged.emit(self.schema_name_line_edit.text())

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

        self.connection_setting_button.setText(QCoreApplication.translate('DialogImportSchema', 'Connection Settings'))

        # GPKG
        self.gpkg_file_browse_button.clicked.connect(make_file_selector(self.gpkg_file_line_edit,
                                                                        title=QCoreApplication.translate('DialogImportSchema', 'Open GeoPackage database file'),
                                                                        file_filter=QCoreApplication.translate('DialogImportSchema','GeoPackage Database (*.gpkg)')))

        gpkgFileValidator = FileValidator(pattern='*.gpkg')
        self.gpkg_file_line_edit.setValidator(gpkgFileValidator)

        self.gpkgSaveFileValidator = FileValidator(pattern='*.gpkg', allow_non_existing=True)
        self.gpkgOpenFileValidator = FileValidator(pattern='*.gpkg')
        self.gpkg_file_line_edit.textChanged.connect(self.validators.validate_line_edits)

        # LOG
        self.log_config.setTitle(QCoreApplication.translate('DialogImportSchema', 'Show log'))

        self.bar = QgsMessageBar()
        self.bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.layout().addWidget(self.bar, 0, 0, Qt.AlignTop)

        self.buttonBox.accepted.disconnect()
        self.buttonBox.accepted.connect(self.accepted)
        self.buttonBox.clear()
        self.buttonBox.addButton(QDialogButtonBox.Cancel)
        self.buttonBox.addButton(QCoreApplication.translate('DialogImportSchema', 'Import schema'), QDialogButtonBox.AcceptRole)
        self.buttonBox.addButton(QDialogButtonBox.Help)
        self.buttonBox.helpRequested.connect(self.show_help)

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

    def accepted(self):
        configuration = self.updated_configuration()

        if not self.get_checked_models():
            message_error = QCoreApplication.translate('DialogImportSchema','Please set a valid INTERLIS model(s) before creating the project.')
            self.txtStdout.setText(message_error)
            self.show_message(message_error, Qgis.Critical)
            self.import_models_list_view.setFocus()
            return

        if self.type_combo_box.currentData() == 'ili2pg':
            if not self.schema_name_line_edit.text().strip():
                message_error = QCoreApplication.translate('DialogImportSchema','Please set a valid schema name before creating the project.')
                self.txtStdout.setText(message_error)
                self.show_message(message_error, Qgis.Critical)
                self.schema_name_line_edit.setFocus()
                return
        elif self.type_combo_box.currentData() == 'ili2gpkg':
            if not configuration.dbfile or self.gpkg_file_line_edit.validator().validate(configuration.dbfile, 0)[0] != QValidator.Acceptable:
                message_error = QCoreApplication.translate("DialogImportSchema", 'Please set a valid database file before creating the project.')
                self.txtStdout.setText(message_error)
                self.show_message(message_error, Qgis.Critical)
                self.gpkg_file_line_edit.setFocus()
                return

        configuration.dbschema = self.schema_name_line_edit.text().strip().lower()
        self.save_configuration(configuration)

        if self.type_combo_box.currentData() == 'ili2pg':
            _db_connector = PGConnector(self.db.get_uri_without_schema(), configuration.dbschema)
            res, msg = _db_connector.test_connection()
            if res:
                if _db_connector._schema_exists():
                    message_error = QCoreApplication.translate("DialogImportSchema", 'Schema {} exist, please set a valid schema name before creating the project.'.format(configuration.dbschema))
                    self.show_message(message_error, Qgis.Critical)
                    self.print_new_info(message_error)
                    return

        with OverrideCursor(Qt.WaitCursor):
            self.progress_bar.show()
            self.progress_bar.setValue(0)

            self.disable()
            self.txtStdout.setTextColor(QColor('#000000'))
            self.txtStdout.clear()

            importer = iliimporter.Importer()

            importer.tool_name = self.type_combo_box.currentData()
            importer.configuration = configuration
            importer.stdout.connect(self.print_info)
            importer.stderr.connect(self.on_stderr)
            importer.process_started.connect(self.on_process_started)
            importer.process_finished.connect(self.on_process_finished)

            try:
                self.progress_bar.setValue(50)
                if importer.run() != iliimporter.Importer.SUCCESS:
                    self.enable()
                    self.progress_bar.hide()
                    return
            except JavaNotFoundError:
                self.txtStdout.setTextColor(QColor('#000000'))
                self.txtStdout.clear()
                self.txtStdout.setText(QCoreApplication.translate('DialogImportSchema',
                    'Java could not be found. Please <a href="https://java.com/en/download/">install Java</a> and or <a href="#configure">configure a custom java path</a>. We also support the JAVA_HOME environment variable in case you prefer this.'))
                self.enable()
                self.progress_bar.hide()
                return

            self.buttonBox.clear()
            self.buttonBox.setEnabled(True)
            self.buttonBox.addButton(QDialogButtonBox.Close)
            self.progress_bar.setValue(100)
            self.print_info(QCoreApplication.translate('DialogImportSchema', '\nDone!'), '#004905')

    def save_configuration(self, configuration):
        settings = QSettings()
        settings.setValue('QgisModelBaker/importtype', self.type_combo_box.currentData())
        if self.type_combo_box.currentData() == 'ili2gpkg':
            settings.setValue('QgisModelBaker/ili2gpkg/dbfile', configuration.dbfile)

    def restore_configuration(self):
        settings = QSettings()
        self.type_combo_box.setCurrentIndex(self.type_combo_box.findData(settings.value('QgisModelBaker/importtype', 'ili2pg')))
        self.type_changed()

    def updated_configuration(self):
        configuration = SchemaImportConfiguration()

        if self.type_combo_box.currentData() == 'ili2pg':
            # PostgreSQL specific options
            configuration.tool_name = 'ili2pg'
            configuration.dbhost = self.db.host
            configuration.dbport = self.db.port
            configuration.dbusr = self.db.user
            configuration.database = self.db.dbname
            configuration.dbschema = self.schema_name_line_edit.text().strip().lower()
            configuration.dbpwd = self.db.password
        elif self.type_combo_box.currentData() == 'ili2gpkg':
            configuration.tool_name = 'ili2gpkg'
            configuration.dbfile = self.gpkg_file_line_edit.text().strip()

        configuration.epsg = DEFAULT_EPSG
        configuration.inheritance = DEFAULT_INHERITANCE
        configuration.create_basket_col = False
        configuration.create_import_tid = False
        configuration.stroke_arcs = True

        configuration.base_configuration = self.base_configuration
        if self.get_checked_models():
            configuration.ilimodels = ';'.join(self.get_checked_models())

        return configuration

    def print_info(self, text, text_color='#000000'):
        self.txtStdout.setTextColor(QColor(text_color))
        self.txtStdout.append(text)
        QCoreApplication.processEvents()

    def print_new_info(self, message_error):
        self.txtStdout.setTextColor(QColor('#000000'))
        self.txtStdout.clear()
        self.txtStdout.setText(message_error)

    def on_stderr(self, text):
        color_log_text(text, self.txtStdout)
        self.advance_progress_bar_by_text(text)
        QCoreApplication.processEvents()

    def on_process_started(self, command):
        self.txtStdout.setText(command)
        self.progress_bar.setValue(30)
        QCoreApplication.processEvents()

    def on_process_finished(self, exit_code, result):
        if exit_code == 0:
            color = '#004905'
            message = QCoreApplication.translate('DialogImportSchema', 'Interlis model(s) successfully imported into the database!')
        else:
            color = '#aa2222'
            message = QCoreApplication.translate('DialogImportSchema','Finished with errors!')

        self.txtStdout.setTextColor(QColor(color))
        self.txtStdout.append(message)
        self.progress_bar.setValue(50)

    def advance_progress_bar_by_text(self, text):
        if text.strip() == 'Info: compile models…':
            self.progress_bar.setValue(20)
        elif text.strip() == 'Info: create table structure…':
            self.progress_bar.setValue(30)

    def show_help(self):
        self.qgis_utils.show_help("import_schema")

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
            self.gpkg_file_line_edit.setValidator(self.gpkgSaveFileValidator)
            self.gpkg_file_line_edit.textChanged.emit(self.gpkg_file_line_edit.text())
            try:
                self.gpkg_file_browse_button.clicked.disconnect()
            except:
                pass
            self.gpkg_file_browse_button.clicked.connect(
                make_save_file_selector(
                    self.gpkg_file_line_edit,
                    title=QCoreApplication.translate('DialogImportSchema', 'Open GeoPackage database file'),
                    file_filter=QCoreApplication.translate('DialogImportSchema','GeoPackage Database (*.gpkg)'),
                    extension='.gpkg'))
