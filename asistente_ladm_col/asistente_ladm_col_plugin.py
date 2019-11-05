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
import glob
import os.path
import shutil
from copy import deepcopy
from functools import partial
import processing

import qgis.utils
from processing.modeler.ModelerUtils import ModelerUtils
from qgis.PyQt.QtCore import (Qt,
                              QObject,
                              QCoreApplication,
                              QSettings,
                              pyqtSignal)
from qgis.PyQt.QtGui import QIcon, QColor
from qgis.PyQt.QtWidgets import (QAction,
                                 QMenu,
                                 QPushButton,
                                 QProgressBar)
from qgis.core import (Qgis,
                       QgsApplication,
                       QgsProcessingModelAlgorithm,
                       QgsExpression)

from asistente_ladm_col.config.enums import EnumDbActionType
from asistente_ladm_col.config.enums import WizardTypeEnum
from asistente_ladm_col.config.general_config import (ANNEX_17_REPORT,
                                                      ANT_MAP_REPORT,
                                                      CADASTRE_MENU_OBJECTNAME,
                                                      LADM_COL_MENU_OBJECTNAME,
                                                      PROPERTY_RECORD_CARD_MENU_OBJECTNAME,
                                                      OFFICIAL_DB_SOURCE,
                                                      PLUGIN_NAME,
                                                      PLUGIN_VERSION,
                                                      QUERIES_ACTION_OBJECTNAME,
                                                      RELEASE_URL,
                                                      REPORTS_MENU_OBJECTNAME,
                                                      URL_REPORTS_LIBRARIES,
                                                      TOOLBAR_NAME,
                                                      TOOLBAR_ID,
                                                      TOOLBAR_BUILD_BOUNDARY,
                                                      TOOLBAR_MOVE_NODES,
                                                      TOOLBAR_FILL_POINT_BFS,
                                                      TOOLBAR_FILL_MORE_BFS_LESS,
                                                      TOOLBAR_FILL_RIGHT_OF_WAY_RELATIONS,
                                                      TOOLBAR_IMPORT_FROM_INTERMEDIATE_STRUCTURE,
                                                      TOOLBAR_FINALIZE_GEOMETRY_CREATION,
                                                      ACTION_FINALIZE_GEOMETRY_CREATION_OBJECT_NAME,
                                                      VALUATION_MENU_OBJECTNAME,
                                                      SUPPLIES_MENU_OBJECTNAME,
                                                      NATIONAL_LAND_AGENCY, WIZARD_TYPE,
                                                      WIZARD_CLASS,
                                                      WIZARD_CREATE_COL_PARTY_CADASTRAL,
                                                      WIZARD_CREATE_ADMINISTRATIVE_SOURCE_CADASTRE,
                                                      WIZARD_CREATE_BOUNDARY_CADASTRE,
                                                      WIZARD_CREATE_BUILDING_CADASTRE,
                                                      WIZARD_CREATE_BUILDING_UNIT_CADASTRE,
                                                      WIZARD_CREATE_RIGHT_CADASTRE,
                                                      WIZARD_CREATE_RESTRICTION_CADASTRE,
                                                      WIZARD_CREATE_SPATIAL_SOURCE_CADASTRE,
                                                      WIZARD_CREATE_PARCEL_CADASTRE,
                                                      WIZARD_CREATE_PLOT_CADASTRE,
                                                      WIZARD_CREATE_EXT_ADDRESS_CADASTRE,
                                                      WIZARD_CREATE_RIGHT_OF_WAY_CADASTRE,
                                                      WIZARD_CREATE_GEOECONOMIC_ZONE_VALUATION,
                                                      WIZARD_CREATE_PHYSICAL_ZONE_VALUATION,
                                                      WIZARD_CREATE_BUILDING_UNIT_VALUATION,
                                                      WIZARD_CREATE_BUILDING_UNIT_QUALIFICATION_VALUATION,
                                                      WIZARD_LAYERS,
                                                      WIZARD_TOOL_NAME)
from asistente_ladm_col.config.wizard_config import WIZARDS_SETTINGS
from asistente_ladm_col.config.expression_functions import get_domain_code_from_value  # Registers it in QgsExpression
from asistente_ladm_col.data.ladm_data import LADM_DATA
from asistente_ladm_col.gui.change_detection.dockwidget_change_detection import DockWidgetChangeDetection
from asistente_ladm_col.gui.dialogs.dlg_about import AboutDialog
from asistente_ladm_col.gui.dialogs.dlg_controlled_measurement import ControlledMeasurementDialog
from asistente_ladm_col.gui.dialogs.dlg_import_from_excel import ImportFromExcelDialog
from asistente_ladm_col.gui.dialogs.dlg_load_layers import LoadLayersDialog
from asistente_ladm_col.gui.dialogs.dlg_log_excel import LogExcelDialog
from asistente_ladm_col.gui.dialogs.dlg_log_quality import LogQualityDialog
from asistente_ladm_col.gui.dialogs.dlg_official_data_settings import OfficialDataSettingsDialog
from asistente_ladm_col.gui.dialogs.dlg_quality import QualityDialog
from asistente_ladm_col.gui.dialogs.dlg_settings import SettingsDialog
from asistente_ladm_col.gui.dockwidget_queries import DockWidgetQueries
from asistente_ladm_col.gui.reports import ReportGenerator
from asistente_ladm_col.gui.right_of_way import RightOfWay
from asistente_ladm_col.gui.toolbar import ToolBar
from asistente_ladm_col.gui.wizards.cadastre.dlg_create_group_party_cadastre import CreateGroupPartyCadastre
from asistente_ladm_col.gui.wizards.cadastre.wiz_create_points_cadastre import CreatePointsCadastreWizard
from asistente_ladm_col.lib.db.db_connection_manager import ConnectionManager
from asistente_ladm_col.processing.ladm_col_provider import LADMCOLAlgorithmProvider
from asistente_ladm_col.utils.decorators import (_db_connection_required,
                                                 _validate_if_wizard_is_open,
                                                 _qgis_model_baker_required,
                                                 _activate_processing_plugin,
                                                 _map_swipe_tool_required,
                                                 _official_db_connection_required,
                                                 _different_db_connections_required)
from asistente_ladm_col.utils.qgis_utils import QGISUtils
from asistente_ladm_col.utils.qt_utils import OverrideCursor
from asistente_ladm_col.utils.quality import QualityUtils


