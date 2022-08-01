"""
/***************************************************************************
                              Asistente LADM-COL
                             --------------------
        begin           : 2022-06-15
        git sha         : :%H$
        copyright       : (C) 2022 by Germán Carrillo (SwissTierras Colombia)
                          (C) 2022 by Leo Cardona (SwissTierras Colombia)
        email           : gcarrillo@linuxmail.org
                          contacto@ceicol.com
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
from asistente_ladm_col.config.quality_rule_config import (QR_IGACR4012,
                                                           QRE_IGACR4012E01)
from asistente_ladm_col.core.quality_rules.abstract_logic_quality_rule import AbstractLogicQualityRule
from asistente_ladm_col.core.quality_rules.quality_rule_execution_result import QualityRuleExecutionResult
from asistente_ladm_col.logic.ladm_col.ladm_data import LADMData


class QRDuplicateSurveyPointRecords(AbstractLogicQualityRule):
    """
    Check that boundary point don't have duplicate records
    """
    _ERROR_01 = QRE_IGACR4012E01  # Boundary with duplicate records

    def __init__(self):
        AbstractLogicQualityRule.__init__(self)

        self._id = QR_IGACR4012
        self._name = "Punto de Levantamiento no debe tener registros duplicados"
        self._tags = ["igac", "instituto geográfico agustín codazzi", "lógica", "negocio", "punto levantamiento", "duplicado"]
        self._models = [LADMNames.SURVEY_MODEL_KEY]

        self._errors = {self._ERROR_01: "Punto de Levantamiento no debe tener registros repetidos"}

        # Optional. Only useful for display purposes.
        self._field_mapping = dict()  # E.g., {'id_objetos': 'ids_punto_lindero', 'valores': 'conteo'}

    def layers_config(self, names):
        return {QUALITY_RULE_LADM_COL_LAYERS: [names.LC_SURVEY_POINT_T]}

    def _validate(self, db, db_qr, layer_dict, tolerance, **kwargs):
        self.progress_changed.emit(5)
        ladm_queries = self._get_ladm_queries(db.engine)

        pre_res, pre_obj = self._check_prerrequisite_layers(layer_dict)
        if not pre_res:
            return pre_obj

        table = db.names.LC_SURVEY_POINT_T
        fields = [db.names.LC_SURVEY_POINT_T_SURVEY_POINT_TYPE_F,
                  db.names.LC_SURVEY_POINT_T_PHOTO_IDENTIFICATION_F,
                  db.names.LC_SURVEY_POINT_T_VERTICAL_ACCURACY_F,
                  db.names.LC_SURVEY_POINT_T_HORIZONTAL_ACCURACY_F,
                  db.names.COL_POINT_T_INTERPOLATION_POSITION_F,
                  db.names.COL_POINT_T_PRODUCTION_METHOD_F,
                  db.names.LC_SURVEY_POINT_T_POINT_TYPE_F,
                  db.names.COL_POINT_T_ORIGINAL_LOCATION_F]

        res, records = ladm_queries.get_duplicate_records_in_table(db, table, fields)
        count = len(records)

        self.progress_changed.emit(50)

        if res:
            error_state = LADMData().get_domain_code_from_value(db_qr, db_qr.names.ERR_ERROR_STATE_D,
                                                                LADMNames.ERR_ERROR_STATE_D_ERROR_V)
            errors = {'geometries': list(), 'data': list()}
            for record in records:
                error_data = [  # [obj_uuids, rel_obj_uuids, values, details, state]
                    record['duplicate_uuids'].split(','),
                    None,
                    None,
                    'Punto levantamiento repetido {} veces'.format(record['duplicate_total']),
                    error_state]
                errors['data'].append(error_data)

            self._save_errors(db_qr, self._ERROR_01, errors)

        self.progress_changed.emit(85)

        if count > 0:
            res_type = EnumQualityRuleResult.ERRORS
            msg = QCoreApplication.translate("QualityRules", "{} survey points "
                                                             "with duplicate records were found.").format(count)
        else:
            res_type = EnumQualityRuleResult.SUCCESS
            msg = QCoreApplication.translate("QualityRules", "No duplicate survey points were found.")

        self.progress_changed.emit(100)

        return QualityRuleExecutionResult(res_type, msg, count)
