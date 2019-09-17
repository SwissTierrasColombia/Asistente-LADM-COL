from qgis.PyQt.QtCore import QCoreApplication

from ..config.help_strings import HelpStrings
from ..config.table_mapping_config import (COL_PARTY_TABLE,
                                           BUILDING_TABLE,
                                           BUILDING_UNIT_TABLE,
                                           SURVEY_POINT_TABLE,
                                           LEGAL_PARTY_TABLE,
                                           NATURAL_PARTY_TABLE,
                                           NUCLEAR_FAMILY_TABLE,
                                           MARKET_RESEARCH_TABLE,
                                           PROPERTY_RECORD_CARD_TABLE,
                                           ADMINISTRATIVE_SOURCE_TABLE,
                                           RIGHT_TABLE,
                                           RESTRICTION_TABLE,
                                           RESPONSIBILITY_TABLE,
                                           RRR_SOURCE_RELATION_TABLE,
                                           BOUNDARY_TABLE,
                                           BOUNDARY_POINT_TABLE,
                                           EXTFILE_TABLE,
                                           VALUATION_HORIZONTAL_PROPERTY_TABLE,
                                           VALUATION_COMMON_EQUIPMENT_TABLE,
                                           VALUATION_BUILDING_TABLE,
                                           VALUATION_GEOECONOMIC_ZONE_TABLE,
                                           VALUATION_PHYSICAL_ZONE_TABLE,
                                           VALUATION_PARCEL_TABLE)
from ..config.general_config import LAYER

from qgis.core import (QgsMapLayerProxyModel,
                       QgsWkbTypes)

help_strings = HelpStrings()


