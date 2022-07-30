"""
/***************************************************************************
                              Asistente LADM-COL
                             --------------------
        begin           : 2022-07-05
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
from asistente_ladm_col.config.keys.common import (QUALITY_RULE_LADM_COL_LAYERS,
                                                   QUALITY_RULE_ADJUSTED_LAYERS,
                                                   ADJUSTED_INPUT_LAYER,
                                                   ADJUSTED_REFERENCE_LAYER)
from asistente_ladm_col.config.layer_config import LADMNames
from asistente_ladm_col.config.quality_rule_config import (QR_IGACR3002,
                                                           QRE_IGACR3002E01)
from asistente_ladm_col.core.quality_rules.abstract_polygon_quality_rule import AbstractPolygonQualityRule
from asistente_ladm_col.core.quality_rules.quality_rule_execution_result import QualityRuleExecutionResult
from asistente_ladm_col.lib.geometry import GeometryUtils
from asistente_ladm_col.logic.ladm_col.ladm_data import LADMData


class QROverlappingBuildings(AbstractPolygonQualityRule):
    """
    Check that buildings do not overlap
    """
    _ERROR_01 = QRE_IGACR3002E01

    def __init__(self):
        AbstractPolygonQualityRule.__init__(self)

        self._id = QR_IGACR3002
        self._name = "Las construcciones no deben superponerse"
        self._tags = ["igac", "instituto geográfico agustín codazzi", "construcción", "superposición"]
        self._models = [LADMNames.SURVEY_MODEL_KEY]

        self._errors = {self._ERROR_01: "Las construcciones no deben superponerse"}

        # Optional. Only useful for display purposes.
        self._field_mapping = dict()  # E.g., {'id_objetos': 'ids_punto_lindero', 'valores': 'conteo'}

    def field_mapping(self, names):
        return {names.ERR_QUALITY_ERROR_T_OBJECT_IDS_F: QCoreApplication.translate("QualityRules", "Buildings")}

    def layers_config(self, names):
        return {
            QUALITY_RULE_LADM_COL_LAYERS: [names.LC_BUILDING_T],
            QUALITY_RULE_ADJUSTED_LAYERS: {
                names.LC_BUILDING_T: {
                    ADJUSTED_INPUT_LAYER: names.LC_BUILDING_T,
                    ADJUSTED_REFERENCE_LAYER: names.LC_BUILDING_T
                }
            }
        }

    def _validate(self, db, db_qr, layer_dict, tolerance, **kwargs):
        self.progress_changed.emit(5)

        building_layer = self._get_layer(layer_dict)
        pre_res, res_obj = self._check_prerrequisite_layer(QCoreApplication.translate("QualityRules", "Building"),
                                                           building_layer)
        if not pre_res:
            return res_obj

        overlapping = GeometryUtils.get_overlapping_polygons(self, building_layer)
        flat_overlapping = [fid for items in overlapping for fid in items]  # Build a flat list of ids
        flat_overlapping = list(set(flat_overlapping))  # unique values

        self.progress_changed.emit(70)

        dict_uuids = {f.id(): f[db.names.T_ILI_TID_F] for f in building_layer.getFeatures(flat_overlapping)}
        error_state = LADMData().get_domain_code_from_value(db_qr, db_qr.names.ERR_ERROR_STATE_D,
                                                            LADMNames.ERR_ERROR_STATE_D_ERROR_V)

        errors = {'geometries': list(), 'data': list()}
        for items in overlapping:
            polygon_id_field = items[0]
            overlapping_id_field = items[1]
            polygon_intersection = GeometryUtils.get_intersection_polygons(building_layer, polygon_id_field, overlapping_id_field)

            if polygon_intersection is not None:
                errors['geometries'].append(polygon_intersection)

                error_data = [  # [obj_uuids, rel_obj_uuids, values, details, state]
                    [dict_uuids.get(polygon_id_field)],
                    [dict_uuids.get(overlapping_id_field)],
                    None,
                    self._errors[self._ERROR_01],
                    error_state]
                errors['data'].append(error_data)

        self._save_errors(db_qr, self._ERROR_01, errors)

        if len(flat_overlapping) > 0:
            res_type = EnumQualityRuleResult.ERRORS
            msg = QCoreApplication.translate("QualityRules", "{} overlapping buildings were found!").format(len(flat_overlapping))
        else:
            res_type = EnumQualityRuleResult.SUCCESS
            msg = QCoreApplication.translate("QualityRules", "There are no overlapping buildings!")

        self.progress_changed.emit(100)

        return QualityRuleExecutionResult(res_type, msg, len(flat_overlapping))
