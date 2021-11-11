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
                              QObject)

from asistente_ladm_col.app_interface import AppInterface
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

        self._id = ""  # E.g., "IGAC-R1001"
        self._name = ""  # E.g., "Los puntos de lindero no deben superponerse"
        self._type = None  # E.g., EnumQualityRuleType.POINT
        self._tags = list()  # List of keywords to search for this QR. Must be lowercase.
        self._models = list()  # List of model keys required by this rule.

        # Dict with error codes (keys) and error messages (values)
        self._errors = dict()

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
