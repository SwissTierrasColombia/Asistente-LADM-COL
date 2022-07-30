"""
/***************************************************************************
                              Asistente LADM-COL
                             --------------------
        begin           : 2022-07-08
        git sha         : :%H$
        copyright       : (C) 2021 by Germán Carrillo (SwissTierras Colombia)
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
from qgis.PyQt.QtCore import QCoreApplication

from asistente_ladm_col.config.enums import EnumQualityRuleResult
from asistente_ladm_col.config.keys.common import QUALITY_RULE_LADM_COL_LAYERS
from asistente_ladm_col.config.layer_config import LADMNames
from asistente_ladm_col.config.quality_rule_config import (QR_IGACR3007,
                                                           QRE_IGACR3007E01)
from asistente_ladm_col.core.quality_rules.abstract_polygon_quality_rule import AbstractPolygonQualityRule
from asistente_ladm_col.core.quality_rules.quality_rule_execution_result import QualityRuleExecutionResult

from asistente_ladm_col.lib.geometry import GeometryUtils
from asistente_ladm_col.logic.ladm_col.ladm_data import LADMData


class QRMultiPartsInRightOfWay(AbstractPolygonQualityRule):
    """
    Check that rights of way don't have multipart geometries
    """
    _ERROR_01 = QRE_IGACR3007E01

    def __init__(self):
        AbstractPolygonQualityRule.__init__(self)

        self._id = QR_IGACR3007
        self._name = "Las servidumbres de tránsito no deben tener geometrías multiparte"
        self._tags = ["igac", "instituto geográfico agustín codazzi", "polígonos", "servidumbre tránsito", "multiparte"]
        self._models = [LADMNames.SURVEY_MODEL_KEY]

        self._errors = {self._ERROR_01: "La servidumbre de tránsito no debe tener geometría multiparte"}

        # Optional. Only useful for display purposes.
        self._field_mapping = dict()  # E.g., {'id_objetos': 'ids_punto_lindero', 'valores': 'conteo'}

    def field_mapping(self, names):
        return {names.ERR_QUALITY_ERROR_T_OBJECT_IDS_F: QCoreApplication.translate("QualityRules", "Right of way")}

    def layers_config(self, names):
        return {
            QUALITY_RULE_LADM_COL_LAYERS: [names.LC_RIGHT_OF_WAY_T]
        }

    def _validate(self, db, db_qr, layer_dict, tolerance, **kwargs):
        self.progress_changed.emit(5)

        right_of_way_layer = self._get_layer(layer_dict)
        pre_res, res_obj = self._check_prerrequisite_layer(QCoreApplication.translate("QualityRules", "Right of way"),
                                                           right_of_way_layer)
        if not pre_res:
            return res_obj

        self.progress_changed.emit(10)
        multi_parts, right_of_way_ids = GeometryUtils.get_multipart_geoms(right_of_way_layer)
        self.progress_changed.emit(70)

        error_state = LADMData().get_domain_code_from_value(db_qr, db_qr.names.ERR_ERROR_STATE_D,
                                                            LADMNames.ERR_ERROR_STATE_D_ERROR_V)

        errors = {'geometries': list(), 'data': list()}
        if multi_parts:
            for right_of_way_geom, right_of_way_id in zip(multi_parts, right_of_way_ids):
                errors['geometries'].append(right_of_way_geom)
                error_data = [  # [obj_uuids, rel_obj_uuids, values, details, state]
                    [right_of_way_layer.getFeature(right_of_way_id)[db.names.T_ILI_TID_F]],
                    None,
                    None,
                    self._errors[self._ERROR_01],
                    error_state]
                errors['data'].append(error_data)

            self._save_errors(db_qr, self._ERROR_01, errors)
            self.progress_changed.emit(90)

        count = len(errors['data'])

        if count > 0:
            res_type = EnumQualityRuleResult.ERRORS
            msg = QCoreApplication.translate("QualityRules", "{} rights of way with "
                                                             "multipart geometry were found.").format(count)
        else:
            res_type = EnumQualityRuleResult.SUCCESS
            msg = QCoreApplication.translate("QualityRules", "All rights of way have simple geometry!!")

        self.progress_changed.emit(100)

        return QualityRuleExecutionResult(res_type, msg, count)
