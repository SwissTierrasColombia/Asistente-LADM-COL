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
from qgis.PyQt.QtCore import QCoreApplication

from qgis.core import Qgis

from asistente_ladm_col.config.enums import EnumQualityRuleType
from asistente_ladm_col.config.keys.common import (QUALITY_RULE_LAYERS,
                                                   QUALITY_RULE_LADM_COL_LAYERS,
                                                   QUALITY_RULE_ADJUSTED_LAYERS,
                                                   ADJUSTED_INPUT_LAYER,
                                                   ADJUSTED_REFERENCE_LAYER)
from asistente_ladm_col.config.layer_config import LADMNames
from asistente_ladm_col.config.quality_rule_config import (QR_IGACR1001,
                                                           QRE_IGACR1001E01)
from asistente_ladm_col.core.quality_rules.abstract_quality_rule import AbstractQualityRule
from asistente_ladm_col.core.quality_rules.quality_rule_execution_result import QualityRuleExecutionResult
from asistente_ladm_col.lib.geometry import GeometryUtils


class QROverlappingBoundaryPoints(AbstractQualityRule):
    """
    Check that boundary points do not overlap
    """
    _ERROR_01 = QRE_IGACR1001E01

    def __init__(self):
        AbstractQualityRule.__init__(self)

        self._id = QR_IGACR1001
        self._name = "Los puntos de lindero no deben superponerse"
        self._type = EnumQualityRuleType.POINT
        self._tags = ["igac", "instituto geográfico agustín codazzi", "puntos", "punto lindero", "superposición"]
        self._models = [LADMNames.SURVEY_MODEL_KEY]

        self._errors = {self._ERROR_01: "Los puntos de lindero no deben superponerse"}

        # Optional. Only useful for display purposes.
        self._field_mapping = dict()  # E.g., {'id_objetos': 'ids_punto_lindero', 'valores': 'conteo'}

    def layers_config(self, names):
        return {
            QUALITY_RULE_LADM_COL_LAYERS: [names.LC_BOUNDARY_POINT_T],
            QUALITY_RULE_ADJUSTED_LAYERS: {
                names.LC_BOUNDARY_POINT_T: {
                    ADJUSTED_INPUT_LAYER: names.LC_BOUNDARY_POINT_T,
                    ADJUSTED_REFERENCE_LAYER: names.LC_BOUNDARY_POINT_T}
            }
        }

    def validate(self, db, db_qr, layer_dict, tolerance, **kwargs):
        # TODO: emit progress values
        point_layer = list(layer_dict[QUALITY_RULE_LAYERS].values())[0] if layer_dict[QUALITY_RULE_LAYERS] else None
        if not point_layer:
            return QualityRuleExecutionResult(Qgis.Critical,
                                              QCoreApplication.translate("QualityRules",
                                                                         "'Boundary point' layer not found!"))

        if point_layer.featureCount() == 0:
            return QualityRuleExecutionResult(Qgis.Warning,
                                              QCoreApplication.translate("QualityRules",
                                                                         "There are no points in layer 'Boundary point' to check for overlaps!"))

        else:
            overlapping = GeometryUtils.get_overlapping_points(point_layer)
            flat_overlapping = [fid for items in overlapping for fid in items]  # Build a flat list of ids

            dict_uuids = {f.id(): f[db.names.T_ILI_TID_F] for f in point_layer.getFeatures(flat_overlapping)}

            errors = {'geometries': list(), 'data': list()}
            for items in overlapping:
                # We need a feature geometry, pick the first id to get it
                feature = point_layer.getFeature(items[0])
                errors['geometries'].append(feature.geometry())

                error_data = [  # [obj_uuids, rel_obj_uuids, values, details]
                    [str(dict_uuids.get(i)) for i in items],
                    None,
                    len(items),
                    None]
                errors['data'].append(error_data)

            self._save_errors(db_qr, self._ERROR_01, errors)

            if len(flat_overlapping) > 0:
                return QualityRuleExecutionResult(Qgis.Critical,
                                                  QCoreApplication.translate("QualityRules",
                                                                             "{} overlapping boundary points were found!").format(
                                                      len(flat_overlapping)))
            else:
                return QualityRuleExecutionResult(Qgis.Success,
                                                  QCoreApplication.translate("QualityRules",
                                                                             "There are no overlapping boundary points."))
