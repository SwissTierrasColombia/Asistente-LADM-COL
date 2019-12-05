# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-12-05
        copyright            : (C) 2019 by Germán Carrillo (BSF Swissphoto)
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
from qgis.PyQt.QtCore import (QCoreApplication,
                              Qt,
                              QObject)

from asistente_ladm_col.config.gui.common_keys import *
from asistente_ladm_col.lib.logger import Logger


STEP_CODE_ACTION_MAPPING = {"001": ACTION_SCHEMA_IMPORT,
                            "002": ACTION_RUN_ETL_COBOL,
                            "003": ACTION_EXPORT_DATA,
                            "004": ACTION_ST_UPLOAD_XTF}

class STTaskSteps(QObject):
    """
    Manage task steps
    """
    def __init__(self, steps_data):
        QObject.__init__(self)
        self.logger = Logger()

        self.__steps = list()

        self.__initialize_steps(steps_data)

    def __initialize_steps(self, steps_data):
        """
        Get actions and add them to each step

        :param steps_data: List of task steps. Each step is a dict with (at least) "description" y "code"
        :return: List of steps ready to use
        """
        for step_data in steps_data:
            step_data["action"] = self.__map_action_to_step(step_data["code"])
            status = self.load_task_steps_status()
            step_data["status"] = status if status is not None else step_data["status"]
            self.__steps.append(STTaskStep(step_data))

    def __map_action_to_step(self, code):
        """
        Get actions and add them to each step

        :param code:
        :return: action key corresponding to the given code
        """
        return STEP_CODE_ACTION_MAPPING[code] if code in STEP_CODE_ACTION_MAPPING else None

    def get_steps(self):
        return self.__steps

    def save_task_steps_status(self):
        """
        Save status in QSettings
        """
        pass

    def load_task_steps_status(self):
        """
        Load status from QSettings
        """
        return None


class STTaskStep(QObject):
    """
    Single task step
    """
    def __init__(self, step_data):
        QObject.__init__(self)
        self.logger = Logger()

        self.__name = ""
        self.__description = ""
        self.__action = ""
        self.__status = False

        self.__initialize_task_step(step_data)

    def __initialize_task_step(self, step_data):
        self.__name = step_data["description"]
        self.__action = step_data["action"]
        self.__description = step_data["description"]
        self.__status = step_data["status"]

    def get_name(self):
        return self.__name

    def get_description(self):
        return self.__description

    def get_action(self):
        return self.__action

    def get_status(self):
        return self.__status