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
from processing.modeler.ModelerUtils import ModelerUtils
from processing.script import ScriptUtils

from asistente_ladm_col.config.ladm_names import MODEL_CONFIG
from asistente_ladm_col.lib.ladm_col_models import (LADMColModelRegistry,
                                                    LADMColModel)
from asistente_ladm_col.lib.dependency.plugin_dependency import PluginDependency
from asistente_ladm_col.config.enums import (EnumDbActionType,
                                             EnumWizardType,
                                             EnumLogHandler,
                                             EnumUserLevel)
from asistente_ladm_col.config.general_config import (ANNEX_17_REPORT,
                                                      ANT_MAP_REPORT,
                                                      DEFAULT_LOG_MODE,
                                                      SUPPLIES_DB_SOURCE,
                                                      PLUGIN_VERSION,
                                                      RELEASE_URL,
                                                      COLLECTED_DB_SOURCE,
                                                      WIZARD_CLASS,
                                                      WIZARD_TOOL_NAME,
                                                      WIZARD_TYPE,
                                                      WIZARD_LAYERS,
                                                      WIZARD_CREATE_COL_PARTY_CADASTRAL,
                                                      WIZARD_CREATE_ADMINISTRATIVE_SOURCE_SURVEY,
                                                      WIZARD_CREATE_BOUNDARY_SURVEY,
                                                      WIZARD_CREATE_BUILDING_SURVEY,
                                                      WIZARD_CREATE_BUILDING_UNIT_SURVEY,
                                                      WIZARD_CREATE_RIGHT_SURVEY,
                                                      WIZARD_CREATE_RESTRICTION_SURVEY,
                                                      WIZARD_CREATE_SPATIAL_SOURCE_SURVEY,
                                                      WIZARD_CREATE_PARCEL_SURVEY, WIZARD_CREATE_PLOT_SURVEY,
                                                      WIZARD_CREATE_EXT_ADDRESS_SURVEY,
                                                      WIZARD_CREATE_RIGHT_OF_WAY_SURVEY,
                                                      WIZARD_CREATE_GEOECONOMIC_ZONE_VALUATION,
                                                      WIZARD_CREATE_PHYSICAL_ZONE_VALUATION,
                                                      WIZARD_CREATE_BUILDING_UNIT_VALUATION,
                                                      WIZARD_CREATE_BUILDING_UNIT_QUALIFICATION_VALUATION,
                                                      QGIS_MODEL_BAKER_PLUGIN_NAME,
                                                      QGIS_MODEL_BAKER_MIN_REQUIRED_VERSION,
                                                      QGIS_MODEL_BAKER_EXACT_REQUIRED_VERSION,
                                                      QGIS_MODEL_BAKER_REQUIRED_VERSION_URL,
                                                      MAP_SWIPE_TOOL_PLUGIN_NAME,
                                                      MAP_SWIPE_TOOL_MIN_REQUIRED_VERSION,
                                                      MAP_SWIPE_TOOL_EXACT_REQUIRED_VERSION,
                                                      MAP_SWIPE_TOOL_REQUIRED_VERSION_URL)
from asistente_ladm_col.config.layer_tree_indicator_config import LayerTreeIndicatorConfig
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
                                                            get_domain_value_from_code,
                                                            get_domain_description_from_code)  # >> DON'T REMOVE << Registers it in QgsExpression
from asistente_ladm_col.config.gui.common_keys import *
from asistente_ladm_col.core.app_core_interface import AppCoreInterface
from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.gui.app_gui_interface import AppGUIInterface
from asistente_ladm_col.gui.supplies.wiz_supplies_etl import SuppliesETLWizard
from asistente_ladm_col.gui.transitional_system.dlg_login_st import LoginSTDialog
from asistente_ladm_col.gui.gui_builder.gui_builder import GUI_Builder
from asistente_ladm_col.gui.transitional_system.dockwidget_transitional_system import DockWidgetTransitionalSystem
from asistente_ladm_col.lib.context import (Context,
                                            TaskContext,
                                            SettingsContext)
from asistente_ladm_col.lib.transitional_system.st_session.st_session import STSession
from asistente_ladm_col.logic.ladm_col.ladm_data import LADMDATA
from asistente_ladm_col.gui.change_detection.dockwidget_change_detection import DockWidgetChangeDetection
from asistente_ladm_col.gui.dialogs.dlg_about import AboutDialog
from asistente_ladm_col.gui.dialogs.dlg_import_from_excel import ImportFromExcelDialog
from asistente_ladm_col.gui.dialogs.dlg_load_layers import LoadLayersDialog
from asistente_ladm_col.gui.dialogs.dlg_log_excel import LogExcelDialog
from asistente_ladm_col.gui.supplies.dlg_missing_cobol_supplies import MissingCobolSupplies
from asistente_ladm_col.gui.dialogs.dlg_log_quality import LogQualityDialog
from asistente_ladm_col.gui.change_detection.dlg_change_detection_settings import ChangeDetectionSettingsDialog
from asistente_ladm_col.gui.dialogs.dlg_quality import QualityDialog
from asistente_ladm_col.gui.dialogs.dlg_settings import SettingsDialog
from asistente_ladm_col.gui.dialogs.dlg_welcome_screen import WelcomeScreenDialog
from asistente_ladm_col.gui.queries.dockwidget_queries import DockWidgetQueries
from asistente_ladm_col.gui.reports.reports import ReportGenerator
from asistente_ladm_col.gui.right_of_way import RightOfWay
from asistente_ladm_col.gui.toolbar import ToolBar
from asistente_ladm_col.gui.transitional_system.dlg_upload_file import STUploadFileDialog
from asistente_ladm_col.gui.wizards.survey.dlg_create_group_party_survey import CreateGroupPartySurvey
from asistente_ladm_col.gui.wizards.survey.wiz_create_points_survey import CreatePointsSurveyWizard
from asistente_ladm_col.lib.db.db_connection_manager import ConnectionManager
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.lib.processing.ladm_col_provider import LADMCOLAlgorithmProvider
from asistente_ladm_col.logic.quality.quality_rule_engine import QualityRuleEngine
from asistente_ladm_col.utils.decorators import (_db_connection_required,
                                                 _validate_if_wizard_is_open,
                                                 _qgis_model_baker_required,
                                                 _activate_processing_plugin,
                                                 _map_swipe_tool_required,
                                                 _validate_if_layers_in_editing_mode_with_changes,
                                                 _supplies_model_required,
                                                 _valuation_model_required,
                                                 _survey_model_required)
from asistente_ladm_col.utils.utils import show_plugin_help
from asistente_ladm_col.utils.qt_utils import (ProcessWithStatus, 
                                               normalize_local_url)
from asistente_ladm_col.resources_rc import *  # Necessary to show icons


