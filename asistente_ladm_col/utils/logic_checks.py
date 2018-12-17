from qgis.core import QgsApplication
from qgis.PyQt.QtCore import QObject

class LogicChecks(QObject):

    def __init__(self):
        QObject.__init__(self)
        self.log = QgsApplication.messageLog()

    def get_parcel_right_relationship_errors(self, db):
        parcels_no_right = db.get_parcels_with_no_right()
        parcels_repeated_domain_right = db.get_parcels_with_repeated_domain_right()
        return ([sublist[0] for sublist in parcels_no_right], [sublist[0] for sublist in parcels_repeated_domain_right])

    def get_fractions_which_sum_is_not_one(self, db):
        incomplete_fractions = db.get_fractions_which_sum_is_not_one()
        print(incomplete_fractions)
        return [sublist for sublist in incomplete_fractions]
