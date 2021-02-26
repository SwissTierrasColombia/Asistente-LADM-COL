from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import QgsMapLayerProxyModel

from asistente_ladm_col.config.ladm_names import LADMNames
from asistente_ladm_col.config.general_config import (WIZARD_CLASS,
                                                      WIZARD_FEATURE_NAME,
                                                      WIZARD_UI,
                                                      WIZARD_HELP,
                                                      WIZARD_HELP_PAGES,
                                                      WIZARD_QSETTINGS,
                                                      WIZARD_QSETTINGS_LOAD_DATA_TYPE,
                                                      WIZARD_QSETTINGS_LOAD_CONVENTION_TYPE,
                                                      WIZARD_QSETTINGS_TYPE_PARCEL_SELECTED,
                                                      WIZARD_TOOL_NAME,
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
                                                      WIZARD_CREATE_ADMINISTRATIVE_SOURCE_SURVEY,
                                                      WIZARD_CREATE_BOUNDARY_SURVEY,
                                                      WIZARD_CREATE_BUILDING_SURVEY,
                                                      WIZARD_CREATE_BUILDING_UNIT_SURVEY,
                                                      WIZARD_CREATE_RIGHT_SURVEY,
                                                      WIZARD_CREATE_RESTRICTION_SURVEY,
                                                      WIZARD_CREATE_SPATIAL_SOURCE_SURVEY,
                                                      WIZARD_CREATE_PARCEL_SURVEY,
                                                      WIZARD_CREATE_PLOT_SURVEY,
                                                      WIZARD_CREATE_EXT_ADDRESS_SURVEY,
                                                      WIZARD_CREATE_RIGHT_OF_WAY_SURVEY,
                                                      WIZARD_CREATE_GEOECONOMIC_ZONE_VALUATION,
                                                      WIZARD_CREATE_PHYSICAL_ZONE_VALUATION,
                                                      WIZARD_CREATE_BUILDING_UNIT_VALUATION,
                                                      WIZARD_CREATE_BUILDING_UNIT_QUALIFICATION_VALUATION,
                                                      WIZARD_STRINGS, WIZARD_SEL_SOURCE_TITLE,
                                                      WIZARD_SEL_SOURCE_ENTERING_DATA_MANUALLY)

from asistente_ladm_col.config.enums import EnumWizardType
# from asistente_ladm_col.gui.wizards.survey.wiz_create_parcel_survey import CreateParcelSurveyWizard
# from asistente_ladm_col.gui.wizards.survey.wiz_create_rrr_survey import CreateRRRSurveyWizard
from asistente_ladm_col.config.help_strings import HelpStrings
from asistente_ladm_col.gui.wizards.survey.wiz_create_spatial_source_survey import CreateSpatialSourceSurveyWizard
# from asistente_ladm_col.gui.wizards.survey.wiz_create_ext_address_survey import CreateExtAddressSurveyWizard
# from asistente_ladm_col.gui.wizards.survey.wiz_create_plot_survey import CreatePlotSurveyWizard
from asistente_ladm_col.gui.wizards.survey.wiz_create_right_of_way_survey import CreateRightOfWaySurveyWizard
# from asistente_ladm_col.gui.wizards.single_page_spatial_wizard_factory import SinglePageSpatialWizardFactory
# from asistente_ladm_col.gui.wizards.single_page_wizard_factory import SinglePageWizardFactory
from asistente_ladm_col.gui.wizards.valuation.wiz_create_building_unit_qualification_valuation import CreateBuildingUnitQualificationValuationWizard
# from asistente_ladm_col.gui.wizards.valuation.wiz_create_building_unit_valuation import CreateBuildingUnitValuationWizard

from asistente_ladm_col.gui.wizards.wizard3.create_building_unit_valuation import CreateBuildingUnitValuationWizard
from asistente_ladm_col.gui.wizards.wizard3.create_parcel_survey import CreateParcelSurveyWizard
from asistente_ladm_col.gui.wizards.wizard3.create_plot_survey import CreatePlotSurveyWizard
from asistente_ladm_col.gui.wizards.wizard3.create_rrr_survey import CreateRRRSurveyWizard

from asistente_ladm_col.gui.wizards.wizard3.create_spatial_source_survey import CreateSpatialSourceSurveyWizard

