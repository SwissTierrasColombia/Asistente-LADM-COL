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
import json
from qgis.PyQt.QtCore import (QObject,
                              QCoreApplication,
                              QSettings)

from asistente_ladm_col.utils.singleton import SingletonQObject

class STSession(QObject, metaclass=SingletonQObject):
    TOKEN_KEY = "Asistente-LADM_COL/transition_system/token"

    def __init__(self):
        QObject.__init__(self)
        self.__logged_user = None

    def login(self, user, password):
        url = "http://192.168.98.61:8090/api/security/oauth/token"

        payload = "username={}&password={}&grant_type=password".format(user, password)
        headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'Authorization': "Basic c3Qtd2ViLWRldmVsb3AtaUxmdm9uU2g6MTIzNDU=",  # TODO
            'Accept': "*/*",
            'Cache-Control': "no-cache",
            'Accept-Encoding': "gzip, deflate",
            'Connection': "keep-alive",
            'cache-control': "no-cache"
        }
        response = requests.request("POST", url, data=payload, headers=headers)

        status_OK = response.status_code == 200
        if status_OK:
            logged_data = json.loads(response.text)
            self.__logged_user = STLoggedUser("{} {}".format(logged_data['first_name'], logged_data['last_name']), logged_data['email'], logged_data['roles'][0]['name'])
            QSettings().setValue(self.TOKEN_KEY, logged_data['access_token'])

        return status_OK

    def logout(self):
        if self.is_user_logged():
            self.__logged_user = None
            QSettings().setValue(self.TOKEN_KEY, '')
            return True

        return False

    def get_logged_st_user(self):
        return self.__logged_user

    def get_logged_role(self):
        return self.__logged_user.get_role() if self.__logged_user is not None else None

    def is_user_logged(self):
        return bool(QSettings().value(self.TOKEN_KEY, ''))


class STLoggedUser:
    def __init__(self, name, e_mail, role):
        self.__user_name = name
        self.__user_e_mail = e_mail
        self.__user_role = role

    def get_name(self):
        return self.__user_name

    def get_e_mail(self):
        return self.__user_e_mail

    def get_role(self):
        return self.__user_role
