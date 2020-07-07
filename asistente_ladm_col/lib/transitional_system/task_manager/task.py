# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-11-28
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
from datetime import datetime

from qgis.PyQt.QtCore import QObject

from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.lib.transitional_system.task_manager.task_steps import STTaskSteps


class STTask(QObject):
    """
    Read and store task info
    """
    ID_KEY = 'id'
    NAME_KEY = 'name'
    DESCRIPTION_KEY = 'description'
    DEADLINE_KEY = 'deadline'
    CREATED_AT_KEY = 'createdAt'
    CLOSING_DATE_KEY = 'closingDate'
    TASK_STATE_KEY = 'taskState'
    MEMBERS_KEY = 'members'
    CATEGORIES_KEY = 'categories'
    DATA_KEY = 'data'

    def __init__(self, task_server_data):
        QObject.__init__(self)
        self.logger = Logger()
        self.__is_valid = True
        self.__id = None
        self.__name = None
        self.__description = None
        self.__deadline = None
        self.__created_at = None
        self.__closing_date = None
        self.__task_status = None
        self.__members = None
        self.__categories = None
        self.__data = None
        self.__task_steps = None

        self.__task_server_data = task_server_data

        self._initialize_task(task_server_data)

    def __get_mandatory_attributes(self):
            return {self.ID_KEY: self.__id,
                    self.NAME_KEY: self.__name,
                    self.CATEGORIES_KEY: self.__categories,
                    self.TASK_STATE_KEY: self.__task_status,
                    self.CREATED_AT_KEY: self.__created_at}

    def _initialize_task(self, task_server_data):
        self.logger.info(__name__, "Creating task...")
        if self.ID_KEY in task_server_data:
            self.__id = task_server_data[self.ID_KEY]
        if self.NAME_KEY in task_server_data:
            self.__name = task_server_data[self.NAME_KEY]
        if self.DESCRIPTION_KEY in task_server_data:
            self.__description = task_server_data[self.DESCRIPTION_KEY]
        if self.DEADLINE_KEY in task_server_data:
            self.__deadline = self.normalize_date(task_server_data[self.DEADLINE_KEY])
        if self.CREATED_AT_KEY in task_server_data:
            self.__created_at = self.normalize_date(task_server_data[self.CREATED_AT_KEY])
        if self.CLOSING_DATE_KEY in task_server_data:
            self.__closing_date = self.normalize_date(task_server_data[self.CLOSING_DATE_KEY])
        if self.TASK_STATE_KEY in task_server_data:
            self.__task_status = task_server_data[self.TASK_STATE_KEY]
        if self.MEMBERS_KEY in task_server_data:
            self.__members = task_server_data[self.MEMBERS_KEY]
        if self.CATEGORIES_KEY in task_server_data:
            self.__categories = task_server_data[self.CATEGORIES_KEY]
        if self.DATA_KEY in task_server_data:
            self.__data = task_server_data[self.DATA_KEY]

        for k, attribute in self.__get_mandatory_attributes().items():
            if attribute is None:
                self.logger.debug(__name__, "Missing attribute to create task: {}".format(k))
                self.__is_valid = False

        if self.__is_valid:
            self.__task_steps = STTaskSteps(self)

        self.logger.debug(__name__, "Is task valid? {}".format(self.is_valid()))

    def is_valid(self):
        return self.__is_valid

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_description(self):
        return self.__description

    def get_type(self):
        return self.__categories[0]['id'] if self.__categories is not None else None

    def get_deadline(self):
        return self.__deadline

    def get_creation_date(self):
        return self.__created_at

    def get_started_date(self):
        return self.__created_at

    def get_status(self):
        return self.__task_status['name'] if self.__task_status is not None else None

    def get_connection(self):
        pass

    def get_steps(self):
        return self.__task_steps.get_steps() if self.__task_steps is not None else list()

    def get_step(self, id):
        return self.__task_steps.get_step(id) if self.__task_steps is not None else None

    def steps_complete(self):
        return self.__task_steps.steps_complete() if self.__task_steps is not None else False

    def task_started(self):
        return self.__task_steps.steps_started() if self.__task_steps is not None else False

    def save_steps_status(self, steps_status):
        if self.__task_steps is not None:
            self.__task_steps.save_status(self.get_id(), steps_status)

    def close_task(self):
        pass

    def validate_task(self):
        pass

    def load_task_status(self):
        pass

    def save_task_status(self):
        pass

    def get_data(self):
        return self.__data

    def normalize_date(self, date_str):
        if date_str:
            date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f%z')  # e.g., '2019-02-01T08:01:31.664+0000'
            return date.strftime("%Y-%m-%d %H:%M")

        return ''