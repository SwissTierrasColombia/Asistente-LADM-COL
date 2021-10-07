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

from asistente_ladm_col.config.keys.common import (ROLE_SUPPORTED_MODELS,
                                                   ROLE_HIDDEN_MODELS,
                                                   ROLE_CHECKED_MODELS,
                                                   ROLE_MODEL_ILI2DB_PARAMETERS,
                                                   MODEL_ALIAS,
                                                   MODEL_IS_SUPPORTED,
                                                   MODEL_SUPPORTED_VERSION,
                                                   MODEL_HIDDEN_BY_DEFAULT,
                                                   MODEL_CHECKED_BY_DEFAULT,
                                                   MODEL_ILI2DB_PARAMETERS,
                                                   MODEL_MAPPING,
                                                   MODEL_DIR,
                                                   MODEL_BASKET_INFO,
                                                   MODEL_BASKET_TOPIC_NAME,
                                                   MODEL_BASKET_TOPIC_NAME_PREFERRED)
from asistente_ladm_col.config.model_config import ModelConfig
from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.gui.gui_builder.role_registry import RoleRegistry
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.utils.singleton import Singleton


class LADMColModelRegistry(metaclass=Singleton):
    """
    Registry of supported models.

    The following info of registered models is updated each time the current role changes:
        is_supported, hidden, checked and get_ili2db_params.
    """
    def __init__(self):
        self.logger = Logger()
        self.app = AppInterface()
        self.__models = dict()  # {model_key1: LADMColModel1, ...}
        self.__model_config = ModelConfig()

        # Register default models
        for model_key, model_config in self.__model_config.get_models_config().items():
            self.register_model(LADMColModel(model_key, model_config), False)

    def register_model(self, model, refresh_model_for_active_role=True):
        """
        Registers an INTERLIS model to be accessible for registered roles.

        :param model: LADMColModel instance.
        :return: True if the model was registered, False otherwise.
        """
        if not isinstance(model, LADMColModel) or model.id() in self.__models:
            return False

        self.__models[model.id()] = model
        self.logger.info(__name__, "Model '{}' has been registered!".format(model.id()))

        if model.model_dir():
            self.app.settings.add_custom_model_dir(model.model_dir())
            self.logger.info(__name__, "Model dir '{}' has been registered!".format(model.model_dir()))

        # Finally, update model.is_supported() data according to the active role.
        #
        # Note we don't want to call this while initializing the plugin,
        # as it calls back and forth registered_roles and registered_models,
        # or, in other words, it requires to have both models and roles
        # registered before calling the method (or we end up with max recursion).
        if refresh_model_for_active_role:
            self.refresh_models_for_active_role(model.id())

        return True

    def unregister_model(self, model_key, unregister_model_dir=False):
        """
        Unregisters an INTERLIS model.

        :param model_key: Id of the model to unregister.
        :param unregister_model_dir: If True, we'll search the paths associated to the model_key. If any path is found,
                                     it will be removed, so we won't search for models in that path anymore. This is
                                     False by default because it might affect other registered models, so only set it
                                     as True if removing such path won't affect discovering other models.
        :return: True if the model was unregistered, False otherwise.
        """
        if model_key not in self.__models:
            self.logger.error(__name__, "Model '{}' was not found in registered models, therefore, it cannot be unregistered!".format(model_key))
            return False

        if unregister_model_dir:
            model_dir = self.__models[model_key].model_dir()
            if model_dir:
                self.app.settings.remove_custom_model_dir(model_dir)
                self.logger.info(__name__, "Model dir '{}' has been unregistered!".format(model_dir))

        self.__models[model_key] = None
        del self.__models[model_key]
        self.logger.info(__name__, "Model '{}' has been unregistered!".format(model_key))

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

    def refresh_models_for_active_role(self, only_for_model=''):
        role_key = RoleRegistry().get_active_role()
        role_models = RoleRegistry().get_role_models(role_key)

        # ili2db params may come from the model config itself or overwritten by the current user.
        # If the user does not have such config, we grab it from MODEL_CONFIG.
        ili2db_params = role_models.get(ROLE_MODEL_ILI2DB_PARAMETERS, dict())

        for model_key, model in self.__models.items():
            if only_for_model and model_key != only_for_model:
                continue  # Avoid overwriting data of the other models (useful for refreshing a just-registered model)

            model.set_is_supported(model_key in role_models[ROLE_SUPPORTED_MODELS])
            model.set_is_hidden(model_key in role_models[ROLE_HIDDEN_MODELS])
            model.set_is_checked(model_key in role_models[ROLE_CHECKED_MODELS])

            # First attempt to get ili2db parameters from role, otherwise from model config
            model_ili2db_params = ili2db_params.get(model_key, dict()) or model.get_default_ili2db_params()
            model.set_ili2db_params(model_ili2db_params)
            if model_ili2db_params:
                self.logger.debug(__name__, "Model ili2db params are: {}".format(model_ili2db_params))

        self.logger.debug(__name__, "Supported models for active role '{}': {}".format(role_key, role_models[ROLE_SUPPORTED_MODELS]))

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
        self.__mapping = model_data.get(MODEL_MAPPING, dict())

        self.__default_ili2db_parameters = model_data.get(MODEL_ILI2DB_PARAMETERS, dict())
        self.__ili2db_parameters = deepcopy(self.__default_ili2db_parameters)  # Default params shouldn't be modified

        # String with paths where to find the model. If several paths are needed, they must be
        # separated by a semicolon ";". Paths will be passed to ili2db, so any path ili2db understands
        # will work (see https://github.com/claeis/ili2db/blob/master/docs/ili2db.rst).
        self.__model_dir = model_data.get(MODEL_DIR, "")  # Only expected if the model comes from an Add-on

        # Information about baskets for this model, if needed
        self.__basket_info = model_data.get(MODEL_BASKET_INFO, dict())

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

    def get_default_ili2db_params(self):
        # Come from the model config itself and won't be modified
        return deepcopy(self.__default_ili2db_parameters)

    def get_ili2db_params(self):
        return deepcopy(self.__ili2db_parameters)

    def set_ili2db_params(self, parameters):
        self.__ili2db_parameters = parameters

    def get_mapping(self):
        return deepcopy(self.__mapping)

    def model_dir(self):
        return self.__model_dir

    def has_basket_info(self):
        return bool(self.__basket_info)

    def basket_topic_name(self):
        return self.__basket_info.get(MODEL_BASKET_TOPIC_NAME, '')

    def is_basket_topic_name_preferred(self):
        return self.__basket_info.get(MODEL_BASKET_TOPIC_NAME_PREFERRED, False)
