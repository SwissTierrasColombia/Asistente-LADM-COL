# -*- coding: utf-8 -*-
from qgis.core import QgsCoordinateReferenceSystem

from asistente_ladm_col.config.general_config import DEFAULT_SRS_AUTHID

ctm_12_crs = QgsCoordinateReferenceSystem()


def get_ctm12_crs():
    global ctm_12_crs
    if not ctm_12_crs.isValid():
        ctm_12_crs = QgsCoordinateReferenceSystem(DEFAULT_SRS_AUTHID)  # Initialize it
    return ctm_12_crs


def get_crs_authid(crs):
    """
    :param crs: QgsCoordinateReferenceSystem object
    :return: str representing the authid
    """
    return crs.authid()


def get_crs_from_auth_and_code(auth, code):
    """
    Get a CRS object from auth and code.

    :param auth: SRS auth
    :param code: SRS code
    :return: QgsCoordinateReferenceSystem
    """
    crs = QgsCoordinateReferenceSystem("{}:{}".format(auth, code))
    return crs if crs.isValid() else get_ctm12_crs()