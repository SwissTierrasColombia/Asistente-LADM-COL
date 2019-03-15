from .db_ladm_layer_tester import DbLadmLayerTester
from qgis.core import (QgsDataSourceUri)


class NoneLadmLayerTester(DbLadmLayerTester):

    def is_ladm_layer(self, layer, db):
        return False