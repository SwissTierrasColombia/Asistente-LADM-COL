"""
/***************************************************************************
                              Asistente LADM-COL
                             --------------------
        begin           : 2023-02-03
        git sha         : :%H$
        copyright       : (C) 2023 by Yesid Polania (CEICOL SAS)
        email           : yesidpol3@gmail.com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""
from asistente_ladm_col.config.enums import EnumQualityRuleResult
from asistente_ladm_col.config.keys.common import QUALITY_RULE_LADM_COL_LAYERS
from asistente_ladm_col.config.layer_config import LADMNames
from asistente_ladm_col.core.quality_rules.abstract_logic_quality_rule import AbstractLogicQualityRule
from asistente_ladm_col.core.quality_rules.quality_rule_execution_result import QualityRuleExecutionResult
from asistente_ladm_col.logic.ladm_col.ladm_data import LADMData


class QRFDCSimpleMandatory(AbstractLogicQualityRule):
    """
    This quality rule validates that the type of the parcel is not null
    """

    def __init__(self, config: dict):
        AbstractLogicQualityRule.__init__(self)

        self._id = config['id']
        self._name = config['name']
        self._tags = config['tags']
        self._models = [LADMNames.FIELD_DATA_CAPTURE_MODEL_KEY]
        self._errors = {config['error']['code']: config['error']['message']}
        
        self._config = config

        # Optional. Only useful for display purposes.
        self._field_mapping = dict()  # E.g., {'id_objetos': 'ids_punto_lindero', 'valores': 'conteo'}

    def layers_config(self, names):
        layer_name = getattr(names, self._config['layer'])
        return {QUALITY_RULE_LADM_COL_LAYERS: [layer_name]}

    def _validate(self, db, db_qr, layer_dict, tolerance, **kwargs):
        self.progress_changed.emit(5)
        ladm_queries = self._get_ladm_queries(db.engine)

        pre_res, pre_obj = self._check_prerrequisite_layers(layer_dict)
        if not pre_res:
            return pre_obj

        cnf = self._config
        layer_name = getattr(db.names, cnf['layer'])
        field_name = getattr(db.names, cnf['field'])

        # validates that the land class  not null
        res, records = ladm_queries.get_invalid_null_values(db, layer_name, field_name)

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
                    'La clase de suelo del predio no debe ser nula',
                    error_state]
                errors['data'].append(error_data)

            self._save_errors(db_qr, cnf['error']['code'], errors)

        self.progress_changed.emit(85)

        if count > 0:
            res_type = EnumQualityRuleResult.ERRORS
            msg = cnf['notification_messages']['error'].format(count)
        else:
            res_type = EnumQualityRuleResult.SUCCESS
            msg = cnf['notification_messages']['ok']

        self.progress_changed.emit(100)

        return QualityRuleExecutionResult(res_type, msg, count)
