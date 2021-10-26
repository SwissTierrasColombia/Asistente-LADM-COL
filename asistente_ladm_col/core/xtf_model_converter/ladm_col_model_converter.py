from abc import ABCMeta

from qgis.PyQt.QtCore import (pyqtSignal,
                              QObject)

try:
    from qgis.PyQt.QtCore import pyqtWrapperType
except ImportError:
    from sip import wrappertype as pyqtWrapperType


class AbstractQObjectMeta(pyqtWrapperType, ABCMeta):
    pass


class LADMColModelConverter(QObject):
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
        return self.id().strip() and self.display_name().strip() and len(self._from_models) and len(self._to_models)

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
