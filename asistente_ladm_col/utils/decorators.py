import time
from functools import wraps

from qgis.PyQt.QtCore import (Qt,
                              QCoreApplication,
                              QSettings)
from qgis.PyQt.QtWidgets import QPushButton
from qgis.core import (Qgis,
                       QgsApplication)
from qgis.utils import (isPluginLoaded, loadPlugin, startPlugin)

from ..config.general_config import (PLUGIN_NAME,
                                     QGIS_MODEL_BAKER_PLUGIN_NAME,
                                     QGIS_MODEL_BAKER_REQUIRED_VERSION_URL,
                                     QGIS_MODEL_BAKER_MIN_REQUIRED_VERSION,
                                     QGIS_MODEL_BAKER_EXACT_REQUIRED_VERSION, MAP_SWIPE_TOOL_PLUGIN_NAME,
                                     MAP_SWIPE_TOOL_MIN_REQUIRED_VERSION, MAP_SWIPE_TOOL_EXACT_REQUIRED_VERSION,
                                     MAP_SWIPE_TOOL_REQUIRED_VERSION_URL, QGIS_MODEL_BAKER_PLUGIN_NAME)

from ..config.general_config import (LOG_QUALITY_PREFIX_TOPOLOGICAL_RULE_TITLE,
                                     LOG_QUALITY_SUFFIX_TOPOLOGICAL_RULE_TITLE,
                                     LOG_QUALITY_LIST_CONTAINER_OPEN,
                                     LOG_QUALITY_LIST_CONTAINER_CLOSE,
                                     LOG_QUALITY_CONTENT_SEPARATOR)
from .qt_utils import OverrideCursor


