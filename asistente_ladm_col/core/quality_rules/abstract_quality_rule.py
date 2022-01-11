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
from abc import abstractmethod

from qgis.PyQt.QtCore import (pyqtSignal,
                              QObject,
                              QCoreApplication)

from qgis.core import Qgis

from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.config.keys.common import QUALITY_RULE_LAYERS
from asistente_ladm_col.core.quality_rules.quality_rule_execution_result import QualityRuleExecutionResult
from asistente_ladm_col.core.quality_rules.quality_rule_option import QualityRuleOptions
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.utils.abstract_class import AbstractQObjectMeta
from asistente_ladm_col.utils.quality_error_db_utils import save_errors


class AbstractQualityRule(QObject, metaclass=AbstractQObjectMeta):
    """
    Abstract class for LADM-COL quality rules
    """
    progress_changed = pyqtSignal(int)

    def __init__(self):
        QObject.__init__(self)

        self.app = AppInterface()
        self.logger = Logger()

        self._id = ""  # E.g., "IGAC-R1001"
        self._name = ""  # E.g., "Los puntos de lindero no deben superponerse"
        self._type = None  # E.g., EnumQualityRuleType.POINT
        self._tags = list()  # List of keywords to search for this QR. Must be lowercase.
        self._models = list()  # List of model keys required by this rule.

        # Dict with error codes (keys) and error messages (values)
        self._errors = dict()

        self._options = self._initialize_option_definition()

        # Optional. Only useful for display purposes.
        self._field_mapping = dict()  # E.g., {'id_objetos': 'ids_punto_lindero', 'valores': 'conteo'}

    def id(self):
        return self._id

    def name(self):
        return self._name

    def type(self):
        return self._type

    def tags(self):
        return self._tags

    def models(self):
        return self._models

    def field_mapping(self):
        return self._field_mapping

    @staticmethod
    def layers_config(names):
        # Dictionary of layer configuration. Specifies which layers are needed
        # by the rule and how it needs them for a 'tolerance > 0' scenario.
        return dict()

    def is_valid(self):
        return bool(self.id().strip()) and bool(self.name().strip()) and len(self._errors) and self._type is not None

    @abstractmethod
    def validate(self, db, db_qr, layer_dict, tolerance, **kwargs):
        """
        Validate the quality rule.

        :param db: DBConnector to main DB
        :param db_qr: DBConnector to quality rules DB
        :param layer_dict: Resolved layers (from LADM and/or after snapping)
        :param tolerance: Tolerance in millimeters
        :param kwargs: Other parameters needed by the rule. Optional.
        :return: An instance of QualityRuleExecutionResult
        """
        raise NotImplementedError

    def validate_features(self, features=None, feature_ids=list()):
        return False

    def _initialize_option_definition(self):
        """
        Overwrite this method if needed.
        """
        return QualityRuleOptions(list())

    def _read_option_values(self, option_values):
        # Create member variables per option to ease value access
        for k,v in self._options.get_options().items():
            setattr(self._options, k, option_values.get(k, v.default_value()))

    def _save_errors(self, db_qr, error_code, error_data, target_layer=None, ili_name=None):
        """
        Save errors into DB with errores_calidad model structure

        :param db_qr: DBConnector of the target database
        :param error_code: Exactly as specified in error catalogs
        :param error_data: Dict of lists:
                           {'geometries': [geometries], 'data': [obj_uuids, rel_obj_uuids, values, details]}
                           Note: this dict will always have 2 elements.
                           Note 2: For geometry errors, this dict will always have the same number of elements in
                                   each of the two lists (and the element order matters!).
                           Note 3: For geometryless errors, the 'geometries' value won't be even read.
        :param target_layer: Useful if a rule of one type needs to write the error in an error layer that doesn't
                             correspond to its type. For instance, a line QR that needs to write an error as point.
                             By default None, which means the self._type should be used to know the target layer.
        :param ili_name: Interlis name of the class obj_uuids belong to.
        :return: Boolean, depending on whether the errors were saved or not.
        """
        target_layer = self._type if target_layer is None else target_layer
        res, msg = save_errors(db_qr, self._id, error_code, error_data, target_layer, ili_name=None)
        print(res, msg)

    def _check_prerrequisite_layers(self, layer_dict):
        """
        Use it when you don't need the layers themselves,
        but just to verify if the layers are valid and have features.
        """
        for layer_name, layer in layer_dict[QUALITY_RULE_LAYERS].items():
            res, obj = self._check_prerrequisite_layer(layer_name, layer)
            if not res:
                return res, obj

        return True, None

    def _check_prerrequisite_layer(self, layer_name, layer):
        if not layer:
            return False, QualityRuleExecutionResult(Qgis.Critical,
                                                     QCoreApplication.translate("QualityRules",
                                                                                "'{}' layer not found!").format(
                                                         layer_name))
        if layer.featureCount() == 0:
            return False, QualityRuleExecutionResult(Qgis.NoLevel,
                                                     QCoreApplication.translate("QualityRules",
                                                                                "There are no records in layer '{}' to validate the quality rule!").format(
                                                         layer.name()))

        return True, None

    def _check_qr_options(self, params):
        if self._options.get_num_mandatory_options():
            mandatory_option_keys = [o.id() for o in self._options.get_mandatory_option_list()]
            if 'options' not in params:  # No options at all
                return False, QualityRuleExecutionResult(Qgis.Critical,
                                                         QCoreApplication.translate("QualityRules",
                                                                                    "No options were given to the quality rule, but it requires {} mandatory options ({})!").format(
                                                             self._options.get_num_mandatory_options(),
                                                             ", ".join(mandatory_option_keys)))

            # Now check that we've got all mandatory options
            not_found = [k for k in mandatory_option_keys if k not in params['options']]
            if not_found:
                return False, QualityRuleExecutionResult(Qgis.Critical,
                                                         QCoreApplication.translate("QualityRules",
                                                                                    "The following mandatory options were missing: '{}'!").format(
                                                             "', '".join(not_found)))

        return True, None

    def _get_layer(self, layer_dict, layer_name=''):
        """
        Get layer from layer_dict based on a layer name.

        If layer_name is not passed, the first layer in layer_dict will be returned,
        so this option is suitable for getting a layer when there is only one in the dict.
        """
        if layer_name:
            return layer_dict[QUALITY_RULE_LAYERS][layer_name]
        else:
            for layer_name, layer in layer_dict[QUALITY_RULE_LAYERS].items():
                return layer  # Get the first one

        return None
