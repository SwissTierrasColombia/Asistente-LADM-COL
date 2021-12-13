"""
/***************************************************************************
                              Asistente LADM-COL
                             --------------------
        begin           : 2021-12-13
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
from asistente_ladm_col.config.config_db_supported import ConfigDBsSupported
from asistente_ladm_col.config.enums import EnumQualityRuleType
from asistente_ladm_col.core.quality_rules.abstract_quality_rule import AbstractQualityRule
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.utils.abstract_class import AbstractQObjectMeta
from asistente_ladm_col.utils.quality_error_db_utils import save_errors


class AbstractLogicQualityRule(AbstractQualityRule, metaclass=AbstractQObjectMeta):
    """
    Abstract class for LADM-COL logic quality rules
    """
    def __init__(self):
        AbstractQualityRule.__init__(self)

        self._type = EnumQualityRuleType.LOGIC  # E.g., EnumQualityRuleType.POINT

    def _get_ladm_queries(self, engine):
        return ConfigDBsSupported().get_db_factory(engine).get_ladm_queries()
