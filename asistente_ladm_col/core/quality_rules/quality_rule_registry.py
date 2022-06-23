"""
/***************************************************************************
                              Asistente LADM-COL
                             --------------------
        begin           : 2021-11-08
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
from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.lib.model_registry import LADMColModelRegistry
from asistente_ladm_col.config.keys.common import ALL_QUALITY_RULES
from asistente_ladm_col.core.quality_rules.abstract_quality_rule import AbstractQualityRule
from asistente_ladm_col.gui.gui_builder.role_registry import RoleRegistry
from asistente_ladm_col.logic.quality_rules.qr_overlapping_boundary_points import QROverlappingBoundaryPoints
from asistente_ladm_col.logic.quality_rules.qr_overlapping_boundaries import QROverlappingBoundaries
from asistente_ladm_col.logic.quality_rules.qr_overlapping_buildings import QROverlappingBuildings
from asistente_ladm_col.logic.quality_rules.qr_validate_data_against_model import QRValidateDataAgainstModel
from asistente_ladm_col.logic.quality_rules.qr_gaps_in_plots import QRGapsInPlots
from asistente_ladm_col.logic.quality_rules.qr_multiparts_in_right_of_way import QRMultiPartsInRightOfWay
from asistente_ladm_col.logic.quality_rules.qr_parcel_right_relationship import QRParcelRightRelationship
from asistente_ladm_col.logic.quality_rules.qr_parcel_with_invalid_parcel_number import QRParcelWithInvalidParcelNumber
from asistente_ladm_col.logic.quality_rules.qr_parcel_with_invalid_previous_parcel_number import QRParcelWithInvalidPreviousParcelNumber
from asistente_ladm_col.logic.quality_rules.qr_parcel_department_field_valid_code import QRParcelWithInvalidDepartmentCode
from asistente_ladm_col.logic.quality_rules.qr_parcel_with_invalid_municipality_code import QRParcelWithInvalidMunicipalityCode
from asistente_ladm_col.logic.quality_rules.qr_validate_legal_party import QRValidateLegalParty
from asistente_ladm_col.logic.quality_rules.qr_duplicate_boundary_point_records import QRDuplicateBoundaryPointRecords
from asistente_ladm_col.logic.quality_rules.qr_duplicate_survey_point_records import QRDuplicateSurveyPointRecords
from asistente_ladm_col.logic.quality_rules.qr_duplicate_control_point_records import QRDuplicateControlPointRecords
from asistente_ladm_col.logic.quality_rules.qr_duplicate_administrative_source_records import QRDuplicateAdministrativeSourceRecords
from asistente_ladm_col.logic.quality_rules.qr_duplicate_boundary_records import QRDuplicateBoundaryRecords
from asistente_ladm_col.logic.quality_rules.qr_duplicate_building_records import QRDuplicateBuildingRecords
from asistente_ladm_col.logic.quality_rules.qr_duplicate_building_unit_records import QRDuplicateBuildingUnitRecords
from asistente_ladm_col.logic.quality_rules.qr_duplicate_party_records import QRDuplicatePartyRecords
from asistente_ladm_col.logic.quality_rules.qr_duplicate_right_records import QRDuplicateRightRecords
from asistente_ladm_col.logic.quality_rules.qr_duplicate_restriction_records import QRDuplicateRestrictionRecords
from asistente_ladm_col.utils.singleton import Singleton


class QualityRuleRegistry(metaclass=Singleton):
    """
    Registry of supported quality rules.
    """
    def __init__(self):
        self.logger = Logger()
        self.app = AppInterface()
        self.__quality_rules = dict()  # {quality_rule_key1: QualityRule1, ...}

        # Register default quality rules
        self.register_quality_rule(QRValidateDataAgainstModel())  # QR_ILIVALIDATORR0001
        self.register_quality_rule(QROverlappingBoundaryPoints())  # QR_IGACR1001
        self.register_quality_rule(QROverlappingBoundaries())  # QR_IGACR2001
        self.register_quality_rule(QROverlappingBuildings())  # QR_IGACR3002
        self.register_quality_rule(QRGapsInPlots())  # QR_IGACR3006
        self.register_quality_rule(QRMultiPartsInRightOfWay())  # QR_IGACR3007
        self.register_quality_rule(QRParcelRightRelationship())  # QR_IGACR4001
        self.register_quality_rule(QRParcelWithInvalidDepartmentCode())  # QR_IGACR4003
        self.register_quality_rule(QRParcelWithInvalidMunicipalityCode())  # QR_IGACR4004
        self.register_quality_rule(QRParcelWithInvalidParcelNumber())  # QR_IGACR4005
        self.register_quality_rule(QRParcelWithInvalidPreviousParcelNumber())  # QR_IGACR4006
        self.register_quality_rule(QRValidateLegalParty())  # QR_IGACR4008
        self.register_quality_rule(QRDuplicateBoundaryPointRecords())  # QR_IGACR4011
        self.register_quality_rule(QRDuplicateSurveyPointRecords())  # QR_IGACR4012
        self.register_quality_rule(QRDuplicateControlPointRecords())  # QR_IGACR4013
        self.register_quality_rule(QRDuplicateBoundaryRecords())  # QR_IGACR4014
        self.register_quality_rule(QRDuplicateBuildingRecords())  # QR_IGACR4016
        self.register_quality_rule(QRDuplicateBuildingUnitRecords())  # QR_IGACR4017
        self.register_quality_rule(QRDuplicatePartyRecords())  # QR_IGACR4019
        self.register_quality_rule(QRDuplicateRightRecords())  # QR_IGACR4020
        self.register_quality_rule(QRDuplicateRestrictionRecords())  # QR_IGACR4021
        self.register_quality_rule(QRDuplicateAdministrativeSourceRecords())  # QR_IGACR4022

    def register_quality_rule(self, quality_rule):
        """
        Registers a quality rule.

        :param quality_rule: QualityRule instance.
        :return: True if the quality rule was registered, False otherwise.
        """
        if not isinstance(quality_rule, AbstractQualityRule):
            self.logger.warning(__name__,
                                "The quality rule '{}' is not an 'AbstractQualityRule' instance!".format(quality_rule.id()))
            return False

        if not quality_rule.is_valid():
            self.logger.warning(__name__, "The quality rule '{}' is not valid! Check the quality rule definition!".format(
                quality_rule.id()))
            return False

        if quality_rule.id() in self.__quality_rules:
            self.logger.warning(__name__, "The quality rule '{}' is already registered.".format(quality_rule.id()))
            return False

        self.__quality_rules[quality_rule.id()] = quality_rule
        self.logger.info(__name__, "Quality rule '{}' has been registered!".format(quality_rule.id()))

        return True

    def unregister_quality_rule(self, quality_rule_id):
        """
        Unregisters a quality rule by id.

        :param quality_rule_id: Id of the quality rule to unregister.
        :return: True if the quality rule was unregistered, False otherwise.
        """
        if quality_rule_id not in self.__quality_rules:
            self.logger.error(__name__, "Quality rule '{}' was not found in registered quality rules, therefore, it cannot be unregistered!".format(quality_rule_id))
            return False

        self.__quality_rules[quality_rule_id] = None
        del self.__quality_rules[quality_rule_id]
        self.logger.info(__name__, "Quality rule '{}' has been unregistered!".format(quality_rule_id))

        return True

    def get_quality_rule(self, quality_rule_id):
        qr = self.__quality_rules.get(quality_rule_id, None)
        if not qr:
            self.logger.warning(__name__, "Quality rule '{}' is not registered, therefore it cannot be obtained!".format(quality_rule_id))

        return qr

    def get_qrs_per_role_and_models(self, db, as_dict=True):
        """
        :param as_dict: Boolean. If False, the result is returned as a list or rule keys
        """
        qrs = dict()
        role_registry = RoleRegistry()
        role_qrs = role_registry.get_role_quality_rules(role_registry.get_active_role())
        if role_qrs == ALL_QUALITY_RULES:
            role_qrs = self.__quality_rules

        if role_qrs:
            db_models = db.get_models()
            model_registry = LADMColModelRegistry()

            for qr in role_qrs:
                # First check if the role QR is registered
                if qr in self.__quality_rules:
                    # Then check if the models required by the QR are in the DB
                    req_models = self.__quality_rules[qr].models()
                    num_models = len(req_models)

                    all_models_found = True
                    if num_models:  # We don't check models if a QR has no required models (e.g., iliValidator)
                        for req_model in req_models:
                            model = model_registry.model(req_model)
                            model_key = model.full_name()
                            if model_key and model_key not in db_models:
                                all_models_found = False
                                self.logger.debug(__name__,
                                                  "Model '{}' not found in the DB. QR '{}' cannot be listed.".format(
                                                      model_key, qr
                                                  ))
                                break

                    if all_models_found:
                        qrs[qr] = self.__quality_rules[qr]

        return qrs if as_dict else list(qrs.keys())
