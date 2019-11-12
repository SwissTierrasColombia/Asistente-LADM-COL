# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-09-10
        git sha              : :%H$
        copyright            : (C) 2017 by Germán Carrillo (BSF Swissphoto)
                               (C) 2018 by Sergio Ramírez (Incige SAS)
                               (C) 2019 by Leo Cardona (BSF Swissphoto)
        email                : gcarrillo@linuxmail.com
                               sergio.ramirez@incige.com
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
from functools import partial

from qgis.PyQt.QtCore import (QCoreApplication,
                              pyqtSignal)
from qgis.core import (QgsVectorLayerUtils,
                       Qgis)

from asistente_ladm_col.config.general_config import (LAYER,
                                                      PLUGIN_NAME)
from asistente_ladm_col.gui.wizards.multi_page_wizard_factory import MultiPageWizardFactory
from asistente_ladm_col.gui.wizards.select_features_by_expression_dialog_wrapper import SelectFeatureByExpressionDialogWrapper


class CreateRRROperationWizard(MultiPageWizardFactory, SelectFeatureByExpressionDialogWrapper):
    update_wizard_is_open_flag = pyqtSignal(bool)
    set_finalize_geometry_creation_enabled_emitted = pyqtSignal(bool)

    def __init__(self, iface, db, qgis_utils, wizard_settings):
        MultiPageWizardFactory.__init__(self, iface, db, qgis_utils, wizard_settings)
        SelectFeatureByExpressionDialogWrapper.__init__(self)

    def post_save(self, features):
        message = QCoreApplication.translate(self.WIZARD_NAME,
                                             "'{}' tool has been closed because an error occurred while trying to save the data.").format(self.WIZARD_TOOL_NAME)

        if len(features) != 1:
            message = QCoreApplication.translate(self.WIZARD_NAME, "'{}' tool has been closed. We should have got only one {} by we have {}").format(self.WIZARD_TOOL_NAME, self.WIZARD_FEATURE_NAME, len(features))
            self.log.logMessage("We should have got only one {}, but we have {}".format(self.WIZARD_FEATURE_NAME, len(features)), PLUGIN_NAME, Qgis.Warning)
        else:
            fid = features[0].id()
            administrative_source_ids = [f[self.names.T_ID_F] for f in self._layers[self.names.OP_ADMINISTRATIVE_SOURCE_T][LAYER].selectedFeatures()]

            if not self._layers[self.EDITING_LAYER_NAME][LAYER].getFeature(fid).isValid():
                self.log.logMessage("Feature not found in layer {}...".format(self.EDITING_LAYER_NAME), PLUGIN_NAME, Qgis.Warning)
            else:
                # feature_rrr_id: generic name used for represent id for right, restriction
                feature_rrr_id = self._layers[self.EDITING_LAYER_NAME][LAYER].getFeature(fid)[self.names.T_ID_F]

                # Fill rrrfuente table
                new_features = []
                for administrative_source_id in administrative_source_ids:
                    new_feature = QgsVectorLayerUtils().createFeature(self._layers[self.names.COL_RRR_SOURCE_T][LAYER])

                    new_feature.setAttribute(self.names.COL_RRR_SOURCE_T_SOURCE_F, administrative_source_id)
                    if self.EDITING_LAYER_NAME == self.names.OP_RIGHT_T:
                        new_feature.setAttribute(self.names.COL_RRR_SOURCE_T_OP_RIGHT_F, feature_rrr_id)
                    elif self.EDITING_LAYER_NAME == self.names.OP_RESTRICTION_T:
                        new_feature.setAttribute(self.names.COL_RRR_SOURCE_T_OP_RESTRICTION_F, feature_rrr_id)

                    self.log.logMessage("Saving Administrative_source-{}: {}-{}".format(self.WIZARD_FEATURE_NAME, administrative_source_id, feature_rrr_id), PLUGIN_NAME, Qgis.Info)
                    new_features.append(new_feature)

                self._layers[self.names.COL_RRR_SOURCE_T][LAYER].dataProvider().addFeatures(new_features)
                message = QCoreApplication.translate(self.WIZARD_NAME,"The new {} (t_id={}) was successfully created and associated with its corresponding administrative source (t_id={})!").format(self.WIZARD_FEATURE_NAME, feature_rrr_id, ", ".join([str(b) for b in administrative_source_ids]))

        return message

    def exec_form_advanced(self, layer):
        pass

    def check_selected_features(self):
        # Check selected features in administrative source layer
        if self._layers[self.names.OP_ADMINISTRATIVE_SOURCE_T][LAYER].selectedFeatureCount():
            self.lb_admin_source.setText(QCoreApplication.translate(self.WIZARD_NAME, "<b>Administrative Source(s)</b>: {count} Feature Selected").format(count=self._layers[self.names.OP_ADMINISTRATIVE_SOURCE_T][LAYER].selectedFeatureCount()))
            self.button(self.FinishButton).setDisabled(False)
        else:
            self.lb_admin_source.setText(QCoreApplication.translate(self.WIZARD_NAME, "<b>Administrative Source(s)</b>: 0 Features Selected"))
            self.button(self.FinishButton).setDisabled(True)

    def disconnect_signals_select_features_by_expression(self):
        signals = [self.btn_expression.clicked]

        for signal in signals:
            try:
                signal.disconnect()
            except:
                pass

    def register_select_features_by_expression(self):
        self.btn_expression.clicked.connect(partial(self.select_features_by_expression, self._layers[self.names.OP_ADMINISTRATIVE_SOURCE_T][LAYER]))