def _db_connection_required(func_to_decorate):
    @wraps(func_to_decorate)
    def decorated_function(inst, *args, **kwargs):
        # Check if current connection is valid and disable access if not
        db = inst.get_db_connection()
        res, msg = db.test_connection()
        if res:
            if not inst.qgis_utils._layers and not inst.qgis_utils._relations:
                inst.qgis_utils.cache_layers_and_relations(db, ladm_col_db=True)

            func_to_decorate(inst)
        else:
            widget = inst.iface.messageBar().createMessage("Asistente LADM_COL",
                                                           QCoreApplication.translate("AsistenteLADMCOLPlugin",
                                                                                      "Check your database connection, since there was a problem accessing a valid Cadastre-Registry model in the database. Click the button to go to Settings."))
            button = QPushButton(widget)
            button.setText(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Settings"))
            button.pressed.connect(inst.show_settings)
            widget.layout().addWidget(button)
            inst.iface.messageBar().pushWidget(widget, Qgis.Warning, 15)
            inst.log.logMessage(
                QCoreApplication.translate("AsistenteLADMCOLPlugin",
                                           "A dialog/tool couldn't be opened/executed, connection to DB was not valid."),
                PLUGIN_NAME,
                Qgis.Warning
            )

    return decorated_function

def _qgis_model_baker_required(func_to_decorate):
    @wraps(func_to_decorate)
    def decorated_function(inst, *args, **kwargs):
        # Check if QGIS Model Baker is installed and active, disable access if not
        plugin_version_right = inst.is_plugin_version_valid(QGIS_MODEL_BAKER_PLUGIN_NAME,
                                                            QGIS_MODEL_BAKER_MIN_REQUIRED_VERSION,
                                                            QGIS_MODEL_BAKER_EXACT_REQUIRED_VERSION)

        if plugin_version_right:
            func_to_decorate(inst)
        else:
            if QGIS_MODEL_BAKER_REQUIRED_VERSION_URL:
                # If we depend on a specific version of QGIS Model Baker (only on that one)
                # and it is not the latest version, show a download link
                msg = QCoreApplication.translate("AsistenteLADMCOLPlugin",
                                                 "The plugin 'QGIS Model Baker' version {} is required, but couldn't be found. Download it <a href=\"{}\">from this link</a> and use 'Install from ZIP' in the Plugin Manager.").format(
                    QGIS_MODEL_BAKER_MIN_REQUIRED_VERSION, QGIS_MODEL_BAKER_REQUIRED_VERSION_URL)
            else:
                msg = QCoreApplication.translate("AsistenteLADMCOLPlugin",
                                                 "The plugin 'QGIS Model Baker' version {} {}is required, but couldn't be found. Click the button to show the Plugin Manager.").format(
                    QGIS_MODEL_BAKER_MIN_REQUIRED_VERSION,
                    '' if QGIS_MODEL_BAKER_EXACT_REQUIRED_VERSION else '(or higher) ')

            widget = inst.iface.messageBar().createMessage("Asistente LADM_COL", msg)
            button = QPushButton(widget)
            button.setText(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Plugin Manager"))
            button.pressed.connect(inst.show_plugin_manager)
            widget.layout().addWidget(button)
            inst.iface.messageBar().pushWidget(widget, Qgis.Warning, 15)

            inst.log.logMessage(
                QCoreApplication.translate("AsistenteLADMCOLPlugin",
                                           "A dialog/tool couldn't be opened/executed, QGIS Model Baker not found."),
                PLUGIN_NAME,
                Qgis.Warning
            )

    return decorated_function

def _activate_processing_plugin(func_to_decorate):
    @wraps(func_to_decorate)
    def decorated_function(*args, **kwargs):

        if not isPluginLoaded("processing"):
            loadPlugin('processing')
            startPlugin('processing')
            msg = QCoreApplication.translate("AsistenteLADMCOLPlugin", "The processing plugin has been activated!")
            QgsApplication.messageLog().logMessage(msg, PLUGIN_NAME, Qgis.Info)

            # Check in the plugin manager that the processing plugin was activated
            QSettings().setValue("PythonPlugins/processing", True)

        func_to_decorate(*args, **kwargs)

    return decorated_function

def _log_quality_checks(func_to_decorate):
    @wraps(func_to_decorate)
    def add_format_to_text(self, db, **args):
        rule_name = args['rule_name']
        self.log_quality_set_initial_progress_emitted.emit(rule_name)
        self.log_dialog_quality_text_content += LOG_QUALITY_LIST_CONTAINER_OPEN

        start_time = time.time()
        with OverrideCursor(Qt.WaitCursor):
            func_to_decorate(self, db, **args)
        end_time = time.time()

        self.total_time = self.total_time + (end_time - start_time)

        self.log_dialog_quality_text_content += LOG_QUALITY_LIST_CONTAINER_CLOSE
        self.log_dialog_quality_text_content += LOG_QUALITY_CONTENT_SEPARATOR

        self.log_dialog_quality_text += "{}{} [{}]{}".format(LOG_QUALITY_PREFIX_TOPOLOGICAL_RULE_TITLE,
                                                              rule_name, self.utils.set_time_format(end_time - start_time), LOG_QUALITY_SUFFIX_TOPOLOGICAL_RULE_TITLE)
        self.log_dialog_quality_text += self.log_dialog_quality_text_content
        self.log_dialog_quality_text_content = ""

        self.log_quality_set_final_progress_emitted.emit(rule_name)

    return add_format_to_text

def _official_db_connection_required(func_to_decorate):
    @wraps(func_to_decorate)
    def decorated_function(inst, *args, **kwargs):
        # Check if current connection is valid and disable access if not
        db = inst.get_official_db_connection()
        res, msg = db.test_connection()
        if res:
            func_to_decorate(inst)
        else:
            widget = inst.iface.messageBar().createMessage("Asistente LADM_COL",
                         QCoreApplication.translate("AsistenteLADMCOLPlugin",
                         "Check your official database connection, since there was a problem accessing a valid Cadastre-Registry model in the database. Click the button to go to Settings."))
            button = QPushButton(widget)
            button.setText(QCoreApplication.translate("AsistenteLADMCOLPlugin", " Official Data Settings"))
            button.pressed.connect(inst.show_official_data_settings)
            widget.layout().addWidget(button)
            inst.iface.messageBar().pushWidget(widget, Qgis.Warning, 15)
            inst.log.logMessage(
                QCoreApplication.translate("AsistenteLADMCOLPlugin", "A dialog/tool couldn't be opened/executed, connection to official DB was not valid."),
                PLUGIN_NAME,
                Qgis.Warning
            )

    return decorated_function

def _different_db_connections_required(func_to_decorate):
    @wraps(func_to_decorate)
    def decorated_function(inst, *args, **kwargs):
        db = inst.get_db_connection()
        official_db = inst.get_official_db_connection()
        res = db.equals(official_db)

        if not res:
            func_to_decorate(inst)
        else:
            widget = inst.iface.messageBar().createMessage("Asistente LADM_COL",
                         QCoreApplication.translate("AsistenteLADMCOLPlugin",
                         "Your 'official' database is the same 'collected' database!!! Click the proper button to change connection settings."))

            button1 = QPushButton(widget)
            button1.setText(QCoreApplication.translate("AsistenteLADMCOLPlugin", " Change official settings"))
            button1.pressed.connect(inst.show_official_data_settings_clear_message_bar)
            widget.layout().addWidget(button1)

            button2 = QPushButton(widget)
            button2.setText(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Change collected settings"))
            button2.pressed.connect(inst.show_settings_clear_message_bar)
            widget.layout().addWidget(button2)

            inst.iface.messageBar().pushWidget(widget, Qgis.Warning, 20)
            inst.log.logMessage(
                QCoreApplication.translate("AsistenteLADMCOLPlugin", "A dialog/tool couldn't be opened/executed, official DB is the same collected DB!"),
                PLUGIN_NAME,
                Qgis.Warning
            )

    return decorated_function

def _map_swipe_tool_required(func_to_decorate):
    @wraps(func_to_decorate)
    def decorated_function(inst, *args, **kwargs):
        # Check if Map Swipe Tool is installed and active, disable access if not
        plugin_version_right = inst.is_plugin_version_valid(MAP_SWIPE_TOOL_PLUGIN_NAME,
                                                            MAP_SWIPE_TOOL_MIN_REQUIRED_VERSION,
                                                            MAP_SWIPE_TOOL_EXACT_REQUIRED_VERSION)

        if plugin_version_right:
            func_to_decorate(inst)
        else:
            if MAP_SWIPE_TOOL_REQUIRED_VERSION_URL:
                # If we depend on a specific version of Map Swipe Tool (only on that one)
                # and it is not the latest version, show a download link
                msg = QCoreApplication.translate("AsistenteLADMCOLPlugin", "The plugin 'MapSwipe Tool' version {} is required, but couldn't be found. Download it <a href=\"{}\">from this link</a> and use 'Install from ZIP' in the Plugin Manager.").format(MAP_SWIPE_TOOL_MIN_REQUIRED_VERSION, MAP_SWIPE_TOOL_REQUIRED_VERSION_URL)
            else:
                msg = QCoreApplication.translate("AsistenteLADMCOLPlugin", "The plugin 'MapSwipe Tool' version {} {}is required, but couldn't be found. Click the button to show the Plugin Manager.").format(MAP_SWIPE_TOOL_MIN_REQUIRED_VERSION, '' if MAP_SWIPE_TOOL_EXACT_REQUIRED_VERSION else '(or higher) ')

            widget = inst.iface.messageBar().createMessage("Asistente LADM_COL", msg)
            button = QPushButton(widget)
            button.setText(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Plugin Manager"))
            button.pressed.connect(inst.show_plugin_manager)
            widget.layout().addWidget(button)
            inst.iface.messageBar().pushWidget(widget, Qgis.Warning, 15)

            inst.log.logMessage(
                QCoreApplication.translate("AsistenteLADMCOLPlugin", "A dialog/tool couldn't be opened/executed, MapSwipe Tool not found."),
                PLUGIN_NAME,
                Qgis.Warning
            )

    return decorated_function
