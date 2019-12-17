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
import json

from qgis.PyQt.QtCore import (QCoreApplication,
                              Qt,
                              QObject,
                              QSettings)

from asistente_ladm_col.config.gui.common_keys import *
from asistente_ladm_col.lib.logger import Logger


STEP_CODE_ACTION_MAPPING = {"001": ACTION_SCHEMA_IMPORT_SUPPLIES,
                            "002": ACTION_RUN_ETL_COBOL,
                            "003": ACTION_EXPORT_DATA_SUPPLIES,
                            "004": ACTION_ST_UPLOAD_XTF}

class STTaskSteps(QObject):
    """
    Manage task steps
    """
    def __init__(self, task_id, steps_data):
        QObject.__init__(self)
        self.logger = Logger()

        self.__steps = list()

        self.__initialize_steps(task_id, steps_data)

    def __initialize_steps(self, task_id, steps_data):
        """
        Get actions and add them to each step

        :param task_id: Id of the task (to retrieve steps status)
        :param steps_data: List of task steps. Each step is a dict with (at least) "description" y "code"
        :return: List of steps ready to use
        """
        for step_data in steps_data:
            step_data["action"] = self.__map_action_to_step(step_data["code"])
            step_data["status"] = step_data["status"]
            self.__steps.append(STTaskStep(step_data))

        self.load_status(task_id)  # Update status if found in QSettings

    def __map_action_to_step(self, code):
        """
        Get actions and add them to each step

        :param code:
        :return: action key corresponding to the given code
        """
        return STEP_CODE_ACTION_MAPPING[code] if code in STEP_CODE_ACTION_MAPPING else None

    def get_steps(self):
        return self.__steps

    def steps_complete(self):
        """
        :return: boolean --> Are all steps done?
        """
        for step in self.__steps:
            if not step.get_status():
                return False

        return True

    def save_status(self, task_id, steps_status):
        """
        Save status in QSettings

        :param task_id: Id of the task.
        :param steps_status: dict --> {step number: boolean status}
        """
        if steps_status:
            self.logger.debug(__name__, "Saving step status for task ({}): {}".format(task_id, steps_status))
            QSettings().setValue("Asistente-LADM_COL/transition_system/tasks/{}/step_status".format(task_id),
                                 json.dumps(steps_status))

            for i, step in enumerate(self.__steps):
                index = i + 1
                if index in steps_status:
                    step.set_status(steps_status[index])

    def load_status(self, task_id):
        """
        Load status from QSettings
        """
        try:
            status = json.loads(QSettings().value("Asistente-LADM_COL/transition_system/tasks/{}/step_status".format(task_id), "{}"))
        except TypeError as e:
            # The QSettings value is not in the format we expect, just reset it
            QSettings().setValue("Asistente-LADM_COL/transition_system/tasks/{}/step_status".format(task_id), "{}")
            return

        if status:
            self.logger.debug(__name__, "Loading step status for task ({}): {}".format(task_id, status))
            for i, step in enumerate(self.__steps):
                index = str(i+1)
                if index in status:
                    step.set_status(status[index])


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

    def set_status(self, status):
        self.__status = status