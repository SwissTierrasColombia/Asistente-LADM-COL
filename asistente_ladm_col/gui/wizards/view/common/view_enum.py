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

    @staticmethod
    def enum_value_from_db_name(db_names, item_db_name):
        dict_result = {
            db_names.LC_PLOT_T: EnumOptionType.PLOT,
            db_names.LC_BUILDING_T: EnumOptionType.BUILDING,
            db_names.LC_BUILDING_UNIT_T: EnumOptionType.BUILDING_UNIT,
            db_names.LC_BOUNDARY_T: EnumOptionType.BOUNDARY,
            db_names.LC_BOUNDARY_POINT_T: EnumOptionType.BOUNDARY_POINT,
            db_names.LC_SURVEY_POINT_T: EnumOptionType.SURVEY_POINT,
            db_names.LC_CONTROL_POINT_T: EnumOptionType.CONTROL_POINT,
            db_names.LC_ADMINISTRATIVE_SOURCE_T: EnumOptionType.ADMINISTRATIVE_SOURCE
        }
        return dict_result[item_db_name] if item_db_name in dict_result else None

    def get_db_name(self, db_names):
        dict_result = {
            EnumOptionType.PLOT: db_names.LC_PLOT_T,
            EnumOptionType.BUILDING: db_names.LC_BUILDING_T,
            EnumOptionType.BUILDING_UNIT: db_names.LC_BUILDING_UNIT_T,
            EnumOptionType.BOUNDARY: db_names.LC_BOUNDARY_T,
            EnumOptionType.BOUNDARY_POINT: db_names.LC_BOUNDARY_POINT_T,
            EnumOptionType.SURVEY_POINT: db_names.LC_SURVEY_POINT_T,
            EnumOptionType.CONTROL_POINT: db_names.LC_CONTROL_POINT_T,
            EnumOptionType.ADMINISTRATIVE_SOURCE: db_names.LC_ADMINISTRATIVE_SOURCE_T
        }

        return dict_result[self]


class EnumLayerCreationMode(Enum):
    MANUALLY = 1,
    REFACTOR = 2,
    DIGITIZING_LINE = 3
