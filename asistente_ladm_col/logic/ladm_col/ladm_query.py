from abc import ABC

from asistente_ladm_col.config.mapping_config import QueryNames


class LADMQuery(ABC):

    def __init__(self):
        super(LADMQuery, self).__init__()

    def get_igac_basic_info(self, db, **kwargs):
        raise NotImplementedError

    def get_igac_legal_info(self, db, **kwargs):
        raise NotImplementedError

    def get_igac_physical_info(self, db, **kwargs):
        raise NotImplementedError

    def get_igac_economic_info(self, db, **kwargs):
        raise NotImplementedError

    def get_igac_property_record_card_info(self, db, **kwargs):
        raise NotImplementedError

    @staticmethod
    def _get_parameters(kwargs):
        params = {
            QueryNames.SEARCH_KEY_PLOT_T_IDS: 'NULL',
            QueryNames.SEARCH_KEY_PARCEL_FMI: 'NULL',
            QueryNames.SEARCH_KEY_PARCEL_NUMBER: 'NULL',
            QueryNames.SEARCH_KEY_PREVIOUS_PARCEL_NUMBER: 'NULL'
        }

        params.update(kwargs)
        return params