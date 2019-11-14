# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-09-10
        git sha              : :%H$
        copyright            : (C) 2017 by Germán Carrillo (BSF Swissphoto)
                               (C) 2019 by Leo Cardona (BSF Swissphoto)
        email                : gcarrillo@linuxmail.com
                               leo.cardona.p@gmail.com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
 """
from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsMapLayerProxyModel,
                       QgsWkbTypes)

from asistente_ladm_col.config.table_mapping_config import (Names,
                                                            VALUATION_GEOECONOMIC_ZONE_TABLE,
                                                            VALUATION_PHYSICAL_ZONE_TABLE,
                                                            AVALUOUNIDADCONSTRUCCION_TABLE,
                                                            VALUATION_BUILDING_UNIT_TABLE,
                                                            VALUATION_BUILDING_UNIT_QUALIFICATION_NO_CONVENTIONAL_TABLE,
                                                            VALUATION_BUILDING_UNIT_QUALIFICATION_CONVENTIONAL_TABLE)
from asistente_ladm_col.config.general_config import (LAYER,
                                                      WIZARD_NAME,
                                                      WIZARD_CLASS,
                                                      WIZARD_FEATURE_NAME,
                                                      WIZARD_UI,
                                                      WIZARD_HELP,
                                                      WIZARD_HELP_PAGES,
                                                      WIZARD_QSETTINGS,
                                                      WIZARD_QSETTINGS_LOAD_DATA_TYPE,
                                                      WIZARD_QSETTINGS_LOAD_CONVENTION_TYPE,
                                                      WIZARD_QSETTINGS_TYPE_PARCEL_SELECTED,
                                                      WIZARD_HELP1,
                                                      WIZARD_HELP2,
                                                      WIZARD_HELP3,
                                                      WIZARD_HELP4,
                                                      WIZARD_HELP5,
                                                      WIZARD_TYPE,
                                                      WIZARD_LAYERS,
                                                      WIZARD_EDITING_LAYER_NAME,
                                                      WIZARD_MAP_LAYER_PROXY_MODEL,
                                                      WIZARD_READ_ONLY_FIELDS,
                                                      WIZARD_CREATE_COL_PARTY_CADASTRAL,
                                                      WIZARD_CREATE_ADMINISTRATIVE_SOURCE_OPERATION,
                                                      WIZARD_CREATE_BOUNDARY_OPERATION,
                                                      WIZARD_CREATE_BUILDING_OPERATION,
                                                      WIZARD_CREATE_BUILDING_UNIT_OPERATION,
                                                      WIZARD_CREATE_RIGHT_OPERATION,
                                                      WIZARD_CREATE_RESTRICTION_OPERATION,
                                                      WIZARD_CREATE_SPATIAL_SOURCE_OPERATION,
                                                      WIZARD_CREATE_PARCEL_OPERATION,
                                                      WIZARD_CREATE_PLOT_OPERATION,
                                                      WIZARD_CREATE_EXT_ADDRESS_OPERATION,
                                                      WIZARD_CREATE_RIGHT_OF_WAY_OPERATION,
                                                      WIZARD_CREATE_GEOECONOMIC_ZONE_VALUATION,
                                                      WIZARD_CREATE_PHYSICAL_ZONE_VALUATION,
                                                      WIZARD_CREATE_BUILDING_UNIT_VALUATION,
                                                      WIZARD_CREATE_BUILDING_UNIT_QUALIFICATION_VALUATION,
                                                      WIZARD_TOOL_NAME)

from asistente_ladm_col.config.enums import WizardTypeEnum
from asistente_ladm_col.gui.wizards.operation.wiz_create_parcel_operation import CreateParcelOperationWizard
from asistente_ladm_col.gui.wizards.operation.wiz_create_rrr_operation import CreateRRROperationWizard
from asistente_ladm_col.config.help_strings import HelpStrings
from asistente_ladm_col.gui.wizards.operation.wiz_create_spatial_source_operation import CreateSpatialSourceOperationWizard
from asistente_ladm_col.gui.wizards.operation.wiz_create_ext_address_operation import CreateExtAddressOperationWizard
from asistente_ladm_col.gui.wizards.operation.wiz_create_plot_operation import CreatePlotOperationWizard
from asistente_ladm_col.gui.wizards.operation.wiz_create_right_of_way_operation import CreateRightOfWayOperationWizard
from asistente_ladm_col.gui.wizards.single_page_spatial_wizard_factory import SinglePageSpatialWizardFactory
from asistente_ladm_col.gui.wizards.single_page_wizard_factory import SinglePageWizardFactory
from asistente_ladm_col.gui.wizards.valuation.wiz_create_building_unit_qualification_valuation import CreateBuildingUnitQualificationValuationWizard
from asistente_ladm_col.gui.wizards.valuation.wiz_create_building_unit_valuation import CreateBuildingUnitValuationWizard

help_strings = HelpStrings()


class WizardConfig:

    def __init__(self):
        self.names = Names()

    def get_wizard_config(self, wizard_config_name):
        if wizard_config_name == WIZARD_CREATE_COL_PARTY_CADASTRAL:
            return {
                WIZARD_TYPE: WizardTypeEnum.SINGLE_PAGE_WIZARD_TYPE,
                WIZARD_NAME: "CreateColPartyOperationWizard",
                WIZARD_CLASS: SinglePageWizardFactory,
                WIZARD_FEATURE_NAME: QCoreApplication.translate("CreateColPartyOperationWizard", "party"),
                WIZARD_TOOL_NAME: QCoreApplication.translate("CreateColPartyOperationWizard", "Create party"),
                WIZARD_HELP: "col_party",
                WIZARD_UI: "wizards/operation/wiz_create_col_party_operation.ui",
                WIZARD_QSETTINGS: {
                    WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM_COL/wizards/col_party_load_data_type"
                },
                WIZARD_HELP_PAGES: {
                    WIZARD_HELP1: help_strings.WIZ_CREATE_COL_PARTY_OPERATION_PAGE_1_OPTION_FORM,
                    WIZARD_HELP2: ""
                },
                WIZARD_LAYERS: {
                    self.names.OP_PARTY_T: {'name': self.names.OP_PARTY_T, 'geometry': None, LAYER: None}
                },
                WIZARD_EDITING_LAYER_NAME: self.names.OP_PARTY_T,
                WIZARD_READ_ONLY_FIELDS: [self.names.COL_PARTY_T_NAME_F],
                WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.NoGeometry
            }
        elif wizard_config_name == WIZARD_CREATE_ADMINISTRATIVE_SOURCE_OPERATION:
            return {
                WIZARD_TYPE: WizardTypeEnum.SINGLE_PAGE_WIZARD_TYPE,
                WIZARD_NAME: "CreateAdministrativeSourceOperationWizard",
                WIZARD_CLASS: SinglePageWizardFactory,
                WIZARD_FEATURE_NAME: QCoreApplication.translate("CreateAdministrativeSourceOperationWizard",
                                                                        "administrative source"),
                WIZARD_TOOL_NAME: QCoreApplication.translate("CreateAdministrativeSourceOperationWizard",
                                                                        "Create administrative source"),
                WIZARD_HELP: "create_admin_source",
                WIZARD_UI: "wizards/operation/wiz_create_administrative_source_operation.ui",
                WIZARD_QSETTINGS: {
                    WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM_COL/wizards/administrative_source_load_data_type"
                },
                WIZARD_HELP_PAGES: {
                    WIZARD_HELP1: help_strings.WIZ_CREATE_ADMINISTRATIVE_SOURCE_PAGE_1_OPTION_FORM,
                    WIZARD_HELP2: ""
                },
                WIZARD_LAYERS: {
                    self.names.OP_ADMINISTRATIVE_SOURCE_T: {'name': self.names.OP_ADMINISTRATIVE_SOURCE_T, 'geometry': None, LAYER: None},
                    self.names.EXT_ARCHIVE_S: {'name': self.names.EXT_ARCHIVE_S, 'geometry': None, LAYER: None}
                },
                WIZARD_EDITING_LAYER_NAME: self.names.OP_ADMINISTRATIVE_SOURCE_T,
                WIZARD_READ_ONLY_FIELDS: [],
                WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.NoGeometry
            }
        elif wizard_config_name == WIZARD_CREATE_BOUNDARY_OPERATION:
            return {
                WIZARD_TYPE: WizardTypeEnum.SINGLE_PAGE_SPATIAL_WIZARD_TYPE,
                WIZARD_NAME: "CreateBoundaryOperationWizard",
                WIZARD_CLASS: SinglePageSpatialWizardFactory,
                WIZARD_FEATURE_NAME: QCoreApplication.translate("CreateBoundaryOperationWizard", "boundary"),
                WIZARD_TOOL_NAME: QCoreApplication.translate("CreateBoundaryOperationWizard", "Create boundary"),
                WIZARD_HELP: "create_boundaries",
                WIZARD_UI: "wizards/operation/wiz_create_boundaries_operation.ui",
                WIZARD_QSETTINGS: {
                    WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM_COL/wizards/boundary_load_data_type"
                },
                WIZARD_HELP_PAGES: {
                    WIZARD_HELP1: help_strings.WIZ_DEFINE_BOUNDARIES_OPERATION_PAGE_1_OPTION_DIGITIZE,
                    WIZARD_HELP2: ""
                },
                WIZARD_LAYERS: {
                    self.names.OP_BOUNDARY_T: {'name': self.names.OP_BOUNDARY_T, 'geometry': QgsWkbTypes.LineGeometry, LAYER: None},
                    self.names.OP_BOUNDARY_POINT_T: {'name': self.names.OP_BOUNDARY_POINT_T, 'geometry': QgsWkbTypes.PointGeometry, LAYER: None}
                },
                WIZARD_EDITING_LAYER_NAME: self.names.OP_BOUNDARY_T,
                WIZARD_READ_ONLY_FIELDS: [],
                WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.LineLayer
            }
        elif wizard_config_name == WIZARD_CREATE_BUILDING_OPERATION:
            return {
                WIZARD_TYPE: WizardTypeEnum.SINGLE_PAGE_SPATIAL_WIZARD_TYPE,
                WIZARD_NAME: "CreateBuildingOperationWizard",
                WIZARD_CLASS: SinglePageSpatialWizardFactory,
                WIZARD_FEATURE_NAME: QCoreApplication.translate("CreateBuildingOperationWizard", "building"),
                WIZARD_TOOL_NAME: QCoreApplication.translate("CreateBuildingOperationWizard", "Create building"),
                WIZARD_HELP: "create_building",
                WIZARD_UI: "wizards/operation/wiz_create_building_operation.ui",
                WIZARD_QSETTINGS: {
                    WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM_COL/wizards/building_load_data_type"
                },
                WIZARD_HELP_PAGES: {
                    WIZARD_HELP1: help_strings.WIZ_CREATE_BUILDING_OPERATION_PAGE_1_OPTION_POINTS,
                    WIZARD_HELP2: ""
                },
                WIZARD_LAYERS: {
                    self.names.OP_BUILDING_T: {'name': self.names.OP_BUILDING_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
                    self.names.OP_SURVEY_POINT_T: {'name': self.names.OP_SURVEY_POINT_T, 'geometry': None, LAYER: None}
                },
                WIZARD_EDITING_LAYER_NAME: self.names.OP_BUILDING_T,
                WIZARD_READ_ONLY_FIELDS: [],
                WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.PolygonLayer
            }
        elif wizard_config_name == WIZARD_CREATE_BUILDING_UNIT_OPERATION:
            return {
                WIZARD_TYPE: WizardTypeEnum.SINGLE_PAGE_SPATIAL_WIZARD_TYPE,
                WIZARD_NAME: "CreateBuildingUnitOperationWizard",
                WIZARD_CLASS: SinglePageSpatialWizardFactory,
                WIZARD_FEATURE_NAME: QCoreApplication.translate("CreateBuildingUnitOperationWizard", "building unit"),
                WIZARD_TOOL_NAME: QCoreApplication.translate("CreateBuildingUnitOperationWizard", "Create building unit"),
                WIZARD_HELP: "create_building_unit",
                WIZARD_UI: "wizards/operation/wiz_create_building_unit_operation.ui",
                WIZARD_QSETTINGS: {
                    WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM_COL/wizards/building_unit_load_data_type"
                },
                WIZARD_HELP_PAGES: {
                    WIZARD_HELP1: help_strings.WIZ_CREATE_BUILDING_UNIT_OPERATION_PAGE_1_OPTION_POINTS,
                    WIZARD_HELP2: ""
                },
                WIZARD_LAYERS: {
                    self.names.OP_BUILDING_UNIT_T: {'name': self.names.OP_BUILDING_UNIT_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
                    self.names.OP_BUILDING_T: {'name': self.names.OP_BUILDING_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
                    self.names.OP_SURVEY_POINT_T: {'name': self.names.OP_SURVEY_POINT_T, 'geometry': None, LAYER: None}
                },
                WIZARD_EDITING_LAYER_NAME: self.names.OP_BUILDING_UNIT_T,
                WIZARD_READ_ONLY_FIELDS: [],
                WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.PolygonLayer
            }
        elif wizard_config_name == WIZARD_CREATE_RIGHT_OPERATION:
            return {
                WIZARD_TYPE: WizardTypeEnum.MULTI_PAGE_WIZARD_TYPE,
                WIZARD_NAME: "CreateRightOperationWizard",
                WIZARD_CLASS: CreateRRROperationWizard,
                WIZARD_FEATURE_NAME: QCoreApplication.translate("CreateRightOperationWizard", "right"),
                WIZARD_TOOL_NAME: QCoreApplication.translate("CreateRightOperationWizard", "Create right"),
                WIZARD_HELP: "create_right",
                WIZARD_UI: "wizards/operation/wiz_create_right_operation.ui",
                WIZARD_QSETTINGS: {
                    WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM_COL/wizards/right_load_data_type"
                },
                WIZARD_HELP_PAGES: {
                    WIZARD_HELP1: help_strings.WIZ_CREATE_RIGHT_OPERATION_PAGE_1_OPTION_FORM,
                    WIZARD_HELP2: help_strings.WIZ_CREATE_RIGHT_OPERATION_PAGE_2
                },
                WIZARD_LAYERS: {
                    self.names.OP_RIGHT_T: {'name': self.names.OP_RIGHT_T, 'geometry': None, LAYER: None},
                    self.names.OP_ADMINISTRATIVE_SOURCE_T: {'name': self.names.OP_ADMINISTRATIVE_SOURCE_T, 'geometry': None, LAYER: None},
                    self.names.COL_RRR_SOURCE_T: {'name': self.names.COL_RRR_SOURCE_T, 'geometry': None, LAYER: None}
                },
                WIZARD_EDITING_LAYER_NAME: self.names.OP_RIGHT_T,
                WIZARD_READ_ONLY_FIELDS: [],
                WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.NoGeometry
            }
        elif wizard_config_name == WIZARD_CREATE_RESTRICTION_OPERATION:
            return {
                WIZARD_TYPE: WizardTypeEnum.MULTI_PAGE_WIZARD_TYPE,
                WIZARD_NAME: "CreateRestrictionOperationWizard",
                WIZARD_CLASS: CreateRRROperationWizard,
                WIZARD_FEATURE_NAME: QCoreApplication.translate("CreateRestrictionOperationWizard", "restriction"),
                WIZARD_TOOL_NAME: QCoreApplication.translate("CreateRestrictionOperationWizard", "Create restriction"),
                WIZARD_HELP: "create_restriction",
                WIZARD_UI: "wizards/operation/wiz_create_restriction_operation.ui",
                WIZARD_QSETTINGS: {
                    WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM_COL/wizards/restriction_load_data_type"
                },
                WIZARD_HELP_PAGES: {
                    WIZARD_HELP1: help_strings.WIZ_CREATE_RESTRICTION_OPERATION_PAGE_1_OPTION_FORM,
                    WIZARD_HELP2: help_strings.WIZ_CREATE_RESTRICTION_OPERATION_PAGE_2
                },
                WIZARD_LAYERS: {
                    self.names.OP_RESTRICTION_T: {'name': self.names.OP_RESTRICTION_T, 'geometry': None, LAYER: None},
                    self.names.OP_ADMINISTRATIVE_SOURCE_T: {'name': self.names.OP_ADMINISTRATIVE_SOURCE_T, 'geometry': None, LAYER: None},
                    self.names.COL_RRR_SOURCE_T: {'name': self.names.COL_RRR_SOURCE_T, 'geometry': None, LAYER: None}
                },
                WIZARD_EDITING_LAYER_NAME: self.names.OP_RESTRICTION_T,
                WIZARD_READ_ONLY_FIELDS: [],
                WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.NoGeometry
            }
        elif wizard_config_name == WIZARD_CREATE_SPATIAL_SOURCE_OPERATION:
            return {
                WIZARD_TYPE: WizardTypeEnum.MULTI_PAGE_WIZARD_TYPE,
                WIZARD_NAME: "CreateSpatialSourceOperationWizard",
                WIZARD_CLASS: CreateSpatialSourceOperationWizard,
                WIZARD_FEATURE_NAME: QCoreApplication.translate("CreateSpatialSourceOperationWizard",
                                                                        "spatial source"),
                WIZARD_TOOL_NAME: QCoreApplication.translate("CreateSpatialSourceOperationWizard",
                                                                                "Create spatial source"),
                WIZARD_HELP: "create_spatial_source",
                WIZARD_UI: "wizards/operation/wiz_create_spatial_source_operation.ui",
                WIZARD_QSETTINGS: {
                    WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM_COL/wizards/spatial_source_load_data_type"
                },
                WIZARD_HELP_PAGES: {
                    WIZARD_HELP1: help_strings.WIZ_CREATE_SPATIAL_SOURCE_OPERATION_PAGE_1_OPTION_FORM,
                    WIZARD_HELP2: help_strings.WIZ_CREATE_SPATIAL_SOURCE_OPERATION_PAGE_2
                },
                WIZARD_LAYERS: {
                    self.names.OP_SPATIAL_SOURCE_T: {'name': self.names.OP_SPATIAL_SOURCE_T, 'geometry': None, LAYER: None},
                    self.names.EXT_ARCHIVE_S: {'name': self.names.EXT_ARCHIVE_S, 'geometry': None, LAYER: None},
                    self.names.OP_PLOT_T: {'name': self.names.OP_PLOT_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
                    self.names.COL_UE_SOURCE_T: {'name': self.names.COL_UE_SOURCE_T, 'geometry': None, LAYER: None},
                    self.names.OP_BOUNDARY_T: {'name': self.names.OP_BOUNDARY_T, 'geometry': None, LAYER: None},
                    self.names.COL_CCL_SOURCE_T: {'name': self.names.COL_CCL_SOURCE_T, 'geometry': None, LAYER: None},
                    self.names.COL_POINT_SOURCE_T: {'name': self.names.COL_POINT_SOURCE_T, 'geometry': None, LAYER: None},
                    self.names.OP_BOUNDARY_POINT_T: {'name': self.names.OP_BOUNDARY_POINT_T, 'geometry': None, LAYER: None},
                    self.names.OP_SURVEY_POINT_T: {'name': self.names.OP_SURVEY_POINT_T, 'geometry': None, LAYER: None},
                    self.names.OP_CONTROL_POINT_T: {'name': self.names.OP_CONTROL_POINT_T, 'geometry': None, LAYER: None}
                },
                WIZARD_EDITING_LAYER_NAME: self.names.OP_SPATIAL_SOURCE_T,
                WIZARD_READ_ONLY_FIELDS: [],
                WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.NoGeometry
            }
        elif wizard_config_name == WIZARD_CREATE_PARCEL_OPERATION:
            return {
                WIZARD_TYPE: WizardTypeEnum.MULTI_PAGE_WIZARD_TYPE,
                WIZARD_NAME: "CreateParcelOperationWizard",
                WIZARD_CLASS: CreateParcelOperationWizard,
                WIZARD_FEATURE_NAME: QCoreApplication.translate("CreateParcelOperationWizard", "parcel"),
                WIZARD_TOOL_NAME: QCoreApplication.translate("CreateParcelOperationWizard", "Create parcel"),
                WIZARD_HELP: "create_parcel",
                WIZARD_UI: "wizards/operation/wiz_create_parcel_operation.ui",
                WIZARD_QSETTINGS: {
                    WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM_COL/wizards/parcel_load_data_type",
                    WIZARD_QSETTINGS_TYPE_PARCEL_SELECTED: "Asistente-LADM_COL/wizards/type_of_parcel_selected"
                },
                WIZARD_HELP_PAGES: {
                    WIZARD_HELP1: help_strings.WIZ_CREATE_PARCEL_OPERATION_PAGE_1_OPTION_EXISTING_PLOT,
                    WIZARD_HELP2: help_strings.WIZ_CREATE_PARCEL_OPERATION_PAGE_2
                },
                WIZARD_LAYERS: {
                    self.names.OP_PLOT_T: {'name': self.names.OP_PLOT_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
                    self.names.OP_PARCEL_T: {'name': self.names.OP_PARCEL_T, 'geometry': None, LAYER: None},
                    self.names.OP_BUILDING_T: {'name': self.names.OP_BUILDING_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
                    self.names.OP_BUILDING_UNIT_T: {'name': self.names.OP_BUILDING_UNIT_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
                    self.names.COL_UE_BAUNIT_T: {'name': self.names.COL_UE_BAUNIT_T, 'geometry': None, LAYER: None},
                    self.names.OP_PARCEL_TYPE_D: {'name': self.names.OP_PARCEL_TYPE_D, 'geometry': None, LAYER: None}
                },
                WIZARD_EDITING_LAYER_NAME: self.names.OP_PARCEL_T,
                WIZARD_READ_ONLY_FIELDS: [self.names.OP_PARCEL_T_PARCEL_TYPE_F],
                WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.NoGeometry
            }
        elif wizard_config_name == WIZARD_CREATE_PLOT_OPERATION:
            return {
                WIZARD_TYPE: WizardTypeEnum.MULTI_PAGE_WIZARD_TYPE,
                WIZARD_NAME: "CreatePlotOperationWizard",
                WIZARD_CLASS: CreatePlotOperationWizard,
                WIZARD_FEATURE_NAME: QCoreApplication.translate("CreatePlotOperationWizard", "plot"),
                WIZARD_TOOL_NAME: QCoreApplication.translate("CreatePlotOperationWizard", "Create plot"),
                WIZARD_HELP: "create_plot",
                WIZARD_UI: "wizards/operation/wiz_create_plot_operation.ui",
                WIZARD_QSETTINGS: {
                    WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM_COL/wizards/plot_load_data_type"
                },
                WIZARD_HELP_PAGES: {
                    WIZARD_HELP1: help_strings.WIZ_CREATE_PLOT_OPERATION_PAGE_1_OPTION_BOUNDARIES,
                    WIZARD_HELP2: help_strings.WIZ_CREATE_PLOT_OPERATION_PAGE_2
                },
                WIZARD_LAYERS: {
                    self.names.OP_PLOT_T: {'name': self.names.OP_PLOT_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
                    self.names.OP_BOUNDARY_T: {'name': self.names.OP_BOUNDARY_T, 'geometry': None, LAYER: None}
                },
                WIZARD_EDITING_LAYER_NAME: self.names.OP_PLOT_T,
                WIZARD_READ_ONLY_FIELDS: [],
                WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.PolygonLayer
            }
        elif wizard_config_name == WIZARD_CREATE_EXT_ADDRESS_OPERATION:
            return {
                WIZARD_TYPE: WizardTypeEnum.MULTI_PAGE_SPATIAL_WIZARD_TYPE,
                WIZARD_NAME: "CreateExtAddressOperationWizard",
                WIZARD_CLASS: CreateExtAddressOperationWizard,
                WIZARD_FEATURE_NAME: QCoreApplication.translate("CreateExtAddressOperationWizard", "ext address"),
                WIZARD_TOOL_NAME: QCoreApplication.translate("CreateExtAddressOperationWizard", "Create ext address"),
                WIZARD_HELP: "associate_ext_address",
                WIZARD_UI: "wizards/operation/wiz_associate_extaddress_operation.ui",
                WIZARD_QSETTINGS: {
                    WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM_COL/wizards/ext_address_load_data_type"
                },
                WIZARD_HELP_PAGES: {
                    WIZARD_HELP1: help_strings.WIZ_ASSOCIATE_EXTADDRESS_OPERATION_PAGE_2_OPTION_1,
                    WIZARD_HELP2: help_strings.WIZ_ASSOCIATE_EXTADDRESS_OPERATION_PAGE_2_OPTION_2,
                    WIZARD_HELP3: help_strings.WIZ_ASSOCIATE_EXTADDRESS_OPERATION_PAGE_2_OPTION_3
                },
                WIZARD_LAYERS: {
                    self.names.EXT_ADDRESS_S: {'name': self.names.EXT_ADDRESS_S, 'geometry': QgsWkbTypes.PointGeometry, LAYER: None},
                    self.names.OP_PLOT_T: {'name': self.names.OP_PLOT_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
                    self.names.OP_BUILDING_T: {'name': self.names.OP_BUILDING_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
                    self.names.OP_BUILDING_UNIT_T: {'name': self.names.OP_BUILDING_UNIT_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None}
                },
                WIZARD_EDITING_LAYER_NAME: self.names.EXT_ADDRESS_S,
                WIZARD_READ_ONLY_FIELDS: [],
                WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.PointLayer
            }
        elif wizard_config_name == WIZARD_CREATE_RIGHT_OF_WAY_OPERATION:
            return {
                WIZARD_TYPE: WizardTypeEnum.SINGLE_PAGE_SPATIAL_WIZARD_TYPE,
                WIZARD_NAME: "CreateRightOfWayOperationWizard",
                WIZARD_CLASS: CreateRightOfWayOperationWizard,
                WIZARD_FEATURE_NAME: QCoreApplication.translate("CreateRightOfWayOperationWizard", "right of way"),
                WIZARD_TOOL_NAME: QCoreApplication.translate("CreateRightOfWayOperationWizard", "Create right of way"),
                WIZARD_HELP: "create_right_of_way",
                WIZARD_UI: "wizards/operation/wiz_create_right_of_way_operation.ui",
                WIZARD_QSETTINGS: {
                    WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM_COL/wizards/right_of_way_load_data_type"
                },
                WIZARD_HELP_PAGES: {
                    WIZARD_HELP1: help_strings.WIZ_CREATE_RIGHT_OF_WAY_OPERATION_PAGE_1_OPTION_POINTS,
                    WIZARD_HELP2: help_strings.WIZ_CREATE_RIGHT_OF_WAY_OPERATION_PAGE_1_OPTION2_POINTS,
                    WIZARD_HELP3: help_strings.WIZ_ASSOCIATE_EXTADDRESS_OPERATION_PAGE_2_OPTION_2,
                    WIZARD_HELP4: help_strings.WIZ_ASSOCIATE_EXTADDRESS_OPERATION_PAGE_2_OPTION_3
                },
                WIZARD_LAYERS: {
                    self.names.OP_RIGHT_OF_WAY_T: {'name': self.names.OP_RIGHT_OF_WAY_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
                    self.names.OP_PLOT_T: {'name': self.names.OP_PLOT_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
                    self.names.OP_SURVEY_POINT_T: {'name': self.names.OP_SURVEY_POINT_T, 'geometry': None, LAYER: None}
                },
                WIZARD_EDITING_LAYER_NAME: self.names.OP_RIGHT_OF_WAY_T,
                WIZARD_READ_ONLY_FIELDS: [],
                WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.PolygonLayer
            }
        elif wizard_config_name == WIZARD_CREATE_GEOECONOMIC_ZONE_VALUATION:
            return {
                WIZARD_TYPE: WizardTypeEnum.SINGLE_PAGE_SPATIAL_WIZARD_TYPE,
                WIZARD_NAME: "CreateGeoeconomicZoneValuationWizard",
                WIZARD_CLASS: SinglePageSpatialWizardFactory,
                WIZARD_FEATURE_NAME: QCoreApplication.translate("CreateGeoeconomicZoneValuationWizard",
                                                                        "geoeconomic zone"),
                WIZARD_TOOL_NAME: QCoreApplication.translate("CreateGeoeconomicZoneValuationWizard",
                                                                        "Create geoeconomic zone"),
                WIZARD_HELP: "create_geoeconomic_zone_valuation",
                WIZARD_UI: "wizards/valuation/wiz_create_geoeconomic_zone_valuation.ui",
                WIZARD_QSETTINGS: {
                    WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM_COL/wizards/geoeconomic_zone_valuation_load_data_type"
                },
                WIZARD_HELP_PAGES: {
                    WIZARD_HELP1: help_strings.WIZ_CREATE_GEOECONOMIC_ZONE_VALUATION_PAGE_1_OPTION_FORM,
                    WIZARD_HELP2: ""
                },
                WIZARD_LAYERS: {
                    VALUATION_GEOECONOMIC_ZONE_TABLE: {'name': VALUATION_GEOECONOMIC_ZONE_TABLE, 'geometry': None, LAYER: None}
                },
                WIZARD_EDITING_LAYER_NAME: VALUATION_GEOECONOMIC_ZONE_TABLE,
                WIZARD_READ_ONLY_FIELDS: [],
                WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.PolygonLayer
            }
        elif wizard_config_name == WIZARD_CREATE_PHYSICAL_ZONE_VALUATION:
            return {
                WIZARD_TYPE: WizardTypeEnum.SINGLE_PAGE_SPATIAL_WIZARD_TYPE,
                WIZARD_NAME: "CreatePhysicalZoneValuationWizard",
                WIZARD_CLASS: SinglePageSpatialWizardFactory,
                WIZARD_FEATURE_NAME: QCoreApplication.translate("CreatePhysicalZoneValuationWizard", "physical zone"),
                WIZARD_TOOL_NAME: QCoreApplication.translate("CreatePhysicalZoneValuationWizard", "Create physical zone"),
                WIZARD_HELP: "create_physical_zone_valuation",
                WIZARD_UI: "wizards/valuation/wiz_create_physical_zone_valuation.ui",
                WIZARD_QSETTINGS: {
                    WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM_COL/wizards/physical_zone_valuation_load_data_type"
                },
                WIZARD_HELP_PAGES: {
                    WIZARD_HELP1: help_strings.WIZ_CREATE_PHYSICAL_ZONE_VALUATION_PAGE_1_OPTION_FORM,
                    WIZARD_HELP2: ""
                },
                WIZARD_LAYERS: {
                    VALUATION_PHYSICAL_ZONE_TABLE: {'name': VALUATION_PHYSICAL_ZONE_TABLE, 'geometry': None, LAYER: None}
                },
                WIZARD_EDITING_LAYER_NAME: VALUATION_PHYSICAL_ZONE_TABLE,
                WIZARD_READ_ONLY_FIELDS: [],
                WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.PolygonLayer
            }
        elif wizard_config_name == WIZARD_CREATE_BUILDING_UNIT_VALUATION:
            return {
                WIZARD_TYPE: WizardTypeEnum.MULTI_PAGE_WIZARD_TYPE,
                WIZARD_NAME: "CreateBuildingUnitValuationWizard",
                WIZARD_CLASS: CreateBuildingUnitValuationWizard,
                WIZARD_FEATURE_NAME: QCoreApplication.translate("CreateBuildingUnitValuationWizard",
                                                                        "building unit valuation"),
                WIZARD_TOOL_NAME: QCoreApplication.translate("CreateBuildingUnitValuationWizard",
                                                                        "Create building unit valuation"),
                WIZARD_HELP: "create_building_unit_valuation",
                WIZARD_UI: "wizards/valuation/wiz_create_building_unit_valuation.ui",
                WIZARD_QSETTINGS: {
                    WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM_COL/wizards/valuation_building_unit_load_data_type"
                },
                WIZARD_HELP_PAGES: {
                    WIZARD_HELP1: help_strings.WIZ_CREATE_BUILDING_UNIT_VALUATION_PAGE_1_OPTION_FORM,
                    WIZARD_HELP2: help_strings.WIZ_CREATE_BUILDING_UNIT_VALUATION_PAGE_2
                },
                WIZARD_LAYERS: {
                    VALUATION_BUILDING_UNIT_TABLE: {'name': VALUATION_BUILDING_UNIT_TABLE, 'geometry': None, LAYER: None},
                    self.names.OP_BUILDING_UNIT_T: {'name': self.names.OP_BUILDING_UNIT_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
                    AVALUOUNIDADCONSTRUCCION_TABLE: {'name': AVALUOUNIDADCONSTRUCCION_TABLE, 'geometry': None, LAYER: None}
                },
                WIZARD_EDITING_LAYER_NAME: VALUATION_BUILDING_UNIT_TABLE,
                WIZARD_READ_ONLY_FIELDS: [],
                WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.NoGeometry
            }
        elif wizard_config_name == WIZARD_CREATE_BUILDING_UNIT_QUALIFICATION_VALUATION:
            return {
                WIZARD_TYPE: WizardTypeEnum.MULTI_PAGE_WIZARD_TYPE,
                WIZARD_NAME: "CreateBuildingUnitQualificationValuationWizard",
                WIZARD_CLASS: CreateBuildingUnitQualificationValuationWizard,
                WIZARD_FEATURE_NAME: QCoreApplication.translate("CreateBuildingUnitQualificationValuationWizard",
                                                                        "building unit qualification valuation"),
                WIZARD_TOOL_NAME: QCoreApplication.translate("CreateBuildingUnitQualificationValuationWizard",
                                                                        "Create building unit qualification valuation"),
                WIZARD_HELP: "create_building_unit_qualification_valuation_conventional",
                WIZARD_UI: "wizards/valuation/wiz_create_building_unit_qualification_valuation.ui",
                WIZARD_QSETTINGS: {
                    WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM_COL/wizards/building_unit_qualification_load_data_type",
                    WIZARD_QSETTINGS_LOAD_CONVENTION_TYPE: "Asistente-LADM_COL/wizards/building_unit_qualification_load_convention_type"
                },
                WIZARD_HELP_PAGES: {
                    WIZARD_HELP1: help_strings.WIZ_ADD_POINTS_OPERATION_PAGE_2_OPTION_CSV,
                    WIZARD_HELP2: help_strings.WIZ_USING_FORM_BUILDING_UNIT_QUALIFICATION_PAGE_2_OPTION,
                    WIZARD_HELP3: help_strings.WIZ_USING_FORM_BUILDING_UNIT_NO_QUALIFICATION_PAGE_2_OPTION,
                    WIZARD_HELP4: help_strings.WIZ_CREATE_BUILDING_UNIT_QUALIFICATION_CONVENTIONAL_VALUATION_PAGE_1_OPTION_FORM,
                    WIZARD_HELP5: help_strings.WIZ_CREATE_BUILDING_UNIT_QUALIFICATION_NO_CONVENTIONAL_VALUATION_PAGE_1_OPTION_FORM
                },
                WIZARD_LAYERS: {
                    VALUATION_BUILDING_UNIT_QUALIFICATION_NO_CONVENTIONAL_TABLE: {
                        'name': VALUATION_BUILDING_UNIT_QUALIFICATION_NO_CONVENTIONAL_TABLE, 'geometry': None, LAYER: None},
                    VALUATION_BUILDING_UNIT_QUALIFICATION_CONVENTIONAL_TABLE: {
                        'name': VALUATION_BUILDING_UNIT_QUALIFICATION_CONVENTIONAL_TABLE, 'geometry': None, LAYER: None}
                },
                WIZARD_EDITING_LAYER_NAME: VALUATION_BUILDING_UNIT_QUALIFICATION_CONVENTIONAL_TABLE,
                WIZARD_READ_ONLY_FIELDS: [],
                WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.NoGeometry
            }
