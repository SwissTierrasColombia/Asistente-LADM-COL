"""
/***************************************************************************
                              Asistente LADM-COL
                             --------------------
        begin           : 2020-07-15
        git sha         : :%H$
        copyright       : (C) 2020 by Germán Carrillo (SwissTierras Colombia)
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
import os.path

from qgis.PyQt.QtCore import QSettings

from asistente_ladm_col.config.general_config import (TOLERANCE_MAX_VALUE,
                                                      PLUGIN_VERSION,
                                                      DEFAULT_TOLERANCE_VALUE,
                                                      DEFAULT_USE_CUSTOM_MODELS,
                                                      DEFAULT_MODELS_DIR)


class AppSettings:
    """
    Centralize application setting handlers and keys
    """

    # Note that keys should be accessible from the outside. Sometimes it's handy to
    # call functions that use app.settings.get_setting() and app.settings.set_setting()
    ACTIVE_ROLE_KEY = "Asistente-LADM-COL/roles/active_role_key_{}".format(PLUGIN_VERSION)
    COBOL_FILES_DIR_KEY = "Asistente-LADM-COL/etl_cobol/files_path"
    CUSTOM_MODELS_KEY = "Asistente-LADM-COL/models/use_custom_models"
    CUSTOM_MODEL_DIRS_KEY = "Asistente-LADM-COL/models/custom_model_dirs"
    ETL_SPLITTER_COLLAPSED_KEY = "Asistente-LADM-COL/supplies/etl_splitter_collapsed"
    EXPORT_DIR_FIELD_DATA_KEY = "Asistente-LADM-COL/field_data_capture/export_dir"
    SNC_FILES_DIR_KEY = "Asistente-LADM-COL/etl_snc/files_path"
    TOLERANCE_KEY = "Asistente-LADM-COL/quality/tolerance"

    def __init__(self):
        self.__settings = QSettings()
        self.__with_gui = True

    def get_setting(self, key):
        # Generic get_setting method
        return self.__settings.value(key, None)

    def set_setting(self, key, value):
        # Generic set_setting method
        self.__settings.setValue(key, value)

    @property
    def with_gui(self):
        return self.__with_gui

    @with_gui.setter
    def with_gui(self, with_gui):
        self.__with_gui = with_gui

    @property
    def active_role(self):
        return self.__settings.value(self.ACTIVE_ROLE_KEY, None)

    @active_role.setter
    def active_role(self, value):
        self.__settings.setValue(self.ACTIVE_ROLE_KEY, value)

    @property
    def cobol_files_path(self):
        return self.__settings.value(self.COBOL_FILES_DIR_KEY, '')

    @cobol_files_path.setter
    def cobol_files_path(self, value):
        self.__settings.setValue(self.COBOL_FILES_DIR_KEY, value)

    def add_custom_model_dir(self, model_dir):
        """
        :param model_dir: May consist of several paths separated by ;
        """
        self.custom_model_dirs = ";".join(list(set(self.custom_model_dirs.split(";") + model_dir.split(";"))))

    def remove_custom_model_dir(self, model_dir):
        """
        :param model_dir: May consist of several paths separated by ;
        """
        dirs = self.custom_model_dirs.split(";")
        for part_model_dir in model_dir.split(";"):
            if part_model_dir in dirs:
                dirs.remove(part_model_dir)

        self.custom_model_dirs = ";".join(dirs)

    @property
    def custom_model_dirs(self):
        return self.__settings.value(self.CUSTOM_MODEL_DIRS_KEY, DEFAULT_MODELS_DIR)

    @custom_model_dirs.setter
    def custom_model_dirs(self, value):
        self.__settings.setValue(self.CUSTOM_MODEL_DIRS_KEY, value)

    @property
    def custom_models(self):
        return self.__settings.value(self.CUSTOM_MODELS_KEY, DEFAULT_USE_CUSTOM_MODELS, bool)

    @custom_models.setter
    def custom_models(self, value):
        self.__settings.setValue(self.CUSTOM_MODELS_KEY, value)

    @property
    def etl_splitter_collapsed(self):
        return self.__settings.value(self.ETL_SPLITTER_COLLAPSED_KEY, False, bool)

    @etl_splitter_collapsed.setter
    def etl_splitter_collapsed(self, value):
        self.__settings.setValue(self.ETL_SPLITTER_COLLAPSED_KEY, value)

    @property
    def export_dir_field_data(self):
        return self.__settings.value(self.EXPORT_DIR_FIELD_DATA_KEY, os.path.expanduser('~'))

    @export_dir_field_data.setter
    def export_dir_field_data(self, value):
        self.__settings.setValue(self.EXPORT_DIR_FIELD_DATA_KEY, value)

    @property
    def snc_files_path(self):
        return self.__settings.value(self.SNC_FILES_DIR_KEY, '')

    @snc_files_path.setter
    def snc_files_path(self, value):
        self.__settings.setValue(self.SNC_FILES_DIR_KEY, value)

    @property
    def tolerance(self):
        q_tolerance = self.__settings.value(self.TOLERANCE_KEY, DEFAULT_TOLERANCE_VALUE, int)
        return q_tolerance if q_tolerance <= TOLERANCE_MAX_VALUE else TOLERANCE_MAX_VALUE

    @tolerance.setter
    def tolerance(self, value):
        tolerance = DEFAULT_TOLERANCE_VALUE  # If value is invalid (less than 0), we'll set the default value
        if value >= TOLERANCE_MAX_VALUE:
            tolerance = TOLERANCE_MAX_VALUE
        elif TOLERANCE_MAX_VALUE > value >= 0:
            tolerance = value
        self.__settings.setValue(self.TOLERANCE_KEY, tolerance)
