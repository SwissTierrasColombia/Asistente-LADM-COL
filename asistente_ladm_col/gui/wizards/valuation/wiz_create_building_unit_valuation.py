from functools import partial

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsVectorLayerUtils)

from asistente_ladm_col.config.ladm_names import LADMNames
from asistente_ladm_col.config.general_config import (CSS_COLOR_OKAY_LABEL,
                                                      CSS_COLOR_ERROR_LABEL)
from asistente_ladm_col.gui.wizards.multi_page_wizard_factory import MultiPageWizardFactory
from asistente_ladm_col.gui.wizards.select_features_by_expression_dialog_wrapper import SelectFeatureByExpressionDialogWrapper
from asistente_ladm_col.gui.wizards.select_features_on_map_wrapper import SelectFeaturesOnMapWrapper


class CreateBuildingUnitValuationWizard(MultiPageWizardFactory,
                                        SelectFeatureByExpressionDialogWrapper,
                                        SelectFeaturesOnMapWrapper):
    def __init__(self, iface, db, qgis_utils, wizard_settings):
        MultiPageWizardFactory.__init__(self, iface, db, qgis_utils, wizard_settings)
        SelectFeatureByExpressionDialogWrapper.__init__(self)
        SelectFeaturesOnMapWrapper.__init__(self)

    def post_save(self, features):
        message = QCoreApplication.translate("WizardTranslations",
                                             "'{}' tool has been closed because an error occurred while trying to save the data.").format(self.WIZARD_TOOL_NAME)
        if len(features) != 1:
            message = QCoreApplication.translate("WizardTranslations", "'{}' tool has been closed. We should have got only one {} by we have {}").format(self.WIZARD_TOOL_NAME, self.WIZARD_FEATURE_NAME, len(features))
            self.logger.warning(__name__, "We should have got only one {}, but we have {}".format(self.WIZARD_FEATURE_NAME, len(features)))
        else:
            fid = features[0].id()
            building_unit_ids = [f[self.names.T_ID_F] for f in self._layers[self.names.OP_BUILDING_UNIT_T].selectedFeatures()]

            if not self._layers[self.EDITING_LAYER_NAME].getFeature(fid).isValid():
                self.logger.warning(__name__, "Feature not found in layer {}...".format(self.EDITING_LAYER_NAME))
            else:
                building_unit_valuation_id = self._layers[self.EDITING_LAYER_NAME].getFeature(fid)[self.names.T_ID_F]

                # Fill avaluounidadconstruccion table
                new_features = []
                for building_unit_id in building_unit_ids:
                    new_feature = QgsVectorLayerUtils().createFeature(self._layers[LADMNames.AVALUOUNIDADCONSTRUCCION_TABLE])
                    new_feature.setAttribute(LADMNames.AVALUOUNIDADCONSTRUCCION_TABLE_BUILDING_UNIT_FIELD, building_unit_id)
                    new_feature.setAttribute(LADMNames.AVALUOUNIDADCONSTRUCCION_TABLE_BUILDING_UNIT_VALUATION_FIELD, building_unit_valuation_id)
                    self.logger.info(__name__, "Saving Building unit-Building unit valuation: {}-{}".format(building_unit_id, building_unit_valuation_id))
                    new_features.append(new_feature)

                self._layers[LADMNames.AVALUOUNIDADCONSTRUCCION_TABLE].dataProvider().addFeatures(new_features)
                if building_unit_ids:
                    message = QCoreApplication.translate("WizardTranslations", "The new {} (t_id={}) was successfully created and associated with its corresponding building unit (t_id={})!").format(self.WIZARD_FEATURE_NAME, building_unit_valuation_id, building_unit_ids[0])

        return message

    def exec_form_advanced(self, layer):
        pass

    def check_selected_features(self):
        _count = self._layers[self.names.OP_BUILDING_UNIT_T].selectedFeatureCount()
        self.lb_info.setText(QCoreApplication.translate("WizardTranslations", "<b>Building unit(s)</b>: {count} Feature(s) Selected").format(count=_count))
        self.lb_info.setStyleSheet(CSS_COLOR_OKAY_LABEL)  # Default color

        if _count != 1:
            _color = CSS_COLOR_ERROR_LABEL
            self.lb_info.setStyleSheet(_color)
        self.button(self.FinishButton).setEnabled(_count == 1)

    def disconnect_signals_select_features_by_expression(self):
        signals = [self.btn_expression.clicked]

        for signal in signals:
            try:
                signal.disconnect()
            except:
                pass

    def register_select_features_by_expression(self):
        self.btn_expression.clicked.connect(partial(self.select_features_by_expression, self._layers[self.names.OP_BUILDING_UNIT_T]))

    def disconnect_signals_controls_select_features_on_map(self):
        signals = [self.btn_map.clicked]

        for signal in signals:
            try:
                signal.disconnect()
            except:
                pass

    def register_select_feature_on_map(self):
        self.btn_map.clicked.connect(partial(self.select_features_on_map, self._layers[self.names.OP_BUILDING_UNIT_T]))
