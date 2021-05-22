# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2021-05-21
        git sha              : :%H$
        copyright            : (C) 2021 by Yesid Polanía (BFS Swissphoto)
        email                : yesidpol.3@gmail.com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
 """
from enum import Enum


class EnumOptionType(Enum):
    PLOT = 1
    BUILDING = 2
    BUILDING_UNIT = 3

    BOUNDARY = 4
    BOUNDARY_POINT = 5
    SURVEY_POINT = 6
    CONTROL_POINT = 7

    ADMINISTRATIVE_SOURCE = 8


class EnumLayerCreationMode(Enum):
    MANUALLY = 1,
    REFACTOR = 2,
    DIGITIZING_LINE = 3
