# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-02-21
        git sha              : :%H$
        copyright            : (C) 2019 by Yesid Polanía (BSF Swissphoto)
        email                : yesidpol.3@gmail.com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""
from abc import ABC
from qgis.PyQt.QtCore import QSettings


class DbFactory(ABC):

    def __init__(self):
        self._mode = None

    def get_id(self):
        raise NotImplementedError

    def get_name(self):
        raise NotImplementedError

    def get_config_panel(self, parent):
        raise NotImplementedError

    def get_mbaker_db_ili_mode(self):
        raise NotImplementedError

    def get_db_connector(self, parameters={}):
        raise NotImplementedError

    def set_db_configuration_params(self, params, configuration):
        raise NotImplementedError

    def save_parameters_conn(self, dict_conn, db_source):
        settings = QSettings()
        for parameter, value in dict_conn.items():
                settings.setValue(
                    'Asistente-LADM_COL/db/{db_source}/{scope}/{parameter}'.format(db_source=db_source,
                                                                                   scope=self._mode,
                                                                                   parameter=parameter), value)

    def get_parameters_conn(self, db_source):
        dict_conn = dict()
        settings = QSettings()
        settings.beginGroup('Asistente-LADM_COL/db/{db_source}/{scope}/'.format(db_source=db_source, scope=self._mode))
        for key in settings.allKeys():
            dict_conn[key] = settings.value(key)

        settings.endGroup()
        return dict_conn
