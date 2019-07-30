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
import re

from qgis.PyQt.QtCore import QCoreApplication

from ..config.general_config import (CADASTRE_MODEL_PREFIX,
                                     CADASTRE_MODEL_PREFIX_LEGACY,
                                     LATEST_UPDATE_FOR_SUPPORTED_MODEL_VERSION,
                                     PROPERTY_RECORD_CARD_MODEL_PREFIX, VALUATION_MODEL_PREFIX)
from ..utils.qgis_model_baker_utils import QgisModelBakerUtils


class ModelParser:
    def __init__(self, db_connector):
        self.debug = False
        self.cadastre_model = None
        self.cadastre_model_legacy = None
        self.property_record_card_model = None
        self.valuation_model = None

        self._db_connector = db_connector
        qgis_model_baker_utils = QgisModelBakerUtils()
        self._pro_gen_db_connector = qgis_model_baker_utils.get_model_baker_db_connection(self._db_connector)

        if self._pro_gen_db_connector:
            model_records = self._get_models()
            if self.debug:
                print("Models:", model_records)
            for record in model_records:
                current_model_name = record['modelname'].split("{")[0]
                if current_model_name.startswith(CADASTRE_MODEL_PREFIX):
                    self.cadastre_model = record['content']
                if current_model_name.startswith(CADASTRE_MODEL_PREFIX_LEGACY):
                    self.cadastre_model_legacy = record['content']
                if current_model_name.startswith(PROPERTY_RECORD_CARD_MODEL_PREFIX):
                    self.property_record_card_model = record['content']
                if current_model_name.startswith(VALUATION_MODEL_PREFIX):
                    self.valuation_model = record['content']

    def validate_cadastre_model_version(self):
        if self.debug:
            print("Cadastre model:", self.cadastre_model)

        if self._pro_gen_db_connector is None:
            return (False, QCoreApplication.translate("ModelParser",
                                                      "The plugin 'QGIS Model Baker' is a prerequisite, but could not be found. Install it before continuing."))

        if self.cadastre_model is None:
            if self.cadastre_model_legacy is None:
                return (False, QCoreApplication.translate("ModelParser",
                           "The Cadastre model couldn't be found in the database..."))
            else:
                self.cadastre_model = self.cadastre_model_legacy

        latest_update = self.get_latest_model_update_date()

        if self.debug:
            print("Current Cadastre model's latest update:", latest_update)

        if latest_update is None:
            # By default we will let the plugin work with the current model
            return (True, QCoreApplication.translate("ModelParser",
                "Model revision not found"))

        res, msg = self.validate_model_version(latest_update)
        if not res:
            return (False, QCoreApplication.translate("ModelParser", "The Cadastre model version found in the database is not supported!"))

        return (True, msg)

    def validate_model_version(self, current_version_found):
        latest_supported = LATEST_UPDATE_FOR_SUPPORTED_MODEL_VERSION.split('.')
        current_version = current_version_found.split('.')

        if self.debug:
            print("Latest_supported: {}, Current_version: {}".format(latest_supported, current_version))

        if len(latest_supported) != 3 or len(current_version) != 3:
            # By default we will let the plugin work with the current model
            return (True, QCoreApplication.translate("ModelParser",
                        "Couldn't determine versions to compare..."))

        # Compare dates in format dd.mm.yyyy
        #Latest_supported: ['17', '07', '2018'] --> 20180717
        #Current_version:  ['10', '08', '2018'] --> 20180810
        latest_supported.reverse()
        current_version.reverse()
        latest_supported = "".join(latest_supported)
        current_version = "".join(current_version)

        if int(latest_supported) > int(current_version):
            return (False, QCoreApplication.translate("ModelParser", "The model version is not supported!"))

        if self.debug:
            print("Validation passed...")

        return (True, QCoreApplication.translate("ModelParser", "Supported model version!"))

    def get_latest_model_update_date(self):
        re_comment = re.compile(r'\s*/\*')  # /* comment
        re_end_comment = re.compile(r'\s*\*/')  # comment */
        re_oneline_comment = re.compile(r'\s*/\*.*\*/')  # /* comment */

        # * 10.08.2018/fm: Eliminado clase Interesado Natural e Interesado Juridico
        re_update_date = re.compile(r'\s*\*\s*([0-9]{2}\.[0-9]{2}\.[0-9]{4})\/*')

        # * (c) IGAC y SNR con apoyo de la Cooperacion Suiza
        re_end_revision_history = re.compile(r'\s*\*\s*\(c\) IGAC y SNR con apoyo de la Cooperacion Suiza*')

        currently_inside_comment = False
        latest_update_date = None

        for line in self.cadastre_model.splitlines():

            if not currently_inside_comment:
                result = re_comment.search(line)
                if result:
                    result = re_oneline_comment.search(line)
                    if not result:
                        currently_inside_comment = True

                    continue
            else:
                result = re_end_comment.search(line)
                if result:
                    currently_inside_comment = False

                result = re_update_date.search(line)
                if result:
                    latest_update_date = result.group(1)

                result = re_end_revision_history.search(line)
                if result:
                    return latest_update_date

                continue # Whether comment ends or not, we are done in this line

        # Model parsed, no update date could be found
        return latest_update_date

    def property_record_card_model_exists(self):
        return self.property_record_card_model is not None

    def valuation_model_exists(self):
        return self.valuation_model is not None

    def _get_models(self):
        return self._pro_gen_db_connector.get_models()
