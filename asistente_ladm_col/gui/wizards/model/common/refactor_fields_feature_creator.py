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


class RefactorFieldsFeatureCreator:
    def __init__(self, app, db):
        self.__app = app
        self.__db = db

    def create(self, selected_layer, editing_layer_name, field_mapping):
        res_etl_model = self.__app.core.show_etl_model(self.__db,
                                                       selected_layer,
                                                       editing_layer_name,
                                                       field_mapping=field_mapping)
        if res_etl_model:  # Features were added?
            self.__app.gui.redraw_all_layers()  # Redraw all layers to show imported data

            # If the result of the etl_model is successful and we used a stored recent mapping, we delete the
            # previous mapping used (we give preference to the latest used mapping)
            if field_mapping:
                self.__app.core.delete_old_field_mapping(field_mapping)

            self.__app.core.save_field_mapping(editing_layer_name)
