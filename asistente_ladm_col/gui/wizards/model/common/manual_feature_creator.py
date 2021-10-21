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
from abc import (abstractmethod,
                 ABC)

from qgis.PyQt.QtCore import (QCoreApplication,
                              QObject,
                             pyqtSignal)
from qgis.core import QgsProject

from asistente_ladm_col.gui.wizards.model.common.abstract_qobject_meta import AbstractQObjectMeta
from asistente_ladm_col.gui.wizards.model.common.args.model_args import (ValidFeaturesDigitizedArgs,
                                                                         ExecFormAdvancedArgs,
                                                                         UnexpectedFeaturesDigitizedArgs)
from asistente_ladm_col.config.enums import EnumDigitizedFeatureStatus


class ManualFeatureCreator(QObject, metaclass=AbstractQObjectMeta):
    finish_feature_creation = pyqtSignal(str, list)
    form_rejected = pyqtSignal()
    exec_form_advanced = pyqtSignal(ExecFormAdvancedArgs)

    def __init__(self, iface, app, logger, layer, feature_name):
        QObject.__init__(self)
        self._iface = iface
        self._app = app
        self._layer = layer

        self._logger = logger
        self._feature_name = feature_name

    def create(self):
        layer = self._get_editing_layer()
        self.__prepare_layer(layer)

        self._add_feature(layer)

    def disconnect_signals(self):
        try:
            self._layer.committedFeaturesAdded.disconnect(self.__finish_feature_creation)
        except:
            # TODO specify what type of exception is caught
            pass

    @abstractmethod
    def _add_feature(self, layer):
        pass

    @abstractmethod
    def _get_editing_layer(self):
        pass

    def __prepare_layer(self, layer):
        self._iface.layerTreeView().setCurrentLayer(layer)
        # The original layer. It is not the editing layer
        self._layer.committedFeaturesAdded.connect(self.__finish_feature_creation)

        if not layer.isEditable():
            layer.startEditing()

    def _exec_form(self, layer, feature):
        dialog = self._iface.getFeatureForm(layer, feature)

        dialog.rejected.connect(self.form_rejected)
        dialog.setModal(True)

        if dialog.exec_():
            args = ExecFormAdvancedArgs(layer, feature)
            self.exec_form_advanced.emit(args)
            saved = layer.commitChanges()

            if not saved:
                layer.rollBack()
                self._logger.warning_msg(__name__,
                                          QCoreApplication.translate("WizardTranslations",
                                                                     "Error while saving changes. {} could not be created.").format(
                                              self._feature_name))

                for e in layer.commitErrors():
                    self._logger.warning(__name__, "Commit error: {}".format(e))
        else:
            layer.rollBack()
        self._iface.mapCanvas().refresh()
        dialog.rejected.disconnect(self.form_rejected)

    def __finish_feature_creation(self, layerId, features):
        self._layer.committedFeaturesAdded.disconnect(self.__finish_feature_creation)
        self._logger.info(__name__, "{} committedFeaturesAdded SIGNAL disconnected".format(self._feature_name))
        self.finish_feature_creation.emit(layerId, features)


class AlphaFeatureCreator(ManualFeatureCreator):

    def __init__(self, iface, app, logger, layer, feature_name):
        ManualFeatureCreator.__init__(self, iface, app, logger, layer, feature_name)

    def _add_feature(self, layer):
        feature = self._app.core.get_new_feature(layer)
        self._exec_form(layer, feature)

    def _get_editing_layer(self):
        return self._layer


class SpatialFeatureCreator(ManualFeatureCreator):
    valid_features_digitized = pyqtSignal(ValidFeaturesDigitizedArgs)
    unexpected_features_digitized = pyqtSignal(UnexpectedFeaturesDigitizedArgs)

    def __init__(self, iface, app, logger, layer, feature_name, tolerance=None):
        ManualFeatureCreator.__init__(self, iface, app, logger, layer, feature_name)
        self.__tolerance = tolerance
        self.editing_layer = layer

    def _add_feature(self, layer):
        QgsProject.instance().setAutoTransaction(False)

        # Activate snapping
        if self.__tolerance:
            self._app.core.active_snapping_all_layers(self.__tolerance)
        else:
            self._app.core.active_snapping_all_layers()

        self._app.core.suppress_form(layer, True)
        self._iface.actionAddFeature().trigger()
        # ------------------------------------------

        self._logger.info_msg(__name__, QCoreApplication.translate(
            "WizardTranslations", "You can now start capturing {} digitizing on the map...")
                               .format(self._feature_name))

    def save_created_geometry(self):
        if self.editing_layer.editBuffer():
            feature_count = len(self.editing_layer.editBuffer().addedFeatures())
            if feature_count == 0:
                self.unexpected_features_digitized.emit(
                    UnexpectedFeaturesDigitizedArgs(self.editing_layer, EnumDigitizedFeatureStatus.ZERO_FEATURES,
                                                    feature_count))

            elif self.is_a_valid_amount_of_features(feature_count):
                feature = [value for index, value in self.editing_layer.editBuffer().addedFeatures().items()][0]

                if feature.geometry().isGeosValid():
                    feature = self.__pre_exe_form()
                    self._exec_form(self._layer, feature)
                else:
                    self.unexpected_features_digitized.emit(
                        UnexpectedFeaturesDigitizedArgs(self.editing_layer, EnumDigitizedFeatureStatus.INVALID,
                                                        feature_count))
            else:
                self.unexpected_features_digitized.emit(
                    UnexpectedFeaturesDigitizedArgs(self.editing_layer, EnumDigitizedFeatureStatus.OTHER,
                                                    feature_count))
        # TODO check case: editBuffer=false

    @staticmethod
    def is_a_valid_amount_of_features(feature_count):
        return feature_count == 1

    def __pre_exe_form(self):
        args = ValidFeaturesDigitizedArgs(self.editing_layer, self.__get_added_feature())
        self.valid_features_digitized.emit(args)
        return args.feature

    #  ok
    def __get_added_feature(self):
        # [value for index, value in layer.editBuffer().addedFeatures().items()][0]
        feature = None
        for id, added_feature in self.editing_layer.editBuffer().addedFeatures().items():
            feature = added_feature
            break

        return feature

    def _get_editing_layer(self):
        return self.editing_layer if self.editing_layer and self.editing_layer != self._layer else self._layer

    def disconnect_signals(self):
        super(SpatialFeatureCreator, self).disconnect_signals()
        # TODO this code does not disconnect signals
        if self.editing_layer != self._layer:
            self.editing_layer.rollBack()
            QgsProject.instance().removeMapLayer(self.editing_layer)
