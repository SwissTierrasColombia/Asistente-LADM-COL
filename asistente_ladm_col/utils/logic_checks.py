from qgis.core import QgsApplication
from qgis.PyQt.QtCore import QObject

class LogicChecks(QObject):

    def __init__(self):
        QObject.__init__(self)
        self.log = QgsApplication.messageLog()

    def get_parcel_right_relationship_errors(self, db):
        parcels_no_right = db.get_parcels_with_no_right()
        return [sublist[0] for sublist in parcels_no_right]
