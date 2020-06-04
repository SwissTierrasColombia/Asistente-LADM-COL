# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2020-06-01
        copyright            : (C) 2020 by Germán Carrillo (SwissTierras Colombia)
        email                : gcarrillo@linuxmail.org
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""
import json
import requests
from qgis.PyQt.QtCore import (QCoreApplication,
                              Qt,
                              QObject,
                              pyqtSignal)

import processing

from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.config.quality_rules_config import (QualityRuleConfig,
                                                            QUALITY_RULE_LAYERS,
                                                            QUALITY_RULE_ADJUSTED_LAYERS,
                                                            ADJUSTED_REFERENCE_LAYER,
                                                            ADJUSTED_INPUT_LAYER)
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.lib.transitional_system.task_manager.task import STTask
from asistente_ladm_col.utils.decorators import _with_override_cursor


class QualityRuleLayerManager(QObject):
    """
    Responsible for managing all layers during a Quality Rule execution
    session. It goes for LADM-COL layers only once and also manages
    intermediate layers (after snapping).
    """
    def __init__(self, db, rule_keys):
        QObject.__init__(self)
        self.logger = Logger()
        self.app = AppInterface()

        self.__db = db
        self.__rule_keys = rule_keys

        self.__quality_rule_layers_config = QualityRuleConfig.get_quality_rules_layer_config(self.__db.names)
        self.__layers = dict()  # {rule_key: {layer_name: layer}

        self.__tolerance = 10  # TODO: read from settings

    def initialize(self, rule_keys):
        """
        Objects of this class are reusable calling initialize()
        """
        self.__rule_keys = rule_keys
        self.__layers = dict()

    def __prepare_layers(self):
        """
        Get layers from DB and prepare snapped layers for all rules
        """
        self.logger.info(__name__, QCoreApplication.translate("QualityRuleLayerManager", "Preparing layers..."))
        # First go for ladm-col layers
        ladm_layers = dict()
        for rule_key, rule_layers_config in self.__quality_rule_layers_config.items():
            if rule_key in self.__rule_keys:  # Only get selected rules' layers
                for layer_name in rule_layers_config[QUALITY_RULE_LAYERS]:
                    ladm_layers[layer_name] = None

        self.logger.debug(__name__, QCoreApplication.translate("QualityRuleLayerManager", "Getting {} LADM-COL layers...").format(len(ladm_layers)))
        self.app.core.get_layers(self.__db, ladm_layers, load=True)
        if not ladm_layers:
            return False

        # If tolerance > 0, prepare adjusted layers
        #   We create an adjusted_layers dict to override ladm_layers per rule.
        #   For that, we need to read the config and, if not yet calculated,
        #   adjust the layers and store them in temporary cache.

        # {rule_key: {layer_name: layer}}, because each rule might need
        # different adjustments for the same layer, compared to other rules
        adjusted_layers = {rule_key:dict() for rule_key in self.__rule_keys}

        if self.__tolerance:
            self.logger.debug(__name__, QCoreApplication.translate("QualityRuleLayerManager", "Tolerance > 0, adjusting layers..."))
            adjusted_layers_cache = {}  # adjusted_layers_key: layer
            for rule_key, rule_layers_config in self.__quality_rule_layers_config.items():
                if rule_key in self.__rule_keys:  # Only get selected rules' layers
                    if QUALITY_RULE_ADJUSTED_LAYERS in rule_layers_config:

                        for layer_name, snap_config in rule_layers_config[QUALITY_RULE_ADJUSTED_LAYERS].items():
                            input = snap_config[ADJUSTED_INPUT_LAYER]  # input layer name
                            reference = snap_config[ADJUSTED_REFERENCE_LAYER]  # reference layer name
                            adjusted_layers_key = "{}..{}".format(input, reference)

                            # Try to reuse if already calculated!
                            if adjusted_layers_key not in adjusted_layers_cache:
                                adjusted_layers_cache[adjusted_layers_key] = self.__adjust_layers(ladm_layers[input],
                                                                                                  ladm_layers[reference])

                            adjusted_layers[rule_key][layer_name] = adjusted_layers_cache[adjusted_layers_key]

        self.logger.debug(__name__, QCoreApplication.translate("QualityRuleLayerManager", "Layers adjusted..."))

        # Now that we have both ladm_layers and adjusted_layers, join them
        # in a single member dict of layers per rule, preferring adjusted layers
        self.__layers = {rule_key:dict() for rule_key in self.__rule_keys}
        for rule_key, rule_layers_config in self.__quality_rule_layers_config.items():
            if rule_key in self.__rule_keys:  # Only get selected rules' layers
                for layer_name in rule_layers_config[QUALITY_RULE_LAYERS]:
                    if layer_name in adjusted_layers[rule_key]:
                        self.__layers[rule_key][layer_name] = adjusted_layers[rule_key][layer_name]
                    elif layer_name in ladm_layers:
                        self.__layers[rule_key][layer_name] = ladm_layers[layer_name]

        return True

    def get_layer(self, layer_name, rule_key):
        return self.get_layers([layer_name], rule_key)

    def get_layers(self, rule_key):
        if not self.__layers:
            if not self.__prepare_layers():
                return None

        return self.__layers[rule_key]

    def __adjust_layers(self, input_layer, reference_layer):
        # Single layer --> behavior 7
        # Different layers --> behavior 2, tolerance + 0.0001
        single_layer = input_layer == reference_layer
        behavior = 7 if single_layer else 2
        tolerance = self.__tolerance if single_layer else self.__tolerance + 0.00001

        params = {
            'INPUT': input_layer,
            'REFERENCE_LAYER': reference_layer,
            'TOLERANCE': tolerance,
            'BEHAVIOR': behavior,
            'OUTPUT': 'TEMPORARY_OUTPUT'
        }
        res = processing.run("qgis:snapgeometries", params)
        return res['OUTPUT']