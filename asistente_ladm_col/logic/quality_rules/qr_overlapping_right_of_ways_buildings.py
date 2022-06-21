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
from asistente_ladm_col.config.quality_rule_config import (QR_IGACR3005,
                                                           QRE_IGACR3005E01)
from asistente_ladm_col.core.quality_rules.abstract_polygon_quality_rule import AbstractPolygonQualityRule
from asistente_ladm_col.core.quality_rules.quality_rule_execution_result import QualityRuleExecutionResult
from asistente_ladm_col.lib.geometry import GeometryUtils
from asistente_ladm_col.logic.ladm_col.ladm_data import LADMData
from asistente_ladm_col.utils.utils import get_uuid_dict


class QROverlappingRightOfWaysBuildings(AbstractPolygonQualityRule):
    """
    Check that right of ways do not overlap with buildings
    """
    _ERROR_01 = QRE_IGACR3005E01

    def __init__(self):
        AbstractPolygonQualityRule.__init__(self)

        self._id = QR_IGACR3005
        self._name = "Los servidumbres de tránsito no deben superponerse con construcciones"
        self._tags = ["igac", "instituto geográfico agustín codazzi", "polígonos", "servidumbre de tránsito con construcciones", "superposición"]
        self._models = [LADMNames.SURVEY_MODEL_KEY]

        self._errors = {self._ERROR_01: "Los servidumbres de tránsito no deben superponerse con construcciones"}

        # Optional. Only useful for display purposes.
        self._field_mapping = dict()  # E.g., {'id_objetos': 'ids_punto_lindero', 'valores': 'conteo'}

    def field_mapping(self, names):
        return {names.ERR_QUALITY_ERROR_T_OBJECT_IDS_F: QCoreApplication.translate("QualityRules", "Right of ways")}

    def layers_config(self, names):
        return {
            QUALITY_RULE_LADM_COL_LAYERS: [names.LC_RIGHT_OF_WAY_T,
                                           names.LC_BUILDING_T],
            QUALITY_RULE_ADJUSTED_LAYERS: {
                names.LC_RIGHT_OF_WAY_T: {
                    ADJUSTED_INPUT_LAYER: names.LC_RIGHT_OF_WAY_T,
                    ADJUSTED_REFERENCE_LAYER: names.LC_RIGHT_OF_WAY_T},
                names.LC_BUILDING_T: {
                    ADJUSTED_INPUT_LAYER: names.LC_BUILDING_T,
                    ADJUSTED_REFERENCE_LAYER: names.LC_BUILDING_T}
            }
        }

    def _validate(self, db, db_qr, layer_dict, tolerance, **kwargs):
        self.progress_changed.emit(5)

        right_of_way_layer = self._get_layer(layer_dict, db.names.LC_RIGHT_OF_WAY_T)
        building_layer = self._get_layer(layer_dict, db.names.LC_BUILDING_T)
        pre_res, res_obj = self._check_prerrequisite_layers(layer_dict)
        if not pre_res:
            return res_obj

        dict_uuid_right_of_way = get_uuid_dict(right_of_way_layer, db.names)
        dict_uuid_building = get_uuid_dict(building_layer, db.names)

        ids, overlapping = GeometryUtils.get_inner_intersections_between_polygons(right_of_way_layer, building_layer)

        self.progress_changed.emit(70)

        error_state = LADMData().get_domain_code_from_value(db_qr, db_qr.names.ERR_ERROR_STATE_D,
                                                            LADMNames.ERR_ERROR_STATE_D_ERROR_V)

        errors = {'geometries': list(), 'data': list()}

        if overlapping:
            for key, polygon in zip(ids, overlapping.asGeometryCollection()):

                errors['geometries'].append(polygon)

                error_data = [  # [obj_uuids, rel_obj_uuids, values, details, state]
                    [dict_uuid_right_of_way.get(key[0])],
                    [dict_uuid_building.get(key[1])],
                    None,
                    self._errors[self._ERROR_01],
                    error_state]
                errors['data'].append(error_data)

            self._save_errors(db_qr, self._ERROR_01, errors)

        self.progress_changed.emit(100)

        count = len(errors['geometries'])

        if count > 0:
            return QualityRuleExecutionResult(EnumQualityRuleResult.ERRORS,
                                              QCoreApplication.translate("QualityRules",
                                                                         "{} overlapping right of ways with buildings were found!").format(
                                                  count),
                                              len(errors['data']))
        else:
            return QualityRuleExecutionResult(EnumQualityRuleResult.SUCCESS,
                                              QCoreApplication.translate("QualityRules",
                                                                         "There are no overlapping right of ways with buildings."))