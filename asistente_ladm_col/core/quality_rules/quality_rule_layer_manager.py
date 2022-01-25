"""
/***************************************************************************
                              Asistente LADM-COL
                             --------------------
        begin          : 2020-06-01
        copyright      : (C) 2020 by Germán Carrillo (SwissTierras Colombia)
        email          : gcarrillo@linuxmail.org
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
                              QObject,
                              pyqtSignal)
from qgis.core import QgsProject

from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.config.keys.common import (QUALITY_RULE_LADM_COL_LAYERS,
                                                   QUALITY_RULE_ADJUSTED_LAYERS,
                                                   ADJUSTED_INPUT_LAYER,
                                                   ADJUSTED_REFERENCE_LAYER,
                                                   ADJUSTED_BEHAVIOR,
                                                   FIX_ADJUSTED_LAYER,
                                                   ADJUSTED_TOPOLOGICAL_POINTS,
                                                   QUALITY_RULE_LAYERS,
                                                   HAS_ADJUSTED_LAYERS)
from asistente_ladm_col.lib.geometry import GeometryUtils
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.utils.qt_utils import ProcessWithStatus
from asistente_ladm_col.utils.utils import get_key_for_quality_rule_adjusted_layer

MAX_PROGRESS_PREPARE_LAYERS = 70  # Total percentage given to layer iteration


class QualityRuleLayerManager(QObject):
    """
    Responsible for managing all layers during a Quality Rule execution
    session. It goes for LADM-COL layers only once and also manages
    intermediate layers (after snapping).
    """
    progress_changed = pyqtSignal(int)  # Progress changed

    def __init__(self, db, rules, tolerance):
        QObject.__init__(self)
        self.logger = Logger()
        self.app = AppInterface()

        self.__db = db
        self.__rules = rules
        self.__tolerance = tolerance

        self.__quality_rule_layers_config = {k: qr.layers_config(self.__db.names) if qr else dict() for k, qr in self.__rules.items()}

        # {rule_key: {QUALITY_RULE_LAYERS: {layer_name: layer},
        #             QUALITY_RULE_LADM_COL_LAYERS: {layer_name: layer}}
        self.__layers = dict()

        self.__adjusted_layers_cache = dict()

        self.__current_progress = 0

    def initialize(self, rules, tolerance):
        """
        Objects of this class are reusable calling initialize()
        """
        self.__rules = rules
        self.__tolerance = tolerance
        self.__layers = dict()

        self.__quality_rule_layers_config = {k: qr.layers_config(self.__db.names) if qr else dict() for k, qr in self.__rules.items()}

        self.__current_progress = 0

    def __prepare_layers(self):
        """
        Get layers from DB and prepare snapped layers for all rules
        """
        self.logger.info(__name__, QCoreApplication.translate("QualityRuleLayerManager", "Preparing layers..."))
        self.__emit_progress_changed(1)

        # First go for ladm-col layers
        ladm_layers = dict()
        for rule_key, rule_layers_config in self.__quality_rule_layers_config.items():
            for layer_name in rule_layers_config.get(QUALITY_RULE_LADM_COL_LAYERS, list()):
                ladm_layers[layer_name] = None

        self.logger.debug(__name__, QCoreApplication.translate("QualityRuleLayerManager", "Getting {} LADM-COL layers...").format(len(ladm_layers)))
        self.app.core.get_layers(self.__db, ladm_layers, load=True)
        if ladm_layers is None:  # If there are errors with get_layers, ladm_layers is None
            self.logger.critical(__name__, QCoreApplication.translate("QualityRuleLayerManager", "Couldn't finish preparing required layers!"))
            return False

        for name,layer in ladm_layers.items():
            if layer.isSpatial():
                GeometryUtils.create_spatial_index(layer)  # To improve performance of quality rules
        self.__emit_progress_changed(15)

        # If tolerance > 0, prepare adjusted layers
        #   We create an adjusted_layers dict to override ladm_layers per rule.
        #   For that, we need to read the config and, if not yet calculated,
        #   adjust the layers and store them in temporary cache.

        # {rule_key: {layer_name: layer}}, because each rule might need
        # different adjustments for the same layer, compared to other rules
        adjusted_layers = {rule_key: dict() for rule_key in self.__rules}

        if self.__tolerance:
            self.logger.debug(__name__, QCoreApplication.translate("QualityRuleLayerManager", "Tolerance > 0 ({}mm), adjusting layers...").format(self.__tolerance))
            self.__adjusted_layers_cache = dict()  # adjusted_layers_key: layer

            count_rules = 0
            total_rules = len([k for k, layer_config in self.__quality_rule_layers_config.items() if layer_config])
            count_layers = 0
            total_layers = 0
            for k, layer_config in self.__quality_rule_layers_config.items():
                total_layers += len(layer_config.get(QUALITY_RULE_ADJUSTED_LAYERS, dict()))

            with ProcessWithStatus(QCoreApplication.translate("QualityRuleLayerManager",
                                                              "Preparing tolerance on layers...")):
                for rule_key, rule_layers_config in self.__quality_rule_layers_config.items():
                    count_rules += 1
                    self.logger.status(QCoreApplication.translate("QualityRuleLayerManager",
                                                                  "Preparing tolerance on layers... ({} quality rules out of {})").format(count_rules, total_rules))

                    for layer_name, snap_config in rule_layers_config.get(QUALITY_RULE_ADJUSTED_LAYERS, dict()).items():
                        count_layers += 1

                        # Read from config
                        input_name = snap_config[ADJUSTED_INPUT_LAYER]  # input layer name
                        reference_name = snap_config[ADJUSTED_REFERENCE_LAYER]  # reference layer name
                        behavior = snap_config.get(ADJUSTED_BEHAVIOR, None)
                        fix = snap_config.get(FIX_ADJUSTED_LAYER, False)
                        add_topological_points = snap_config.get(ADJUSTED_TOPOLOGICAL_POINTS, False)

                        # Get input and reference layers. Note that they could be adjusted layers and in that
                        # case they would have a composed name (see get_key_for_quality_rule_adjusted_layer())
                        input = self.__adjusted_layers_cache[input_name] if input_name in self.__adjusted_layers_cache else ladm_layers[input_name]
                        reference = self.__adjusted_layers_cache[reference_name] if reference_name in self.__adjusted_layers_cache else ladm_layers[reference_name]

                        # Try to reuse if already calculated!
                        adjusted_layers_key = get_key_for_quality_rule_adjusted_layer(input_name, reference_name, fix)
                        if adjusted_layers_key not in self.__adjusted_layers_cache:
                            self.__adjusted_layers_cache[adjusted_layers_key] = self.app.core.adjust_layer(input, reference, self.__tolerance, behavior, fix, add_topological_points)
                        adjusted_layers[rule_key][layer_name] = self.__adjusted_layers_cache[adjusted_layers_key]

                        self.__emit_layer_progress(total_layers, count_layers)

            self.logger.debug(__name__, QCoreApplication.translate("QualityRuleLayerManager", "Layers adjusted..."))

        self.__emit_progress_changed(85)

        # Now that we have both ladm_layers and adjusted_layers, use them
        # in a single member dict of layers per rule (preserving original LADM-COL layers)
        self.__layers = {rule_key:{QUALITY_RULE_LAYERS: dict(), QUALITY_RULE_LADM_COL_LAYERS: dict()} for rule_key in self.__rules}
        for rule_key, rule_layers_config in self.__quality_rule_layers_config.items():
            for layer_name in rule_layers_config.get(QUALITY_RULE_LADM_COL_LAYERS, list()):
                # Fill both subdicts
                # In LADM-COL layers we send all original layers
                self.__layers[rule_key][QUALITY_RULE_LADM_COL_LAYERS][layer_name] = ladm_layers[layer_name] if layer_name in ladm_layers else None

                # In QR_Layers we store the best layer we have available (preferring adjusted over ladm-col)
                if layer_name in adjusted_layers[rule_key]:
                    self.__layers[rule_key][QUALITY_RULE_LAYERS][layer_name] = adjusted_layers[rule_key][layer_name]
                elif layer_name in ladm_layers:
                    self.__layers[rule_key][QUALITY_RULE_LAYERS][layer_name] = ladm_layers[layer_name]

            # Let QRs know if they should switch between dicts looking for original geometries
            self.__layers[rule_key][HAS_ADJUSTED_LAYERS] = bool(self.__tolerance)

        self.__emit_progress_changed(90)

        # Register adjusted layers so that Processing can properly find them
        if self.__adjusted_layers_cache:
            load_to_registry = [layer for key, layer in self.__adjusted_layers_cache.items() if layer is not None]
            self.logger.debug(__name__, "{} adjusted layers loaded to QGIS registry...".format(len(load_to_registry)))
            QgsProject.instance().addMapLayers(load_to_registry, False)

        self.__emit_progress_changed(100)

        return True

    def get_layer(self, layer_name, rule_key):
        return self.get_layers([layer_name], rule_key)

    def get_layers(self, rule_key):
        """
        Gets the layers a quality rule requires to run. This is based on the quality rule layer config.

        :param rule_key: Key of the quality rule.
        :return: Dict of layers for the given rule_key. This dict has both a 'layers' dict which has the best available
                 layer (which means, if an adjusted layer is required, it will be preferred, and if no adjusted layer is
                 required, just pass the LADM-COL layer) and a 'ladm-col' dict with the original LADM-COL layers,
                 because the quality rule might need to refer to the original object (or geometry) to build its result.
        """
        # Make sure we only call Prepare layers once for each call to run quality validations.
        if not self.__layers:
            if not self.__prepare_layers():
                return None

        return self.__layers[rule_key]

    def __emit_progress_changed(self, value, save_value=True):
        if value != self.__current_progress:  # Avoid emitting the same value twice
            if save_value:
                self.__current_progress = value
            self.progress_changed.emit(value)

    def __emit_layer_progress(self, total_layers, count_layers):
        """
        Add the normalized current layer progress value to what we have already in the overall progress
        """
        step = MAX_PROGRESS_PREPARE_LAYERS / total_layers
        value = self.__current_progress + (count_layers * step)
        self.__emit_progress_changed(int(value), count_layers == total_layers)  # Only save when all layers are done

    def clean_temporary_layers(self):
        # Removes adjusted layers from registry
        unload_from_registry = [layer.id() for key, layer in self.__adjusted_layers_cache.items() if layer is not None]
        self.logger.debug(__name__, "{} adjusted layers removed from QGIS registry...".format(len(unload_from_registry)))
        QgsProject.instance().removeMapLayers(unload_from_registry)
