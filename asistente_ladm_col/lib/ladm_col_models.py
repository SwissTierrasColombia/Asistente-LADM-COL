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
from asistente_ladm_col.config.gui.common_keys import (ROLE_SUPPORTED_MODELS,
                                                       ROLE_HIDDEN_MODELS,
                                                       ROLE_CHECKED_MODELS)
from asistente_ladm_col.config.ladm_names import (MODEL_ALIAS,
                                                  MODEL_IS_SUPPORTED,
                                                  MODEL_SUPPORTED_VERSION,
                                                  MODEL_HIDDEN_BY_DEFAULT,
                                                  MODEL_CHECKED_BY_DEFAULT)
from asistente_ladm_col.gui.gui_builder.role_registry import RoleRegistry
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.utils.singleton import Singleton


class LADMColModelRegistry(metaclass=Singleton):
    def __init__(self):
        self.logger = Logger()
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

    def refresh_models_for_role(self):
        role_key = RoleRegistry().get_active_role()
        role_models = RoleRegistry().get_role_models(role_key)
        for model_key, model in self.__models.items():
            model.set_is_supported(model_key in role_models[ROLE_SUPPORTED_MODELS])
            model.set_is_hidden(model_key in role_models[ROLE_HIDDEN_MODELS])
            model.set_is_checked(model_key in role_models[ROLE_CHECKED_MODELS])

        self.logger.debug(__name__, "Supported models for role '{}': {}".format(role_key, role_models[ROLE_SUPPORTED_MODELS]))


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

    def set_is_supported(self, supported):
        self.__is_supported = supported

    def supported_version(self):
        # From this version on the plugin will work, a message will block prior versions
        return self.__supported_version

    def hidden(self):
        return self.__hidden_by_default

    def set_is_hidden(self, hidden):
        self.__hidden_by_default = hidden

    def checked(self):
        return self.__checked_by_default

    def set_is_checked(self, checked):
        self.__checked_by_default = checked