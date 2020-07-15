# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2020-07-15
        git sha              : :%H$
        copyright            : (C) 2020 by Germán Carrillo (SwissTierras Colombia)
        email                : gcarrillo@linuxmail.org
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QSettings

from asistente_ladm_col.config.general_config import TOLERANCE_MAX_VALUE


class AppSettings:
    """
    Centralize application setting handlers and keys
    """
    TOLERANCE_KEY = 'Asistente-LADM-COL/quality/tolerance'

    def __init__(self):
        self.settings = QSettings()

    @property
    def tolerance(self):
        q_tolerance = self.settings.value(self.TOLERANCE_KEY, 0, int)
        return q_tolerance if q_tolerance <= TOLERANCE_MAX_VALUE else TOLERANCE_MAX_VALUE

    @tolerance.setter
    def tolerance(self, value):
        self.settings.setValue(self.TOLERANCE_KEY, value if value <= TOLERANCE_MAX_VALUE else TOLERANCE_MAX_VALUE)
