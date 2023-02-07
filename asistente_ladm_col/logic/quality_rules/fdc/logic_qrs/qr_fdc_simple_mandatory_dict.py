from qgis.PyQt.QtCore import QCoreApplication

from asistente_ladm_col.config.quality_rule_config import (QR_FDCR4003,
                                                           QR_FDCR4004,
                                                           QR_FDCR4005,
                                                           QR_FDCR4006,
                                                           QR_FDCR4007,
                                                           QRE_FDCR4003E01,
                                                           QRE_FDCR4004E01,
                                                           QRE_FDCR4005E01,
                                                           QRE_FDCR4006E01,
                                                           QRE_FDCR4007E01)

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
    },
    QR_FDCR4005: {
        'id': QR_FDCR4005,
        'name': 'La fecha de la visita predial no debe ser nula',
        'tags': ['fdc', 'captura', 'campo', 'lógica', 'negocio', 'predio', 'fecha visita predial'],
        'error': {'code': QRE_FDCR4005E01, 'message': 'La fecha de la visita predial no debe ser nula'},
        'layer': 'FDC_PARCEL_T',
        'field': 'FDC_PARCEL_T_DATE_OF_PROPERTY_VISIT_F',
        'notification_messages': {
            'error': QCoreApplication.translate('QualityRules', '{} parcels with invalid parcel visit date were found.'),
            'ok': QCoreApplication.translate('QualityRules', 'All parcels have valid parcel visit date.')
        }
    },
    QR_FDCR4006: {
        'id': QR_FDCR4006,
        'name': 'El resultado de la visita al predio no debe ser nulo',
        'tags': ['fdc', 'captura', 'campo', 'lógica', 'negocio', 'predio', 'resultado visita predial'],
        'error': {'code': QRE_FDCR4006E01, 'message': 'El resultado de la visita al predio no debe ser nulo'},
        'layer': 'FDC_PARCEL_T',
        'field': 'FDC_PARCEL_T_VISIT_RESULT_F',
        'notification_messages': {
            'error': QCoreApplication.translate('QualityRules', '{} parcels with invalid visit result were found.'),
            'ok': QCoreApplication.translate('QualityRules', 'All parcels have valid visit result.')
        }
    },
    QR_FDCR4007: {
        'id': QR_FDCR4007,
        'name': 'El atributo tiene área registral del predio no debe ser nulo',
        'tags': ['fdc', 'captura', 'campo', 'lógica', 'negocio', 'predio', 'tiene area registral'],
        'error': {'code': QRE_FDCR4007E01, 'message': 'El atributo tiene área registral del predio no debe ser nulo'},
        'layer': 'FDC_PARCEL_T',
        'field': 'FDC_PARCEL_T_HAS_REGISTER_AREA_F',
        'notification_messages': {
            'error': QCoreApplication.translate('QualityRules', '{} parcels with invalid "has register area?" were found.'),
            'ok': QCoreApplication.translate('QualityRules', 'All parcels have valid "has register area?".')
        }
    }
}