# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              -------------------
        begin                : 2020
        copyright            : (C) 2020 by Germán Carrillo (SwissTierras Colombia)
        email                : gcarrillo@linuxmail.org
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.core import QgsCoordinateReferenceSystem

from asistente_ladm_col.config.general_config import DEFAULT_SRS_CODE


ctm_12_crs = QgsCoordinateReferenceSystem(int(DEFAULT_SRS_CODE))


def get_ctm12_crs():
    return ctm_12_crs

def get_crs_authid(crs):
    """
    If EPSG is the auth, return the authid as is, but if not, we're likely
    using STC:38820, so use the QGIS INTERNAL auth to get the SRS right.

    :param crs: QgsCoordinateReferenceSystem object
    :return: str representing the authid
    """
    auth, code = crs.authid().split(":")
    return "{}:{}".format("INTERNAL" if auth != "EPSG" else auth, code)

def get_crs_from_auth_and_code(auth, code):
    """
    Get a CRS object from auth and code. If auth is not EPSG, we pass only
    code to QgsCoordinateReferenceSystem constructor as it is most likely
    CTM12 (38820).

    :param auth: SRS auth
    :param code: SRS code
    :return: QgsCoordinateReferenceSystem
    """
    crs_def = "{}:{}".format(auth, code) if auth == "EPSG" else int(code)
    return QgsCoordinateReferenceSystem(crs_def)