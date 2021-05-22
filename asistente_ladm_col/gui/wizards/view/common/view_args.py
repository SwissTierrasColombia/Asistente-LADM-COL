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
from asistente_ladm_col.gui.wizards.view.pages.features_selector_view import EnumFeatureSelectionType
from asistente_ladm_col.gui.wizards.view.common.view_enum import EnumOptionType


class OptionChangedArgs:
    def __init__(self, selected_type: EnumOptionType):
        self.selected_type = selected_type


class PickFeaturesSelectedArgs:
    def __init__(self, selected_type: EnumOptionType, feature_selection_type: EnumFeatureSelectionType):
        self.selected_type = selected_type
        self.feature_selection_type = feature_selection_type
