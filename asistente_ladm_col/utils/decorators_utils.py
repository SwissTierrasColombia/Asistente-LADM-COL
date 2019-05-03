from functools import wraps

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (Qgis,
                       QgsApplication)
from qgis.utils import (isPluginLoaded, loadPlugin, startPlugin)

from ..config.general_config import PLUGIN_NAME


def _activate_processing_module(func_to_decorate):
    @wraps(func_to_decorate)
    def decorated_function(*args, **kwargs):

        if not isPluginLoaded("processing"):
            loadPlugin('processing')
            startPlugin('processing')
            msg = QCoreApplication.translate("AsistenteLADMCOLPlugin", "The processing plugin has been activated!")
            QgsApplication.messageLog().logMessage(msg, PLUGIN_NAME, Qgis.Info)

        func_to_decorate(*args, **kwargs)

    return decorated_function
