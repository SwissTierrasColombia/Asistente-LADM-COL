"""
/***************************************************************************
                              Asistente LADM-COL
                             --------------------
        begin           : 2021-10-26
        git sha         : :%H$
        copyright       : (C) 2021 by Germán Carrillo (SwissTierras Colombia)
        email           : gcarrillo@linuxmail.org
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""
from abc import abstractmethod

from qgis.PyQt.QtCore import (pyqtSignal,
                              QObject)

from asistente_ladm_col.utils.abstract_class import AbstractQObjectMeta


class AbstractLADMColModelConverter(QObject, metaclass=AbstractQObjectMeta):
    """
    Abstract class for LADM-COL model converters
    """
    progress_changed = pyqtSignal(int)

    def __init__(self):
        QObject.__init__(self)

        self._key = ""  # E.g., "lev_cat_1_0-lev_cat_1_1"
        self._display_name = ""  # E.g., "Levantamiento Catastral 1.0 a Levantamiento Catastral 1.1"
        self._from_models = list()  # List of full names of supported models
        self._to_models = list()  # List of full names of target models

    def id(self):
        return self._key

    def display_name(self):
        return self._display_name

    def supports_source_model(self, model_full_name):
        return model_full_name in self._from_models

    def is_valid(self):
        return bool(self.id().strip()) and bool(self.display_name().strip()) and len(self._from_models) and len(self._to_models)

    @abstractmethod
    def convert(self, source_xtf, target_xtf, params):
        """
        Convert the data inside the source XTF file to the LADM-COL structure in self.__to_models().

        :param source_xtf: Path to source XTF file
        :param target_xtf: Path to target XTF file
        :param params:
        :return: tuple: (res, msg), where res is a boolean saying whether the conversion was successful or not, and
                        msg is a string explaining the reason of a failure.
        """
        raise NotImplementedError
