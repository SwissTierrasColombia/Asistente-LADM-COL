from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import QgsMapLayerProxyModel

from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.config.general_config import (WIZARD_FEATURE_NAME,
                                                      WIZARD_HELP,
                                                      WIZARD_HELP_PAGES,
                                                      WIZARD_QSETTINGS,
                                                      WIZARD_TOOL_NAME,
                                                      WIZARD_HELP1,
                                                      WIZARD_HELP2,
                                                      WIZARD_HELP3,
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
                                                      WIZARD_STRINGS, WIZARD_SEL_SOURCE_TITLE,
                                                      WIZARD_SEL_SOURCE_ENTERING_DATA_MANUALLY,
                                                      WIZARD_SEL_FEATURES_TITLE,
                                                      WIZARD_QSETTINGS_PATH)

from asistente_ladm_col.config.help_strings import HelpStrings
from asistente_ladm_col.gui.wizards.new_implementation.SingleController import SingleController
from asistente_ladm_col.gui.wizards.controller.parcel_controller import ParcelController
from asistente_ladm_col.gui.wizards.controller.plot_controller import PlotController
from asistente_ladm_col.gui.wizards.controller.right_of_way_controller import RightOfWayController
from asistente_ladm_col.gui.wizards.controller.ext_address_controller import ExtAddressController

from asistente_ladm_col.gui.wizards.controller.rrr_controller import RrrController
from asistente_ladm_col.gui.wizards.controller.single_spatial_wizard_controller import SingleSpatialWizardController
from asistente_ladm_col.gui.wizards.controller.spatial_source_controller import SpatialSourceController
from asistente_ladm_col.gui.wizards.model.plot_model import PlotModel
from asistente_ladm_col.gui.wizards.model.right_of_way_model import RightOfWayModel
from asistente_ladm_col.gui.wizards.model.ext_address_model import ExtAddressModel
from asistente_ladm_col.gui.wizards.model.rrr_model import RrrModel
from asistente_ladm_col.gui.wizards.model.single_spatial_wizard_model import SingleSpatialWizardModel
from asistente_ladm_col.gui.wizards.model.spatial_source_model import SpatialSourceModel

help_strings = HelpStrings()


class WizardFactory:

    def __init__(self):
        self.app = AppInterface()

    def get_wizard(self, iface, db, wizard_name, observer):
        wizard_config_factory = WizardConfigFactory()

        wizard_config = wizard_config_factory.get_wizard_config(db, wizard_name)

        wizard_result = None

        if wizard_name == WIZARD_CREATE_COL_PARTY_CADASTRAL or wizard_name == WIZARD_CREATE_ADMINISTRATIVE_SOURCE_SURVEY:
            wizard_result = SingleController(iface, db, wizard_config)

        elif wizard_name == WIZARD_CREATE_BOUNDARY_SURVEY or wizard_name == WIZARD_CREATE_BUILDING_SURVEY or \
                wizard_name == WIZARD_CREATE_BUILDING_UNIT_SURVEY:
            model = SingleSpatialWizardModel(iface, db, wizard_config)
            wizard_result = SingleSpatialWizardController(model, iface, db, wizard_config)

            self.__connect_spatial_signals(wizard_result, model, observer)

        elif wizard_name == WIZARD_CREATE_RIGHT_OF_WAY_SURVEY:
            model = RightOfWayModel(iface, db, wizard_config)
            wizard_result = RightOfWayController(model, iface, db, wizard_config)
            self.__connect_spatial_signals(wizard_result, model, observer)

        elif wizard_name == WIZARD_CREATE_SPATIAL_SOURCE_SURVEY:
            model = SpatialSourceModel(iface, db, wizard_config)
            wizard_result = SpatialSourceController(model, db, wizard_config)

        elif wizard_name == WIZARD_CREATE_RIGHT_SURVEY or wizard_name == WIZARD_CREATE_RESTRICTION_SURVEY:
            model = RrrModel(iface, db, wizard_config)
            wizard_result = RrrController(model, db, wizard_config)

        elif wizard_name == WIZARD_CREATE_EXT_ADDRESS_SURVEY:
            model = ExtAddressModel(iface, db, wizard_config)
            wizard_result = ExtAddressController(model, iface, db, wizard_config)
            self.__connect_spatial_signals(wizard_result, model, observer)

        elif wizard_name == WIZARD_CREATE_PLOT_SURVEY:
            model = PlotModel(iface, db, wizard_config)
            wizard_result = PlotController(model, db, wizard_config)

        elif wizard_name == WIZARD_CREATE_PARCEL_SURVEY:
            wizard_result = ParcelController(iface, db, wizard_config)

        self.__connect_signals(wizard_result, observer)

        return wizard_result

    @staticmethod
    def __connect_spatial_signals(wizard, model, observer):
        # Required signal for wizard geometry creating
        wizard.enable_save_geometry_button.connect(
            observer.set_enable_finalize_geometry_creation_action)
        observer.wiz_geometry_creation_finished.connect(model.save_created_geometry)

    @staticmethod
    def __connect_signals(wizard, observer):
        # Required signal that allow to know if there is a wizard opened
        wizard.update_wizard_is_open_flag.connect(observer.set_wizard_is_open_flag)


