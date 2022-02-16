"""
/***************************************************************************
                              Asistente LADM-COL
                             --------------------
        begin           : 2021-10-26
        git sha         : :%H$
        copyright       : (C) 2021 by Germán Carrillo (SwissTierras Colombia)
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
from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.core.xtf_model_converter.abstract_ladm_col_model_converter import AbstractLADMColModelConverter
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.logic.xtf_model_converter.lev_cat_1_0_to_1_1_converter import Survey10To11Converter
from asistente_ladm_col.logic.xtf_model_converter.lev_cat_1_1_to_1_0_converter import Survey11To10Converter
from asistente_ladm_col.utils.singleton import Singleton


class XTFModelConverterRegistry(metaclass=Singleton):
    """
    Registry of supported model converters.
    """
    def __init__(self):
        self.logger = Logger()
        self.app = AppInterface()
        self.__converters = dict()  # {converter_key1: LADMColModelConverter1, ...}

        # Register default models
        self.register_model_converter(Survey10To11Converter())
        self.register_model_converter(Survey11To10Converter())

    def register_model_converter(self, converter):
        """
        :param converter: LADMColModelConverter instance.
        :return: True if the converter was registered, False otherwise.
        """
        if not isinstance(converter, AbstractLADMColModelConverter):
            self.logger.warning(__name__, "The converter '{}' is not a 'LADMColModelConverter' instance!".format(converter.id()))
            return False

        if not converter.is_valid():
            self.logger.warning(__name__, "The converter '{}' is not valid! Check the converter definition!".format(converter.id()))
            return False

        if converter.id() in self.__converters:
            self.logger.warning(__name__, "The converter '{}' is already registered.".format(converter.id()))
            return False

        self.__converters[converter.id()] = converter
        self.logger.info(__name__, "Model converter '{}' has been registered!".format(converter.id()))

        return True

    def unregister_model_converter(self, converter_key):
        """
        Unregisters a model converter.

        :param converter_key: Id of the converter to unregister.
        :return: True if the converter was unregistered, False otherwise.
        """
        if converter_key not in self.__converters:
            self.logger.error(__name__, "Converter '{}' was not found in registered model converters, therefore, it cannot be unregistered!".format(converter_key))
            return False

        self.__converters[converter_key] = None
        del self.__converters[converter_key]
        self.logger.info(__name__, "Model converter '{}' has been unregistered!".format(converter_key))

        return True

    def get_converter(self, converter_key):
        converter = self.__converters.get(converter_key, None)  # To avoid exceptions
        if not converter:
            self.logger.critical(__name__, "No model converter found with key '{}'".format(converter_key))

        return converter

    def get_converters_for_models(self, models):
        converters = dict()  # {converter_key_1: converter_display_name_1, ...]
        for converter_key, converter in self.__converters.items():
            for model in models:
                if converter.supports_source_model(model):
                    converters[converter_key] = converter.display_name()

        return converters
