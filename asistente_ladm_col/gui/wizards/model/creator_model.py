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
from abc import (ABC,
                 abstractmethod)

from qgis.PyQt.QtCore import (QObject,
                             pyqtSignal)

from asistente_ladm_col import Logger
from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.config.general_config import (WIZARD_LAYERS,
                                                      WIZARD_EDITING_LAYER_NAME,
                                                      WIZARD_READ_ONLY_FIELDS)
from asistente_ladm_col.gui.wizards.model.common.abstract_qobject_meta import AbstractQObjectMeta
from asistente_ladm_col.gui.wizards.model.common.args.model_args import (FinishFeatureCreationArgs,
                                                                         ExecFormAdvancedArgs)
from asistente_ladm_col.gui.wizards.model.common.manual_feature_creator import ManualFeatureCreator
from asistente_ladm_col.gui.wizards.model.common.refactor_fields_feature_creator import RefactorFieldsFeatureCreator
from asistente_ladm_col.gui.wizards.model.common.common_operations import CommonOperationsModel
from asistente_ladm_col.gui.wizards.model.common.layer_remove_signals_manager import LayerRemovedSignalsManager


class CreatorModel(QObject, metaclass=AbstractQObjectMeta):
    finish_feature_creation = pyqtSignal(FinishFeatureCreationArgs)
    form_rejected = pyqtSignal()
    layer_removed = pyqtSignal()

    def __init__(self, iface, db, wiz_config):
        QObject.__init__(self)
        self.app = AppInterface()

        self._db = db
        self._wizard_config = wiz_config
        self._iface = iface

        self._logger = Logger()

        self._editing_layer_name = self._wizard_config[WIZARD_EDITING_LAYER_NAME]
        self._editing_layer = self._wizard_config[WIZARD_LAYERS][self._editing_layer_name]

        self.__manual_feature_creator = self._create_feature_creator()
        # chain of signals
        self.__manual_feature_creator.form_rejected.connect(self.form_rejected)
        self.__manual_feature_creator.exec_form_advanced.connect(self.exec_form_advanced)
        # connect local method finish feature creator
        self.__manual_feature_creator.finish_feature_creation.connect(self._finish_feature_creation)

        self.__feature_creator_from_refactor = RefactorFieldsFeatureCreator(self.app, db)

        self.__common_operations = \
            CommonOperationsModel(self._wizard_config[WIZARD_LAYERS], self._editing_layer_name, self.app,
                                  self._wizard_config[WIZARD_READ_ONLY_FIELDS])

        self.refactor_field_mapping = self.__common_operations.get_field_mappings_file_names()

        self._layer_remove_manager = LayerRemovedSignalsManager(self._wizard_config[WIZARD_LAYERS])
        self._layer_remove_manager.layer_removed.connect(self.layer_removed)

    def _finish_feature_creation(self, layerId, features):
        fid = features[0].id()
        is_valid = False
        feature_tid = None

        if not self._editing_layer.getFeature(fid).isValid():
            self._logger.warning(__name__, "Feature not found in layer {} ...".format(self._editing_layer_name))
        else:
            is_valid = True
            feature_tid = self._editing_layer.getFeature(fid)[self._db.names.T_ID_F]

        args = FinishFeatureCreationArgs(is_valid, feature_tid)
        self.finish_feature_creation.emit(args)

    @abstractmethod
    def _create_feature_creator(self) -> ManualFeatureCreator:
        pass

    @abstractmethod
    def exec_form_advanced(self, args: ExecFormAdvancedArgs):
        pass

    def set_ready_only_fields(self, read_only):
        self.__common_operations.set_read_only_fields(read_only)

    def create_feature_from_refactor(self, selected_layer, field_mapping):
        self.__feature_creator_from_refactor.create(selected_layer, self._editing_layer_name, field_mapping)

    def create_feature_manually(self):
        self._layer_remove_manager.reconnect_signals()
        self.__manual_feature_creator.create()

    def dispose(self):
        self._layer_remove_manager.disconnect_signals()
        self.__manual_feature_creator.disconnect_signals()
        self.__common_operations.rollback_in_layers_with_empty_editing_buffer()
        self.__common_operations.set_read_only_fields(False)
