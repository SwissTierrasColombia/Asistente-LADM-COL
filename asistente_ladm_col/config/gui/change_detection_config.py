from qgis.PyQt.QtCore import (QCoreApplication,
                              Qt)

# Change detection
PARCEL_STATUS = '_PARCEL_STATUS_'
PARCEL_STATUS_DISPLAY = ''
CHANGE_DETECTION_NEW_PARCEL = QCoreApplication.translate("TranslatableConfigStrings", "New parcel") # alta
CHANGE_DETECTION_MISSING_PARCEL = QCoreApplication.translate("TranslatableConfigStrings", "Missing parcel") # Baja
CHANGE_DETECTION_PARCEL_CHANGED = QCoreApplication.translate("TranslatableConfigStrings", "Parcel changed")
CHANGE_DETECTION_PARCEL_ONLY_GEOMETRY_CHANGED = QCoreApplication.translate("TranslatableConfigStrings", "Only geometry changed")
CHANGE_DETECTION_PARCEL_REMAINS = QCoreApplication.translate("TranslatableConfigStrings", "OK")
CHANGE_DETECTION_SEVERAL_PARCELS = QCoreApplication.translate("TranslatableConfigStrings", "Several")
CHANGE_DETECTION_NULL_PARCEL = QCoreApplication.translate("TranslatableConfigStrings", "null")
STATUS_COLORS = {CHANGE_DETECTION_NEW_PARCEL: Qt.red,
                 CHANGE_DETECTION_MISSING_PARCEL: Qt.red,
                 CHANGE_DETECTION_PARCEL_CHANGED: Qt.red,
                 CHANGE_DETECTION_PARCEL_ONLY_GEOMETRY_CHANGED: Qt.red,
                 CHANGE_DETECTION_PARCEL_REMAINS: Qt.green,
                 CHANGE_DETECTION_SEVERAL_PARCELS: Qt.yellow,
                 CHANGE_DETECTION_NULL_PARCEL: Qt.yellow}
PLOT_GEOMETRY_KEY = 'GEOMETRY_PLOT'