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
import os.path

from qgis.PyQt.QtCore import QSettings

from asistente_ladm_col.config.general_config import (TOLERANCE_MAX_VALUE,
                                                      PLUGIN_VERSION)


class AppSettings:
    """
    Centralize application setting handlers and keys
    """
    ACTIVE_ROLE_KEY = "Asistente-LADM-COL/roles/active_role_key_{}".format(PLUGIN_VERSION)
    COBOL_FILES_DIR_KEY = "Asistente-LADM-COL/etl_cobol/files_path"
    ETL_SPLITTER_COLLAPSED_KEY = "Asistente-LADM-COL/etl_supplies/splitter_collapsed"
    EXPORT_DIR_FIELD_DATA_KEY = "Asistente-LADM-COL/field_data_capture/export_dir"
    SNC_FILES_DIR_KEY = "Asistente-LADM-COL/etl_snc/files_path"
    TOLERANCE_KEY = "Asistente-LADM-COL/quality/tolerance"

    def __init__(self):
        self.settings = QSettings()

    def get_setting(self, key):
        # Generic get_setting method
        return self.settings.value(key, None)

    def set_setting(self, key, value):
        # Generic set_setting method
        self.settings.setValue(key, value)

    @property
    def active_role(self):
        return self.settings.value(self.ACTIVE_ROLE_KEY, None)

    @active_role.setter
    def active_role(self, value):
        self.settings.setValue(self.ACTIVE_ROLE_KEY, value)

    @property
    def cobol_files_path(self):
        return self.settings.value(self.COBOL_FILES_DIR_KEY, '')

    @cobol_files_path.setter
    def cobol_files_path(self, value):
        self.settings.setValue(self.COBOL_FILES_DIR_KEY, value)

    @property
    def etl_splitter_collapsed(self):
        return self.settings.value(self.ETL_SPLITTER_COLLAPSED_KEY, False, bool)

    @etl_splitter_collapsed.setter
    def etl_splitter_collapsed(self, value):
        self.settings.setValue(self.ETL_SPLITTER_COLLAPSED_KEY, value)

    @property
    def export_dir_field_data(self):
        return self.settings.value(self.EXPORT_DIR_FIELD_DATA_KEY, os.path.expanduser('~'))

    @export_dir_field_data.setter
    def export_dir_field_data(self, value):
        self.settings.setValue(self.EXPORT_DIR_FIELD_DATA_KEY, value)

    @property
    def snc_files_path(self):
        return self.settings.value(self.SNC_FILES_DIR_KEY, '')

    @snc_files_path.setter
    def snc_files_path(self, value):
        self.settings.setValue(self.SNC_FILES_DIR_KEY, value)

    @property
    def tolerance(self):
        q_tolerance = self.settings.value(self.TOLERANCE_KEY, 0, int)
        return q_tolerance if q_tolerance <= TOLERANCE_MAX_VALUE else TOLERANCE_MAX_VALUE

    @tolerance.setter
    def tolerance(self, value):
        self.settings.setValue(self.TOLERANCE_KEY, value if value <= TOLERANCE_MAX_VALUE else TOLERANCE_MAX_VALUE)
