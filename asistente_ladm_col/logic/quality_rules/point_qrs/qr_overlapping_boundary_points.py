"""
/***************************************************************************
                              Asistente LADM-COL
                             --------------------
        begin           : 2021-11-09
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
import json

from qgis.PyQt.QtCore import QCoreApplication

from asistente_ladm_col.config.enums import EnumQualityRuleResult
from asistente_ladm_col.config.keys.common import (QUALITY_RULE_LADM_COL_LAYERS,
                                                   QUALITY_RULE_ADJUSTED_LAYERS,
                                                   ADJUSTED_INPUT_LAYER,
                                                   ADJUSTED_REFERENCE_LAYER)
from asistente_ladm_col.config.layer_config import LADMNames
from asistente_ladm_col.config.quality_rule_config import (QR_IGACR1001,
                                                           QRE_IGACR1001E01)
from asistente_ladm_col.core.quality_rules.abstract_point_quality_rule import AbstractPointQualityRule
from asistente_ladm_col.core.quality_rules.quality_rule_execution_result import QualityRuleExecutionResult
from asistente_ladm_col.lib.geometry import GeometryUtils
from asistente_ladm_col.logic.ladm_col.ladm_data import LADMData


class QROverlappingBoundaryPoints(AbstractPointQualityRule):
    """
    Check that boundary points do not overlap
    """
    _ERROR_01 = QRE_IGACR1001E01

    def __init__(self):
        AbstractPointQualityRule.__init__(self)

        self._id = QR_IGACR1001
        self._name = "Los puntos de lindero no deben superponerse"
        self._tags = ["igac", "instituto geográfico agustín codazzi", "puntos", "punto lindero", "superposición"]
        self._models = [LADMNames.SURVEY_MODEL_KEY]

        self._errors = {self._ERROR_01: "Los puntos de lindero no deben superponerse"}

        # Optional. Only useful for display purposes.
        self._field_mapping = dict()  # E.g., {'id_objetos': 'ids_punto_lindero', 'valores': 'conteo'}

    def field_mapping(self, names):
        return {names.ERR_QUALITY_ERROR_T_OBJECT_IDS_F: QCoreApplication.translate("QualityRules", "Boundary Points")}

    def layers_config(self, names):
        return {
            QUALITY_RULE_LADM_COL_LAYERS: [names.LC_BOUNDARY_POINT_T],
            QUALITY_RULE_ADJUSTED_LAYERS: {
                names.LC_BOUNDARY_POINT_T: {
                    ADJUSTED_INPUT_LAYER: names.LC_BOUNDARY_POINT_T,
                    ADJUSTED_REFERENCE_LAYER: names.LC_BOUNDARY_POINT_T}
            }
        }

    def _validate(self, db, db_qr, layer_dict, tolerance, **kwargs):
        self.progress_changed.emit(5)

        point_layer = self._get_layer(layer_dict)
        pre_res, res_obj = self._check_prerrequisite_layer(QCoreApplication.translate("QualityRules", "Boundary point"), point_layer)
        if not pre_res:
            return res_obj

        overlapping = GeometryUtils.get_overlapping_points(point_layer)
        flat_overlapping = [fid for items in overlapping for fid in items]  # Build a flat list of ids

        self.progress_changed.emit(70)

        dict_uuids = {f.id(): f[db.names.T_ILI_TID_F] for f in point_layer.getFeatures(flat_overlapping)}
        error_state = LADMData().get_domain_code_from_value(db_qr, db_qr.names.ERR_ERROR_STATE_D,
                                                            LADMNames.ERR_ERROR_STATE_D_ERROR_V)

        errors = {'geometries': list(), 'data': list()}
        for items in overlapping:
            # We need a feature geometry, pick the first id to get it
            feature = point_layer.getFeature(items[0])
            errors['geometries'].append(feature.geometry())

            error_data = [  # [obj_uuids, rel_obj_uuids, values, details, state]
                [str(dict_uuids.get(i)) for i in items],
                None,
                json.dumps({"conteo": len(items)}),
                None,
                error_state]
            errors['data'].append(error_data)

        self._save_errors(db_qr, self._ERROR_01, errors)

        count = len(flat_overlapping) > 0

        if count > 0:
            res_type = EnumQualityRuleResult.ERRORS
            msg = QCoreApplication.translate("QualityRules","{} overlapping boundary points were found!").format(count)
        else:
            res_type = EnumQualityRuleResult.SUCCESS
            msg = QCoreApplication.translate("QualityRules", "There are no overlapping boundary points.")

        self.progress_changed.emit(100)

        return QualityRuleExecutionResult(res_type, msg, count)
