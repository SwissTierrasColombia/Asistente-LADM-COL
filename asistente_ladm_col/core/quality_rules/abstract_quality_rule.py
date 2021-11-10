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

    def _save_errors(self, db_qr, error_code, error_data, ili_name=''):
        """
        Save errors into DB with errores_calidad model structure

        :param db_qr: DBConnector of the target database
        :param error_code: Exactly as specified in error catalogues
        :param error_data: List of lists: [[obj_uuids, geometries, rel_obj_uuids, values, details], ...]
        :param ili_name: Interlis name of the class obj_uuids belong to.
        :return: Boolean, depending on whether the errors were saved or not.
        """

        pass  # self.app.core.get_layers()
