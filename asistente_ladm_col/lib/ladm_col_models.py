# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2020-07-06
        git sha              : :%H$
        copyright            : (C) 2020 by Germán Carrillo (SwissTierras Colombia)
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
from asistente_ladm_col.config.ladm_names import (MODEL_ALIAS,
                                                  MODEL_IS_SUPPORTED,
                                                  MODEL_SUPPORTED_VERSION,
                                                  MODEL_HIDDEN_BY_DEFAULT,
                                                  MODEL_CHECKED_BY_DEFAULT)
from asistente_ladm_col.utils.singleton import Singleton


class LADMColModelRegistry(metaclass=Singleton):
    def __init__(self):
        self.__models = dict()

    def register_model(self, model):
        if not isinstance(model, LADMColModel) or model.id() in self.__models:
            return False

        self.__models[model.id()] = model
        return True

    def supported_models(self):
        return [model for model in self.__models.values() if model.is_supported()]

    def hidden_models(self):
        return [model.full_name() for model in self.__models.values() if model.hidden()]

    def model(self, model_id):
        return self.__models.get(model_id, LADMColModel("foo", dict()))  # To avoid exceptions

    def model_ids(self):
        return list(self.__models.keys())


class LADMColModel:
    def __init__(self, model_id, model_data):
        self.__id = model_id
        self.__alias = model_data.get(MODEL_ALIAS, "")
        self.__is_supported = model_data.get(MODEL_IS_SUPPORTED, True)
        self.__supported_version = model_data.get(MODEL_SUPPORTED_VERSION, "")
        self.__hidden_by_default = model_data.get(MODEL_HIDDEN_BY_DEFAULT, False)
        self.__checked_by_default = model_data.get(MODEL_CHECKED_BY_DEFAULT, False)

    def id(self):
        return self.__id

    def full_name(self):
        return "{}_V{}".format(self.__id, self.__supported_version.replace(".", "_"))

    def alias(self):
        return self.__alias

    def full_alias(self):
        return "{} v{}".format(self.__alias, self.__supported_version)

    def is_supported(self):
        return self.__is_supported

    def supported_version(self):
        # From this version on the plugin will work, a message will block prior versions
        return self.__supported_version

    def hidden(self):
        return self.__hidden_by_default

    def checked(self):
        return self.__checked_by_default