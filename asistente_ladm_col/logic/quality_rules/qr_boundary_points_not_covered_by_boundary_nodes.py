"""
/***************************************************************************
                              Asistente LADM-COL
                             --------------------
        begin           : 2022-06-22
        git sha         : :%H$
        copyright       : (C) 2022 by Leo Cardona (SwissTierras Colombia)
                          (C) 2021 by Germán Carrillo (SwissTierras Colombia)
        email           : contacto@ceicol.com
                          gcarrillo@linuxmail.org
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

from qgis.core import QgsFeatureRequest

from asistente_ladm_col.config.enums import EnumQualityRuleResult
from asistente_ladm_col.config.keys.common import (QUALITY_RULE_LADM_COL_LAYERS,
                                                   QUALITY_RULE_ADJUSTED_LAYERS,
                                                   ADJUSTED_INPUT_LAYER,
                                                   ADJUSTED_REFERENCE_LAYER)
from asistente_ladm_col.config.layer_config import LADMNames
from asistente_ladm_col.config.quality_rule_config import (QR_IGACR1003,
                                                           QRE_IGACR1003E01,
                                                           QRE_IGACR1003E02,
                                                           QRE_IGACR1003E03)
from asistente_ladm_col.core.quality_rules.abstract_point_quality_rule import AbstractPointQualityRule
from asistente_ladm_col.core.quality_rules.quality_rule_execution_result import QualityRuleExecutionResult
from asistente_ladm_col.lib.geometry import GeometryUtils
from asistente_ladm_col.logic.ladm_col.ladm_data import LADMData


class QRBoundaryPointsNotCoveredByBoundaryNodes(AbstractPointQualityRule):
    """
    Check that boundary points not covered by boundary nodes
    """
    _ERROR_01 = QRE_IGACR1003E01
    _ERROR_02 = QRE_IGACR1003E02
    _ERROR_03 = QRE_IGACR1003E03

    def __init__(self):
        AbstractPointQualityRule.__init__(self)

        self._id = QR_IGACR1003
        self._name = "Los Puntos de Lindero deben estar cubiertos por nodos de Lindero"
        self._tags = ["igac", "instituto geográfico agustín codazzi", "puntos", "punto lindero", 'lindero', "superposición"]
        self._models = [LADMNames.SURVEY_MODEL_KEY]

        self._errors = {self._ERROR_01: "Punto lindero no esta cubierto por un nodo de lindero",
                        self._ERROR_02: "La relación topológica entre el punto lindero y el nodo de un lindero no está registrada en la tabla puntoccl",
                        self._ERROR_03: "La relación topológica entre el punto lindero y el nodo de un lindero está duplicada en la tabla puntoccl"}

        # Optional. Only useful for display purposes.
        self._field_mapping = dict()  # E.g., {'id_objetos': 'ids_punto_lindero', 'valores': 'conteo'}

    def field_mapping(self, names):
        return {names.ERR_QUALITY_ERROR_T_OBJECT_IDS_F: QCoreApplication.translate("QualityRules", "Boundary Points")}

    def layers_config(self, names):
        return {
            QUALITY_RULE_LADM_COL_LAYERS: [names.LC_BOUNDARY_T,
                                           names.POINT_BFS_T,
                                           names.LC_BOUNDARY_POINT_T],
            QUALITY_RULE_ADJUSTED_LAYERS: {
                names.LC_BOUNDARY_T: {
                    ADJUSTED_INPUT_LAYER: names.LC_BOUNDARY_T,
                    ADJUSTED_REFERENCE_LAYER: names.LC_BOUNDARY_POINT_T}
            }
        }

    def _validate(self, db, db_qr, layer_dict, tolerance, **kwargs):
        self.progress_changed.emit(5)
        pre_res, pre_obj = self._check_prerrequisite_layers(layer_dict)
        if not pre_res:
            return pre_obj

        boundary_point_layer = self._get_layer(layer_dict, db.names.LC_BOUNDARY_POINT_T)
        boundary_layer = self._get_layer(layer_dict, db.names.LC_BOUNDARY_T)
        point_bfs_layer = self._get_layer(layer_dict, db.names.POINT_BFS_T)
        id_field = db.names.T_ID_F

        dict_uuid_boundary = {f[id_field]: f[db.names.T_ILI_TID_F] for f in boundary_layer.getFeatures()}
        dict_uuid_boundary_point = {f[id_field]: f[db.names.T_ILI_TID_F] for f in boundary_point_layer.getFeatures()}

        # create dict with layer data
        id_field_idx = boundary_point_layer.fields().indexFromName(id_field)
        request = QgsFeatureRequest().setSubsetOfAttributes([id_field_idx])
        dict_boundary_point = {feature[id_field]: feature for feature in boundary_point_layer.getFeatures(request)}

        result = GeometryUtils.get_boundary_points_not_covered_by_boundary_nodes(
            db, boundary_point_layer, boundary_layer, point_bfs_layer, id_field
        )

        boundary_point_without_boundary_node = result[0]
        no_register_point_bfs = result[1]
        duplicate_in_point_bfs = result[2]

        self.progress_changed.emit(70)

        error_state = LADMData().get_domain_code_from_value(db_qr, db_qr.names.ERR_ERROR_STATE_D,
                                                            LADMNames.ERR_ERROR_STATE_D_ERROR_V)

        errors_e01 = {'geometries': list(), 'data': list()}
        errors_e02 = {'geometries': list(), 'data': list()}
        errors_e03 = {'geometries': list(), 'data': list()}

        # boundary point without boundary node
        if boundary_point_without_boundary_node:
            for item in boundary_point_without_boundary_node:
                boundary_point_id = item  # boundary_point_id
                errors_e01['geometries'].append(dict_boundary_point[boundary_point_id].geometry())
                error_data = [  # [obj_uuids, rel_obj_uuids, values, details, state]
                    [dict_uuid_boundary_point.get(boundary_point_id)],
                    None,
                    None,
                    self._errors[self._ERROR_01],
                    error_state]
                errors_e01['data'].append(error_data)
            self._save_errors(db_qr, self._ERROR_01, errors_e01)

        # No registered in point_bfs
        if no_register_point_bfs:
            for error_no_register in set(no_register_point_bfs):
                boundary_point_id = error_no_register[0]  # boundary_point_id
                boundary_id = error_no_register[1]  # boundary_id

                errors_e02['geometries'].append(dict_boundary_point[boundary_point_id].geometry())
                error_data = [  # [obj_uuids, rel_obj_uuids, values, details, state]
                    [dict_uuid_boundary_point.get(boundary_point_id)],
                    [dict_uuid_boundary.get(boundary_id)],
                    None,
                    self._errors[self._ERROR_02],
                    error_state]
                errors_e02['data'].append(error_data)
            self._save_errors(db_qr, self._ERROR_02, errors_e02)

        # Duplicate in point_bfs
        if duplicate_in_point_bfs:
            for error_duplicate in set(duplicate_in_point_bfs):
                boundary_point_id = error_duplicate[0]  # boundary_point_id
                boundary_id = error_duplicate[1]  # boundary_id

                errors_e03['geometries'].append(dict_boundary_point[boundary_point_id].geometry())
                error_data = [  # [obj_uuids, rel_obj_uuids, values, details, state]
                    [dict_uuid_boundary_point.get(boundary_point_id)],
                    [dict_uuid_boundary.get(boundary_id)],
                    None,
                    self._errors[self._ERROR_03],
                    error_state]
                errors_e03['data'].append(error_data)
            self._save_errors(db_qr, self._ERROR_03, errors_e03)

        self.progress_changed.emit(100)

        count = len(errors_e01['data']) + len(errors_e02['data']) + len(errors_e03['data'])

        if count > 0:
            res_type = EnumQualityRuleResult.ERRORS
            msg = QCoreApplication.translate("QualityRules", "{} boundary points not covered by boundary nodes were found.").format(
                count)
        else:
            res_type = EnumQualityRuleResult.SUCCESS
            msg = QCoreApplication.translate("QualityRules", "All boundary points are covered by boundary nodes!")

        self.progress_changed.emit(100)

        return QualityRuleExecutionResult(res_type, msg, count)