from asistente_ladm_col.gui.wizards.wizard3.single_page_spatial_wizard_factory import SinglePageSpatialWizardFactory
from asistente_ladm_col.gui.wizards.wizard3.single_page_wizard_factory import SinglePageWizardFactory
from asistente_ladm_col.gui.wizards.wizard3.create_ext_address_survey import CreateExtAddressSurveyWizard

help_strings = HelpStrings()


class WizardConfig:

    def __init__(self):
        pass

    def get_wizard_config(self, names, wizard_config_name):
        if wizard_config_name == WIZARD_CREATE_COL_PARTY_CADASTRAL:
            return {
                WIZARD_TYPE: EnumWizardType.SINGLE_PAGE_WIZARD_TYPE,
                WIZARD_CLASS: SinglePageWizardFactory,
                WIZARD_FEATURE_NAME: QCoreApplication.translate("CreateColPartySurveyWizard", "party"),
                WIZARD_TOOL_NAME: QCoreApplication.translate("CreateColPartySurveyWizard", "Create party"),
                WIZARD_HELP: "party",
                WIZARD_UI: "wizards/survey/wiz_create_col_party_survey.ui",
                WIZARD_QSETTINGS: {
                    WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM-COL/wizards/col_party_load_data_type"
                },
                WIZARD_HELP_PAGES: {
                    WIZARD_HELP1: help_strings.WIZ_CREATE_COL_PARTY_SURVEY_PAGE_1_OPTION_FORM,
                    WIZARD_HELP2: ""
                },
                WIZARD_STRINGS: {
                    WIZARD_SEL_SOURCE_TITLE: "How would you like to create parties?",  # TODO Translate
                    WIZARD_SEL_SOURCE_ENTERING_DATA_MANUALLY: "Entering data manually using a form"  # TODO Translate
                },
                WIZARD_LAYERS: {names.LC_PARTY_T: None},
                WIZARD_EDITING_LAYER_NAME: names.LC_PARTY_T,
                WIZARD_READ_ONLY_FIELDS: [names.COL_PARTY_T_NAME_F],
                WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.NoGeometry
            }
        elif wizard_config_name == WIZARD_CREATE_ADMINISTRATIVE_SOURCE_SURVEY:
            return {
                WIZARD_TYPE: EnumWizardType.SINGLE_PAGE_WIZARD_TYPE,
                WIZARD_CLASS: SinglePageWizardFactory,
                WIZARD_FEATURE_NAME: QCoreApplication.translate("CreateAdministrativeSourceSurveyWizard",
                                                                        "administrative source"),
                WIZARD_TOOL_NAME: QCoreApplication.translate("CreateAdministrativeSourceSurveyWizard",
                                                                        "Create administrative source"),
                WIZARD_HELP: "create_admin_source",
                WIZARD_UI: "wizards/survey/wiz_create_administrative_source_survey.ui",
                WIZARD_QSETTINGS: {
                    WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM-COL/wizards/administrative_source_load_data_type"
                },
                WIZARD_HELP_PAGES: {
                    WIZARD_HELP1: help_strings.WIZ_CREATE_ADMINISTRATIVE_SOURCE_PAGE_1_OPTION_FORM,
                    WIZARD_HELP2: ""
                },
                WIZARD_STRINGS: {
                    WIZARD_SEL_SOURCE_TITLE: "How would you like to create administrative sources?",  # TODO Translate
                    WIZARD_SEL_SOURCE_ENTERING_DATA_MANUALLY: "Entering data manually using a form"  # TODO Translate
                },
                WIZARD_LAYERS: {
                    names.LC_ADMINISTRATIVE_SOURCE_T: None,
                    names.EXT_ARCHIVE_S: None
                },
                WIZARD_EDITING_LAYER_NAME: names.LC_ADMINISTRATIVE_SOURCE_T,
                WIZARD_READ_ONLY_FIELDS: [],
                WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.NoGeometry
            }
        elif wizard_config_name == WIZARD_CREATE_BOUNDARY_SURVEY:
            return {
                WIZARD_TYPE: EnumWizardType.SINGLE_PAGE_SPATIAL_WIZARD_TYPE,
                WIZARD_CLASS: SinglePageSpatialWizardFactory,
                WIZARD_FEATURE_NAME: QCoreApplication.translate("CreateBoundarySurveyWizard", "boundary"),
                WIZARD_TOOL_NAME: QCoreApplication.translate("CreateBoundarySurveyWizard", "Create boundary"),
                WIZARD_HELP: "create_boundaries",
                WIZARD_UI: "wizards/survey/wiz_create_boundaries_survey.ui",
                WIZARD_QSETTINGS: {
                    WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM-COL/wizards/boundary_load_data_type"
                },
                WIZARD_HELP_PAGES: {
                    WIZARD_HELP1: help_strings.WIZ_DEFINE_BOUNDARIES_SURVEY_PAGE_1_OPTION_DIGITIZE,
                    WIZARD_HELP2: ""
                },
                WIZARD_LAYERS: {
                    names.LC_BOUNDARY_T: None,
                    names.LC_BOUNDARY_POINT_T: None
                },
                WIZARD_EDITING_LAYER_NAME: names.LC_BOUNDARY_T,
                WIZARD_READ_ONLY_FIELDS: [],
                WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.LineLayer
            }
        elif wizard_config_name == WIZARD_CREATE_BUILDING_SURVEY:
            return {
                WIZARD_TYPE: EnumWizardType.SINGLE_PAGE_SPATIAL_WIZARD_TYPE,
                WIZARD_CLASS: SinglePageSpatialWizardFactory,
                WIZARD_FEATURE_NAME: QCoreApplication.translate("CreateBuildingSurveyWizard", "building"),
                WIZARD_TOOL_NAME: QCoreApplication.translate("CreateBuildingSurveyWizard", "Create building"),
                WIZARD_HELP: "create_building",
                WIZARD_UI: "wizards/survey/wiz_create_building_survey.ui",
                WIZARD_QSETTINGS: {
                    WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM-COL/wizards/building_load_data_type"
                },
                WIZARD_HELP_PAGES: {
                    WIZARD_HELP1: help_strings.WIZ_CREATE_BUILDING_SURVEY_PAGE_1_OPTION_POINTS,
                    WIZARD_HELP2: ""
                },
                WIZARD_LAYERS: {
                    names.LC_BUILDING_T: None,
                    names.LC_SURVEY_POINT_T: None
                },
                WIZARD_EDITING_LAYER_NAME: names.LC_BUILDING_T,
                WIZARD_READ_ONLY_FIELDS: [],
                WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.PolygonLayer
            }
        elif wizard_config_name == WIZARD_CREATE_BUILDING_UNIT_SURVEY:
            return {
                WIZARD_TYPE: EnumWizardType.SINGLE_PAGE_SPATIAL_WIZARD_TYPE,
                WIZARD_CLASS: SinglePageSpatialWizardFactory,
                WIZARD_FEATURE_NAME: QCoreApplication.translate("CreateBuildingUnitSurveyWizard", "building unit"),
                WIZARD_TOOL_NAME: QCoreApplication.translate("CreateBuildingUnitSurveyWizard", "Create building unit"),
                WIZARD_HELP: "create_building_unit",
                WIZARD_UI: "wizards/survey/wiz_create_building_unit_survey.ui",
                WIZARD_QSETTINGS: {
                    WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM-COL/wizards/building_unit_load_data_type"
                },
                WIZARD_HELP_PAGES: {
                    WIZARD_HELP1: help_strings.WIZ_CREATE_BUILDING_UNIT_SURVEY_PAGE_1_OPTION_POINTS,
                    WIZARD_HELP2: ""
                },
                WIZARD_LAYERS: {
                    names.LC_BUILDING_UNIT_T: None,
                    names.LC_BUILDING_T: None,
                    names.LC_SURVEY_POINT_T: None
                },
                WIZARD_EDITING_LAYER_NAME: names.LC_BUILDING_UNIT_T,
                WIZARD_READ_ONLY_FIELDS: [],
                WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.PolygonLayer
            }
        elif wizard_config_name == WIZARD_CREATE_RIGHT_SURVEY:
            print('ok1')
            return {
                WIZARD_TYPE: EnumWizardType.MULTI_PAGE_WIZARD_TYPE,
                WIZARD_CLASS: CreateRRRSurveyWizard,
                WIZARD_FEATURE_NAME: QCoreApplication.translate("CreateRightSurveyWizard", "right"),
                WIZARD_TOOL_NAME: QCoreApplication.translate("CreateRightSurveyWizard", "Create right"),
                WIZARD_HELP: "create_right",
                WIZARD_UI: "wizards/wizard_pages/survey/wiz_create_right_survey.ui",
                WIZARD_QSETTINGS: {
                    WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM-COL/wizards/right_load_data_type"
                },
                WIZARD_HELP_PAGES: {
                    WIZARD_HELP1: help_strings.WIZ_CREATE_RIGHT_SURVEY_PAGE_1_OPTION_FORM,
                    WIZARD_HELP2: help_strings.WIZ_CREATE_RIGHT_SURVEY_PAGE_2
                },
                WIZARD_STRINGS: {
                    WIZARD_SEL_SOURCE_TITLE: "What source do you want to associate the right with?",  # TODO Translate
                    WIZARD_SEL_SOURCE_ENTERING_DATA_MANUALLY: "Entering data manually using a form"  # TODO Translate
                },
                WIZARD_LAYERS: {
                    names.LC_RIGHT_T: None,
                    names.LC_ADMINISTRATIVE_SOURCE_T: None,
                    names.COL_RRR_SOURCE_T: None
                },
                WIZARD_EDITING_LAYER_NAME: names.LC_RIGHT_T,
                WIZARD_READ_ONLY_FIELDS: [],
                WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.NoGeometry
            }
        elif wizard_config_name == WIZARD_CREATE_RESTRICTION_SURVEY:
            print('ok')
            return {
                WIZARD_TYPE: EnumWizardType.MULTI_PAGE_WIZARD_TYPE,
                WIZARD_CLASS: CreateRRRSurveyWizard,
                WIZARD_FEATURE_NAME: QCoreApplication.translate("CreateRestrictionSurveyWizard", "restriction"),
                WIZARD_TOOL_NAME: QCoreApplication.translate("CreateRestrictionSurveyWizard", "Create restriction"),
                WIZARD_HELP: "create_restriction",
                WIZARD_UI: "wizards/wizard_pages/survey/wiz_create_restriction_survey.ui",
                WIZARD_QSETTINGS: {
                    WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM-COL/wizards/restriction_load_data_type"
                },
                WIZARD_HELP_PAGES: {
                    WIZARD_HELP1: help_strings.WIZ_CREATE_RESTRICTION_SURVEY_PAGE_1_OPTION_FORM,
                    WIZARD_HELP2: help_strings.WIZ_CREATE_RESTRICTION_SURVEY_PAGE_2
                },
                WIZARD_STRINGS: {
                    WIZARD_SEL_SOURCE_TITLE: "How would you like to create restrictions?",  # TODO Translate
                    WIZARD_SEL_SOURCE_ENTERING_DATA_MANUALLY: "Entering data manually using a form"  # TODO Translate
                },
                WIZARD_LAYERS: {
                    names.LC_RESTRICTION_T: None,
                    names.LC_ADMINISTRATIVE_SOURCE_T: None,
                    names.COL_RRR_SOURCE_T: None
                },
                WIZARD_EDITING_LAYER_NAME: names.LC_RESTRICTION_T,
                WIZARD_READ_ONLY_FIELDS: [],
                WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.NoGeometry
            }
        elif wizard_config_name == WIZARD_CREATE_SPATIAL_SOURCE_SURVEY:
            return {
                WIZARD_TYPE: EnumWizardType.MULTI_PAGE_WIZARD_TYPE,
                WIZARD_CLASS: CreateSpatialSourceSurveyWizard,
                WIZARD_FEATURE_NAME: QCoreApplication.translate("CreateSpatialSourceSurveyWizard",
                                                                        "spatial source"),
                WIZARD_TOOL_NAME: QCoreApplication.translate("CreateSpatialSourceSurveyWizard",
                                                                                "Create spatial source"),
                WIZARD_HELP: "create_spatial_source",
                WIZARD_UI: "wizards/wizard_pages/survey/wiz_create_spatial_source_survey.ui",
                WIZARD_QSETTINGS: {
                    WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM-COL/wizards/spatial_source_load_data_type"
                },
                WIZARD_HELP_PAGES: {
                    WIZARD_HELP1: help_strings.WIZ_CREATE_SPATIAL_SOURCE_SURVEY_PAGE_1_OPTION_FORM,
                    WIZARD_HELP2: help_strings.WIZ_CREATE_SPATIAL_SOURCE_SURVEY_PAGE_2
                },
                WIZARD_STRINGS: {
                    WIZARD_SEL_SOURCE_TITLE: "How would you like to create spatial sources?",  # TODO Translate
                    WIZARD_SEL_SOURCE_ENTERING_DATA_MANUALLY: "Entering data manually using a form"  # TODO Translate
                },
                WIZARD_LAYERS: {
                    names.LC_SPATIAL_SOURCE_T: None,
                    names.EXT_ARCHIVE_S: None,
                    names.LC_PLOT_T: None,
                    names.COL_UE_SOURCE_T: None,
                    names.LC_BOUNDARY_T: None,
                    names.COL_CCL_SOURCE_T: None,
                    names.COL_POINT_SOURCE_T: None,
                    names.LC_BOUNDARY_POINT_T: None,
                    names.LC_SURVEY_POINT_T: None,
                    names.LC_CONTROL_POINT_T: None
                },
                WIZARD_EDITING_LAYER_NAME: names.LC_SPATIAL_SOURCE_T,
                WIZARD_READ_ONLY_FIELDS: [],
                WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.NoGeometry
            }
        elif wizard_config_name == WIZARD_CREATE_PARCEL_SURVEY:
            return {
                WIZARD_TYPE: EnumWizardType.MULTI_PAGE_WIZARD_TYPE,
                WIZARD_CLASS: CreateParcelSurveyWizard,
                WIZARD_FEATURE_NAME: QCoreApplication.translate("CreateParcelSurveyWizard", "parcel"),
                WIZARD_TOOL_NAME: QCoreApplication.translate("CreateParcelSurveyWizard", "Create parcel"),
                WIZARD_HELP: "create_parcel",
                WIZARD_UI: "wizards/wizard_pages/survey/wiz_create_parcel_survey.ui",
                WIZARD_QSETTINGS: {
                    WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM-COL/wizards/parcel_load_data_type",
                    WIZARD_QSETTINGS_TYPE_PARCEL_SELECTED: "Asistente-LADM-COL/wizards/type_of_parcel_selected"
                },
                WIZARD_HELP_PAGES: {
                    WIZARD_HELP1: help_strings.WIZ_CREATE_PARCEL_SURVEY_PAGE_1_OPTION_EXISTING_PLOT,
                    WIZARD_HELP2: help_strings.WIZ_CREATE_PARCEL_SURVEY_PAGE_2
                },
                WIZARD_STRINGS: {
                    WIZARD_SEL_SOURCE_TITLE: "How would you like to create parcels?",  # TODO Translate
                    WIZARD_SEL_SOURCE_ENTERING_DATA_MANUALLY: "Entering data manually using a form"  # TODO Translate
                },
                WIZARD_LAYERS: {
                    names.LC_PLOT_T: None,
                    names.LC_PARCEL_T: None,
                    names.LC_RIGHT_T: None,
                    names.LC_BUILDING_T: None,
                    names.LC_BUILDING_UNIT_T: None,
                    names.COL_UE_BAUNIT_T: None,
                    names.LC_CONDITION_PARCEL_TYPE_D: None,
                    names.EXT_ADDRESS_S: None
                },
                WIZARD_EDITING_LAYER_NAME: names.LC_PARCEL_T,
                WIZARD_READ_ONLY_FIELDS: [names.LC_PARCEL_T_PARCEL_TYPE_F],
                WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.NoGeometry
            }
        elif wizard_config_name == WIZARD_CREATE_PLOT_SURVEY:
            return {
                WIZARD_TYPE: EnumWizardType.MULTI_PAGE_WIZARD_TYPE,
                WIZARD_CLASS: CreatePlotSurveyWizard,
                WIZARD_FEATURE_NAME: QCoreApplication.translate("CreatePlotSurveyWizard", "plot"),
                WIZARD_TOOL_NAME: QCoreApplication.translate("CreatePlotSurveyWizard", "Create plot"),
                WIZARD_HELP: "create_plot",
                WIZARD_UI: "wizards/wizard_pages/survey/wiz_create_plot_survey.ui",
                WIZARD_QSETTINGS: {
                    WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM-COL/wizards/plot_load_data_type"
                },
                WIZARD_HELP_PAGES: {
                    WIZARD_HELP1: help_strings.WIZ_CREATE_PLOT_SURVEY_PAGE_1_OPTION_BOUNDARIES,
                    WIZARD_HELP2: help_strings.WIZ_CREATE_PLOT_SURVEY_PAGE_2
                },
                WIZARD_STRINGS: {
                    WIZARD_SEL_SOURCE_TITLE: "How would you like to create plots?",  # TODO Translate
                    WIZARD_SEL_SOURCE_ENTERING_DATA_MANUALLY: "Selecting existing boundaries"  # TODO Translate
                },
                WIZARD_LAYERS: {
                    names.LC_PLOT_T: None,
                    names.LC_BOUNDARY_T: None
                },
                WIZARD_EDITING_LAYER_NAME: names.LC_PLOT_T,
                WIZARD_READ_ONLY_FIELDS: [],
                WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.PolygonLayer
            }
        elif wizard_config_name == WIZARD_CREATE_EXT_ADDRESS_SURVEY:
            return {
                WIZARD_TYPE: EnumWizardType.MULTI_PAGE_SPATIAL_WIZARD_TYPE,
                WIZARD_CLASS: CreateExtAddressSurveyWizard,
                WIZARD_FEATURE_NAME: QCoreApplication.translate("CreateExtAddressSurveyWizard", "ext address"),
                WIZARD_TOOL_NAME: QCoreApplication.translate("CreateExtAddressSurveyWizard", "Create ext address"),
                WIZARD_HELP: "associate_ext_address",
                WIZARD_UI: "wizards/wizard_pages/survey/wiz_associate_extaddress_survey.ui",
                WIZARD_QSETTINGS: {
                    WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM-COL/wizards/ext_address_load_data_type"
                },
                WIZARD_HELP_PAGES: {
                    WIZARD_HELP1: help_strings.WIZ_ASSOCIATE_EXTADDRESS_SURVEY_PAGE_2_OPTION_1,
                    WIZARD_HELP2: help_strings.WIZ_ASSOCIATE_EXTADDRESS_SURVEY_PAGE_2_OPTION_2,
                    WIZARD_HELP3: help_strings.WIZ_ASSOCIATE_EXTADDRESS_SURVEY_PAGE_2_OPTION_3
                },
                WIZARD_STRINGS: {
                    WIZARD_SEL_SOURCE_TITLE: "How would you like to create and associate addresses?",  # TODO Translate
                    WIZARD_SEL_SOURCE_ENTERING_DATA_MANUALLY: "Entering data manually using a form"  # TODO Translate
                },
                WIZARD_LAYERS: {
                    names.EXT_ADDRESS_S: None,
                    names.LC_PLOT_T: None,
                    names.LC_BUILDING_T: None,
                    names.LC_BUILDING_UNIT_T: None
                },
                WIZARD_EDITING_LAYER_NAME: names.EXT_ADDRESS_S,
                WIZARD_READ_ONLY_FIELDS: [],
                WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.PointLayer
            }
        elif wizard_config_name == WIZARD_CREATE_RIGHT_OF_WAY_SURVEY:
            return {
                WIZARD_TYPE: EnumWizardType.SINGLE_PAGE_SPATIAL_WIZARD_TYPE,
                WIZARD_CLASS: CreateRightOfWaySurveyWizard,
                WIZARD_FEATURE_NAME: QCoreApplication.translate("CreateRightOfWaySurveyWizard", "right of way"),
                WIZARD_TOOL_NAME: QCoreApplication.translate("CreateRightOfWaySurveyWizard", "Create right of way"),
                WIZARD_HELP: "create_right_of_way",
                WIZARD_UI: "wizards/survey/wiz_create_right_of_way_survey.ui",
                WIZARD_QSETTINGS: {
                    WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM-COL/wizards/right_of_way_load_data_type"
                },
                WIZARD_HELP_PAGES: {
                    WIZARD_HELP1: help_strings.WIZ_CREATE_RIGHT_OF_WAY_SURVEY_PAGE_1_OPTION_POINTS,
                    WIZARD_HELP2: help_strings.WIZ_CREATE_RIGHT_OF_WAY_SURVEY_PAGE_1_OPTION2_POINTS,
                    WIZARD_HELP3: help_strings.WIZ_ASSOCIATE_EXTADDRESS_SURVEY_PAGE_2_OPTION_2,
                    WIZARD_HELP4: help_strings.WIZ_ASSOCIATE_EXTADDRESS_SURVEY_PAGE_2_OPTION_3
                },
                WIZARD_LAYERS: {
                    names.LC_RIGHT_OF_WAY_T: None,
                    names.LC_PLOT_T: None,
                    names.LC_SURVEY_POINT_T: None
                },
                WIZARD_EDITING_LAYER_NAME: names.LC_RIGHT_OF_WAY_T,
                WIZARD_READ_ONLY_FIELDS: [],
                WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.PolygonLayer
            }
        elif wizard_config_name == WIZARD_CREATE_GEOECONOMIC_ZONE_VALUATION:
            return {
                WIZARD_TYPE: EnumWizardType.SINGLE_PAGE_SPATIAL_WIZARD_TYPE,
                WIZARD_CLASS: SinglePageSpatialWizardFactory,
                WIZARD_FEATURE_NAME: QCoreApplication.translate("CreateGeoeconomicZoneValuationWizard",
                                                                        "geoeconomic zone"),
                WIZARD_TOOL_NAME: QCoreApplication.translate("CreateGeoeconomicZoneValuationWizard",
                                                                        "Create geoeconomic zone"),
                WIZARD_HELP: "",
                WIZARD_UI: "wizards/valuation/wiz_create_geoeconomic_zone_valuation.ui",
                WIZARD_QSETTINGS: {
                    WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM-COL/wizards/geoeconomic_zone_valuation_load_data_type"
                },
                WIZARD_HELP_PAGES: {
                    WIZARD_HELP1: help_strings.WIZ_CREATE_GEOECONOMIC_ZONE_VALUATION_PAGE_1_OPTION_FORM,
                    WIZARD_HELP2: ""
                },
                WIZARD_LAYERS: {LADMNames.VALUATION_GEOECONOMIC_ZONE_TABLE: None},
                WIZARD_EDITING_LAYER_NAME: LADMNames.VALUATION_GEOECONOMIC_ZONE_TABLE,
                WIZARD_READ_ONLY_FIELDS: [],
                WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.PolygonLayer
            }
        elif wizard_config_name == WIZARD_CREATE_PHYSICAL_ZONE_VALUATION:
            return {
                WIZARD_TYPE: EnumWizardType.SINGLE_PAGE_SPATIAL_WIZARD_TYPE,
                WIZARD_CLASS: SinglePageSpatialWizardFactory,
                WIZARD_FEATURE_NAME: QCoreApplication.translate("CreatePhysicalZoneValuationWizard", "physical zone"),
                WIZARD_TOOL_NAME: QCoreApplication.translate("CreatePhysicalZoneValuationWizard", "Create physical zone"),
                WIZARD_HELP: "",
                WIZARD_UI: "wizards/valuation/wiz_create_physical_zone_valuation.ui",
                WIZARD_QSETTINGS: {
                    WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM-COL/wizards/physical_zone_valuation_load_data_type"
                },
                WIZARD_HELP_PAGES: {
                    WIZARD_HELP1: help_strings.WIZ_CREATE_PHYSICAL_ZONE_VALUATION_PAGE_1_OPTION_FORM,
                    WIZARD_HELP2: ""
                },
                WIZARD_LAYERS: {LADMNames.VALUATION_PHYSICAL_ZONE_TABLE: None},
                WIZARD_EDITING_LAYER_NAME: LADMNames.VALUATION_PHYSICAL_ZONE_TABLE,
                WIZARD_READ_ONLY_FIELDS: [],
                WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.PolygonLayer
            }
        elif wizard_config_name == WIZARD_CREATE_BUILDING_UNIT_VALUATION:
            return {
                WIZARD_TYPE: EnumWizardType.MULTI_PAGE_WIZARD_TYPE,
                WIZARD_CLASS: CreateBuildingUnitValuationWizard,
                WIZARD_FEATURE_NAME: QCoreApplication.translate("CreateBuildingUnitValuationWizard",
                                                                        "building unit valuation"),
                WIZARD_TOOL_NAME: QCoreApplication.translate("CreateBuildingUnitValuationWizard",
                                                                        "Create building unit valuation"),
                WIZARD_HELP: "",
                WIZARD_UI: "wizards/valuation/wiz_create_building_unit_valuation.ui",
                WIZARD_QSETTINGS: {
                    WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM-COL/wizards/valuation_building_unit_load_data_type"
                },
                WIZARD_HELP_PAGES: {
                    WIZARD_HELP1: help_strings.WIZ_CREATE_BUILDING_UNIT_VALUATION_PAGE_1_OPTION_FORM,
                    WIZARD_HELP2: help_strings.WIZ_CREATE_BUILDING_UNIT_VALUATION_PAGE_2
                },
                WIZARD_LAYERS: {
                    LADMNames.VALUATION_BUILDING_UNIT_TABLE: None,
                    names.LC_BUILDING_UNIT_T: None,
                    LADMNames.AVALUOUNIDADCONSTRUCCION_TABLE: None
                },
                WIZARD_EDITING_LAYER_NAME: LADMNames.VALUATION_BUILDING_UNIT_TABLE,
                WIZARD_READ_ONLY_FIELDS: [],
                WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.NoGeometry
            }
        elif wizard_config_name == WIZARD_CREATE_BUILDING_UNIT_QUALIFICATION_VALUATION:
            return {
                WIZARD_TYPE: EnumWizardType.MULTI_PAGE_WIZARD_TYPE,
                WIZARD_CLASS: CreateBuildingUnitQualificationValuationWizard,
                WIZARD_FEATURE_NAME: QCoreApplication.translate("CreateBuildingUnitQualificationValuationWizard",
                                                                        "building unit qualification valuation"),
                WIZARD_TOOL_NAME: QCoreApplication.translate("CreateBuildingUnitQualificationValuationWizard",
                                                                        "Create building unit qualification valuation"),
                WIZARD_HELP: "",
                WIZARD_UI: "wizards/valuation/wiz_create_building_unit_qualification_valuation.ui",
                WIZARD_QSETTINGS: {
                    WIZARD_QSETTINGS_LOAD_DATA_TYPE: "Asistente-LADM-COL/wizards/building_unit_qualification_load_data_type",
                    WIZARD_QSETTINGS_LOAD_CONVENTION_TYPE: "Asistente-LADM-COL/wizards/building_unit_qualification_load_convention_type"
                },
                WIZARD_HELP_PAGES: {
                    WIZARD_HELP1: help_strings.WIZ_ADD_POINTS_SURVEY_PAGE_2_OPTION_CSV,
                    WIZARD_HELP2: help_strings.WIZ_USING_FORM_BUILDING_UNIT_QUALIFICATION_PAGE_2_OPTION,
                    WIZARD_HELP3: help_strings.WIZ_USING_FORM_BUILDING_UNIT_NO_QUALIFICATION_PAGE_2_OPTION,
                    WIZARD_HELP4: help_strings.WIZ_CREATE_BUILDING_UNIT_QUALIFICATION_CONVENTIONAL_VALUATION_PAGE_1_OPTION_FORM,
                    WIZARD_HELP5: help_strings.WIZ_CREATE_BUILDING_UNIT_QUALIFICATION_NO_CONVENTIONAL_VALUATION_PAGE_1_OPTION_FORM
                },
                WIZARD_LAYERS: {
                    LADMNames.VALUATION_BUILDING_UNIT_QUALIFICATION_NO_CONVENTIONAL_TABLE: None,
                    LADMNames.VALUATION_BUILDING_UNIT_QUALIFICATION_CONVENTIONAL_TABLE: None
                },
                WIZARD_EDITING_LAYER_NAME: LADMNames.VALUATION_BUILDING_UNIT_QUALIFICATION_CONVENTIONAL_TABLE,
                WIZARD_READ_ONLY_FIELDS: [],
                WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.NoGeometry
            }
