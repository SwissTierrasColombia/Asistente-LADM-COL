"""
/***************************************************************************
                              Asistente LADM-COL
                             --------------------
        begin                : 2021-10-26
        git sha              : :%H$
        copyright            : (C) 2021 by Germán Carrillo (BSF Swissphoto)
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
from qgis.PyQt.QtCore import (QObject,
                              pyqtSignal)

from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.core.xtf_model_converter.xtf_model_converter_registry import XTFModelConverterRegistry
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.utils.interlis_utils import get_models_from_xtf


class XTFModelConverterController(QObject):

    progress_changed = pyqtSignal(int)  # Percentage

    def __init__(self):
        QObject.__init__(self)

        self.logger = Logger()
        self.app = AppInterface()

        self._converter_registry = XTFModelConverterRegistry()

    def get_converters(self, source_xtf):
        converters = dict()  # {converter_key: name}

        if source_xtf:
            # Get models present in the source XTF
            models = get_models_from_xtf(source_xtf)
            self.logger.debug(__name__, "Models found in source XTF: {}".format(models))

            # Ask the registry for converters that apply for those models
            if models:
                converters = self._converter_registry.get_converters_for_models(models)
                self.logger.debug(__name__, "Converters found for source XTF models: {}".format(list(converters.keys())))

        return converters

    #def get_converter_parameter_widgets(self, converter_key):
    #    return self._converter_registry.get_converter_parameter_widgets(converter_key)  # List of widgets

    def convert(self, converter_key, source_xtf, target_xtf, params):
        converter = self._converter_registry.get_converter(converter_key)
        converter.progress_changed.connect(self.progress_changed)
        res, msg = converter.convert(source_xtf, target_xtf, params)

        return res, msg