class WizardConfigFactory:

    def __init__(self):
        self.app = AppInterface()

    def get_wizard_config(self, db, wizard_config_name):
        names = db.names
        wizard_config = None

        if wizard_config_name == WIZARD_CREATE_COL_PARTY_CADASTRAL:
            wizard_config = {
                # MODEL
                WIZARD_LAYERS: {names.LC_PARTY_T: None},
                WIZARD_EDITING_LAYER_NAME: names.LC_PARTY_T,
                WIZARD_FEATURE_NAME: QCoreApplication.translate("CreateColPartySurveyWizard", "party"),
                WIZARD_READ_ONLY_FIELDS: [names.COL_PARTY_T_NAME_F],
                # VIEW / CONTROLLER?
                WIZARD_QSETTINGS: {
                    WIZARD_QSETTINGS_PATH: "wizards/col_party"
                },
                WIZARD_TOOL_NAME: QCoreApplication.translate("CreateColPartySurveyWizard", "Create party"),
                # VIEW
                WIZARD_HELP: "party",
                WIZARD_HELP_PAGES: {
                    WIZARD_HELP1: help_strings.WIZ_CREATE_COL_PARTY_SURVEY_PAGE_1_OPTION_FORM,
                    WIZARD_HELP2: ""
                },
                WIZARD_STRINGS: {
                    WIZARD_SEL_SOURCE_TITLE: "How would you like to create parties?",  # TODO Translate
                    WIZARD_SEL_SOURCE_ENTERING_DATA_MANUALLY: "Entering data manually using a form"  # TODO Translate
                }
            }
        elif wizard_config_name == WIZARD_CREATE_ADMINISTRATIVE_SOURCE_SURVEY:
            wizard_config = {
                # MODEL
                WIZARD_LAYERS: {
                    names.LC_ADMINISTRATIVE_SOURCE_T: None,
                    names.EXT_ARCHIVE_S: None
                },
                WIZARD_EDITING_LAYER_NAME: names.LC_ADMINISTRATIVE_SOURCE_T,
                WIZARD_FEATURE_NAME: QCoreApplication.translate("CreateAdministrativeSourceSurveyWizard",
                                                                "administrative source"),
                WIZARD_READ_ONLY_FIELDS: [],
                # VIEW / CONTROLLER?
                WIZARD_QSETTINGS: {
                    WIZARD_QSETTINGS_PATH: "wizards/administrative_source"
                },
                # VIEW
                WIZARD_TOOL_NAME: QCoreApplication.translate("CreateAdministrativeSourceSurveyWizard",
                                                             "Create administrative source"),  # VIEW
                WIZARD_HELP: "create_admin_source",
                WIZARD_HELP_PAGES: {
                    WIZARD_HELP1: help_strings.WIZ_CREATE_ADMINISTRATIVE_SOURCE_PAGE_1_OPTION_FORM,
                    WIZARD_HELP2: ""
                },
                WIZARD_STRINGS: {
                    WIZARD_SEL_SOURCE_TITLE: "How would you like to create administrative sources?",  # TODO Translate
                    WIZARD_SEL_SOURCE_ENTERING_DATA_MANUALLY: "Entering data manually using a form"  # TODO Translate
                }
            }
        elif wizard_config_name == WIZARD_CREATE_BOUNDARY_SURVEY:
            wizard_config = {
                # MODEL
                WIZARD_LAYERS: {
                    names.LC_BOUNDARY_T: None,
                    names.LC_BOUNDARY_POINT_T: None
                },
                WIZARD_EDITING_LAYER_NAME: names.LC_BOUNDARY_T,
                WIZARD_FEATURE_NAME: QCoreApplication.translate("CreateBoundarySurveyWizard", "boundary"),
                WIZARD_READ_ONLY_FIELDS: [],
                # VIEW / CONTROLLER?
                WIZARD_QSETTINGS: {
                    WIZARD_QSETTINGS_PATH: "wizards/boundary"
                },
                WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.LineLayer,
                # VIEW
                WIZARD_TOOL_NAME: QCoreApplication.translate("CreateBoundarySurveyWizard", "Create boundary"), # VIEW
                WIZARD_HELP: "create_boundaries",
                WIZARD_HELP_PAGES: {
                    WIZARD_HELP1: help_strings.WIZ_DEFINE_BOUNDARIES_SURVEY_PAGE_1_OPTION_DIGITIZE,
                    WIZARD_HELP2: ""
                },
                WIZARD_STRINGS: {
                    WIZARD_SEL_SOURCE_TITLE: "How would you like to create boundaries?",  # TODO Translate
                    WIZARD_SEL_SOURCE_ENTERING_DATA_MANUALLY: "Digitizing"  # TODO Translate
                }
            }
        elif wizard_config_name == WIZARD_CREATE_BUILDING_SURVEY:
            wizard_config = {
                # MODEL
                WIZARD_LAYERS: {
                    names.LC_BUILDING_T: None,
                    names.LC_SURVEY_POINT_T: None
                },
                WIZARD_EDITING_LAYER_NAME: names.LC_BUILDING_T,
                WIZARD_FEATURE_NAME: QCoreApplication.translate("CreateBuildingSurveyWizard", "building"),
                WIZARD_READ_ONLY_FIELDS: [],
                # VIEW / CONTROLLER?
                WIZARD_QSETTINGS: {
                    WIZARD_QSETTINGS_PATH: "wizards/building"
                },
                WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.PolygonLayer,
                # VIEW
                WIZARD_TOOL_NAME: QCoreApplication.translate("CreateBuildingSurveyWizard", "Create building"),
                WIZARD_HELP: "create_building",
                WIZARD_HELP_PAGES: {
                    WIZARD_HELP1: help_strings.WIZ_CREATE_BUILDING_SURVEY_PAGE_1_OPTION_POINTS,
                    WIZARD_HELP2: ""
                },
                WIZARD_STRINGS: {
                    WIZARD_SEL_SOURCE_TITLE: "How would you like to create buildings?",  # TODO Translate
                    WIZARD_SEL_SOURCE_ENTERING_DATA_MANUALLY: "Digitizing"  # TODO Translate
                }
            }
        elif wizard_config_name == WIZARD_CREATE_BUILDING_UNIT_SURVEY:
            wizard_config = {
                # MODEL
                WIZARD_LAYERS: {
                    names.LC_BUILDING_UNIT_T: None,
                    names.LC_BUILDING_T: None,
                    names.LC_SURVEY_POINT_T: None
                },
                WIZARD_EDITING_LAYER_NAME: names.LC_BUILDING_UNIT_T,
                WIZARD_FEATURE_NAME: QCoreApplication.translate("CreateBuildingUnitSurveyWizard", "building unit"),
                WIZARD_READ_ONLY_FIELDS: [],
                # VIEW / CONTROLLER?
                WIZARD_QSETTINGS: {
                    WIZARD_QSETTINGS_PATH: "wizards/building_unit"
                },
                WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.PolygonLayer,
                # VIEW
                WIZARD_TOOL_NAME: QCoreApplication.translate("CreateBuildingUnitSurveyWizard", "Create building unit"),
                WIZARD_HELP: "create_building_unit",
                WIZARD_HELP_PAGES: {
                    WIZARD_HELP1: help_strings.WIZ_CREATE_BUILDING_UNIT_SURVEY_PAGE_1_OPTION_POINTS,
                    WIZARD_HELP2: ""
                },
                WIZARD_STRINGS: {
                    WIZARD_SEL_SOURCE_TITLE: "How would you like to create building units?",  # TODO Translate
                    WIZARD_SEL_SOURCE_ENTERING_DATA_MANUALLY: "Digitizing"  # TODO Translate
                }
            }
        elif wizard_config_name == WIZARD_CREATE_RIGHT_OF_WAY_SURVEY:
            wizard_config = {
                # MODEL
                WIZARD_LAYERS: {
                    names.LC_RIGHT_OF_WAY_T: None,
                    names.LC_PLOT_T: None,
                    names.LC_SURVEY_POINT_T: None
                },
                WIZARD_EDITING_LAYER_NAME: names.LC_RIGHT_OF_WAY_T,
                WIZARD_FEATURE_NAME: QCoreApplication.translate("CreateRightOfWaySurveyWizard", "right of way"),
                WIZARD_READ_ONLY_FIELDS: [],
                # VIEW / CONTROLLER?
                WIZARD_QSETTINGS: {
                    WIZARD_QSETTINGS_PATH: "wizards/right_of_way"
                },
                WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.PolygonLayer,
                # VIEW
                WIZARD_TOOL_NAME: QCoreApplication.translate("CreateRightOfWaySurveyWizard", "Create right of way"),
                WIZARD_HELP: "create_right_of_way",
                WIZARD_HELP_PAGES: {
                    WIZARD_HELP1: help_strings.WIZ_CREATE_RIGHT_OF_WAY_SURVEY_PAGE_1_OPTION_POINTS,
                    WIZARD_HELP2: help_strings.WIZ_CREATE_RIGHT_OF_WAY_SURVEY_PAGE_1_OPTION2_POINTS
                },
                WIZARD_STRINGS: {
                    WIZARD_SEL_SOURCE_TITLE: "How would you like to create and associate addresses?",  # TODO Translate
                    WIZARD_SEL_SOURCE_ENTERING_DATA_MANUALLY: "Entering data manually using a form"  # TODO Translate
                }
            }
        elif wizard_config_name == WIZARD_CREATE_SPATIAL_SOURCE_SURVEY:
            wizard_config = {
                # MODEL
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
                WIZARD_FEATURE_NAME: QCoreApplication.translate("CreateSpatialSourceSurveyWizard","spatial source"),
                WIZARD_READ_ONLY_FIELDS: [],
                # VIEW / CONTROLLER?
                WIZARD_QSETTINGS: {
                    WIZARD_QSETTINGS_PATH: "wizards/spatial_source"
                },
                WIZARD_TOOL_NAME: QCoreApplication.translate("CreateSpatialSourceSurveyWizard", "Create spatial source"),
                # VIEW
                WIZARD_HELP: "create_spatial_source",
                WIZARD_HELP_PAGES: {
                    WIZARD_HELP1: help_strings.WIZ_CREATE_SPATIAL_SOURCE_SURVEY_PAGE_1_OPTION_FORM,
                    WIZARD_HELP2: help_strings.WIZ_CREATE_SPATIAL_SOURCE_SURVEY_PAGE_2
                },
                WIZARD_STRINGS: {
                    WIZARD_SEL_SOURCE_TITLE: "How would you like to create spatial sources?",  # TODO Translate
                    WIZARD_SEL_SOURCE_ENTERING_DATA_MANUALLY: "Entering data manually using a form"  # TODO Translate
                }
            }
        elif wizard_config_name == WIZARD_CREATE_RIGHT_SURVEY:
            wizard_config = {
                # MODEL
                WIZARD_LAYERS: {
                    names.LC_RIGHT_T: None,
                    names.LC_ADMINISTRATIVE_SOURCE_T: None,
                    names.COL_RRR_SOURCE_T: None
                },
                WIZARD_EDITING_LAYER_NAME: names.LC_RIGHT_T,
                WIZARD_FEATURE_NAME: QCoreApplication.translate("CreateRightSurveyWizard", "right"),
                WIZARD_READ_ONLY_FIELDS: [],
                # VIEW / CONTROLLER?
                WIZARD_QSETTINGS: {
                    WIZARD_QSETTINGS_PATH: "wizards/right"
                },
                WIZARD_TOOL_NAME: QCoreApplication.translate("CreateRightSurveyWizard", "Create right"),
                # VIEW
                WIZARD_HELP: "create_right",
                WIZARD_HELP_PAGES: {
                    WIZARD_HELP1: help_strings.WIZ_CREATE_RIGHT_SURVEY_PAGE_1_OPTION_FORM,
                    WIZARD_HELP2: help_strings.WIZ_CREATE_RIGHT_SURVEY_PAGE_2
                },
                WIZARD_STRINGS: {
                    WIZARD_SEL_SOURCE_TITLE: "What source do you want to associate the right with?",  # TODO Translate
                    WIZARD_SEL_SOURCE_ENTERING_DATA_MANUALLY: "Entering data manually using a form",  # TODO Translate
                    WIZARD_SEL_FEATURES_TITLE: "What source do you want to associate the right with?"
                }
            }
        elif wizard_config_name == WIZARD_CREATE_RESTRICTION_SURVEY:
            wizard_config = {
                # MODEL
                WIZARD_LAYERS: {
                    names.LC_RESTRICTION_T: None,
                    names.LC_ADMINISTRATIVE_SOURCE_T: None,
                    names.COL_RRR_SOURCE_T: None
                },
                WIZARD_EDITING_LAYER_NAME: names.LC_RESTRICTION_T,
                WIZARD_FEATURE_NAME: QCoreApplication.translate("CreateRestrictionSurveyWizard", "restriction"),
                WIZARD_READ_ONLY_FIELDS: [],
                # VIEW / CONTROLLER?
                WIZARD_QSETTINGS: {
                    WIZARD_QSETTINGS_PATH: "wizards/restriction"
                },
                WIZARD_TOOL_NAME: QCoreApplication.translate("CreateRestrictionSurveyWizard", "Create restriction"),
                # VIEW
                WIZARD_HELP: "create_restriction",
                WIZARD_HELP_PAGES: {
                    WIZARD_HELP1: help_strings.WIZ_CREATE_RESTRICTION_SURVEY_PAGE_1_OPTION_FORM,
                    WIZARD_HELP2: help_strings.WIZ_CREATE_RESTRICTION_SURVEY_PAGE_2
                },
                WIZARD_STRINGS: {
                    WIZARD_SEL_SOURCE_TITLE: "How would you like to create restrictions?",  # TODO Translate
                    WIZARD_SEL_SOURCE_ENTERING_DATA_MANUALLY: "Entering data manually using a form",  # TODO Translate
                    WIZARD_SEL_FEATURES_TITLE: "What source do you want to associate the restriction with?"
                }
            }
        elif wizard_config_name == WIZARD_CREATE_EXT_ADDRESS_SURVEY:
            wizard_config = {
                # MODEL
                WIZARD_LAYERS: {
                    names.EXT_ADDRESS_S: None,
                    names.LC_PLOT_T: None,
                    names.LC_BUILDING_T: None,
                    names.LC_BUILDING_UNIT_T: None
                },
                WIZARD_EDITING_LAYER_NAME: names.EXT_ADDRESS_S,
                WIZARD_FEATURE_NAME: QCoreApplication.translate("CreateExtAddressSurveyWizard", "ext address"),
                WIZARD_READ_ONLY_FIELDS: [],
                # VIEW / CONTROLLER?
                WIZARD_QSETTINGS: {
                    WIZARD_QSETTINGS_PATH: "wizards/ext_address"
                },
                WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.PointLayer,
                # VIEW
                WIZARD_TOOL_NAME: QCoreApplication.translate("CreateExtAddressSurveyWizard", "Create ext address"),
                WIZARD_HELP: "associate_ext_address",
                WIZARD_HELP_PAGES: {
                    WIZARD_HELP1: help_strings.WIZ_ASSOCIATE_EXTADDRESS_SURVEY_PAGE_2_OPTION_1,
                    WIZARD_HELP2: help_strings.WIZ_ASSOCIATE_EXTADDRESS_SURVEY_PAGE_2_OPTION_2,
                    WIZARD_HELP3: help_strings.WIZ_ASSOCIATE_EXTADDRESS_SURVEY_PAGE_2_OPTION_3
                },
                WIZARD_STRINGS: {
                    WIZARD_SEL_SOURCE_TITLE: "How would you like to create and associate addresses?",  # TODO Translate
                    WIZARD_SEL_SOURCE_ENTERING_DATA_MANUALLY: "Entering data manually using a form"  # TODO Translate
                }
            }
        elif wizard_config_name == WIZARD_CREATE_PLOT_SURVEY:
            wizard_config = {
                # MODEL
                WIZARD_LAYERS: {
                    names.LC_PLOT_T: None,
                    names.LC_BOUNDARY_T: None
                },
                WIZARD_EDITING_LAYER_NAME: names.LC_PLOT_T,
                WIZARD_FEATURE_NAME: QCoreApplication.translate("CreatePlotSurveyWizard", "plot"),
                WIZARD_READ_ONLY_FIELDS: [],
                # VIEW / CONTROLLER?
                WIZARD_QSETTINGS: {
                    WIZARD_QSETTINGS_PATH: "wizards/plot"
                },
                WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.PolygonLayer,
                # VIEW
                WIZARD_TOOL_NAME: QCoreApplication.translate("CreatePlotSurveyWizard", "Create plot"),
                WIZARD_HELP: "create_plot",
                WIZARD_HELP_PAGES: {
                    WIZARD_HELP1: help_strings.WIZ_CREATE_PLOT_SURVEY_PAGE_1_OPTION_BOUNDARIES,
                    WIZARD_HELP2: help_strings.WIZ_CREATE_PLOT_SURVEY_PAGE_2
                },
                WIZARD_STRINGS: {
                    WIZARD_SEL_SOURCE_TITLE: "How would you like to create plots?",  # TODO Translate
                    WIZARD_SEL_SOURCE_ENTERING_DATA_MANUALLY: "Selecting existing boundaries"  # TODO Translate
                }
            }
        elif wizard_config_name == WIZARD_CREATE_PARCEL_SURVEY:
            wizard_config = {
                # MODEL
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
                WIZARD_FEATURE_NAME: QCoreApplication.translate("CreateParcelSurveyWizard", "parcel"),
                WIZARD_READ_ONLY_FIELDS: [names.LC_PARCEL_T_PARCEL_TYPE_F],
                # VIEW / CONTROLLER?
                WIZARD_QSETTINGS: {
                    WIZARD_QSETTINGS_PATH: "wizards/parcel"
                },
                WIZARD_MAP_LAYER_PROXY_MODEL: QgsMapLayerProxyModel.NoGeometry,
                # VIEW
                WIZARD_TOOL_NAME: QCoreApplication.translate("CreateParcelSurveyWizard", "Create parcel"),
                WIZARD_HELP: "create_parcel",
                WIZARD_HELP_PAGES: {
                    WIZARD_HELP1: help_strings.WIZ_CREATE_PARCEL_SURVEY_PAGE_1_OPTION_EXISTING_PLOT,
                    WIZARD_HELP2: help_strings.WIZ_CREATE_PARCEL_SURVEY_PAGE_2
                },
                WIZARD_STRINGS: {
                    WIZARD_SEL_SOURCE_TITLE: "How would you like to create parcels?",  # TODO Translate
                    WIZARD_SEL_SOURCE_ENTERING_DATA_MANUALLY: "Entering data manually using a form"  # TODO Translate
                }
            }

        if not wizard_config or not self.app.core.required_layers_are_available(
                db, wizard_config[WIZARD_LAYERS], wizard_config[WIZARD_TOOL_NAME]):
            return None

        return wizard_config
