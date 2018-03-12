# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2017-10-31
        git sha              : :%H$
        copyright            : (C) 2017 by Germán Carrillo (BSF Swissphoto)
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

import qgis.utils
from qgis.core import QgsMessageLog, Qgis
from qgis.PyQt.QtCore import (QObject, Qt, QCoreApplication, QTranslator,
                              QLocale, QSettings)
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QMenu, QPushButton, QMessageBox

from .config.table_mapping_config import PROJECT_GENERATOR_MIN_REQUIRED_VERSION
from .gui.point_spa_uni_cadastre_wizard import PointsSpatialUnitCadastreWizard
from .gui.define_boundaries_cadastre_wizard import DefineBoundariesCadastreWizard
from .gui.create_plot_cadastre_wizard import CreatePlotCadastreWizard
from .gui.create_parcel_cadastre_wizard import CreateParcelCadastreWizard
from .gui.create_natural_party_cadastre_wizard import CreateNaturalPartyCadastreWizard
from .gui.create_legal_party_cadastre_wizard import CreateLegalPartyCadastreWizard
from .gui.create_right_cadastre_wizard import CreateRightCadastreWizard
from .gui.create_responsibility_cadastre_wizard import CreateResponsibilityCadastreWizard
from .gui.create_restriction_cadastre_wizard import CreateRestrictionCadastreWizard
from .gui.create_administrative_source_cadastre_wizard import CreateAdministrativeSourceCadastreWizard
from .gui.create_spatial_source_cadastre_wizard import CreateSpatialSourceCadastreWizard
from .gui.settings_dialog import SettingsDialog
from .utils.qgis_utils import QGISUtils

from functools import partial, wraps
#import resources_rc

