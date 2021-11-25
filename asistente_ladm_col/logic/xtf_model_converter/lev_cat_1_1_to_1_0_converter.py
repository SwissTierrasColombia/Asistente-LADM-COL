"""
/***************************************************************************
                              Asistente LADM-COL
                             --------------------
        begin           : 2021-10-28
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
from qgis.PyQt.QtCore import (pyqtSignal,
                              QObject,
                              QCoreApplication)

from asistente_ladm_col.core.xtf_model_converter.ladm_col_model_converter import LADMColModelConverter
from asistente_ladm_col.utils.utils import get_number_of_lines_in_file


class Survey11To10Converter(LADMColModelConverter):
    """
    Convert data from Lev_Cat_V1_1 to Lev_Cat_V1_0
    """
    _REPLACE_STRINGS = {"Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_1": "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0",
                        "<Tipo>Documento_Publico.Escritura_Publica</Tipo>": "<Tipo>Escritura_Publica</Tipo>",
                        "<Tipo>Documento_Publico.Sentencia_Judicial</Tipo>": "<Tipo>Sentencia_Judicial</Tipo>",
                        "<Tipo>Documento_Publico.Acto_Administrativo</Tipo>": "<Tipo>Acto_Administrativo</Tipo>",
                        "<Tipo>Documento_Privado.Documento_Privado</Tipo>": "<Tipo>Documento_Privado</Tipo>",
                        "<Tipo>Documento_Privado.Sin_Documento</Tipo>": "<Tipo>Sin_Documento</Tipo>",
                        "<Tipo>Predio.Publico.Baldio</Tipo>": "<Tipo>Publico.Baldio</Tipo>",
                        "<Tipo>Predio.Publico.Fiscal</Tipo>": "<Tipo>Publico.Fiscal</Tipo>",
                        "<Tipo>Predio.Publico.Patrimonial</Tipo>": "<Tipo>Publico.Patrimonial</Tipo>",
                        "<Tipo>Predio.Publico.Uso_Publico</Tipo>": "<Tipo>Publico.Uso_Publico</Tipo>",
                        "<Tipo>Predio.Privado</Tipo>": "<Tipo>Privado</Tipo>",
                        "<Tipo>Predio.Territorio_Colectivo</Tipo>": "<Tipo>Territorio_Colectivo</Tipo>",
                        "<Tipo>Predio.Vacante</Tipo>": "<Tipo>Vacante</Tipo>",
                        "<PuntoTipo>Catastro.Poste</PuntoTipo>": "<PuntoTipo>Poste</PuntoTipo>",
                        "<PuntoTipo>Catastro.Construccion</PuntoTipo>": "<PuntoTipo>Construccion</PuntoTipo>",
                        "<PuntoTipo>Catastro.Punto_Dinamico</PuntoTipo>": "<PuntoTipo>Punto_Dinamico</PuntoTipo>",
                        "<PuntoTipo>Catastro.Elemento_Natural</PuntoTipo>": "<PuntoTipo>Elemento_Natural</PuntoTipo>",
                        "<PuntoTipo>Catastro.Piedra</PuntoTipo>": "<PuntoTipo>Piedra</PuntoTipo>",
                        "<PuntoTipo>Catastro.Sin_Materializacion</PuntoTipo>": "<PuntoTipo>Sin_Materializacion</PuntoTipo>",
                        "<PuntoTipo>Catastro.Mojon</PuntoTipo>": "<PuntoTipo>Mojon</PuntoTipo>",
                        "<PuntoTipo>Catastro.Incrustacion</PuntoTipo>": "<PuntoTipo>Incrustacion</PuntoTipo>",
                        "<PuntoTipo>Catastro.Pilastra</PuntoTipo>": "<PuntoTipo>Pilastra</PuntoTipo>",
                        "Submodelo_Cartografia_Catastral_V1_1": "Submodelo_Cartografia_Catastral_V1_0",
                        "Submodelo_Avaluos_V1_1": "Submodelo_Avaluos_V1_0"}

    def __init__(self):
        LADMColModelConverter.__init__(self)

        self._key = "lev_cat_1_1-lev_cat_1_0"
        self._display_name = "Levantamiento Catastral 1.1 a Levantamiento Catastral 1.0"
        self._from_models = ["Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_1"]
        self._to_models = ["Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0"]

    def convert(self, source_xtf, target_xtf, params):
        num_lines = get_number_of_lines_in_file(source_xtf)
        dict_percentages = {0 if k == 0 else int(num_lines * k / 100): k for k in range(0, 100, 10)}  # {val: percentage}
        list_percentages = list(dict_percentages.keys())

        count = 0
        try:
            with open(source_xtf, "r") as f:
                with open(target_xtf, "w") as output:
                    for line in f:
                        # Progress handling
                        count += 1
                        if list_percentages and count > list_percentages[0]:
                            self.progress_changed.emit(dict_percentages[list_percentages[0]])
                            list_percentages.pop(0)

                        for k in self._REPLACE_STRINGS:
                            if k in line:
                                line = line.replace(k, self._REPLACE_STRINGS[k])
                        output.write(line)
        except Exception as e:
            return False, QCoreApplication.translate("Survey11To10Converter",
                                                     "A problem was found converting data to '{}' model! Details: {}").format(
                self._to_models[0], e)

        self.progress_changed.emit(100)
        return True, QCoreApplication.translate("Survey11To10Converter",
                                                "The data was successfully converted to '{}' model!").format(
            self._to_models[0])
