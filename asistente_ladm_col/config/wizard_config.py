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

from asistente_ladm_col.config.table_mapping_config import (COL_PARTY_TABLE,
                                                            BUILDING_TABLE,
                                                            PARCEL_TABLE,
                                                            PARCEL_TYPE_FIELD,
                                                            UEBAUNIT_TABLE,
                                                            BUILDING_UNIT_TABLE,
                                                            RIGHT_OF_WAY_TABLE,
                                                            SURVEY_POINT_TABLE,
                                                            ADMINISTRATIVE_SOURCE_TABLE,
                                                            RIGHT_TABLE,
                                                            RESTRICTION_TABLE,
                                                            RRR_SOURCE_RELATION_TABLE,
                                                            BOUNDARY_TABLE,
                                                            BOUNDARY_POINT_TABLE,
                                                            EXTADDRESS_TABLE,
                                                            EXTFILE_TABLE,
                                                            SPATIAL_SOURCE_TABLE,
                                                            PLOT_TABLE,
                                                            UESOURCE_TABLE,
                                                            CCLSOURCE_TABLE,
                                                            POINTSOURCE_TABLE,
                                                            CONTROL_POINT_TABLE,
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
                                                      WIZARD_TOOL_NAME)

from asistente_ladm_col.config.enums import WizardTypeEnum
from asistente_ladm_col.gui.wizards.cadastre.wiz_create_parcel_cadastre import CreateParcelCadastreWizard
from asistente_ladm_col.gui.wizards.cadastre.wiz_create_rrr_cadastre import CreateRRRCadastreWizard
from asistente_ladm_col.config.help_strings import HelpStrings
from asistente_ladm_col.gui.wizards.cadastre.wiz_create_spatial_source_cadastre import CreateSpatialSourceCadastreWizard
from asistente_ladm_col.gui.wizards.cadastre.wiz_create_ext_address_cadastre import CreateExtAddressCadastreWizard
from asistente_ladm_col.gui.wizards.cadastre.wiz_create_plot_cadastre import CreatePlotCadastreWizard
from asistente_ladm_col.gui.wizards.cadastre.wiz_create_right_of_way_cadastre import CreateRightOfWayCadastreWizard
from asistente_ladm_col.gui.wizards.single_page_spatial_wizard_factory import SinglePageSpatialWizardFactory
from asistente_ladm_col.gui.wizards.single_page_wizard_factory import SinglePageWizardFactory
from asistente_ladm_col.gui.wizards.valuation.wiz_create_building_unit_qualification_valuation import CreateBuildingUnitQualificationValuationWizard
from asistente_ladm_col.gui.wizards.valuation.wiz_create_building_unit_valuation import CreateBuildingUnitValuationWizard

help_strings = HelpStrings()