class AsistenteLADMCOLPlugin(QObject):
    def __init__(self, iface):
        QObject.__init__(self)
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.installTranslator()

    def initGui(self):
        # Set Menus
        icon = QIcon(":/Asistente-LADM_COL/images/icon.png")
        self._menu = QMenu("LAD&M_COL", self.iface.mainWindow().menuBar())
        actions = self.iface.mainWindow().menuBar().actions()
        if len(actions) > 0:
            last_action = actions[-1]
            self.iface.mainWindow().menuBar().insertMenu(last_action, self._menu)
        else:
            self.iface.mainWindow().menuBar().addMenu(self._menu)

        self._settings_dialog = None
        self.qgis_utils = QGISUtils()

        self._cadastre_menu = QMenu(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Cadastre"), self._menu)
        self._spatial_unit_cadastre_menu = QMenu(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Spatial Unit"), self._cadastre_menu)
        self._point_spatial_unit_cadastre_action = QAction(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Add Points"), self._spatial_unit_cadastre_menu)
        self._boundary_spatial_unit_cadastre_action = QAction(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Define Boundaries"), self._spatial_unit_cadastre_menu)
        self._plot_spatial_unit_cadastre_action = QAction(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create plot"), self._spatial_unit_cadastre_menu)
        self._spatial_unit_cadastre_menu.addActions([self._point_spatial_unit_cadastre_action,
                                                     self._boundary_spatial_unit_cadastre_action,
                                                     self._plot_spatial_unit_cadastre_action])

        self._baunit_cadastre_menu = QMenu(QCoreApplication.translate("AsistenteLADMCOLPlugin", "BA Unit"), self._cadastre_menu)
        self._parcel_baunit_cadastre_action = QAction(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Parcel"), self._baunit_cadastre_menu)
        self._baunit_cadastre_menu.addActions([self._parcel_baunit_cadastre_action])

        self._party_cadastre_menu = QMenu(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Party"), self._cadastre_menu)
        self._natural_party_cadastre_action = QAction(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Natural Party"), self._party_cadastre_menu)
        self._legal_party_cadastre_action = QAction(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Legal Party"), self._party_cadastre_menu)
        self._party_cadastre_menu.addActions([self._natural_party_cadastre_action,
                                              self._legal_party_cadastre_action])

        self._rrr_cadastre_menu = QMenu(QCoreApplication.translate("AsistenteLADMCOLPlugin", "RRR"), self._cadastre_menu)
        self._right_rrr_cadastre_action = QAction(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Right"), self._rrr_cadastre_menu)
        self._restriction_rrr_cadastre_action = QAction(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Restriction"), self._rrr_cadastre_menu)
        self._responsibility_rrr_cadastre_action = QAction(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Responsibility"), self._rrr_cadastre_menu)
        self._rrr_cadastre_menu.addActions([self._right_rrr_cadastre_action,
                                            self._restriction_rrr_cadastre_action,
                                            self._responsibility_rrr_cadastre_action])

        self._source_cadastre_menu = QMenu(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Source"), self._cadastre_menu)
        self._administrative_source_cadastre_action = QAction(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Administrative Source"), self._source_cadastre_menu)
        self._spatial_source_cadastre_action = QAction(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Spatial Source"), self._source_cadastre_menu)
        self._source_cadastre_menu.addActions([self._administrative_source_cadastre_action,
                                               self._spatial_source_cadastre_action])

        self._quality_cadastre_menu = QMenu(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Quality"), self._cadastre_menu)
        self._too_long_boundary_cadastre_action = QAction(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Check too long boundary segments"), self._quality_cadastre_menu)
        self._quality_cadastre_menu.addActions([self._too_long_boundary_cadastre_action])

        self._cadastre_menu.addMenu(self._spatial_unit_cadastre_menu)
        self._cadastre_menu.addMenu(self._baunit_cadastre_menu)
        self._cadastre_menu.addMenu(self._party_cadastre_menu)
        self._cadastre_menu.addMenu(self._rrr_cadastre_menu)
        self._cadastre_menu.addMenu(self._source_cadastre_menu)
        self._cadastre_menu.addSeparator()
        self._cadastre_menu.addMenu(self._quality_cadastre_menu)

        self._menu.addMenu(self._cadastre_menu)
        self._menu.addSeparator()
        self._settings_action = QAction(icon, QCoreApplication.translate("AsistenteLADMCOLPlugin", "Settings"), self.iface.mainWindow())
        self._help_action = QAction(icon, QCoreApplication.translate("AsistenteLADMCOLPlugin", "Help"), self.iface.mainWindow())
        self._about_action = QAction(icon, QCoreApplication.translate("AsistenteLADMCOLPlugin", "About"), self.iface.mainWindow())
        self._menu.addActions([self._settings_action,
                               self._help_action,
                               self._about_action])

        # Set connections
        self._point_spatial_unit_cadastre_action.triggered.connect(self.show_wiz_point_sp_un_cad)
        self._boundary_spatial_unit_cadastre_action.triggered.connect(self.show_wiz_boundaries_cad)
        self._plot_spatial_unit_cadastre_action.triggered.connect(self.show_wiz_plot_cad)
        self._parcel_baunit_cadastre_action.triggered.connect(self.show_wiz_parcel_cad)
        self._natural_party_cadastre_action.triggered.connect(self.show_wiz_natural_party_cad)
        self._legal_party_cadastre_action.triggered.connect(self.show_wiz_legal_party_cad)
        self._right_rrr_cadastre_action.triggered.connect(self.show_wiz_right_rrr_cad)
        self._responsibility_rrr_cadastre_action.triggered.connect(self.show_wiz_responsibility_rrr_cad)
        self._restriction_rrr_cadastre_action.triggered.connect(self.show_wiz_restriction_rrr_cad)
        self._administrative_source_cadastre_action.triggered.connect(self.show_wiz_administrative_source_cad)
        self._spatial_source_cadastre_action.triggered.connect(self.show_wiz_spatial_source_cad)
        self._too_long_boundary_cadastre_action.triggered.connect(self.check_too_long_segments)
        self._settings_action.triggered.connect(self.show_settings)
        self._about_action.triggered.connect(self.show_about_dialog)
        self.qgis_utils.layer_symbology_changed.connect(self.refresh_layer_symbology)
        self.qgis_utils.message_emitted.connect(self.show_message)
        self.qgis_utils.message_with_button_load_layer_emitted.connect(self.show_message_to_load_layer)
        self.qgis_utils.message_with_button_load_layers_emitted.connect(self.show_message_to_load_layers)
        self.qgis_utils.map_refresh_requested.connect(self.refresh_map)

        # Toolbar for Define Boundaries
        self._boundary_explode_action = QAction(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Explode..."), self.iface.mainWindow())
        self._boundary_explode_action.triggered.connect(self.call_explode_boundaries)
        self._boundary_merge_action = QAction(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Merge..."), self.iface.mainWindow())
        self._boundary_merge_action.triggered.connect(self.call_merge_boundaries)
        self._fill_point_BFS_action = QAction(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Fill Point BFS"), self.iface.mainWindow())
        self._fill_point_BFS_action.triggered.connect(self.call_fill_topology_table_pointbfs)
        self._fill_more_BFS_less_action = QAction(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Fill More BFS and Less"), self.iface.mainWindow())
        self._fill_more_BFS_less_action.triggered.connect(self.call_fill_topology_tables_morebfs_less)
        self._define_boundary_toolbar = self.iface.addToolBar(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Define Boundaries"))
        self._define_boundary_toolbar.setObjectName("DefineBoundaries")
        self._define_boundary_toolbar.addActions([self._boundary_explode_action,
                                                  self._boundary_merge_action,
                                                  self._fill_point_BFS_action,
                                                  self._fill_more_BFS_less_action])
        self._define_boundary_toolbar.setVisible(False)

    def refresh_map(self):
        self.iface.mapCanvas().refresh()

    def refresh_layer_symbology(self, layer_id):
        self.iface.layerTreeView().refreshLayerSymbology(layer_id)

    def show_message(self, msg, level):
        self.iface.messageBar().pushMessage("Asistente LADM_COL", msg, level)

    def show_message_to_load_layer(self, msg, button_text, layer, level):
        widget = self.iface.messageBar().createMessage("Asistente LADM_COL", msg)
        button = QPushButton(widget)
        button.setText(button_text)
        button.pressed.connect(partial(self.load_layer, layer))
        widget.layout().addWidget(button)
        self.iface.messageBar().pushWidget(widget, level, 15)

    def show_message_to_load_layers(self, msg, button_text, layers, level):
        widget = self.iface.messageBar().createMessage("Asistente LADM_COL", msg)
        button = QPushButton(widget)
        button.setText(button_text)
        button.pressed.connect(partial(self.load_layers, layers))
        widget.layout().addWidget(button)
        self.iface.messageBar().pushWidget(widget, level, 15)

    def load_layer(self, layer):
        self.qgis_utils.get_layer(self.get_db_connection(), layer[0], layer[1], load=True)

    def load_layers(self, layers):
        self.qgis_utils.get_layers(self.get_db_connection(), layers, True)

    def _db_connection_required(func_to_decorate):
        @wraps(func_to_decorate)
        def decorated_function(inst, *args, **kwargs):
            # Check if current connection is valid and disable access if not
            db = inst.get_db_connection()
            res, msg = db.test_connection()
            if res:
                func_to_decorate(inst)
            else:
                widget = inst.iface.messageBar().createMessage("Asistente LADM_COL",
                             QCoreApplication.translate("AsistenteLADMCOLPlugin", "You need to set a valid connection to your DB first. Click the button to go to Settings."))
                button = QPushButton(widget)
                button.setText(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Settings"))
                button.pressed.connect(inst.show_settings)
                widget.layout().addWidget(button)
                inst.iface.messageBar().pushWidget(widget, Qgis.Warning, 15)
                QgsMessageLog.logMessage(QCoreApplication.translate("AsistenteLADMCOLPlugin", "A dialog couldn't be open, connection to DB was not valid."), "Asistente LADM_COL")

        return decorated_function

    def _project_generator_required(func_to_decorate):
        @wraps(func_to_decorate)
        def decorated_function(inst, *args, **kwargs):
            # Check if Project Generator is installed and active, disable access if not
            plugin_version_right = inst.is_plugin_version_valid()

            if plugin_version_right:
                func_to_decorate(inst)
            else:
                widget = inst.iface.messageBar().createMessage("Asistente LADM_COL",
                             QCoreApplication.translate("AsistenteLADMCOLPlugin", "The plugin 'Project Generator' version {} (or higher) is required, but couldn't be found. Click the button to show the Plugin Manager.").format(PROJECT_GENERATOR_MIN_REQUIRED_VERSION))
                button = QPushButton(widget)
                button.setText(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Plugin Manager"))
                button.pressed.connect(inst.show_plugin_manager)
                widget.layout().addWidget(button)
                inst.iface.messageBar().pushWidget(widget, Qgis.Warning, 15)
                QgsMessageLog.logMessage(QCoreApplication.translate("AsistenteLADMCOLPlugin", "A dialog couldn't be open, Project Generator not found."), "Asistente LADM_COL")

        return decorated_function

    def get_plugin_version(self, plugin_dir):
        file_path = os.path.join(plugin_dir, 'metadata.txt')
        if os.path.isfile(file_path):
            with open(file_path) as metadata:
                for line in metadata:
                    line_array = line.strip().split("=")
                    if line_array[0] == 'version':
                        return line_array[1]
        return None

    def is_plugin_version_valid(self):
        plugin_found = 'projectgenerator' in qgis.utils.plugins
        if not plugin_found:
            return False
        current_version = self.get_plugin_version(qgis.utils.plugins['projectgenerator'].plugin_dir)
        min_required_version = PROJECT_GENERATOR_MIN_REQUIRED_VERSION
        if current_version is None:
            return False

        current_version_splitted = current_version.split(".")
        if len(current_version_splitted) < 4: # We could need 4 places for custom Project Generator versions
            current_version_splitted = current_version_splitted + ['0','0','0','0']
            current_version_splitted = current_version_splitted[:4]

        min_required_version_splitted = min_required_version.split(".")
        if len(min_required_version_splitted) < 4:
            min_required_version_splitted = min_required_version_splitted + ['0','0','0','0']
            min_required_version_splitted = min_required_version_splitted[:4]

        print(min_required_version_splitted, current_version_splitted)

        for i in range(len(current_version_splitted)):
            if int(current_version_splitted[i]) < int(min_required_version_splitted[i]):
                return False
            elif int(current_version_splitted[i]) > int(min_required_version_splitted[i]):
                return True

        return True

    @_project_generator_required
    @_db_connection_required
    def call_explode_boundaries(self):
        self.qgis_utils.explode_boundaries(self.get_db_connection())

    @_project_generator_required
    @_db_connection_required
    def call_merge_boundaries(self):
        self.qgis_utils.merge_boundaries(self.get_db_connection())

    @_project_generator_required
    @_db_connection_required
    def call_fill_topology_table_pointbfs(self):
        self.qgis_utils.fill_topology_table_pointbfs(self.get_db_connection())

    @_project_generator_required
    @_db_connection_required
    def call_fill_topology_tables_morebfs_less(self):
        self.qgis_utils.fill_topology_tables_morebfs_less(self.get_db_connection())

    def unload(self):
        # remove the plugin menu item and icon
        self._menu.deleteLater()
        self.iface.mainWindow().removeToolBar(self._define_boundary_toolbar)
        del self._define_boundary_toolbar

    def show_settings(self):
        self._settings_dialog = self.get_settings_dialog()
        self._settings_dialog.exec_()

    def show_plugin_manager(self):
        self.iface.actionManagePlugins().trigger()

    def get_settings_dialog(self):
        if self._settings_dialog is None:
            self._settings_dialog = SettingsDialog(self.iface)
        return self._settings_dialog

    def get_db_connection(self):
        self._settings_dialog = self.get_settings_dialog()
        return self._settings_dialog.get_db_connection()

    @_project_generator_required
    @_db_connection_required
    def show_wiz_point_sp_un_cad(self):
        wiz = PointsSpatialUnitCadastreWizard(self.iface, self.get_db_connection(), self.qgis_utils)
        wiz.exec_()

    @_project_generator_required
    @_db_connection_required
    def show_wiz_boundaries_cad(self):
        wiz = DefineBoundariesCadastreWizard(self.iface, self.get_db_connection(), self.qgis_utils)
        wiz.exec_()

    @_project_generator_required
    @_db_connection_required
    def show_wiz_plot_cad(self):
        wiz = CreatePlotCadastreWizard(self.iface, self.get_db_connection(), self.qgis_utils)
        wiz.exec_()

    @_project_generator_required
    @_db_connection_required
    def show_wiz_parcel_cad(self):
        wiz = CreateParcelCadastreWizard(self.iface, self.get_db_connection(), self.qgis_utils)
        wiz.exec_()

    @_project_generator_required
    @_db_connection_required
    def show_wiz_natural_party_cad(self):
        wiz = CreateNaturalPartyCadastreWizard(self.iface, self.get_db_connection(), self.qgis_utils)
        wiz.exec_()

    @_project_generator_required
    @_db_connection_required
    def show_wiz_legal_party_cad(self):
        wiz = CreateLegalPartyCadastreWizard(self.iface, self.get_db_connection(), self.qgis_utils)
        wiz.exec_()

    @_project_generator_required
    @_db_connection_required
    def show_wiz_right_rrr_cad(self):
        wiz = CreateRightCadastreWizard(self.iface, self.get_db_connection(), self.qgis_utils)
        wiz.exec_()

    @_project_generator_required
    @_db_connection_required
    def show_wiz_responsibility_rrr_cad(self):
        wiz = CreateResponsibilityCadastreWizard(self.iface, self.get_db_connection(), self.qgis_utils)
        wiz.exec_()

    @_project_generator_required
    @_db_connection_required
    def show_wiz_restriction_rrr_cad(self):
        wiz = CreateRestrictionCadastreWizard(self.iface, self.get_db_connection(), self.qgis_utils)
        wiz.exec_()

    @_project_generator_required
    @_db_connection_required
    def show_wiz_administrative_source_cad(self):
        wiz = CreateAdministrativeSourceCadastreWizard(self.iface, self.get_db_connection(), self.qgis_utils)
        wiz.exec_()

    @_project_generator_required
    @_db_connection_required
    def show_wiz_spatial_source_cad(self):
        wiz = CreateSpatialSourceCadastreWizard(self.iface, self.get_db_connection(), self.qgis_utils)
        wiz.exec_()

    @_project_generator_required
    @_db_connection_required
    def check_too_long_segments(self):
        self.qgis_utils.check_too_long_segments(self.get_db_connection())

    def show_about_dialog(self):
        self.msg = QMessageBox()
        #self.msg.setIcon(QMessageBox.Information)
        self.msg.setTextFormat(Qt.RichText)
        self.msg.setWindowTitle(QCoreApplication.translate("AsistenteLADMCOLPlugin", 'About'))
        description = QCoreApplication.translate("AsistenteLADMCOLPlugin", """<html><head/><body><p align="center"><span style=" font-size:14pt; font-weight:600;">Asistente LADM_COL</span></p><p align="center">Plugin de <a href="http://qgis.org"><span style=" text-decoration: underline; color:#0000ff;">QGIS</span></a> que ayuda a capturar y mantener datos conformes con <a href="https://github.com/AgenciaImplementacion/LADM_COL"><span style=" text-decoration: underline; color:#0000ff;">LADM_COL</span></a> y a generar archivos de intercambio de <a href="http://www.interlis.ch/index_e.htm"><span style=" text-decoration: underline; color:#0000ff;">INTERLIS</span></a> (.XTF).</p><p align="center">Licencia: <a href="https://github.com/AgenciaImplementacion/Asistente-LADM_COL/blob/master/LICENSE"><span style=" text-decoration: underline; color:#0000ff;">GNU General Public License v3.0</span></a></p><p align="center">Repositorio código fuente: <a href="https://github.com/AgenciaImplementacion/Asistente-LADM_COL"><span style=" text-decoration: underline; color:#0000ff;">Github</span></a></p><p align="center">Un proyecto de:<br/><a href="https://www.proadmintierra.info/"><span style=" text-decoration: underline; color:#0000ff;">Agencia de Implementación</span></a> (<a href="http://bsf-swissphoto.com/"><span style=" text-decoration: underline; color:#0000ff;">BSF-Swissphoto AG</span></a> - <a href="http://www.incige.com/"><span style=" text-decoration: underline; color:#0000ff;">INCIGE S.A.S</span></a>)</p><p align="center"><br/></p></body></html>""")
        self.msg.setText(description)
        self.msg.setStandardButtons(QMessageBox.Ok)
        msg_box = self.msg.exec_()

    def installTranslator(self):
        qgis_locale = QLocale(QSettings().value('locale/userLocale'))
        locale_path = os.path.join(self.plugin_dir, 'i18n')
        self.translator = QTranslator()
        self.translator.load(qgis_locale, 'Asistente-LADM_COL', '_', locale_path)
        QCoreApplication.installTranslator(self.translator)
