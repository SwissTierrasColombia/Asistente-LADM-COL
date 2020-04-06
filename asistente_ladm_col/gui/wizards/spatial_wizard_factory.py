# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-09-10
        git sha              : :%H$
        copyright            : (C) 2017 by Germán Carrillo (BSF Swissphoto)
                               (C) 2018 by Sergio Ramírez (Incige SAS)
                               (C) 2018 by Jorge Useche (Incige SAS)
                               (C) 2018 by Jhon Galindo (Incige SAS)
                               (C) 2019 by Leo Cardona (BSF Swissphoto)
        email                : gcarrillo@linuxmail.org
                               sergio.ramirez@incige.com
                               naturalmentejorge@gmail.com
                               jhonsigpjc@gmail.com
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
from qgis.PyQt.QtCore import (QCoreApplication,
                              pyqtSignal)
from qgis.core import (QgsProject,
                       Qgis)

from asistente_ladm_col.gui.wizards.abs_wizard_factory import AbsWizardFactory
from asistente_ladm_col.gui.wizards.select_features_by_expression_dialog_wrapper import SelectFeatureByExpressionDialogWrapper
from asistente_ladm_col.gui.wizards.select_features_on_map_wrapper import SelectFeaturesOnMapWrapper
from asistente_ladm_col.gui.wizards.map_interaction_expansion import MapInteractionExpansion


class SpatialWizardFactory(AbsWizardFactory, MapInteractionExpansion):
    update_wizard_is_open_flag = pyqtSignal(bool)
    set_finalize_geometry_creation_enabled_emitted = pyqtSignal(bool)

    def __init__(self, iface, db, wizard_settings):
        self.iface = iface
        AbsWizardFactory.__init__(self, iface, db, wizard_settings)
        MapInteractionExpansion.__init__(self)
        self.set_disable_digitize_actions()

    def init_gui(self):
        raise NotImplementedError

    def adjust_page_1_controls(self):
        raise NotImplementedError

    def finished_dialog(self):
        self.save_settings()

        if self.rad_refactor.isChecked():
            if self.mMapLayerComboBox.currentLayer() is not None:
                field_mapping = self.cbo_mapping.currentText()
                res_etl_model = self.app.core.show_etl_model(self._db,
                                                               self.mMapLayerComboBox.currentLayer(),
                                                               self.EDITING_LAYER_NAME,
                                                               field_mapping=field_mapping)
                if res_etl_model: # Features were added?
                    # If the result of the etl_model is successful and we used a stored recent mapping, we delete the
                    # previous mapping used (we give preference to the latest used mapping)
                    if field_mapping:
                        self.app.core.delete_old_field_mapping(field_mapping)

                    self.app.core.save_field_mapping(self.EDITING_LAYER_NAME)
            else:
                self.logger.warning_msg(__name__, QCoreApplication.translate("WizardTranslations",
                    "Select a source layer to set the field mapping to '{}'.").format(self.EDITING_LAYER_NAME))

            self.close_wizard()

        elif self.rad_create_manually.isChecked():
            self.set_finalize_geometry_creation_enabled_emitted.emit(True)
            self.prepare_feature_creation()

    def prepare_feature_creation_layers(self):
        self.connect_on_removing_layers()

        # All layers were successfully loaded
        return True

    def disconnect_signals(self):
        if isinstance(self, SelectFeatureByExpressionDialogWrapper):
            self.disconnect_signals_select_features_by_expression()

        if isinstance(self, SelectFeaturesOnMapWrapper):
            self.disconnect_signals_select_features_on_map()

        try:
            self._layers[self.EDITING_LAYER_NAME].committedFeaturesAdded.disconnect(self.finish_feature_creation)
        except:
            pass

        self.disconnect_signals_map_interaction_expansion()

    def close_wizard(self, message=None, show_message=True):
        if message is None:
            message = QCoreApplication.translate("WizardTranslations", "'{}' tool has been closed.").format(self.WIZARD_TOOL_NAME)
        if show_message:
            self.logger.info_msg(__name__, message)

        if isinstance(self, SelectFeaturesOnMapWrapper):
            self.init_map_tool()

        self.rollback_in_layers_with_empty_editing_buffer()
        self.set_finalize_geometry_creation_enabled_emitted.emit(False)
        self.disconnect_signals()
        self.set_ready_only_field(read_only=False)
        self.set_disable_digitize_actions(visible=True)
        self.update_wizard_is_open_flag.emit(False)
        self.close()

    def edit_feature(self):
        self.iface.layerTreeView().setCurrentLayer(self._layers[self.EDITING_LAYER_NAME])
        self._layers[self.EDITING_LAYER_NAME].committedFeaturesAdded.connect(self.finish_feature_creation)

        # Disable transactions groups
        QgsProject.instance().setAutoTransaction(False)

        # Activate snapping
        self.app.core.active_snapping_all_layers(tolerance=9)
        self.open_form(self._layers[self.EDITING_LAYER_NAME])

        self.logger.info_msg(__name__, QCoreApplication.translate("WizardTranslations",
           "You can now start capturing {} digitizing on the map...").format(self.WIZARD_FEATURE_NAME))

    def post_save(self, features):
        raise NotImplementedError

    def open_form(self, layer):
        if not layer.isEditable():
            layer.startEditing()

        self.app.core.suppress_form(layer, True)
        self.iface.actionAddFeature().trigger()

    def get_feature_exec_form(self, layer):
        self.set_finalize_geometry_creation_enabled_emitted.emit(False)
        feature = None
        for id, added_feature in layer.editBuffer().addedFeatures().items():
            feature = added_feature
            break

        return feature

    def exec_form_advanced(self, layer):
        raise NotImplementedError
