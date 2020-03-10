# -*- coding: utf-8 -*-
"""
/***************************************************************************
    begin                :    28/08/18
    git sha              :    :%H$
    copyright            :    (C) 2018 by Germán Carrillo (BSF-Swissphoto)
    email                :    gcarrillo@linuxmail.org
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import (QObject,
                              QCoreApplication)

from asistente_ladm_col.config.mapping_config import LADMNames
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.utils.utils import is_version_valid


class ModelParser(QObject):
    def __init__(self, db):
        QObject.__init__(self)
        self.logger = Logger()

        self.current_model_version = {
            LADMNames.OPERATION_MODEL_PREFIX: None,
            LADMNames.CADASTRAL_FORM_MODEL_PREFIX: None,
            LADMNames.VALUATION_MODEL_PREFIX: None,
            LADMNames.LADM_MODEL_PREFIX: None,
            LADMNames.ANT_MODEL_PREFIX: None,
            LADMNames.REFERENCE_CARTOGRAPHY_PREFIX: None,
            LADMNames.SNR_DATA_MODEL_PREFIX: None,
            LADMNames.SUPPLIES_INTEGRATION_MODEL_PREFIX: None,
            LADMNames.SUPPLIES_MODEL_PREFIX: None
        }

        self.model_version_is_supported = {
            LADMNames.OPERATION_MODEL_PREFIX: False,
            LADMNames.CADASTRAL_FORM_MODEL_PREFIX: False,
            LADMNames.VALUATION_MODEL_PREFIX: False,
            LADMNames.LADM_MODEL_PREFIX: False,
            LADMNames.ANT_MODEL_PREFIX: False,
            LADMNames.REFERENCE_CARTOGRAPHY_PREFIX: False,
            LADMNames.SNR_DATA_MODEL_PREFIX: False,
            LADMNames.SUPPLIES_INTEGRATION_MODEL_PREFIX: False,
            LADMNames.SUPPLIES_MODEL_PREFIX: False
        }

        self._db = db

        # Fill versions for each model found
        for current_model_name in self._get_models():
            for model_prefix,v in self.current_model_version.items():
                if current_model_name.startswith(model_prefix):
                    parts = current_model_name.split(model_prefix)
                    if len(parts) > 1:
                        current_version = self.parse_version(parts[1])
                        current_version_valid = is_version_valid(current_version,
                                                                 LADMNames.SUPPORTED_MODEL_VERSIONS[model_prefix],
                                                                 True,  # Exact version required
                                                                 QCoreApplication.translate("ModelParser", model_prefix))
                        self.current_model_version[model_prefix] = current_version
                        self.model_version_is_supported[model_prefix] = current_version_valid
                        self.logger.debug(__name__, "Model '{}' found! Valid: {}".format(model_prefix, current_version_valid))
                        break

    def parse_version(self, str_version):
        """ E.g., _V2_9_6 -> 2.9.6 """
        return ".".join(str_version.replace("_V", "").split("_"))

    def operation_model_exists(self):
        return self.model_version_is_supported[LADMNames.OPERATION_MODEL_PREFIX]

    def cadastral_form_model_exists(self):
        return self.model_version_is_supported[LADMNames.CADASTRAL_FORM_MODEL_PREFIX]

    def valuation_model_exists(self):
        return self.model_version_is_supported[LADMNames.VALUATION_MODEL_PREFIX]

    def ant_model_exists(self):
        return self.model_version_is_supported[LADMNames.ANT_MODEL_PREFIX]

    def ladm_model_exists(self):
        return self.model_version_is_supported[LADMNames.LADM_MODEL_PREFIX]

    def reference_cartography_model_exists(self):
        return self.model_version_is_supported[LADMNames.REFERENCE_CARTOGRAPHY_PREFIX]

    def snr_data_model_exists(self):
        return self.model_version_is_supported[LADMNames.SNR_DATA_MODEL_PREFIX]

    def supplies_integration_model_exists(self):
        return self.model_version_is_supported[LADMNames.SUPPLIES_INTEGRATION_MODEL_PREFIX]

    def supplies_model_exists(self):
        return self.model_version_is_supported[LADMNames.SUPPLIES_MODEL_PREFIX]

    def ladm_col_model_exists(self, model_prefix):
        return self.model_version_is_supported[model_prefix] if model_prefix in self.model_version_is_supported else False

    def at_least_one_ladm_col_model_exists(self):
        return True in self.model_version_is_supported.values()

    def _get_models(self):
        return self._db.get_models()
