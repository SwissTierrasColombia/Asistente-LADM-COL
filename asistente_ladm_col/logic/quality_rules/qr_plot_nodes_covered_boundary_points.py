"""
/***************************************************************************
                              Asistente LADM-COL
                             --------------------
        begin           : 2022-06-20
        git sha         : :%H$
        copyright       : (C) 2021 by Germán Carrillo (SwissTierras Colombia)
                          (C) 2022 by Sergio Ramírez (SwissTierras Colombia)
        email           : gcarrillo@linuxmail.org
                          sramirez@colsolutions.com
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
from asistente_ladm_col.config.keys.common import (QUALITY_RULE_LADM_COL_LAYERS,
                                                   QUALITY_RULE_ADJUSTED_LAYERS,
                                                   ADJUSTED_INPUT_LAYER,
                                                   ADJUSTED_REFERENCE_LAYER)
from asistente_ladm_col.config.layer_config import LADMNames
from asistente_ladm_col.config.quality_rule_config import (QR_IGACR3008,
                                                           QRE_IGACR3008E01)
from asistente_ladm_col.core.quality_rules.abstract_point_quality_rule import AbstractPointQualityRule
from asistente_ladm_col.core.quality_rules.quality_rule_execution_result import QualityRuleExecutionResult
from asistente_ladm_col.lib.geometry import GeometryUtils
from asistente_ladm_col.logic.ladm_col.ladm_data import LADMData


class QRPlotNodesCoveredBoundaryPoints(AbstractPointQualityRule):
    """
    Check that plot nodes must be covered by boundary points
    """
    _ERROR_01 = QRE_IGACR3008E01

    def __init__(self):
        AbstractPointQualityRule.__init__(self)

        self._id = QR_IGACR3008
        self._name = "Los nodos de terreno deben estar cubiertos por puntos de lindero"
        self._tags = ["igac", "instituto geográfico agustín codazzi", "puntos", "nodos de terreno", "cobertura"]
        self._models = [LADMNames.SURVEY_MODEL_KEY]

        self._errors = {self._ERROR_01: "Los nodos de terreno deben estar cubiertos por puntos de lindero"}

        # Optional. Only useful for display purposes.
        self._field_mapping = dict()  # E.g., {'id_objetos': 'ids_punto_lindero', 'valores': 'conteo'}

    def field_mapping(self, names):
        return {names.ERR_QUALITY_ERROR_T_OBJECT_IDS_F: QCoreApplication.translate("QualityRules", "Plot nodes")}

    def layers_config(self, names):
        return {
            QUALITY_RULE_LADM_COL_LAYERS: [names.LC_BOUNDARY_POINT_T,
                                           names.LC_PLOT_T],
            QUALITY_RULE_ADJUSTED_LAYERS: {
                names.LC_BOUNDARY_POINT_T: {
                    ADJUSTED_INPUT_LAYER: names.LC_BOUNDARY_POINT_T,
                    ADJUSTED_REFERENCE_LAYER: names.LC_BOUNDARY_POINT_T},
                names.LC_PLOT_T: {
                    ADJUSTED_INPUT_LAYER: names.LC_PLOT_T,
                    ADJUSTED_REFERENCE_LAYER: names.LC_PLOT_T}
            }
        }

    def _validate(self, db, db_qr, layer_dict, tolerance, **kwargs):
        self.progress_changed.emit(5)

        pre_res, res_obj = self._check_prerrequisite_layers(layer_dict)
        if not pre_res:
            return res_obj

        point_layer = self._get_layer(layer_dict, db.names.LC_BOUNDARY_POINT_T)
        plot_layer = self._get_layer(layer_dict, db.names.LC_PLOT_T)
        
        plot_nodes = GeometryUtils.get_polygon_nodes_layer(plot_layer, db.names.T_ILI_TID_F)
        not_covered_points = GeometryUtils.get_non_intersecting_geometries(plot_nodes, point_layer, db.names.T_ILI_TID_F)
        flat_result = [fid for items in not_covered_points for fid in items]  # Build a flat list of ids
        count = len(flat_result)

        self.progress_changed.emit(70)

        error_state = LADMData().get_domain_code_from_value(db_qr, db_qr.names.ERR_ERROR_STATE_D,
                                                            LADMNames.ERR_ERROR_STATE_D_ERROR_V)

        errors = {'geometries': list(), 'data': list()}
        for point in not_covered_points:
            
            errors['geometries'].append(point[1])

            error_data = [  # [obj_uuids, rel_obj_uuids, values, details, state]
                [str(point[0])],
                None,
                None,
                self._errors[self._ERROR_01],
                error_state]
            errors['data'].append(error_data)

        self._save_errors(db_qr, self._ERROR_01, errors)

        self.progress_changed.emit(100)

        if count > 0:
            return QualityRuleExecutionResult(EnumQualityRuleResult.ERRORS,
                                              QCoreApplication.translate("QualityRules",
                                                                         "{} plot nodes that aren't covered by boundary points!").format(
                                                  count),
                                              len(errors['data']))
        else:
            return QualityRuleExecutionResult(EnumQualityRuleResult.SUCCESS,
                                              QCoreApplication.translate("QualityRules",
                                                                         "All plot nodes are covered by boundary points!"))