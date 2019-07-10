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
                              QSettings)
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import (QAction,
                                 QMenu,
                                 QPushButton,
                                 QProgressBar)

from qgis.core import (Qgis,
                       QgsApplication,
                       QgsProcessingModelAlgorithm)

from .config.general_config import (CADASTRE_MENU_OBJECTNAME,
                                    LADM_COL_MENU_OBJECTNAME,
                                    QGIS_MODEL_BAKER_MIN_REQUIRED_VERSION,
                                    QGIS_MODEL_BAKER_EXACT_REQUIRED_VERSION,
                                    PROPERTY_RECORD_CARD_MENU_OBJECTNAME,
                                    PLUGIN_NAME,
                                    PLUGIN_VERSION,
                                    RELEASE_URL,
                                    URL_REPORTS_LIBRARIES,
                                    TOOL_BAR_NAME,
                                    VALUATION_MENU_OBJECTNAME)
from .utils.decorators import (_db_connection_required,
                               _qgis_model_baker_required,
                               _activate_processing_plugin)

from .gui.about_dialog import AboutDialog
from .gui.controlled_measurement_dialog import ControlledMeasurementDialog
from .gui.wizards.cadastre.source.create_administrative_source_cadastre_wizard import CreateAdministrativeSourceCadastreWizard
from .gui.wizards.cadastre.surveying.create_boundaries_cadastre_wizard import CreateBoundariesCadastreWizard
from .gui.wizards.cadastre.spatial_unit.create_building_cadastre_wizard import CreateBuildingCadastreWizard
from .gui.wizards.cadastre.spatial_unit.create_building_unit_cadastre_wizard import CreateBuildingUnitCadastreWizard
from .gui.wizards.cadastre.spatial_unit.create_right_of_way_cadastre_wizard import CreateRightOfWayCadastreWizard
from .gui.wizards.cadastre.spatial_unit.associate_extaddress_cadastre_wizard import AssociateExtAddressWizard
from .gui.wizards.cadastre.party.create_col_party_cadastre_wizard import CreateColPartyCadastreWizard
from .gui.wizards.cadastre.party.create_group_party_cadastre import CreateGroupPartyCadastre
from .gui.wizards.property_record_card.create_legal_party_prc import CreateLegalPartyPRCWizard
from .gui.wizards.property_record_card.create_market_research_prc import CreateMarketResearchPRCWizard
from .gui.wizards.property_record_card.create_natural_party_prc import CreateNaturalPartyPRCWizard
from .gui.wizards.property_record_card.create_nuclear_family_prc import CreateNuclearFamilyPRCWizard
from .gui.wizards.cadastre.baunit.create_parcel_cadastre_wizard import CreateParcelCadastreWizard
from .gui.wizards.cadastre.spatial_unit.create_plot_cadastre_wizard import CreatePlotCadastreWizard
from .gui.wizards.cadastre.surveying.create_points_cadastre_wizard import CreatePointsCadastreWizard
from .gui.wizards.property_record_card.create_property_record_card_prc import CreatePropertyRecordCardPRCWizard
from .gui.wizards.cadastre.rrr.create_responsibility_cadastre_wizard import CreateResponsibilityCadastreWizard
from .gui.wizards.cadastre.rrr.create_restriction_cadastre_wizard import CreateRestrictionCadastreWizard
from .gui.wizards.cadastre.rrr.create_right_cadastre_wizard import CreateRightCadastreWizard
from .gui.wizards.cadastre.source.create_spatial_source_cadastre_wizard import CreateSpatialSourceCadastreWizard
from .gui.wizards.valuation.create_parcel_valuation_wizard import CreateParcelValuationWizard
from .gui.wizards.valuation.create_horizontal_property_valuation_wizard import CreateHorizontalPropertyValuationWizard
from .gui.wizards.valuation.create_common_equipment_valuation_wizard import CreateCommonEquipmentValuationWizard
from .gui.wizards.valuation.create_building_valuation_wizard import CreateBuildingValuationWizard
from .gui.wizards.valuation.create_building_unit_valuation_wizard import CreateBuildingUnitValuationWizard
from .gui.wizards.valuation.create_building_unit_qualification_valuation_wizard import CreateBuildingUnitQualificationValuationWizard
from .gui.wizards.valuation.create_geoeconomic_zone_valuation_wizard import CreateGeoeconomicZoneValuationWizard
from .gui.wizards.valuation.create_physical_zone_valuation_wizard import CreatePhysicalZoneValuationWizard
from .gui.dialog_load_layers import DialogLoadLayers
from .gui.dialog_quality import DialogQuality
from .gui.dialog_import_from_excel import DialogImportFromExcel
from .gui.dockwidget_queries import DockWidgetQueries
from .gui.log_quality_dialog import LogQualityDialog
from .gui.reports import ReportGenerator
from .gui.toolbar import ToolBar
from .gui.log_excel_dialog import LogExcelDialog
from .data.ladm_data import LADM_DATA
from .processing.ladm_col_provider import LADMCOLAlgorithmProvider
from .utils.qgis_utils import QGISUtils
from .utils.qt_utils import get_plugin_metadata
from .utils.quality import QualityUtils
from .lib.db.enum_db_action_type import EnumDbActionType

