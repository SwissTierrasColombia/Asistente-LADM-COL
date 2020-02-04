# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-11-20
        git sha              : :%H$
        copyright            : (C) 2017 by Germán Carrillo (BSF Swissphoto)
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
import requests
from requests.adapters import HTTPAdapter
import json

from qgis.PyQt.QtCore import (QObject,
                              QCoreApplication,
                              QSettings,
                              pyqtSignal)

from asistente_ladm_col.config.transition_system_config import TransitionSystemConfig
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.lib.transition_system.task_manager.task_manager import STTaskManager
from asistente_ladm_col.utils.singleton import SingletonQObject


class STSession(QObject, metaclass=SingletonQObject):
    TOKEN_KEY = "Asistente-LADM_COL/transition_system/token"

    login_status_changed = pyqtSignal(bool)  # Status of the login: True if a user is logged in, False otherwise
    logout_finished = pyqtSignal()

    def __init__(self):
        QObject.__init__(self)
        self.logger = Logger()
        self.task_manager = STTaskManager()
        self.__logged_user = None

    def login(self, user, password):
        msg = ""
        st_config = TransitionSystemConfig()
        payload = st_config.ST_LOGIN_SERVICE_PAYLOAD.format(user, password)
        headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'Authorization': st_config.ST_LOGIN_AUTHORIZATION_CLIENT,
            'Accept': "*/*",
            'Cache-Control': "no-cache",
            'Accept-Encoding': "gzip, deflate",
            'Connection': "keep-alive",
            'cache-control': "no-cache"
        }
        s = requests.Session()
        s.mount(st_config.ST_LOGIN_SERVICE_URL, HTTPAdapter(max_retries=0))

        try:
            response = s.request("POST", st_config.ST_LOGIN_SERVICE_URL, data=payload, headers=headers)
        except requests.ConnectionError as e:
            msg = QCoreApplication.translate("STSession", "There was an error accessing the login service. Details: {}").format(e)
            self.logger.warning(__name__, msg)
            return False, msg

        status_OK = response.status_code == 200
        self.logger.info(__name__, "Login response status code: {}".format(response.status_code))
        if status_OK:
            msg = QCoreApplication.translate("STSession", "User logged in successfully!")
            logged_data = json.loads(response.text)
            self.__logged_user = STLoggedUser("{} {}".format(logged_data['first_name'],
                                                             logged_data['last_name']),
                                              logged_data['email'],
                                              logged_data['roles'][0]['name'],
                                              logged_data['access_token'])
            QSettings().setValue(self.TOKEN_KEY, logged_data['access_token'])  # Register (login) the user
            self.login_status_changed.emit(True)
            self.logger.info(__name__, msg)
        else:
            if response.status_code == 400:
                msg = QCoreApplication.translate("STSession",
                                                 "Wrong user name or password, change credentials and try again.")
            elif response.status_code == 500:
                msg = QCoreApplication.translate("STSession", "There is an error in the login server!")
            elif response.status_code == 401:
                msg = QCoreApplication.translate("STSession", "Unauthorized client! The server won't allow requests from this client.")
            self.logger.warning(__name__, msg)

        return status_OK, msg

    def logout(self):
        msg = ""
        logged_out = False
        if self.is_user_logged():
            QSettings().setValue(self.TOKEN_KEY, "")  # Unregister (logout) the user
            self.__logged_user = None
            logged_out = True
            self.login_status_changed.emit(False)
            self.logout_finished.emit()
            self.task_manager.unregister_tasks()
            msg = QCoreApplication.translate("STSession", "User was logged out successfully!")
        else:
            msg = QCoreApplication.translate("STSession", "There was not logged in user! Therefore, no logout.")

        self.logger.info(__name__, msg)
        return logged_out, msg

    def get_logged_st_user(self):
        return self.__logged_user

    def get_logged_role(self):
        return self.__logged_user.get_role() if self.__logged_user is not None else None

    def is_user_logged(self):
        return self.__logged_user is not None


class STLoggedUser:
    def __init__(self, name, e_mail, role, token):
        self.__user_name = name
        self.__user_e_mail = e_mail
        self.__user_role = role
        self.__token = token

    def get_name(self):
        return self.__user_name

    def get_e_mail(self):
        return self.__user_e_mail

    def get_role(self):
        return self.__user_role

    def get_token(self):
        # Should we make sure the TOKEN_KEY is stored? Apparently not. As we create and destroy the user as long as the
        # session is alive.
        return self.__token
