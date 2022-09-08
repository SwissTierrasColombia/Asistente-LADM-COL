"""
/***************************************************************************
                              Asistente LADM-COL
                             --------------------
        begin           : 2022-07-19
        git sha         : :%H$
        copyright       : (C) 2021 by Germán Carrillo (SwissTierras Colombia)
                          (C) 2022 by Leo Cardona (BSF Swissphoto)
        email           : gcarrillo@linuxmail.org
                          leo.cardona.p@gmail.com
 ***************************************************************************/
4/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
 """

from qgis.PyQt.QtCore import QCoreApplication

from asistente_ladm_col.config.enums import EnumQualityRuleResult
from asistente_ladm_col.config.keys.common import QUALITY_RULE_LADM_COL_LAYERS
from asistente_ladm_col.config.layer_config import LADMNames
from asistente_ladm_col.config.quality_rule_config import (QR_IGACR4002,
                                                           QRE_IGACR4002E01)
from asistente_ladm_col.core.quality_rules.abstract_logic_quality_rule import AbstractLogicQualityRule
from asistente_ladm_col.core.quality_rules.quality_rule_execution_result import QualityRuleExecutionResult
from asistente_ladm_col.logic.ladm_col.ladm_data import LADMData
from asistente_ladm_col.utils.utils import get_uuid_dict


class QRGroupPartyPercentageThatDoNotMakeOne(AbstractLogicQualityRule):
    """
    Check that the sum of the participation of the group party adds up to one
    """
    _ERROR_01 = QRE_IGACR4002E01  # The participation of a group party does not add up to one.

    def __init__(self):
        AbstractLogicQualityRule.__init__(self)

        self._id = QR_IGACR4002
        self._name = "Los porcentajes de participación de la agrupación de interesados deben sumar uno"
        self._tags = ["igac", "instituto geográfico agustín codazzi", "lógica", "negocio", "agrupación de interesados",
                      "porcentaje de participación"]
        self._models = [LADMNames.SURVEY_MODEL_KEY]

        self._errors = {self._ERROR_01: "Los porcentajes de participación de la agrupación de interesados deben sumar uno"}

        # Optional. Only useful for display purposes.
        self._field_mapping = dict()  # E.g., {'id_objetos': 'ids_punto_lindero', 'valores': 'conteo'}

    def layers_config(self, names):
        return {QUALITY_RULE_LADM_COL_LAYERS: [names.MEMBERS_T,
                                               names.LC_GROUP_PARTY_T,
                                               names.LC_PARTY_T]}

    def _validate(self, db, db_qr, layer_dict, tolerance, **kwargs):
        self.progress_changed.emit(5)
        ladm_queries = self._get_ladm_queries(db.engine)

        pre_res, res_obj = self._check_prerrequisite_layers(layer_dict)
        if not pre_res:
            return res_obj

        members_layer = self._get_layer(layer_dict, db.names.MEMBERS_T)
        group_party_layer = self._get_layer(layer_dict, db.names.LC_GROUP_PARTY_T)
        party_layer = self._get_layer(layer_dict, db.names.LC_PARTY_T)

        dict_uuid_party = get_uuid_dict(party_layer, db.names, db.names.T_ID_F)
        dict_uuid_group_party = get_uuid_dict(group_party_layer, db.names, db.names.T_ID_F)

        error_state = None

        res, records = ladm_queries.get_group_party_fractions_that_do_not_make_one(db)
        count = len(records)

        self.progress_changed.emit(50)

        if res:
            error_state = LADMData().get_domain_code_from_value(db_qr, db_qr.names.ERR_ERROR_STATE_D,
                                                                LADMNames.ERR_ERROR_STATE_D_ERROR_V)
            errors = {'geometries': list(), 'data': list()}
            for record in records:
                error_data = [  # [obj_uuids, rel_obj_uuids, values, details, state]
                    [dict_uuid_group_party.get(record['agrupacion'])],
                    [str(dict_uuid_party.get(int(t_id))) for t_id in record['interesados'].split(',')],
                    None,
                    'Los porcentajes de participación de la agrupación de interesados no suma uno ({})'.format(record['suma_participacion']),
                    error_state]
                errors['data'].append(error_data)

            self._save_errors(db_qr, self._ERROR_01, errors)

        self.progress_changed.emit(85)

        if count > 0:
            res_type = EnumQualityRuleResult.ERRORS
            msg = QCoreApplication.translate("QualityRules",
                                             "{} group parties participations not add up to one.").format(count)
        else:
            res_type = EnumQualityRuleResult.SUCCESS
            msg = QCoreApplication.translate("QualityRules", "All group parties participations add up to one.")

        self.progress_changed.emit(100)

        return QualityRuleExecutionResult(res_type, msg, count)
