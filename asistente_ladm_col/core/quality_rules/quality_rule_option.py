"""
/***************************************************************************
                              Asistente LADM-COL
                             --------------------
        begin           : 2022-01-11
        copyright       : (C) 2022 by Germán Carrillo (SwissTierras Colombia)
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

class QualityRuleOptions:
    def __init__(self, options):
        """
        Stores the options that a quality rule requires. An option can be mandatory or optional.

        :param options: List of QualityRuleOption objects
        """
        self.__dict_options = {o.id(): o for o in options}

        # Let's cache some useful data since the object is not supposed to change
        self.__num_options = len(self.__dict_options)
        self.__mandatory_option_list = [v for v in self.__dict_options.values() if v.is_mandatory()]
        self.__optional_option_list = [v for v in self.__dict_options.values() if not v.is_mandatory()]
        self.__num_mandatory_options = len(self.__mandatory_option_list)
        self.__num_optional_options = len(self.__optional_option_list)

    def get_options(self):
        # Note: You are not supposed to overwrite the options objects. We trust you :)
        return self.__dict_options

    def get_option_list(self):
        # Note: You are not supposed to overwrite the options objects. We trust you :)
        return list(self.__dict_options.values())

    def get_num_options(self):
        return self.__num_options

    def get_mandatory_option_list(self):
        return self.__mandatory_option_list

    def get_num_mandatory_options(self):
        return self.__num_mandatory_options

    def get_optional_option_list(self):
        return self.__optional_option_list

    def get_num_optional_options(self):
        return self.__num_optional_options


class QualityRuleOption:
    def __init__(self, id, title, description, is_mandatory, default_value=None):
        """
        Stores the data of a single quality rule option.
        """
        self.__id = id
        self.__title = title
        self.__description = description
        self.__is_mandatory = is_mandatory
        self.__default_value = default_value

    def id(self):
        return self.__id

    def title(self):
        return self.__title

    def description(self):
        return self.__description

    def is_mandatory(self):
        return self.__is_mandatory

    def default_value(self):
        return self.__default_value