class WizardConfig:
    SINGLE_PAGE_WIZARD_TYPE = "SinglePageWizard"
    SINGLE_PAGE_SPATIAL_WIZARD_TYPE = "SinglePageSpatialWizard"
    MULTI_PAGE_WIZARD_TYPE = "MultiPageWizard"
    RRR_CADASTRE_WIZARD_TYPE = "RRRCadastreWizard"

    WIZARD_NAME_SETTING = "wizard_name"
    WIZARD_FEATURE_NAME_SETTING = "wizard_tool_name"
    WIZARD_UI_SETTING = "wizard_ui"
    WIZARD_HELP_SETTING = "wizard_help"
    WIZARD_HELP_PAGES_SETTING = "wizard_help_page"
    WIZARD_QSETTINGS_SETTING = "wizard_qsettings"
    WIZARD_QSETTINGS_LOAD_DATA_TYPE = "wizard_qsettings_load_data_type"
    WIZARD_HELP_PAGE1 = "wizard_help_pages_page1"
    WIZARD_HELP_PAGE2 = "wizard_help_pages_page2"
    WIZARD_LAYERS_SETTING = "wizard_layers"
    WIZARD_EDITING_LAYER_NAME_SETTING = "wizard_editing_layer_name"
    WIZARD_MAP_LAYER_PROXY_MODEL = "wizard_map_layer_proxy_model"

    # Cadastral model
    WIZARD_CREATE_COL_PARTY_CADASTRAL = "wizard_create_col_party_cadastral"
    WIZARD_CREATE_ADMINISTRATIVE_SOURCE_CADASTRE = "wizard_create_administrative_source_cadastre"
    WIZARD_CREATE_BOUNDARY_CADASTRE = "wizard_create_boundary_cadastre"
    WIZARD_CREATE_BUILDING_CADASTRE = "wizard_create_building_cadastre"
    WIZARD_CREATE_BUILDING_UNIT_CADASTRE = "wizard_create_building_unit_cadastre"
    WIZARD_CREATE_RIGHT_CADASTRE = "wizard_create_right_cadastre"
    WIZARD_CREATE_RESTRICTION_CADASTRE = "wizard_create_restriction_cadastre"
    WIZARD_CREATE_RESPONSIBILITY_CADASTRE = "wizard_create_responsibility_cadastre"

    # Valuation model
    WIZARD_CREATE_PARCEL_VALUATION = "wizard_create_parcel_valuation"
    WIZARD_CREATE_HORIZONTAL_PROPERTY_VALUATION = "wizard_create_horizontal_property_valuation"
    WIZARD_CREATE_COMMON_EQUIPMENT_VALUATION = "wizard_create_common_equipment_valuation"
    WIZARD_CREATE_BUILDING_VALUATION = "wizard_create_building_valuation"
    WIZARD_CREATE_GEOECONOMIC_ZONE_VALUATION = "wizard_create_geoeconomic_zone_valuation"
    WIZARD_CREATE_PHYSICAL_ZONE_VALUATION = "wizard_create_physical_zone_valuation"

    # Property Record Card model
    WIZARD_CREATE_LEGAL_PARTY_PRC = "wizard_create_legal_party_prc"
    WIZARD_CREATE_NATURAL_PARTY_PRC = "wizard_create_natural_party_prc"
    WIZARD_CREATE_NUCLEAR_FAMILY_PRC = "wizard_create_nuclear_family_prc"
    WIZARD_CREATE_MARKET_RESEARCH_PRC = "wizard_create_market_research_prc"
    WIZARD_CREATE_PROPERTY_RECORD_CARD_PRC = "wizard_create_property_record_card"

    WIZARDS_SETTINGS = {
        # CADASTRAL MODEL
        WIZARD_CREATE_COL_PARTY_CADASTRAL: {
            WIZARD_NAME_SETTING: "CreateColPartyCadastreWizard",
            WIZARD_FEATURE_NAME_SETTING: QCoreApplication.translate("CreateColPartyCadastreWizard", "party"),
            WIZARD_HELP_SETTING: "col_party",
            WIZARD_UI_SETTING: "wizards/cadastre/party/wiz_create_col_party_cadastre.ui",
            WIZARD_QSETTINGS_SETTING: {
                WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM_COL/wizards/col_party_load_data_type"
            },
            WIZARD_HELP_PAGES_SETTING: {
                WIZARD_HELP_PAGE1: help_strings.WIZ_CREATE_COL_PARTY_CADASTRE_PAGE_1_OPTION_FORM,
                WIZARD_HELP_PAGE2: ""
            },
            WIZARD_LAYERS_SETTING: {
                COL_PARTY_TABLE: {'name': COL_PARTY_TABLE, 'geometry': None, LAYER: None}
            },
            WIZARD_EDITING_LAYER_NAME_SETTING: COL_PARTY_TABLE,
            WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.NoGeometry
        },
        WIZARD_CREATE_ADMINISTRATIVE_SOURCE_CADASTRE: {
            WIZARD_NAME_SETTING: "CreateAdministrativeSourceCadastreWizard",
            WIZARD_FEATURE_NAME_SETTING: QCoreApplication.translate("CreateAdministrativeSourceCadastreWizard", "administrative source"),
            WIZARD_HELP_SETTING: "create_admin_source",
            WIZARD_UI_SETTING: "wizards/cadastre/source/wiz_create_administrative_source_cadastre.ui",
            WIZARD_QSETTINGS_SETTING: {
                WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM_COL/wizards/administrative_source_load_data_type"
            },
            WIZARD_HELP_PAGES_SETTING: {
                WIZARD_HELP_PAGE1: help_strings.WIZ_CREATE_ADMINISTRATIVE_SOURCE_PAGE_1_OPTION_FORM,
                WIZARD_HELP_PAGE2: ""
            },
            WIZARD_LAYERS_SETTING: {
                ADMINISTRATIVE_SOURCE_TABLE: {'name': ADMINISTRATIVE_SOURCE_TABLE, 'geometry': None, LAYER: None},
                EXTFILE_TABLE: {'name': EXTFILE_TABLE, 'geometry': None, LAYER: None}
            },
            WIZARD_EDITING_LAYER_NAME_SETTING: ADMINISTRATIVE_SOURCE_TABLE,
            WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.NoGeometry
        },
        WIZARD_CREATE_BOUNDARY_CADASTRE:{
            WIZARD_NAME_SETTING: "CreateBoundaryCadastreWizard",
            WIZARD_FEATURE_NAME_SETTING: QCoreApplication.translate("CreateBoundaryCadastreWizard", "boundary"),
            WIZARD_HELP_SETTING: "create_boundaries",
            WIZARD_UI_SETTING: "wizards/cadastre/surveying/wiz_create_boundaries_cadastre.ui",
            WIZARD_QSETTINGS_SETTING: {
                WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM_COL/wizards/boundary_load_data_type"
            },
            WIZARD_HELP_PAGES_SETTING: {
                WIZARD_HELP_PAGE1: help_strings.WIZ_DEFINE_BOUNDARIES_CADASTRE_PAGE_1_OPTION_DIGITIZE,
                WIZARD_HELP_PAGE2: ""
            },
            WIZARD_LAYERS_SETTING: {
                BOUNDARY_TABLE: {'name': BOUNDARY_TABLE, 'geometry': QgsWkbTypes.LineGeometry, LAYER: None},
                BOUNDARY_POINT_TABLE: {'name': BOUNDARY_POINT_TABLE, 'geometry': QgsWkbTypes.PointGeometry, LAYER: None}
            },
            WIZARD_EDITING_LAYER_NAME_SETTING: BOUNDARY_TABLE,
            WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.LineLayer
        },
        WIZARD_CREATE_BUILDING_CADASTRE: {
            WIZARD_NAME_SETTING: "CreateBuildingCadastreWizard",
            WIZARD_FEATURE_NAME_SETTING: QCoreApplication.translate("CreateBuildingCadastreWizard", "building"),
            WIZARD_HELP_SETTING: "create_building",
            WIZARD_UI_SETTING: "wizards/cadastre/spatial_unit/wiz_create_building_cadastre.ui",
            WIZARD_QSETTINGS_SETTING: {
                WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM_COL/wizards/building_load_data_type"
            },
            WIZARD_HELP_PAGES_SETTING: {
                WIZARD_HELP_PAGE1: help_strings.WIZ_CREATE_BUILDING_CADASTRE_PAGE_1_OPTION_POINTS,
                WIZARD_HELP_PAGE2: ""
            },
            WIZARD_LAYERS_SETTING: {
                BUILDING_TABLE: {'name': BUILDING_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
                SURVEY_POINT_TABLE: {'name': SURVEY_POINT_TABLE, 'geometry': None, LAYER: None}
            },
            WIZARD_EDITING_LAYER_NAME_SETTING: BUILDING_TABLE,
            WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.PolygonLayer
        },
        WIZARD_CREATE_BUILDING_UNIT_CADASTRE: {
            WIZARD_NAME_SETTING: "CreateBuildingUnitCadastreWizard",
            WIZARD_FEATURE_NAME_SETTING: QCoreApplication.translate("CreateBuildingUnitCadastreWizard", "building unit"),
            WIZARD_HELP_SETTING: "create_building_unit",
            WIZARD_UI_SETTING: "wizards/cadastre/spatial_unit/wiz_create_building_unit_cadastre.ui",
            WIZARD_QSETTINGS_SETTING: {
                WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM_COL/wizards/building_unit_load_data_type"
            },
            WIZARD_HELP_PAGES_SETTING: {
                WIZARD_HELP_PAGE1: help_strings.WIZ_CREATE_BUILDING_UNIT_CADASTRE_PAGE_1_OPTION_POINTS,
                WIZARD_HELP_PAGE2: ""
            },
            WIZARD_LAYERS_SETTING: {
                BUILDING_UNIT_TABLE: {'name': BUILDING_UNIT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
                SURVEY_POINT_TABLE: {'name': SURVEY_POINT_TABLE, 'geometry': None, LAYER: None}
            },
            WIZARD_EDITING_LAYER_NAME_SETTING: BUILDING_UNIT_TABLE,
            WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.PolygonLayer
        },
        WIZARD_CREATE_RIGHT_CADASTRE: {
            WIZARD_NAME_SETTING: "CreateRightCadastreWizard",
            WIZARD_FEATURE_NAME_SETTING: QCoreApplication.translate("CreateRightCadastreWizard", "right"),
            WIZARD_HELP_SETTING: "create_right",
            WIZARD_UI_SETTING: "wizards/cadastre/rrr/wiz_create_right_cadastre.ui",
            WIZARD_QSETTINGS_SETTING: {
                WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM_COL/wizards/right_load_data_type"
            },
            WIZARD_HELP_PAGES_SETTING: {
                WIZARD_HELP_PAGE1: help_strings.WIZ_CREATE_RIGHT_CADASTRE_PAGE_1_OPTION_FORM,
                WIZARD_HELP_PAGE2: help_strings.WIZ_CREATE_RIGHT_CADASTRE_PAGE_2
            },
            WIZARD_LAYERS_SETTING: {
                RIGHT_TABLE: {'name': RIGHT_TABLE, 'geometry': None, LAYER: None},
                ADMINISTRATIVE_SOURCE_TABLE: {'name': ADMINISTRATIVE_SOURCE_TABLE, 'geometry': None, LAYER: None},
                RRR_SOURCE_RELATION_TABLE: {'name': RRR_SOURCE_RELATION_TABLE, 'geometry': None, LAYER: None}
            },
            WIZARD_EDITING_LAYER_NAME_SETTING: RIGHT_TABLE,
            WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.NoGeometry
        },
        WIZARD_CREATE_RESTRICTION_CADASTRE: {
            WIZARD_NAME_SETTING: "CreateRestrictionCadastreWizard",
            WIZARD_FEATURE_NAME_SETTING: QCoreApplication.translate("CreateRestrictionCadastreWizard", "restriction"),
            WIZARD_HELP_SETTING: "create_restriction",
            WIZARD_UI_SETTING: "wizards/cadastre/rrr/wiz_create_restriction_cadastre.ui",
            WIZARD_QSETTINGS_SETTING: {
                WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM_COL/wizards/restriction_load_data_type"
            },
            WIZARD_HELP_PAGES_SETTING: {
                WIZARD_HELP_PAGE1: help_strings.WIZ_CREATE_RESTRICTION_CADASTRE_PAGE_1_OPTION_FORM,
                WIZARD_HELP_PAGE2: help_strings.WIZ_CREATE_RESTRICTION_CADASTRE_PAGE_2
            },
            WIZARD_LAYERS_SETTING: {
                RESTRICTION_TABLE: {'name': RESTRICTION_TABLE, 'geometry': None, LAYER: None},
                ADMINISTRATIVE_SOURCE_TABLE: {'name': ADMINISTRATIVE_SOURCE_TABLE, 'geometry': None, LAYER: None},
                RRR_SOURCE_RELATION_TABLE: {'name': RRR_SOURCE_RELATION_TABLE, 'geometry': None, LAYER: None}
            },
            WIZARD_EDITING_LAYER_NAME_SETTING: RESTRICTION_TABLE,
            WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.NoGeometry
        },
        WIZARD_CREATE_RESPONSIBILITY_CADASTRE: {
            WIZARD_NAME_SETTING: "CreateResponsibilityCadastreWizard",
            WIZARD_FEATURE_NAME_SETTING: QCoreApplication.translate("CreateResponsibilityCadastreWizard", "responsibility"),
            WIZARD_HELP_SETTING: "create_responsibility",
            WIZARD_UI_SETTING: "wizards/cadastre/rrr/wiz_create_responsibility_cadastre.ui",
            WIZARD_QSETTINGS_SETTING: {
                WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM_COL/wizards/responsibility_load_data_type"
            },
            WIZARD_HELP_PAGES_SETTING: {
                WIZARD_HELP_PAGE1: help_strings.WIZ_CREATE_RESPONSIBILITY_CADASTRE_PAGE_1_OPTION_FORM,
                WIZARD_HELP_PAGE2: help_strings.WIZ_CREATE_RESPONSIBILITY_CADASTRE_PAGE_2
            },
            WIZARD_LAYERS_SETTING: {
                RESPONSIBILITY_TABLE: {'name': RESPONSIBILITY_TABLE, 'geometry': None, LAYER: None},
                ADMINISTRATIVE_SOURCE_TABLE: {'name': ADMINISTRATIVE_SOURCE_TABLE, 'geometry': None, LAYER: None},
                RRR_SOURCE_RELATION_TABLE: {'name': RRR_SOURCE_RELATION_TABLE, 'geometry': None, LAYER: None}
            },
            WIZARD_EDITING_LAYER_NAME_SETTING: RESPONSIBILITY_TABLE,
            WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.NoGeometry
        },
        # VALUATION MODEL
        WIZARD_CREATE_PARCEL_VALUATION: {
            WIZARD_NAME_SETTING: "CreateParcelValuationWizard",
            WIZARD_FEATURE_NAME_SETTING: QCoreApplication.translate("CreateParcelValuationWizard", "parcel valuation"),
            WIZARD_HELP_SETTING: "create_parcel_valuation",
            WIZARD_UI_SETTING: "wizards/valuation/wiz_create_parcel_valuation.ui",
            WIZARD_QSETTINGS_SETTING: {
                WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM_COL/wizards/valuation_parcel_load_data_type"
            },
            WIZARD_HELP_PAGES_SETTING: {
                WIZARD_HELP_PAGE1: help_strings.WIZ_CREATE_PARCEL_VALUATION_PAGE_1_OPTION_FORM,
                WIZARD_HELP_PAGE2: ""
            },
            WIZARD_LAYERS_SETTING: {
                VALUATION_PARCEL_TABLE: {'name': VALUATION_PARCEL_TABLE, 'geometry': None, LAYER: None}
            },
            WIZARD_EDITING_LAYER_NAME_SETTING: VALUATION_PARCEL_TABLE,
            WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.NoGeometry
        },
        WIZARD_CREATE_HORIZONTAL_PROPERTY_VALUATION: {
            WIZARD_NAME_SETTING: "CreateHorizontalPropertyValuationWizard",
            WIZARD_FEATURE_NAME_SETTING: QCoreApplication.translate("CreateHorizontalPropertyValuationWizard", "horizontal property valuation"),
            WIZARD_HELP_SETTING: "create_horizontal_property_valuation",
            WIZARD_UI_SETTING: "wizards/valuation/wiz_create_horizontal_property_valuation.ui",
            WIZARD_QSETTINGS_SETTING: {
                WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM_COL/wizards/valuation_horizontal_property_load_data_type"
            },
            WIZARD_HELP_PAGES_SETTING: {
                WIZARD_HELP_PAGE1: help_strings.WIZ_CREATE_HORIZONTAL_PROPERTY_VALUATION_PAGE_1_OPTION_FORM,
                WIZARD_HELP_PAGE2: ""
            },
            WIZARD_LAYERS_SETTING: {
                VALUATION_HORIZONTAL_PROPERTY_TABLE: {'name': VALUATION_HORIZONTAL_PROPERTY_TABLE, 'geometry': None, LAYER: None}
            },
            WIZARD_EDITING_LAYER_NAME_SETTING: VALUATION_HORIZONTAL_PROPERTY_TABLE,
            WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.NoGeometry
        },
        WIZARD_CREATE_COMMON_EQUIPMENT_VALUATION: {
            WIZARD_NAME_SETTING: "CreateCommonEquipmentValuationWizard",
            WIZARD_FEATURE_NAME_SETTING: QCoreApplication.translate("CreateCommonEquipmentValuationWizard", "common equipment valuation"),
            WIZARD_HELP_SETTING: "create_common_equipment_valuation",
            WIZARD_UI_SETTING: "wizards/valuation/wiz_create_common_equipment_valuation.ui",
            WIZARD_QSETTINGS_SETTING: {
                WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM_COL/wizards/valuation_common_equipment_load_data_type"
            },
            WIZARD_HELP_PAGES_SETTING: {
                WIZARD_HELP_PAGE1: help_strings.WIZ_CREATE_COMMON_EQUIPMENT_VALUATION_PAGE_1_OPTION_FORM,
                WIZARD_HELP_PAGE2: ""
            },
            WIZARD_LAYERS_SETTING: {
                VALUATION_COMMON_EQUIPMENT_TABLE: {'name': VALUATION_COMMON_EQUIPMENT_TABLE, 'geometry': None, LAYER: None}
            },
            WIZARD_EDITING_LAYER_NAME_SETTING: VALUATION_COMMON_EQUIPMENT_TABLE,
            WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.NoGeometry
        },
        WIZARD_CREATE_BUILDING_VALUATION: {
            WIZARD_NAME_SETTING: "CreateBuildingValuationWizard",
            WIZARD_FEATURE_NAME_SETTING: QCoreApplication.translate("CreateBuildingValuationWizard", "building valuation"),
            WIZARD_HELP_SETTING: "create_building_valuation",
            WIZARD_UI_SETTING: "wizards/valuation/wiz_create_building_valuation.ui",
            WIZARD_QSETTINGS_SETTING: {
                WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM_COL/wizards/valuation_building_load_data_type"
            },
            WIZARD_HELP_PAGES_SETTING: {
                WIZARD_HELP_PAGE1: help_strings.WIZ_CREATE_BUILDING_VALUATION_PAGE_1_OPTION_FORM,
                WIZARD_HELP_PAGE2: ""
            },
            WIZARD_LAYERS_SETTING: {
                VALUATION_BUILDING_TABLE: {'name': VALUATION_BUILDING_TABLE, 'geometry': None, LAYER: None}
            },
            WIZARD_EDITING_LAYER_NAME_SETTING: VALUATION_BUILDING_TABLE,
            WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.NoGeometry
        },
        WIZARD_CREATE_GEOECONOMIC_ZONE_VALUATION: {
            WIZARD_NAME_SETTING: "CreateGeoeconomicZoneValuationWizard",
            WIZARD_FEATURE_NAME_SETTING: QCoreApplication.translate("CreateGeoeconomicZoneValuationWizard", "geoeconomic zone"),
            WIZARD_HELP_SETTING: "create_geoeconomic_zone_valuation",
            WIZARD_UI_SETTING: "wizards/valuation/wiz_create_geoeconomic_zone_valuation.ui",
            WIZARD_QSETTINGS_SETTING: {
                WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM_COL/wizards/geoeconomic_zone_valuation_load_data_type"
            },
            WIZARD_HELP_PAGES_SETTING: {
                WIZARD_HELP_PAGE1: help_strings.WIZ_CREATE_GEOECONOMIC_ZONE_VALUATION_PAGE_1_OPTION_FORM,
                WIZARD_HELP_PAGE2: ""
            },
            WIZARD_LAYERS_SETTING: {
                VALUATION_GEOECONOMIC_ZONE_TABLE: {'name': VALUATION_GEOECONOMIC_ZONE_TABLE, 'geometry': None, LAYER: None}
            },
            WIZARD_EDITING_LAYER_NAME_SETTING: VALUATION_GEOECONOMIC_ZONE_TABLE,
            WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.PolygonLayer
        },
        WIZARD_CREATE_PHYSICAL_ZONE_VALUATION: {
            WIZARD_NAME_SETTING: "CreatePhysicalZoneValuationWizard",
            WIZARD_FEATURE_NAME_SETTING: QCoreApplication.translate("CreatePhysicalZoneValuationWizard", "physical zone"),
            WIZARD_HELP_SETTING: "create_physical_zone_valuation",
            WIZARD_UI_SETTING: "wizards/valuation/wiz_create_physical_zone_valuation.ui",
            WIZARD_QSETTINGS_SETTING: {
                WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM_COL/wizards/physical_zone_valuation_load_data_type"
            },
            WIZARD_HELP_PAGES_SETTING: {
                WIZARD_HELP_PAGE1: help_strings.WIZ_CREATE_PHYSICAL_ZONE_VALUATION_PAGE_1_OPTION_FORM,
                WIZARD_HELP_PAGE2: ""
            },
            WIZARD_LAYERS_SETTING: {
                VALUATION_PHYSICAL_ZONE_TABLE: {'name': VALUATION_PHYSICAL_ZONE_TABLE, 'geometry': None, LAYER: None}
            },
            WIZARD_EDITING_LAYER_NAME_SETTING: VALUATION_PHYSICAL_ZONE_TABLE,
            WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.PolygonLayer
        },
        # PROPERTY RECORD CARD MODEL
        WIZARD_CREATE_LEGAL_PARTY_PRC: {
            WIZARD_NAME_SETTING: "CreateLegalPartyWizard",
            WIZARD_FEATURE_NAME_SETTING: QCoreApplication.translate("CreateLegalPartyWizard", "legal party card"),
            WIZARD_HELP_SETTING: "create_legal_party",
            WIZARD_UI_SETTING: "wizards/property_record_card/wiz_create_legal_party_prc.ui",
            WIZARD_QSETTINGS_SETTING: {
                WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM_COL/wizards/legal_party_load_data_type"
            },
            WIZARD_HELP_PAGES_SETTING: {
                WIZARD_HELP_PAGE1: help_strings.WIZ_CREATE_LEGAL_PARTY_PRC_PAGE_1_OPTION_FORM,
                WIZARD_HELP_PAGE2: ""
            },
            WIZARD_LAYERS_SETTING: {
                LEGAL_PARTY_TABLE: {'name': LEGAL_PARTY_TABLE, 'geometry': None, LAYER: None},
                COL_PARTY_TABLE: {'name': COL_PARTY_TABLE, 'geometry': None, LAYER: None}
            },
            WIZARD_EDITING_LAYER_NAME_SETTING: LEGAL_PARTY_TABLE,
            WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.NoGeometry
        },
        WIZARD_CREATE_NATURAL_PARTY_PRC: {
            WIZARD_NAME_SETTING: "CreateNaturalPartyPRCWizard",
            WIZARD_FEATURE_NAME_SETTING: QCoreApplication.translate("CreateNaturalPartyPRCWizard", "natural party"),
            WIZARD_HELP_SETTING: "create_natural_party",
            WIZARD_UI_SETTING: "wizards/property_record_card/wiz_create_natural_party_prc.ui",
            WIZARD_QSETTINGS_SETTING: {
                WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM_COL/wizards/natural_party_load_data_type"
            },
            WIZARD_HELP_PAGES_SETTING: {
                WIZARD_HELP_PAGE1: help_strings.WIZ_CREATE_NATURAL_PARTY_PRC_PAGE_1_OPTION_FORM,
                WIZARD_HELP_PAGE2: ""
            },
            WIZARD_LAYERS_SETTING: {
                NATURAL_PARTY_TABLE: {'name': NATURAL_PARTY_TABLE, 'geometry': None, LAYER: None}
            },
            WIZARD_EDITING_LAYER_NAME_SETTING: NATURAL_PARTY_TABLE,
            WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.NoGeometry
        },
        WIZARD_CREATE_NUCLEAR_FAMILY_PRC: {
            WIZARD_NAME_SETTING: "CreateNuclearFamilyPRCWizard",
            WIZARD_FEATURE_NAME_SETTING: QCoreApplication.translate("CreateNuclearFamilyPRCWizard", "nuclear family"),
            WIZARD_HELP_SETTING: "create_nuclear_family",
            WIZARD_UI_SETTING: "wizards/property_record_card/wiz_create_nuclear_family_prc.ui",
            WIZARD_QSETTINGS_SETTING: {
                WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM_COL/wizards/nuclear_family_load_data_type"
            },
            WIZARD_HELP_PAGES_SETTING: {
                WIZARD_HELP_PAGE1: help_strings.WIZ_CREATE_NUCLEAR_FAMILY_PRC_PAGE_1_OPTION_FORM,
                WIZARD_HELP_PAGE2: ""
            },
            WIZARD_LAYERS_SETTING: {
                NUCLEAR_FAMILY_TABLE: {'name': NUCLEAR_FAMILY_TABLE, 'geometry': None, LAYER: None}
            },
            WIZARD_EDITING_LAYER_NAME_SETTING: NUCLEAR_FAMILY_TABLE,
            WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.NoGeometry
        },
        WIZARD_CREATE_MARKET_RESEARCH_PRC: {
            WIZARD_NAME_SETTING: "CreateMarketResearchPRCWizard",
            WIZARD_FEATURE_NAME_SETTING: QCoreApplication.translate("CreateMarketResearchPRCWizard", "market research"),
            WIZARD_HELP_SETTING: "create_market_research",
            WIZARD_UI_SETTING: "wizards/property_record_card/wiz_create_market_research_prc.ui",
            WIZARD_QSETTINGS_SETTING: {
                WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM_COL/wizards/market_research_load_data_type"
            },
            WIZARD_HELP_PAGES_SETTING: {
                WIZARD_HELP_PAGE1: help_strings.WIZ_CREATE_MARKET_RESEARCH_PRC_PAGE_1_OPTION_FORM,
                WIZARD_HELP_PAGE2: ""
            },
            WIZARD_LAYERS_SETTING: {
                MARKET_RESEARCH_TABLE: {'name': MARKET_RESEARCH_TABLE, 'geometry': None, LAYER: None}
            },
            WIZARD_EDITING_LAYER_NAME_SETTING: MARKET_RESEARCH_TABLE,
            WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.NoGeometry
        },
        WIZARD_CREATE_PROPERTY_RECORD_CARD_PRC: {
            WIZARD_NAME_SETTING: "CreatePropertyRecordCardPRCWizard",
            WIZARD_FEATURE_NAME_SETTING: QCoreApplication.translate("CreatePropertyRecordCardPRCWizard", "property record card"),
            WIZARD_HELP_SETTING: "create_property_record_card",
            WIZARD_UI_SETTING: "wizards/property_record_card/wiz_create_property_record_card_prc.ui",
            WIZARD_QSETTINGS_SETTING: {
                WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM_COL/wizards/property_record_card_load_data_type"
            },
            WIZARD_HELP_PAGES_SETTING: {
                WIZARD_HELP_PAGE1: help_strings.WIZ_CREATE_PROPERTY_RECORD_CARD_PRC_PAGE_1_OPTION_FORM,
                WIZARD_HELP_PAGE2: ""
            },
            WIZARD_LAYERS_SETTING: {
                PROPERTY_RECORD_CARD_TABLE: {'name': PROPERTY_RECORD_CARD_TABLE, 'geometry': None, LAYER: None}
            },
            WIZARD_EDITING_LAYER_NAME_SETTING: PROPERTY_RECORD_CARD_TABLE,
            WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.NoGeometry
        }
    }
