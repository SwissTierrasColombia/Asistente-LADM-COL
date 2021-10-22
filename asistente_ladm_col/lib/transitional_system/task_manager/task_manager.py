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
                              QObject,
                              pyqtSignal)

from asistente_ladm_col.config.transitional_system_config import TransitionalSystemConfig
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.lib.transitional_system.task_manager.task import STTask
from asistente_ladm_col.utils.decorators import with_override_cursor


class STTaskManager(QObject):
    """
    Retrieve tasks for a user from the Transitional System's Task Service and store them during the session.
    """
    task_started = pyqtSignal(int)  # task_id
    task_canceled = pyqtSignal(int)  # task_id
    task_closed = pyqtSignal(int)  # task_id

    def __init__(self):
        QObject.__init__(self)
        self.logger = Logger()
        self.__registered_tasks = dict()
        self.st_config = TransitionalSystemConfig()

    @with_override_cursor
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
            response = requests.request("GET", self.st_config.ST_GET_TASKS_SERVICE_URL, headers=headers)
        except requests.ConnectionError as e:
            msg = self.st_config.ST_CONNECTION_ERROR_MSG.format(e)
            self.logger.warning(__name__, msg)
            return False, msg

        status_OK = response.status_code == 200
        if status_OK:
            # Parse, create and register tasks
            response_data = json.loads(response.text)
            for task_data in response_data:
                task = STTask(task_data)
                if task.is_valid():
                    self.__register_task(task)
        else:
             if response.status_code == 500:
                 self.logger.warning(__name__, self.st_config.ST_STATUS_500_MSG)
             elif response.status_code > 500 and response.status_code < 600:
                 self.logger.warning(__name__, self.st_config.ST_STATUS_GT_500_MSG)
             elif response.status_code == 401:
                 self.logger.warning(__name__, self.st_config.ST_STATUS_401_MSG)

    def get_tasks(self, st_user, task_type=None, task_status=None):
        """
        Go to server for current tasks per user
        :param st_user:
        :param task_type: To filter task types. Still unused.
        :param task_status: To filter task statuses. Still unused.
        :return: dict of task ids with the corresponding task object
        """
        # Each call refreshes the registered tasks.
        self.unregister_tasks()
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
        self.logger.debug(__name__, "Task {} registered!".format(task.get_id()))
        self.__registered_tasks[task.get_id()] = task

    def __unregister_task(self, task_id):
        self.logger.debug(__name__, "Task {} unregistered!".format(task_id))
        self.__registered_tasks[task_id] = None
        del self.__registered_tasks[task_id]

    def unregister_tasks(self):
        for k,v in self.__registered_tasks.items():
            self.__registered_tasks[k] = None

        self.__registered_tasks = dict()
        self.logger.info(__name__, "All tasks have been unregistered!")

    @with_override_cursor
    def start_task(self, st_user, task_id):
        payload = {}
        headers = {
            'Authorization': "Bearer {}".format(st_user.get_token()),
        }

        try:
            self.logger.debug(__name__, "Telling the server to start a task...")
            response = requests.request("PUT", self.st_config.ST_START_TASK_SERVICE_URL.format(task_id), headers=headers, data=payload)
        except requests.ConnectionError as e:
            msg = self.st_config.ST_CONNECTION_ERROR_MSG.format(e)
            self.logger.warning(__name__, msg)
            return False, msg

        status_OK = response.status_code == 200
        if status_OK:
            # Parse response
            response_data = json.loads(response.text)
            self.logger.info(__name__, "Task id '{}' started in server!...".format(task_id))
            self.logger.info_msg(__name__, QCoreApplication.translate("TaskManager",
                                                                      "The task '{}' was successfully started!".format(
                                                                          self.get_task(task_id).get_name())))
            self.update_task_info(task_id, response_data)
            self.task_started.emit(task_id)
        else:
            if response.status_code == 500:
                self.logger.warning(__name__, self.st_config.ST_STATUS_500_MSG)
            elif response.status_code > 500 and response.status_code < 600:
                self.logger.warning(__name__, self.st_config.ST_STATUS_GT_500_MSG)
            elif response.status_code == 401:
                self.logger.warning(__name__, self.st_config.ST_STATUS_401_MSG)
            else:
                self.logger.warning(__name__, "Status code not handled: {}".format(response.status_code))

    @with_override_cursor
    def cancel_task(self, st_user, task_id, reason):
        payload = json.dumps({"reason": reason})
        headers = {
            'Authorization': "Bearer {}".format(st_user.get_token()),
            'Content-Type': 'application/json'
        }

        try:
            self.logger.debug(__name__, "Telling the server to cancel a task...")
            response = requests.request("PUT", self.st_config.ST_CANCEL_TASK_SERVICE_URL.format(task_id), headers=headers, data=payload)
        except requests.ConnectionError as e:
            msg = self.st_config.ST_CONNECTION_ERROR_MSG.format(e)
            self.logger.warning(__name__, msg)
            return False, msg

        status_OK = response.status_code == 200
        if status_OK:
            # No need to parse response this time, we'll ask tasks from server again anyways
            self.logger.info(__name__, "Task id '{}' canceled in server!".format(task_id))
            self.logger.info_msg(__name__, QCoreApplication.translate("TaskManager", "The task '{}' was successfully canceled!".format(self.get_task(task_id).get_name())))
            self.task_canceled.emit(task_id)
        else:
            if response.status_code == 500:
                self.logger.warning(__name__, self.st_config.ST_STATUS_500_MSG)
            elif response.status_code > 500 and response.status_code < 600:
                self.logger.warning(__name__, self.st_config.ST_STATUS_GT_500_MSG)
            elif response.status_code == 401:
                self.logger.warning(__name__, self.st_config.ST_STATUS_401_MSG)
            else:
                self.logger.warning(__name__, "Status code not handled: {}, payload: {}".format(response.status_code, payload))

    @with_override_cursor
    def close_task(self, st_user, task_id):
        payload = {}
        headers = {
            'Authorization': "Bearer {}".format(st_user.get_token()),
        }

        try:
            self.logger.debug(__name__, "Telling the server to close a task...")
            response = requests.request("PUT", self.st_config.ST_CLOSE_TASK_SERVICE_URL.format(task_id), headers=headers, data=payload)
        except requests.ConnectionError as e:
            msg = self.st_config.ST_CONNECTION_ERROR_MSG.format(e)
            self.logger.warning(__name__, msg)
            return False, msg

        status_OK = response.status_code == 200
        if status_OK:
            # No need to parse response this time, we'll ask tasks from server again anyways
            self.logger.success(__name__, "Task id '{}' closed in server!".format(task_id))
            self.logger.success_msg(__name__, QCoreApplication.translate("TaskManager",
                                                                      "The task '{}' was successfully closed!".format(
                                                                          self.get_task(task_id).get_name())))
            self.task_closed.emit(task_id)
        else:
            if response.status_code == 500:
                self.logger.warning(__name__, self.st_config.ST_STATUS_500_MSG)
            elif response.status_code > 500 and response.status_code < 600:
                self.logger.warning(__name__, self.st_config.ST_STATUS_GT_500_MSG)
            elif response.status_code == 401:
                self.logger.warning(__name__, self.st_config.ST_STATUS_401_MSG)
            elif response.status_code == 422:
                response_data = json.loads(response.text)
                msg = QCoreApplication.translate("STSession", QCoreApplication.translate("TaskManager",
                    "Task not closed! Details: {}").format(response_data['message'] if 'message' in response_data else "Unreadable response from server."))
                self.logger.warning_msg(__name__, msg)
            else:
                self.logger.warning(__name__, "Status code not handled: {}".format(response.status_code))

    def update_task_info(self, task_id, task_data):
        task = STTask(task_data)
        if task.is_valid():
            self.__unregister_task(task_id)
            self.__register_task(task)

