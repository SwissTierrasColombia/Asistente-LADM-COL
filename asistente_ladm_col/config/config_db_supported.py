from qgis.PyQt.QtCore import QObject

from ..db_support.pg_admin import PgAdmin
from ..db_support.gpkg_admin import GpkgAdmin


class ConfigDbSupported(QObject):

    def __init__(self):
        self.id_default_db = None
        self._db_items = dict()
        self._init_db_items()

    def _init_db_items(self):
        db_item = PgAdmin()
        self._db_items[db_item.get_id()] = db_item
        self.id_default_db = db_item.get_id()

        db_item = GpkgAdmin()
        self._db_items[db_item.get_id()] = db_item

    def get_db_items(self):
        return self._db_items
