from abc import abstractmethod, ABC
from qgis.core import QgsMapLayerProxyModel

from qgis.PyQt.QtCore import (QObject,
                              pyqtSignal,
                              QCoreApplication)

from qgis.PyQt.QtWidgets import QMessageBox
from asistente_ladm_col import Logger
from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.config.enums import EnumLayerCreationMode
from asistente_ladm_col.config.general_config import (WIZARD_EDITING_LAYER_NAME,
                                                      WIZARD_STRINGS,
                                                      WIZARD_REFACTOR_FIELDS_RECENT_MAPPING_OPTIONS,
                                                      WIZARD_REFACTOR_FIELDS_LAYER_FILTERS,
                                                      WIZARD_HELP_PAGES,
                                                      WIZARD_HELP,
                                                      WIZARD_FINISH_BUTTON_TEXT,
                                                      WIZARD_SELECT_SOURCE_HELP,
                                                      WIZARD_HELP1,
                                                      WIZARD_LAYERS,
                                                      WIZARD_READ_ONLY_FIELDS,
                                                      WIZARD_TOOL_NAME,
                                                      WIZARD_CREATION_MODE_KEY,
                                                      WIZARD_SELECTED_TYPE_KEY,
                                                      WIZARD_QSETTINGS,
                                                      WIZARD_QSETTINGS_PATH,
                                                      WIZARD_FEATURE_NAME)
from asistente_ladm_col.config.help_strings import HelpStrings
from asistente_ladm_col.gui.wizards.controller.controller_args import CreateFeatureArgs
from asistente_ladm_col.gui.wizards.model.common.abstract_qobject_meta import AbstractQObjectMeta
from asistente_ladm_col.gui.wizards.model.common.args.model_args import (ExecFormAdvancedArgs,
                                                                         FinishFeatureCreationArgs,
                                                                         MapToolChangedArgs)
from asistente_ladm_col.gui.wizards.model.common.common_operations import CommonOperationsModel
from asistente_ladm_col.gui.wizards.model.common.layer_remove_signals_manager import LayerRemovedSignalsManager
from asistente_ladm_col.gui.wizards.model.common.refactor_fields_feature_creator import RefactorFieldsFeatureCreator
from asistente_ladm_col.gui.wizards.model.common.wizard_q_settings_manager import WizardQSettingsManager


class ProductFactory(ABC):
    @abstractmethod
    def create_feature_manager(self, db, layers, editing_layer):
        pass

    @abstractmethod
    def create_manual_feature_creator(self, iface, app, logger, layer, feature_name):
        pass

    @abstractmethod
    def create_feature_selector_on_map(self, iface, logger, multiple_features=True):
        pass

    @abstractmethod
    def create_feature_selector_by_expression(self, iface):
        pass

    @abstractmethod
    def create_wizard_messages_manager(self, wizard_tool_name, editing_layer_name, logger):
        pass


