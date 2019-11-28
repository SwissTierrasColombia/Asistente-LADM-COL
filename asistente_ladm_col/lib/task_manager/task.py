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
from qgis.PyQt.QtCore import (QCoreApplication,
                              Qt,
                              QObject)
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import (QMenu,
                                 QPushButton,
                                 QToolBar)

from asistente_ladm_col.config.enums import LogHandlerEnum
from asistente_ladm_col.config.gui.common_keys import *
from asistente_ladm_col.config.gui.gui_config import GUI_Config
from asistente_ladm_col.gui.gui_builder.role_registry import Role_Registry
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.utils.qt_utils import OverrideCursor

class STTask(QObject):
    """
    Build plugin GUI according to roles and LADM_COL models present in the current db connection
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
    METADATA_KEY = 'metadata'

    def __init__(self, task_data):
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
        self.__metadata = None

        self._initialize_task(task_data)

    def __get_mandatory_attributes(self):
            return {self.ID_KEY: self.__id,
                    self.NAME_KEY: self.__name,
                    self.CATEGORIES_KEY: self.__categories,
                    self.TASK_STATE_KEY: self.__task_status,
                    self.CREATED_AT_KEY: self.__created_at}

    def _initialize_task(self, task_data):
        self.logger.info(__name__, "Creating task...")
        if self.ID_KEY in task_data:
            self.__id = task_data[self.ID_KEY]
        if self.NAME_KEY in task_data:
            self.__name = task_data[self.NAME_KEY]
        if self.DESCRIPTION_KEY in task_data:
            self.__description = task_data[self.DESCRIPTION_KEY]
        if self.DEADLINE_KEY in task_data:
            self.__deadline = task_data[self.DEADLINE_KEY]
        if self.CREATED_AT_KEY in task_data:
            self.__created_at = task_data[self.CREATED_AT_KEY]
        if self.CLOSING_DATE_KEY in task_data:
            self.__closing_date = task_data[self.CLOSING_DATE_KEY]
        if self.TASK_STATE_KEY in task_data:
            self.__task_status = task_data[self.TASK_STATE_KEY]
        if self.MEMBERS_KEY in task_data:
            self.__members = task_data[self.MEMBERS_KEY]
        if self.CATEGORIES_KEY in task_data:
            self.__categories = task_data[self.CATEGORIES_KEY]
        if self.METADATA_KEY in task_data:
            self.__metadata = task_data[self.METADATA_KEY]

        for k, attribute in self.__get_mandatory_attributes().items():
            if attribute is None:
                self.logger.debug(__name__, "Missing attribute to create task: {}".format(k))
                self.__is_valid = False

        self.logger.debug(__name__, "Task is valid? {}".format(self.is_valid()))

    def is_valid(self):
        return self.__is_valid

    def id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_description(self):
        return self.__description

    def get_type(self):
        return self.__categories[0]['name'] if self.__categories is not None else None

    def get_deadline(self):
        return self.__deadline

    def get_creation_date(self):
        return self.__created_at

    def get_status(self):
        return self.__task_status['name'] if self.__task_status is not None else None

    def get_connection(self):
        pass

    def close_task(self):
        pass

    def validate_task(self):
        pass

    def load_task_status(self):
        pass

    def save_task_status(self):
        pass
