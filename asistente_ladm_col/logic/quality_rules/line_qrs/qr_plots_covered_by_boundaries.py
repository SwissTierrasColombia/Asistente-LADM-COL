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
import processing

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsWkbTypes,
                       QgsFeatureRequest)

from asistente_ladm_col.config.enums import EnumQualityRuleResult
from asistente_ladm_col.config.keys.common import (QUALITY_RULE_LADM_COL_LAYERS,
                                                   QUALITY_RULE_ADJUSTED_LAYERS,
                                                   ADJUSTED_INPUT_LAYER,
                                                   ADJUSTED_REFERENCE_LAYER,
                                                   FIX_ADJUSTED_LAYER)
from asistente_ladm_col.config.layer_config import LADMNames
from asistente_ladm_col.config.quality_rule_config import (QR_IGACR3004,
                                                           QRE_IGACR3004E01,
                                                           QRE_IGACR3004E02,
                                                           QRE_IGACR3004E03,
                                                           QRE_IGACR3004E04,
                                                           QRE_IGACR3004E05)
from asistente_ladm_col.core.quality_rules.abstract_line_quality_rule import AbstractLineQualityRule
from asistente_ladm_col.core.quality_rules.quality_rule_execution_result import QualityRuleExecutionResult
from asistente_ladm_col.lib.geometry import GeometryUtils
from asistente_ladm_col.logic.ladm_col.ladm_data import LADMData
from asistente_ladm_col.utils.utils import (get_key_for_quality_rule_adjusted_layer,
                                            get_uuid_dict)


