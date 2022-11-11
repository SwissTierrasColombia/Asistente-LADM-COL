"""
/***************************************************************************
                              Asistente LADM-COL
                             --------------------
        begin           : 2021-12-13
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
from qgis.PyQt.QtCore import (QCoreApplication,
                              QSettings)

from qgis.core import QgsVectorLayer

from asistente_ladm_col.config.enums import EnumQualityRuleResult
from asistente_ladm_col.config.keys.common import QUALITY_RULE_LADM_COL_LAYERS
from asistente_ladm_col.config.layer_config import LADMNames
from asistente_ladm_col.config.quality_rule_config import (QR_IGACR4001,
                                                           QRE_IGACR4001E01,
                                                           QRE_IGACR4001E02)
from asistente_ladm_col.core.quality_rules.abstract_logic_quality_rule import AbstractLogicQualityRule
from asistente_ladm_col.core.quality_rules.quality_rule_execution_result import QualityRuleExecutionResult
from asistente_ladm_col.lib.geometry import GeometryUtils
from asistente_ladm_col.logic.ladm_col.ladm_data import LADMData


class QRParcelRightRelationship(AbstractLogicQualityRule):
    """
    Check that parcels and right relationship is consistent
    """
    _ERROR_01 = QRE_IGACR4001E01  # Parcel with no rights
    _ERROR_02 = QRE_IGACR4001E02  # More than one 'domain' right

    def __init__(self):
        AbstractLogicQualityRule.__init__(self)

        self._id = QR_IGACR4001
        self._name = "La relación entre predio y derecho debe ser consistente"
        self._tags = ["igac", "instituto geográfico agustín codazzi", "lógica", "negocio", "predio", "derecho"]
        self._models = [LADMNames.SURVEY_MODEL_KEY]

        self._errors = {self._ERROR_01: "El predio no tiene derecho asociado",
                        self._ERROR_02: "El predio tiene más de un derecho de dominio asociado"}

        # Optional. Only useful for display purposes.
        self._field_mapping = dict()  # E.g., {'id_objetos': 'ids_punto_lindero', 'valores': 'conteo'}

    def layers_config(self, names):
        return {QUALITY_RULE_LADM_COL_LAYERS: [names.LC_PARCEL_T,
                                               names.LC_RIGHT_T]}

    def _validate(self, db, db_qr, layer_dict, tolerance, **kwargs):
        self.progress_changed.emit(5)
        ladm_queries = self._get_ladm_queries(db.engine)

        pre_res, pre_obj = self._check_prerrequisite_layers(layer_dict)
        if not pre_res:
            return pre_obj

        # First error type: parcel with no rights
        res, records = ladm_queries.get_parcels_with_no_right(db)
        count_e01_records = len(records)

        self.progress_changed.emit(40)

        if res:
            error_state = LADMData().get_domain_code_from_value(db_qr, db_qr.names.ERR_ERROR_STATE_D,
                                                                LADMNames.ERR_ERROR_STATE_D_ERROR_V)
            errors = {'geometries': list(), 'data': list()}
            for record in records:
                error_data = [  # [obj_uuids, rel_obj_uuids, values, details, state]
                    [record[db.names.T_ILI_TID_F]],
                    None,
                    None,
                    self._errors[self._ERROR_01],
                    error_state]
                errors['data'].append(error_data)

            self._save_errors(db_qr, self._ERROR_01, errors)

            self.progress_changed.emit(50)

        # Second error type: parcel with more than one domain right
        res, records = ladm_queries.get_parcels_with_repeated_domain_right(db)
        count_e02_records = len(records)

        self.progress_changed.emit(85)

        if res:
            # Reuse it if present, otherwise get it
            error_state = error_state if error_state is not None else LADMData().get_domain_code_from_value(db_qr,
                                                                                                            db_qr.names.ERR_ERROR_STATE_D,
                                                                                                            LADMNames.ERR_ERROR_STATE_D_ERROR_V)
            errors = {'geometries': list(), 'data': list()}
            for record in records:
                related_objects = record['dominios'].split(";")
                error_data = [  # [obj_uuids, rel_obj_uuids, values, details, state]
                    [record[db.names.T_ILI_TID_F]],
                    related_objects,
                    None,
                    '{} (asociado a: {})'.format(self._errors[self._ERROR_02], len(related_objects)),
                    error_state]
                errors['data'].append(error_data)

            self._save_errors(db_qr, self._ERROR_02, errors)

            self.progress_changed.emit(95)

        count = count_e01_records + count_e02_records
        if count > 0:
            res_type = EnumQualityRuleResult.ERRORS
            msg = QCoreApplication.translate("QualityRules", "{} parcels with inconsistent rights were found.").format(
                count)
        else:
            res_type = EnumQualityRuleResult.SUCCESS
            msg = QCoreApplication.translate("QualityRules", "All parcels have valid right relationships.")

        self.progress_changed.emit(100)

        return QualityRuleExecutionResult(res_type, msg, count)
