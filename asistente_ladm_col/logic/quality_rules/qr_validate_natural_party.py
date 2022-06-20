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
from qgis.PyQt.QtCore import (QCoreApplication,
                              QSettings)

from qgis.core import QgsVectorLayer

from asistente_ladm_col.config.enums import EnumQualityRuleResult
from asistente_ladm_col.config.keys.common import QUALITY_RULE_LADM_COL_LAYERS
from asistente_ladm_col.config.layer_config import LADMNames
from asistente_ladm_col.config.ladm_names import (SPECIAL_CHARACTERS,
                                                  DIGITS)
from asistente_ladm_col.config.quality_rule_config import (QR_IGACR4007,
                                                           QRE_IGACR4007E01,
                                                           QRE_IGACR4007E02,
                                                           QRE_IGACR4007E03,
                                                           QRE_IGACR4007E04,
                                                           QRE_IGACR4007E05,
                                                           QRE_IGACR4007E06,
                                                           QRE_IGACR4007E07,
                                                           QRE_IGACR4007E08,
                                                           QRE_IGACR4007E09,
                                                           QRE_IGACR4007E10,
                                                           QRE_IGACR4007E11,
                                                           QRE_IGACR4007E12,
                                                           QRE_IGACR4007E13)
from asistente_ladm_col.core.quality_rules.abstract_logic_quality_rule import AbstractLogicQualityRule
from asistente_ladm_col.core.quality_rules.quality_rule_execution_result import QualityRuleExecutionResult
from asistente_ladm_col.lib.geometry import GeometryUtils
from asistente_ladm_col.logic.ladm_col.ladm_data import LADMData


