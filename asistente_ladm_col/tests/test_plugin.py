# -*- coding: utf-8 -*-
import os

from qgis.testing.mocked import get_iface
from asistente_ladm_col.asistente_ladm_col_plugin import AsistenteLADMCOLPlugin
from asistente_ladm_col.tests.utils import import_projectgenerator

import_projectgenerator()

iface = get_iface()
asistente_ladm_col_plugin = AsistenteLADMCOLPlugin(iface)
asistente_ladm_col_plugin.initGui()