WIZARDS_SETTINGS = {
    # CADASTRAL MODEL
    WIZARD_CREATE_COL_PARTY_CADASTRAL: {
        WIZARD_TYPE: WizardTypeEnum.SINGLE_PAGE_WIZARD_TYPE,
        WIZARD_NAME: "CreateColPartyCadastreWizard",
        WIZARD_CLASS: SinglePageWizardFactory,
        WIZARD_FEATURE_NAME: QCoreApplication.translate("CreateColPartyCadastreWizard", "party"),
        WIZARD_TOOL_NAME: QCoreApplication.translate("CreateColPartyCadastreWizard", "Create party"),
        WIZARD_HELP: "col_party",
        WIZARD_UI: "wizards/cadastre/wiz_create_col_party_cadastre.ui",
        WIZARD_QSETTINGS: {
            WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM_COL/wizards/col_party_load_data_type"
        },
        WIZARD_HELP_PAGES: {
            WIZARD_HELP1: help_strings.WIZ_CREATE_COL_PARTY_CADASTRE_PAGE_1_OPTION_FORM,
            WIZARD_HELP2: ""
        },
        WIZARD_LAYERS: {
            COL_PARTY_TABLE: {'name': COL_PARTY_TABLE, 'geometry': None, LAYER: None}
        },
        WIZARD_EDITING_LAYER_NAME: COL_PARTY_TABLE,
        WIZARD_READ_ONLY_FIELDS: [],
        WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.NoGeometry
    },
    WIZARD_CREATE_ADMINISTRATIVE_SOURCE_CADASTRE: {
        WIZARD_TYPE: WizardTypeEnum.SINGLE_PAGE_WIZARD_TYPE,
        WIZARD_NAME: "CreateAdministrativeSourceCadastreWizard",
        WIZARD_CLASS: SinglePageWizardFactory,
        WIZARD_FEATURE_NAME: QCoreApplication.translate("CreateAdministrativeSourceCadastreWizard",
                                                                "administrative source"),
        WIZARD_TOOL_NAME: QCoreApplication.translate("CreateAdministrativeSourceCadastreWizard",
                                                                "Create administrative source"),
        WIZARD_HELP: "create_admin_source",
        WIZARD_UI: "wizards/cadastre/wiz_create_administrative_source_cadastre.ui",
        WIZARD_QSETTINGS: {
            WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM_COL/wizards/administrative_source_load_data_type"
        },
        WIZARD_HELP_PAGES: {
            WIZARD_HELP1: help_strings.WIZ_CREATE_ADMINISTRATIVE_SOURCE_PAGE_1_OPTION_FORM,
            WIZARD_HELP2: ""
        },
        WIZARD_LAYERS: {
            ADMINISTRATIVE_SOURCE_TABLE: {'name': ADMINISTRATIVE_SOURCE_TABLE, 'geometry': None, LAYER: None},
            EXTFILE_TABLE: {'name': EXTFILE_TABLE, 'geometry': None, LAYER: None}
        },
        WIZARD_EDITING_LAYER_NAME: ADMINISTRATIVE_SOURCE_TABLE,
        WIZARD_READ_ONLY_FIELDS: [],
        WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.NoGeometry
    },
    WIZARD_CREATE_BOUNDARY_CADASTRE: {
        WIZARD_TYPE: WizardTypeEnum.SINGLE_PAGE_SPATIAL_WIZARD_TYPE,
        WIZARD_NAME: "CreateBoundaryCadastreWizard",
        WIZARD_CLASS: SinglePageSpatialWizardFactory,
        WIZARD_FEATURE_NAME: QCoreApplication.translate("CreateBoundaryCadastreWizard", "boundary"),
        WIZARD_TOOL_NAME: QCoreApplication.translate("CreateBoundaryCadastreWizard", "Create boundary"),
        WIZARD_HELP: "create_boundaries",
        WIZARD_UI: "wizards/cadastre/wiz_create_boundaries_cadastre.ui",
        WIZARD_QSETTINGS: {
            WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM_COL/wizards/boundary_load_data_type"
        },
        WIZARD_HELP_PAGES: {
            WIZARD_HELP1: help_strings.WIZ_DEFINE_BOUNDARIES_CADASTRE_PAGE_1_OPTION_DIGITIZE,
            WIZARD_HELP2: ""
        },
        WIZARD_LAYERS: {
            BOUNDARY_TABLE: {'name': BOUNDARY_TABLE, 'geometry': QgsWkbTypes.LineGeometry, LAYER: None},
            BOUNDARY_POINT_TABLE: {'name': BOUNDARY_POINT_TABLE, 'geometry': QgsWkbTypes.PointGeometry, LAYER: None}
        },
        WIZARD_EDITING_LAYER_NAME: BOUNDARY_TABLE,
        WIZARD_READ_ONLY_FIELDS: [],
        WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.LineLayer
    },
    WIZARD_CREATE_BUILDING_CADASTRE: {
        WIZARD_TYPE: WizardTypeEnum.SINGLE_PAGE_SPATIAL_WIZARD_TYPE,
        WIZARD_NAME: "CreateBuildingCadastreWizard",
        WIZARD_CLASS: SinglePageSpatialWizardFactory,
        WIZARD_FEATURE_NAME: QCoreApplication.translate("CreateBuildingCadastreWizard", "building"),
        WIZARD_TOOL_NAME: QCoreApplication.translate("CreateBuildingCadastreWizard", "Create building"),
        WIZARD_HELP: "create_building",
        WIZARD_UI: "wizards/cadastre/wiz_create_building_cadastre.ui",
        WIZARD_QSETTINGS: {
            WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM_COL/wizards/building_load_data_type"
        },
        WIZARD_HELP_PAGES: {
            WIZARD_HELP1: help_strings.WIZ_CREATE_BUILDING_CADASTRE_PAGE_1_OPTION_POINTS,
            WIZARD_HELP2: ""
        },
        WIZARD_LAYERS: {
            BUILDING_TABLE: {'name': BUILDING_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            SURVEY_POINT_TABLE: {'name': SURVEY_POINT_TABLE, 'geometry': None, LAYER: None}
        },
        WIZARD_EDITING_LAYER_NAME: BUILDING_TABLE,
        WIZARD_READ_ONLY_FIELDS: [],
        WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.PolygonLayer
    },
    WIZARD_CREATE_BUILDING_UNIT_CADASTRE: {
        WIZARD_TYPE: WizardTypeEnum.SINGLE_PAGE_SPATIAL_WIZARD_TYPE,
        WIZARD_NAME: "CreateBuildingUnitCadastreWizard",
        WIZARD_CLASS: SinglePageSpatialWizardFactory,
        WIZARD_FEATURE_NAME: QCoreApplication.translate("CreateBuildingUnitCadastreWizard", "building unit"),
        WIZARD_TOOL_NAME: QCoreApplication.translate("CreateBuildingUnitCadastreWizard", "Create building unit"),
        WIZARD_HELP: "create_building_unit",
        WIZARD_UI: "wizards/cadastre/wiz_create_building_unit_cadastre.ui",
        WIZARD_QSETTINGS: {
            WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM_COL/wizards/building_unit_load_data_type"
        },
        WIZARD_HELP_PAGES: {
            WIZARD_HELP1: help_strings.WIZ_CREATE_BUILDING_UNIT_CADASTRE_PAGE_1_OPTION_POINTS,
            WIZARD_HELP2: ""
        },
        WIZARD_LAYERS: {
            BUILDING_UNIT_TABLE: {'name': BUILDING_UNIT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            BUILDING_TABLE: {'name': BUILDING_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            SURVEY_POINT_TABLE: {'name': SURVEY_POINT_TABLE, 'geometry': None, LAYER: None}
        },
        WIZARD_EDITING_LAYER_NAME: BUILDING_UNIT_TABLE,
        WIZARD_READ_ONLY_FIELDS: [],
        WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.PolygonLayer
    },
    WIZARD_CREATE_RIGHT_CADASTRE: {
        WIZARD_TYPE: WizardTypeEnum.MULTI_PAGE_WIZARD_TYPE,
        WIZARD_NAME: "CreateRightCadastreWizard",
        WIZARD_CLASS: CreateRRRCadastreWizard,
        WIZARD_FEATURE_NAME: QCoreApplication.translate("CreateRightCadastreWizard", "right"),
        WIZARD_TOOL_NAME: QCoreApplication.translate("CreateRightCadastreWizard", "Create right"),
        WIZARD_HELP: "create_right",
        WIZARD_UI: "wizards/cadastre/wiz_create_right_cadastre.ui",
        WIZARD_QSETTINGS: {
            WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM_COL/wizards/right_load_data_type"
        },
        WIZARD_HELP_PAGES: {
            WIZARD_HELP1: help_strings.WIZ_CREATE_RIGHT_CADASTRE_PAGE_1_OPTION_FORM,
            WIZARD_HELP2: help_strings.WIZ_CREATE_RIGHT_CADASTRE_PAGE_2
        },
        WIZARD_LAYERS: {
            RIGHT_TABLE: {'name': RIGHT_TABLE, 'geometry': None, LAYER: None},
            ADMINISTRATIVE_SOURCE_TABLE: {'name': ADMINISTRATIVE_SOURCE_TABLE, 'geometry': None, LAYER: None},
            RRR_SOURCE_RELATION_TABLE: {'name': RRR_SOURCE_RELATION_TABLE, 'geometry': None, LAYER: None}
        },
        WIZARD_EDITING_LAYER_NAME: RIGHT_TABLE,
        WIZARD_READ_ONLY_FIELDS: [],
        WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.NoGeometry
    },
    WIZARD_CREATE_RESTRICTION_CADASTRE: {
        WIZARD_TYPE: WizardTypeEnum.MULTI_PAGE_WIZARD_TYPE,
        WIZARD_NAME: "CreateRestrictionCadastreWizard",
        WIZARD_CLASS: CreateRRRCadastreWizard,
        WIZARD_FEATURE_NAME: QCoreApplication.translate("CreateRestrictionCadastreWizard", "restriction"),
        WIZARD_TOOL_NAME: QCoreApplication.translate("CreateRestrictionCadastreWizard", "Create restriction"),
        WIZARD_HELP: "create_restriction",
        WIZARD_UI: "wizards/cadastre/wiz_create_restriction_cadastre.ui",
        WIZARD_QSETTINGS: {
            WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM_COL/wizards/restriction_load_data_type"
        },
        WIZARD_HELP_PAGES: {
            WIZARD_HELP1: help_strings.WIZ_CREATE_RESTRICTION_CADASTRE_PAGE_1_OPTION_FORM,
            WIZARD_HELP2: help_strings.WIZ_CREATE_RESTRICTION_CADASTRE_PAGE_2
        },
        WIZARD_LAYERS: {
            RESTRICTION_TABLE: {'name': RESTRICTION_TABLE, 'geometry': None, LAYER: None},
            ADMINISTRATIVE_SOURCE_TABLE: {'name': ADMINISTRATIVE_SOURCE_TABLE, 'geometry': None, LAYER: None},
            RRR_SOURCE_RELATION_TABLE: {'name': RRR_SOURCE_RELATION_TABLE, 'geometry': None, LAYER: None}
        },
        WIZARD_EDITING_LAYER_NAME: RESTRICTION_TABLE,
        WIZARD_READ_ONLY_FIELDS: [],
        WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.NoGeometry
    },
    WIZARD_CREATE_SPATIAL_SOURCE_CADASTRE: {
        WIZARD_TYPE: WizardTypeEnum.MULTI_PAGE_WIZARD_TYPE,
        WIZARD_NAME: "CreateSpatialSourceCadastreWizard",
        WIZARD_CLASS: CreateSpatialSourceCadastreWizard,
        WIZARD_FEATURE_NAME: QCoreApplication.translate("CreateSpatialSourceCadastreWizard",
                                                                "spatial source"),
        WIZARD_TOOL_NAME: QCoreApplication.translate("CreateSpatialSourceCadastreWizard",
                                                                        "Create spatial source"),
        WIZARD_HELP: "create_spatial_source",
        WIZARD_UI: "wizards/cadastre/wiz_create_spatial_source_cadastre.ui",
        WIZARD_QSETTINGS: {
            WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM_COL/wizards/spatial_source_load_data_type"
        },
        WIZARD_HELP_PAGES: {
            WIZARD_HELP1: help_strings.WIZ_CREATE_SPATIAL_SOURCE_CADASTRE_PAGE_1_OPTION_FORM,
            WIZARD_HELP2: help_strings.WIZ_CREATE_SPATIAL_SOURCE_CADASTRE_PAGE_2
        },
        WIZARD_LAYERS: {
            SPATIAL_SOURCE_TABLE: {'name': SPATIAL_SOURCE_TABLE, 'geometry': None, LAYER: None},
            EXTFILE_TABLE: {'name': EXTFILE_TABLE, 'geometry': None, LAYER: None},
            PLOT_TABLE: {'name': PLOT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            UESOURCE_TABLE: {'name': UESOURCE_TABLE, 'geometry': None, LAYER: None},
            BOUNDARY_TABLE: {'name': BOUNDARY_TABLE, 'geometry': None, LAYER: None},
            CCLSOURCE_TABLE: {'name': CCLSOURCE_TABLE, 'geometry': None, LAYER: None},
            POINTSOURCE_TABLE: {'name': POINTSOURCE_TABLE, 'geometry': None, LAYER: None},
            BOUNDARY_POINT_TABLE: {'name': BOUNDARY_POINT_TABLE, 'geometry': None, LAYER: None},
            SURVEY_POINT_TABLE: {'name': SURVEY_POINT_TABLE, 'geometry': None, LAYER: None},
            CONTROL_POINT_TABLE: {'name': CONTROL_POINT_TABLE, 'geometry': None, LAYER: None}
        },
        WIZARD_EDITING_LAYER_NAME: SPATIAL_SOURCE_TABLE,
        WIZARD_READ_ONLY_FIELDS: [],
        WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.NoGeometry
    },
    WIZARD_CREATE_PARCEL_CADASTRE: {
        WIZARD_TYPE: WizardTypeEnum.MULTI_PAGE_WIZARD_TYPE,
        WIZARD_NAME: "CreateParcelCadastreWizard",
        WIZARD_CLASS: CreateParcelCadastreWizard,
        WIZARD_FEATURE_NAME: QCoreApplication.translate("CreateParcelCadastreWizard", "parcel"),
        WIZARD_TOOL_NAME: QCoreApplication.translate("CreateParcelCadastreWizard", "Create parcel"),
        WIZARD_HELP: "create_parcel",
        WIZARD_UI: "wizards/cadastre/wiz_create_parcel_cadastre.ui",
        WIZARD_QSETTINGS: {
            WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM_COL/wizards/parcel_load_data_type",
            WIZARD_QSETTINGS_TYPE_PARCEL_SELECTED: "Asistente-LADM_COL/wizards/type_of_parcel_selected"
        },
        WIZARD_HELP_PAGES: {
            WIZARD_HELP1: help_strings.WIZ_CREATE_PARCEL_CADASTRE_PAGE_1_OPTION_EXISTING_PLOT,
            WIZARD_HELP2: help_strings.WIZ_CREATE_PARCEL_CADASTRE_PAGE_2
        },
        WIZARD_LAYERS: {
            PLOT_TABLE: {'name': PLOT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            PARCEL_TABLE: {'name': PARCEL_TABLE, 'geometry': None, LAYER: None},
            BUILDING_TABLE: {'name': BUILDING_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            BUILDING_UNIT_TABLE: {'name': BUILDING_UNIT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            UEBAUNIT_TABLE: {'name': UEBAUNIT_TABLE, 'geometry': None, LAYER: None}
        },
        WIZARD_EDITING_LAYER_NAME: PARCEL_TABLE,
        WIZARD_READ_ONLY_FIELDS: [PARCEL_TYPE_FIELD],
        WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.NoGeometry
    },
    WIZARD_CREATE_PLOT_CADASTRE: {
        WIZARD_TYPE: WizardTypeEnum.MULTI_PAGE_WIZARD_TYPE,
        WIZARD_NAME: "CreatePlotCadastreWizard",
        WIZARD_CLASS: CreatePlotCadastreWizard,
        WIZARD_FEATURE_NAME: QCoreApplication.translate("CreatePlotCadastreWizard", "plot"),
        WIZARD_TOOL_NAME: QCoreApplication.translate("CreatePlotCadastreWizard", "Create plot"),
        WIZARD_HELP: "create_plot",
        WIZARD_UI: "wizards/cadastre/wiz_create_plot_cadastre.ui",
        WIZARD_QSETTINGS: {
            WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM_COL/wizards/plot_load_data_type"
        },
        WIZARD_HELP_PAGES: {
            WIZARD_HELP1: help_strings.WIZ_CREATE_PLOT_CADASTRE_PAGE_1_OPTION_BOUNDARIES,
            WIZARD_HELP2: help_strings.WIZ_CREATE_PLOT_CADASTRE_PAGE_2
        },
        WIZARD_LAYERS: {
            PLOT_TABLE: {'name': PLOT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            BOUNDARY_TABLE: {'name': BOUNDARY_TABLE, 'geometry': None, LAYER: None}
        },
        WIZARD_EDITING_LAYER_NAME: PLOT_TABLE,
        WIZARD_READ_ONLY_FIELDS: [],
        WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.PolygonLayer
    },
    WIZARD_CREATE_EXT_ADDRESS_CADASTRE: {
        WIZARD_TYPE: WizardTypeEnum.MULTI_PAGE_SPATIAL_WIZARD_TYPE,
        WIZARD_NAME: "CreateExtAddressCadastreWizard",
        WIZARD_CLASS: CreateExtAddressCadastreWizard,
        WIZARD_FEATURE_NAME: QCoreApplication.translate("CreateExtAddressCadastreWizard", "ext address"),
        WIZARD_TOOL_NAME: QCoreApplication.translate("CreateExtAddressCadastreWizard", "Create ext address"),
        WIZARD_HELP: "associate_ext_address",
        WIZARD_UI: "wizards/cadastre/wiz_associate_extaddress_cadastre.ui",
        WIZARD_QSETTINGS: {
            WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM_COL/wizards/ext_address_load_data_type"
        },
        WIZARD_HELP_PAGES: {
            WIZARD_HELP1: help_strings.WIZ_ASSOCIATE_EXTADDRESS_CADASTRE_PAGE_1,
            WIZARD_HELP1: help_strings.WIZ_ASSOCIATE_EXTADDRESS_CADASTRE_PAGE_2_OPTION_1,
            WIZARD_HELP2: help_strings.WIZ_ASSOCIATE_EXTADDRESS_CADASTRE_PAGE_2_OPTION_2,
            WIZARD_HELP3: help_strings.WIZ_ASSOCIATE_EXTADDRESS_CADASTRE_PAGE_2_OPTION_3
        },
        WIZARD_LAYERS: {
            EXTADDRESS_TABLE: {'name': EXTADDRESS_TABLE, 'geometry': QgsWkbTypes.PointGeometry, LAYER: None},
            PLOT_TABLE: {'name': PLOT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            BUILDING_TABLE: {'name': BUILDING_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            BUILDING_UNIT_TABLE: {'name': BUILDING_UNIT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None}
        },
        WIZARD_EDITING_LAYER_NAME: EXTADDRESS_TABLE,
        WIZARD_READ_ONLY_FIELDS: [],
        WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.PolygonLayer
    },
    WIZARD_CREATE_RIGHT_OF_WAY_CADASTRE: {
        WIZARD_TYPE: WizardTypeEnum.SINGLE_PAGE_SPATIAL_WIZARD_TYPE,
        WIZARD_NAME: "CreateRightOfWayCadastreWizard",
        WIZARD_CLASS: CreateRightOfWayCadastreWizard,
        WIZARD_FEATURE_NAME: QCoreApplication.translate("CreateRightOfWayCadastreWizard", "right of way"),
        WIZARD_TOOL_NAME: QCoreApplication.translate("CreateRightOfWayCadastreWizard", "Create right of way"),
        WIZARD_HELP: "create_right_of_way",
        WIZARD_UI: "wizards/cadastre/wiz_create_right_of_way_cadastre.ui",
        WIZARD_QSETTINGS: {
            WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM_COL/wizards/right_of_way_load_data_type"
        },
        WIZARD_HELP_PAGES: {
            WIZARD_HELP1: help_strings.WIZ_CREATE_RIGHT_OF_WAY_CADASTRE_PAGE_1_OPTION_POINTS,
            WIZARD_HELP2: help_strings.WIZ_CREATE_RIGHT_OF_WAY_CADASTRE_PAGE_1_OPTION2_POINTS,
            WIZARD_HELP3: help_strings.WIZ_ASSOCIATE_EXTADDRESS_CADASTRE_PAGE_2_OPTION_2,
            WIZARD_HELP4: help_strings.WIZ_ASSOCIATE_EXTADDRESS_CADASTRE_PAGE_2_OPTION_3
        },
        WIZARD_LAYERS: {
            RIGHT_OF_WAY_TABLE: {'name': RIGHT_OF_WAY_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            PLOT_TABLE: {'name': PLOT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            SURVEY_POINT_TABLE: {'name': SURVEY_POINT_TABLE, 'geometry': None, LAYER: None}
        },
        WIZARD_EDITING_LAYER_NAME: RIGHT_OF_WAY_TABLE,
        WIZARD_READ_ONLY_FIELDS: [],
        WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.PolygonLayer
    },
    # VALUATION MODEL
    WIZARD_CREATE_GEOECONOMIC_ZONE_VALUATION: {
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
    },
    WIZARD_CREATE_PHYSICAL_ZONE_VALUATION: {
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
    },
    WIZARD_CREATE_BUILDING_UNIT_VALUATION: {
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
            BUILDING_UNIT_TABLE: {'name': BUILDING_UNIT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            AVALUOUNIDADCONSTRUCCION_TABLE: {'name': AVALUOUNIDADCONSTRUCCION_TABLE, 'geometry': None, LAYER: None}
        },
        WIZARD_EDITING_LAYER_NAME: VALUATION_BUILDING_UNIT_TABLE,
        WIZARD_READ_ONLY_FIELDS: [],
        WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.NoGeometry
    },
    WIZARD_CREATE_BUILDING_UNIT_QUALIFICATION_VALUATION: {
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
            WIZARD_HELP1: help_strings.WIZ_ADD_POINTS_CADASTRE_PAGE_2_OPTION_CSV,
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
}