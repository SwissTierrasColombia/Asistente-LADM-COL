# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2020-04-02
        git sha              : :%H$
        copyright            : (C) 2020 by Leo Cardona (BSF Swissphoto)
        email                : leo.cardona.p@gmail.com
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
                              QVariant)
from qgis.core import QgsField

from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.config.quality_rules_config import (QUALITY_RULE_ID,
                                                            QUALITY_RULE_NAME,
                                                            QUALITY_RULE_TABLE_NAME,
                                                            QUALITY_RULE_TABLE_FIELDS,
                                                            QUALITY_RULE_DOMAIN_ERROR_CODES)


class QualityRule:
    def __init__(self, quality_rule_data):
        self.__quality_rule_data = quality_rule_data
        self.logger = Logger()
        self._rule_id = None
        self._rule_name = None
        self._error_table_name = None
        self._error_table_fields = None
        self._error_codes = None

        self._initialize_quality_rule()

    def _initialize_quality_rule(self):
        self.logger.info(__name__, "Creating quality rule...")
        common_fields = [QgsField(QCoreApplication.translate("QualityRule", "tipo_error"), QVariant.String),
                         QgsField(QCoreApplication.translate("QualityRule", "codigo_error"), QVariant.String)]

        if self.__quality_rule_data:
            self._rule_id = self.__quality_rule_data.get(QUALITY_RULE_ID)
            self._rule_name = self.__quality_rule_data.get(QUALITY_RULE_NAME)
            self._error_table_name = self.__quality_rule_data.get(QUALITY_RULE_TABLE_NAME)
            self._error_table_fields = self.__quality_rule_data.get(QUALITY_RULE_TABLE_FIELDS)

            if self._error_table_fields:
                self._error_table_fields.extend(common_fields)

            self._error_codes = self.__quality_rule_data.get(QUALITY_RULE_DOMAIN_ERROR_CODES)

    @property
    def rule_id(self):
        return self._rule_id

    @property
    def rule_name(self):
        return self._rule_name

    @property
    def error_table_name(self):
        return self._error_table_name

    @property
    def error_table_fields(self):
        return self._error_table_fields

    @property
    def error_codes(self):
        return self._error_codes
