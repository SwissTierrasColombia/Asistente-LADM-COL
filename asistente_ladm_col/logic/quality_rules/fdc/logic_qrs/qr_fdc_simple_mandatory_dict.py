from qgis.PyQt.QtCore import QCoreApplication

from asistente_ladm_col.config.quality_rule_config import (QR_FDCR4003,
                                                           QR_FDCR4004,
                                                           QRE_FDCR4003E01,
                                                           QRE_FDCR4004E01)

qr_simple_mandatory_dict = {
    QR_FDCR4003: {
        'id': QR_FDCR4003,
        'name': 'La clase de suelo del predio no debe ser nula',
        'tags': ['fdc', 'captura', 'campo', 'lógica', 'negocio', 'predio', 'clase suelo'],
        'error': {'code': QRE_FDCR4003E01, 'message': 'La clase de suelo del predio no debe ser nula'},
        'layer': 'FDC_PARCEL_T',
        'field': 'FDC_PARCEL_T_LAND_CLASS_F',
        'notification_messages': {
            'error': QCoreApplication.translate('QualityRules', '{} parcels with invalid land class were found.'),
            'ok': QCoreApplication.translate('QualityRules', 'All parcels have valid land class.')
        }
    },
    QR_FDCR4004: {
        'id': QR_FDCR4004,
        'name': 'La destinación económica del predio no debe ser nula',
        'tags': ['fdc', 'captura', 'campo', 'lógica', 'negocio', 'predio', 'destinación económica'],
        'error': {'code': QRE_FDCR4004E01, 'message': 'La destinación económica del predio no debe ser nula'},
        'layer': 'FDC_PARCEL_T',
        'field': 'FDC_ECONOMIC_DESTINATION_F',
        'notification_messages': {
            'error': QCoreApplication.translate('QualityRules', '{} parcels with invalid economic destination were found.'),
            'ok': QCoreApplication.translate('QualityRules', 'All parcels have valid economic destination.')
        }
    }
}