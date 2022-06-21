"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2022-05-04
        git sha              : :%H$
        copyright            : (C) 2022 by Leo Cardona (BSF Swissphoto)
                               (C) 2022 by Sergio Ramírez (BSF Swissphoto)
        email                : leo.cardona.p@gmail.com
                               seralra96@gmail.com

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
                              QSettings)

from asistente_ladm_col.config.enums import EnumQualityRuleResult
from asistente_ladm_col.config.keys.common import QUALITY_RULE_LADM_COL_LAYERS
from asistente_ladm_col.config.layer_config import LADMNames
from asistente_ladm_col.config.quality_rule_config import (QR_IGACR4005,
                                                           QRE_IGACR4005E01)
from asistente_ladm_col.core.quality_rules.abstract_logic_quality_rule import AbstractLogicQualityRule
from asistente_ladm_col.core.quality_rules.quality_rule_execution_result import QualityRuleExecutionResult
from asistente_ladm_col.logic.ladm_col.ladm_data import LADMData


class QRParcelWithInvalidParcelNumber(AbstractLogicQualityRule):
    """
    Check that parcel has a valid parcel number.
    """
    _ERROR_01 = QRE_IGACR4005E01  # Parcel with incorrect parcel number

    def __init__(self):
        AbstractLogicQualityRule.__init__(self)

        self._id = QR_IGACR4005
        self._name = "Revisar que el número predial tiene 30 caracteres numéricos"
        self._tags = ["igac", "instituto geográfico agustín codazzi", "lógica", "negocio", "predio", "número predial"]
        self._models = [LADMNames.SURVEY_MODEL_KEY]

        self._errors = {self._ERROR_01: "El número predial debe tener 30 caracteres numéricos"}

        # Optional. Only useful for display purposes.
        self._field_mapping = dict()  # E.g., {'id_objetos': 'ids_punto_lindero', 'valores': 'conteo'}

    def layers_config(self, names):
        return {QUALITY_RULE_LADM_COL_LAYERS: [names.LC_PARCEL_T]}

    def _validate(self, db, db_qr, layer_dict, tolerance, **kwargs):
        self.progress_changed.emit(5)
        ladm_queries = self._get_ladm_queries(db.engine)

        pre_res, pre_obj = self._check_prerrequisite_layers(layer_dict)
        if not pre_res:
            return pre_obj

        error_state = None

        # Check parcel with invalid parcel number
        res, records = ladm_queries.get_parcels_with_invalid_parcel_number(db)
        count = len(records)

        self.progress_changed.emit(50)

        if res:
            error_state = LADMData().get_domain_code_from_value(db_qr, db_qr.names.ERR_ERROR_STATE_D,
                                                                LADMNames.ERR_ERROR_STATE_D_ERROR_V)
            errors = {'geometries': list(), 'data': list()}
            for record in records:
                error_data = [  # [obj_uuids, rel_obj_uuids, values, details, state]
                    [record[db.names.T_ILI_TID_F]],
                    None,
                    None,
                    'El número predial debe tener 30 caracteres numéricos',
                    error_state]
                errors['data'].append(error_data)

            self._save_errors(db_qr, self._ERROR_01, errors)

        self.progress_changed.emit(85)

        if count > 0:
            res_type = EnumQualityRuleResult.ERRORS
            msg = QCoreApplication.translate("QualityRules", "{} parcels with invalid parcel number were found.").format(
                count)
        else:
            res_type = EnumQualityRuleResult.SUCCESS
            msg = QCoreApplication.translate("QualityRules", "All parcels have valid parcel number.")

        self.progress_changed.emit(100)

        return QualityRuleExecutionResult(res_type, msg, count)