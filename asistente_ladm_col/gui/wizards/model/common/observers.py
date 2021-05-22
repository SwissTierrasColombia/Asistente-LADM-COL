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
from abc import (abstractmethod,
                 ABC)

from asistente_ladm_col.gui.wizards.model.common.args.model_args import (FinishFeatureCreationArgs,
                                                                         ValidFeaturesDigitizedArgs,
                                                                         UnexpectedFeaturesDigitizedArgs)


class FinishFeatureCreationObserver(ABC):
    @abstractmethod
    def finish_feature_creation(self, args: FinishFeatureCreationArgs):
        pass


class FormRejectedObserver(ABC):
    @abstractmethod
    def form_rejected(self):
        pass


class ValidFeatureDigitizedObserver(ABC):
    @abstractmethod
    def valid_features_digitized(self, args: ValidFeaturesDigitizedArgs):
        pass


class UnexpectedFeatureDigitizedObserver(ABC):
    @abstractmethod
    def unexpected_features_digitized(self, args: UnexpectedFeaturesDigitizedArgs):
        pass
