# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM-COL
                             --------------------
        begin                : 2020-10-22
        git sha              : :%H$
        copyright            : (C) 2020 by Germán Carrillo (SwissTierras Colombia)
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
import os

from qgis.PyQt.QtCore import QCoreApplication

from asistente_ladm_col.config.ladm_names import LADMNames
from asistente_ladm_col.gui.field_data_capture.base_fdc_synchronization_controller import BaseFDCSynchronizationController


class FDCAdminSynchronizationController(BaseFDCSynchronizationController):
    def __init__(self, iface, db, ladm_data):
        BaseFDCSynchronizationController.__init__(self, iface, db, ladm_data)

        self.receiver_type = self._ladm_data.get_domain_code_from_value(self._db,
                                                                           self._db.names.FDC_ROLE_TYPE_D,
                                                                           LADMNames.FDC_ROLE_TYPE_D_COORDINATOR_V)

    def synchronize_data(self, db, file_path):
        if file_path and os.path.isfile(file_path):
            self.app.settings.fdc_coordinator_xtf_path = file_path
        else:
            return False, QCoreApplication.translate("FDCAdminSynchronizationController",
                                                     "First, choose a valid XTF file to synchronize.")

        return True, QCoreApplication.translate("FDCAdminSynchronizationController",
                                                "Coordinator's data have been synchronized successfully!")
