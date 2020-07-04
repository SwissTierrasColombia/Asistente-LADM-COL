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
DICT_KEY_PARTIES = "Interesados"

# Change Detections keys to compare
DICT_KEY_PARCEL_T_DEPARTMENT_F = "departamento"
DICT_KEY_PARCEL_T_FMI_F = "matricula_inmobiliaria"
DICT_KEY_PARCEL_T_PARCEL_NUMBER_F = "numero_predial"
DICT_KEY_PARCEL_T_CONDITION_F = "condicion_predio"
DICT_KEY_PARCEL_T_NAME_F = "nombre"

DICT_KEY_PARTY_T_DOCUMENT_TYPE_F = "tipo_documento"
DICT_KEY_PARTY_T_DOCUMENT_ID_F = "documento_identidad"
DICT_KEY_PARTY_T_NAME_F = "nombre"
DICT_KEY_PARTY_T_RIGHT = "derecho"

DICT_KEY_PLOT_T_AREA_F = "area_terreno"

DICT_ALIAS_KEYS_CHANGE_DETECTION = {
    DICT_KEY_PARCEL_T_DEPARTMENT_F: QCoreApplication.translate("TranslatableConfigStrings", "Parcel department"),
    DICT_KEY_PARCEL_T_FMI_F: QCoreApplication.translate("TranslatableConfigStrings", " Parcel FMI"),
    DICT_KEY_PARCEL_T_PARCEL_NUMBER_F: QCoreApplication.translate("TranslatableConfigStrings", "Parcel number"),
    DICT_KEY_PARCEL_T_CONDITION_F: QCoreApplication.translate("TranslatableConfigStrings", "Parcel condition"),
    DICT_KEY_PARCEL_T_NAME_F: QCoreApplication.translate("TranslatableConfigStrings", "Parcel name"),
    DICT_KEY_PARTY_T_DOCUMENT_TYPE_F: QCoreApplication.translate("TranslatableConfigStrings", "Document type"),
    DICT_KEY_PARTY_T_DOCUMENT_ID_F: QCoreApplication.translate("TranslatableConfigStrings", "Document ID"),
    DICT_KEY_PARTY_T_NAME_F: QCoreApplication.translate("TranslatableConfigStrings", "Party Name"),
    DICT_KEY_PARTY_T_RIGHT: QCoreApplication.translate("TranslatableConfigStrings", "Right"),
    DICT_KEY_PLOT_T_AREA_F: QCoreApplication.translate("TranslatableConfigStrings", "Plot area"),
    DICT_KEY_PARTIES: QCoreApplication.translate("TranslatableConfigStrings", "Parties")
}


# Search criteria
PARCEL_NUMBER_SEARCH_KEY = "Parcel Number"
PREVIOUS_PARCEL_NUMBER_SEARCH_KEY = "Previous Parcel Number"
FMI_PARCEL_SEARCH_KEY = "Folio de Matrícula Inmobiliaria"


def get_supplies_search_options(names):
    return {
        PARCEL_NUMBER_SEARCH_KEY: names.GC_PARCEL_T_PARCEL_NUMBER_F,
        PREVIOUS_PARCEL_NUMBER_SEARCH_KEY: names.GC_PARCEL_T_PARCEL_NUMBER_BEFORE_F,
        FMI_PARCEL_SEARCH_KEY: names.GC_PARCEL_T_FMI_F
    }


def get_collected_search_options(names):
    return {
        PARCEL_NUMBER_SEARCH_KEY: names.LC_PARCEL_T_PARCEL_NUMBER_F,
        PREVIOUS_PARCEL_NUMBER_SEARCH_KEY: names.LC_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F,
        FMI_PARCEL_SEARCH_KEY: names.LC_PARCEL_T_FMI_F
    }