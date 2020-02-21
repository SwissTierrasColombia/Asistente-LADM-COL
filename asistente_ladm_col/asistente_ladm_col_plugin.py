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
from functools import partial

import qgis.utils
from processing.modeler.ModelerUtils import ModelerUtils
from qgis.PyQt.QtCore import (Qt,
                              QObject,
                              QCoreApplication,
                              QSettings,
                              pyqtSignal)
from qgis.PyQt.QtGui import QIcon, QColor
from qgis.PyQt.QtWidgets import (QAction,
                                 QPushButton,
                                 QProgressBar,
                                 QMessageBox)
from qgis.core import (Qgis,
                       QgsApplication,
                       QgsProcessingModelAlgorithm,
                       QgsExpression)

from asistente_ladm_col.config.enums import (EnumDbActionType,
                                             WizardTypeEnum,
                                             LogHandlerEnum,
                                             EnumUserLevel)
from asistente_ladm_col.config.general_config import (ANNEX_17_REPORT,
                                                      ANT_MAP_REPORT,
                                                      DEFAULT_LOG_MODE,
                                                      SUPPLIES_DB_SOURCE,
                                                      PLUGIN_NAME,
                                                      PLUGIN_VERSION,
                                                      RELEASE_URL,
                                                      URL_REPORTS_LIBRARIES,
                                                      DEPENDENCY_REPORTS_DIR_NAME,
                                                      COLLECTED_DB_SOURCE, WIZARD_CLASS, 
                                                      WIZARD_TOOL_NAME, 
                                                      WIZARD_TYPE,
                                                      WIZARD_LAYERS, 
                                                      WIZARD_CREATE_COL_PARTY_CADASTRAL,
                                                      WIZARD_CREATE_ADMINISTRATIVE_SOURCE_OPERATION,
                                                      WIZARD_CREATE_BOUNDARY_OPERATION,
                                                      WIZARD_CREATE_BUILDING_OPERATION,
                                                      WIZARD_CREATE_BUILDING_UNIT_OPERATION,
                                                      WIZARD_CREATE_RIGHT_OPERATION,
                                                      WIZARD_CREATE_RESTRICTION_OPERATION,
                                                      WIZARD_CREATE_SPATIAL_SOURCE_OPERATION,
                                                      WIZARD_CREATE_PARCEL_OPERATION, WIZARD_CREATE_PLOT_OPERATION,
                                                      WIZARD_CREATE_EXT_ADDRESS_OPERATION,
                                                      WIZARD_CREATE_RIGHT_OF_WAY_OPERATION,
                                                      WIZARD_CREATE_GEOECONOMIC_ZONE_VALUATION,
                                                      WIZARD_CREATE_PHYSICAL_ZONE_VALUATION,
                                                      WIZARD_CREATE_BUILDING_UNIT_VALUATION,
                                                      WIZARD_CREATE_BUILDING_UNIT_QUALIFICATION_VALUATION)
from asistente_ladm_col.config.task_steps_config import TaskStepsConfig
from asistente_ladm_col.config.translation_strings import (TOOLBAR_FINALIZE_GEOMETRY_CREATION,
                                                           TOOLBAR_BUILD_BOUNDARY,
                                                           TOOLBAR_MOVE_NODES,
                                                           TOOLBAR_FILL_POINT_BFS,
                                                           TOOLBAR_FILL_MORE_BFS_LESS,
                                                           TOOLBAR_FILL_RIGHT_OF_WAY_RELATIONS,
                                                           TOOLBAR_IMPORT_FROM_INTERMEDIATE_STRUCTURE)
from asistente_ladm_col.config.wizard_config import (WizardConfig)
from asistente_ladm_col.config.expression_functions import (get_domain_code_from_value,
                                                            get_domain_value_from_code)  # >> DON'T REMOVE << Registers it in QgsExpression
from asistente_ladm_col.config.gui.common_keys import *
from asistente_ladm_col.gui.transitional_system.dlg_login_st import LoginSTDialog
from asistente_ladm_col.gui.gui_builder.gui_builder import GUI_Builder
from asistente_ladm_col.gui.transitional_system.dockwidget_transitional_system import DockWidgetTransitionalSystem
from asistente_ladm_col.lib.transitional_system.st_session.st_session import STSession
from asistente_ladm_col.logic.ladm_col.ladm_data import LADM_DATA
from asistente_ladm_col.gui.change_detection.dockwidget_change_detection import DockWidgetChangeDetection
from asistente_ladm_col.gui.dialogs.dlg_about import AboutDialog
from asistente_ladm_col.gui.dialogs.dlg_import_from_excel import ImportFromExcelDialog
from asistente_ladm_col.gui.dialogs.dlg_load_layers import LoadLayersDialog
from asistente_ladm_col.gui.dialogs.dlg_log_excel import LogExcelDialog
from asistente_ladm_col.gui.supplies.dlg_etl_cobol import ETLCobolDialog
from asistente_ladm_col.gui.supplies.dlg_missing_cobol_supplies import MissingCobolSupplies
from asistente_ladm_col.gui.dialogs.dlg_log_quality import LogQualityDialog
from asistente_ladm_col.gui.dialogs.dlg_quality import QualityDialog
from asistente_ladm_col.gui.dialogs.dlg_settings import SettingsDialog
from asistente_ladm_col.gui.dialogs.dlg_welcome_screen import WelcomeScreenDialog
from asistente_ladm_col.gui.queries.dockwidget_queries import DockWidgetQueries
from asistente_ladm_col.gui.reports.reports import ReportGenerator
from asistente_ladm_col.gui.right_of_way import RightOfWay
from asistente_ladm_col.gui.toolbar import ToolBar
from asistente_ladm_col.gui.transitional_system.dlg_upload_file import STUploadFileDialog
from asistente_ladm_col.gui.wizards.operation.dlg_create_group_party_operation import CreateGroupPartyOperation
from asistente_ladm_col.gui.wizards.operation.wiz_create_points_operation import CreatePointsOperationWizard
from asistente_ladm_col.lib.db.db_connection_manager import ConnectionManager
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.lib.processing.ladm_col_provider import LADMCOLAlgorithmProvider
from asistente_ladm_col.utils.decorators import (_db_connection_required,
                                                 _validate_if_wizard_is_open,
                                                 _qgis_model_baker_required,
                                                 _activate_processing_plugin,
                                                 _map_swipe_tool_required,
                                                 _supplies_db_connection_required,
                                                 _supplies_model_required,
                                                 _valuation_model_required,
                                                 _operation_model_required,
                                                 _different_db_connections_required)