class QRValidateNaturalParty(AbstractLogicQualityRule):
    """
    Check that natural party has not have data of legal party
    """
    _ERROR_01 = QRE_IGACR4007E01  # Business name must not be filled in
    _ERROR_02 = QRE_IGACR4007E02  # First last name is mandatory and must be filled in
    _ERROR_03 = QRE_IGACR4007E03  # First name is mandatory and must be filled in
    _ERROR_04 = QRE_IGACR4007E04  # Type of document must different from NIT
    _ERROR_05 = QRE_IGACR4007E05  # Sex field must be filled in
    _ERROR_06 = QRE_IGACR4007E06  # First last name cannot contain special characters
    _ERROR_07 = QRE_IGACR4007E07  # First last name cannot contain digits
    _ERROR_08 = QRE_IGACR4007E08  # First name cannot contain special characters
    _ERROR_09 = QRE_IGACR4007E09  # First name cannot contain digits
    _ERROR_10 = QRE_IGACR4007E10  # Second last name cannot contain special characters
    _ERROR_11 = QRE_IGACR4007E11  # Second last name cannot contain digits
    _ERROR_12 = QRE_IGACR4007E12  # Second name cannot contain special characters
    _ERROR_13 = QRE_IGACR4007E13  # Second name cannot contain digits

    def __init__(self):
        AbstractLogicQualityRule.__init__(self)

        self._id = QR_IGACR4007
        self._name = "Interesado natural no puede incluir datos de interesado jurídico"
        self._tags = ["igac", "instituto geográfico agustín codazzi", "lógica", "negocio", "interesado natural"]
        self._models = [LADMNames.SURVEY_MODEL_KEY]

        self._errors = {self._ERROR_01: "La razón social no debe estar diligenciada",
                        self._ERROR_02: "El primer apellido es obligatorio y debe estar diligenciado",
                        self._ERROR_03: "El primer nombre es obligatorio y debe estar diligenciado",
                        self._ERROR_04: "El tipo de documento debe ser diferente de NIT",
                        self._ERROR_05: "El campo 'Sexo' debe estar diligenciado",
                        self._ERROR_06: "El primer apellido no puede contener caracteres especiales",
                        self._ERROR_07: "El primer apellido no puede contener dígitos",
                        self._ERROR_08: "El primer nombre no puede contener caracteres especiales",
                        self._ERROR_09: "El primer nombre no puede contener dígitos",
                        self._ERROR_10: "El segundo apellido no puede contener caracteres especiales",
                        self._ERROR_11: "El segundo apellido no puede contener dígitos",
                        self._ERROR_12: "El segundo nombre no puede contener caracteres especiales",
                        self._ERROR_13: "El segundo nombre no puede contener dígitos"}

        # Optional. Only useful for display purposes.
        self._field_mapping = dict()  # E.g., {'id_objetos': 'ids_punto_lindero', 'valores': 'conteo'}

    def layers_config(self, names):
        return {QUALITY_RULE_LADM_COL_LAYERS: [names.LC_PARTY_T]}

    def _validate(self, db, db_qr, layer_dict, tolerance, **kwargs):
        self.progress_changed.emit(5)
        ladm_queries = self._get_ladm_queries(db.engine)

        pre_res, pre_obj = self._check_prerrequisite_layers(layer_dict)
        if not pre_res:
            return pre_obj

        error_state = None

        res, records = ladm_queries.get_invalid_col_party_type_natural(db)
        self.progress_changed.emit(40)

        if res:
            error_state = LADMData().get_domain_code_from_value(db_qr, db_qr.names.ERR_ERROR_STATE_D,
                                                                LADMNames.ERR_ERROR_STATE_D_ERROR_V)

            errors_rules = {
                self._ERROR_01: {'geometries': list(), 'data': list()},
                self._ERROR_02: {'geometries': list(), 'data': list()},
                self._ERROR_03: {'geometries': list(), 'data': list()},
                self._ERROR_04: {'geometries': list(), 'data': list()},
                self._ERROR_05: {'geometries': list(), 'data': list()},
                self._ERROR_06: {'geometries': list(), 'data': list()},
                self._ERROR_07: {'geometries': list(), 'data': list()},
                self._ERROR_08: {'geometries': list(), 'data': list()},
                self._ERROR_09: {'geometries': list(), 'data': list()},
                self._ERROR_10: {'geometries': list(), 'data': list()},
                self._ERROR_11: {'geometries': list(), 'data': list()},
                self._ERROR_12: {'geometries': list(), 'data': list()},
                self._ERROR_13: {'geometries': list(), 'data': list()}
            }

            progress = 40
            record_count = 0

            for record in records:
                record_count += 1
                if record[db.names.LC_PARTY_T_BUSINESS_NAME_F] > 0:
                    error_data = [  # [obj_uuids, rel_obj_uuids, values, details, state]
                        [record[db.names.T_ILI_TID_F]],
                        None,
                        None,
                        self._errors[self._ERROR_01],
                        error_state]
                    errors_rules[self._ERROR_01]['data'].append(error_data)

                if record[db.names.LC_PARTY_T_SURNAME_1_F] > 0:
                    error_data = [  # [obj_uuids, rel_obj_uuids, values, details, state]
                        [record[db.names.T_ILI_TID_F]],
                        None,
                        None,
                        self._errors[self._ERROR_02],
                        error_state]
                    errors_rules[self._ERROR_02]['data'].append(error_data)

                if record[db.names.LC_PARTY_T_FIRST_NAME_1_F] > 0:
                    error_data = [  # [obj_uuids, rel_obj_uuids, values, details, state]
                        [record[db.names.T_ILI_TID_F]],
                        None,
                        None,
                        self._errors[self._ERROR_03],
                        error_state]
                    errors_rules[self._ERROR_03]['data'].append(error_data)

                if record[db.names.LC_PARTY_T_DOCUMENT_TYPE_F] > 0:
                    error_data = [  # [obj_uuids, rel_obj_uuids, values, details, state]
                        [record[db.names.T_ILI_TID_F]],
                        None,
                        None,
                        self._errors[self._ERROR_04],
                        error_state]
                    errors_rules[self._ERROR_04]['data'].append(error_data)

                if record[db.names.LC_PARTY_T_GENRE_F] > 0:
                    error_data = [  # [obj_uuids, rel_obj_uuids, values, details, state]
                        [record[db.names.T_ILI_TID_F]],
                        None,
                        None,
                        self._errors[self._ERROR_05],
                        error_state]
                    errors_rules[self._ERROR_05]['data'].append(error_data)

                if record[db.names.LC_PARTY_T_SURNAME_1_F + '_' + SPECIAL_CHARACTERS] > 0:
                    error_data = [  # [obj_uuids, rel_obj_uuids, values, details, state]
                        [record[db.names.T_ILI_TID_F]],
                        None,
                        None,
                        self._errors[self._ERROR_06],
                        error_state]
                    errors_rules[self._ERROR_06]['data'].append(error_data)

                if record[db.names.LC_PARTY_T_SURNAME_1_F + '_' + DIGITS] > 0:
                    error_data = [  # [obj_uuids, rel_obj_uuids, values, details, state]
                        [record[db.names.T_ILI_TID_F]],
                        None,
                        None,
                        self._errors[self._ERROR_07],
                        error_state]
                    errors_rules[self._ERROR_07]['data'].append(error_data)

                if record[db.names.LC_PARTY_T_FIRST_NAME_1_F + '_' + SPECIAL_CHARACTERS] > 0:
                    error_data = [  # [obj_uuids, rel_obj_uuids, values, details, state]
                        [record[db.names.T_ILI_TID_F]],
                        None,
                        None,
                        self._errors[self._ERROR_08],
                        error_state]
                    errors_rules[self._ERROR_08]['data'].append(error_data)

                if record[db.names.LC_PARTY_T_FIRST_NAME_1_F + '_' + DIGITS] > 0:
                    error_data = [  # [obj_uuids, rel_obj_uuids, values, details, state]
                        [record[db.names.T_ILI_TID_F]],
                        None,
                        None,
                        self._errors[self._ERROR_09],
                        error_state]
                    errors_rules[self._ERROR_09]['data'].append(error_data)

                if record[db.names.LC_PARTY_T_SURNAME_2_F + '_' + SPECIAL_CHARACTERS] > 0:
                    error_data = [  # [obj_uuids, rel_obj_uuids, values, details, state]
                        [record[db.names.T_ILI_TID_F]],
                        None,
                        None,
                        self._errors[self._ERROR_10],
                        error_state]
                    errors_rules[self._ERROR_10]['data'].append(error_data)

                if record[db.names.LC_PARTY_T_SURNAME_2_F + '_' + DIGITS] > 0:
                    error_data = [  # [obj_uuids, rel_obj_uuids, values, details, state]
                        [record[db.names.T_ILI_TID_F]],
                        None,
                        None,
                        self._errors[self._ERROR_11],
                        error_state]
                    errors_rules[self._ERROR_11]['data'].append(error_data)

                if record[db.names.LC_PARTY_T_FIRST_NAME_2_F + '_' + SPECIAL_CHARACTERS] > 0:
                    error_data = [  # [obj_uuids, rel_obj_uuids, values, details, state]
                        [record[db.names.T_ILI_TID_F]],
                        None,
                        None,
                        self._errors[self._ERROR_12],
                        error_state]
                    errors_rules[self._ERROR_12]['data'].append(error_data)

                if record[db.names.LC_PARTY_T_FIRST_NAME_2_F + '_' + DIGITS] > 0:
                    error_data = [  # [obj_uuids, rel_obj_uuids, values, details, state]
                        [record[db.names.T_ILI_TID_F]],
                        None,
                        None,
                        self._errors[self._ERROR_13],
                        error_state]
                    errors_rules[self._ERROR_13]['data'].append(error_data)

                delta_progress = record_count * 50 /  len(records)
                self.progress_changed.emit(progress + delta_progress)

            count = 0
            for error_key, errors_rule in errors_rules.items():
                if errors_rule:
                    self._save_errors(db_qr, error_key, errors_rule)
                    count += len(errors_rule['data'])

            self.progress_changed.emit(90)

        if count > 0:
            res_type = EnumQualityRuleResult.ERRORS
            msg = QCoreApplication.translate("QualityRules", "{} natural parties with inconsistent were found.").format(
                count)
        else:
            res_type = EnumQualityRuleResult.SUCCESS
            msg = QCoreApplication.translate("QualityRules", "All natural parties have valid data.")

        self.progress_changed.emit(100)

        return QualityRuleExecutionResult(res_type, msg, count)