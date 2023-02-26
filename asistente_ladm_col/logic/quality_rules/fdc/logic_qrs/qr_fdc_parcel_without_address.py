"""
/***************************************************************************
                              Asistente LADM-COL
                             --------------------
        begin           : 2022-06-22
        git sha         : :%H$
        copyright       : (C) 2023 by Leo Cardona (SwissTierras Colombia)
        email           : contacto@ceicol.com
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
from asistente_ladm_col.config.quality_rule_config import (QR_FDCR4017,
                                                           QRE_FDCR4017E01)
from asistente_ladm_col.core.quality_rules.abstract_logic_quality_rule import AbstractLogicQualityRule
from asistente_ladm_col.core.quality_rules.quality_rule_execution_result import QualityRuleExecutionResult
from asistente_ladm_col.logic.ladm_col.ladm_data import LADMData
from asistente_ladm_col.logic.queries.query_manager import QueryManager


class QRFDCParcelWithoutAddress(AbstractLogicQualityRule):
    """
    This quality rule validates that the condition of the parcel is not null
    """
    _ERROR_01 = QRE_FDCR4017E01  # Condition of the parcel is null

    def __init__(self):
        AbstractLogicQualityRule.__init__(self)

        self._id = QR_FDCR4017
        self._name = "Predio sin dirección asociada"
        self._tags = ["fdc", "captura", "campo", "lógica", "negocio", "predio", "sin dirección"]
        self._models = [LADMNames.FIELD_DATA_CAPTURE_MODEL_KEY]

        self._errors = {self._ERROR_01: "La condición de predio no puede ser null"}

        # Optional. Only useful for display purposes.
        self._field_mapping = dict()  # E.g., {'id_objetos': 'ids_punto_lindero', 'valores': 'conteo'}

    def layers_config(self, names):
        return {QUALITY_RULE_LADM_COL_LAYERS: [names.FDC_PARCEL_T]}

    def _validate(self, db, db_qr, layer_dict, tolerance, **kwargs):
        self.progress_changed.emit(5)

        query_manager = QueryManager()

        query = query_manager.get_query("ParcelWithoutAssociatedAddress", db)

        pre_res, pre_obj = self._check_prerrequisite_layers(layer_dict)
        if not pre_res:
            return pre_obj

        res, records = query.execute(db)
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
                    'Predio sin dirección asociada',
                    error_state]
                errors['data'].append(error_data)

            self._save_errors(db_qr, self._ERROR_01, errors)

        self.progress_changed.emit(85)

        if count > 0:
            res_type = EnumQualityRuleResult.ERRORS
            msg = QCoreApplication.translate("QualityRules", "{} parcels without associated address were found.").format(count)
        else:
            res_type = EnumQualityRuleResult.SUCCESS
            msg = QCoreApplication.translate("QualityRules", "All parcels have associated address.")

        self.progress_changed.emit(100)

        return QualityRuleExecutionResult(res_type, msg, count)
