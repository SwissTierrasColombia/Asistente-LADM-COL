import os.path
from qgis.PyQt.QtCore import (QLocale,
                              QSettings,
                              QCoreApplication,
                              QTranslator)

DEFAULT_LANGUAGE = 'en'

try:
    # Errors here could happen if the value cannot be converted to string or
    # if it is not subscriptable (see https://github.com/gacarrillor/loadthemall/issues/11)
    locale = QSettings().value("locale/userLocale", type=str)
    QGIS_LANG = str( locale[:2] )
except TypeError as e:
    QGIS_LANG = DEFAULT_LANGUAGE
PLUGIN_DIR = os.path.dirname(os.path.dirname(__file__))

# Install Qt Translator
qgis_locale = QLocale(QGIS_LANG)
locale_path = os.path.join(PLUGIN_DIR, 'i18n')
translator = QTranslator()
translator.load(qgis_locale, 'Asistente-LADM_COL', '_', locale_path)
QCoreApplication.installTranslator(translator)
