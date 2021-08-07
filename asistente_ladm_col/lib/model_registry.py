"""
/***************************************************************************
                              Asistente LADM-COL
                             --------------------
        begin           : 2020-07-06
        git sha         : :%H$
        copyright       : (C) 2020 by Germán Carrillo (SwissTierras Colombia)
        email           : gcarrillo@linuxmail.org
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""
from copy import deepcopy

from asistente_ladm_col.config.gui.common_keys import (ROLE_SUPPORTED_MODELS,
                                                       ROLE_HIDDEN_MODELS,
                                                       ROLE_CHECKED_MODELS,
                                                       ROLE_MODEL_ILI2DB_PARAMETERS)
from asistente_ladm_col.config.model_config import (MODEL_ALIAS,
                                                    MODEL_IS_SUPPORTED,
                                                    MODEL_SUPPORTED_VERSION,
                                                    MODEL_HIDDEN_BY_DEFAULT,
                                                    MODEL_CHECKED_BY_DEFAULT,
                                                    MODEL_ILI2DB_PARAMETERS,
                                                    MODEL_MAPPING,
                                                    ModelConfig)
from asistente_ladm_col.gui.gui_builder.role_registry import RoleRegistry
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.utils.singleton import Singleton


class LADMColModelRegistry(metaclass=Singleton):
    """
    Registry of supported models.
    The model in the registry is updated each time the current role changes.
    """
    def __init__(self):
        self.logger = Logger()
        self.__models = dict()
        self.__model_config = ModelConfig()

        # Register default models
        for model_key, model_config in self.__model_config.get_models_config().items():
            self.register_model(LADMColModel(model_key, model_config))

    def register_model(self, model):
        if not isinstance(model, LADMColModel) or model.id() in self.__models:
            return False

        self.__models[model.id()] = model
        return True

    def supported_models(self):
        return [model for model in self.__models.values() if model.is_supported()]

    def supported_model_keys(self):
        return [model.id() for model in self.__models.values() if model.is_supported()]

    def model(self, model_key):
        return self.__models.get(model_key, LADMColModel("foo", dict()))  # To avoid exceptions

    def model_by_full_name(self, full_name):
        for model in self.__models.values():
            if model.full_name() == full_name:
                return model

        return LADMColModel("foo", dict())  # To avoid exceptions

    def model_keys(self):
        return list(self.__models.keys())

    def hidden_and_supported_models(self):
        return [model for model in self.__models.values() if model.hidden() and model.is_supported()]

    def non_hidden_and_supported_models(self):
        return [model for model in self.__models.values() if not model.hidden() and model.is_supported()]

    def refresh_models_for_role(self):
        role_key = RoleRegistry().get_active_role()
        role_models = RoleRegistry().get_role_models(role_key)

        # ili2db params may come from the model config itself or overwritten by the current user.
        # It the user does not have such config, we grab it from MODEL_CONFIG.
        ili2db_params = role_models.get(ROLE_MODEL_ILI2DB_PARAMETERS, dict())

        for model_key, model in self.__models.items():
            model.set_is_supported(model_key in role_models[ROLE_SUPPORTED_MODELS])
            model.set_is_hidden(model_key in role_models[ROLE_HIDDEN_MODELS])
            model.set_is_checked(model_key in role_models[ROLE_CHECKED_MODELS])

            if model_key in ili2db_params and ili2db_params[model_key]:
                model_ili2db_params = ili2db_params[model_key]
            else:
                model_ili2db_params = self.__model_config.get_default_ili2db_parameters(model_key)

            if model_ili2db_params:
                self.logger.debug(__name__, "Model ili2db params are: {}".format(model_ili2db_params))

            model.set_ili2db_params(model_ili2db_params)

        self.logger.debug(__name__, "Supported models for role '{}': {}".format(role_key, role_models[ROLE_SUPPORTED_MODELS]))

    def get_model_mapping(self, model_key):
        return self.model(model_key).get_mapping()


class LADMColModel:
    def __init__(self, model_id, model_data):
        self.__id = model_id
        self.__alias = model_data.get(MODEL_ALIAS, "")
        self.__is_supported = model_data.get(MODEL_IS_SUPPORTED, True)
        self.__supported_version = model_data.get(MODEL_SUPPORTED_VERSION, "")
        self.__hidden_by_default = model_data.get(MODEL_HIDDEN_BY_DEFAULT, False)
        self.__checked_by_default = model_data.get(MODEL_CHECKED_BY_DEFAULT, False)
        self.__ili2db_parameters = model_data.get(MODEL_ILI2DB_PARAMETERS, dict())
        self.__mapping = model_data.get(MODEL_MAPPING, dict())

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

    def get_ili2db_params(self):
        return self.__ili2db_parameters.copy()

    def set_ili2db_params(self, parameters):
        self.__ili2db_parameters = parameters

    def get_mapping(self):
        return deepcopy(self.__mapping)