class AbstractWizardController(QObject, metaclass=AbstractQObjectMeta):
    update_wizard_is_open_flag = pyqtSignal(bool)

    def __init__(self, iface, db, wizard_config, product_factory: ProductFactory, observer):
        QObject.__init__(self)

        self._app = AppInterface()

        self._db = db
        self._wizard_config = wizard_config
        self._iface = iface

        self._logger = Logger()

        self._layers = self._wizard_config[WIZARD_LAYERS]
        self._editing_layer_name = self._wizard_config[WIZARD_EDITING_LAYER_NAME]
        self._editing_layer = self._layers[self._editing_layer_name]
        self._WIZARD_TOOL_NAME = self._wizard_config[WIZARD_TOOL_NAME]

        self.__settings_manager = WizardQSettingsManager(self._wizard_config[WIZARD_QSETTINGS][WIZARD_QSETTINGS_PATH])

        self._feature_manager = None
        self._feature_selector_on_map = None
        self._feature_selector_by_expression = None

        self.__product_factory = product_factory

        self._observer = observer

    def _initialize(self):
        self._feature_manager = self.__product_factory.create_feature_manager(
            self._db, self._wizard_config[WIZARD_LAYERS], self._editing_layer)
        self._common_operations = \
            CommonOperationsModel(self._wizard_config[WIZARD_LAYERS], self._editing_layer_name, self._app,
                                  self._wizard_config[WIZARD_READ_ONLY_FIELDS])

        self._common_operations.set_read_only_fields(True)
        self.refactor_field_mapping = self._common_operations.get_field_mappings_file_names()  # view
        self.__view = self._create_view()  # view

        # REFACTOR FEATURE CREATOR
        self._feature_creator_from_refactor = RefactorFieldsFeatureCreator(self._app, self._db)

        # Manual
        self._manual_feature_creator = self.__product_factory.create_manual_feature_creator(
            self._iface, self._app, self._logger, self._editing_layer, self._wizard_config[WIZARD_FEATURE_NAME])

        self._manual_feature_creator.form_rejected.connect(self._form_rejected)

        self._manual_feature_creator.exec_form_advanced.connect(self.exec_form_advanced)
        self._manual_feature_creator.finish_feature_creation.connect(self.__finish_feature_creation)

        # features selector on map
        self._feature_selector_on_map = \
            self.__product_factory.create_feature_selector_on_map(self._iface, self._logger)

        self._feature_selector_on_map.features_selected.connect(self.features_selected)
        self._feature_selector_on_map.map_tool_changed.connect(self._map_tool_changed)

        # features selector by expression
        self._feature_selector_by_expression =\
            self.__product_factory.create_feature_selector_by_expression(self._iface)

        self._feature_selector_by_expression.feature_selection_by_expression_changed.connect(
            self.feature_selection_by_expression_changed)

        # layer_remove
        self._layer_remove_manager = LayerRemovedSignalsManager(self._wizard_config[WIZARD_LAYERS])
        self._layer_remove_manager.layer_removed.connect(self.layer_removed)

        self._wizard_messages = self.__product_factory.create_wizard_messages_manager(
            self._WIZARD_TOOL_NAME, self._editing_layer_name, self._logger)

        self._connect_external_signals()

    def create_feature(self, args: CreateFeatureArgs):
        self._save_settings()
        if args.layer_creation_mode == EnumLayerCreationMode.REFACTOR_FIELDS:
            self.create_feature_from_refactor_fields()
        else:
            self._create_manually()

    def _create_manually(self):
        self._layer_remove_manager.reconnect_signals()
        self._manual_feature_creator.create()

    # called from manual feature creator
    @abstractmethod
    def exec_form_advanced(self, args: ExecFormAdvancedArgs):
        pass

    # called from selector on map
    @abstractmethod
    def features_selected(self):
        pass

    # called from feature selection by expression
    @abstractmethod
    def feature_selection_by_expression_changed(self):
        pass

    # from refactor fields
    def create_feature_from_refactor_fields(self):
        selected_layer = self.__view.get_selected_layer_refactor()

        if selected_layer is not None:
            field_mapping = self.__view.get_field_mapping_refactor()
            self._feature_creator_from_refactor.create(selected_layer, self._editing_layer_name, field_mapping)
        else:
            self._wizard_messages.show_select_a_source_layer_warning()

        self._wizard_messages.show_wizard_closed_msg()
        self.close_wizard()

    def __finish_feature_creation(self, layerId, features):
        args = self._feature_manager.finish_feature_creation(layerId, features)
        self._show_feature_creation_result(args)

    def _show_feature_creation_result(self, args: FinishFeatureCreationArgs):
        if not args.is_valid:
            self._wizard_messages.show_feature_not_found_in_layer_msg()
            self._wizard_messages.show_feature_not_found_in_layer_warning()
        else:
            self._wizard_messages.\
                show_feature_successfully_created_msg(self._wizard_config[WIZARD_FEATURE_NAME], args.feature_tid)

        self.close_wizard()

    # manual feature
    # view ---------------------------------------------------
    @abstractmethod
    def _create_view(self):
        pass

    def close_wizard(self):
        self.update_wizard_is_open_flag.emit(False)
        self.dispose()
        self.__view.close()

    def _get_view_config(self):
        # TODO Load help_strings from wizard_config
        help_strings = HelpStrings()
        return {
            WIZARD_STRINGS: self._wizard_config[WIZARD_STRINGS],
            WIZARD_REFACTOR_FIELDS_RECENT_MAPPING_OPTIONS: self.refactor_field_mapping,
            WIZARD_REFACTOR_FIELDS_LAYER_FILTERS: QgsMapLayerProxyModel.Filter(QgsMapLayerProxyModel.NoGeometry),
            WIZARD_HELP_PAGES: self._wizard_config[WIZARD_HELP_PAGES],
            WIZARD_HELP: self._wizard_config[WIZARD_HELP],
            WIZARD_FINISH_BUTTON_TEXT: {
                EnumLayerCreationMode.REFACTOR_FIELDS: QCoreApplication.translate("WizardTranslations", "Import"),
                EnumLayerCreationMode.MANUALLY: QCoreApplication.translate("WizardTranslations", "Create")
            },
            WIZARD_SELECT_SOURCE_HELP: {
                EnumLayerCreationMode.REFACTOR_FIELDS:
                    help_strings.get_refactor_help_string(self._db, self._editing_layer),
                EnumLayerCreationMode.MANUALLY:
                    self._wizard_config[WIZARD_HELP_PAGES][WIZARD_HELP1]
            }
        }

    def _save_settings(self):
        self.__settings_manager.save_settings(self.__view.get_settings())

    def _restore_settings(self):
        settings = self.__settings_manager.get_settings()

        if WIZARD_CREATION_MODE_KEY not in settings or settings[WIZARD_CREATION_MODE_KEY] is None:
            settings[WIZARD_CREATION_MODE_KEY] = EnumLayerCreationMode.MANUALLY

        if WIZARD_SELECTED_TYPE_KEY not in settings:
            settings[WIZARD_SELECTED_TYPE_KEY] = None

        self.__view.restore_settings(settings)

    #  called by view
    def wizard_rejected(self):
        self._wizard_messages.show_wizard_closed_msg()
        self.close_wizard()

    def _form_rejected(self):
        self._wizard_messages.show_form_closed_msg()
        self.close_wizard()

    def _map_tool_changed(self, args: MapToolChangedArgs):
        # TODO parent was removed
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText(QCoreApplication.translate("WizardTranslations", "Do you really want to change the map tool?"))
        msg.setWindowTitle(QCoreApplication.translate("WizardTranslations", "CHANGING MAP TOOL?"))
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.button(QMessageBox.Yes).setText(QCoreApplication.translate("WizardTranslations", "Yes, and close the wizard"))
        msg.button(QMessageBox.No).setText(QCoreApplication.translate("WizardTranslations", "No, continue editing"))
        reply = msg.exec_()

        if reply == QMessageBox.Yes:
            args.change_map_tool = True
            self._wizard_messages.show_map_tool_changed_msg()
            self.close_wizard()

    def layer_removed(self):
        self._wizard_messages.show_layer_removed_msg()
        self.close_wizard()

    def exec_(self):
        self._restore_settings()
        self.__view.exec_()

    def dispose(self):
        self._layer_remove_manager.disconnect_signals()
        self._manual_feature_creator.disconnect_signals()
        self._common_operations.rollback_in_layers_with_empty_editing_buffer()
        self._common_operations.set_read_only_fields(False)

        self._feature_selector_on_map.disconnect_signals()
        self._disconnect_external_signals()

    def _connect_external_signals(self):
        self.update_wizard_is_open_flag.connect(self._observer.set_wizard_is_open_flag)

    def _disconnect_external_signals(self):
        self.update_wizard_is_open_flag.disconnect(self._observer.set_wizard_is_open_flag)
