"""
/***************************************************************************
                              Asistente LADM-COL
                             --------------------
        begin           : 2021-12-13
        git sha         : :%H$
        copyright       : (C) 2021 by Germán Carrillo (SwissTierras Colombia)
                          (C) 2018 by Fernando Pineda (SwissTierras Colombia)
        email           : gcarrillo@linuxmail.org
                          wfpinedar@gmail.com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import (QCoreApplication,
                              QSettings)

from qgis.core import (Qgis,
                       QgsVectorLayer)

from asistente_ladm_col.config.keys.common import (QUALITY_RULE_LADM_COL_LAYERS,
                                                   QUALITY_RULE_ADJUSTED_LAYERS,
                                                   ADJUSTED_INPUT_LAYER,
                                                   ADJUSTED_REFERENCE_LAYER,
                                                   FIX_ADJUSTED_LAYER)
from asistente_ladm_col.config.general_config import DEFAULT_USE_ROADS_VALUE
from asistente_ladm_col.config.layer_config import LADMNames
from asistente_ladm_col.config.quality_rule_config import (QR_IGACR3006,
                                                           QRE_IGACR3006E01)
from asistente_ladm_col.core.quality_rules.abstract_polygon_quality_rule import AbstractPolygonQualityRule
from asistente_ladm_col.core.quality_rules.quality_rule_execution_result import QualityRuleExecutionResult
from asistente_ladm_col.core.quality_rules.quality_rule_option import (QualityRuleOption,
                                                                       QualityRuleOptions)
from asistente_ladm_col.lib.geometry import GeometryUtils


class QRGapsInPlots(AbstractPolygonQualityRule):
    """
    Check that there are no gaps in plots
    """
    _ERROR_01 = QRE_IGACR3006E01

    def __init__(self):
        AbstractPolygonQualityRule.__init__(self)

        self._id = QR_IGACR3006
        self._name = "No deben haber huecos entre terrenos"
        self._tags = ["igac", "instituto geográfico agustín codazzi", "polígonos", "terrenos", "huecos", "agujeros"]
        self._models = [LADMNames.SURVEY_MODEL_KEY]

        self._errors = {self._ERROR_01: "No deben haber huecos entre terrenos"}

        # Optional. Only useful for display purposes.
        self._field_mapping = dict()  # E.g., {'id_objetos': 'ids_punto_lindero', 'valores': 'conteo'}

    def layers_config(self, names):
        return {QUALITY_RULE_LADM_COL_LAYERS: [names.LC_PLOT_T],
                QUALITY_RULE_ADJUSTED_LAYERS: {
                    names.LC_PLOT_T: {
                        ADJUSTED_INPUT_LAYER: names.LC_PLOT_T,
                        ADJUSTED_REFERENCE_LAYER: names.LC_PLOT_T,
                        FIX_ADJUSTED_LAYER: True
                    }}}

    def _initialize_option_definition(self):
        dict_options = [
            QualityRuleOption('use_roads',
                              QCoreApplication.translate("QualityRules", "Use roads"),
                              QCoreApplication.translate("QualityRules",
                                                         "Take roads into account when checking for gaps in plots"),
                              True,
                              DEFAULT_USE_ROADS_VALUE)
        ]
        return QualityRuleOptions(dict_options)

    def validate(self, db, db_qr, layer_dict, tolerance, **kwargs):
        self.progress_changed.emit(5)

        option_check_res, res_obj = self._check_qr_options(kwargs)
        if not option_check_res:
            return res_obj

        self._read_option_values(kwargs['options'])

        plot_layer = self._get_layer(layer_dict)
        pre_res, res_obj = self._check_prerrequisite_layer(QCoreApplication.translate("QualityRules", "Plot"), plot_layer)
        if not pre_res:
            return res_obj

        self.progress_changed.emit(10)
        gaps = GeometryUtils.get_gaps_in_polygon_layer(plot_layer, self._options.use_roads)
        self.progress_changed.emit(60)

        res_type, msg = Qgis.NoLevel, ""
        if gaps:
            fids_list = GeometryUtils.get_intersection_features(plot_layer, gaps)  # List of lists of qgis ids
            self.progress_changed.emit(80)

            uuids_list = list()
            for fids in fids_list:
                # Note this preserve order from gaps list, so we are able
                # to get gap geometry and its correspondant t_ili_tid list
                uuids_list.append([f[db.names.T_ILI_TID_F] for f in plot_layer.getFeatures(fids)])

            errors = {'geometries': list(), 'data': list()}
            for serial, geometry in enumerate(gaps):
                errors['geometries'].append(geometry)

                error_data = [  # [obj_uuids, rel_obj_uuids, values, details]
                    uuids_list[serial],
                    None,
                    None,
                    None]
                errors['data'].append(error_data)

            self._save_errors(db_qr, self._ERROR_01, errors)
            self.progress_changed.emit(90)

            res_type = Qgis.Warning
            msg = QCoreApplication.translate("QualityRules", "{} gaps were found in 'Plot' layer.").format(len(gaps))
        else:
            res_type = Qgis.Success
            msg = QCoreApplication.translate("QualityRules", "There are no gaps in layer Plot.")

        self.progress_changed.emit(100)
        return QualityRuleExecutionResult(res_type, msg)
