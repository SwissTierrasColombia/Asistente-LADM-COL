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
from asistente_ladm_col.config.enums import EnumFeatureCreationMode


class CreateFeatureArgs:

    def __init__(self, layer_creation_mode: EnumFeatureCreationMode):
        self.layer_creation_mode = layer_creation_mode
