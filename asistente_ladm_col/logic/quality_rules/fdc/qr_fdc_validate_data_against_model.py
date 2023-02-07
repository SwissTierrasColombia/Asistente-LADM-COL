"""
/***************************************************************************
                              Asistente LADM-COL
                             --------------------
        begin           : 2021-11-12
        git sha         : :%H$
        copyright       : (C) 2021 by Germán Carrillo (SwissTierras Colombia)
        email           : gcarrillo@linuxmail.org
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""
import os.path
import time
import tempfile

from qgis.PyQt.QtCore import QCoreApplication

from asistente_ladm_col.config.enums import (EnumQualityRuleType,
                                             EnumQualityRuleResult)
from asistente_ladm_col.config.layer_config import LADMNames
from asistente_ladm_col.config.quality_rule_config import (QR_FDCILIVALIDATORR0001,
                                                           QRE_FDCILIVALIDATORR0001E01,
                                                           QR_NAME,
                                                           QR_ERROR)
from asistente_ladm_col.core.ili2db import Ili2DB
from asistente_ladm_col.core.quality_rules.abstract_quality_rule import AbstractQualityRule
from asistente_ladm_col.core.quality_rules.quality_rule_execution_result import QualityRuleExecutionResult
from asistente_ladm_col.lib.model_registry import LADMColModelRegistry
from asistente_ladm_col.logic.xtf_model_converter.iliverrors_to_errores_calidad_0_1_converter import IliVErrorsToErroresCalidad01Converter


class QRFDCValidateDataAgainstModel(AbstractQualityRule):
    """
    Check that the DB data is valid against their model.
    Note: This uses ili2db --validate rather than iliValidator.
    """
    _ERROR_01 = QRE_FDCILIVALIDATORR0001E01

    def __init__(self):
        AbstractQualityRule.__init__(self)

        self._id = QR_FDCILIVALIDATORR0001
        self._name = "Los datos deben corresponder a su modelo (iliValidator)"
        self._type = EnumQualityRuleType.GENERIC
        self._tags = ["ilivalidator", "modelo", "datos", "integridad"]
        self._models = [LADMNames.FIELD_DATA_CAPTURE_MODEL_KEY]

        self._errors = {self._ERROR_01: "Errores de integridad de los datos respecto al modelo"}

        # Optional. Only useful for display purposes.
        self._field_mapping = dict()  # E.g., {'id_objetos': 'ids_punto_lindero', 'valores': 'conteo'}

        self._xtf_log = os.path.join(tempfile.gettempdir(), "validation_fdc_{}.xtf".format(time.strftime('%Y%m%d_%H%M%S')))

    def layers_config(self, names):
        return dict()

    def _validate(self, db, db_qr, layer_dict, tolerance, **kwargs):
        self.progress_changed.emit(5)
        # First, run an ili2db --validate on the data
        model = LADMColModelRegistry().model(LADMNames.FIELD_DATA_CAPTURE_MODEL_KEY)
        res, msg = Ili2DB().validate(db, [model.full_name()], self._xtf_log)

        if not res:
            return QualityRuleExecutionResult(EnumQualityRuleResult.CRITICAL,
                                              QCoreApplication.translate("QualityRules",
                                                                         "There was an error running the quality rule '{}'! Details: '{}'.").format(
                self._id, msg))

        self.progress_changed.emit(85)

        error_layer = self.app.core.get_layer(db_qr, db_qr.names.ERR_QUALITY_ERROR_T, load=True)
        count_before = error_layer.featureCount()

        # Write errors to QR DB
        params = {
            QR_NAME: QR_FDCILIVALIDATORR0001,
            QR_ERROR: QRE_FDCILIVALIDATORR0001E01
        }

        res, msg = IliVErrorsToErroresCalidad01Converter().convert(self._xtf_log, db_qr, params)

        self.progress_changed.emit(100)

        if not res:
            return QualityRuleExecutionResult(EnumQualityRuleResult.CRITICAL,
                                              QCoreApplication.translate("QualityRules",
                                                                         "There was an error running the quality rule '{}'! Details: '{}'.")).format(
                self._id, msg)
        else:
            count = error_layer.featureCount() - count_before
            if count:
                return QualityRuleExecutionResult(EnumQualityRuleResult.ERRORS,
                                                  QCoreApplication.translate("QualityRules",
                                                                             "There were {} errors validating the data against their model!").format(
                                                      count),
                                                  count)
            else:
                return QualityRuleExecutionResult(EnumQualityRuleResult.SUCCESS,
                                                  QCoreApplication.translate("QualityRules",
                                                                             "The data comply with their model."))