class AsistenteLADMCOLPlugin(QObject):
    wiz_geometry_creation_finished = pyqtSignal()

    def __init__(self, iface, unit_tests=False):
        QObject.__init__(self)
        self.iface = iface
        self.unit_tests = unit_tests
        self.main_window = self.iface.mainWindow()
        self._about_dialog = None
        self.toolbar = None
        self.wiz_address = None
        self.conn_manager = ConnectionManager()
        self.wiz = None
        self.is_wizard_open = False  # Helps to make the plugin modules aware of open wizards
        self.wizard_config = WizardConfig()
        self.logger = Logger()
        self.logger.set_mode(DEFAULT_LOG_MODE)
        self.gui_builder = GUI_Builder(self.iface)
        self.session = STSession()
        task_steps_config = TaskStepsConfig()
        task_steps_config.set_slot_caller(self)
        layer_tree_indicator_config = LayerTreeIndicatorConfig()
        layer_tree_indicator_config.set_slot_caller(self)

        # Register LADM-COL models
        model_registry = LADMColModelRegistry()
        for model_key, model_config in MODEL_CONFIG.items():
            model_registry.register_model(LADMColModel(model_key, model_config))

        # Let's persist some dependency objects
        self.qmb_plugin = PluginDependency(QGIS_MODEL_BAKER_PLUGIN_NAME,
                                           QGIS_MODEL_BAKER_MIN_REQUIRED_VERSION,
                                           QGIS_MODEL_BAKER_EXACT_REQUIRED_VERSION,
                                           QGIS_MODEL_BAKER_REQUIRED_VERSION_URL)
        self.mst_plugin = PluginDependency(MAP_SWIPE_TOOL_PLUGIN_NAME,
                                           MAP_SWIPE_TOOL_MIN_REQUIRED_VERSION,
                                           MAP_SWIPE_TOOL_EXACT_REQUIRED_VERSION,
                                           MAP_SWIPE_TOOL_REQUIRED_VERSION_URL)

        # We need a couple of contexts when running tools, so, prepare them in advance
        self._context_collected = Context()  # By default, only collected source is set
        self._context_supplies = Context()
        self._context_supplies.set_db_sources([SUPPLIES_DB_SOURCE])
        self._context_collected_supplies = Context()
        self._context_collected_supplies.set_db_sources([COLLECTED_DB_SOURCE, SUPPLIES_DB_SOURCE])
        self._context_settings = SettingsContext()
        self._context_settings.blocking_mode = False  # Settings dialog should not block if called from the action

        self.ladm_col_provider = LADMCOLAlgorithmProvider()
        self.__processing_resources_installed = list()

    def initGui(self):
        self.app = AppInterface()
        self.app.set_core_interface(AppCoreInterface())
        self.app.set_gui_interface(AppGUIInterface(self.iface))

        self.right_of_way = RightOfWay(self.iface, self.get_db_connection().names)
        self.toolbar = ToolBar(self.iface)
        self.ladm_data = LADMDATA()
        self.report_generator = ReportGenerator(self.ladm_data)

        self.create_actions()
        self.register_dock_widgets()
        self.set_signal_slot_connections()

        if not self.unit_tests:
            # Ask for role name before building the GUI, only the first time the plugin is run
            if self.gui_builder.show_welcome_screen():
                dlg_welcome = WelcomeScreenDialog(self.main_window)
                dlg_welcome.exec_()

        if not qgis.utils.active_plugins:
            self.iface.initializationCompleted.connect(self.call_refresh_gui)
            self.iface.initializationCompleted.connect(self.initialize_requirements)
        else:
            self.call_refresh_gui()
            self.initialize_requirements()

        # Add LADM-COL provider, models and sripts to QGIS
        self.initialize_processing_resources()

    def create_actions(self):
        self.create_supplies_actions()
        self.create_survey_actions()
        self.create_cadastre_form_actions()
        self.create_valuation_actions()
        self.create_change_detection_actions()
        self.create_toolbar_actions()
        self.create_transitional_system_actions()
        self.create_generic_actions()

    def register_dock_widgets(self):
        """
        We register them so that GUI Builder can delete them properly when unloading the GUI
        """
        self.gui_builder.register_dock_widget(DOCK_WIDGET_TRANSITION_SYSTEM, None)
        self.gui_builder.register_dock_widget(DOCK_WIDGET_CHANGE_DETECTION, None)
        self.gui_builder.register_dock_widget(DOCK_WIDGET_QUERIES, None)

    def set_signal_slot_connections(self):
        self.conn_manager.db_connection_changed.connect(self.refresh_gui)

        self.logger.message_with_duration_emitted.connect(self.app.gui.show_message)
        self.logger.status_bar_message_emitted.connect(self.app.gui.show_status_bar_message)
        self.logger.clear_status_bar_emitted.connect(self.app.gui.clear_status_bar)
        self.logger.clear_message_bar_emitted.connect(self.app.gui.clear_message_bar)
        self.logger.message_with_button_load_layer_emitted.connect(self.show_message_to_load_layer)
        self.logger.message_with_button_open_table_attributes_emitted.connect(
            self.show_message_with_open_table_attributes_button)
        self.logger.message_with_buttons_change_detection_all_and_per_parcel_emitted.connect(
            self.show_message_with_buttons_change_detection_all_and_per_parcel)

        self.app.gui.add_indicators_requested.connect(self.add_indicators)
        self.report_generator.enable_action_requested.connect(self.enable_action)
        self.session.login_status_changed.connect(self.set_login_controls_visibility)

    @staticmethod
    def uninstall_custom_expression_functions():
        QgsExpression.unregisterFunction('get_domain_code_from_value')
        QgsExpression.unregisterFunction('get_domain_value_from_code')
        QgsExpression.unregisterFunction('get_domain_description_from_code')

    def initialize_requirements(self):
        """
        Make sure all we need from QGIS is set
        """
        # We need CTM12 projection in the QGIS SRS database
        res = self.app.core.initialize_ctm12()
        self.logger.info_warning(__name__, res, "CTM12 is in the QGIS SRS database? {}!!!".format(res))
        if not res and not self.unit_tests:
            folder, filename = os.path.split(QgsApplication.srsDatabaseFilePath())
            msg_box = QMessageBox(self.main_window)
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setTextFormat(Qt.RichText)
            msg_box.setWindowTitle(QCoreApplication.translate("AsistenteLADMCOLPlugin", "LADM-COL Assistant - Warning"))
            msg_box.setText(QCoreApplication.translate("AsistenteLADMCOLPlugin",
                                                       "The spatial reference database is not editable. Therefore, CTM12 cannot be configured.<br><br>" \
                                                       "Go to the folder <a href='file:///{normalized_folder}'>{folder}</a> and grant the current user permissions to write over that folder and over the '<b>{filename}</b>' file.<br><br>" \
                                                       "Once you're done, click <b>Ok</b> to continue loading <i>LADM-COL Assistant</i>. " \
                                                       "If you click <b>Cancel</b>, the <i>LADM-COL Assistant</i> won't be available, as the CTM12 projection is a prerequisite.".format(normalized_folder=normalize_local_url(folder), folder=folder, filename=filename)))
            msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg_box.setDefaultButton(QMessageBox.Ok)
            reply = msg_box.exec_()

            if reply == QMessageBox.Ok:
                self.initialize_requirements()
            else:
                self.unload()
                self.logger.critical_msg(__name__, QCoreApplication.translate("AsistenteLADMCOLPlugin",
                    "CTM12 could not be configured. Therefore you cannot use this version of the LADM-COL Assistant."))

    def call_refresh_gui(self):
        """
        SLOT. Intermediate step to call refresh gui adding proper parameters.
        """
        self.refresh_gui(self.get_db_connection(), None, COLLECTED_DB_SOURCE)  # 3rd value is required to refresh GUI

    def refresh_gui(self, db, res, db_source):
        if db_source == COLLECTED_DB_SOURCE:  # Only refresh GUI for changes in COLLECTED DB SOURCE
            msg = QCoreApplication.translate("AsistenteLADMCOLPlugin", "Refreshing GUI for the LADM-COL Assistant...")
            with ProcessWithStatus(msg):
                self.gui_builder.set_db_connection(db, res)
                self.gui_builder.build_gui()

    def create_toolbar_actions(self):
        self._finalize_geometry_creation_action = QAction(
            QIcon(":/Asistente-LADM-COL/resources/images/mActionFinalizeGeometryCreation.svg"),
            TOOLBAR_FINALIZE_GEOMETRY_CREATION,
            self.main_window)
        self._finalize_geometry_creation_action.triggered.connect(
            self.wiz_geometry_creation_finished)  # SIGNAL chaining
        self._finalize_geometry_creation_action.setEnabled(False)

        self._build_boundary_action = QAction(QIcon(":/Asistente-LADM-COL/resources/images/build_boundaries.svg"),
                                              TOOLBAR_BUILD_BOUNDARY, self.main_window)
        self._build_boundary_action.triggered.connect(partial(self.call_explode_boundaries, self._context_collected))

        self._topological_editing_action = QAction(QIcon(":/Asistente-LADM-COL/resources/images/move_nodes.svg"),
            TOOLBAR_MOVE_NODES, self.main_window)
        self._topological_editing_action.triggered.connect(partial(self.call_topological_editing, self._context_collected))

        self._fill_point_BFS_action = QAction(QIcon(":/Asistente-LADM-COL/resources/images/relationships.svg"),
                                              TOOLBAR_FILL_POINT_BFS,
                                              self.main_window)
        self._fill_point_BFS_action.triggered.connect(partial(self.call_fill_topology_table_pointbfs, self._context_collected))

        self._fill_more_BFS_less_action = QAction(QIcon(":/Asistente-LADM-COL/resources/images/relationships.svg"),
                                                  TOOLBAR_FILL_MORE_BFS_LESS,
                                                  self.main_window)
        self._fill_more_BFS_less_action.triggered.connect(partial(self.call_fill_topology_tables_morebfs_less, self._context_collected))

        self._fill_right_of_way_relations_action = QAction(QIcon(":/Asistente-LADM-COL/resources/images/relationships.svg"),
                                                           TOOLBAR_FILL_RIGHT_OF_WAY_RELATIONS, self.main_window)
        self._fill_right_of_way_relations_action.triggered.connect(partial(self.call_fill_right_of_way_relations, self._context_collected))

        self._import_from_intermediate_structure_action = QAction(QIcon(":/Asistente-LADM-COL/resources/images/excel.svg"),
                                                                  TOOLBAR_IMPORT_FROM_INTERMEDIATE_STRUCTURE,
                                                                  self.main_window)
        self._import_from_intermediate_structure_action.triggered.connect(partial(self.call_import_from_intermediate_structure, self._context_collected))

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
            QIcon(":/Asistente-LADM-COL/resources/images/login.svg"),
            QCoreApplication.translate("AsistenteLADMCOLPlugin", "Login..."),
            self.main_window)
        self._st_logout_action = QAction(
            QIcon(":/Asistente-LADM-COL/resources/images/logout.svg"),
            QCoreApplication.translate("AsistenteLADMCOLPlugin", "Logout"),
            self.main_window)

        self._st_login_action.triggered.connect(self.show_st_login_dialog)
        self._st_logout_action.triggered.connect(self.session_logout_from_action)
        self._st_logout_action.setVisible(False)

        self.gui_builder.register_actions({
            ACTION_ST_LOGIN: self._st_login_action,
            ACTION_ST_LOGOUT: self._st_logout_action})

    def create_supplies_actions(self):
        self._etl_supplies_action = QAction(
            QIcon(":/Asistente-LADM-COL/resources/images/etl.png"),
            QCoreApplication.translate("AsistenteLADMCOLPlugin", "Run supplies ETL"),
            self.main_window)

        self._missing_cobol_supplies_action = QAction(
            QIcon(":/Asistente-LADM-COL/resources/images/missing_supplies.svg"),
            QCoreApplication.translate("AsistenteLADMCOLPlugin", "Find missing Cobol supplies"),
            self.main_window)

        # Connections
        self._etl_supplies_action.triggered.connect(partial(self.show_wiz_supplies_etl, self._context_supplies))
        self._missing_cobol_supplies_action.triggered.connect(partial(self.show_missing_cobol_supplies_dialog, self._context_supplies))

        self.gui_builder.register_actions({ACTION_RUN_ETL_SUPPLIES: self._etl_supplies_action,
                                           ACTION_FIND_MISSING_COBOL_SUPPLIES: self._missing_cobol_supplies_action})

    def create_survey_actions(self):
        self._point_surveying_and_representation_survey_action = QAction(
                QIcon(":/Asistente-LADM-COL/resources/images/points.png"),
                QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Point"),
                self.main_window)
        self._boundary_surveying_and_representation_survey_action = QAction(
                QIcon(":/Asistente-LADM-COL/resources/images/lines.png"),
                QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Boundary"),
                self.main_window)
        self._plot_spatial_unit_survey_action = QAction(
                QIcon(":/Asistente-LADM-COL/resources/images/polygons.png"),
                QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Plot"),
                self.main_window)
        self._building_spatial_unit_survey_action = QAction(
                QIcon(":/Asistente-LADM-COL/resources/images/polygons.png"),
                QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Building"),
                self.main_window)
        self._building_unit_spatial_unit_survey_action = QAction(
                QIcon(":/Asistente-LADM-COL/resources/images/polygons.png"),
                QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Building Unit"),
                self.main_window)
        self._right_of_way_survey_action = QAction(
                QIcon(":/Asistente-LADM-COL/resources/images/polygons.png"),
                QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Right of Way"),
                self.main_window)
        self._extaddress_survey_action = QAction(
                QIcon(":/Asistente-LADM-COL/resources/images/points.png"),
                QCoreApplication.translate("AsistenteLADMCOLPlugin", "Associate Address")
                )

        self._parcel_baunit_survey_action = QAction(
                QIcon(":/Asistente-LADM-COL/resources/images/tables.png"),
                QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Parcel"),
                self.main_window)

        self._col_party_survey_action = QAction(
                QIcon(":/Asistente-LADM-COL/resources/images/tables.png"),
                QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Party"),
                self.main_window)
        self._group_party_survey_action = QAction(
                QIcon(":/Asistente-LADM-COL/resources/images/tables.png"),
                QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Group Party"),
                self.main_window)

        self._administrative_source_survey_action = QAction(
                QIcon(":/Asistente-LADM-COL/resources/images/tables.png"),
                QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Administrative Source"),
                self.main_window)
        self._spatial_source_survey_action = QAction(
                QIcon(":/Asistente-LADM-COL/resources/images/tables.png"),
                QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Spatial Source"),
                self.main_window)
        self._upload_source_files_survey_action = QAction(QIcon(":/Asistente-LADM-COL/resources/images/upload.svg"),
                                                          QCoreApplication.translate("AsistenteLADMCOLPlugin",
                                                                                        "Upload Pending Source Files"),
                                                          self.main_window)

        self._right_rrr_survey_action = QAction(
                QIcon(":/Asistente-LADM-COL/resources/images/tables.png"),
                QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Right"),
                self.main_window)
        self._restriction_rrr_survey_action = QAction(
                QIcon(":/Asistente-LADM-COL/resources/images/tables.png"),
                QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Restriction"),
                self.main_window)

        self._quality_survey_action = QAction(
                QIcon(":/Asistente-LADM-COL/resources/images/validation.svg"),
                QCoreApplication.translate("AsistenteLADMCOLPlugin", "Quality"),
                self.main_window)

        self._fix_ladm_col_relations_action = QAction(
                QIcon(":/Asistente-LADM-COL/resources/images/relationships.svg"),
                QCoreApplication.translate("AsistenteLADMCOLPlugin", "Fix LADM-COL relations"),
                self.main_window)

        # Set connections
        self._point_surveying_and_representation_survey_action.triggered.connect(partial(self.show_wiz_point_cad, self._context_collected))
        self._boundary_surveying_and_representation_survey_action.triggered.connect(partial(self.show_wiz_boundaries_cad, self._context_collected))
        self._plot_spatial_unit_survey_action.triggered.connect(partial(self.show_wiz_plot_cad, self._context_collected))
        self._parcel_baunit_survey_action.triggered.connect(partial(self.show_wiz_parcel_cad, self._context_collected))
        self._building_spatial_unit_survey_action.triggered.connect(partial(self.show_wiz_building_cad, self._context_collected))
        self._building_unit_spatial_unit_survey_action.triggered.connect(partial(self.show_wiz_building_unit_cad, self._context_collected))
        self._right_of_way_survey_action.triggered.connect(partial(self.show_wiz_right_of_way_cad, self._context_collected))
        self._extaddress_survey_action.triggered.connect(partial(self.show_wiz_extaddress_cad, self._context_collected))
        self._col_party_survey_action.triggered.connect(partial(self.show_wiz_col_party_cad, self._context_collected))
        self._group_party_survey_action.triggered.connect(partial(self.show_dlg_group_party, self._context_collected))
        self._right_rrr_survey_action.triggered.connect(partial(self.show_wiz_right_rrr_cad, self._context_collected))
        self._restriction_rrr_survey_action.triggered.connect(partial(self.show_wiz_restriction_rrr_cad, self._context_collected))
        self._administrative_source_survey_action.triggered.connect(partial(self.show_wiz_administrative_source_cad, self._context_collected))
        self._spatial_source_survey_action.triggered.connect(partial(self.show_wiz_spatial_source_cad, self._context_collected))
        self._upload_source_files_survey_action.triggered.connect(partial(self.upload_source_files, self._context_collected))
        self._quality_survey_action.triggered.connect(partial(self.show_dlg_quality, self._context_collected))
        self._fix_ladm_col_relations_action.triggered.connect(partial(self.call_fix_ladm_col_relations, self._context_collected))

        self.gui_builder.register_actions({
            ACTION_CREATE_POINT: self._point_surveying_and_representation_survey_action,
            ACTION_CREATE_BOUNDARY: self._boundary_surveying_and_representation_survey_action,
            ACTION_CREATE_PLOT: self._plot_spatial_unit_survey_action,
            ACTION_CREATE_BUILDING: self._building_spatial_unit_survey_action,
            ACTION_CREATE_BUILDING_UNIT: self._building_unit_spatial_unit_survey_action,
            ACTION_CREATE_RIGHT_OF_WAY: self._right_of_way_survey_action,
            ACTION_CREATE_EXT_ADDRESS: self._extaddress_survey_action,
            ACTION_CREATE_PARCEL: self._parcel_baunit_survey_action,
            ACTION_CREATE_PARTY: self._col_party_survey_action,
            ACTION_CREATE_GROUP_PARTY: self._group_party_survey_action,
            ACTION_CREATE_ADMINISTRATIVE_SOURCE: self._administrative_source_survey_action,
            ACTION_CREATE_SPATIAL_SOURCE: self._spatial_source_survey_action,
            ACTION_UPLOAD_PENDING_SOURCE: self._upload_source_files_survey_action,
            ACTION_CREATE_RIGHT: self._right_rrr_survey_action,
            ACTION_CREATE_RESTRICTION: self._restriction_rrr_survey_action,
            ACTION_CHECK_QUALITY_RULES: self._quality_survey_action,
            ACTION_FIX_LADM_COL_RELATIONS: self._fix_ladm_col_relations_action})

    def create_cadastre_form_actions(self):
        self._property_record_card_action = QAction(
            QIcon(":/Asistente-LADM-COL/resources/images/tables.png"),
            QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Property Record Card"),
            self.main_window)

        # Connections
        self._property_record_card_action.triggered.connect(self.show_wiz_property_record_card)

    def create_valuation_actions(self):
        self._parcel_valuation_action = QAction(
            QIcon(":/Asistente-LADM-COL/resources/images/tables.png"),
            QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Parcel"),
            self.main_window)
        self._building_unit_valuation_action = QAction(
            QIcon(":/Asistente-LADM-COL/resources/images/tables.png"),
            QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Building Unit"),
            self.main_window)
        self._building_unit_qualification_valuation_action = QAction(
            QIcon(":/Asistente-LADM-COL/resources/images/tables.png"),
            QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Building Unit Qualification"),
            self.main_window)
        self._geoeconomic_zone_valuation_action = QAction(
            QIcon(":/Asistente-LADM-COL/resources/images/polygons.png"),
            QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Geoeconomic Zone"),
            self.main_window)
        self._physical_zone_valuation_action = QAction(
            QIcon(":/Asistente-LADM-COL/resources/images/polygons.png"),
            QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Physical Zone"),
            self.main_window)

        # Connections
        self._parcel_valuation_action.triggered.connect(self.show_wiz_parcel_valuation)
        self._building_unit_valuation_action.triggered.connect(partial(self.show_wiz_building_unit_valuation, self._context_collected))
        self._building_unit_qualification_valuation_action.triggered.connect(partial(
            self.show_wiz_building_unit_qualification_valuation, self._context_collected))
        self._geoeconomic_zone_valuation_action.triggered.connect(partial(self.show_wiz_geoeconomic_zone_valuation, self._context_collected))
        self._physical_zone_valuation_action.triggered.connect(partial(self.show_wiz_physical_zone_valuation_action, self._context_collected))

    def create_change_detection_actions(self):
        self._query_changes_per_parcel_action = QAction(
            QCoreApplication.translate("AsistenteLADMCOLPlugin", "Query per parcel"), self.main_window)
        self._query_changes_all_parcels_action = QAction(
            QCoreApplication.translate("AsistenteLADMCOLPlugin", "Query all parcels"), self.main_window)
        self._change_detections_settings_action = QAction(
            QCoreApplication.translate("AsistenteLADMCOLPlugin", "Change detection settings"), self.main_window)

        # Set connections
        self._query_changes_per_parcel_action.triggered.connect(partial(self.query_changes_per_parcel, self._context_collected_supplies))
        self._query_changes_all_parcels_action.triggered.connect(partial(self.query_changes_all_parcels, self._context_collected_supplies))
        self._change_detections_settings_action.triggered.connect(partial(self.show_change_detection_settings, self._context_collected_supplies))

        self.gui_builder.register_actions({
            ACTION_CHANGE_DETECTION_PER_PARCEL: self._query_changes_per_parcel_action,
            ACTION_CHANGE_DETECTION_ALL_PARCELS: self._query_changes_all_parcels_action,
            ACTION_CHANGE_DETECTION_SETTINGS: self._change_detections_settings_action
        })

    def create_generic_actions(self):
        self._load_layers_action = QAction(QIcon(":/Asistente-LADM-COL/resources/images/load_layers.png"), QCoreApplication.translate("AsistenteLADMCOLPlugin", "Load layers"),
                                           self.main_window)
        self._queries_action = QAction(QIcon(":/Asistente-LADM-COL/resources/images/search.png"), QCoreApplication.translate("AsistenteLADMCOLPlugin", "Queries"),
                                       self.main_window)
        self._annex_17_action = QAction(QIcon(":/Asistente-LADM-COL/resources/images/report_annex_17.svg"),
                                        QCoreApplication.translate("AsistenteLADMCOLPlugin", "Annex 17"),
                                        self.main_window)
        self._annex_17_action.triggered.connect(partial(self.call_annex_17_report_generation, self._context_collected))
        self._ant_map_action = QAction(QIcon(":/Asistente-LADM-COL/resources/images/report_ant.svg"),
                                       QCoreApplication.translate("AsistenteLADMCOLPlugin", "ANT Map"),
                                       self.main_window)
        self._ant_map_action.triggered.connect(partial(self.call_ant_map_report_generation, self._context_collected))
        self._import_schema_action = QAction(QIcon(":/Asistente-LADM-COL/resources/images/schema_import.svg"),
            QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create LADM-COL structure"), self.main_window)

        self._import_data_action = QAction(QIcon(":/Asistente-LADM-COL/resources/images/import_xtf.svg"),
                                           QCoreApplication.translate("AsistenteLADMCOLPlugin", "Import data"),
                                           self.main_window)
        self._export_data_action = QAction(QIcon(":/Asistente-LADM-COL/resources/images/export_to_xtf.svg"),
                                           QCoreApplication.translate("AsistenteLADMCOLPlugin", "Export data"),
                                           self.main_window)
        self._settings_action = QAction(QIcon(":/Asistente-LADM-COL/resources/images/settings.svg"),
                                        QCoreApplication.translate("AsistenteLADMCOLPlugin", "Settings"),
                                        self.main_window)
        self._help_action = QAction(QIcon(":/Asistente-LADM-COL/resources/images/help.png"),
                                    QCoreApplication.translate("AsistenteLADMCOLPlugin", "Help"),
                                    self.main_window)
        self._about_action = QAction(QIcon(":/Asistente-LADM-COL/resources/images/info.svg"), QCoreApplication.translate("AsistenteLADMCOLPlugin", "About"),
                                     self.main_window)

        self._import_schema_action.triggered.connect(partial(self.show_dlg_import_schema, self._context_collected, **{'selected_models':list()}))
        self._import_data_action.triggered.connect(partial(self.show_dlg_import_data, self._context_collected))
        self._export_data_action.triggered.connect(partial(self.show_dlg_export_data, self._context_collected))
        self._queries_action.triggered.connect(partial(self.show_queries, self._context_collected))
        self._load_layers_action.triggered.connect(partial(self.load_layers_from_qgis_model_baker, self._context_collected))
        self._settings_action.triggered.connect(partial(self.show_settings, self._context_settings))
        self._help_action.triggered.connect(partial(show_plugin_help, ''))
        self._about_action.triggered.connect(self.show_about_dialog)

        self.gui_builder.register_actions({
            ACTION_REPORT_ANNEX_17: self._annex_17_action,
            ACTION_REPORT_ANT: self._ant_map_action,
            ACTION_LOAD_LAYERS: self._load_layers_action,
            ACTION_PARCEL_QUERY: self._queries_action,
            ACTION_CHECK_QUALITY_RULES: self._quality_survey_action,
            ACTION_SCHEMA_IMPORT: self._import_schema_action,
            ACTION_IMPORT_DATA: self._import_data_action,
            ACTION_EXPORT_DATA: self._export_data_action,
            ACTION_SETTINGS: self._settings_action,
            ACTION_HELP: self._help_action,
            ACTION_ABOUT: self._about_action
        })

    def initialize_processing_resources(self):
        """
        Add custom provider, models and scripts to QGIS
        """
        QgsApplication.processingRegistry().addProvider(self.ladm_col_provider)

        connect_provider_added = False
        if QgsApplication.processingRegistry().providerById('model'):
            self.add_processing_resources('model')
        else:
            connect_provider_added = True

        if QgsApplication.processingRegistry().providerById('script'):
            self.add_processing_resources('script')
        else:
            connect_provider_added = True

        if connect_provider_added:  # We need to wait until processing is initialized
            QgsApplication.processingRegistry().providerAdded.connect(self.add_processing_resources)

    def add_processing_resources(self, provider_id):
        if provider_id not in ['model', 'script']:
            return

        if sorted(self.__processing_resources_installed) == ["models", "script"]:  # We are done, disconnect.
            QgsApplication.processingRegistry().providerAdded.disconnect(self.add_processing_resources)

        if provider_id == 'model':
            # Add LADM-COL models
            basepath = os.path.dirname(os.path.abspath(__file__))
            plugin_models_dir = os.path.join(basepath, "lib", "processing", "models")

            count = 0
            for filename in glob.glob(os.path.join(plugin_models_dir, '*.model3')):
                alg = QgsProcessingModelAlgorithm()
                if not alg.fromFile(filename):
                    self.logger.critical(__name__, "Couldn't load model from {}".format(filename))
                    return

                destFilename = os.path.join(ModelerUtils.modelsFolders()[0], os.path.basename(filename))
                shutil.copyfile(filename, destFilename)
                count += 1

            if count:
                QgsApplication.processingRegistry().providerById('model').refreshAlgorithms()
                self.logger.debug(__name__, "{} LADM-COL models were installed!".format(count))

            self.__processing_resources_installed.append('model')
        elif provider_id == 'script':
            # Add LADM-COL scripts
            basepath = os.path.dirname(os.path.abspath(__file__))
            plugin_scripts_dir = os.path.join(basepath, "lib", "processing", "scripts")

            count = 0
            scripts_dir = ScriptUtils.defaultScriptsFolder()
            for filename in glob.glob(os.path.join(plugin_scripts_dir, '*.py')):
                try:
                    shutil.copy(filename, scripts_dir)
                    count += 1
                except OSError as e:
                    self.logger.critical(__name__, "Couldn't install LADM-COL script '{}'!".format(filename))

            if count:
                QgsApplication.processingRegistry().providerById("script").refreshAlgorithms()
                self.logger.debug(__name__, "{} LADM-COL scripts were installed!".format(count))

            self.__processing_resources_installed.append('script')

    def enable_action(self, action_name, enable):
        if action_name == ANT_MAP_REPORT:
            self._ant_map_action.setEnabled(enable)
        elif action_name == ANNEX_17_REPORT:
            self._annex_17_action.setEnabled(enable)

    def show_message_with_open_table_attributes_button(self, msg, button_text, level, layer, filter):
        self.app.gui.clear_message_bar()  # Remove previous messages before showing a new one
        widget = self.iface.messageBar().createMessage("Asistente LADM-COL", msg)
        button = QPushButton(widget)
        button.setText(button_text)
        button.pressed.connect(partial(self.open_table, layer, filter))
        widget.layout().addWidget(button)
        self.iface.messageBar().pushWidget(widget, level, 15)

    def show_message_to_load_layer(self, msg, button_text, layer, level):
        self.app.gui.clear_message_bar()  # Remove previous messages before showing a new one
        widget = self.iface.messageBar().createMessage("Asistente LADM-COL", msg)
        button = QPushButton(widget)
        button.setText(button_text)
        button.pressed.connect(partial(self.load_layer, layer))
        widget.layout().addWidget(button)
        self.iface.messageBar().pushWidget(widget, level, 15)

    def show_message_to_open_about_dialog(self, msg):
        self.app.gui.clear_message_bar()  # Remove previous messages before showing a new one
        widget = self.iface.messageBar().createMessage("Asistente LADM-COL", msg)
        button = QPushButton(widget)
        button.setText(QCoreApplication.translate("AsistenteLADMCOLPlugin",
            "Open About Dialog"))
        button.pressed.connect(self.show_about_dialog)
        widget.layout().addWidget(button)
        self.iface.messageBar().pushWidget(widget, Qgis.Info, 60)

    def show_message_with_buttons_change_detection_all_and_per_parcel(self, msg):
        self.app.gui.clear_message_bar()  # Remove previous messages before showing a new one
        widget = self.iface.messageBar().createMessage("Asistente LADM-COL", msg)

        btn_query_per_parcel = QPushButton(widget)
        btn_query_per_parcel.setText(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Query per parcel"))
        btn_query_per_parcel.pressed.connect(partial(self.query_changes_per_parcel, self._context_collected_supplies))
        widget.layout().addWidget(btn_query_per_parcel)

        btn_query_all_parcels = QPushButton(widget)
        btn_query_all_parcels.setText(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Query all parcels"))
        btn_query_all_parcels.pressed.connect(partial(self.query_changes_all_parcels, self._context_collected_supplies))
        widget.layout().addWidget(btn_query_all_parcels)

        self.iface.messageBar().pushWidget(widget, Qgis.Success, 60)

    def show_message_with_settings_button(self, msg, button_text, level):
        self.app.gui.clear_message_bar()  # Remove previous messages before showing a new one
        widget = self.iface.messageBar().createMessage("Asistente LADM-COL", msg)
        button = QPushButton(widget)
        button.setText(button_text)
        button.pressed.connect(self.show_settings)
        widget.layout().addWidget(button)
        self.iface.messageBar().pushWidget(widget, level, 25)

    def show_message_with_close_wizard_button(self, msg, button_text, level):
        self.app.gui.clear_message_bar()  # Remove previous messages before showing a new one
        widget = self.iface.messageBar().createMessage("Asistente LADM-COL", msg)
        button = QPushButton(widget)
        button.setText(button_text)
        button.pressed.connect(self.close_wizard_if_opened)
        widget.layout().addWidget(button)
        self.iface.messageBar().pushWidget(widget, level, 25)

    def load_layer(self, layer):
        self.app.gui.clear_message_bar()
        self.app.core.get_layer(self.get_db_connection(), layer, load=True)

    def load_layers(self, layers):
        self.app.core.get_layers(self.get_db_connection(), layers, True)

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
        self.progress_message_bar = self.iface.messageBar().createMessage("Asistente LADM_COL", msg)
        self.log_quality_validation_progress = QProgressBar()
        self.log_quality_validation_progress.setFixedWidth(80)
        self.log_quality_total_rule_count = count
        self.log_quality_validation_progress.setMaximum(self.log_quality_total_rule_count * 10)
        self.progress_message_bar.layout().addWidget(self.log_quality_validation_progress)
        self.iface.messageBar().pushWidget(self.progress_message_bar, Qgis.Info)
        self.log_quality_validation_progress_count = 0
        self.log_quality_current_rule_count = 0

    def show_log_quality_button(self):
        self.button = QPushButton(self.progress_message_bar)
        self.button.pressed.connect(self.show_log_quality_dialog)
        self.button.setText(QCoreApplication.translate("LogQualityDialog", "Show Results"))
        self.progress_message_bar.layout().addWidget(self.button)
        QCoreApplication.processEvents()

    def set_log_quality_initial_progress(self, msg):
        self.log_quality_validation_progress_count += 2  # 20% of the current rule
        self.log_quality_validation_progress.setValue(self.log_quality_validation_progress_count)
        self.progress_message_bar.setText(
            QCoreApplication.translate("LogQualityDialog",
                                       "Checking {} out of {}: '{}'").format(
                                        self.log_quality_current_rule_count + 1,
                                        self.log_quality_total_rule_count,
                                        msg))
        QCoreApplication.processEvents()

    def set_log_quality_final_progress(self, msg):
        self.log_quality_validation_progress_count += 8  # 80% of the current rule
        self.log_quality_validation_progress.setValue(self.log_quality_validation_progress_count)
        self.log_quality_current_rule_count += 1
        if self.log_quality_current_rule_count ==  self.log_quality_total_rule_count:
            self.progress_message_bar.setText(QCoreApplication.translate("LogQualityDialog",
                "All the {} quality rules were checked! Click the button at the right-hand side to see a report.").format(self.log_quality_total_rule_count))
        else:
            self.progress_message_bar.setText(msg)
        QCoreApplication.processEvents()

    def show_log_quality_dialog(self):
        log_text, tolerance, log_total_time = self.quality_rule_engine.quality_rule_logger.get_log_text()
        dlg = LogQualityDialog(self.conn_manager.get_db_connector_from_source(), log_text, tolerance, log_total_time)
        dlg.exec_()

    def show_log_excel_button(self, text):
        self.progress_message_bar = self.iface.messageBar().createMessage("Import from Excel",
                                                                          QCoreApplication.translate("ImportFromExcelDialog",
                                       "Some errors were found while importing from the intermediate Excel file into LADM-COL!"))
        self.button = QPushButton(self.progress_message_bar)
        self.button.pressed.connect(self.show_log_excel_dialog)
        self.button.setText(QCoreApplication.translate("ImportFromExcelDialog", "Show errors found"))
        self.progress_message_bar.layout().addWidget(self.button)
        self.iface.messageBar().pushWidget(self.progress_message_bar, Qgis.Warning)
        self.log_excel_text = text

    def show_log_excel_dialog(self):
        dlg = LogExcelDialog(self.log_excel_text)
        dlg.exec_()

    @_db_connection_required
    @_supplies_model_required
    def show_wiz_supplies_etl(self, *args):
        # TODO: Should use @_activate_processing_plugin

        if not args or not isinstance(args[0], Context):
            return

        context = args[0]

        wiz = SuppliesETLWizard(self.get_db_connection(SUPPLIES_DB_SOURCE), self.conn_manager, self.iface.mainWindow())
        if isinstance(context, TaskContext):
            wiz.on_result.connect(context.get_slot_on_result())
        wiz.exec_()

    @_db_connection_required
    @_supplies_model_required
    def show_missing_cobol_supplies_dialog(self, *args):
        if not args or not isinstance(args[0], Context):
            return

        context = args[0]

        dlg = MissingCobolSupplies(self.get_db_connection(SUPPLIES_DB_SOURCE), self.conn_manager, self.iface.mainWindow())
        if isinstance(context, TaskContext):
            dlg.on_result.connect(context.get_slot_on_result())
        dlg.exec_()

    @_validate_if_wizard_is_open
    @_qgis_model_baker_required
    @_db_connection_required
    @_survey_model_required
    def call_explode_boundaries(self, *args):
        self.toolbar.build_boundary(self.get_db_connection())

    @_validate_if_wizard_is_open
    @_qgis_model_baker_required
    @_db_connection_required
    @_survey_model_required
    def call_topological_editing(self, *args):
        self.app.core.enable_topological_editing(self.get_db_connection())

    @_validate_if_wizard_is_open
    @_qgis_model_baker_required
    @_db_connection_required
    @_survey_model_required
    def call_fill_topology_table_pointbfs(self, *args):
        self.toolbar.fill_topology_table_pointbfs(self.get_db_connection())

    @_validate_if_wizard_is_open
    @_qgis_model_baker_required
    @_db_connection_required
    @_survey_model_required
    def call_fill_topology_tables_morebfs_less(self, *args):
        self.toolbar.fill_topology_tables_morebfs_less(self.get_db_connection())

    @_validate_if_wizard_is_open
    @_qgis_model_baker_required
    @_db_connection_required
    @_survey_model_required
    @_activate_processing_plugin
    def call_fill_right_of_way_relations(self, *args):
        self.right_of_way.fill_right_of_way_relations(self.get_db_connection())

    @_validate_if_wizard_is_open
    @_qgis_model_baker_required
    @_db_connection_required
    @_survey_model_required
    def call_ant_map_report_generation(self, *args):
        self.report_generator.generate_report(self.get_db_connection(), ANT_MAP_REPORT)

    @_validate_if_wizard_is_open
    @_qgis_model_baker_required
    @_db_connection_required
    @_survey_model_required
    def call_annex_17_report_generation(self, *args):
        self.report_generator.generate_report(self.get_db_connection(), ANNEX_17_REPORT)

    @_validate_if_wizard_is_open
    @_qgis_model_baker_required
    @_db_connection_required
    @_survey_model_required
    @_activate_processing_plugin
    def call_import_from_intermediate_structure(self, *args):
        self._dlg = ImportFromExcelDialog(self.iface, self.get_db_connection())
        self._dlg.log_excel_show_message_emitted.connect(self.show_log_excel_button)
        self._dlg.exec_()

    @_qgis_model_baker_required
    @_db_connection_required
    def call_fix_ladm_col_relations(self, *args):
        self.app.core.fix_ladm_col_relations(self.get_db_connection())  # Always for COLLECTED db

    def unload(self):
        self.session_logout(False, False)  # Do not show message when deactivating plugin, closing QGIS, etc.)
        self.uninstall_custom_expression_functions()

        self.gui_builder.unload_gui()

        # Close all connections
        self.conn_manager.close_db_connections()
        QgsApplication.processingRegistry().removeProvider(self.ladm_col_provider)

    @_validate_if_wizard_is_open
    def show_settings(self, *args):
        if args and isinstance(args[0], SettingsContext):
            context = args[0]
        else:
            context = SettingsContext()  # Context with default configuration for the Settings Dialog

        dlg = SettingsDialog(self.conn_manager, context)
        dlg.db_connection_changed.connect(self.conn_manager.db_connection_changed)

        if context.db_source == COLLECTED_DB_SOURCE:  # Only update cache and gui when db_source is collected
            dlg.db_connection_changed.connect(self.app.core.cache_layers_and_relations)
            dlg.active_role_changed.connect(self.call_refresh_gui)

        if context.action_type == EnumDbActionType.CONFIG:
            dlg.open_dlg_import_schema.connect(self.show_dlg_import_schema)

        dlg.exec_()

    def show_settings_clear_message_bar(self, context):
        self.show_settings(context)
        self.iface.messageBar().popWidget()  # Display the next message in the stack if any or hide the bar

    def use_current_db_connection(self, db_source):
        """ Slot useful when qsettings connection differs from conn_manager connection """
        db = self.get_db_connection(db_source)
        self.conn_manager.save_parameters_conn(db, db_source)  # Update QSettings
        self.conn_manager.set_db_connector_for_source(db, db_source)
        self.iface.messageBar().popWidget()

    def update_db_connection_from_qsettings(self, db_source):
        """ Slot useful when qsettings connection differs from conn_manager connection """
        self.conn_manager.update_db_connector_for_source(db_source)
        self.conn_manager.db_connection_changed.emit(self.get_db_connection(db_source),
                                                     self.get_db_connection(db_source).test_connection()[0],
                                                     db_source)
        self.iface.messageBar().popWidget()

    def show_plugin_manager(self):
        self.iface.actionManagePlugins().trigger()

    @_qgis_model_baker_required
    @_db_connection_required
    def load_layers_from_qgis_model_baker(self, *args):
        dlg = LoadLayersDialog(self.get_db_connection())
        dlg.exec_()

    @_validate_if_wizard_is_open
    @_qgis_model_baker_required
    @_db_connection_required
    @_survey_model_required
    def show_queries(self, *args):
        self.gui_builder.close_dock_widgets([DOCK_WIDGET_QUERIES])

        dock_widget_queries = DockWidgetQueries(self.iface,
                                                self.get_db_connection(),
                                                self.ladm_data)
        self.gui_builder.register_dock_widget(DOCK_WIDGET_QUERIES, dock_widget_queries)
        self.conn_manager.db_connection_changed.connect(dock_widget_queries.update_db_connection)
        dock_widget_queries.zoom_to_features_requested.connect(self.zoom_to_features)
        self.app.gui.add_tabified_dock_widget(Qt.RightDockWidgetArea, dock_widget_queries)

    def get_db_connection(self, db_source=COLLECTED_DB_SOURCE):
        return self.conn_manager.get_db_connector_from_source(db_source)

    @_validate_if_wizard_is_open
    @_qgis_model_baker_required
    def show_dlg_import_schema(self, *args, **kwargs):
        """
        Can be called from 1) an action, 2) from a signal or 3) directly.

        In 1) args has a Context argument and then a False argument from QAction.triggered.
        In 2) args comes with a dict inside (hence the "if args" below) from import_data.
        In 3) **{} is passed, hence the "if kwargs" below.
        """
        from .gui.qgis_model_baker.dlg_import_schema import DialogImportSchema

        if not args or not isinstance(args[0], Context):
            return

        context = args[0]

        # parse parameters
        params = dict()
        if len(args) > 1:
            args_params = args[1]
            if type(args_params) is dict:
                params.update(args_params)
        if kwargs:
            params.update(kwargs)

        selected_models_import_schema = params['selected_models'] if 'selected_models' in params else list()
        link_to_import_data = params['link_to_import_data'] if 'link_to_import_data' in params else True

        dlg = DialogImportSchema(self.iface, self.conn_manager, context, selected_models_import_schema, link_to_import_data)
        dlg.open_dlg_import_data.connect(partial(self.show_dlg_import_data, context))

        if isinstance(context, TaskContext):
            dlg.on_result.connect(context.get_slot_on_result())

        self.logger.info(__name__, "Import Schema dialog ({}) opened.".format(context.get_db_sources()[0]))
        dlg.exec_()

    @_validate_if_wizard_is_open
    @_qgis_model_baker_required
    def show_dlg_import_data(self, *args):
        from .gui.qgis_model_baker.dlg_import_data import DialogImportData

        if not args or not isinstance(args[0], Context):
            return

        context = args[0]

        dlg = DialogImportData(self.iface, self.conn_manager, context)
        dlg.open_dlg_import_schema.connect(partial(self.show_dlg_import_schema, context))

        if isinstance(context, TaskContext):
            dlg.on_result.connect(context.get_slot_on_result())

        self.logger.info(__name__, "Import data dialog ({}) opened.".format(context.get_db_sources()[0]))
        dlg.exec_()

    @_validate_if_wizard_is_open
    @_qgis_model_baker_required
    def show_dlg_export_data(self, *args):
        from .gui.qgis_model_baker.dlg_export_data import DialogExportData

        if not args or not isinstance(args[0], Context):
            return

        context = args[0]

        dlg = DialogExportData(self.iface, self.conn_manager, context)
        if isinstance(context, TaskContext):
            dlg.on_result.connect(context.get_slot_on_result())

        self.logger.info(__name__, "Export data dialog ({}) opened.".format(context.get_db_sources()[0]))
        dlg.exec_()

    @_validate_if_wizard_is_open
    @_qgis_model_baker_required
    @_db_connection_required
    @_survey_model_required
    def show_wiz_point_cad(self, *args):
        self.wiz = CreatePointsSurveyWizard(self.iface, self.get_db_connection())
        self.exec_wizard(self.wiz)

    @_db_connection_required
    @_survey_model_required
    def show_wiz_boundaries_cad(self, *args):
        self.show_wizard(WIZARD_CREATE_BOUNDARY_SURVEY)

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
    @_survey_model_required
    def show_wiz_plot_cad(self, *args):
        self.show_wizard(WIZARD_CREATE_PLOT_SURVEY)

    @_db_connection_required
    @_survey_model_required
    def show_wiz_building_cad(self, *args):
        self.show_wizard(WIZARD_CREATE_BUILDING_SURVEY)

    @_db_connection_required
    @_survey_model_required
    def show_wiz_building_unit_cad(self, *args):
        self.show_wizard(WIZARD_CREATE_BUILDING_UNIT_SURVEY)

    @_db_connection_required
    @_survey_model_required
    def show_wiz_right_of_way_cad(self, *args):
        self.show_wizard(WIZARD_CREATE_RIGHT_OF_WAY_SURVEY)

    @_db_connection_required
    @_survey_model_required
    def show_wiz_extaddress_cad(self, *args):
        self.show_wizard(WIZARD_CREATE_EXT_ADDRESS_SURVEY)

    @_db_connection_required
    @_survey_model_required
    def show_wiz_parcel_cad(self, *args):
        self.show_wizard(WIZARD_CREATE_PARCEL_SURVEY)

    @_db_connection_required
    @_survey_model_required
    def show_wiz_col_party_cad(self, *args):
        self.show_wizard(WIZARD_CREATE_COL_PARTY_CADASTRAL)

    @_validate_if_wizard_is_open
    @_qgis_model_baker_required
    @_db_connection_required
    @_survey_model_required
    def show_dlg_group_party(self, *args):
        namespace_enabled = QSettings().value('Asistente-LADM-COL/automatic_values/namespace_enabled', True, bool)
        local_id_enabled = QSettings().value('Asistente-LADM-COL/automatic_values/local_id_enabled', True, bool)
        t_ili_tid_enabled = QSettings().value('Asistente-LADM-COL/automatic_values/t_ili_tid_enabled', True, bool)

        if not namespace_enabled or not local_id_enabled or not t_ili_tid_enabled:
            self.show_message_with_settings_button(QCoreApplication.translate("CreateGroupPartySurvey",
                                                       "First enable automatic values for namespace, local_id and t_ili_tid fields before creating group parties. Click the button to open the settings dialog."),
                                                   QCoreApplication.translate("CreateGroupPartySurvey", "Open Settings"),
                                                   Qgis.Info)
            return

        dlg = CreateGroupPartySurvey(self.iface, self.get_db_connection())

        # Check if required layers are available
        if dlg.required_layers_are_available():
            # Load required data, it is necessary in the dlg
            dlg.load_parties_data()
            dlg.exec_()
        else:
            del dlg

    @_db_connection_required
    @_survey_model_required
    def show_wiz_right_rrr_cad(self, *args):
        self.show_wizard(WIZARD_CREATE_RIGHT_SURVEY)

    @_db_connection_required
    @_survey_model_required
    def show_wiz_restriction_rrr_cad(self, *args):
        self.show_wizard(WIZARD_CREATE_RESTRICTION_SURVEY)

    @_db_connection_required
    @_survey_model_required
    def show_wiz_administrative_source_cad(self, *args):
        self.show_wizard(WIZARD_CREATE_ADMINISTRATIVE_SOURCE_SURVEY)

    @_db_connection_required
    @_survey_model_required
    def show_wiz_spatial_source_cad(self, *args):
        self.show_wizard(WIZARD_CREATE_SPATIAL_SOURCE_SURVEY)

    @_validate_if_wizard_is_open
    @_qgis_model_baker_required
    @_db_connection_required
    @_survey_model_required
    def upload_source_files(self, *args):
        self.app.core.upload_source_files(self.get_db_connection())

    @_validate_if_wizard_is_open
    @_qgis_model_baker_required
    @_db_connection_required
    @_survey_model_required
    @_activate_processing_plugin
    def show_dlg_quality(self, *args):
        quality_dialog = QualityDialog()
        quality_dialog.exec_()

        self.quality_rule_engine = QualityRuleEngine(self.get_db_connection(), quality_dialog.selected_rules)
        self.quality_rule_engine.quality_rule_logger.show_message_emitted.connect(self.show_log_quality_message)
        self.quality_rule_engine.quality_rule_logger.show_button_emitted.connect(self.show_log_quality_button)
        self.quality_rule_engine.quality_rule_logger.set_initial_progress_emitted.connect(self.set_log_quality_initial_progress)
        self.quality_rule_engine.quality_rule_logger.set_final_progress_emitted.connect(self.set_log_quality_final_progress)
        self.quality_rule_engine.validate_quality_rules()

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
    @_survey_model_required
    @_validate_if_layers_in_editing_mode_with_changes
    def query_changes_per_parcel(self, *args):
        msg = QCoreApplication.translate("AsistenteLADMCOLPlugin", "Opening Query Changes per Parcel panel...")
        with ProcessWithStatus(msg):
            self.show_change_detection_dockwidget(False)  # all_parcels_mode is False, we want the per_parcel_mode instead

    @_validate_if_wizard_is_open
    @_qgis_model_baker_required
    @_map_swipe_tool_required
    @_db_connection_required
    @_survey_model_required
    @_validate_if_layers_in_editing_mode_with_changes
    def query_changes_all_parcels(self, *args):
        msg = QCoreApplication.translate("AsistenteLADMCOLPlugin", "Opening Query Changes for All Parcels panel...")
        with ProcessWithStatus(msg):
            self.show_change_detection_dockwidget()

    def show_change_detection_dockwidget(self, all_parcels_mode=True):
        self.gui_builder.close_dock_widgets([DOCK_WIDGET_CHANGE_DETECTION])

        dock_widget_change_detection = DockWidgetChangeDetection(self.iface,
                                                                 self.get_db_connection(),
                                                                 self.get_db_connection(SUPPLIES_DB_SOURCE),
                                                                 self.ladm_data,
                                                                 all_parcels_mode)
        self.gui_builder.register_dock_widget(DOCK_WIDGET_CHANGE_DETECTION, dock_widget_change_detection)
        self.conn_manager.db_connection_changed.connect(dock_widget_change_detection.update_db_connection)
        dock_widget_change_detection.zoom_to_features_requested.connect(self.zoom_to_features)
        self.app.gui.add_tabified_dock_widget(Qt.RightDockWidgetArea, dock_widget_change_detection)

    @_validate_if_layers_in_editing_mode_with_changes
    def show_change_detection_settings(self, *args, **kwargs):
        dlg = ChangeDetectionSettingsDialog(self.conn_manager)
        dlg.exec_()

    def open_table(self, layer, filter=None):
        self.iface.showAttributeTable(layer, filter)

    def show_about_dialog(self):
        if self._about_dialog is None:
            self._about_dialog = AboutDialog()
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
    def show_wizard(self, wizard_name, *args, **kwargs):
        wiz_settings = self.wizard_config.get_wizard_config(self.get_db_connection().names, wizard_name)
        if self.app.core.required_layers_are_available(self.get_db_connection(),
                                                         wiz_settings[WIZARD_LAYERS],
                                                         wiz_settings[WIZARD_TOOL_NAME]):
            self.wiz = wiz_settings[WIZARD_CLASS](self.iface, self.get_db_connection(), wiz_settings)
            if wiz_settings[WIZARD_TYPE] & EnumWizardType.SPATIAL_WIZARD:
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
        dlg.active_role_changed.connect(self.call_refresh_gui)
        dlg.exec_()

        if self.session.is_user_logged():
            # If the user didn't change the active role in the LADM-COL
            # Assistant, the dock might not be deleted yet. Just in case...
            self.gui_builder.close_dock_widgets([DOCK_WIDGET_TRANSITION_SYSTEM])

            # Update controls: It was to be a SIGNAL-SLOT, but since a GUI
            # refresh happens in between, the control update would be lost,
            # so, now we call it directly.
            self.set_login_controls_visibility(True)

            # Show Transitional System dock widget
            user = self.session.get_logged_st_user()
            dock_widget_transitional_system = DockWidgetTransitionalSystem(user, self.main_window)
            self.gui_builder.register_dock_widget(DOCK_WIDGET_TRANSITION_SYSTEM, dock_widget_transitional_system)
            self.conn_manager.db_connection_changed.connect(dock_widget_transitional_system.update_db_connection)
            dock_widget_transitional_system.logout_requested.connect(self.session_logout)
            dock_widget_transitional_system.trigger_action_emitted.connect(self.trigger_action_emitted)
            self.session.logout_finished.connect(dock_widget_transitional_system.after_logout)
            self.app.gui.add_tabified_dock_widget(Qt.RightDockWidgetArea, dock_widget_transitional_system)

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
                self.logger.log_message(__name__, msg, Qgis.Info if logged_out else Qgis.Warning, EnumLogHandler.MESSAGE_BAR)

    def set_login_controls_visibility(self, login_activated):
        """
        React upon changes in ST login. If a user is logged in or logged out, we want to show only certain controls.

        :param login_activated: Boolean, True if a user is logged in
        """
        self._st_login_action.setVisible(not login_activated)
        self._st_logout_action.setVisible(login_activated)

        self._st_login_action.setEnabled(not login_activated)
        self._st_logout_action.setEnabled(login_activated)

    def trigger_action_emitted(self, action_tag):
        action = self.gui_builder.get_action(action_tag)
        if action is not None:
            action.trigger()

    def show_dlg_st_upload_file(self, *args, **kwargs):
        if not args and not kwargs:
            return

        context = None

        # Parse parameters
        params = dict()

        if isinstance(args[0], Context):
            context = args[0]
        elif type(args[0]) is dict:  # No context was given
            params.update(args[0])

        if len(args) > 1:  # Context was passed as args[0]
            params.update(args[1])

        if kwargs:
            params.update(kwargs)

        if 'request_id' not in params or 'supply_type' not in params:
            return

        request_id = params['request_id']
        supply_type = params['supply_type']

        dlg = STUploadFileDialog(request_id, supply_type, self.main_window)
        if isinstance(context, TaskContext):
            dlg.on_result.connect(context.get_slot_on_result())

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
                db.names.INI_PARCEL_SUPPLIES_T: None,
                db.names.GC_PARCEL_T: None,
                db.names.SNR_PARCEL_REGISTRY_T: None
            }
            self.app.core.get_layers(db, layers, load=True)

    def add_indicators(self, node_name, node_type):
        """Slot to inject the db object"""
        self.app.add_indicators(self.get_db_connection(), node_name, node_type)

    def export_error_group(self):
        self.app.gui.export_error_group()
