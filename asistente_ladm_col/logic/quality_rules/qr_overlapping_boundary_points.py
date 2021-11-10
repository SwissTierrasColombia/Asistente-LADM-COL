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
from asistente_ladm_col.core.quality_rules.abstract_quality_rule import AbstractQualityRule
from asistente_ladm_col.core.quality_rules.quality_rule_execution_result import QualityRuleExecutionResult
from asistente_ladm_col.lib.geometry import GeometryUtils


class QROverlappingBoundaryPoints(AbstractQualityRule):
    """
    Check that boundary points do not overlap
    """
    _ERROR_01 = "IGAC-R1001-E01"

    def __init__(self):
        AbstractQualityRule.__init__(self)

        self._id = "IGAC-R1001"
        self._name = "Los puntos de lindero no deben superponerse"
        self._type = EnumQualityRuleType.POINT

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
        layer_name = list(layer_dict[QUALITY_RULE_LAYERS].keys())[0] if layer_dict[QUALITY_RULE_LAYERS] else None
        point_layer = list(layer_dict[QUALITY_RULE_LAYERS].values())[0] if layer_dict[QUALITY_RULE_LAYERS] else None
        if not point_layer:
            return QualityRuleExecutionResult(Qgis.Critical,
                                              QCoreApplication.translate("QualityRules",
                                                                         "'{}' layer not found!").format(
                                                  layer_name))

        if point_layer.featureCount() == 0:
            return QualityRuleExecutionResult(Qgis.Warning,
                                              QCoreApplication.translate("QualityRules",
                                                                         "There are no points in layer '{}' to check for overlaps!").format(
                                                  layer_name))

        else:
            overlapping = GeometryUtils.get_overlapping_points(point_layer)
            flat_overlapping = [fid for items in overlapping for fid in items]  # Build a flat list of ids

            dict_uuids = {f.id(): f[db.names.T_ILI_TID_F] for f in point_layer.getFeatures(flat_overlapping)}

            errors = []
            for items in overlapping:
                # We need a feature geometry, pick the first id to get it
                feature = point_layer.getFeature(items[0])
                error_data = [
                    feature.geometry(),
                    [str(dict_uuids.get(i)) for i in items],
                    len(items)]

                errors.append(error_data)

            self._save_errors(db_qr, self._ERROR_01, errors)

            if len(errors) > 0:
                return QualityRuleExecutionResult(Qgis.Critical,
                                                  QCoreApplication.translate("QualityRules",
                                                                             "{} overlapping points were found in '{}'!").format(
                                                      len(errors), layer_name),
                                                  )
            else:
                return QualityRuleExecutionResult(Qgis.Success,
                                                  QCoreApplication.translate("QualityRules",
                                                                             "There are no overlapping points in layer '{}'!").format(
                                                      layer_name))
