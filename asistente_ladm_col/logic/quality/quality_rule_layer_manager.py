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
from qgis.PyQt.QtCore import (QCoreApplication,
                              QObject)
from qgis.core import (QgsProject,
                       QgsWkbTypes)
import processing

from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.config.quality_rules_config import (QualityRuleConfig,
                                                            QUALITY_RULE_LAYERS,
                                                            QUALITY_RULE_ADJUSTED_LAYERS,
                                                            ADJUSTED_REFERENCE_LAYER,
                                                            ADJUSTED_INPUT_LAYER,
                                                            FIX_ADJUSTED_LAYER)
from asistente_ladm_col.lib.logger import Logger


class QualityRuleLayerManager(QObject):
    """
    Responsible for managing all layers during a Quality Rule execution
    session. It goes for LADM-COL layers only once and also manages
    intermediate layers (after snapping).
    """
    def __init__(self, db, rule_keys, tolerance):
        QObject.__init__(self)
        self.logger = Logger()
        self.app = AppInterface()

        self.__db = db
        self.__rule_keys = rule_keys
        self.__tolerance = tolerance

        self.__quality_rule_layers_config = QualityRuleConfig.get_quality_rules_layer_config(self.__db.names)
        self.__layers = dict()  # {rule_key: {layer_name: layer}
        self.__adjusted_layers_cache = dict()

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
            self.__adjusted_layers_cache = dict()  # adjusted_layers_key: layer
            for rule_key, rule_layers_config in self.__quality_rule_layers_config.items():
                if rule_key in self.__rule_keys:  # Only get selected rules' layers
                    if QUALITY_RULE_ADJUSTED_LAYERS in rule_layers_config:

                        for layer_name, snap_config in rule_layers_config[QUALITY_RULE_ADJUSTED_LAYERS].items():
                            input = snap_config[ADJUSTED_INPUT_LAYER]  # input layer name
                            reference = snap_config[ADJUSTED_REFERENCE_LAYER]  # reference layer name
                            fix = snap_config[FIX_ADJUSTED_LAYER] if FIX_ADJUSTED_LAYER in snap_config else False

                            adjusted_layers_key = "{}..{}{}".format(input, reference, '..fix' if fix else '')

                            # Try to reuse if already calculated!
                            if adjusted_layers_key not in self.__adjusted_layers_cache:
                                self.__adjusted_layers_cache[adjusted_layers_key] = self.__adjust_layers(ladm_layers[input],
                                                                                                  ladm_layers[reference],
                                                                                                  fix)

                            adjusted_layers[rule_key][layer_name] = self.__adjusted_layers_cache[adjusted_layers_key]

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

        # Register adjusted layers so that Processing can properly find them
        load_to_registry = [layer for key, layer in self.__adjusted_layers_cache.items()]
        self.logger.debug(__name__, "{} adjusted layers loaded to QGIS registry...".format(len(load_to_registry)))
        QgsProject.instance().addMapLayers(load_to_registry, False)

        return True

    def get_layer(self, layer_name, rule_key):
        return self.get_layers([layer_name], rule_key)

    def get_layers(self, rule_key):
        if not self.__layers:
            if not self.__prepare_layers():
                return None

        return self.__layers[rule_key]

    def __adjust_layers(self, input_layer, reference_layer, fix=False):
        # Single layer --> behavior 7
        # Different layers --> behavior 2, tolerance + 0.0001
        single_layer = input_layer == reference_layer
        if single_layer and input_layer.geometryType() == QgsWkbTypes.PointGeometry:
            behavior = 7  # It's a bit aggressive for polygons, for points works fine
            tolerance = self.__tolerance
        else:
            behavior = 2
            tolerance = self.__tolerance + 0.001  # Behavior 2 doesn't work with the exact tolerance

        tolerance /= 1000  # Tolerance comes in mm., we need it in m.

        params = {
            'INPUT': input_layer,
            'REFERENCE_LAYER': reference_layer,
            'TOLERANCE': tolerance,
            'BEHAVIOR': behavior,
            'OUTPUT': 'TEMPORARY_OUTPUT'
        }
        res = processing.run("qgis:snapgeometries", params)['OUTPUT']

        if fix:
            self.logger.debug(__name__, "Fixing adjusted layer ({}-->{})...".format(input_layer.name(), reference_layer.name()))
            params = {
                'INPUT': res,
                'OUTPUT': 'TEMPORARY_OUTPUT'}
            res = processing.run("native:fixgeometries", params)['OUTPUT']

        return res

    def clean_temporary_layers(self):
        # Removes adjusted layers from registry
        unload_from_registry = [layer.id() for key, layer in self.__adjusted_layers_cache.items()]
        self.logger.debug(__name__, "{} adjusted layers removed from QGIS registry...".format(len(unload_from_registry)))
        QgsProject.instance().removeMapLayers(unload_from_registry)
