from qgis.core import QgsApplication
from qgis.PyQt.QtCore import QObject

from ..config.table_mapping_config import ID_FIELD

class LogicChecks(QObject):

    def __init__(self):
        QObject.__init__(self)
        self.log = QgsApplication.messageLog()

    def get_parcel_right_relationship_errors(self, db):
        parcels_no_right = db.get_parcels_with_no_right()
        parcels_repeated_domain_right = db.get_parcels_with_repeated_domain_right()
        return ([sublist[0] for sublist in parcels_no_right], [sublist[0] for sublist in parcels_repeated_domain_right])

    def get_duplicate_records_in_a_table(self, db, table, fields, id_field=ID_FIELD):
        duplicate_records = db.duplicate_records_in_a_table(table, fields)
        return [(sublist[0], sublist[1]) for sublist in duplicate_records]
