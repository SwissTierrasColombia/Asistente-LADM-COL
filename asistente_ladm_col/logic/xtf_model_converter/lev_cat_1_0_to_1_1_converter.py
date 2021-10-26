from qgis.PyQt.QtCore import (pyqtSignal,
                              QObject)

from asistente_ladm_col.core.xtf_model_converter.ladm_col_model_converter import LADMColModelConverter


class Survey10To11Converter(LADMColModelConverter):
    """
    Abstract class for LADM-COL model converters
    """
    progress_changed = pyqtSignal(int)

    def __init__(self):
        LADMColModelConverter.__init__(self)

        self._key = "lev_cat_1_0-lev_cat_1_1"
        self._display_name = "Levantamiento Catastral 1.0 a Levantamiento Catastral 1.1"
        self._from_models = ["Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0"]
        self._to_models = ["Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_1"]

    def id(self):
        return self._key

    def display_name(self):
        return self._display_name

    def convert(self, source_xtf, target_xtf, params):
        return True, "Success!"