from asistente_ladm_col.utils.utils import Utils
from asistente_ladm_col.utils.qgis_utils import QGISUtils
from asistente_ladm_col.utils.qt_utils import ProcessWithStatus
from asistente_ladm_col.logic.quality.quality import QualityUtils
from asistente_ladm_col.resources_rc import *  # Necessary to show icons


class AsistenteLADMCOLPlugin(QObject):
    wiz_geometry_creation_finished = pyqtSignal()

    def __init__(self, iface, unit_tests=False):
        QObject.__init__(self)
        self.iface = iface
        self.unit_tests = unit_tests
        self.main_window = self.iface.mainWindow()
        self._about_dialog = None
        self._dock_widget_queries = None
        self._dock_widget_change_detection = None
        self._dock_widget_transitional_system = None
        self.toolbar = None
        self.wiz_address = None
        self.qgis_utils = QGISUtils(self.iface.layerTreeView())
        self.conn_manager = ConnectionManager(self.qgis_utils)
        self.wiz = None
        self.is_wizard_open = False  # Helps to make the plugin modules aware of open wizards
        self.wizard_config = WizardConfig()
        self.logger = Logger()
        self.logger.set_mode(DEFAULT_LOG_MODE)
        self.gui_builder = GUI_Builder(self.iface)
        self.session = STSession()
        task_steps_config = TaskStepsConfig()
        task_steps_config.set_slot_caller(self)

    def initGui(self):
        self.right_of_way = RightOfWay(self.iface, self.qgis_utils, self.get_db_connection().names)
        self.quality = QualityUtils(self.qgis_utils)
        self.toolbar = ToolBar(self.iface, self.qgis_utils)
        self.ladm_data = LADM_DATA(self.qgis_utils)
        self.report_generator = ReportGenerator(self.qgis_utils, self.ladm_data)

        self.create_actions()
        self.set_connections()

        if not self.unit_tests:
            # Ask for role name before building the GUI, only the first time the plugin is run
            if self.gui_builder.show_welcome_screen():
                dlg_welcome = WelcomeScreenDialog(self.qgis_utils, self.main_window)
                dlg_welcome.exec_()

        if not qgis.utils.active_plugins:
            self.iface.initializationCompleted.connect(self.call_refresh_gui)
        else:
            self.call_refresh_gui()

        # Add LADM_COL provider and models to QGIS
        self.ladm_col_provider = LADMCOLAlgorithmProvider()
        QgsApplication.processingRegistry().addProvider(self.ladm_col_provider)
        if QgsApplication.processingRegistry().providerById('model'):
            self.add_processing_models(None)
        else: # We need to wait until processing is initialized
            QgsApplication.processingRegistry().providerAdded.connect(self.add_processing_models)

    def create_actions(self):
        self.create_supplies_actions()
        self.create_operation_actions()
        self.create_cadastre_form_actions()
        self.create_valuation_actions()
        self.create_change_detection_actions()
        self.create_toolbar_actions()
        self.create_transitional_system_actions()
        self.create_generic_actions()

    def set_connections(self):
        self.conn_manager.db_connection_changed.connect(self.refresh_gui)

        self.logger.message_with_duration_emitted.connect(self.show_message)
        self.logger.status_bar_message_emitted.connect(self.show_status_bar_message)
        self.logger.clear_status_bar_emitted.connect(self.clear_status_bar)
        self.logger.clear_message_bar_emitted.connect(self.clear_message_bar)
        self.logger.message_with_button_load_layer_emitted.connect(self.show_message_to_load_layer)
        self.logger.message_with_button_open_table_attributes_emitted.connect(
            self.show_message_with_open_table_attributes_button)
        self.logger.message_with_button_download_report_dependency_emitted.connect(
            self.show_message_to_download_report_dependency)
        self.logger.message_with_button_remove_report_dependency_emitted.connect(
            self.show_message_to_remove_report_dependency)

        self.qgis_utils.action_add_feature_requested.connect(self.trigger_add_feature)
        self.qgis_utils.action_vertex_tool_requested.connect(self.trigger_vertex_tool)
        self.qgis_utils.activate_layer_requested.connect(self.activate_layer)
        self.qgis_utils.create_progress_message_bar_emitted.connect(self.create_progress_message_bar)
        self.qgis_utils.remove_error_group_requested.connect(self.remove_error_group)
        self.qgis_utils.layer_symbology_changed.connect(self.refresh_layer_symbology)
        self.qgis_utils.map_refresh_requested.connect(self.refresh_map)
        self.qgis_utils.map_freeze_requested.connect(self.freeze_map)
        self.qgis_utils.set_node_visibility_requested.connect(self.set_node_visibility)

        self.quality.log_quality_show_message_emitted.connect(self.show_log_quality_message)
        self.quality.log_quality_show_button_emitted.connect(self.show_log_quality_button)
        self.quality.log_quality_set_initial_progress_emitted.connect(self.set_log_quality_initial_progress)
        self.quality.log_quality_set_final_progress_emitted.connect(self.set_log_quality_final_progress)

        self.report_generator.enable_action_requested.connect(self.enable_action)

        self.session.login_status_changed.connect(self.set_login_controls_visibility)

    @staticmethod
    def uninstall_custom_expression_functions():
        QgsExpression.unregisterFunction('get_domain_code_from_value')
        QgsExpression.unregisterFunction('get_domain_value_from_code')

    def call_refresh_gui(self):
        """
        SLOT. Intermediate step to call refresh gui with proper parameters.
        """
        self.refresh_gui(self.get_db_connection(), None, COLLECTED_DB_SOURCE)  # 3rd value is required to refresh GUI

    def refresh_gui(self, db, res, db_source):
        if db_source == COLLECTED_DB_SOURCE:
            msg = QCoreApplication.translate("AsistenteLADMCOLPlugin", "Refreshing GUI for the LADM_COL Assistant...")
            with ProcessWithStatus(msg):
                self.gui_builder.build_gui(db, res)

    def create_toolbar_actions(self):
        self._finalize_geometry_creation_action = QAction(
            QIcon(":/Asistente-LADM_COL/resources/images/mActionFinalizeGeometryCreation.svg"),
            TOOLBAR_FINALIZE_GEOMETRY_CREATION,
            self.main_window)
        self._finalize_geometry_creation_action.triggered.connect(
            self.wiz_geometry_creation_finished)  # SIGNAL chaining
        self._finalize_geometry_creation_action.setEnabled(False)

        self._build_boundary_action = QAction(QIcon(":/Asistente-LADM_COL/resources/images/build_boundaries.svg"),
                                              TOOLBAR_BUILD_BOUNDARY, self.main_window)
        self._build_boundary_action.triggered.connect(self.call_explode_boundaries)

        self._topological_editing_action = QAction(QIcon(":/Asistente-LADM_COL/resources/images/move_nodes.svg"),
            TOOLBAR_MOVE_NODES, self.main_window)
        self._topological_editing_action.triggered.connect(self.call_topological_editing)

        self._fill_point_BFS_action = QAction(QIcon(":/Asistente-LADM_COL/resources/images/relationships.svg"),
                                              TOOLBAR_FILL_POINT_BFS,
                                              self.main_window)
        self._fill_point_BFS_action.triggered.connect(self.call_fill_topology_table_pointbfs)

        self._fill_more_BFS_less_action = QAction(QIcon(":/Asistente-LADM_COL/resources/images/relationships.svg"),
                                                  TOOLBAR_FILL_MORE_BFS_LESS,
                                                  self.main_window)
        self._fill_more_BFS_less_action.triggered.connect(self.call_fill_topology_tables_morebfs_less)

        self._fill_right_of_way_relations_action = QAction(QIcon(":/Asistente-LADM_COL/resources/images/relationships.svg"),
                                                           TOOLBAR_FILL_RIGHT_OF_WAY_RELATIONS, self.main_window)
        self._fill_right_of_way_relations_action.triggered.connect(self.call_fill_right_of_way_relations)

        self._import_from_intermediate_structure_action = QAction(
            QIcon(":/Asistente-LADM_COL/resources/images/excel.svg"),
            TOOLBAR_IMPORT_FROM_INTERMEDIATE_STRUCTURE,
            self.main_window)
        self._import_from_intermediate_structure_action.triggered.connect(self.call_import_from_intermediate_structure)

        self.gui_builder.register_actions({
            ACTION_FINALIZE_GEOMETRY_CREATION: self._finalize_geometry_creation_action,
            ACTION_BUILD_BOUNDARY: self._build_boundary_action,
            ACTION_MOVE_NODES: self._topological_editing_action,
            ACTION_FILL_BFS: self._fill_point_BFS_action,
            ACTION_FILL_MORE_BFS_AND_LESS: self._fill_more_BFS_less_action,
            ACTION_FILL_RIGHT_OF_WAY_RELATIONS: self._fill_right_of_way_relations_action,
            ACTION_IMPORT_FROM_INTERMEDIATE_STRUCTURE: self._import_from_intermediate_structure_action})

    def create_transitional_system_actions(self):
        self._st_login_action = QAction(
            QIcon(":/Asistente-LADM_COL/resources/images/login.svg"),
            QCoreApplication.translate("AsistenteLADMCOLPlugin", "Login..."),
            self.main_window)
        self._st_logout_action = QAction(
            QIcon(":/Asistente-LADM_COL/resources/images/logout.svg"),
            QCoreApplication.translate("AsistenteLADMCOLPlugin", "Logout"),
            self.main_window)

        self._st_login_action.triggered.connect(self.show_st_login_dialog)
        self._st_logout_action.triggered.connect(self.session_logout_from_action)
        self._st_logout_action.setVisible(False)

        self.gui_builder.register_actions({
            ACTION_ST_LOGIN: self._st_login_action,
            ACTION_ST_LOGOUT: self._st_logout_action})

    def create_supplies_actions(self):
        self._etl_cobol_supplies_action = QAction(
            QIcon(":/Asistente-LADM_COL/resources/images/etl_cobol.png"),
            QCoreApplication.translate("AsistenteLADMCOLPlugin", "Load Cobol data"),
            self.main_window)

        self._missing_cobol_supplies_action = QAction(
            QIcon(":/Asistente-LADM_COL/resources/images/missing_supplies.svg"),
            QCoreApplication.translate("AsistenteLADMCOLPlugin", "Find missing Cobol supplies"),
            self.main_window)

        # Connections
        self._etl_cobol_supplies_action.triggered.connect(self.show_etl_cobol_dialog)
        self._missing_cobol_supplies_action.triggered.connect(self.show_missing_cobol_supplies_dialog)

        self.gui_builder.register_actions({ACTION_RUN_ETL_COBOL: self._etl_cobol_supplies_action,
                                           ACTION_FIND_MISSING_COBOL_SUPPLIES: self._missing_cobol_supplies_action})

    def create_operation_actions(self):
        self._point_surveying_and_representation_operation_action = QAction(
                QIcon(":/Asistente-LADM_COL/resources/images/points.png"),
                QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Point"),
                self.main_window)
        self._boundary_surveying_and_representation_operation_action = QAction(
                QIcon(":/Asistente-LADM_COL/resources/images/lines.png"),
                QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Boundary"),
                self.main_window)
        self._plot_spatial_unit_operation_action = QAction(
                QIcon(":/Asistente-LADM_COL/resources/images/polygons.png"),
                QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Plot"),
                self.main_window)
        self._building_spatial_unit_operation_action = QAction(
                QIcon(":/Asistente-LADM_COL/resources/images/polygons.png"),
                QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Building"),
                self.main_window)
        self._building_unit_spatial_unit_operation_action = QAction(
                QIcon(":/Asistente-LADM_COL/resources/images/polygons.png"),
                QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Building Unit"),
                self.main_window)
        self._right_of_way_operation_action = QAction(
                QIcon(":/Asistente-LADM_COL/resources/images/polygons.png"),
                QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Right of Way"),
                self.main_window)
        self._extaddress_operation_action = QAction(
                QIcon(":/Asistente-LADM_COL/resources/images/points.png"),
                QCoreApplication.translate("AsistenteLADMCOLPlugin", "Associate Address")
                )

        self._parcel_baunit_operation_action = QAction(
                QIcon(":/Asistente-LADM_COL/resources/images/tables.png"),
                QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Parcel"),
                self.main_window)

        self._col_party_operation_action = QAction(
                QIcon(":/Asistente-LADM_COL/resources/images/tables.png"),
                QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Party"),
                self.main_window)
        self._group_party_operation_action = QAction(
                QIcon(":/Asistente-LADM_COL/resources/images/tables.png"),
                QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Group Party"),
                self.main_window)

        self._administrative_source_operation_action = QAction(
                QIcon(":/Asistente-LADM_COL/resources/images/tables.png"),
                QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Administrative Source"),
                self.main_window)
        self._spatial_source_operation_action = QAction(
                QIcon(":/Asistente-LADM_COL/resources/images/tables.png"),
                QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Spatial Source"),
                self.main_window)
        self._upload_source_files_operation_action = QAction(QIcon(":/Asistente-LADM_COL/resources/images/upload.svg"),
                                                             QCoreApplication.translate("AsistenteLADMCOLPlugin",
                                                                                        "Upload Pending Source Files"),
                                                             self.main_window)

        self._right_rrr_operation_action = QAction(
                QIcon(":/Asistente-LADM_COL/resources/images/tables.png"),
                QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Right"),
                self.main_window)
        self._restriction_rrr_operation_action = QAction(
                QIcon(":/Asistente-LADM_COL/resources/images/tables.png"),
                QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Restriction"),
                self.main_window)

        self._quality_operation_action = QAction(
                QIcon(":/Asistente-LADM_COL/resources/images/validation.svg"),
                QCoreApplication.translate("AsistenteLADMCOLPlugin", "Quality"), self.main_window)

        # Set connections
        self._point_surveying_and_representation_operation_action.triggered.connect(self.show_wiz_point_cad)
        self._boundary_surveying_and_representation_operation_action.triggered.connect(self.show_wiz_boundaries_cad)
        self._plot_spatial_unit_operation_action.triggered.connect(self.show_wiz_plot_cad)
        self._parcel_baunit_operation_action.triggered.connect(self.show_wiz_parcel_cad)
        self._building_spatial_unit_operation_action.triggered.connect(self.show_wiz_building_cad)
        self._building_unit_spatial_unit_operation_action.triggered.connect(self.show_wiz_building_unit_cad)
        self._right_of_way_operation_action.triggered.connect(self.show_wiz_right_of_way_cad)
        self._extaddress_operation_action.triggered.connect(self.show_wiz_extaddress_cad)
        self._col_party_operation_action.triggered.connect(self.show_wiz_col_party_cad)
        self._group_party_operation_action.triggered.connect(self.show_dlg_group_party)
        self._right_rrr_operation_action.triggered.connect(self.show_wiz_right_rrr_cad)
        self._restriction_rrr_operation_action.triggered.connect(self.show_wiz_restriction_rrr_cad)
        self._administrative_source_operation_action.triggered.connect(self.show_wiz_administrative_source_cad)
        self._spatial_source_operation_action.triggered.connect(self.show_wiz_spatial_source_cad)
        self._upload_source_files_operation_action.triggered.connect(self.upload_source_files)
        self._quality_operation_action.triggered.connect(self.show_dlg_quality)

        self.gui_builder.register_actions({
            ACTION_CREATE_POINT: self._point_surveying_and_representation_operation_action,
            ACTION_CREATE_BOUNDARY: self._boundary_surveying_and_representation_operation_action,
            ACTION_CREATE_PLOT: self._plot_spatial_unit_operation_action,
            ACTION_CREATE_BUILDING: self._building_spatial_unit_operation_action,
            ACTION_CREATE_BUILDING_UNIT: self._building_unit_spatial_unit_operation_action,
            ACTION_CREATE_RIGHT_OF_WAY: self._right_of_way_operation_action,
            ACTION_CREATE_EXT_ADDRESS: self._extaddress_operation_action,
            ACTION_CREATE_PARCEL: self._parcel_baunit_operation_action,
            ACTION_CREATE_PARTY: self._col_party_operation_action,
            ACTION_CREATE_GROUP_PARTY: self._group_party_operation_action,
            ACTION_CREATE_ADMINISTRATIVE_SOURCE: self._administrative_source_operation_action,
            ACTION_CREATE_SPATIAL_SOURCE: self._spatial_source_operation_action,
            ACTION_UPLOAD_PENDING_SOURCE: self._upload_source_files_operation_action,
            ACTION_CREATE_RIGHT: self._right_rrr_operation_action,
            ACTION_CREATE_RESTRICTION: self._restriction_rrr_operation_action,
            ACTION_CHECK_QUALITY_RULES: self._quality_operation_action})

    def create_cadastre_form_actions(self):
        self._property_record_card_action = QAction(
            QIcon(":/Asistente-LADM_COL/resources/images/tables.png"),
            QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Property Record Card"),
            self.main_window)

        # Connections
        self._property_record_card_action.triggered.connect(self.show_wiz_property_record_card)

    def create_valuation_actions(self):
        self._parcel_valuation_action = QAction(
            QIcon(":/Asistente-LADM_COL/resources/images/tables.png"),
            QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Parcel"),
            self.main_window)
        self._building_unit_valuation_action = QAction(
            QIcon(":/Asistente-LADM_COL/resources/images/tables.png"),
            QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Building Unit"),
            self.main_window)
        self._building_unit_qualification_valuation_action = QAction(
            QIcon(":/Asistente-LADM_COL/resources/images/tables.png"),
            QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Building Unit Qualification"),
            self.main_window)
        self._geoeconomic_zone_valuation_action = QAction(
            QIcon(":/Asistente-LADM_COL/resources/images/polygons.png"),
            QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Geoeconomic Zone"),
            self.main_window)
        self._physical_zone_valuation_action = QAction(
            QIcon(":/Asistente-LADM_COL/resources/images/polygons.png"),
            QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Physical Zone"),
            self.main_window)

        # Connections
        self._parcel_valuation_action.triggered.connect(self.show_wiz_parcel_valuation)
        self._building_unit_valuation_action.triggered.connect(self.show_wiz_building_unit_valuation)
        self._building_unit_qualification_valuation_action.triggered.connect(
            self.show_wiz_building_unit_qualification_valuation)
        self._geoeconomic_zone_valuation_action.triggered.connect(self.show_wiz_geoeconomic_zone_valuation)
        self._physical_zone_valuation_action.triggered.connect(self.show_wiz_physical_zone_valuation_action)

    def create_change_detection_actions(self):
        self._query_changes_per_parcel_action = QAction(
            QCoreApplication.translate("AsistenteLADMCOLPlugin", "Query per parcel"), self.main_window)
        self._query_changes_all_parcels_action = QAction(
            QCoreApplication.translate("AsistenteLADMCOLPlugin", "Query all parcels"), self.main_window)
        self._settings_changes_action = QAction(
            QCoreApplication.translate("AsistenteLADMCOLPlugin", "Supplies data settings"), self.main_window)

        # Set connections
        self._query_changes_per_parcel_action.triggered.connect(self.query_changes_per_parcel)
        self._query_changes_all_parcels_action.triggered.connect(self.query_changes_all_parcels)
        self._settings_changes_action.triggered.connect(self.show_supplies_data_settings)

        self.gui_builder.register_actions({
            ACTION_CHANGE_DETECTION_PER_PARCEL: self._query_changes_per_parcel_action,
            ACTION_CHANGE_DETECTION_ALL_PARCELS: self._query_changes_all_parcels_action,
            ACTION_SUPPLIES_SETTINGS: self._settings_changes_action
        })

    def create_generic_actions(self):
        self._load_layers_action = QAction(QIcon(":/Asistente-LADM_COL/resources/images/load_layers.png"), QCoreApplication.translate("AsistenteLADMCOLPlugin", "Load layers"),
                                           self.main_window)
        self._queries_action = QAction(QIcon(":/Asistente-LADM_COL/resources/images/search.png"), QCoreApplication.translate("AsistenteLADMCOLPlugin", "Queries"),
                                       self.main_window)
        self._annex_17_action = QAction(QIcon(":/Asistente-LADM_COL/resources/images/report_annex_17.svg"),
                                        QCoreApplication.translate("AsistenteLADMCOLPlugin", "Annex 17"),
                                        self.main_window)
        self._annex_17_action.triggered.connect(self.call_annex_17_report_generation)
        self._ant_map_action = QAction(QIcon(":/Asistente-LADM_COL/resources/images/report_ant.svg"),
                                       QCoreApplication.translate("AsistenteLADMCOLPlugin", "ANT Map"),
                                       self.main_window)
        self._ant_map_action.triggered.connect(self.call_ant_map_report_generation)
        self._import_schema_action = QAction(QIcon(":/Asistente-LADM_COL/resources/images/schema_import.svg"),
            QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create LADM-COL structure"), self.main_window)

        # Created to be called by the task manager, not necessarily to show it in a menu/toolbar.
        self._import_schema_supplies_action = QAction(QIcon(":/Asistente-LADM_COL/resources/images/schema_import.svg"),
                                                      QCoreApplication.translate("AsistenteLADMCOLPlugin",
                                                                                 "Create LADM-COL structure (Supplies)"),
                                                      self.main_window)

        self._import_data_action = QAction(QIcon(":/Asistente-LADM_COL/resources/images/import_xtf.svg"),
                                           QCoreApplication.translate("AsistenteLADMCOLPlugin", "Import data"),
                                           self.main_window)
        self._import_data_action_supplies = QAction(QIcon(":/Asistente-LADM_COL/resources/images/import_xtf.svg"),
                                           QCoreApplication.translate("AsistenteLADMCOLPlugin", "Import data (Supplies)"),
                                           self.main_window)
        self._export_data_action = QAction(QIcon(":/Asistente-LADM_COL/resources/images/export_to_xtf.svg"),
                                           QCoreApplication.translate("AsistenteLADMCOLPlugin", "Export data"),
                                           self.main_window)
        self._export_data_action_supplies = QAction(QIcon(":/Asistente-LADM_COL/resources/images/export_to_xtf.svg"),
                                           QCoreApplication.translate("AsistenteLADMCOLPlugin", "Export data (Supplies)"),
                                           self.main_window)
        self._settings_action = QAction(QIcon(":/Asistente-LADM_COL/resources/images/settings.svg"),
                                        QCoreApplication.translate("AsistenteLADMCOLPlugin", "Settings"),
                                        self.main_window)
        self._supplies_settings_action = QAction(QIcon(":/Asistente-LADM_COL/resources/images/settings.svg"),
                                                 QCoreApplication.translate("AsistenteLADMColPlugin", "Supplies Settings"),
                                                 self.main_window)
        self._help_action = QAction(QIcon(":/Asistente-LADM_COL/resources/images/help.png"),
                                    QCoreApplication.translate("AsistenteLADMCOLPlugin", "Help"),
                                    self.main_window)
        self._about_action = QAction(QIcon(":/Asistente-LADM_COL/resources/images/info.svg"), QCoreApplication.translate("AsistenteLADMCOLPlugin", "About"),
                                     self.main_window)

        self._import_schema_action.triggered.connect(partial(self.show_dlg_import_schema, **{'selected_models':list()}))
        self._import_schema_supplies_action.triggered.connect(partial(self.show_dlg_import_schema, **{'selected_models':list(), 'db_source': SUPPLIES_DB_SOURCE}))
        self._import_data_action.triggered.connect(self.show_dlg_import_data)
        self._import_data_action_supplies.triggered.connect(partial(self.show_dlg_import_data, {'db_source': SUPPLIES_DB_SOURCE}))
        self._export_data_action.triggered.connect(self.show_dlg_export_data)
        self._export_data_action_supplies.triggered.connect(partial(self.show_dlg_export_data, {'db_source': SUPPLIES_DB_SOURCE}))
        self._queries_action.triggered.connect(self.show_queries)
        self._load_layers_action.triggered.connect(self.load_layers_from_qgis_model_baker)
        self._settings_action.triggered.connect(self.show_settings)
        self._supplies_settings_action.triggered.connect(self.show_supplies_data_settings_clear_message_bar)
        self._help_action.triggered.connect(self.show_help)
        self._about_action.triggered.connect(self.show_about_dialog)

        self.gui_builder.register_actions({
            ACTION_REPORT_ANNEX_17: self._annex_17_action,
            ACTION_REPORT_ANT: self._ant_map_action,
            ACTION_LOAD_LAYERS: self._load_layers_action,
            ACTION_PARCEL_QUERY: self._queries_action,
            ACTION_CHECK_QUALITY_RULES: self._quality_operation_action,
            ACTION_SCHEMA_IMPORT: self._import_schema_action,
            ACTION_SCHEMA_IMPORT_SUPPLIES: self._import_schema_supplies_action,
            ACTION_IMPORT_DATA: self._import_data_action,
            ACTION_IMPORT_DATA_SUPPLIES: self._import_data_action_supplies,
            ACTION_EXPORT_DATA: self._export_data_action,
            ACTION_EXPORT_DATA_SUPPLIES: self._export_data_action_supplies,
            ACTION_SETTINGS: self._settings_action,
            ACTION_SUPPLIES_SETTINGS: self._supplies_settings_action,
            ACTION_HELP: self._help_action,
            ACTION_ABOUT: self._about_action
        })

    def add_processing_models(self, provider_id):
        if not (provider_id == 'model' or provider_id is None):
            return

        if provider_id is not None: # If method acted as slot
            QgsApplication.processingRegistry().providerAdded.disconnect(self.add_processing_models)

        # Add ladm_col models
        basepath = os.path.dirname(os.path.abspath(__file__))
        plugin_models_dir = os.path.join(basepath, "lib", "processing", "models")

        for filename in glob.glob(os.path.join(plugin_models_dir, '*.model3')):
            alg = QgsProcessingModelAlgorithm()
            if not alg.fromFile(filename):
                self.logger.critical(__name__, "Couldn't load model from {}".format(filename))
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
        button.setText(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Remove dependency"))
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
        self.clear_message_bar()
        self.qgis_utils.get_layer(self.get_db_connection(), layer, load=True)

    def load_layers(self, layers):
        self.qgis_utils.get_layers(self.get_db_connection(), layers, True)

    def zoom_to_features(self, layer, ids=list(), t_ids=dict(), duration=500):
        if t_ids:
            t_id_name = list(t_ids.keys())[0]
            t_ids_list = t_ids[t_id_name]

            features = self.ladm_data.get_features_from_t_ids(layer, t_id_name, t_ids_list, True, True)
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
        dlg = LogQualityDialog(self.quality, self.conn_manager.get_db_connector_from_source())
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

    @_db_connection_required
    @_supplies_model_required
    def show_etl_cobol_dialog(self, *args):
        # TODO: Should use @_activate_processing_plugin
        dlg = ETLCobolDialog(self.qgis_utils, self.get_supplies_db_connection(), self.conn_manager, self.iface.mainWindow())
        dlg.exec_()

    def show_missing_cobol_supplies_dialog(self):
        dlg = MissingCobolSupplies(self.qgis_utils, self.get_supplies_db_connection(), self.conn_manager, self.iface.mainWindow())
        dlg.exec_()

    @_validate_if_wizard_is_open
    @_qgis_model_baker_required
    @_db_connection_required
    @_operation_model_required
    def call_explode_boundaries(self, *args):
        self.toolbar.build_boundary(self.get_db_connection())

    @_validate_if_wizard_is_open
    @_qgis_model_baker_required
    @_db_connection_required
    @_operation_model_required
    def call_topological_editing(self, *args):
        self.qgis_utils.enable_topological_editing(self.get_db_connection())

    @_validate_if_wizard_is_open
    @_qgis_model_baker_required
    @_db_connection_required
    @_operation_model_required
    def call_fill_topology_table_pointbfs(self, *args):
        self.toolbar.fill_topology_table_pointbfs(self.get_db_connection())

    @_validate_if_wizard_is_open
    @_qgis_model_baker_required
    @_db_connection_required
    @_operation_model_required
    def call_fill_topology_tables_morebfs_less(self, *args):
        self.toolbar.fill_topology_tables_morebfs_less(self.get_db_connection())

    @_validate_if_wizard_is_open
    @_qgis_model_baker_required
    @_db_connection_required
    @_operation_model_required
    @_activate_processing_plugin
    def call_fill_right_of_way_relations(self, *args):
        self.right_of_way.fill_right_of_way_relations(self.get_db_connection())

    @_validate_if_wizard_is_open
    @_qgis_model_baker_required
    @_db_connection_required
    @_operation_model_required
    def call_ant_map_report_generation(self, *args):
        self.report_generator.generate_report(self.get_db_connection(), ANT_MAP_REPORT)

    @_validate_if_wizard_is_open
    @_qgis_model_baker_required
    @_db_connection_required
    @_operation_model_required
    def call_annex_17_report_generation(self, *args):
        self.report_generator.generate_report(self.get_db_connection(), ANNEX_17_REPORT)

    @_validate_if_wizard_is_open
    @_qgis_model_baker_required
    @_db_connection_required
    @_operation_model_required
    @_activate_processing_plugin
    def call_import_from_intermediate_structure(self, *args):
        self._dlg = ImportFromExcelDialog(self.iface, self.get_db_connection(), self.qgis_utils)
        self._dlg.log_excel_show_message_emitted.connect(self.show_log_excel_button)
        self._dlg.exec_()

    def unload(self):
        self.session_logout(False, False)  # Do not show message when deactivating plugin, closing QGIS, etc.)
        self.uninstall_custom_expression_functions()

        self.close_dock_widgets([self._dock_widget_transitional_system,
                                 self._dock_widget_change_detection,
                                 self._dock_widget_queries])
        self.gui_builder.unload_gui()

        # Close all connections
        self.conn_manager.close_db_connections()
        QgsApplication.processingRegistry().removeProvider(self.ladm_col_provider)

    def close_dock_widgets(self, dock_widgets):
        for dock_widget in dock_widgets:
            if dock_widget is not None:
                dock_widget.close()
                dock_widget = None

    @_validate_if_wizard_is_open
    def show_settings(self, *args):
        dlg = SettingsDialog(qgis_utils=self.qgis_utils, conn_manager=self.conn_manager)

        # Connect signals (DBUtils, QgisUtils)
        dlg.db_connection_changed.connect(self.conn_manager.db_connection_changed)
        dlg.db_connection_changed.connect(self.qgis_utils.cache_layers_and_relations)
        dlg.active_role_changed.connect(self.call_refresh_gui)

        dlg.set_action_type(EnumDbActionType.CONFIG)
        dlg.exec_()

    def show_settings_clear_message_bar(self):
        self.clear_message_bar()
        self.show_settings()

    def show_plugin_manager(self):
        self.iface.actionManagePlugins().trigger()

    @_db_connection_required
    @_qgis_model_baker_required
    def load_layers_from_qgis_model_baker(self, *args):
        dlg = LoadLayersDialog(self.iface, self.get_db_connection(), self.qgis_utils)
        dlg.exec_()

    @_validate_if_wizard_is_open
    @_qgis_model_baker_required
    @_db_connection_required
    @_operation_model_required
    def show_queries(self, *args):
        self.close_dock_widgets([self._dock_widget_queries])

        self._dock_widget_queries = DockWidgetQueries(self.iface,
                                                      self.get_db_connection(),
                                                      self.get_query_manager(),
                                                      self.qgis_utils,
                                                      self.ladm_data)
        self.conn_manager.db_connection_changed.connect(self._dock_widget_queries.update_db_connection)
        self._dock_widget_queries.zoom_to_features_requested.connect(self.zoom_to_features)
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self._dock_widget_queries)

    def get_db_connection(self):
        return self.conn_manager.get_db_connector_from_source()

    def get_query_manager(self):
        return self.conn_manager.get_query_manager()

    def get_supplies_db_connection(self):
        return self.conn_manager.get_db_connector_from_source(db_source=SUPPLIES_DB_SOURCE)

    @_validate_if_wizard_is_open
    @_qgis_model_baker_required
    def show_dlg_import_schema(self, *args, **kwargs):
        """
        Can be called from 1) an action, 2) from a signal or 3) directly.

        In 1) args has a False argument from QAction.triggered.
        In 2) either args comes with a dict inside (hence the "if args" below), or **{} is send (hence the "if kwargs" below).
        In 3) **{} is passed, hence the "if kwargs" below.
        """
        from .gui.qgis_model_baker.dlg_import_schema import DialogImportSchema

        selected_models_import_schema = list()
        db_source = COLLECTED_DB_SOURCE
        if args:
            param = args[0]
            if type(param) is dict:
                if 'db_source' in param:
                    db_source = param['db_source']
                if 'selected_models' in param:
                    selected_models_import_schema = param['selected_models']

        if kwargs:
            if 'db_source' in kwargs:
                db_source = kwargs['db_source']
            if 'selected_models' in kwargs:
                selected_models_import_schema = kwargs['selected_models']

        dlg = DialogImportSchema(self.iface, self.qgis_utils, self.conn_manager, selected_models_import_schema, db_source)
        dlg.open_dlg_import_data.connect(self.show_dlg_import_data)
        self.logger.info(__name__, "Import Schema dialog ({}) opened.".format(db_source))
        dlg.exec_()

    @_validate_if_wizard_is_open
    @_qgis_model_baker_required
    def show_dlg_import_data(self, *args):
        from .gui.qgis_model_baker.dlg_import_data import DialogImportData

        db_source = COLLECTED_DB_SOURCE
        if args:
            param = args[0]
            if type(param) is dict:
                if 'db_source' in param:
                    db_source = param['db_source']

        dlg = DialogImportData(self.iface, self.qgis_utils, self.conn_manager, db_source)
        dlg.open_dlg_import_schema.connect(self.show_dlg_import_schema)
        self.logger.info(__name__, "Import data dialog ({}) opened.".format(db_source))
        dlg.exec_()

    @_validate_if_wizard_is_open
    @_qgis_model_baker_required
    def show_dlg_export_data(self, *args):
        from .gui.qgis_model_baker.dlg_export_data import DialogExportData

        db_source = COLLECTED_DB_SOURCE
        if args:
            param = args[0]
            if type(param) is dict:
                if 'db_source' in param:
                    db_source = param['db_source']

        dlg = DialogExportData(self.iface, self.qgis_utils, self.conn_manager, db_source)
        self.logger.info(__name__, "Export data dialog ({}) opened.".format(db_source))
        dlg.exec_()

    @_validate_if_wizard_is_open
    @_qgis_model_baker_required
    @_db_connection_required
    @_operation_model_required
    def show_wiz_point_cad(self, *args):
        self.wiz = CreatePointsOperationWizard(self.iface, self.get_db_connection(), self.qgis_utils)
        self.exec_wizard(self.wiz)

    @_db_connection_required
    @_operation_model_required
    def show_wiz_boundaries_cad(self, *args):
        self.show_wizard(WIZARD_CREATE_BOUNDARY_OPERATION)

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

    @_db_connection_required
    @_operation_model_required
    def show_wiz_plot_cad(self, *args):
        self.show_wizard(WIZARD_CREATE_PLOT_OPERATION)

    @_db_connection_required
    @_operation_model_required
    def show_wiz_building_cad(self, *args):
        self.show_wizard(WIZARD_CREATE_BUILDING_OPERATION)

    @_db_connection_required
    @_operation_model_required
    def show_wiz_building_unit_cad(self, *args):
        self.show_wizard(WIZARD_CREATE_BUILDING_UNIT_OPERATION)

    @_db_connection_required
    @_operation_model_required
    def show_wiz_right_of_way_cad(self, *args):
        self.show_wizard(WIZARD_CREATE_RIGHT_OF_WAY_OPERATION)

    @_db_connection_required
    @_operation_model_required
    def show_wiz_extaddress_cad(self, *args):
        self.show_wizard(WIZARD_CREATE_EXT_ADDRESS_OPERATION)

    @_db_connection_required
    @_operation_model_required
    def show_wiz_parcel_cad(self, *args):
        self.show_wizard(WIZARD_CREATE_PARCEL_OPERATION)

    @_db_connection_required
    @_operation_model_required
    def show_wiz_col_party_cad(self, *args):
        self.show_wizard(WIZARD_CREATE_COL_PARTY_CADASTRAL)

    @_validate_if_wizard_is_open
    @_qgis_model_baker_required
    @_db_connection_required
    @_operation_model_required
    def show_dlg_group_party(self, *args):
        namespace_enabled = QSettings().value('Asistente-LADM_COL/automatic_values/namespace_enabled', True, bool)
        local_id_enabled = QSettings().value('Asistente-LADM_COL/automatic_values/local_id_enabled', True, bool)

        if not namespace_enabled or not local_id_enabled:
            self.show_message_with_settings_button(QCoreApplication.translate("CreateGroupPartyOperation",
                                                       "First enable automatic values for both namespace and local_id fields before creating group parties. Click the button to open the settings dialog."),
                                                   QCoreApplication.translate("CreateGroupPartyOperation", "Open Settings"),
                                                   Qgis.Info)
            return

        dlg = CreateGroupPartyOperation(self.iface, self.get_db_connection(), self.qgis_utils)

        # Check if required layers are available
        if dlg.required_layers_are_available():
            # Load required data, it is necessary in the dlg
            dlg.load_parties_data()
            dlg.exec_()
        else:
            del dlg

    @_db_connection_required
    @_operation_model_required
    def show_wiz_right_rrr_cad(self, *args):
        self.show_wizard(WIZARD_CREATE_RIGHT_OPERATION)

    @_db_connection_required
    @_operation_model_required
    def show_wiz_restriction_rrr_cad(self, *args):
        self.show_wizard(WIZARD_CREATE_RESTRICTION_OPERATION)

    @_db_connection_required
    @_operation_model_required
    def show_wiz_administrative_source_cad(self, *args):
        self.show_wizard(WIZARD_CREATE_ADMINISTRATIVE_SOURCE_OPERATION)

    @_db_connection_required
    @_operation_model_required
    def show_wiz_spatial_source_cad(self, *args):
        self.show_wizard(WIZARD_CREATE_SPATIAL_SOURCE_OPERATION)

    @_validate_if_wizard_is_open
    @_qgis_model_baker_required
    @_db_connection_required
    @_operation_model_required
    def upload_source_files(self, *args):
        self.qgis_utils.upload_source_files(self.get_db_connection())

    @_validate_if_wizard_is_open
    @_qgis_model_baker_required
    @_db_connection_required
    @_operation_model_required
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

    @_db_connection_required
    @_valuation_model_required
    def show_wiz_building_unit_valuation(self, *args):
        self.show_wizard(WIZARD_CREATE_BUILDING_UNIT_VALUATION)

    @_db_connection_required
    @_valuation_model_required
    def show_wiz_building_unit_qualification_valuation(self, *args):
        self.show_wizard(WIZARD_CREATE_BUILDING_UNIT_QUALIFICATION_VALUATION)

    @_db_connection_required
    @_valuation_model_required
    def show_wiz_geoeconomic_zone_valuation(self, *args):
        self.show_wizard(WIZARD_CREATE_GEOECONOMIC_ZONE_VALUATION)

    @_db_connection_required
    @_valuation_model_required
    def show_wiz_physical_zone_valuation_action(self, *args):
        self.show_wizard(WIZARD_CREATE_PHYSICAL_ZONE_VALUATION)

    @_validate_if_wizard_is_open
    @_qgis_model_baker_required
    @_map_swipe_tool_required
    @_db_connection_required
    @_operation_model_required
    @_supplies_db_connection_required
    @_different_db_connections_required
    def query_changes_per_parcel(self, *args):
        msg = QCoreApplication.translate("AsistenteLADMCOLPlugin", "Opening Query Changes per Parcel panel...")
        with ProcessWithStatus(msg):
            self.show_change_detection_dockwidget(False)  # all_parcels_mode is False, we want the per_parcel_mode instead

    @_validate_if_wizard_is_open
    @_qgis_model_baker_required
    @_map_swipe_tool_required
    @_db_connection_required
    @_operation_model_required
    @_supplies_db_connection_required
    @_different_db_connections_required
    def query_changes_all_parcels(self, *args):
        msg = QCoreApplication.translate("AsistenteLADMCOLPlugin", "Opening Query Changes for All Parcels panel...")
        with ProcessWithStatus(msg):
            self.show_change_detection_dockwidget()

    def show_change_detection_dockwidget(self, all_parcels_mode=True):
        self.close_dock_widgets([self._dock_widget_change_detection])

        self._dock_widget_change_detection = DockWidgetChangeDetection(self.iface,
                                                                       self.get_db_connection(),
                                                                       self.get_supplies_db_connection(),
                                                                       self.qgis_utils,
                                                                       self.ladm_data,
                                                                       all_parcels_mode)
        self.conn_manager.db_connection_changed.connect(self._dock_widget_change_detection.update_db_connection)
        self._dock_widget_change_detection.zoom_to_features_requested.connect(self.zoom_to_features)
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self._dock_widget_change_detection)

    def show_supplies_data_settings(self):
        dlg = SettingsDialog(qgis_utils=self.qgis_utils, conn_manager=self.conn_manager, db_source=SUPPLIES_DB_SOURCE)
        dlg.db_connection_changed.connect(self.conn_manager.db_connection_changed)
        dlg.exec_()

    def show_supplies_data_settings_clear_message_bar(self):
        self.clear_message_bar()
        self.show_supplies_data_settings()

    def open_table(self, layer, filter=None):
        self.iface.showAttributeTable(layer, filter)

    def download_report_dependency(self):
        self.clear_message_bar()  # Remove messages
        self.report_generator.download_report_dependency()

    def remove_report_dependency(self):
        self.clear_message_bar()  # Remove messages
        Utils.remove_dependency_directory(DEPENDENCY_REPORTS_DIR_NAME)

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
        wiz_settings = self.wizard_config.get_wizard_config(self.get_db_connection().names, wizard_name)
        if self.qgis_utils.required_layers_are_available(self.get_db_connection(),
                                                         wiz_settings[WIZARD_LAYERS],
                                                         wiz_settings[WIZARD_TOOL_NAME]):
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

    def show_st_login_dialog(self):
        dlg = LoginSTDialog(self.main_window)
        dlg.exec_()

        if self.session.is_user_logged():
            self.close_dock_widgets([self._dock_widget_transitional_system])

            # Show Transitional System dock widget
            user = self.session.get_logged_st_user()
            self._dock_widget_transitional_system = DockWidgetTransitionalSystem(user, self.main_window)
            self.conn_manager.db_connection_changed.connect(self._dock_widget_transitional_system.update_db_connection)
            self._dock_widget_transitional_system.logout_requested.connect(self.session_logout)
            self._dock_widget_transitional_system.trigger_action_emitted.connect(self.trigger_action_emitted)
            self.session.logout_finished.connect(self._dock_widget_transitional_system.after_logout)
            self.iface.addDockWidget(Qt.RightDockWidgetArea, self._dock_widget_transitional_system)

    def session_logout_from_action(self):
        """ Overwrite action.triggered SIGNAL parameters and call session_logout properly """
        self.session_logout(True, True)

    def session_logout(self, show_confirmation_dialog=True, show_message=True):
        """
        Handles logout from GUI. All logout calls should be redirected to this method.

        :param show_confirmation_dialog: Whether to show a question to the user to confirm logout or not.
        :param show_message: Whether a response msg should be shown or not (e.g., when leaving QGIS we don't need the msg)
        """
        logout = True
        if show_confirmation_dialog:
            reply = QMessageBox.question(None,
                                 QCoreApplication.translate("AsistenteLADMCOLPlugin", "Continue?"),
                                 QCoreApplication.translate("AsistenteLADMCOLPlugin",
                                                            "Are you sure you want to log out from the Transitional System?"),
                                 QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.No:
                logout = False

        if logout:
            logged_out, msg = self.session.logout()
            if show_message:
                self.logger.log_message(__name__, msg, Qgis.Info if logged_out else Qgis.Warning, LogHandlerEnum.MESSAGE_BAR)

    def set_login_controls_visibility(self, login_activated):
        """
        React upon changes in ST login. If a user is logged in or logged out, we want to show only certain controls.

        :param login_activated: Boolean, True if a user is logged in
        """
        self._st_login_action.setVisible(not login_activated)
        self._st_logout_action.setVisible(login_activated)

    def trigger_action_emitted(self, action_tag):
        action = self.gui_builder.get_action(action_tag)
        if action is not None:
            action.trigger()

    def show_dlg_st_upload_file(self, request_id, supply_type):
        dlg = STUploadFileDialog(request_id, supply_type, self.main_window)
        dlg.exec_()

    def open_encrypted_db_connection(self, db_engine, conn_dict, user_level=EnumUserLevel.CREATE):
        if conn_dict:
            with ProcessWithStatus(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Connecting to remote db...")):
                db = self.conn_manager.get_encrypted_db_connector(db_engine, conn_dict)

            res, code, msg = db.test_connection(user_level=user_level)
            if res:
                self.logger.success_msg(__name__, QCoreApplication.translate("AsistenteLADMCOLPlugin",
                                                                             "{} Models: {}".format(msg, db.get_models())))
            else:
                self.logger.warning_msg(__name__, QCoreApplication.translate("AsistenteLADMCOLPlugin",
                                                                             "The connection could not be established! Details: {}".format(msg)))

            return db if res else None

        return None

    def task_step_explore_data_cadastre_registry(self, db_engine, conn_dict, user_level):
        db = self.open_encrypted_db_connection(db_engine, conn_dict, user_level)
        if db:
            layers = {
                db.names.INI_PARCEL_SUPPLIES_T: {'name': db.names.INI_PARCEL_SUPPLIES_T, 'geometry': None, 'layer': None},
                db.names.GC_PARCEL_T: {'name': db.names.GC_PARCEL_T, 'geometry': None, 'layer': None},
                db.names.SNR_PARCEL_REGISTRY_T: {'name': db.names.SNR_PARCEL_REGISTRY_T, 'geometry': None, 'layer': None},
            }
            self.qgis_utils.get_layers(db, layers, load=True)
