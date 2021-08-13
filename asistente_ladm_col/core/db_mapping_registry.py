"""
/***************************************************************************
                              Asistente LADM-COL
                             --------------------
        begin           : 2020-07-27
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
import datetime
from asistente_ladm_col.config.keys.ili2db_keys import *
from asistente_ladm_col.config.query_names import QueryNames
from asistente_ladm_col.gui.gui_builder.role_registry import RoleRegistry
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.lib.model_registry import LADMColModelRegistry


class DBMappingRegistry:
    """
    Names are dynamic because different DB engines handle different names, and because even in a single DB engine,
    one could shorten table and field names via ili2db.

    Therefore, each DB connector has its own DBMappingRegistry.

    At any time, the DBMapping Registry has all table and field names that are both in the models the active user has
    access to and those which are present in the DB. That is, variable members in DBMapping Registry can be seen as the
    intersection of current active role model objects and current DB connection objects.
    """
    def __init__(self):
        self.id = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        self.logger = Logger()
        self._cached_domain_values = dict()  # Right cache: queries that actually return a domain value/code
        self._cached_wrong_domain_queries = {  # Wrong cache: queries that do not return anything from the domain
            QueryNames.VALUE_KEY: dict(),
            QueryNames.CODE_KEY: dict()
        }

        # To ease addition of new ili2db names (which must be done in several classes),
        # we keep them together in a dict {variable_name: variable_key}
        self.__ili2db_names = {
            "T_ID_F": T_ID_KEY,
            "T_ILI_TID_F": T_ILI_TID_KEY,
            "ILICODE_F": ILICODE_KEY,
            "DESCRIPTION_F": DESCRIPTION_KEY,
            "DISPLAY_NAME_F": DISPLAY_NAME_KEY,
            "T_BASKET_F": T_BASKET_KEY,
            "T_ILI2DB_BASKET_T": T_ILI2DB_BASKET_KEY,
            "T_ILI2DB_DATASET_T": T_ILI2DB_DATASET_KEY,
            "DATASET_T_DATASETNAME_F": DATASET_T_DATASETNAME_KEY,
            "BASKET_T_DATASET_F": BASKET_T_DATASET_KEY,
            "BASKET_T_TOPIC_F": BASKET_T_TOPIC_KEY,
            "BASKET_T_ATTACHMENT_KEY_F": BASKET_T_ATTACHMENT_KEY
        }

        # Main mapping dictionary:
        #     {table_key: {variable: 'table_variable_name', field_dict:{field_key: 'field_variable'}}}
        # It only gets mappings for models that are both, supported by the active rol, and present in the DB.
        # This dict is reset each time the active role changes.
        #
        # It's used to:
        #   1) Set variables that are present in both, the dict itself and the DB. Note: The dict doesn't change
        #      after it has been registered via register_db_mapping().
        #   2) Traverse the expected DB-model variables so that we can test they are set.
        self.__table_field_dict = dict()

    def __register_db_mapping(self, model_key, mapping):
        self.__table_field_dict[model_key] = mapping.copy()

    def __refresh_mapping_for_role(self, db_models):
        model_registry = LADMColModelRegistry()

        for model in model_registry.supported_models():
            if model.full_name() in db_models:
                self.__register_db_mapping(model.id(), model_registry.get_model_mapping(model.id()))

    def initialize_table_and_field_names(self, db_mapping, db_models):
        """
        Update class variables (table and field names) according to a dictionary of names coming from a DB connection.
        This function should be called when a new DB connection is established for making all classes in the plugin able
        to access current DB connection names.

        :param db_mapping: Expected dict with key as iliname (fully qualified object name in the model) with no version
                           info, and value as sqlname (produced by ili2db).
        :param db_models: Models present in the DB.

        :return: True if anything is updated, False otherwise.
        """
        self.__reset_table_and_field_names()  # We will start mapping from scratch, so reset any previous mapping
        self.__refresh_mapping_for_role(db_models)  # Now, for the active role, register the db mappings per allowed model

        any_update = False
        table_names_count = 0
        field_names_count = 0
        if db_mapping:
            for key in self.__ili2db_names.values():
                if key not in db_mapping:
                    self.logger.error(__name__, "dict_names is not properly built, this required field was not found: {}").format(key)
                    return False

            for model_key, registered_mapping in self.__table_field_dict.items():
                for table_key, attrs in registered_mapping.items():
                    if table_key in db_mapping:
                        setattr(self, attrs[QueryNames.VARIABLE_NAME], db_mapping[table_key][QueryNames.TABLE_NAME])
                        table_names_count += 1
                        any_update = True
                        for field_key, field_variable in attrs[QueryNames.FIELDS_DICT].items():
                            if field_key in db_mapping[table_key]:
                                setattr(self, field_variable, db_mapping[table_key][field_key])
                                field_names_count += 1

            # Required fields coming from ili2db (T_ID_F, T_ILI_TID, etc.)
            for k,v in self.__ili2db_names.items():
                setattr(self, k, db_mapping[v])

        self.logger.info(__name__, "Table and field names have been set!")
        self.logger.debug(__name__, "Number of table names set: {}".format(table_names_count))
        self.logger.debug(__name__, "Number of field names set: {}".format(field_names_count))
        self.logger.debug(__name__, "Number of common ili2db names set: {}".format(len(self.__ili2db_names)))

        return any_update

    def __reset_table_and_field_names(self):
        """
        Start __table_field_dict from scratch to prepare the next mapping.
        The other vars are set to None for the same reason.
        """
        self.__table_field_dict = dict()

        for k, v in self.__ili2db_names.items():
            setattr(self, k, None)

        # Clear cache
        self._cached_domain_values = dict()

        self.logger.info(__name__, "Names (DB mapping) have been reset to prepare the next mapping.")

    def test_names(self):
        """
        Test whether required table/field names are present. Required names are all those that are in the
        __table_field_dict variable (names of supported models by the active role and at the same time present in the
        DB) and the ones in ili2db_names variable.

        :return: Tuple bool: Names are valid or not, string: Message to indicate what exactly failed
        """
        # Get required names (registered names) from the __table_field_dict
        required_names = list()
        for model_key, registered_mapping in self.__table_field_dict.items():
            self.logger.debug(__name__, "Names to test in model '{}': {}".format(model_key, len(registered_mapping)))
            for k, v in registered_mapping.items():
                required_names.append(v[QueryNames.VARIABLE_NAME])
                for k1, v1 in v[QueryNames.FIELDS_DICT].items():
                    required_names.append(v1)

        required_names = list(set(required_names))  # Cause tables from base models might be registered by submodels
        required_ili2db_names = list(self.__ili2db_names.keys())
        count_required_names_before = len(required_names)
        required_names.extend(required_ili2db_names)
        self.logger.debug(__name__, "Testing names... Number of required names: {} ({} + {})".format(
            len(required_names),
            count_required_names_before,
            len(required_ili2db_names)
        ))

        names_not_found = list()
        for required_name in required_names:
            if getattr(self, required_name, None) is None:
                names_not_found.append(required_name)

        if names_not_found:
            self.logger.debug(__name__, "Variable names not properly set: {}".format(names_not_found))
            return False, "Name '{}' was not found!".format(names_not_found[0])

        return True, ""

    def cache_domain_value(self, domain_table, t_id, value, value_is_ilicode):
        key = "{}..{}".format('ilicode' if value_is_ilicode else 'dispname', value)

        if domain_table in self._cached_domain_values:
            self._cached_domain_values[domain_table][key] = t_id
        else:
            self._cached_domain_values[domain_table] = {key: t_id}

    def cache_wrong_query(self, query_type, domain_table, code, value, value_is_ilicode):
        """
        If query was by value, then use value in key and code in the corresponding value pair, and viceversa

        :param query_type: QueryNames.VALUE_KEY (search by value) or QueryNames.CODE_KEY (search by code)
        :param domain_table: name of the table being searched
        :param code: t_id
        :param value: iliCode or dispName value
        :param value_is_ilicode: whether the value to be searched is iliCode or not
        """
        key = "{}..{}".format('ilicode' if value_is_ilicode else 'dispname', value if query_type == QueryNames.VALUE_KEY else code)
        if domain_table in self._cached_wrong_domain_queries[query_type]:
            self._cached_wrong_domain_queries[query_type][domain_table][key] = code if query_type == QueryNames.VALUE_KEY else value
        else:
            self._cached_wrong_domain_queries[query_type][domain_table] = {key: code if query_type == QueryNames.VALUE_KEY else value}

    def get_domain_value(self, domain_table, t_id, value_is_ilicode):
        """
        Get a domain value from the cache. First, attempt to get it from the 'right' cache, then from the 'wrong' cache.

        :param domain_table: Domain table name.
        :param t_id: t_id to be searched.
        :param value_is_ilicode: Whether the value is iliCode (True) or dispName (False)
        :return: iliCode of the corresponding t_id.
        """
        # Search in 'right' cache
        field_name = 'ilicode' if value_is_ilicode else 'dispname'
        if domain_table in self._cached_domain_values:
            for k,v in self._cached_domain_values[domain_table].items():
                if v == t_id:
                    key = k.split("..")
                    if key[0] == field_name:
                        return True, key[1]  # Compound key: ilicode..value or dispname..value

        # Search in 'wrong' cache
        if domain_table in self._cached_wrong_domain_queries[QueryNames.CODE_KEY]:
            key = "{}..{}".format('ilicode' if value_is_ilicode else 'dispname', t_id)
            if key in self._cached_wrong_domain_queries[QueryNames.CODE_KEY][domain_table]:
                return True, self._cached_wrong_domain_queries[QueryNames.CODE_KEY][domain_table][key]

        return False, None

    def get_domain_code(self, domain_table, value, value_is_ilicode):
        """
        Get a domain code from the cache. First, attempt to get it from the 'right' cache, then from the 'wrong' cache.

        :param domain_table: Domain table name.
        :param value: value to be searched.
        :param value_is_ilicode: Whether the value is iliCode (True) or dispName (False)
        :return: tuple (found, t_id)
                        found: boolean, whether the value was found in cache or not
                        t_id: t_id of the corresponding ilicode
        """
        # Search in 'right' cache
        key = "{}..{}".format('ilicode' if value_is_ilicode else 'dispname', value)
        if domain_table in self._cached_domain_values:
            if key in self._cached_domain_values[domain_table]:
                return True, self._cached_domain_values[domain_table][key]

        # Search in 'wrong' cache
        if domain_table in self._cached_wrong_domain_queries[QueryNames.VALUE_KEY]:
            if key in self._cached_wrong_domain_queries[QueryNames.VALUE_KEY][domain_table]:
                return True, self._cached_wrong_domain_queries[QueryNames.VALUE_KEY][domain_table][key]

        return False, None
