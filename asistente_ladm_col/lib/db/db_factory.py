"""
/***************************************************************************
                              Asistente LADM-COL
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

from asistente_ladm_col.config.gui.db_engine_gui_config import DBEngineGUIConfig


class DBFactory(ABC):
    """
    Abstract class
    """
    def __init__(self):
        self._engine = None

    def get_id(self):
        return self._engine

    def get_name(self):
        raise NotImplementedError

    def get_config_panel(self, parent):
        raise NotImplementedError

    def get_model_baker_db_ili_mode(self):
        raise NotImplementedError

    def get_db_connector(self, parameters=dict()):
        raise NotImplementedError

    def get_ladm_queries(self):
        raise NotImplementedError

    def set_ili2db_configuration_params(self, params, configuration):
        raise NotImplementedError

    def get_db_engine_actions(self):
        """
        Get the actions supported by a db engine.

        :return: List of actions implemented in the plugin for the DB engine.
        """
        return DBEngineGUIConfig().get_db_engine_actions(self._engine)  # Returns a default if cannot find the engine

    def save_parameters_conn(self, dict_conn, db_source):
        settings = QSettings()
        settings.setValue('Asistente-LADM-COL/db/{db_source}/db_connection_engine'.format(db_source=db_source), self._engine)

        for parameter, value in dict_conn.items():
                settings.setValue(
                    'Asistente-LADM-COL/db/{db_source}/{engine}/{parameter}'.format(db_source=db_source,
                                                                                   engine=self._engine,
                                                                                   parameter=parameter), value)

    def get_parameters_conn(self, db_source):
        dict_conn = dict()
        settings = QSettings()
        settings.beginGroup('Asistente-LADM-COL/db/{db_source}/{engine}/'.format(db_source=db_source, engine=self._engine))
        for key in settings.allKeys():
            dict_conn[key] = settings.value(key)

        settings.endGroup()
        return dict_conn
