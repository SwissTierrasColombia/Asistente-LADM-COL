"""
/***************************************************************************
                              Asistente LADM-COL
                             --------------------
        begin           : 2021-11-25
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

from qgis.core import QgsVectorLayer

from asistente_ladm_col.config.enums import (EnumQualityRuleType,
                                             EnumQualityRuleResult)
from asistente_ladm_col.config.keys.common import (QUALITY_RULE_LADM_COL_LAYERS,
                                                   QUALITY_RULE_ADJUSTED_LAYERS,
                                                   ADJUSTED_INPUT_LAYER,
                                                   ADJUSTED_REFERENCE_LAYER,
                                                   FIX_ADJUSTED_LAYER)
from asistente_ladm_col.config.layer_config import LADMNames
from asistente_ladm_col.config.quality_rule_config import (QR_IGACR2001,
                                                           QRE_IGACR2001E01)
from asistente_ladm_col.core.quality_rules.abstract_line_quality_rule import AbstractLineQualityRule
from asistente_ladm_col.core.quality_rules.quality_rule_execution_result import QualityRuleExecutionResult
from asistente_ladm_col.lib.geometry import GeometryUtils


class QROverlappingBoundaries(AbstractLineQualityRule):
    """
    Check that boundaries do not overlap
    """
    _ERROR_01 = QRE_IGACR2001E01

    def __init__(self):
        AbstractLineQualityRule.__init__(self)

        self._id = QR_IGACR2001
        self._name = "Los linderos no deben superponerse"
        self._tags = ["igac", "instituto geográfico agustín codazzi", "líneas", "linderos", "superposición"]
        self._models = [LADMNames.SURVEY_MODEL_KEY]

        self._errors = {self._ERROR_01: "Los linderos no deben superponerse"}

        # Optional. Only useful for display purposes.
        self._field_mapping = dict()  # E.g., {'id_objetos': 'ids_punto_lindero', 'valores': 'conteo'}

    def layers_config(self, names):
        return {QUALITY_RULE_LADM_COL_LAYERS: [names.LC_BOUNDARY_T],
                QUALITY_RULE_ADJUSTED_LAYERS: {
                    names.LC_BOUNDARY_T: {
                        ADJUSTED_INPUT_LAYER: names.LC_BOUNDARY_T,
                        ADJUSTED_REFERENCE_LAYER: names.LC_BOUNDARY_T,
                        FIX_ADJUSTED_LAYER: True
                    }}}

    def _validate(self, db, db_qr, layer_dict, tolerance, **kwargs):
        self.progress_changed.emit(5)

        # TODO: Check that overlapping points are what we expect. We won't consider end-points as overlapping points
        #       nor common intermediate segmenr's vertices (between line A and B).
        boundary_layer = self._get_layer(layer_dict)

        pre_res, res_obj = self._check_prerrequisite_layer(QCoreApplication.translate("QualityRules", "Boundary"), boundary_layer)
        if not pre_res:
            return res_obj

        res, overlapping, msg = GeometryUtils.get_overlapping_lines(boundary_layer)
        if not res:
            return QualityRuleExecutionResult(EnumQualityRuleResult.CRITICAL,
                                              QCoreApplication.translate("QualityRules",
                                                                         "There was an error checking for boundary overlaps! Details: {}").format(
                                                  msg))
        self.progress_changed.emit(85)

        points_intersected = overlapping['native:deleteduplicategeometries_1:Intersected_Points']
        lines_intersected = overlapping['native:extractbyexpression_3:Intersected_Lines']
        point_errors, line_errors = dict(), dict()

        #from qgis.core import QgsProject
        #QgsProject.instance().addMapLayers([points_intersected, lines_intersected])
        if isinstance(points_intersected, QgsVectorLayer):
            if points_intersected.featureCount() > 0:
                point_errors = self._get_error_dict(db, points_intersected)
                self._save_errors(db_qr, self._ERROR_01, point_errors, EnumQualityRuleType.POINT)

        if isinstance(lines_intersected, QgsVectorLayer):
            if lines_intersected.featureCount() > 0:
                line_errors = self._get_error_dict(db, lines_intersected)
                self._save_errors(db_qr, self._ERROR_01, line_errors)

        len_point_errors = len(point_errors.get('data', dict()))
        len_line_errors = len(line_errors.get('data', dict()))

        self.progress_changed.emit(100)

        if len(point_errors) == 0 and len(line_errors) == 0:
            return QualityRuleExecutionResult(EnumQualityRuleResult.SUCCESS,
                                              QCoreApplication.translate("QualityRules",
                                                                         "There are no overlapping boundaries."))
        else:
            msg = ""
            if len_point_errors and len_line_errors:
                msg = QCoreApplication.translate("QualityRules",
                                                 "{} overlaps were found in boundaries. {} overlaps of type point and {} overlaps of type line.").format(
                    len_point_errors + len_line_errors, len_point_errors, len_line_errors)
            elif len_point_errors:
                msg = QCoreApplication.translate("QualityRules",
                                                 "{} overlaps of type point were found in boundaries.").format(
                    len_point_errors)
            elif len_line_errors:
                msg = QCoreApplication.translate("QualityRules",
                                                 "{} overlaps of type line were found in boundaries.").format(
                    len_line_errors)

            return QualityRuleExecutionResult(EnumQualityRuleResult.ERRORS, msg, len_point_errors + len_line_errors)

    def _get_error_dict(self, db, layer):
        errors = {'geometries': list(), 'data': list()}
        for feature in layer.getFeatures():
            errors['geometries'].append(feature.geometry())

            error_data = [  # [obj_uuids, rel_obj_uuids, values, details]
                [feature[db.names.T_ILI_TID_F]],
                [feature["{}_2".format(db.names.T_ILI_TID_F)]],
                None,
                None]
            errors['data'].append(error_data)

        return errors
