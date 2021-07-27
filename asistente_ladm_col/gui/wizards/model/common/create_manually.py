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

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import QgsProject

from asistente_ladm_col.gui.wizards.model.common.args.model_args import (ValidFeaturesDigitizedArgs,
                                                                         ExecFormAdvancedArgs,
                                                                         UnexpectedFeaturesDigitizedArgs)
from asistente_ladm_col.config.enums import EnumDigitizedFeatureStatus


class CreateFeatureManuallyObserver(ABC):
    @abstractmethod
    def finish_feature_creation(self, layerId, features):
        pass

    @abstractmethod
    def form_rejected(self):
        pass

    @abstractmethod
    def exec_form_advanced(self, args: ExecFormAdvancedArgs):
        pass


class FeatureCreator(ABC):
    def __init__(self, iface, app, logger, layer, feature_name):
        super(FeatureCreator, self).__init__()
        self._iface = iface
        self._app = app
        self._layer = layer

        self._logger = logger
        self._feature_name = feature_name

        self.__observer = None

    def register_observer(self, observer: CreateFeatureManuallyObserver):
        self.__observer = observer

    def create_manually(self):
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

        dialog.rejected.connect(self.__notify_form_rejected)
        dialog.setModal(True)

        if dialog.exec_():
            args = ExecFormAdvancedArgs(layer, feature)
            self.__notify_exec_form_advanced(args)
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
        dialog.rejected.disconnect(self.__notify_form_rejected)

    def __finish_feature_creation(self, layerId, features):
        self._layer.committedFeaturesAdded.disconnect(self.__finish_feature_creation)
        self._logger.info(__name__, "{} committedFeaturesAdded SIGNAL disconnected".format(self._feature_name))
        self.__notify_finish_feature_creation(layerId, features)

    def __notify_finish_feature_creation(self, layerId, features):
        if self.__observer:
            self.__observer.finish_feature_creation(layerId, features)

    def __notify_exec_form_advanced(self, exec_form_advanced_args: ExecFormAdvancedArgs):
        if self.__observer:
            self.__observer.exec_form_advanced(exec_form_advanced_args)

    def __notify_form_rejected(self):
        if self.__observer:
            self.__observer.form_rejected()

    def __register_finish_feature(self):
        if self.__observer:
            self._layer.committedFeaturesAdded.connect(self.__observer.finish_feature_creation)


class AlphaFeatureCreator(FeatureCreator):

    def __init__(self, iface, app, logger, layer, feature_name):
        super(AlphaFeatureCreator, self).__init__(iface, app, logger, layer, feature_name)

    def _add_feature(self, layer):
        feature = self._app.core.get_new_feature(layer)
        self._exec_form(layer, feature)

    def _get_editing_layer(self):
        return self._layer


class SpatialFeatureCreator(FeatureCreator):

    def __init__(self, iface, app, logger, layer, feature_name, tolerance=None):
        super(SpatialFeatureCreator, self).__init__(iface, app, logger, layer, feature_name)
        self.__tolerance = tolerance
        self.editing_layer = layer
        self.__observer = None

    def register_geometry_observer(self, observer):
        self.__observer = observer

    def __notify_valid_features_digitized(self, args: ValidFeaturesDigitizedArgs):
        if self.__observer:
            self.__observer.valid_features_digitized(args)

    def __notify_unexpected_features_digitized(self, args: UnexpectedFeaturesDigitizedArgs):
        if self.__observer:
            self.__observer.unexpected_features_digitized(args)

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
                self.__notify_unexpected_features_digitized(
                    UnexpectedFeaturesDigitizedArgs(self.editing_layer, EnumDigitizedFeatureStatus.ZERO_FEATURES,
                                                    feature_count))

            elif self.is_a_valid_amount_of_features(feature_count):
                feature = [value for index, value in self.editing_layer.editBuffer().addedFeatures().items()][0]

                if feature.geometry().isGeosValid():
                    feature = self.__pre_exe_form()
                    self._exec_form(self._layer, feature)
                else:
                    self.__notify_unexpected_features_digitized(
                        UnexpectedFeaturesDigitizedArgs(self.editing_layer, EnumDigitizedFeatureStatus.INVALID,
                                                        feature_count))
            else:
                self.__notify_unexpected_features_digitized(
                    UnexpectedFeaturesDigitizedArgs(self.editing_layer, EnumDigitizedFeatureStatus.OTHER,
                                                    feature_count))
        # TODO check case: editBuffer=false

    def is_a_valid_amount_of_features(self, feature_count):
        return feature_count == 1

    def __pre_exe_form(self):
        args = ValidFeaturesDigitizedArgs(self.editing_layer, self.__get_added_feature())
        self.__notify_valid_features_digitized(args)
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
