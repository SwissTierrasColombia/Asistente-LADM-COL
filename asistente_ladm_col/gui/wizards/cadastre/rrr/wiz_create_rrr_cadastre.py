# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-09-10
        git sha              : :%H$
        copyright            : (C) 2017 by Germán Carrillo
                               (C) 2018 by Sergio Ramírez (Incige SAS)
                               (C) 2019 by Leo Cardona
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
from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsVectorLayerUtils,
                       Qgis)

from .....config.general_config import (LAYER,
                                        PLUGIN_NAME)
from .....config.table_mapping_config import (ADMINISTRATIVE_SOURCE_TABLE,
                                              RRR_SOURCE_RELATION_TABLE,
                                              RRR_SOURCE_SOURCE_FIELD,
                                              RRR_SOURCE_RIGHT_FIELD,
                                              RRR_SOURCE_RESTRICTION_FIELD,
                                              RRR_SOURCE_RESPONSIBILITY_FIELD,
                                              RIGHT_TABLE,
                                              RESTRICTION_TABLE,
                                              RESPONSIBILITY_TABLE,
                                              ID_FIELD)
from .....gui.wizards.multi_page_wizard import MultiPageWizard
from .....gui.wizards.select_features_by_expression_wizard import SelectFeatureByExpressionWizard


class CreateRRRCadastreWizard(MultiPageWizard, SelectFeatureByExpressionWizard):

    def __init__(self, iface, db, qgis_utils, wizard_settings):
        MultiPageWizard.__init__(self, iface, db, qgis_utils, wizard_settings)
        SelectFeatureByExpressionWizard.__init__(self)

    def register_select_features_by_expression(self):
        self.btn_expression.clicked.connect(partial(self.select_features_by_expression, self._layers[ADMINISTRATIVE_SOURCE_TABLE][LAYER]))

    def check_selected_features(self):
        # Check selected features in administrative source layer
        if self._layers[ADMINISTRATIVE_SOURCE_TABLE][LAYER].selectedFeatureCount():
            self.lb_admin_source.setText(QCoreApplication.translate(self.WIZARD_NAME, "<b>Administrative Source(s)</b>: {count} Feature Selected").format(count=self._layers[ADMINISTRATIVE_SOURCE_TABLE][LAYER].selectedFeatureCount()))
            self.button(self.FinishButton).setDisabled(False)
        else:
            self.lb_admin_source.setText(QCoreApplication.translate(self.WIZARD_NAME, "<b>Administrative Source(s)</b>: 0 Features Selected"))
            self.button(self.FinishButton).setDisabled(True)

    def advance_save(self, features):

        message = QCoreApplication.translate(self.WIZARD_NAME,
                                             "'{}' tool has been closed because an error occurred while trying to save the data.").format(self.WIZARD_TOOL_NAME)

        if len(features) != 1:
            message = QCoreApplication.translate(self.WIZARD_NAME, "'{}' tool has been closed. We should have got only one {} by we have {}").format(self.WIZARD_TOOL_NAME, self.WIZARD_FEATURE_NAME, len(features))
            self.log.logMessage("We should have got only one {}, but we have {}".format(self.WIZARD_FEATURE_NAME, len(features)), PLUGIN_NAME, Qgis.Warning)
        else:
            fid = features[0].id()
            administrative_source_ids = [f['t_id'] for f in self._layers[ADMINISTRATIVE_SOURCE_TABLE][LAYER].selectedFeatures()]

            if not self._layers[self.EDITING_LAYER_NAME][LAYER].getFeature(fid).isValid():
                self.log.logMessage("Feature not found in layer {}...".format(self.EDITING_LAYER_NAME), PLUGIN_NAME, Qgis.Warning)
            else:
                # feature_rrr_id: generic name used for represent id for right, restriction, responsibility
                feature_rrr_id = self._layers[self.EDITING_LAYER_NAME][LAYER].getFeature(fid)[ID_FIELD]

                # Fill rrrfuente table
                new_features = []
                for administrative_source_id in administrative_source_ids:
                    new_feature = QgsVectorLayerUtils().createFeature(self._layers[RRR_SOURCE_RELATION_TABLE][LAYER])

                    new_feature.setAttribute(RRR_SOURCE_SOURCE_FIELD, administrative_source_id)
                    if self.EDITING_LAYER_NAME == RIGHT_TABLE:
                        new_feature.setAttribute(RRR_SOURCE_RIGHT_FIELD, feature_rrr_id)
                    elif self.EDITING_LAYER_NAME == RESTRICTION_TABLE:
                        new_feature.setAttribute(RRR_SOURCE_RESTRICTION_FIELD, feature_rrr_id)
                    elif self.EDITING_LAYER_NAME == RESPONSIBILITY_TABLE:
                        new_feature.setAttribute(RRR_SOURCE_RESPONSIBILITY_FIELD, feature_rrr_id)

                    self.log.logMessage("Saving Administrative_source-{}: {}-{}".format(self.WIZARD_FEATURE_NAME, administrative_source_id, feature_rrr_id), PLUGIN_NAME, Qgis.Info)
                    new_features.append(new_feature)

                self._layers[RRR_SOURCE_RELATION_TABLE][LAYER].dataProvider().addFeatures(new_features)
                message = QCoreApplication.translate(self.WIZARD_NAME,"The new {} (t_id={}) was successfully created and associated with its corresponding administrative source (t_id={})!").format(self.WIZARD_FEATURE_NAME, feature_rrr_id, ", ".join([str(b) for b in administrative_source_ids]))

        return message

    def register_select_feature_on_map(self):
        pass
