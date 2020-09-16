from asistente_ladm_col.utils.singleton import Singleton


class ILI2DBNames(metaclass=Singleton):
    """
    Singleton to access common ili2db names (tables, parameters, etc.)

    Note: This is differente from ili2db_keys.py, which stores vars whose content does not really matter to us.
    """
    TABLE_PROP_ASSOCIATION = "ASSOCIATION"
    TABLE_PROP_DOMAIN = "ENUM"
    TABLE_PROP_STRUCTURE = "STRUCTURE"

    # Default settings to create schema according to LADM-COL
    DEFAULT_INHERITANCE = 'smart2'
    CREATE_BASKET_COL = False
    CREATE_IMPORT_TID = False
    STROKE_ARCS = True

    # For testing if an schema comes from ili2db
    INTERLIS_TEST_METADATA_TABLE_PG = 't_ili2db_table_prop'

    # TAG-SETTING pair to loog for basket col support in t_ili2db_settings
    BASKET_COL_TAG = 'ch.ehi.ili2db.BasketHandling'
    BASKET_COL_VALUE = 'readWrite'