class QRPlotsCoveredByBoundaries(AbstractLineQualityRule):
    """
    Check that plots are covered by boundaries
    """
    _ERROR_01 = QRE_IGACR3004E01
    _ERROR_02 = QRE_IGACR3004E02
    _ERROR_03 = QRE_IGACR3004E03
    _ERROR_04 = QRE_IGACR3004E04
    _ERROR_05 = QRE_IGACR3004E05

    def __init__(self):
        AbstractLineQualityRule.__init__(self)

        self._id = QR_IGACR3004
        self._name = "Los límites de Terreno deben estar cubiertos por Linderos"
        self._tags = ["igac", "instituto geográfico agustín codazzi", "terrenos", "superposición", 'cubiertos', 'linderos']
        self._models = [LADMNames.SURVEY_MODEL_KEY]

        self._errors = {self._ERROR_01: "El terreno no está cubierto por linderos",
                        self._ERROR_02: "La relación topológica entre terreno y lindero está duplicada en la tabla masccl",
                        self._ERROR_03: "La relación topológica entre terreno y lindero está duplicada en la tabla menosccl",
                        self._ERROR_04: "La relación topológica entre terreno y lindero no está registrada en la tabla masccl",
                        self._ERROR_05: "La relación topológica entre terreno y lindero no está registrada en la tabla menosccl"}

        # Optional. Only useful for display purposes.
        self._field_mapping = dict()  # E.g., {'id_objetos': 'ids_punto_lindero', 'valores': 'conteo'}

    def field_mapping(self, names):
        return {names.ERR_QUALITY_ERROR_T_OBJECT_IDS_F: QCoreApplication.translate("QualityRules", "Buildings")}

    def layers_config(self, names):
        return {
            QUALITY_RULE_LADM_COL_LAYERS: [names.LC_PLOT_T,
                                           names.LC_BOUNDARY_T,
                                           names.LESS_BFS_T,
                                           names.MORE_BFS_T],
            QUALITY_RULE_ADJUSTED_LAYERS: {
                names.LC_PLOT_T: {
                    ADJUSTED_INPUT_LAYER: names.LC_PLOT_T,
                    ADJUSTED_REFERENCE_LAYER: names.LC_PLOT_T,
                    FIX_ADJUSTED_LAYER: True
                }, names.LC_BOUNDARY_T: {  # This one uses an adjusted layer as reference layer!
                    ADJUSTED_INPUT_LAYER: names.LC_BOUNDARY_T,
                    ADJUSTED_REFERENCE_LAYER: get_key_for_quality_rule_adjusted_layer(names.LC_PLOT_T, names.LC_PLOT_T, True),
                    FIX_ADJUSTED_LAYER: True
                }
            }
        }

    def _validate(self, db, db_qr, layer_dict, tolerance, **kwargs):
        self.progress_changed.emit(5)

        plot_layer = self._get_layer(layer_dict, db.names.LC_PLOT_T)
        boundary_layer = self._get_layer(layer_dict, db.names.LC_BOUNDARY_T)
        more_bfs_layer = self._get_layer(layer_dict, db.names.MORE_BFS_T)
        less_bfs_layer = self._get_layer(layer_dict, db.names.LESS_BFS_T)

        pre_res, res_obj = self._check_prerrequisite_layer(QCoreApplication.translate("QualityRules", "Plot"), plot_layer)
        if not pre_res:
            return res_obj

        self.progress_changed.emit(10)

        result = QRPlotsCoveredByBoundaries.get_plot_features_not_covered_by_boundaries(
            db, plot_layer, boundary_layer, more_bfs_layer, less_bfs_layer, db.names.T_ID_F
        )

        errors_plot_boundary_diffs = result[0]
        errors_duplicate_in_more_bfs = result[1]
        errors_duplicate_in_less = result[2]
        errors_not_in_more_bfs = result[3]
        errors_not_in_less = result[4]

        self.progress_changed.emit(80)
        error_state = LADMData().get_domain_code_from_value(db_qr, db_qr.names.ERR_ERROR_STATE_D,
                                                            LADMNames.ERR_ERROR_STATE_D_ERROR_V)

        errors_e01 = {'geometries': list(), 'data': list()}
        errors_e02 = {'geometries': list(), 'data': list()}
        errors_e03 = {'geometries': list(), 'data': list()}
        errors_e04 = {'geometries': list(), 'data': list()}
        errors_e05 = {'geometries': list(), 'data': list()}

        # plot not covered by boundary
        if errors_plot_boundary_diffs:
            for error_plot_boundary_diffs in errors_plot_boundary_diffs:
                plot_uuid, boundary_uuid, error_geom = error_plot_boundary_diffs[:3]

                error_data = [  # [obj_uuids, rel_obj_uuids, values, details, state]
                    [plot_uuid],
                    None,  # Plot not covered by boundary
                    None,
                    self._errors[self._ERROR_01],
                    error_state]

                errors_e01['geometries'].append(error_geom)
                errors_e01['data'].append(error_data)
            self._save_errors(db_qr, self._ERROR_01, errors_e01)


        # Duplicate in more bfs
        if errors_duplicate_in_more_bfs:
            for error_duplicate_in_more_bfs in errors_duplicate_in_more_bfs:
                plot_uuid, boundary_uuid, error_geom = error_duplicate_in_more_bfs[:3]

                error_data = [  # [obj_uuids, rel_obj_uuids, values, details, state]
                    [plot_uuid],
                    [boundary_uuid],
                    None,
                    self._errors[self._ERROR_02],
                    error_state]

                errors_e02['geometries'].append(error_geom)
                errors_e02['data'].append(error_data)
            self._save_errors(db_qr, self._ERROR_02, errors_e02)

        # Duplicate in less
        if errors_duplicate_in_less:
            for error_duplicate_in_less in errors_duplicate_in_less:
                plot_uuid, boundary_uuid, error_geom = error_duplicate_in_less[:3]

                error_data = [  # [obj_uuids, rel_obj_uuids, values, details, state]
                    [plot_uuid],
                    [boundary_uuid],
                    None,
                    self._errors[self._ERROR_03],
                    error_state]

                errors_e03['geometries'].append(error_geom)
                errors_e03['data'].append(error_data)
            self._save_errors(db_qr, self._ERROR_03, errors_e03)

        # not registered more bfs
        if errors_not_in_more_bfs:
            for error_not_in_more_bfs in errors_not_in_more_bfs:
                plot_uuid, boundary_uuid, error_geom = error_not_in_more_bfs[:3]

                error_data = [  # [obj_uuids, rel_obj_uuids, values, details, state]
                    [plot_uuid],
                    [boundary_uuid],
                    None,
                    self._errors[self._ERROR_04],
                    error_state]

                errors_e04['geometries'].append(error_geom)
                errors_e04['data'].append(error_data)
            self._save_errors(db_qr, self._ERROR_04, errors_e04)

        # not registered less
        if errors_not_in_less:
            for error_not_in_less in errors_not_in_less:
                plot_uuid, boundary_uuid, error_geom = error_not_in_less[:3]

                error_data = [  # [obj_uuids, rel_obj_uuids, values, details, state]
                    [plot_uuid],
                    [boundary_uuid],
                    None,
                    self._errors[self._ERROR_05],
                    error_state]

                errors_e05['geometries'].append(error_geom)
                errors_e05['data'].append(error_data)
            self._save_errors(db_qr, self._ERROR_05, errors_e05)

        count = len(errors_e01['data']) + len(errors_e02['data']) + len(errors_e03['data']) + len(errors_e04['data']) + len(errors_e05['data'])

        if count > 0:
            res_type = EnumQualityRuleResult.ERRORS
            msg = QCoreApplication.translate("QualityRules", "{} plots not covered by boundaries were found.").format(count)
        else:
            res_type = EnumQualityRuleResult.SUCCESS
            msg = QCoreApplication.translate("QualityRules", "All plots are covered by boundaries!")

        self.progress_changed.emit(100)

        return QualityRuleExecutionResult(res_type, msg, count)

    @staticmethod
    def get_plot_features_not_covered_by_boundaries(db, plot_layer, boundary_layer, more_bfs_layer, less_layer, id_field):
        """
        Returns all plot features that have errors when checking if they are covered by boundaries.
        That is both geometric and alphanumeric (topology table) errors.
        """
        dict_uuid_plots = get_uuid_dict(plot_layer, db.names, id_field)
        dict_uuid_boundary = get_uuid_dict(boundary_layer, db.names, id_field)
        plot_as_lines_layer = processing.run("ladm_col:polygonstolines", {'INPUT': plot_layer, 'OUTPUT': 'memory:'})['OUTPUT']
        GeometryUtils.create_spatial_index(plot_as_lines_layer)

        # create dict with layer data
        id_field_idx = plot_as_lines_layer.fields().indexFromName(id_field)
        request = QgsFeatureRequest().setSubsetOfAttributes([id_field_idx])
        dict_plot_as_lines = {feature[id_field]: feature for feature in plot_as_lines_layer.getFeatures(request)}

        id_field_idx = boundary_layer.fields().indexFromName(id_field)
        request = QgsFeatureRequest().setSubsetOfAttributes([id_field_idx])
        dict_boundary = {feature[id_field]: feature for feature in boundary_layer.getFeatures(request)}

        exp_more = '"{}" is not null and "{}" is not null'.format(db.names.MORE_BFS_T_LC_BOUNDARY_F, db.names.MORE_BFS_T_LC_PLOT_F)
        list_more_bfs = [{'plot_id': feature[db.names.MORE_BFS_T_LC_PLOT_F], 'boundary_id': feature[db.names.MORE_BFS_T_LC_BOUNDARY_F]}
                         for feature in more_bfs_layer.getFeatures(exp_more)]

        exp_less = '"{}" is not null and "{}" is not null'.format(db.names.LESS_BFS_T_LC_BOUNDARY_F, db.names.LESS_BFS_T_LC_PLOT_F)
        list_less = [{'plot_id': feature[db.names.LESS_BFS_T_LC_PLOT_F], 'boundary_id': feature[db.names.LESS_BFS_T_LC_BOUNDARY_F]}
                     for feature in less_layer.getFeatures(exp_less)]

        tmp_inner_rings_layer = GeometryUtils.get_inner_rings_layer(db.names, plot_layer, db.names.T_ID_F)
        inner_rings_layer = processing.run("native:addautoincrementalfield",
                                           {'INPUT': tmp_inner_rings_layer,
                                            'FIELD_NAME': 'AUTO',
                                            'START': 0,
                                            'GROUP_FIELDS': [],
                                            'SORT_EXPRESSION': '',
                                            'SORT_ASCENDING': True,
                                            'SORT_NULLS_FIRST': False,
                                            'OUTPUT': 'memory:'})['OUTPUT']
        GeometryUtils.create_spatial_index(inner_rings_layer)

        id_field_idx = inner_rings_layer.fields().indexFromName(id_field)
        auto_idx = inner_rings_layer.fields().indexFromName('AUTO')
        request = QgsFeatureRequest().setSubsetOfAttributes([id_field_idx, auto_idx])
        dict_inner_rings = {'{}-{}'.format(feature[id_field], feature['AUTO']): feature for feature in inner_rings_layer.getFeatures(request)}

        # spatial joins between inner rings and boundary
        spatial_join_inner_rings_boundary_layer = processing.run("qgis:joinattributesbylocation",
                                                                 {'INPUT': inner_rings_layer,
                                                                  'JOIN': boundary_layer,
                                                                  'PREDICATE': [0],  # Intersects
                                                                  'JOIN_FIELDS': [id_field],
                                                                  'METHOD': 0,
                                                                  'DISCARD_NONMATCHING': True,
                                                                  'PREFIX': '',
                                                                  'OUTPUT': 'memory:'})['OUTPUT']
        # The id field has the same name for both layers
        # This list is only used to check plot's inner rings without boundaries
        dict_spatial_join_inner_rings_boundary = [{'plot_ring_id': '{}-{}'.format(feature[id_field], feature['AUTO']), 'boundary_id': feature[id_field + '_2']}
                                                  for feature in spatial_join_inner_rings_boundary_layer.getFeatures()]

        # list create for filter inner rings from spatial join with between plot and boundary
        list_spatial_join_plot_ring_boundary = [{'plot_id': feature[id_field],
                                                 'boundary_id': feature[id_field + '_2']}
                                                for feature in spatial_join_inner_rings_boundary_layer.getFeatures()]

        # Spatial join between plot as lines and boundary
        spatial_join_plot_boundary_layer = processing.run("qgis:joinattributesbylocation",
                                                          {'INPUT': plot_as_lines_layer,
                                                           'JOIN': boundary_layer,
                                                           'PREDICATE': [0],
                                                           'JOIN_FIELDS': [id_field],
                                                           'METHOD': 0,
                                                           'DISCARD_NONMATCHING': True,
                                                           'PREFIX': '',
                                                           'OUTPUT': 'memory:'})['OUTPUT']
        # The id field has the same name for both layers
        dict_spatial_join_plot_boundary = [{'plot_id': feature[id_field], 'boundary_id': feature[id_field + '_2']}
                                           for feature in spatial_join_plot_boundary_layer.getFeatures()]

        #####################################################
        # Validation of geometric errors
        #####################################################

        # Identify plots with geometry problems and remove coincidence in spatial join between plot as line and boundary
        # and inner_rings and boundary. No need to check further topological rules for plots

        errors_plot_boundary_diffs = GeometryUtils.difference_plot_boundary(plot_as_lines_layer, boundary_layer, db.names.T_ID_F)
        for error_diff in errors_plot_boundary_diffs:
            plot_id = error_diff['id']
            # All plots with geometric errors are eliminated. It is not necessary check more
            # in spatial join between plot as line and boundary
            for item_sj in dict_spatial_join_plot_boundary.copy():
                if item_sj['plot_id'] == plot_id:
                    dict_spatial_join_plot_boundary.remove(item_sj)

            # All plots with geometric errors are eliminated. It is not necessary check more
            # in spatial join between inner_rings and boundary
            for item_sj in dict_spatial_join_inner_rings_boundary.copy():
                if int(item_sj['plot_ring_id'].split('-')[0]) == plot_id:
                    dict_spatial_join_inner_rings_boundary.remove(item_sj)

        ######################################################
        # Validation of errors in alphanumeric topology tables
        ######################################################

        # start validation for more_bfs table
        # remove spatial join intersection with geometries that no contain lines. Because it is not necessary to check
        for item_sj in dict_spatial_join_plot_boundary.copy():
            boundary_id = item_sj['boundary_id']
            plot_id = item_sj['plot_id']

            if item_sj in list_spatial_join_plot_ring_boundary:
                # it is removed because it is registered in the spatial join between rings and boundaries
                # and it shouldn't be registered in the topology table of more_bfs
                dict_spatial_join_plot_boundary.remove(item_sj)
            else:
                plot_geom = dict_plot_as_lines[plot_id].geometry()
                boundary_geom = dict_boundary[boundary_id].geometry()
                intersection = plot_geom.intersection(boundary_geom)

                if not intersection.isEmpty():
                    if intersection.type() != QgsWkbTypes.LineGeometry:
                        if intersection.type() == QgsWkbTypes.UnknownGeometry:
                            has_line = False
                            for part in intersection.asGeometryCollection():
                                if part.isMultipart():
                                    for i in range(part.numGeometries()):
                                        if QgsWkbTypes.geometryType(
                                                part.geometryN(i).wkbType()) == QgsWkbTypes.LineGeometry:
                                            has_line = True
                                            break
                                else:
                                    if part.type() == QgsWkbTypes.LineGeometry:
                                        has_line = True
                                        break
                            if not has_line:
                                # Remove point intersections plot-boundary
                                dict_spatial_join_plot_boundary.remove(item_sj)
                        else:
                            dict_spatial_join_plot_boundary.remove(item_sj)

        # Check relation between plot and boundary not registered in more_bfs
        errors_not_in_more_bfs = list()
        errors_duplicate_in_more_bfs = list()
        for item_sj_pb in dict_spatial_join_plot_boundary:
            count_more_bfs = list_more_bfs.count(item_sj_pb)
            if count_more_bfs > 1:
                errors_duplicate_in_more_bfs.append((item_sj_pb['plot_id'], item_sj_pb['boundary_id']))
            elif count_more_bfs == 0:
                errors_not_in_more_bfs.append((item_sj_pb['plot_id'], item_sj_pb['boundary_id']))

        # finalize validation for more_bfs table

        # start validation for less table

        errors_not_in_less = list()
        errors_duplicate_in_less = list()
        # start validation for more_bfs table
        # remove spatial join intersection with geometries that no contain lines.
        # Because it is not necessary to check topology register

        for inner_ring in dict_spatial_join_inner_rings_boundary:
            boundary_id = inner_ring['boundary_id']
            plot_ring_id = inner_ring['plot_ring_id']

            boundary_geom = dict_boundary[boundary_id].geometry()
            inner_ring_geom = dict_inner_rings[plot_ring_id].geometry()

            # check intersections difference to line, we check that collections dont have lines parts
            intersection = inner_ring_geom.intersection(boundary_geom)
            has_line = False
            if not intersection.isEmpty():
                if intersection.type() != QgsWkbTypes.LineGeometry:
                    if intersection.type() == QgsWkbTypes.UnknownGeometry:
                        for part in intersection.asGeometryCollection():
                            if part.isMultipart():
                                for i in range(part.numGeometries()):
                                    if QgsWkbTypes.geometryType(part.geometryN(i).wkbType()) == QgsWkbTypes.LineGeometry:
                                        has_line = True
                                        break
                            else:
                                if part.type() == QgsWkbTypes.LineGeometry:
                                    has_line = True
                                    break
                else:
                    has_line = True

            if has_line:
                tmp_dict_plot_boundary = {'plot_id': int(plot_ring_id.split('-')[0]), 'boundary_id': boundary_id}
                count_less = list_less.count(tmp_dict_plot_boundary)

                if count_less > 1:
                    errors_duplicate_in_less.append((plot_ring_id, boundary_id))  # duplicate in less table
                elif count_less == 0:
                    errors_not_in_less.append((plot_ring_id, boundary_id))  # not registered less table
        # finalize validation for less table

        # The result for each type of error is a list of list with the plot uuid, boundary uuid and geometry.
        # [[uuid_plot, uuid_boundary, geometry], [uuid_plot, uuid_boundary, geometry], ...]
        result_plot_no_covered_by_boundary = list()  # plot not covered by boundary
        result_duplicate_in_more_bfs = list()  # Duplicate in more bfs
        result_duplicate_in_less_bfs = list()  # Duplicate in less bfs
        result_not_registered_in_more_bfs = list()  # Not registered in more bfs
        result_not_registered_in_less_bfs = list()  # Not registered in less bfs

        # plot not covered by boundary
        if errors_plot_boundary_diffs:
            for plot_boundary_diff in errors_plot_boundary_diffs:
                plot_id = plot_boundary_diff['id']
                plot_geom = plot_boundary_diff['geometry']

                error_data = [dict_uuid_plots.get(plot_id), None, plot_geom]
                result_plot_no_covered_by_boundary.append(error_data)

        # Duplicate in more bfs
        if errors_duplicate_in_more_bfs:
            for error_more_bfs in set(errors_duplicate_in_more_bfs):
                plot_id = error_more_bfs[0]  # plot_id
                boundary_id = error_more_bfs[1]  # boundary_id
                plot_geom = dict_plot_as_lines[plot_id].geometry()

                error_data = [dict_uuid_plots.get(plot_id), dict_uuid_boundary.get(boundary_id), plot_geom]
                result_duplicate_in_more_bfs.append(error_data)

        # Duplicate in less bfs
        if errors_duplicate_in_less:
            for error_less in set(errors_duplicate_in_less):
                plot_ring_id = error_less[0]  # plot_ring_id
                plot_id = int(plot_ring_id.split('-')[0])  # plot_id
                boundary_id = error_less[1]  # boundary_id
                geom_ring = dict_inner_rings[plot_ring_id].geometry()

                error_data = [dict_uuid_plots.get(plot_id), dict_uuid_boundary.get(boundary_id), geom_ring]
                result_duplicate_in_less_bfs.append(error_data)

        # not registered more bfs
        if errors_not_in_more_bfs:
            for error_more_bfs in set(errors_not_in_more_bfs):
                plot_id = error_more_bfs[0]  # plot_id
                boundary_id = error_more_bfs[1]  # boundary_id
                plot_geom = dict_plot_as_lines[plot_id].geometry()

                error_data = [dict_uuid_plots.get(plot_id), dict_uuid_boundary.get(boundary_id), plot_geom]
                result_not_registered_in_more_bfs.append(error_data)

        # not registered less bfs
        if errors_not_in_less:
            for error_less in set(errors_not_in_less):
                plot_ring_id = error_less[0]  # plot_ring_id
                plot_id = int(plot_ring_id.split('-')[0])  # plot_id
                boundary_id = error_less[1]  # boundary_id
                geom_ring = dict_inner_rings[plot_ring_id].geometry()

                error_data = [dict_uuid_plots.get(plot_id), dict_uuid_boundary.get(boundary_id), geom_ring]
                result_not_registered_in_less_bfs.append(error_data)

        return (result_plot_no_covered_by_boundary,
                result_duplicate_in_more_bfs,
                result_duplicate_in_less_bfs,
                result_not_registered_in_more_bfs,
                result_not_registered_in_less_bfs)
