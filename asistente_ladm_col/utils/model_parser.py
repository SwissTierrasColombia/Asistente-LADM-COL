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

from ..config.general_config import (OPERATION_MODEL_PREFIX,
                                     LATEST_OPERATION_MODEL_VERSION_SUPPORTED,
                                     CADASTRAL_FORM_MODEL_PREFIX,
                                     VALUATION_MODEL_PREFIX)
from ..utils.qgis_model_baker_utils import QgisModelBakerUtils
from ..utils.utils import is_version_valid


class ModelParser(QObject):
    def __init__(self, db):
        QObject.__init__(self)
        self.debug = False

        self.current_version_operation_model = None
        self.current_version_cadastral_form_model = None
        self.current_version_valuation_model = None

        self._db = db
        qgis_model_baker_utils = QgisModelBakerUtils()
        self._pro_gen_db_connector = qgis_model_baker_utils.get_model_baker_db_connection(self._db)

        if self._pro_gen_db_connector:
            model_records = self._get_models()
            if self.debug:
                print("Models:", model_records)
            for record in model_records:
                # Models are stored in the DB in this format: Avaluos_V2_9_6{ Operacion_V2_9_6 LADM_COL_V1_2 ISO19107_PLANAS_V1}
                current_model_name = record['modelname'].split("{")[0]  # e.g., Avaluos_V2_9_6

                if current_model_name.startswith(OPERATION_MODEL_PREFIX):
                    parts = current_model_name.split(OPERATION_MODEL_PREFIX)
                    if len(parts) > 1:
                        self.current_version_operation_model = self.parse_version(parts[1])
                if current_model_name.startswith(CADASTRAL_FORM_MODEL_PREFIX):
                    parts = current_model_name.split(CADASTRAL_FORM_MODEL_PREFIX)
                    if len(parts) > 1:
                        self.current_version_cadastral_form_model = self.parse_version(parts[1])
                if current_model_name.startswith(VALUATION_MODEL_PREFIX):
                    parts = current_model_name.split(CADASTRAL_FORM_MODEL_PREFIX)
                    if len(parts) > 1:
                        self.current_version_valuation_model = self.parse_version(parts[1])

    def parse_version(self, str_version):
        """ E.g., V2_9_6 -> 2.9.6 """
        return ".".join(str_version.replace("V", "").split("_"))

    def validate_cadastre_model_version(self):
        if self.debug:
            print("Cadastre model:", self.cadastre_model)

        if self.current_version_operation_model is None:
            return (False, QCoreApplication.translate("ModelParser",
                                                      "We couldn't determine the version of the 'Operation' model. Are you sure the database (or schema) has the 'Operation' model structure?"))

        if self._pro_gen_db_connector is None:
            return (False, QCoreApplication.translate("ModelParser",
                                                      "The plugin 'QGIS Model Baker' is a prerequisite, but could not be found. Install it before continuing."))

        if self.debug:
            print("Current Operation model's latest version:", self.current_version_cadastral_form_model)

        res = is_version_valid(
                self.current_version_operation_model,
                LATEST_OPERATION_MODEL_VERSION_SUPPORTED,
                False,  # Exact version required
                QCoreApplication.translate("ModelParser", "Operation Model"))
        if not res:
            return (False, QCoreApplication.translate("ModelParser", "The 'Operation' model version found in the database ({}) is not supported (it is lesser than {})!").format(
                self.current_version_operation_model,
                LATEST_OPERATION_MODEL_VERSION_SUPPORTED))

        return (True, QCoreApplication.translate("ModelParser", "Supported model version!"))

    def cadastral_form_model_exists(self):
        return self.current_version_cadastral_form_model is not None

    def valuation_model_exists(self):
        return self.current_version_valuation_model is not None

    def _get_models(self):
        return self._pro_gen_db_connector.get_models()
