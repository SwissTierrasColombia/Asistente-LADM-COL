from abc import abstractmethod

from qgis.PyQt.QtCore import (QObject,
                              pyqtSignal,
                              QCoreApplication)
from qgis.core import QgsMapLayerProxyModel

from asistente_ladm_col.config.enums import EnumDigitizedFeatureStatus
from asistente_ladm_col.config.general_config import (WIZARD_REFACTOR_FIELDS_LAYER_FILTERS,
                                                      WIZARD_MAP_LAYER_PROXY_MODEL)
from asistente_ladm_col.gui.wizards.controller.common.abstract_wizard_controller import (AbstractWizardController,
                                                                                         ProductFactory)
from asistente_ladm_col.gui.wizards.model.common.args.model_args import (ValidFeaturesDigitizedArgs,
                                                                         UnexpectedFeaturesDigitizedArgs)
from asistente_ladm_col.gui.wizards.view.common.view_utils import ViewUtils


class AbstractSpatialWizardController(AbstractWizardController):
    enable_save_geometry_button = pyqtSignal(bool)

    def __init__(self, iface, db, wizard_config, product_factory: ProductFactory, observer):
        AbstractWizardController.__init__(self, iface, db, wizard_config, product_factory, observer)

    @abstractmethod
    def _create_view(self):
        pass

    def _initialize(self):
        super()._initialize()
        ViewUtils.enable_digitize_actions(self._iface, False)
        self._manual_feature_creator.valid_features_digitized.connect(self.valid_features_digitized)
        self._manual_feature_creator.unexpected_features_digitized.connect(self.unexpected_features_digitized)

    def valid_features_digitized(self, args: ValidFeaturesDigitizedArgs):
        self.enable_save_geometry_button.emit(False)

    #   spatial methods
    def save_created_geometry(self):
        self._manual_feature_creator.save_created_geometry()

    def close_wizard(self):
        ViewUtils.enable_digitize_actions(self._iface, True)
        self.enable_save_geometry_button.emit(False)

        super().close_wizard()

    def _create_manually(self):
        self.enable_save_geometry_button.emit(True)
        super()._create_manually()

    # spatial
    def unexpected_features_digitized(self, args: UnexpectedFeaturesDigitizedArgs):
        message = ""
        if args.status == EnumDigitizedFeatureStatus.INVALID:
            message = QCoreApplication.translate("WizardTranslations",
                                                 "The geometry is invalid. Do you want to return to the edit session?")
        elif args.status == EnumDigitizedFeatureStatus.ZERO_FEATURES:
            message = QCoreApplication.translate("WizardTranslations",
                                                 "No geometry has been created. Do you want to return to the edit session?")
        elif args.status == EnumDigitizedFeatureStatus.OTHER:
            message = QCoreApplication.translate("WizardTranslations",
                                                 "Several geometries were created but only one was expected. Do you want to return to the edit session?")

        if not ViewUtils.show_message_associate_geometry_creation(message):
            self.rollback_layer(args.layer)

            message = QCoreApplication.translate("WizardTranslations", "'{}' tool has been closed.").format(
                self._WIZARD_TOOL_NAME)

            self._logger.info_msg(__name__, message)
            self.close_wizard()

    def rollback_layer(self, layer):
        # stop edition in close_wizard crash qgis
        if layer.isEditable():
            layer.rollBack()

    def _connect_external_signals(self):
        super()._connect_external_signals()

        self.enable_save_geometry_button.connect(self._observer.set_enable_finalize_geometry_creation_action)
        self._observer.wiz_geometry_creation_finished.connect(self.save_created_geometry)

    def _disconnect_external_signals(self):
        super()._disconnect_external_signals()

        self.enable_save_geometry_button.disconnect(self._observer.set_enable_finalize_geometry_creation_action)
        self._observer.wiz_geometry_creation_finished.disconnect(self.save_created_geometry)
