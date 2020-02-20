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

from qgis.PyQt.QtCore import (QObject,
                              QSettings,
                              QCoreApplication)

from asistente_ladm_col.config.task_steps_config import (TaskStepsConfig,
                                                         STEP_NUMBER,
                                                         STEP_NAME,
                                                         STEP_TYPE,
                                                         STEP_DESCRIPTION,
                                                         STEP_ACTION,
                                                         STEP_CUSTOM_ACTION_SLOT)
from asistente_ladm_col.lib.logger import Logger


class STTaskSteps(QObject):
    """
    Manage task steps
    """
    def __init__(self, task):
        QObject.__init__(self)
        self.task = task
        self.task_id = task.get_id()
        self.task_type = task.get_type()
        self.logger = Logger()

        self.__steps = list()
        self.task_steps_config = TaskStepsConfig()

        self.__initialize_steps()

    def __initialize_steps(self):
        """
        Get actions from task step config and create STTaskStep objects for the task
        :return: List of steps ready to use
        """
        steps_data = self.task_steps_config.get_steps_config(self.task)
        self.logger.info(__name__, "{} steps found for task id {}!".format(len(steps_data), self.task_id))

        for step_data in steps_data:
            step = STTaskStep(step_data)
            if step.is_valid():
                self.__steps.append(step)
            else:
                self.logger.error_msg(__name__, QCoreApplication.translate("STTaskSteps",
                                                                           "The step '{} ({})' for the task '{} ({})' is invalid!").format(
                    step.get_name(), step.get_id(), self.task.get_name(), self.task.get_id()))

        self.load_status(self.task_id)  # Update status if found in QSettings

    def get_steps(self):
        return self.__steps

    def get_step(self, id):
        for step in self.__steps:
            if step.get_id() == id:
                return step

        self.logger.warning(__name__, "Step '{}' not found!".format(id))
        return None

    def steps_complete(self):
        """
        :return: boolean --> Are all steps done?
        """
        for step in self.__steps:
            if not step.get_status():
                return False

        return True

    def steps_started(self):
        """
        :return: boolean --> Whether at least one step is done or not
        """
        count = 0
        for step in self.__steps:
            if step.get_status():
                count += 1

        return count > 0  # and count < len(self.__steps)

    def save_status(self, task_id, steps_status):
        """
        Save status in QSettings

        :param task_id: Id of the task.
        :param steps_status: dict --> {step number: boolean status}
        """
        if steps_status:
            self.logger.debug(__name__, "Saving step status for task ({}): {}".format(task_id, steps_status))
            QSettings().setValue("Asistente-LADM_COL/transitional_system/tasks/{}/step_status".format(task_id),
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
            status = json.loads(QSettings().value("Asistente-LADM_COL/transitional_system/tasks/{}/step_status".format(task_id), "{}"))
        except TypeError as e:
            # The QSettings value is not in the format we expect, just reset it
            QSettings().setValue("Asistente-LADM_COL/transitional_system/tasks/{}/step_status".format(task_id), "{}")
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

        self.__id = None
        self.__name = ""
        self.__type = ""
        self.__description = ""
        self.__action_tag = ""
        self.__custom_action_slot = None
        self.__status = False

        self.__initialize_task_step(step_data)

    def __initialize_task_step(self, step_data):
        self.__id = step_data[STEP_NUMBER] if STEP_NUMBER in step_data else None
        self.__name = step_data[STEP_NAME] if STEP_NAME in step_data else ""
        self.__type = step_data[STEP_TYPE] if STEP_TYPE in step_data else ""
        self.__action_tag = step_data[STEP_ACTION] if STEP_ACTION in step_data else ""
        self.__description = step_data[STEP_DESCRIPTION] if STEP_DESCRIPTION in step_data else ""
        self.__custom_action_slot = step_data[STEP_CUSTOM_ACTION_SLOT] if STEP_CUSTOM_ACTION_SLOT in step_data else None

    def is_valid(self):
        """
        Check if mandatory step data is set. Concerning the actions, either action_tag or custom action slot should be
        set

        :return: Whether the mandatory step data is set or not.
        """
        return self.__id is not None and self.__name and self.__type and \
               (self.__action_tag or self.__custom_action_slot is not None)

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_type(self):
        return self.__type

    def get_description(self):
        return self.__description

    def get_action_tag(self):
        return self.__action_tag

    def get_custom_action_slot(self):
        return self.__custom_action_slot

    def get_status(self):
        return self.__status

    def set_status(self, status):
        self.__status = status