class AsistenteLADMCOLPlugin(QObject):
    def __init__(self, iface):
        QObject.__init__(self)
        self.iface = iface
        self.log = QgsApplication.messageLog()
        self._about_dialog = None
        self._dock_widget_queries = None
        self.toolbar = None
        self.wiz_address = None

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
        self.quality = QualityUtils(self.qgis_utils)
        self.toolbar = ToolBar(self.iface, self.qgis_utils)
        self.ladm_data = LADM_DATA(self.qgis_utils)
        self.report_generator = ReportGenerator(self.qgis_utils, self.ladm_data)

        # Menus
        self.add_cadastre_menu()

        self._menu.addSeparator()
        self._load_layers_action = QAction(QIcon(), QCoreApplication.translate("AsistenteLADMCOLPlugin", "Load layers"), self.iface.mainWindow())
        self._queries_action = QAction(QIcon(), QCoreApplication.translate("AsistenteLADMCOLPlugin", "Queries"), self.iface.mainWindow())
        self._menu.addActions([self._load_layers_action,
                              self._queries_action])
        self._menu.addSeparator()
        self.add_data_management_menu()
        self._settings_action = QAction(QIcon(), QCoreApplication.translate("AsistenteLADMCOLPlugin", "Settings"), self.iface.mainWindow())
        self._help_action = QAction(QIcon(), QCoreApplication.translate("AsistenteLADMCOLPlugin", "Help"), self.iface.mainWindow())
        self._about_action = QAction(QIcon(), QCoreApplication.translate("AsistenteLADMCOLPlugin", "About"), self.iface.mainWindow())
        self._menu.addActions([self._settings_action,
                               self._help_action,
                               self._about_action])

        # Connections

        self._import_schema_action.triggered.connect(self.show_dlg_import_schema)
        self._import_data_action.triggered.connect(self.show_dlg_import_data)
        self._export_data_action.triggered.connect(self.show_dlg_export_data)
        self._controlled_measurement_action.triggered.connect(self.show_dlg_controlled_measurement)
        self._queries_action.triggered.connect(self.show_queries)
        self._load_layers_action.triggered.connect(self.load_layers_from_qgis_model_baker)
        self._settings_action.triggered.connect(self.show_settings)
        self._help_action.triggered.connect(self.show_help)
        self._about_action.triggered.connect(self.show_about_dialog)

        self.qgis_utils.action_add_feature_requested.connect(self.trigger_add_feature)
        self.qgis_utils.action_vertex_tool_requested.connect(self.trigger_vertex_tool)
        self.qgis_utils.activate_layer_requested.connect(self.activate_layer)
        self.qgis_utils.clear_status_bar_emitted.connect(self.clear_status_bar)
        self.qgis_utils.clear_message_bar_emitted.connect(self.clear_message_bar)
        self.qgis_utils.create_progress_message_bar_emitted.connect(self.create_progress_message_bar)
        self.qgis_utils.remove_error_group_requested.connect(self.remove_error_group)
        self.qgis_utils.layer_symbology_changed.connect(self.refresh_layer_symbology)
        self.qgis_utils.db_connection_changed.connect(self.refresh_menus)
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
        self._build_boundary_action = QAction(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Build boundaries..."), self.iface.mainWindow())
        self._build_boundary_action.triggered.connect(self.call_explode_boundaries)
        self._topological_editing_action = QAction(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Move nodes..."), self.iface.mainWindow())
        self._topological_editing_action.triggered.connect(self.call_topological_editing)
        self._fill_point_BFS_action = QAction(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Fill Point BFS"), self.iface.mainWindow())
        self._fill_point_BFS_action.triggered.connect(self.call_fill_topology_table_pointbfs)
        self._fill_more_BFS_less_action = QAction(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Fill More BFS and Less"), self.iface.mainWindow())
        self._fill_more_BFS_less_action.triggered.connect(self.call_fill_topology_tables_morebfs_less)
        self._fill_right_of_way_relations_action = QAction(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Fill Right of Way Relations"), self.iface.mainWindow())
        self._fill_right_of_way_relations_action.triggered.connect(self.call_fill_right_of_way_relations)
        self._report_action = QAction(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Generate Annex 17"), self.iface.mainWindow())
        self._report_action.triggered.connect(self.call_report_generation)
        self._import_from_intermediate_structure_action = QAction(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Import from intermediate structure"),
                                      self.iface.mainWindow())
        self._import_from_intermediate_structure_action.triggered.connect(self.call_import_from_intermediate_structure)
        self._ladm_col_toolbar = self.iface.addToolBar(QCoreApplication.translate("AsistenteLADMCOLPlugin", "LADM-COL tools"))
        self._ladm_col_toolbar.setObjectName("ladmcoltools")
        self._ladm_col_toolbar.setToolTip(TOOL_BAR_NAME)
        self._ladm_col_toolbar.addActions([self._build_boundary_action,
                                           self._topological_editing_action,
                                           self._fill_point_BFS_action,
                                           self._fill_more_BFS_less_action,
                                           self._fill_right_of_way_relations_action,
                                           self._import_from_intermediate_structure_action,
                                           self._report_action])

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

    def call_refresh_menus(self):
        # Refresh menus on QGIS start
        db = self.get_db_connection()
        res, msg = db.test_connection()
        self.refresh_menus(db, res)

    def add_data_management_menu(self):
        self._data_management_menu = QMenu(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Data Management"), self._menu)
        self._import_schema_action = QAction(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create LADM-COL structure"), self._data_management_menu)
        self._import_data_action = QAction(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Import data"), self._data_management_menu)
        self._export_data_action = QAction(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Export data"), self._data_management_menu)
        self._data_management_menu.addActions([self._import_schema_action, self._import_data_action, self._export_data_action])

        self._menu.addMenu(self._data_management_menu)


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
        self._responsibility_rrr_cadastre_action = QAction(
                QIcon(":/Asistente-LADM_COL/resources/images/tables.png"),
                QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Responsibility"),
                self._rrr_cadastre_menu)
        self._rrr_cadastre_menu.addActions([self._right_rrr_cadastre_action,
                                            self._restriction_rrr_cadastre_action,
                                            self._responsibility_rrr_cadastre_action])

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
        self._responsibility_rrr_cadastre_action.triggered.connect(self.show_wiz_responsibility_rrr_cad)
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
        self._market_research_property_record_card_action = QAction(
            QIcon(":/Asistente-LADM_COL/resources/images/tables.png"),
            QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Market Research"),
            self._property_record_card_menu)
        self._nuclear_family_property_record_card_action = QAction(
            QIcon(":/Asistente-LADM_COL/resources/images/tables.png"),
            QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Nuclear Family"),
            self._property_record_card_menu)
        self._natural_party_property_record_card_action = QAction(
            QIcon(":/Asistente-LADM_COL/resources/images/tables.png"),
            QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Natural Party"),
            self._property_record_card_menu)
        self._legal_party_property_record_card_action = QAction(
            QIcon(":/Asistente-LADM_COL/resources/images/tables.png"),
            QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Legal Party"),
            self._property_record_card_menu)

        self._property_record_card_menu.addAction(self._property_record_card_action)
        self._property_record_card_menu.addAction(self._market_research_property_record_card_action)
        self._property_record_card_menu.addAction(self._nuclear_family_property_record_card_action)
        self._property_record_card_menu.addSeparator()
        self._property_record_card_menu.addAction(self._natural_party_property_record_card_action)
        self._property_record_card_menu.addAction(self._legal_party_property_record_card_action)

        if len(self._menu.actions()) > 1:
            self._menu.insertMenu(self._menu.actions()[1], self._property_record_card_menu)
        else: # Just in case...
            self._menu.addMenu(self._property_record_card_menu)

        # Connections
        self._property_record_card_action.triggered.connect(self.show_wiz_property_record_card)
        self._market_research_property_record_card_action.triggered.connect(self.show_wiz_market_research_prc)
        self._nuclear_family_property_record_card_action.triggered.connect(self.show_wiz_nuclear_family_prc)
        self._natural_party_property_record_card_action.triggered.connect(self.show_wiz_natural_party_prc)
        self._legal_party_property_record_card_action.triggered.connect(self.show_wiz_legal_party_prc)

    def remove_property_record_card_menu(self):
        menu = self.iface.mainWindow().findChild(QMenu, PROPERTY_RECORD_CARD_MENU_OBJECTNAME)
        if menu is None:
            return # Nothing to remove...

        self._property_record_card_menu = None
        self._property_record_card_action = None
        self._market_research_property_record_card_action = None
        self._nuclear_family_property_record_card_action = None
        self._natural_party_property_record_card_action = None
        self._legal_party_property_record_card_action = None

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
        self._horizontal_property_main_parcel_valuation_action = QAction(
            QIcon(":/Asistente-LADM_COL/resources/images/tables.png"),
            QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Horizontal Property main Parcel"),
            self._valuation_menu)
        self._common_equipment_valuation_action = QAction(
            QIcon(":/Asistente-LADM_COL/resources/images/tables.png"),
            QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Common Equipment"),
            self._valuation_menu)
        self._building_valuation_action = QAction(
            QIcon(":/Asistente-LADM_COL/resources/images/tables.png"),
            QCoreApplication.translate("AsistenteLADMCOLPlugin", "Create Building"),
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
        self._valuation_menu.addAction(self._horizontal_property_main_parcel_valuation_action)
        self._valuation_menu.addAction(self._common_equipment_valuation_action)
        self._valuation_menu.addAction(self._building_valuation_action)
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
        self._horizontal_property_main_parcel_valuation_action.triggered.connect(
            self.show_wiz_horizontal_property_main_parcel_valuation)
        self._common_equipment_valuation_action.triggered.connect(self.show_wiz_common_equipment_valuation)
        self._building_valuation_action.triggered.connect(self.show_wiz_building_valuation)
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
        self._horizontal_property_main_parcel_valuation_action = None
        self._common_equipment_valuation_action = None
        self._building_valuation_action = None
        self._building_unit_valuation_action = None
        self._building_unit_qualification_valuation_action = None
        self._geoeconomic_zone_valuation_action = None
        self._physical_zone_valuation_action = None

        menu.deleteLater()

    def refresh_menus(self, db, ladm_col_db):
        """
        Depending on the models available in the DB, some menus should appear or
        disappear from the GUI.
        """
        if ladm_col_db:
            if db.property_record_card_model_exists():
                self.add_property_record_card_menu()
            else:
                self.remove_property_record_card_menu()

            if db.valuation_model_exists():
                self.add_valuation_menu()
            else:
                self.remove_valuation_menu()

            self.log.logMessage("Menus refreshed! Valuation: {}; Property Record Card: {}".format(
                    db.valuation_model_exists(),
                    db.property_record_card_model_exists()),
                PLUGIN_NAME,
                Qgis.Info)

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
        self.iface.messageBar().pushMessage("Asistente LADM_COL", msg, level, duration)

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

    def show_message_with_open_table_attributes_button(self, msg, button_text, level, layer, filter):
        widget = self.iface.messageBar().createMessage("Asistente LADM_COL", msg)
        button = QPushButton(widget)
        button.setText(button_text)
        button.pressed.connect(partial(self.open_table, layer, filter))
        widget.layout().addWidget(button)
        self.iface.messageBar().pushWidget(widget, level, 15)

    def show_message_to_open_about_dialog(self, msg):
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
            self.iface.messageBar().pushWidget(widget, Qgis.Info, 60)
        else:
            self.show_message(QCoreApplication.translate("AsistenteLADMCOLPlugin",
                                                         "Report dependency download is in progress..."),
                              Qgis.Info)

    def show_message_to_remove_report_dependency(self, msg):
        widget = self.iface.messageBar().createMessage("Asistente LADM_COL", msg)
        button = QPushButton(widget)
        button.setText(QCoreApplication.translate("AsistenteLADMCOLPlugin",
            "Remove dependency"))
        button.pressed.connect(self.remove_report_dependency)
        widget.layout().addWidget(button)
        self.iface.messageBar().pushWidget(widget, Qgis.Info, 60)

    def show_message_with_settings_button(self, msg, button_text, level):
        widget = self.iface.messageBar().createMessage("Asistente LADM_COL", msg)
        button = QPushButton(widget)
        button.setText(button_text)
        button.pressed.connect(self.show_settings)
        widget.layout().addWidget(button)
        self.iface.messageBar().pushWidget(widget, level, 25)

    def show_status_bar_message(self, msg, duration):
        self.iface.statusBarIface().showMessage(msg, duration)

    def load_layer(self, layer):
        self.qgis_utils.get_layer(self.get_db_connection(), layer[0], layer[1], load=True)

    def load_layers(self, layers):
        self.qgis_utils.get_layers(self.get_db_connection(), layers, True)

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
        dlg = LogQualityDialog(self.qgis_utils, self.quality)
        dlg.exec_()

    def show_log_excel_button(self, text):
        self.progressMessageBar = self.iface.messageBar().createMessage("Import from Excel",
            QCoreApplication.translate("DialogImportFromExcel",
                                       "Some errors were found while importing from the intermediate Excel file into LADM-COL!"))
        self.button = QPushButton(self.progressMessageBar)
        self.button.pressed.connect(self.show_log_excel_dialog)
        self.button.setText(QCoreApplication.translate("DialogImportFromExcel", "Show errors found"))
        self.progressMessageBar.layout().addWidget(self.button)
        self.iface.messageBar().pushWidget(self.progressMessageBar, Qgis.Warning)
        self.text = text

    def show_log_excel_dialog(self):
        dlg = LogExcelDialog(self.qgis_utils, self.text)
        dlg.exec_()


    def is_plugin_version_valid(self):
        plugin_found = 'QgisModelBaker' in qgis.utils.plugins
        if not plugin_found:
            return False
        current_version = get_plugin_metadata('QgisModelBaker', 'version')
        min_required_version = QGIS_MODEL_BAKER_MIN_REQUIRED_VERSION
        if current_version is None:
            return False

        current_version_splitted = current_version.split(".")
        if len(current_version_splitted) < 4: # We could need 4 places for custom QGIS Model Baker versions
            current_version_splitted = current_version_splitted + ['0','0','0','0']
            current_version_splitted = current_version_splitted[:4]

        min_required_version_splitted = min_required_version.split(".")
        if len(min_required_version_splitted) < 4:
            min_required_version_splitted = min_required_version_splitted + ['0','0','0','0']
            min_required_version_splitted = min_required_version_splitted[:4]

        self.log.logMessage("[QGIS Model Baker] Min required version: {}, current_version: {}".format(min_required_version_splitted, current_version_splitted), PLUGIN_NAME, Qgis.Info)

        if QGIS_MODEL_BAKER_EXACT_REQUIRED_VERSION:
            return min_required_version_splitted == current_version_splitted

        else: # Min version and subsequent versions should work
            for i in range(len(current_version_splitted)):
                if int(current_version_splitted[i]) < int(min_required_version_splitted[i]):
                    return False
                elif int(current_version_splitted[i]) > int(min_required_version_splitted[i]):
                    return True

        return True

    @_qgis_model_baker_required
    @_db_connection_required
    def call_explode_boundaries(self):
        self.qgis_utils.build_boundary(self.get_db_connection())

    @_qgis_model_baker_required
    @_db_connection_required
    def call_topological_editing(self):
        self.toolbar.enable_topological_editing(self.get_db_connection())

    @_qgis_model_baker_required
    @_db_connection_required
    def call_fill_topology_table_pointbfs(self):
        self.qgis_utils.fill_topology_table_pointbfs(self.get_db_connection())

    @_qgis_model_baker_required
    @_db_connection_required
    def call_fill_topology_tables_morebfs_less(self):
        self.qgis_utils.fill_topology_tables_morebfs_less(self.get_db_connection())

    @_qgis_model_baker_required
    @_db_connection_required
    @_activate_processing_plugin
    def call_fill_right_of_way_relations(self):
        self.qgis_utils.fill_right_of_way_relations(self.get_db_connection())

    @_qgis_model_baker_required
    @_db_connection_required
    def call_report_generation(self):
        self.report_generator.generate_report(self.get_db_connection(), self._report_action)

    @_qgis_model_baker_required
    @_db_connection_required
    @_activate_processing_plugin
    def call_import_from_intermediate_structure(self):
        self._dlg = DialogImportFromExcel(self.iface, self.get_db_connection(), self.qgis_utils)
        self._dlg.log_excel_show_message_emitted.connect(self.show_log_excel_button)
        self._dlg.exec_()

    def unload(self):
        # remove the plugin menu item and icon
        self._menu.deleteLater()
        self.iface.mainWindow().removeToolBar(self._ladm_col_toolbar)
        del self._ladm_col_toolbar
        del self._dock_widget_queries
        QgsApplication.processingRegistry().removeProvider(self.ladm_col_provider)

    def show_settings(self):
        self.qgis_utils.get_settings_dialog().set_action_type(EnumDbActionType.CONFIG)
        self.qgis_utils.get_settings_dialog().exec_()

    def show_plugin_manager(self):
        self.iface.actionManagePlugins().trigger()

    @_qgis_model_baker_required
    @_db_connection_required
    def load_layers_from_qgis_model_baker(self):
        dlg = DialogLoadLayers(self.iface, self.get_db_connection(), self.qgis_utils)
        dlg.exec_()

    @_db_connection_required
    def show_queries(self):
        if self._dock_widget_queries is None:
            self._dock_widget_queries = DockWidgetQueries(self.iface, self.get_db_connection(), self.qgis_utils, self.ladm_data)
            self.qgis_utils.db_connection_changed.connect(self._dock_widget_queries.update_db_connection)
            self.iface.addDockWidget(Qt.RightDockWidgetArea, self._dock_widget_queries)
        else:
            self._dock_widget_queries.toggleUserVisible()

    def get_db_connection(self):
        return self.qgis_utils.get_db_connection()

    @_qgis_model_baker_required
    def show_dlg_import_schema(self):
        from .gui.qgis_model_baker.dlg_import_schema import DialogImportSchema
        dlg = DialogImportSchema(self.iface, self.get_db_connection(), self.qgis_utils)
        dlg.models_have_changed.connect(self.refresh_menus)
        dlg.exec_()

    @_qgis_model_baker_required
    def show_dlg_import_data(self):
        from .gui.qgis_model_baker.dlg_import_data import DialogImportData
        dlg = DialogImportData(self.iface, self.get_db_connection(), self.qgis_utils)
        dlg.exec_()

    @_qgis_model_baker_required
    def show_dlg_export_data(self):
        from .gui.qgis_model_baker.dlg_export_data import DialogExportData
        dlg = DialogExportData(self.iface, self.get_db_connection(), self.qgis_utils)
        dlg.exec_()

    @_qgis_model_baker_required
    @_activate_processing_plugin
    def show_dlg_controlled_measurement(self):
        dlg = ControlledMeasurementDialog(self.qgis_utils)
        dlg.exec_()

    @_qgis_model_baker_required
    @_db_connection_required
    def show_wiz_point_cad(self):
        wiz = CreatePointsCadastreWizard(self.iface, self.get_db_connection(), self.qgis_utils)
        wiz.exec_()

    @_qgis_model_baker_required
    @_db_connection_required
    def show_wiz_boundaries_cad(self):
        wiz = CreateBoundariesCadastreWizard(self.iface, self.get_db_connection(), self.qgis_utils)
        self.exec_wizard(wiz)

    @_qgis_model_baker_required
    @_db_connection_required
    def show_wiz_plot_cad(self):
        wiz = CreatePlotCadastreWizard(self.iface, self.get_db_connection(), self.qgis_utils)
        self.exec_wizard(wiz)

    @_qgis_model_baker_required
    @_db_connection_required
    def show_wiz_building_cad(self):
        wiz = CreateBuildingCadastreWizard(self.iface, self.get_db_connection(), self.qgis_utils)
        self.exec_wizard(wiz)

    @_qgis_model_baker_required
    @_db_connection_required
    def show_wiz_building_unit_cad(self):
        wiz = CreateBuildingUnitCadastreWizard(self.iface, self.get_db_connection(), self.qgis_utils)
        self.exec_wizard(wiz)

    @_qgis_model_baker_required
    @_db_connection_required
    @_activate_processing_plugin
    def show_wiz_right_of_way_cad(self):
        wiz = CreateRightOfWayCadastreWizard(self.iface, self.get_db_connection(), self.qgis_utils)
        self.exec_wizard(wiz)

    @_qgis_model_baker_required
    @_db_connection_required
    def show_wiz_extaddress_cad(self):
        self.wiz_address = AssociateExtAddressWizard(self.iface, self.get_db_connection(), self.qgis_utils)
        self.exec_wizard(self.wiz_address)

    @_qgis_model_baker_required
    @_db_connection_required
    def show_wiz_parcel_cad(self):
        self._wiz_create_parcel = CreateParcelCadastreWizard(self.iface, self.get_db_connection(), self.qgis_utils)
        self.exec_wizard(self._wiz_create_parcel)

    @_qgis_model_baker_required
    @_db_connection_required
    def show_wiz_col_party_cad(self):
        wiz = CreateColPartyCadastreWizard(self.iface, self.get_db_connection(), self.qgis_utils)
        self.exec_wizard(wiz)

    @_qgis_model_baker_required
    @_db_connection_required
    def show_dlg_group_party(self):
        namespace_enabled = QSettings().value('Asistente-LADM_COL/automatic_values/namespace_enabled', True, bool)
        local_id_enabled = QSettings().value('Asistente-LADM_COL/automatic_values/local_id_enabled', True, bool)

        if not namespace_enabled or not local_id_enabled:
            self.show_message_with_settings_button(QCoreApplication.translate("CreateGroupPartyCadastre",
                                                       "First enable automatic values for both namespace and local_id fields before creating group parties. Click the button to open the settings dialog."),
                                                   QCoreApplication.translate("CreateGroupPartyCadastre", "Open Settings"),
                                                   Qgis.Info)
            return

        dlg = CreateGroupPartyCadastre(self.iface, self.get_db_connection(), self.qgis_utils)

        # Check if requied layers are available
        if dlg.is_enable_layers_wizard():
            # Load required data, it is necessary in the dlg
            dlg.load_parties_data()
            dlg.exec_()
        else:
            del dlg

    @_qgis_model_baker_required
    @_db_connection_required
    def show_wiz_right_rrr_cad(self):
        wiz = CreateRightCadastreWizard(self.iface, self.get_db_connection(), self.qgis_utils)
        self.exec_wizard(wiz)

    @_qgis_model_baker_required
    @_db_connection_required
    def show_wiz_responsibility_rrr_cad(self):
        wiz = CreateResponsibilityCadastreWizard(self.iface, self.get_db_connection(), self.qgis_utils)
        self.exec_wizard(wiz)

    @_qgis_model_baker_required
    @_db_connection_required
    def show_wiz_restriction_rrr_cad(self):
        wiz = CreateRestrictionCadastreWizard(self.iface, self.get_db_connection(), self.qgis_utils)
        self.exec_wizard(wiz)

    @_qgis_model_baker_required
    @_db_connection_required
    def show_wiz_administrative_source_cad(self):
        wiz = CreateAdministrativeSourceCadastreWizard(self.iface, self.get_db_connection(), self.qgis_utils)
        self.exec_wizard(wiz)

    @_qgis_model_baker_required
    @_db_connection_required
    def show_wiz_spatial_source_cad(self):
        wiz = CreateSpatialSourceCadastreWizard(self.iface, self.get_db_connection(), self.qgis_utils)
        self.exec_wizard(wiz)

    @_qgis_model_baker_required
    @_db_connection_required
    def upload_source_files(self):
        self.qgis_utils.upload_source_files(self.get_db_connection())

    @_qgis_model_baker_required
    @_db_connection_required
    @_activate_processing_plugin
    def show_dlg_quality(self):
        dlg = DialogQuality(self.get_db_connection(), self.qgis_utils, self.quality)
        dlg.exec_()

    @_qgis_model_baker_required
    @_db_connection_required
    def show_wiz_property_record_card(self):
        wiz = CreatePropertyRecordCardPRCWizard(self.iface, self.get_db_connection(), self.qgis_utils)
        self.exec_wizard(wiz)

    @_qgis_model_baker_required
    @_db_connection_required
    def show_wiz_market_research_prc(self):
        wiz = CreateMarketResearchPRCWizard(self.iface, self.get_db_connection(), self.qgis_utils)
        self.exec_wizard(wiz)

    @_qgis_model_baker_required
    @_db_connection_required
    def show_wiz_nuclear_family_prc(self):
        wiz = CreateNuclearFamilyPRCWizard(self.iface, self.get_db_connection(), self.qgis_utils)
        self.exec_wizard(wiz)

    @_qgis_model_baker_required
    @_db_connection_required
    def show_wiz_natural_party_prc(self):
        wiz = CreateNaturalPartyPRCWizard(self.iface, self.get_db_connection(), self.qgis_utils)
        self.exec_wizard(wiz)

    @_qgis_model_baker_required
    @_db_connection_required
    def show_wiz_legal_party_prc(self):
        wiz = CreateLegalPartyPRCWizard(self.iface, self.get_db_connection(), self.qgis_utils)
        self.exec_wizard(wiz)

    @_qgis_model_baker_required
    @_db_connection_required
    def show_wiz_parcel_valuation(self):
        wiz = CreateParcelValuationWizard(self.iface, self.get_db_connection(), self.qgis_utils)
        self.exec_wizard(wiz)

    @_qgis_model_baker_required
    @_db_connection_required
    def show_wiz_horizontal_property_main_parcel_valuation(self):
        wiz = CreateHorizontalPropertyValuationWizard(self.iface, self.get_db_connection(), self.qgis_utils)
        self.exec_wizard(wiz)

    @_qgis_model_baker_required
    @_db_connection_required
    def show_wiz_common_equipment_valuation(self):
        wiz = CreateCommonEquipmentValuationWizard(self.iface, self.get_db_connection(), self.qgis_utils)
        self.exec_wizard(wiz)

    @_qgis_model_baker_required
    @_db_connection_required
    def show_wiz_building_valuation(self):
        wiz = CreateBuildingValuationWizard(self.iface, self.get_db_connection(), self.qgis_utils)
        self.exec_wizard(wiz)

    @_qgis_model_baker_required
    @_db_connection_required
    def show_wiz_building_unit_valuation(self):
        wiz = CreateBuildingUnitValuationWizard(self.iface, self.get_db_connection(), self.qgis_utils)
        self.exec_wizard(wiz)

    @_qgis_model_baker_required
    @_db_connection_required
    def show_wiz_building_unit_qualification_valuation(self):
        wiz = CreateBuildingUnitQualificationValuationWizard(self.iface, self.get_db_connection(), self.qgis_utils)
        self.exec_wizard(wiz)

    @_qgis_model_baker_required
    @_db_connection_required
    def show_wiz_geoeconomic_zone_valuation(self):
        wiz = CreateGeoeconomicZoneValuationWizard(self.iface, self.get_db_connection(), self.qgis_utils)
        self.exec_wizard(wiz)

    @_qgis_model_baker_required
    @_db_connection_required
    def show_wiz_physical_zone_valuation_action(self):
        wiz = CreatePhysicalZoneValuationWizard(self.iface, self.get_db_connection(), self.qgis_utils)
        self.exec_wizard(wiz)

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
        # Check if requied layers are available
        if wiz.is_enable_layers_wizard():
            wiz.exec_()
        else:
            del wiz
