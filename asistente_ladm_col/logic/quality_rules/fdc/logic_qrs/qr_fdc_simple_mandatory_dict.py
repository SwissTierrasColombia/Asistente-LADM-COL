from qgis.PyQt.QtCore import QCoreApplication

from asistente_ladm_col.config.quality_rule_config import (QR_FDCR4003,
                                                           QR_FDCR4004,
                                                           QR_FDCR4005,
                                                           QR_FDCR4006,
                                                           QR_FDCR4007,
                                                           QR_FDCR4008,
                                                           QR_FDCR4009,
                                                           QR_FDCR4010,
                                                           QR_FDCR4011,
                                                           QR_FDCR4012,
                                                           QR_FDCR4013,
                                                           QR_FDCR4014,
                                                           QRE_FDCR4003E01,
                                                           QRE_FDCR4004E01,
                                                           QRE_FDCR4005E01,
                                                           QRE_FDCR4006E01,
                                                           QRE_FDCR4007E01,
                                                           QRE_FDCR4008E01,
                                                           QRE_FDCR4009E01,
                                                           QRE_FDCR4010E01,
                                                           QRE_FDCR4011E01,
                                                           QRE_FDCR4012E01,
                                                           QRE_FDCR4013E01,
                                                           QRE_FDCR4014E01)

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
    },
    QR_FDCR4008: {
        'id': QR_FDCR4008,
        'name': 'El atributo tiene FMI no debe ser nulo',
        'tags': ['fdc', 'captura', 'campo', 'lógica', 'negocio', 'predio', 'tiene fmi'],
        'error': {'code': QRE_FDCR4008E01, 'message': 'El atributo tiene FMI no debe ser nulo'},
        'layer': 'FDC_PARCEL_T',
        'field': 'FDC_PARCEL_T_HAS_FMI_F',
        'notification_messages': {
            'error': QCoreApplication.translate('QualityRules', '{} parcels with invalid "has FMI" were found.'),
            'ok': QCoreApplication.translate('QualityRules', 'All parcels have valid "has FMI".')
        }
    },
    QR_FDCR4009: {
        'id': QR_FDCR4009,
        'name': 'El tipo de documento de quien atendio la visita no debe ser nulo',
        'tags': ['fdc', 'captura', 'campo', 'lógica', 'negocio', 'predio', 'tipo documento quien atendio'],
        'error': {'code': QRE_FDCR4009E01, 'message': 'El tipo de documento de quien atendio la visita no debe ser nulo'},
        'layer': 'FDC_PARCEL_T',
        'field': 'FDC_PARCEL_T_DOCUMENT_TYPE_OF_WHO_ATTENDED_THE_VISIT_F',
        'notification_messages': {
            'error': QCoreApplication.translate('QualityRules', '{} parcels with invalid document type of who attended the visit were found.'),
            'ok': QCoreApplication.translate('QualityRules', 'All parcels have valid document type of who attended the visit.')
        }
    },
    QR_FDCR4010: {
        'id': QR_FDCR4010,
        'name': 'El número de documento de quien atendio la visita no debe ser nulo',
        'tags': ['fdc', 'captura', 'campo', 'lógica', 'negocio', 'predio', 'numero documento quien atendio'],
        'error': {'code': QRE_FDCR4010E01, 'message': 'El número de documento de quien atendio la visita no debe ser nulo'},
        'layer': 'FDC_PARCEL_T',
        'field': 'FDC_PARCEL_T_DOCUMENT_NUMBER_OF_WHO_ATTENDED_THE_VISIT_F',
        'notification_messages': {
            'error': QCoreApplication.translate('QualityRules', '{} parcels with invalid document number of who attended the visit were found.'),
            'ok': QCoreApplication.translate('QualityRules', 'All parcels have valid document number of who attended the visit.')
        }
    },
    QR_FDCR4011: {
        'id': QR_FDCR4011,
        'name': 'El nombre de quien atendio la visita no debe ser nulo',
        'tags': ['fdc', 'captura', 'campo', 'lógica', 'negocio', 'predio', 'nombre de quien atendio'],
        'error': {'code': QRE_FDCR4011E01, 'message': 'El nombre de quien atendio la visita no debe ser nulo'},
        'layer': 'FDC_PARCEL_T',
        'field': 'FDC_PARCEL_T_NAME_WHO_ATTENDED_THE_VISIT_F',
        'notification_messages': {
            'error': QCoreApplication.translate('QualityRules', '{} parcels with name who attended the visit were found.'),
            'ok': QCoreApplication.translate('QualityRules', 'All parcels have valid name who attended the visit.')
        }
    },
    QR_FDCR4012: {
        'id': QR_FDCR4012,
        'name': 'La fracción del derecho no debe ser nula',
        'tags': ['fdc', 'captura', 'campo', 'lógica', 'negocio', 'derecho', 'fraccion'],
        'error': {'code': QRE_FDCR4012E01, 'message': 'La fracción del derecho no debe ser nula'},
        'layer': 'FDC_RIGHT_T',
        'field': 'LC_RIGHT_T_RIGHT_FRACTION_F',
        'notification_messages': {
            'error': QCoreApplication.translate('QualityRules', '{} rights with invalid right fraction were found.'),
            'ok': QCoreApplication.translate('QualityRules', 'All rights have valid right fraction.')
        }
    },
    QR_FDCR4013: {
        'id': QR_FDCR4013,
        'name': 'El departamento de residencia del interesado no debe ser nulo',
        'tags': ['fdc', 'captura', 'campo', 'lógica', 'negocio', 'interesado', 'departamento'],
        'error': {'code': QRE_FDCR4013E01, 'message': 'El departamento de residencia del interesado no debe ser nulo'},
        'layer': 'FDC_PARTY_T',
        'field': 'FDC_PARTY_T_RESIDENCE_DEPARTMENT_F',
        'notification_messages': {
            'error': QCoreApplication.translate('QualityRules', '{} parties with invalid residence department were found.'),
            'ok': QCoreApplication.translate('QualityRules', 'All parties have valid residence department.')
        }
    },
    QR_FDCR4014: {
        'id': QR_FDCR4014,
        'name': 'El municipio de residencia del interesado no debe ser nulo',
        'tags': ['fdc', 'captura', 'campo', 'lógica', 'negocio', 'interesado', 'municipio'],
        'error': {'code': QRE_FDCR4014E01, 'message': 'El municipio de residencia del interesado no debe ser nulo'},
        'layer': 'FDC_PARTY_T',
        'field': 'FDC_PARTY_T_RESIDENCE_MUNICIPALITY_F',
        'notification_messages': {
            'error': QCoreApplication.translate('QualityRules', '{} parties with invalid residence municipality were found.'),
            'ok': QCoreApplication.translate('QualityRules', 'All parties have valid residence municipality.')
        }
    }
}