"""
/***************************************************************************
                              Asistente LADM-COL
                             --------------------
        begin           : 2021-11-12
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
from asistente_ladm_col.lib.ili.ili2dbconfig import ValidateDataConfiguration
from asistente_ladm_col.lib.ili.iliexecutable import IliExecutable


class Ili2DBValidator(IliExecutable):
    """
    Executes a validate operation using ili2db.
    Note: this is not iliValidator, but ili2db --validate.
    """
    SUCCESS_WITH_VALIDATION_ERRORS = 1
    __done_with_validation_errors = "...validate failed"

    def __init__(self, parent=None):
        super(Ili2DBValidator, self).__init__(parent)

    def _create_config(self):
        return ValidateDataConfiguration()

    def _search_custom_pattern(self, text):
        if self.__done_with_validation_errors == text.strip():
            self._result = self.SUCCESS_WITH_VALIDATION_ERRORS
