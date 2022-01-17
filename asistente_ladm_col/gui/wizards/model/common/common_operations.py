# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-09-10
        git sha              : :%H$
        copyright            : (C) 2019 by Leo Cardona (BFS Swissphoto)
                               (C) 2021 by Yesid Polanía (BFS Swissphoto)
        email                : leo.cardona.p@gmail.com
                               yesidpol.3@gmail.com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
 """
from asistente_ladm_col.app_interface import AppInterface


class ModelCommonOperations:

    def __init__(self, layers, editing_layer_name, read_only_fields: list):
        self.__layers = layers
        self.__EDITING_LAYER_NAME = editing_layer_name
        self.__app = AppInterface()
        self.__read_only_fields = read_only_fields

    # (absWizardFactory)
    def set_read_only_fields(self, read_only=True):
        if self.__layers[self.__EDITING_LAYER_NAME] is None:
            return

        for field in self.__read_only_fields:
            # Not validate field that are read only
            self.__app.core.set_read_only_field(self.__layers[self.__EDITING_LAYER_NAME], field, read_only)

    # absWizardFactory
    def rollback_in_layers_with_empty_editing_buffer(self):
        for layer_name in self.__layers:
            if self.__layers[layer_name] is None:  # If the layer was removed, this becomes None
                continue

            if self.__layers[layer_name].isEditable() and not self.__layers[layer_name].editBuffer().isModified():
                self.__layers[layer_name].rollBack()

    def get_field_mappings_file_names(self):
        return self.__app.core.get_field_mappings_file_names(self.__EDITING_LAYER_NAME)
