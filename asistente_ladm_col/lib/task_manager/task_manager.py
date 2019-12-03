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
import json
import requests

from qgis.PyQt.QtCore import (QCoreApplication,
                              Qt,
                              QObject)
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import (QMenu,
                                 QPushButton,
                                 QToolBar)

from asistente_ladm_col.config.general_config import ST_GET_TASKS_SERVICE_URL
from asistente_ladm_col.config.enums import LogHandlerEnum
from asistente_ladm_col.config.gui.common_keys import *
from asistente_ladm_col.config.gui.gui_config import GUI_Config
from asistente_ladm_col.gui.gui_builder.role_registry import Role_Registry
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.lib.task_manager.task import STTask
from asistente_ladm_col.utils.qt_utils import OverrideCursor


class STTaskManager(QObject):
    """
    Retrieve tasks for a user from the Transition System's Task Service and store them during the session.
    """
    def __init__(self):
        self.logger = Logger()
        self.__registered_tasks = dict()

    def __retrieve_tasks(self, st_user, task_type=None, task_status=None):
        headers = {
            'Authorization': "Bearer {}".format(st_user.get_token()),
            # 'User-Agent': "PostmanRuntime/7.20.1",
            'Accept': "*/*",
            'Cache-Control': "no-cache",
            # 'Postman-Token': "987c7fbf-af4d-42e8-adee-687f35f4a4a0,0547120a-6f8e-42a8-b97f-f052602cc7ff",
            # 'Host': "st.local:8090",
            'Accept-Encoding': "gzip, deflate",
            'Connection': "keep-alive",
            'cache-control': "no-cache"
        }

        try:
            self.logger.debug(__name__, "Retrieving tasks from server...")
            response = requests.request("GET", ST_GET_TASKS_SERVICE_URL, headers=headers)
        except requests.ConnectionError as e:
            msg = QCoreApplication.translate("TaskManager", "There was an error accessing the task service. Details: {}".format(e))
            self.logger.warning(__name__, msg)
            return False, msg

        status_OK = response.status_code == 200
        response_data = json.loads(response.text)
        if status_OK:
            # Parse, create and register tasks
            for task_data in response_data:
                task = STTask(task_data)
                if task.is_valid():
                    self.__register_task(task)
        else:
             if response.status_code == 500:
                msg = QCoreApplication.translate("STSession", "There is an error in the task server! Message from server: '{}'".format(response_data["message"]))
                self.logger.warning(__name__, msg)

    def get_tasks(self, st_user, task_type=None, task_status=None):
        if not self.__registered_tasks:
            self.__retrieve_tasks(st_user, task_type, task_status)

        return self.__registered_tasks

    def get_task(self, task_id):
        task = self.__registered_tasks[task_id] if task_id in self.__registered_tasks else None
        if task is None:
            self.logger.warning(__name__, "Task {} not found!!!".format(task_id))
        else:
            self.logger.info(__name__, "Task {} found!!!".format(task_id))
        return task

    def __register_task(self, task):
        self.logger.debug(__name__, "Task {} registered!".format(task.id()))
        self.__registered_tasks[task.id()] = task

    def unregister_tasks(self):
        for k,v in self.__registered_tasks.items():
            self.__registered_tasks[k] = None

        self.__registered_tasks = dict()