class AsistenteLADMCOLPlugin(QObject):
    wiz_geometry_creation_finished = pyqtSignal()

    def __init__(self, iface):
        QObject.__init__(self)
        self.iface = iface
        self.log = QgsApplication.messageLog()
        self._about_dialog = None
        self._dock_widget_queries = None
        self._dock_widget_change_detection = None
        self.toolbar = None
        self.wiz_address = None
        self._report_menu = None
        self.conn_manager = ConnectionManager()
        self._db = self.get_db_connection()
        self.wiz = None
        self.is_wizard_open = False  # Helps to make the plugin modules aware of open wizards

    def initGui(self):
        # Set Menus
        icon = QIcon(":/Asistente-LADM_COL/resources/images/icon.png")
        self._menu = QMenu("LAD&M_COL", self.iface.mainWindow().menuBar())
        self._menu.setObjectName(LADM_COL_MENU_OBJECTNAME)
        actions = self.iface.mainWindow().menuBar().actions()
        if len(actions) > 0:
            last_action = actions[-1]
            self.iface.mainWindow().menuBar().insertMenu(last_action, self._menu)
        else:
            self.iface.mainWindow().menuBar().addMenu(self._menu)

        self.qgis_utils = QGISUtils(self.iface.layerTreeView())
        self.right_of_way = RightOfWay(self.iface, self.qgis_utils)
        self.quality = QualityUtils(self.qgis_utils)
        self.toolbar = ToolBar(self.iface, self.qgis_utils, self._db)
        self.ladm_data = LADM_DATA(self.qgis_utils)
        self.report_generator = ReportGenerator(self.qgis_utils, self.ladm_data)

        # Menus
        self.add_cadastre_menu()

        self._menu.addSeparator()
        self._load_layers_action = QAction(QIcon(), QCoreApplication.translate("AsistenteLADMCOLPlugin", "Load layers"), self.iface.mainWindow())
        self._queries_action = QAction(QIcon(), QCoreApplication.translate("AsistenteLADMCOLPlugin", "Queries"), self.iface.mainWindow())
        self._queries_action.setObjectName(QUERIES_ACTION_OBJECTNAME)
        self._menu.addActions([self._load_layers_action, self._queries_action])
        self.configure_reports_menu()
        self._menu.addSeparator()
        self.add_changes_menu()
        self._menu.addSeparator()
        self.add_data_management_menu()
        self._settings_action = QAction(QIcon(), QCoreApplication.translate("AsistenteLADMCOLPlugin", "Settings"), self.iface.mainWindow())
        self._help_action = QAction(QIcon(), QCoreApplication.translate("AsistenteLADMCOLPlugin", "Help"), self.iface.mainWindow())
        self._about_action = QAction(QIcon(), QCoreApplication.translate("AsistenteLADMCOLPlugin", "About"), self.iface.mainWindow())
        self._menu.addActions([self._settings_action,
                               self._help_action,
                               self._about_action])

        # Connections
        self._import_schema_action.triggered.connect(self.call_dlg_import_schema)
        self._import_data_action.triggered.connect(self.show_dlg_import_data)
        self._export_data_action.triggered.connect(self.show_dlg_export_data)
        self._controlled_measurement_action.triggered.connect(self.show_dlg_controlled_measurement)
        self._queries_action.triggered.connect(self.show_queries)
        self._load_layers_action.triggered.connect(self.load_layers_from_qgis_model_baker)
        self._settings_action.triggered.connect(self.show_settings)
        self._help_action.triggered.connect(self.show_help)
        self._about_action.triggered.connect(self.show_about_dialog)

        self.report_generator.enable_action_requested.connect(self.enable_action)

        self.qgis_utils.action_add_feature_requested.connect(self.trigger_add_feature)
        self.qgis_utils.action_vertex_tool_requested.connect(self.trigger_vertex_tool)
        self.qgis_utils.activate_layer_requested.connect(self.activate_layer)
        self.qgis_utils.clear_status_bar_emitted.connect(self.clear_status_bar)
        self.qgis_utils.clear_message_bar_emitted.connect(self.clear_message_bar)
        self.qgis_utils.create_progress_message_bar_emitted.connect(self.create_progress_message_bar)
        self.qgis_utils.remove_error_group_requested.connect(self.remove_error_group)
        self.qgis_utils.layer_symbology_changed.connect(self.refresh_layer_symbology)
        self.conn_manager.db_connection_changed.connect(self.refresh_menus)
        self.qgis_utils.organization_tools_changed.connect(self.refresh_organization_tools)
        self.qgis_utils.message_emitted.connect(self.show_message)
        self.qgis_utils.message_with_duration_emitted.connect(self.show_message)
        self.qgis_utils.message_with_button_load_layer_emitted.connect(self.show_message_to_load_layer)
        self.qgis_utils.message_with_button_load_layers_emitted.connect(self.show_message_to_load_layers)
        self.qgis_utils.message_with_open_table_attributes_button_emitted.connect(self.show_message_with_open_table_attributes_button)
        self.qgis_utils.message_with_button_download_report_dependency_emitted.connect(self.show_message_to_download_report_dependency)
        self.qgis_utils.message_with_button_remove_report_dependency_emitted.connect(self.show_message_to_remove_report_dependency)
        self.qgis_utils.status_bar_message_emitted.connect(self.show_status_bar_message)
        self.qgis_utils.map_refresh_requested.connect(self.refresh_map)
        self.qgis_utils.map_freeze_requested.connect(self.freeze_map)
        self.qgis_utils.set_node_visibility_requested.connect(self.set_node_visibility)
        self.quality.log_quality_show_message_emitted.connect(self.show_log_quality_message)
        self.quality.log_quality_show_button_emitted.connect(self.show_log_quality_button)
        self.quality.log_quality_set_initial_progress_emitted.connect(self.set_log_quality_initial_progress)
        self.quality.log_quality_set_final_progress_emitted.connect(self.set_log_quality_final_progress)

        # Toolbar
        self._finalize_geometry_creation_action = QAction(QIcon(":/Asistente-LADM_COL/resources/images/mActionFinalizeGeometryCreation.svg"),
                                                          TOOLBAR_FINALIZE_GEOMETRY_CREATION,
                                                          self.iface.mainWindow())
        self._finalize_geometry_creation_action.setObjectName(ACTION_FINALIZE_GEOMETRY_CREATION_OBJECT_NAME)
        self._finalize_geometry_creation_action.triggered.connect(self.wiz_geometry_creation_finished)  # SIGNAL chaining

        self._finalize_geometry_creation_action.setEnabled(False)

        self._build_boundary_action = QAction(TOOLBAR_BUILD_BOUNDARY, self.iface.mainWindow())
        self._build_boundary_action.triggered.connect(self.call_explode_boundaries)
        self._topological_editing_action = QAction(TOOLBAR_MOVE_NODES, self.iface.mainWindow())
        self._topological_editing_action.triggered.connect(self.call_topological_editing)
        self._fill_point_BFS_action = QAction(TOOLBAR_FILL_POINT_BFS, self.iface.mainWindow())
        self._fill_point_BFS_action.triggered.connect(self.call_fill_topology_table_pointbfs)
        self._fill_more_BFS_less_action = QAction(TOOLBAR_FILL_MORE_BFS_LESS, self.iface.mainWindow())
        self._fill_more_BFS_less_action.triggered.connect(self.call_fill_topology_tables_morebfs_less)
        self._fill_right_of_way_relations_action = QAction(TOOLBAR_FILL_RIGHT_OF_WAY_RELATIONS, self.iface.mainWindow())
        self._fill_right_of_way_relations_action.triggered.connect(self.call_fill_right_of_way_relations)
        self._import_from_intermediate_structure_action = QAction(TOOLBAR_IMPORT_FROM_INTERMEDIATE_STRUCTURE, self.iface.mainWindow())
        self._import_from_intermediate_structure_action.triggered.connect(self.call_import_from_intermediate_structure)
        self._ladm_col_toolbar = self.iface.addToolBar(QCoreApplication.translate("AsistenteLADMCOLPlugin", "LADM-COL tools"))
        self._ladm_col_toolbar.setObjectName(TOOLBAR_ID)
        self._ladm_col_toolbar.setToolTip(TOOLBAR_NAME)
        self._ladm_col_toolbar.addActions([self._finalize_geometry_creation_action,
                                           self._build_boundary_action,
                                           self._topological_editing_action,
                                           self._fill_point_BFS_action,
                                           self._fill_more_BFS_less_action,
                                           self._fill_right_of_way_relations_action,
                                           self._import_from_intermediate_structure_action])

        if not qgis.utils.active_plugins:
            self.iface.initializationCompleted.connect(self.call_refresh_menus)
        else:
            self.call_refresh_menus()

        # Add LADM_COL provider and models to QGIS
        self.ladm_col_provider = LADMCOLAlgorithmProvider()
        QgsApplication.processingRegistry().addProvider(self.ladm_col_provider)
        if QgsApplication.processingRegistry().providerById('model'):
            self.add_processing_models(None)
        else: # We need to wait until processing is initialized
            QgsApplication.processingRegistry().providerAdded.connect(self.add_processing_models)

    def uninstall_custom_expression_functions(self):
        res = QgsExpression.unregisterFunction('get_domain_code_from_value')

    def call_refresh_menus(self):
        # Refresh menus on QGIS start
        db = self.get_db_connection()
        res, msg = db.test_connection()
        if res:
            self.refresh_menus(db, res)
        else:  # Show by default all model creation tools
            self.add_property_record_card_menu()
            self.add_valuation_menu()
            self.add_supplies_menu()

    def add_data_management_menu(self):
        self._data_management_menu = QMenu(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Data Management"), self._menu)
        self._import_schema_action = QAction(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create LADM-COL structure"), self._data_management_menu)
        self._import_data_action = QAction(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Import data"), self._data_management_menu)
        self._export_data_action = QAction(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Export data"), self._data_management_menu)
        self._data_management_menu.addActions([self._import_schema_action, self._import_data_action, self._export_data_action])

        self._menu.addMenu(self._data_management_menu)

    def configure_reports_menu(self):
        report_menu_exists = False
        if self._report_menu:
            report_menu_exists = True
            self._report_menu.clear()
        else:
            self._report_menu = QMenu(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Reports"), self._menu)
            self._report_menu.setObjectName(REPORTS_MENU_OBJECTNAME)

        self._annex_17_action = QAction(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Annex 17"), self._report_menu)
        self._annex_17_action.triggered.connect(self.call_annex_17_report_generation)
        new_actions = [self._annex_17_action]

        if QSettings().value('Asistente-LADM_COL/advanced_settings/ant_tools', False, bool):  # ant_tools_enabled
             self._ant_map_action = QAction(QCoreApplication.translate("AsistenteLADMCOLPlugin", "ANT Map"), self._report_menu)
             self._ant_map_action.triggered.connect(self.call_ant_map_report_generation)
             new_actions.append(self._ant_map_action)

        self._report_menu.addActions(new_actions)

        if not report_menu_exists:
            self._menu.addMenu(self._report_menu)

    def add_cadastre_menu(self):
        self._cadastre_menu = QMenu(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Cadastre"), self._menu)
        self._cadastre_menu.setObjectName(CADASTRE_MENU_OBJECTNAME)

        self._preprocessing_menu = QMenu(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Preprocessing"), self._cadastre_menu)
        self._controlled_measurement_action = QAction(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Controlled Measurement"), self._preprocessing_menu)
        self._preprocessing_menu.addActions([self._controlled_measurement_action])

        self._surveying_and_representation_cadastre_menu = QMenu(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Surveying and Representation"), self._cadastre_menu)
        self._surveying_and_representation_cadastre_menu.setIcon(QIcon(":/Asistente-LADM_COL/resources/images/surveying.png"))
        self._point_surveying_and_representation_cadastre_action = QAction(
                QIcon(":/Asistente-LADM_COL/resources/images/points.png"),
                QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Point"),
                self._surveying_and_representation_cadastre_menu)
        self._boundary_surveying_and_representation_cadastre_action = QAction(
                QIcon(":/Asistente-LADM_COL/resources/images/lines.png"),
                QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Boundary"),
                self._surveying_and_representation_cadastre_menu)
        self._surveying_and_representation_cadastre_menu.addActions([self._point_surveying_and_representation_cadastre_action,
                                                       self._boundary_surveying_and_representation_cadastre_action])

        self._spatial_unit_cadastre_menu = QMenu(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Spatial Unit"), self._cadastre_menu)
        self._spatial_unit_cadastre_menu.setIcon(QIcon(":/Asistente-LADM_COL/resources/images/spatial_unit.png"))
        self._plot_spatial_unit_cadastre_action = QAction(
                QIcon(":/Asistente-LADM_COL/resources/images/polygons.png"),
                QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Plot"),
                self._spatial_unit_cadastre_menu)
        self._building_spatial_unit_cadastre_action = QAction(
                QIcon(":/Asistente-LADM_COL/resources/images/polygons.png"),
                QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Building"),
                self._spatial_unit_cadastre_menu)
        self._building_unit_spatial_unit_cadastre_action = QAction(
                QIcon(":/Asistente-LADM_COL/resources/images/polygons.png"),
                QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Building Unit"),
                self._spatial_unit_cadastre_menu)
        self._right_of_way_cadastre_action = QAction(
                QIcon(":/Asistente-LADM_COL/resources/images/polygons.png"),
                QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Right of Way"),
                self._spatial_unit_cadastre_menu)
        self._extaddress_cadastre_action = QAction(
                QIcon(":/Asistente-LADM_COL/resources/images/points.png"),
                QCoreApplication.translate("AsistenteLADMCOLPlugin", "Associate Address")
                )

        self._spatial_unit_cadastre_menu.addActions([self._plot_spatial_unit_cadastre_action,
                                                     self._building_spatial_unit_cadastre_action,
                                                     self._building_unit_spatial_unit_cadastre_action,
                                                     self._right_of_way_cadastre_action])
        self._spatial_unit_cadastre_menu.addSeparator()
        self._spatial_unit_cadastre_menu.addAction(self._extaddress_cadastre_action)

        self._baunit_cadastre_menu = QMenu(QCoreApplication.translate("AsistenteLADMCOLPlugin", "BA Unit"), self._cadastre_menu)
        self._baunit_cadastre_menu.setIcon(QIcon(":/Asistente-LADM_COL/resources/images/ba_unit.png"))
        self._parcel_baunit_cadastre_action = QAction(
                QIcon(":/Asistente-LADM_COL/resources/images/tables.png"),
                QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Parcel"),
                self._baunit_cadastre_menu)
        self._baunit_cadastre_menu.addActions([self._parcel_baunit_cadastre_action])

        self._party_cadastre_menu = QMenu(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Party"), self._cadastre_menu)
        self._party_cadastre_menu.setIcon(QIcon(":/Asistente-LADM_COL/resources/images/party.png"))
        self._col_party_cadastre_action = QAction(
                QIcon(":/Asistente-LADM_COL/resources/images/tables.png"),
                QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Party"),
                self._party_cadastre_menu)
        self._group_party_cadastre_action = QAction(
                QIcon(":/Asistente-LADM_COL/resources/images/tables.png"),
                QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Group Party"),
                self._party_cadastre_menu)
        self._party_cadastre_menu.addActions([self._col_party_cadastre_action,
                                              self._group_party_cadastre_action])

        self._source_cadastre_menu = QMenu(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Source"), self._cadastre_menu)
        self._source_cadastre_menu.setIcon(QIcon(":/Asistente-LADM_COL/resources/images/source.png"))
        self._administrative_source_cadastre_action = QAction(
                QIcon(":/Asistente-LADM_COL/resources/images/tables.png"),
                QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Administrative Source"),
                self._source_cadastre_menu)
        self._spatial_source_cadastre_action = QAction(
                QIcon(":/Asistente-LADM_COL/resources/images/tables.png"),
                QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Spatial Source"),
                self._source_cadastre_menu)
        self._upload_source_files_cadastre_action = QAction(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Upload Pending Source Files"), self._source_cadastre_menu)
        self._source_cadastre_menu.addActions([self._administrative_source_cadastre_action,
                                               self._spatial_source_cadastre_action])
        self._source_cadastre_menu.addSeparator()
        self._source_cadastre_menu.addAction(self._upload_source_files_cadastre_action)

        self._rrr_cadastre_menu = QMenu(QCoreApplication.translate("AsistenteLADMCOLPlugin", "RRR"), self._cadastre_menu)
        self._rrr_cadastre_menu.setIcon(QIcon(":/Asistente-LADM_COL/resources/images/rrr.png"))
        self._right_rrr_cadastre_action = QAction(
                QIcon(":/Asistente-LADM_COL/resources/images/tables.png"),
                QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Right"),
                self._rrr_cadastre_menu)
        self._restriction_rrr_cadastre_action = QAction(
                QIcon(":/Asistente-LADM_COL/resources/images/tables.png"),
                QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Restriction"),
                self._rrr_cadastre_menu)
        self._rrr_cadastre_menu.addActions([self._right_rrr_cadastre_action,
                                            self._restriction_rrr_cadastre_action])

        self._quality_cadastre_action = QAction(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Check Quality Rules"), self._cadastre_menu)

        self._cadastre_menu.addMenu(self._preprocessing_menu)
        self._cadastre_menu.addSeparator()
        self._cadastre_menu.addMenu(self._surveying_and_representation_cadastre_menu)
        self._cadastre_menu.addMenu(self._spatial_unit_cadastre_menu)
        self._cadastre_menu.addMenu(self._baunit_cadastre_menu)
        self._cadastre_menu.addMenu(self._party_cadastre_menu)
        self._cadastre_menu.addMenu(self._source_cadastre_menu)
        self._cadastre_menu.addMenu(self._rrr_cadastre_menu)
        self._cadastre_menu.addSeparator()
        self._cadastre_menu.addAction(self._quality_cadastre_action)

        self._menu.addMenu(self._cadastre_menu)

        # Set connections
        self._point_surveying_and_representation_cadastre_action.triggered.connect(self.show_wiz_point_cad)
        self._boundary_surveying_and_representation_cadastre_action.triggered.connect(self.show_wiz_boundaries_cad)
        self._plot_spatial_unit_cadastre_action.triggered.connect(self.show_wiz_plot_cad)
        self._parcel_baunit_cadastre_action.triggered.connect(self.show_wiz_parcel_cad)
        self._building_spatial_unit_cadastre_action.triggered.connect(self.show_wiz_building_cad)
        self._building_unit_spatial_unit_cadastre_action.triggered.connect(self.show_wiz_building_unit_cad)
        self._right_of_way_cadastre_action.triggered.connect(self.show_wiz_right_of_way_cad)
        self._extaddress_cadastre_action.triggered.connect(self.show_wiz_extaddress_cad)
        self._col_party_cadastre_action.triggered.connect(self.show_wiz_col_party_cad)
        self._group_party_cadastre_action.triggered.connect(self.show_dlg_group_party)
        self._right_rrr_cadastre_action.triggered.connect(self.show_wiz_right_rrr_cad)
        self._restriction_rrr_cadastre_action.triggered.connect(self.show_wiz_restriction_rrr_cad)
        self._administrative_source_cadastre_action.triggered.connect(self.show_wiz_administrative_source_cad)
        self._spatial_source_cadastre_action.triggered.connect(self.show_wiz_spatial_source_cad)
        self._upload_source_files_cadastre_action.triggered.connect(self.upload_source_files)
        self._quality_cadastre_action.triggered.connect(self.show_dlg_quality)

    def add_property_record_card_menu(self):
        menu = self.iface.mainWindow().findChild(QMenu, PROPERTY_RECORD_CARD_MENU_OBJECTNAME)
        if menu:
            return # Already there!

        self._property_record_card_menu = QMenu(
            QCoreApplication.translate("AsistenteLADMCOLPlugin", "Property record card"), self._menu)
        self._property_record_card_menu.setObjectName(PROPERTY_RECORD_CARD_MENU_OBJECTNAME)

        self._property_record_card_action = QAction(
            QIcon(":/Asistente-LADM_COL/resources/images/tables.png"),
            QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Property Record Card"),
            self._property_record_card_menu)

        self._property_record_card_menu.addAction(self._property_record_card_action)

        if len(self._menu.actions()) > 1:
            self._menu.insertMenu(self._menu.actions()[1], self._property_record_card_menu)
        else: # Just in case...
            self._menu.addMenu(self._property_record_card_menu)

        # Connections
        self._property_record_card_action.triggered.connect(self.show_wiz_property_record_card)

    def remove_property_record_card_menu(self):
        menu = self.iface.mainWindow().findChild(QMenu, PROPERTY_RECORD_CARD_MENU_OBJECTNAME)
        if menu is None:
            return # Nothing to remove...

        self._property_record_card_menu = None
        self._property_record_card_action = None

        menu.deleteLater()

    def add_valuation_menu(self):
        menu = self.iface.mainWindow().findChild(QMenu, VALUATION_MENU_OBJECTNAME)
        if menu:
            return  # Already there!

        self._valuation_menu = QMenu(
            QCoreApplication.translate("AsistenteLADMCOLPlugin", "Valuation"), self._menu)
        self._valuation_menu.setObjectName(VALUATION_MENU_OBJECTNAME)

        self._parcel_valuation_action = QAction(
            QIcon(":/Asistente-LADM_COL/resources/images/tables.png"),
            QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Parcel"),
            self._valuation_menu)
        self._building_unit_valuation_action = QAction(
            QIcon(":/Asistente-LADM_COL/resources/images/tables.png"),
            QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Building Unit"),
            self._valuation_menu)
        self._building_unit_qualification_valuation_action = QAction(
            QIcon(":/Asistente-LADM_COL/resources/images/tables.png"),
            QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Building Unit Qualification"),
            self._valuation_menu)
        self._geoeconomic_zone_valuation_action = QAction(
            QIcon(":/Asistente-LADM_COL/resources/images/polygons.png"),
            QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Geoeconomic Zone"),
            self._valuation_menu)
        self._physical_zone_valuation_action = QAction(
            QIcon(":/Asistente-LADM_COL/resources/images/polygons.png"),
            QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Physical Zone"),
            self._valuation_menu)

        self._valuation_menu.addAction(self._parcel_valuation_action)
        self._valuation_menu.addAction(self._building_unit_valuation_action)
        self._valuation_menu.addAction(self._building_unit_qualification_valuation_action)
        self._valuation_menu.addSeparator()
        self._valuation_menu.addAction(self._geoeconomic_zone_valuation_action)
        self._valuation_menu.addAction(self._physical_zone_valuation_action)

        if len(self._menu.actions()) > 1:
            if len(self._menu.actions()[2].text()) == 0:
                self._menu.insertMenu(self._menu.actions()[2], self._valuation_menu)
            else:
                self._menu.insertMenu(self._menu.actions()[1], self._valuation_menu)
        else: # Just in case...
            self._menu.addMenu(self._valuation_menu)

        # Connections
        self._parcel_valuation_action.triggered.connect(self.show_wiz_parcel_valuation)
        self._building_unit_valuation_action.triggered.connect(self.show_wiz_building_unit_valuation)
        self._building_unit_qualification_valuation_action.triggered.connect(
            self.show_wiz_building_unit_qualification_valuation)
        self._geoeconomic_zone_valuation_action.triggered.connect(self.show_wiz_geoeconomic_zone_valuation)
        self._physical_zone_valuation_action.triggered.connect(self.show_wiz_physical_zone_valuation_action)

    def remove_valuation_menu(self):
        menu = self.iface.mainWindow().findChild(QMenu, VALUATION_MENU_OBJECTNAME)
        if menu is None:
            return # Nothing to remove...

        self._valuation_menu = None
        self._parcel_valuation_action = None
        self._building_unit_valuation_action = None
        self._building_unit_qualification_valuation_action = None
        self._geoeconomic_zone_valuation_action = None
        self._physical_zone_valuation_action = None

        menu.deleteLater()

    def add_changes_menu(self):
        self._change_detection_menu = QMenu(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Change detection"), self._menu)
        self._query_changes_per_parcel_action = QAction(
            QCoreApplication.translate("AsistenteLADMCOLPlugin", "Query per parcel"), self._change_detection_menu)
        self._query_changes_all_parcels_action = QAction(
            QCoreApplication.translate("AsistenteLADMCOLPlugin", "Query all parcels"), self._change_detection_menu)
        self._settings_changes_action = QAction(
            QCoreApplication.translate("AsistenteLADMCOLPlugin", "Official data settings"), self._change_detection_menu)

        self._change_detection_menu.addActions([self._query_changes_per_parcel_action, self._query_changes_all_parcels_action,
                                                self._change_detection_menu.addSeparator(), self._settings_changes_action])

        self._menu.addMenu(self._change_detection_menu)

        # Set connections
        self._query_changes_per_parcel_action.triggered.connect(self.query_changes_per_parcel)
        self._query_changes_all_parcels_action.triggered.connect(self.query_changes_all_parcels)
        self._settings_changes_action.triggered.connect(self.show_official_data_settings)

    def add_supplies_menu(self):
        menu = self.iface.mainWindow().findChild(QMenu, SUPPLIES_MENU_OBJECTNAME)
        if menu:
            return  # Already there!

        self._supplies_menu = QMenu(
            QCoreApplication.translate("AsistenteLADMCOLPlugin", "Supplies"), self._menu)
        self._supplies_menu.setObjectName(SUPPLIES_MENU_OBJECTNAME)

        self._etl_cobol_supplies_action = QAction(
            QIcon(":/Asistente-LADM_COL/resources/images/tables.png"),
            QCoreApplication.translate("AsistenteLADMCOLPlugin", "load COBOL data"),
            self._supplies_menu)

        self._supplies_menu.addAction(self._etl_cobol_supplies_action)

        if len(self._menu.actions()) > 1:
            if len(self._menu.actions()[2].text()) == 0:
                self._menu.insertMenu(self._menu.actions()[2], self._supplies_menu)
            else:
                self._menu.insertMenu(self._menu.actions()[1], self._supplies_menu)
        else: # Just in case...
            self._menu.addMenu(self._supplies_menu)

        # Connections
        self._etl_cobol_supplies_action.triggered.connect(self.run_etl_cobol)

    def remove_supplies_menu(self):
        menu = self.iface.mainWindow().findChild(QMenu, SUPPLIES_MENU_OBJECTNAME)
        if menu is None:
            return # Nothing to remove...

        self._supplies_menu = None
        self._etl_cobol_supplies_action = None

    def refresh_menus(self, db, ladm_col_db):
        """
        Depending on the models available in the DB, some menus should appear or disappear from the GUI
        """
        if ladm_col_db:
            if db.cadastral_form_model_exists():
                self.add_property_record_card_menu()
            else:
                self.remove_property_record_card_menu()

            if db.valuation_model_exists():
                self.add_valuation_menu()
            else:
                self.remove_valuation_menu()

            if db.supplies_model_exists():
                self.add_supplies_menu()
            else:
                self.remove_supplies_menu()

            self.log.logMessage("Menus refreshed! Valuation: {}; Property Record Card: {}; Supplies: {}".format(
                    db.valuation_model_exists(),
                    db.cadastral_form_model_exists(),
                    db.supplies_model_exists()),
                PLUGIN_NAME,
                Qgis.Info)

    def refresh_organization_tools(self, organization):
        if organization == NATIONAL_LAND_AGENCY:
             self.configure_reports_menu()

    def add_processing_models(self, provider_id):
        if not (provider_id == 'model' or provider_id is None):
            return

        if provider_id is not None: # If method acted as slot
            QgsApplication.processingRegistry().providerAdded.disconnect(self.add_processing_models)

        # Add ladm_col models
        basepath = os.path.dirname(os.path.abspath(__file__))
        plugin_models_dir = os.path.join(basepath, "processing", "models")

        for filename in glob.glob(os.path.join(plugin_models_dir, '*.model3')):
            alg = QgsProcessingModelAlgorithm()
            if not alg.fromFile(filename):
                self.log.logMessage("Couldn't load model from {}".format(filename), PLUGIN_NAME, Qgis.Critical)
                return

            destFilename = os.path.join(ModelerUtils.modelsFolders()[0], os.path.basename(filename))
            shutil.copyfile(filename, destFilename)

        QgsApplication.processingRegistry().providerById('model').refreshAlgorithms()

    def enable_action(self, action_name, enable):
        if action_name == ANT_MAP_REPORT:
            self._ant_map_action.setEnabled(enable)
        elif action_name == ANNEX_17_REPORT:
            self._annex_17_action.setEnabled(enable)

    def refresh_map(self):
        self.iface.mapCanvas().refresh()

    def freeze_map(self, frozen):
        self.iface.mapCanvas().freeze(frozen)

    def trigger_add_feature(self):
        self.iface.actionAddFeature().trigger()

    def trigger_vertex_tool(self):
        self.iface.actionVertexTool().trigger()

    def activate_layer(self, layer):
        self.iface.layerTreeView().setCurrentLayer(layer)

    def set_node_visibility(self, node, visible=True):
        # Modes may eventually be layer_id, group_name, layer, group
        if node is not None:
            node.setItemVisibilityChecked(visible)

    def remove_error_group(self):
        group = self.qgis_utils.get_error_layers_group()
        parent = group.parent()
        parent.removeChildNode(group)

    def clear_status_bar(self):
        self.iface.statusBarIface().clearMessage()

    def clear_message_bar(self):
        self.iface.messageBar().clearWidgets()

    def create_progress_message_bar(self, text, progress):
        progressMessageBar = self.iface.messageBar().createMessage(PLUGIN_NAME, text)
        progressMessageBar.layout().addWidget(progress)
        self.iface.messageBar().pushWidget(progressMessageBar, Qgis.Info)

    def refresh_layer_symbology(self, layer_id):
        self.iface.layerTreeView().refreshLayerSymbology(layer_id)

    def run_etl_cobol(self):
        params={}
        processing.execAlgorithmDialog("model:ETL-model-supplies", params)

    def show_message(self, msg, level, duration=5):
        self.clear_message_bar()  # Remove previous messages before showing a new one
        self.iface.messageBar().pushMessage("Asistente LADM_COL", msg, level, duration)

    def show_message_with_open_table_attributes_button(self, msg, button_text, level, layer, filter):
        self.clear_message_bar()  # Remove previous messages before showing a new one
        widget = self.iface.messageBar().createMessage("Asistente LADM_COL", msg)
        button = QPushButton(widget)
        button.setText(button_text)
        button.pressed.connect(partial(self.open_table, layer, filter))
        widget.layout().addWidget(button)
        self.iface.messageBar().pushWidget(widget, level, 15)

    def show_message_to_load_layer(self, msg, button_text, layer, level):
        self.clear_message_bar()  # Remove previous messages before showing a new one
        widget = self.iface.messageBar().createMessage("Asistente LADM_COL", msg)
        button = QPushButton(widget)
        button.setText(button_text)
        button.pressed.connect(partial(self.load_layer, layer))
        widget.layout().addWidget(button)
        self.iface.messageBar().pushWidget(widget, level, 15)

    def show_message_to_load_layers(self, msg, button_text, layers, level):
        self.clear_message_bar()  # Remove previous messages before showing a new one
        widget = self.iface.messageBar().createMessage("Asistente LADM_COL", msg)
        button = QPushButton(widget)
        button.setText(button_text)
        button.pressed.connect(partial(self.load_layers, layers))
        widget.layout().addWidget(button)
        self.iface.messageBar().pushWidget(widget, level, 15)

    def show_message_to_open_about_dialog(self, msg):
        self.clear_message_bar()  # Remove previous messages before showing a new one
        widget = self.iface.messageBar().createMessage("Asistente LADM_COL", msg)
        button = QPushButton(widget)
        button.setText(QCoreApplication.translate("AsistenteLADMCOLPlugin",
            "Open About Dialog"))
        button.pressed.connect(self.show_about_dialog)
        widget.layout().addWidget(button)
        self.iface.messageBar().pushWidget(widget, Qgis.Info, 60)

    def show_message_to_download_report_dependency(self, msg):
        download_in_process = False
        # Check if report dependency downloading is in process
        for task in QgsApplication.taskManager().activeTasks():
            if URL_REPORTS_LIBRARIES in task.description():
                download_in_process = True

        if not download_in_process:
            widget = self.iface.messageBar().createMessage("Asistente LADM_COL", msg)
            button = QPushButton(widget)
            button.setText(QCoreApplication.translate("AsistenteLADMCOLPlugin",
                                                      "Download and install dependency"))
            button.pressed.connect(self.download_report_dependency)
            widget.layout().addWidget(button)
            self.clear_message_bar()  # Remove previous messages before showing a new one
            self.iface.messageBar().pushWidget(widget, Qgis.Info, 60)
        else:
            self.show_message(QCoreApplication.translate("AsistenteLADMCOLPlugin",
                                                         "Report dependency download is in progress..."),
                              Qgis.Info)

    def show_message_to_remove_report_dependency(self, msg):
        self.clear_message_bar()  # Remove previous messages before showing a new one
        widget = self.iface.messageBar().createMessage("Asistente LADM_COL", msg)
        button = QPushButton(widget)
        button.setText(QCoreApplication.translate("AsistenteLADMCOLPlugin",
            "Remove dependency"))
        button.pressed.connect(self.remove_report_dependency)
        widget.layout().addWidget(button)
        self.iface.messageBar().pushWidget(widget, Qgis.Info, 60)

    def show_message_with_settings_button(self, msg, button_text, level):
        self.clear_message_bar()  # Remove previous messages before showing a new one
        widget = self.iface.messageBar().createMessage("Asistente LADM_COL", msg)
        button = QPushButton(widget)
        button.setText(button_text)
        button.pressed.connect(self.show_settings)
        widget.layout().addWidget(button)
        self.iface.messageBar().pushWidget(widget, level, 25)

    def show_message_with_close_wizard_button(self, msg, button_text, level):
        self.clear_message_bar()  # Remove previous messages before showing a new one
        widget = self.iface.messageBar().createMessage("Asistente LADM_COL", msg)
        button = QPushButton(widget)
        button.setText(button_text)
        button.pressed.connect(self.close_wizard_if_opened)
        widget.layout().addWidget(button)
        self.iface.messageBar().pushWidget(widget, level, 25)

    def show_status_bar_message(self, msg, duration):
        self.iface.statusBarIface().showMessage(msg, duration)

    def load_layer(self, layer):
        self.qgis_utils.get_layer(self.get_db_connection(), layer[0], layer[1], load=True)

    def load_layers(self, layers):
        self.qgis_utils.get_layers(self.get_db_connection(), layers, True)

    def zoom_to_features(self, layer, ids=list(), t_ids=list(), duration=500):
        if t_ids:
            features = self.ladm_data.get_features_from_t_ids(layer, t_ids, True, True)
            for feature in features:
                ids.append(feature.id())

        self.iface.mapCanvas().zoomToFeatureIds(layer, ids)
        self.iface.mapCanvas().flashFeatureIds(layer,
                                               ids,
                                               QColor(255, 0, 0, 255),
                                               QColor(255, 0, 0, 0),
                                               flashes=1,
                                               duration=duration)

    def show_log_quality_message(self, msg, count):
        self.progressMessageBar = self.iface.messageBar().createMessage("Asistente LADM_COL", msg)
        self.progress = QProgressBar()
        self.progress.setFixedWidth(80)
        self.log_quality_total_rule_count = count
        self.progress.setMaximum(self.log_quality_total_rule_count * 10)
        self.progressMessageBar.layout().addWidget(self.progress)
        self.iface.messageBar().pushWidget(self.progressMessageBar, Qgis.Info)
        self.progress_count = 0
        self.log_quality_current_rule_count = 0

    def show_log_quality_button(self):
        self.button = QPushButton(self.progressMessageBar)
        self.button.pressed.connect(self.show_log_quality_dialog)
        self.button.setText(QCoreApplication.translate("LogQualityDialog", "Show Results"))
        self.progressMessageBar.layout().addWidget(self.button)
        QCoreApplication.processEvents()

    def set_log_quality_initial_progress(self, msg):
        self.progress_count += 2 # 20% of the current rule
        self.progress.setValue(self.progress_count)
        self.progressMessageBar.setText(
            QCoreApplication.translate("LogQualityDialog",
                                       "Checking {} out of {}: '{}'").format(
                                        self.log_quality_current_rule_count + 1,
                                        self.log_quality_total_rule_count,
                                        msg))
        QCoreApplication.processEvents()

    def set_log_quality_final_progress(self, msg):
        self.progress_count += 8 # 80% of the current rule
        self.progress.setValue(self.progress_count)
        self.log_quality_current_rule_count += 1
        if self.log_quality_current_rule_count ==  self.log_quality_total_rule_count:
            self.progressMessageBar.setText(QCoreApplication.translate("LogQualityDialog",
                "All the {} quality rules were checked! Click the button at the right-hand side to see a report.").format(self.log_quality_total_rule_count))
        else:
            self.progressMessageBar.setText(msg)
        QCoreApplication.processEvents()
    
    def show_log_quality_dialog(self):
        dlg = LogQualityDialog(self.qgis_utils, self.quality, self.conn_manager.get_db_connector_from_source())
        dlg.exec_()

    def show_log_excel_button(self, text):
        self.progressMessageBar = self.iface.messageBar().createMessage("Import from Excel",
            QCoreApplication.translate("ImportFromExcelDialog",
                                       "Some errors were found while importing from the intermediate Excel file into LADM-COL!"))
        self.button = QPushButton(self.progressMessageBar)
        self.button.pressed.connect(self.show_log_excel_dialog)
        self.button.setText(QCoreApplication.translate("ImportFromExcelDialog", "Show errors found"))
        self.progressMessageBar.layout().addWidget(self.button)
        self.iface.messageBar().pushWidget(self.progressMessageBar, Qgis.Warning)
        self.text = text

    def show_log_excel_dialog(self):
        dlg = LogExcelDialog(self.qgis_utils, self.text)
        dlg.exec_()

    @_validate_if_wizard_is_open
    @_qgis_model_baker_required
    @_db_connection_required
    def call_explode_boundaries(self, *args):
        self.toolbar.build_boundary(self.get_db_connection())

    @_validate_if_wizard_is_open
    @_qgis_model_baker_required
    @_db_connection_required
    def call_topological_editing(self, *args):
        self.toolbar.enable_topological_editing(self.get_db_connection())

    @_validate_if_wizard_is_open
    @_qgis_model_baker_required
    @_db_connection_required
    def call_fill_topology_table_pointbfs(self, *args):
        self.toolbar.fill_topology_table_pointbfs(self.get_db_connection())

    @_validate_if_wizard_is_open
    @_qgis_model_baker_required
    @_db_connection_required
    def call_fill_topology_tables_morebfs_less(self, *args):
        self.toolbar.fill_topology_tables_morebfs_less(self.get_db_connection())

    @_validate_if_wizard_is_open
    @_qgis_model_baker_required
    @_db_connection_required
    @_activate_processing_plugin
    def call_fill_right_of_way_relations(self, *args):
        self.right_of_way.fill_right_of_way_relations(self.get_db_connection())

    @_validate_if_wizard_is_open
    @_qgis_model_baker_required
    @_db_connection_required
    def call_ant_map_report_generation(self, *args):
        self.report_generator.generate_report(self.get_db_connection(), ANT_MAP_REPORT)

    @_validate_if_wizard_is_open
    @_qgis_model_baker_required
    @_db_connection_required
    def call_annex_17_report_generation(self, *args):
        self.report_generator.generate_report(self.get_db_connection(), ANNEX_17_REPORT)

    @_validate_if_wizard_is_open
    @_qgis_model_baker_required
    @_db_connection_required
    @_activate_processing_plugin
    def call_import_from_intermediate_structure(self, *args):
        self._dlg = ImportFromExcelDialog(self.iface, self.get_db_connection(), self.qgis_utils)
        self._dlg.log_excel_show_message_emitted.connect(self.show_log_excel_button)
        self._dlg.exec_()

    def unload(self):
        self.uninstall_custom_expression_functions()

        # Remove toolbars actions
        toolbars_actions = ['_build_boundary_action',
                            '_topological_editing_action',
                            '_fill_point_BFS_action',
                            '_fill_more_BFS_less_action',
                            '_fill_right_of_way_relations_action',
                            '_import_from_intermediate_structure_action']
        self.delete_variables(toolbars_actions)

        # Remove cadastre actions
        cadastre_actions = ['_controlled_measurement_action',
                            '_point_surveying_and_representation_cadastre_action',
                            '_boundary_surveying_and_representation_cadastre_action',
                            '_plot_spatial_unit_cadastre_action',
                            '_building_spatial_unit_cadastre_action',
                            '_building_unit_spatial_unit_cadastre_action',
                            '_right_of_way_cadastre_action',
                            '_extaddress_cadastre_action',
                            '_parcel_baunit_cadastre_action',
                            '_col_party_cadastre_action',
                            '_group_party_cadastre_action',
                            '_administrative_source_cadastre_action',
                            '_spatial_source_cadastre_action',
                            '_upload_source_files_cadastre_action',
                            '_right_rrr_cadastre_action',
                            '_restriction_rrr_cadastre_action',
                            '_quality_cadastre_action']
        self.delete_variables(cadastre_actions)

        # Remove property record card actions
        property_record_card_actions = ['_property_record_card_action']
        self.delete_variables(property_record_card_actions)

        # Remove valuation actions
        valuation_actions = ['_parcel_valuation_action',
                             '_building_unit_valuation_action',
                             '_building_unit_qualification_valuation_action',
                             '_geoeconomic_zone_valuation_action',
                             '_physical_zone_valuation_action']
        self.delete_variables(valuation_actions)

        # Remove queries action
        query_actions = ['_queries_action',
                         '_query_changes_per_parcel_action',
                         '_query_changes_all_parcels_action']
        self.delete_variables(query_actions)

        # Remove reports actions
        reports_actions = ['_annex_17_action',
                           '_ant_map_action']
        self.delete_variables(reports_actions)

        # Remove data management actions
        data_management_actions = ['_import_schema_action',
                                   '_import_data_action',
                                   '_export_data_action']
        self.delete_variables(data_management_actions)

        # Remove other actions
        actions = ['_load_layers_action',
                   '_settings_action',
                   '_settings_changes_action',  # Official database connection settings
                   '_help_action',
                   '_about_action']
        self.delete_variables(actions)

        # Remove menus
        menus = ['_cadastre_menu',
                 '_property_record_card_menu',
                 '_valuation_menu',
                 '_report_menu',
                 '_change_detection_menu',
                 '_data_management_menu',
                 '_menu']
        self.delete_variables(menus)

        # remove the plugin menu item and icon
        self._menu.deleteLater()
        self.iface.mainWindow().removeToolBar(self._ladm_col_toolbar)
        del self._ladm_col_toolbar

        # Close all connections
        self.conn_manager.close_db_connections()
        QgsApplication.processingRegistry().removeProvider(self.ladm_col_provider)

    def delete_variables(self, variables):
        for name_variable in variables:
            if hasattr(self, name_variable):
                variable = getattr(self, name_variable)
                del variable

    @_validate_if_wizard_is_open
    def show_settings(self, *args):
        dlg = SettingsDialog(qgis_utils=self.qgis_utils, conn_manager=self.conn_manager)

        # Connect signals (DBUtils, QgisUtils)
        dlg.db_connection_changed.connect(self.conn_manager.db_connection_changed)
        dlg.db_connection_changed.connect(self.qgis_utils.cache_layers_and_relations)
        dlg.organization_tools_changed.connect(self.qgis_utils.organization_tools_changed)

        dlg.set_action_type(EnumDbActionType.CONFIG)
        dlg.exec_()

    def show_settings_clear_message_bar(self):
        self.clear_message_bar()
        self.show_settings()

    def show_plugin_manager(self):
        self.iface.actionManagePlugins().trigger()

    @_qgis_model_baker_required
    @_db_connection_required
    def load_layers_from_qgis_model_baker(self, *args):
        dlg = LoadLayersDialog(self.iface, self.get_db_connection(), self.qgis_utils)
        dlg.exec_()

    @_validate_if_wizard_is_open
    @_qgis_model_baker_required
    @_db_connection_required
    def show_queries(self, *args):
        if self._dock_widget_queries is not None:
            self._dock_widget_queries.close()
            self._dock_widget_queries = None

        self._dock_widget_queries = DockWidgetQueries(self.iface,
                                                      self.get_db_connection(),
                                                      self.qgis_utils,
                                                      self.ladm_data)
        self.conn_manager.db_connection_changed.connect(self._dock_widget_queries.update_db_connection)
        self._dock_widget_queries.zoom_to_features_requested.connect(self.zoom_to_features)
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self._dock_widget_queries)

    def get_db_connection(self):
        return self.conn_manager.get_db_connector_from_source()

    def get_official_db_connection(self):
        return self.conn_manager.get_db_connector_from_source(db_source=OFFICIAL_DB_SOURCE)

    def call_dlg_import_schema(self, state):
        """
        Slot triggered by a menu
        :param state: Checked state
        :return:
        """
        self.show_dlg_import_schema(list())  # Parameter: No other models selected other than default models

    @_validate_if_wizard_is_open
    @_qgis_model_baker_required
    def show_dlg_import_schema(self, *args):
        from .gui.qgis_model_baker.dlg_import_schema import DialogImportSchema

        selected_models_import_schema = list()
        if args:
            selected_models_import_schema = args[0]  # Argument sent by signal

        dlg = DialogImportSchema(self.iface, self.qgis_utils, self.conn_manager, selected_models_import_schema)
        dlg.models_have_changed.connect(self.refresh_menus)
        dlg.open_dlg_import_data.connect(self.show_dlg_import_data)
        dlg.exec_()

    @_validate_if_wizard_is_open
    @_qgis_model_baker_required
    def show_dlg_import_data(self, *args):
        from .gui.qgis_model_baker.dlg_import_data import DialogImportData
        dlg = DialogImportData(self.iface, self.qgis_utils, self.conn_manager)
        dlg.open_dlg_import_schema.connect(self.show_dlg_import_schema)
        dlg.exec_()

    @_validate_if_wizard_is_open
    @_qgis_model_baker_required
    def show_dlg_export_data(self, *args):
        from .gui.qgis_model_baker.dlg_export_data import DialogExportData
        dlg = DialogExportData(self.iface, self.qgis_utils, self.conn_manager)
        dlg.exec_()

    @_validate_if_wizard_is_open
    @_qgis_model_baker_required
    @_activate_processing_plugin
    def show_dlg_controlled_measurement(self, *args):
        dlg = ControlledMeasurementDialog(self.qgis_utils)
        dlg.exec_()

    @_validate_if_wizard_is_open
    @_qgis_model_baker_required
    @_db_connection_required
    def show_wiz_point_cad(self, *args):
        self.wiz = CreatePointsCadastreWizard(self.iface, self.get_db_connection(), self.qgis_utils)
        self.exec_wizard(self.wiz)

    def show_wiz_boundaries_cad(self):
        self.show_wizard(WIZARD_CREATE_BOUNDARY_CADASTRE)

    def set_wizard_is_open_flag(self, open):
        """
        Slot for wizards to notify when they are open or closed

        :param open: boolean
        """
        self.is_wizard_open = open

    def set_enable_finalize_geometry_creation_action(self, enable):
        """
        Slot for wizards to notify when the finalize_geometry_creation action should be enabled/disabled

        :param enable: boolean
        """
        self._finalize_geometry_creation_action.setEnabled(enable)

    def show_wiz_plot_cad(self):
        self.show_wizard(WIZARD_CREATE_PLOT_CADASTRE)

    def show_wiz_building_cad(self):
        self.show_wizard(WIZARD_CREATE_BUILDING_CADASTRE)

    def show_wiz_building_unit_cad(self):
        self.show_wizard(WIZARD_CREATE_BUILDING_UNIT_CADASTRE)

    def show_wiz_right_of_way_cad(self):
        self.show_wizard(WIZARD_CREATE_RIGHT_OF_WAY_CADASTRE)

    def show_wiz_extaddress_cad(self):
        self.show_wizard(WIZARD_CREATE_EXT_ADDRESS_CADASTRE)

    def show_wiz_parcel_cad(self):
        self.show_wizard(WIZARD_CREATE_PARCEL_CADASTRE)

    def show_wiz_col_party_cad(self):
        self.show_wizard(WIZARD_CREATE_COL_PARTY_CADASTRAL)

    @_validate_if_wizard_is_open
    @_qgis_model_baker_required
    @_db_connection_required
    def show_dlg_group_party(self, *args):
        namespace_enabled = QSettings().value('Asistente-LADM_COL/automatic_values/namespace_enabled', True, bool)
        local_id_enabled = QSettings().value('Asistente-LADM_COL/automatic_values/local_id_enabled', True, bool)

        if not namespace_enabled or not local_id_enabled:
            self.show_message_with_settings_button(QCoreApplication.translate("CreateGroupPartyCadastre",
                                                       "First enable automatic values for both namespace and local_id fields before creating group parties. Click the button to open the settings dialog."),
                                                   QCoreApplication.translate("CreateGroupPartyCadastre", "Open Settings"),
                                                   Qgis.Info)
            return

        dlg = CreateGroupPartyCadastre(self.iface, self.get_db_connection(), self.qgis_utils)

        # Check if required layers are available
        if dlg.required_layers_are_available():
            # Load required data, it is necessary in the dlg
            dlg.load_parties_data()
            dlg.exec_()
        else:
            del dlg

    def show_wiz_right_rrr_cad(self):
        self.show_wizard(WIZARD_CREATE_RIGHT_CADASTRE)

    def show_wiz_restriction_rrr_cad(self):
        self.show_wizard(WIZARD_CREATE_RESTRICTION_CADASTRE)

    def show_wiz_administrative_source_cad(self):
        self.show_wizard(WIZARD_CREATE_ADMINISTRATIVE_SOURCE_CADASTRE)

    def show_wiz_spatial_source_cad(self):
        self.show_wizard(WIZARD_CREATE_SPATIAL_SOURCE_CADASTRE)

    @_validate_if_wizard_is_open
    @_qgis_model_baker_required
    @_db_connection_required
    def upload_source_files(self, *args):
        self.qgis_utils.upload_source_files(self.get_db_connection())

    @_validate_if_wizard_is_open
    @_qgis_model_baker_required
    @_db_connection_required
    @_activate_processing_plugin
    def show_dlg_quality(self, *args):
        dlg = QualityDialog(self.get_db_connection(), self.qgis_utils, self.quality)
        dlg.exec_()

    def show_wiz_property_record_card(self):
        # TODO: Remove
        pass

    def show_wiz_parcel_valuation(self):
        # TODO: Remove
        pass

    def show_wiz_building_unit_valuation(self):
        self.show_wizard(WIZARD_CREATE_BUILDING_UNIT_VALUATION)

    def show_wiz_building_unit_qualification_valuation(self):
        self.show_wizard(WIZARD_CREATE_BUILDING_UNIT_QUALIFICATION_VALUATION)

    def show_wiz_geoeconomic_zone_valuation(self):
        self.show_wizard(WIZARD_CREATE_GEOECONOMIC_ZONE_VALUATION)

    def show_wiz_physical_zone_valuation_action(self):
        self.show_wizard(WIZARD_CREATE_PHYSICAL_ZONE_VALUATION)

    @_validate_if_wizard_is_open
    @_qgis_model_baker_required
    @_map_swipe_tool_required
    @_db_connection_required
    @_official_db_connection_required
    @_different_db_connections_required
    def query_changes_per_parcel(self, *args):
        with OverrideCursor(Qt.WaitCursor):
            self.show_change_detection_dockwidget(False)  # all_parcels_mode is False, we want the per_parcel_mode instead

    @_validate_if_wizard_is_open
    @_qgis_model_baker_required
    @_map_swipe_tool_required
    @_db_connection_required
    @_official_db_connection_required
    @_different_db_connections_required
    def query_changes_all_parcels(self, *args):
        with OverrideCursor(Qt.WaitCursor):
            self.show_change_detection_dockwidget()

    def show_change_detection_dockwidget(self, all_parcels_mode=True):
        if self._dock_widget_change_detection is not None:
            self._dock_widget_change_detection.close()
            self._dock_widget_change_detection = None

        self._dock_widget_change_detection = DockWidgetChangeDetection(self.iface,
                                                                       self.get_db_connection(),
                                                                       self.get_official_db_connection(),
                                                                       self.qgis_utils,
                                                                       self.ladm_data,
                                                                       all_parcels_mode)
        self.conn_manager.db_connection_changed.connect(self._dock_widget_change_detection.update_db_connection)
        self.conn_manager.official_db_connection_changed.connect(self._dock_widget_change_detection.update_db_connection)
        self._dock_widget_change_detection.zoom_to_features_requested.connect(self.zoom_to_features)
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self._dock_widget_change_detection)

    def show_official_data_settings(self):
        dlg = OfficialDataSettingsDialog(qgis_utils=self.qgis_utils, conn_manager=self.conn_manager)
        dlg.official_db_connection_changed.connect(self.conn_manager.official_db_connection_changed)
        dlg.exec_()

    def show_official_data_settings_clear_message_bar(self):
        self.clear_message_bar()
        self.show_official_data_settings()

    def open_table(self, layer, filter=None):
        self.iface.showAttributeTable(layer, filter)

    def download_report_dependency(self):
        self.report_generator.download_report_dependency()

    def remove_report_dependency(self):
        self.report_generator.remove_report_dependency()

    def show_help(self):
        self.qgis_utils.show_help()

    def show_about_dialog(self):
        if self._about_dialog is None:
            self._about_dialog = AboutDialog(self.qgis_utils)
            self._about_dialog.message_with_button_open_about_emitted.connect(self.show_message_to_open_about_dialog)
        else:
            self._about_dialog.check_local_help()

        rich_text = '<html><head/><body><p align="center"><a href="{release_url}{version}"><span style=" font-size:10pt; text-decoration: underline; color:#0000ff;">v{version}</span></a></p></body></html>'
        self._about_dialog.lbl_version.setText(rich_text.format(release_url=RELEASE_URL, version=PLUGIN_VERSION))
        self._about_dialog.exec_()

    def exec_wizard(self, wiz):
        # Check if required layers are available
        if wiz.required_layers_are_available():
            wiz.exec_()
        else:
            self.is_wizard_open = False
            del wiz

    @_activate_processing_plugin
    @_validate_if_wizard_is_open
    @_qgis_model_baker_required
    @_db_connection_required
    def show_wizard(self, wizard_name, *args, **kwargs):
        wiz_settings = deepcopy(WIZARDS_SETTINGS[wizard_name])
        if self.qgis_utils.required_layers_are_available(self.get_db_connection(),
                                                      wiz_settings[WIZARD_LAYERS],
                                                      wiz_settings[WIZARD_TOOL_NAME]):

            if wiz_settings[WIZARD_LAYERS] is not None:
                self.wiz = wiz_settings[WIZARD_CLASS](self.iface, self.get_db_connection(), self.qgis_utils,
                                                      wiz_settings)
                if wiz_settings[WIZARD_TYPE] & WizardTypeEnum.SPATIAL_WIZARD:
                    # Required signal for wizard geometry creating
                    self.wiz.set_finalize_geometry_creation_enabled_emitted.connect(self.set_enable_finalize_geometry_creation_action)
                    self.wiz_geometry_creation_finished.connect(self.wiz.save_created_geometry)

                # Required signal that allow to know if there is a wizard opened
                self.is_wizard_open = True
                self.wiz.update_wizard_is_open_flag.connect(self.set_wizard_is_open_flag)

                if self.wiz:
                    self.wiz.exec_()

    def close_wizard_if_opened(self):
        if self.wiz:
            self.wiz.close_wizard()  # This updates the is_wizard_open flag
