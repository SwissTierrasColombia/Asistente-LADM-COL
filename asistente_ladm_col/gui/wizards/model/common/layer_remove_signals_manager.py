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
from functools import partial


class LayerRemovedSignalsManager:

    def __init__(self, layers: dict, layer_removed_behavior):
        self.__layers = layers
        self.__connected_function_list = []
        self.__layer_removed_behavior = layer_removed_behavior

    # MapInteractionExpansion / SelectFeaturesOnMapWrapper
    def connect_signals(self):
        for layer_name in self.__layers:
            if not self.__layers[layer_name]:
                continue
            connected_function = partial(self.__layer_removed, layer_name)
            self.__connected_function_list.append(connected_function)
            self.__layers[layer_name].willBeDeleted.connect(connected_function)

    def disconnect_signals(self):
        disconnected_functions = []

        for layer_name in self.__connected_function_list:
            if not self.__layers[layer_name]:
                continue
            # Layer was found, listen to its removal so that we can update the variable properly
            try:
                self.__layers[layer_name].willBeDeleted.disconnect(self.__connected_function_list)
                disconnected_functions.append(layer_name)

            except RuntimeError as err:
                if len(err.args) > 0 and err.args[0] == "wrapped C/C++ object of type QgsVectorLayer has been deleted":
                    self.__layers[layer_name] = None
                else:
                    raise err
            except TypeError as err:
                # TODO Workaround?
                if len(err.args) > 0 and err.args[0] == "disconnect() failed between 'willBeDeleted' and all its connections":
                    pass
                else:
                    raise err

        for layer_name in disconnected_functions:
            self.__connected_function_list.pop(layer_name)

    def reconnect_signals(self):
        self.disconnect_signals()
        self.connect_signals()

    def __layer_removed(self, layer_name):
        # assigned None to layer because wrapper object will be deleted but
        # python object will keep pointing to the deleted layer
        self.__layers[layer_name] = None
        if self.__layer_removed_behavior:
            self.__layer_removed_behavior.layer_removed()
