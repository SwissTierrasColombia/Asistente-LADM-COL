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

from asistente_ladm_col.config.ladm_names import LADMNames
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.lib.model_registry import LADMColModelRegistry
from asistente_ladm_col.utils.utils import is_version_valid


class ModelParser(QObject):
    """
    Assembles both Role supported models (known as registered models) and
    models found in the DB to answer questions about the existence of a
    registered model in the DB.
    """
    def __init__(self, db):
        QObject.__init__(self)
        self.logger = Logger()

        ladmcol_models = LADMColModelRegistry()
        self.current_model_version = {model_id: None for model_id in ladmcol_models.model_keys()}
        self.model_version_is_supported = {model_id: False for model_id in ladmcol_models.model_keys()}

        self._db = db

        # Fill versions for each model found
        for current_model_name in self._get_models():
            for model_key, v in self.current_model_version.items():
                if current_model_name.startswith(model_key):
                    parts = current_model_name.split(model_key)
                    if len(parts) > 1:
                        current_version = self.parse_version(parts[1])
                        current_version_valid = is_version_valid(current_version,
                                                                 ladmcol_models.model(model_key).supported_version(),
                                                                 True,  # Exact version required
                                                                 QCoreApplication.translate("ModelParser", model_key))
                        self.current_model_version[model_key] = current_version
                        self.model_version_is_supported[model_key] = current_version_valid
                        self.logger.debug(__name__, "Model '{}' found! Valid: {}".format(model_key, current_version_valid))
                        break

    def parse_version(self, str_version):
        """ E.g., _V2_9_6 -> 2.9.6 """
        return ".".join(str_version.replace("_V", "").split("_"))

    def survey_model_exists(self):
        return self.model_version_is_supported[LADMNames.SURVEY_MODEL_KEY]

    def valuation_model_exists(self):
        return self.model_version_is_supported[LADMNames.VALUATION_MODEL_KEY]

    def ladm_model_exists(self):
        return self.model_version_is_supported[LADMNames.LADM_COL_MODEL_KEY]

    def cadastral_cartography_model_exists(self):
        return self.model_version_is_supported[LADMNames.CADASTRAL_CARTOGRAPHY_MODEL_KEY]

    def snr_data_model_exists(self):
        return self.model_version_is_supported[LADMNames.SNR_DATA_SUPPLIES_MODEL_KEY]

    def supplies_integration_model_exists(self):
        return self.model_version_is_supported[LADMNames.SUPPLIES_INTEGRATION_MODEL_KEY]

    def supplies_model_exists(self):
        return self.model_version_is_supported[LADMNames.SUPPLIES_MODEL_KEY]

    def ladm_col_model_exists(self, model_prefix):
        return self.model_version_is_supported.get(model_prefix, False)

    def at_least_one_ladm_col_model_exists(self):
        """
        Check that all hidden_and_supported models (hidden models are supposed to be the building blocks
        of extended ones) are also supported in the DB and that there is at least one non-hidden_and_supported
        model that is supported in the DB.
        """
        hidden_model_ids = [model.id() for model in LADMColModelRegistry().hidden_and_supported_models()]
        non_hidden_model_ids = [model.id() for model in LADMColModelRegistry().non_hidden_and_supported_models()]

        hidden_models_supported = list()
        non_hidden_models_supported = list()

        for model_id, is_supported in self.model_version_is_supported.items():
            if model_id in hidden_model_ids:
                hidden_models_supported.append(is_supported)
            elif model_id in non_hidden_model_ids:
                non_hidden_models_supported.append(is_supported)

        return not (False in hidden_models_supported) and any(non_hidden_models_supported)

    def _get_models(self):
        return self._db.get_models()
