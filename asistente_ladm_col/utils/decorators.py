import time
from copy import deepcopy
from functools import (wraps,
                       partial)

from qgis.PyQt.QtCore import (Qt,
                              QCoreApplication,
                              QSettings,
                              QEventLoop)
from qgis.PyQt.QtWidgets import QPushButton
from qgis.core import Qgis
from qgis.utils import (isPluginLoaded,
                        loadPlugin,
                        startPlugin)

from asistente_ladm_col.config.enums import EnumQualityRuleResult
from asistente_ladm_col.config.general_config import (MAP_SWIPE_TOOL_MIN_REQUIRED_VERSION,
                                                      MAP_SWIPE_TOOL_EXACT_REQUIRED_VERSION,
                                                      MAP_SWIPE_TOOL_REQUIRED_VERSION_URL,
                                                      INVISIBLE_LAYERS_AND_GROUPS_PLUGIN_NAME,
                                                      INVISIBLE_LAYERS_AND_GROUPS_MIN_REQUIRED_VERSION,
                                                      LOG_QUALITY_PREFIX_TOPOLOGICAL_RULE_TITLE,
                                                      LOG_QUALITY_SUFFIX_TOPOLOGICAL_RULE_TITLE,
                                                      LOG_QUALITY_LIST_CONTAINER_OPEN,
                                                      LOG_QUALITY_LIST_CONTAINER_CLOSE,
                                                      LOG_QUALITY_CONTENT_SEPARATOR,
                                                      COLLECTED_DB_SOURCE,
                                                      SETTINGS_CONNECTION_TAB_INDEX,
                                                      LOG_QUALITY_LIST_ITEM_ERROR_OPEN,
                                                      LOG_QUALITY_LIST_ITEM_ERROR_CLOSE,
                                                      LOG_QUALITY_LIST_ITEM_SUCCESS_OPEN,
                                                      LOG_QUALITY_LIST_ITEM_SUCCESS_CLOSE,
                                                      LOG_QUALITY_LIST_ITEM_OPEN,
                                                      LOG_QUALITY_LIST_ITEM_CLOSE,
                                                      LOG_QUALITY_LIST_ITEM_CRITICAL_OPEN,
                                                      LOG_QUALITY_LIST_ITEM_CRITICAL_CLOSE,
                                                      LOG_QUALITY_OPTIONS_OPEN,
                                                      LOG_QUALITY_OPTIONS_CLOSE)
from asistente_ladm_col.config.ladm_names import LADMNames
from asistente_ladm_col.config.translation_strings import TranslatableConfigStrings as Tr
from asistente_ladm_col.lib.context import (SettingsContext,
                                            TaskContext)
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.lib.model_registry import LADMColModelRegistry
from asistente_ladm_col.utils.qt_utils import OverrideCursor
from asistente_ladm_col.utils.utils import Utils

"""
Decorators to ensure requirements before calling a plugin method.

****************************************  WARNING  *************************************************

If you're adding a decorator to a method, make sure the call to the method complies with the
required parameters of the decorator. For instance, if I add a decorator @_db_connection_required
to my_method(), I need to be sure that ALL calls to my_method() are like this:

   my_action.connect(partial(my_method, context_collected))

If you don't do that, Python errors are likely to appear when the decorator @_db_connection_required
for my_method() is called.

Note that add-ons don't pass an AsistenteLADMCOLPlugin object as first argument. However, the LADM-
COL Assistant is gentle enough to go and search in the ladmcol variable member for a proper object!
****************************************************************************************************
"""


def db_connection_required(func_to_decorate):
    @wraps(func_to_decorate)
    def decorated_function(*args, **kwargs):
        """
        For all db_source in the context check:
        1. that db connection is valid, otherwise show message with button that opens db connection setting dialog.
        2. that db connection parameters are equal to db source connection parameters (in QSettings), otherwise show
           message with two buttons "Use DB from QSettings" and "Use the current connection".
        """
        # Check if current connection is valid and disable access if not
        inst = args[0] if type(args[0]).__name__ == 'AsistenteLADMCOLPlugin' else args[0].ladmcol
        context = args[1]
        db_connections_in_conflict = list()
        invalid_db_connections = list()

        for db_source in context.get_db_sources():
            db = inst.conn_manager.get_db_connector_from_source(db_source)
            qsettings_db = inst.conn_manager.get_db_connection_from_qsettings(db_source)

            if db.equals(qsettings_db):
                res, code, msg = db.test_connection()
                if not res:
                    invalid_db_connections.append(db_source)
                    widget = inst.iface.messageBar().createMessage("Asistente LADM-COL",
                                                                QCoreApplication.translate("AsistenteLADMCOLPlugin",
                                                                                            "The {} DB connection is not valid. Details: {}").format(Tr.tr_db_source(db_source), msg))
                    button = QPushButton(widget)
                    button.setText(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Settings"))

                    settings_context = SettingsContext(db_source)
                    settings_context.title = QCoreApplication.translate("AsistenteLADMCOLPlugin", "{} Connection Settings").format(Tr.tr_db_source(db_source))
                    settings_context.tip = QCoreApplication.translate("AsistenteLADMCOLPlugin", "Configure a valid DB connection for {} source.").format(Tr.tr_db_source(db_source))
                    settings_context.tab_pages_list = [SETTINGS_CONNECTION_TAB_INDEX]
                    button.pressed.connect(partial(inst.show_settings_clear_message_bar, settings_context))

                    widget.layout().addWidget(button)
                    inst.iface.messageBar().pushWidget(widget, Qgis.Warning, 15)
                    inst.logger.warning(__name__, QCoreApplication.translate("AsistenteLADMCOLPlugin",
                        "A dialog/tool couldn't be opened/executed, connection to DB was not valid."))
                else:
                    # Update cache if there is none and source is Collected
                    if db_source == COLLECTED_DB_SOURCE:
                        if not inst.app.core.get_cached_layers() and not inst.app.core.get_cached_relations():
                            inst.app.core.cache_layers_and_relations(db, ladm_col_db=True, db_source=None)
            else:
                db_connections_in_conflict.append(db_source)
                msg = QCoreApplication.translate("AsistenteLADMCOLPlugin",
                                                 "Your current {} DB does not match with the one registered in QSettings. Which connection would you like to use?").format(Tr.tr_db_source(db_source))

                widget = inst.iface.messageBar().createMessage("Asistente LADM-COL", msg)
                btn_current_connection = QPushButton(widget)
                btn_current_connection.setText(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Use the current connection"))
                btn_current_connection.pressed.connect(partial(inst.use_current_db_connection, db_source))

                btn_update_connection = QPushButton(widget)
                btn_update_connection.setText(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Use DB from QSettings"))
                btn_update_connection.pressed.connect(partial(inst.update_db_connection_from_qsettings, db_source))

                widget.layout().addWidget(btn_current_connection)
                widget.layout().addWidget(btn_update_connection)

                inst.iface.messageBar().pushWidget(widget, Qgis.Warning)
                inst.logger.warning(__name__, msg)

        if db_connections_in_conflict or invalid_db_connections:
            return  # If any db connection changed or it's invalid, we don't return the decorated function
        else:
            func_to_decorate(*args, **kwargs)

    return decorated_function


def activate_processing_plugin(func_to_decorate):
    @wraps(func_to_decorate)
    def decorated_function(*args, **kwargs):

        if not isPluginLoaded("processing"):
            loadPlugin('processing')
            startPlugin('processing')
            msg = QCoreApplication.translate("AsistenteLADMCOLPlugin", "The processing plugin has been activated!")
            Logger().info(__name__, msg)

            # Check in the plugin manager that the processing plugin was activated
            QSettings().setValue("PythonPlugins/processing", True)

        return func_to_decorate(*args, **kwargs)

    return decorated_function


def _log_quality_rule_validations(func_to_decorate):
    @wraps(func_to_decorate)
    def add_format_to_text(self, rule, layers, options):
        """
        Decorator used for registering log quality info
        :param self: QualityRuleEngine instance
        :param rule: Quality rule instance
        :param layers: layers
        :param options: Options for the quality rule
        """
        self.qr_logger.set_initial_progress_emitted.emit(rule.name())
        log_text_content = LOG_QUALITY_LIST_CONTAINER_OPEN

        start_time = time.time()
        with OverrideCursor(Qt.WaitCursor):
            qr_result = func_to_decorate(self, rule, layers, options)
        end_time = time.time()

        if qr_result.level == EnumQualityRuleResult.ERRORS:
            prefix = LOG_QUALITY_LIST_ITEM_ERROR_OPEN
            suffix = LOG_QUALITY_LIST_ITEM_ERROR_CLOSE
        elif qr_result.level == EnumQualityRuleResult.SUCCESS:
            prefix = LOG_QUALITY_LIST_ITEM_SUCCESS_OPEN
            suffix = LOG_QUALITY_LIST_ITEM_SUCCESS_CLOSE
        elif qr_result.level == EnumQualityRuleResult.CRITICAL:
            prefix = LOG_QUALITY_LIST_ITEM_CRITICAL_OPEN
            suffix = LOG_QUALITY_LIST_ITEM_CRITICAL_CLOSE
        else:  # EnumQualityRuleResult.UNDEFINED
            prefix = LOG_QUALITY_LIST_ITEM_OPEN
            suffix = LOG_QUALITY_LIST_ITEM_CLOSE

        log_text_content += "{}{}{}".format(prefix, qr_result.msg, suffix)

        self.qr_logger.log_total_time = self.qr_logger.log_total_time + (end_time - start_time)

        log_text_content += LOG_QUALITY_LIST_CONTAINER_CLOSE
        log_text_content += LOG_QUALITY_CONTENT_SEPARATOR

        self.qr_logger.log_text += "{}{} [{}]{}".format(LOG_QUALITY_PREFIX_TOPOLOGICAL_RULE_TITLE,
                                                        rule.name(), Utils().set_time_format(end_time - start_time), LOG_QUALITY_SUFFIX_TOPOLOGICAL_RULE_TITLE)

        if options:
            # Try to get option titles instead of keys
            option_texts = list()
            for k, v in options.items():
                obj = rule.options.get_options().get(k, None)
                option_texts.append("{}: {}".format(obj.title() if obj else k, v))

            self.qr_logger.log_text += "{}{} {}{}".format(LOG_QUALITY_OPTIONS_OPEN,
                                                          QCoreApplication.translate("QualityRules", "(Options)"),
                                                          "; ".join(option_texts),
                                                          LOG_QUALITY_OPTIONS_CLOSE)

        self.qr_logger.log_text += log_text_content

        self.qr_logger.set_final_progress_emitted.emit(rule.name())

        return qr_result

    return add_format_to_text


def survey_model_required(func_to_decorate):
    """Requires list of sources. Example: [COLLECTED_DB_SOURCE, SUPPLIES_DB_SOURCE]"""
    @wraps(func_to_decorate)
    def decorated_function(*args, **kwargs):
        inst = args[0] if type(args[0]).__name__ == 'AsistenteLADMCOLPlugin' else args[0].ladmcol
        context = args[1]

        for db_source in context.get_db_sources():
            db = inst.conn_manager.get_db_connector_from_source(db_source=db_source)
            db.test_connection()
        
            if not db.survey_model_exists():
                widget = inst.iface.messageBar().createMessage("Asistente LADM-COL",
                                                            QCoreApplication.translate("AsistenteLADMCOLPlugin",
                                                                                        "Check your {} database connection. The '{} {}' model is required for this functionality, but could not be found in your current database. Click the button to go to Settings.").format(
                                                                Tr.tr_db_source(db_source),
                                                                LADMColModelRegistry().model(LADMNames.SURVEY_MODEL_KEY).alias(),
                                                                LADMColModelRegistry().model(LADMNames.SURVEY_MODEL_KEY).supported_version()))
                button = QPushButton(widget)
                button.setText(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Settings"))

                settings_context = SettingsContext(db_source)
                settings_context.required_models = [LADMNames.SURVEY_MODEL_KEY]
                settings_context.tab_pages_list = [SETTINGS_CONNECTION_TAB_INDEX]
                settings_context.title = QCoreApplication.translate("SettingsDialog", "{} Connection Settings").format(Tr.tr_db_source(db_source))
                settings_context.tip = QCoreApplication.translate("SettingsDialog", "Set a DB connection with the '{}' model.").format(LADMColModelRegistry().model(LADMNames.SURVEY_MODEL_KEY).alias())
                button.pressed.connect(partial(inst.show_settings_clear_message_bar, settings_context))

                widget.layout().addWidget(button)
                inst.iface.messageBar().pushWidget(widget, Qgis.Warning, 15)
                inst.logger.warning(__name__, QCoreApplication.translate("AsistenteLADMCOLPlugin",
                    "A dialog/tool couldn't be opened/executed, connection to DB was not valid."))
                return

        func_to_decorate(*args, **kwargs)

    return decorated_function


def supplies_model_required(func_to_decorate):
    @wraps(func_to_decorate)
    def decorated_function(*args, **kwargs):
        inst = args[0] if type(args[0]).__name__ == 'AsistenteLADMCOLPlugin' else args[0].ladmcol
        context = args[1]

        for db_source in context.get_db_sources():
            db = inst.conn_manager.get_db_connector_from_source(db_source=db_source)
            db.test_connection()
            if not db.supplies_model_exists():
                widget = inst.iface.messageBar().createMessage("Asistente LADM-COL",
                                                            QCoreApplication.translate("AsistenteLADMCOLPlugin",
                                                                                        "Check your {} database connection. The '{} {}' model is required for this functionality, but could not be found in your current database. Click the button to go to Settings.").format(
                                                                Tr.tr_db_source(db_source),
                                                                LADMColModelRegistry().model(LADMNames.SUPPLIES_MODEL_KEY).alias(),
                                                                LADMColModelRegistry().model(LADMNames.SUPPLIES_MODEL_KEY).supported_version()))
                button = QPushButton(widget)
                button.setText(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Settings"))

                settings_context = SettingsContext(db_source)
                settings_context.required_models = [LADMNames.SUPPLIES_MODEL_KEY]
                settings_context.tab_pages_list = [SETTINGS_CONNECTION_TAB_INDEX]
                settings_context.title = QCoreApplication.translate("SettingsDialog", "{} Connection Settings").format(Tr.tr_db_source(db_source))
                settings_context.tip = QCoreApplication.translate("SettingsDialog", "Set a DB connection with the '{}' model.").format(
                    LADMColModelRegistry().model(LADMNames.SUPPLIES_MODEL_KEY).alias())
                button.pressed.connect(partial(inst.show_settings_clear_message_bar, settings_context))

                widget.layout().addWidget(button)
                inst.iface.messageBar().pushWidget(widget, Qgis.Warning, 15)
                inst.logger.warning(__name__, QCoreApplication.translate("AsistenteLADMCOLPlugin",
                    "A dialog/tool couldn't be opened/executed, connection to DB was not valid."))
                return
        
        func_to_decorate(*args, **kwargs)

    return decorated_function


# TODO: Unify all model required decorators into one with model_key as argument
def field_data_capture_model_required(func_to_decorate):
    """Requires list of sources. Example: [COLLECTED_DB_SOURCE, SUPPLIES_DB_SOURCE]"""
    @wraps(func_to_decorate)
    def decorated_function(*args, **kwargs):
        inst = args[0] if type(args[0]).__name__ == 'AsistenteLADMCOLPlugin' else args[0].ladmcol
        context = args[1]
        model_key = LADMNames.FIELD_DATA_CAPTURE_MODEL_KEY

        for db_source in context.get_db_sources():
            db = inst.conn_manager.get_db_connector_from_source(db_source=db_source)
            db.test_connection()
            if not db.ladm_col_model_exists(model_key):
                widget = inst.iface.messageBar().createMessage("Asistente LADM-COL",
                                                               QCoreApplication.translate("AsistenteLADMCOLPlugin",
                                                                                          "Check your {} database connection. The '{} {}' model is required for this functionality, but could not be found in your current database. Click the button to go to Settings.").format(
                                                                   Tr.tr_db_source(db_source),
                                                                   LADMColModelRegistry().model(model_key).alias(),
                                                                   LADMColModelRegistry().model(model_key).supported_version()))
                button = QPushButton(widget)
                button.setText(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Settings"))

                settings_context = SettingsContext(db_source)
                settings_context.required_models = [model_key]
                settings_context.tab_pages_list = [SETTINGS_CONNECTION_TAB_INDEX]
                settings_context.title = QCoreApplication.translate("SettingsDialog", "{} Connection Settings").format(
                    Tr.tr_db_source(db_source))
                settings_context.tip = QCoreApplication.translate("SettingsDialog",
                                                                  "Set a DB connection with the '{}' model.").format(
                    LADMColModelRegistry().model(model_key).alias())
                button.pressed.connect(partial(inst.show_settings_clear_message_bar, settings_context))

                widget.layout().addWidget(button)
                inst.iface.messageBar().pushWidget(widget, Qgis.Warning, 15)
                inst.logger.warning(__name__, QCoreApplication.translate("AsistenteLADMCOLPlugin",
                                                                         "A dialog/tool couldn't be opened/executed, connection to DB was not valid."))
                return

        func_to_decorate(*args, **kwargs)

    return decorated_function


def valuation_model_required(func_to_decorate):
    @wraps(func_to_decorate)
    def decorated_function(*args, **kwargs):
        inst = args[0] if type(args[0]).__name__ == 'AsistenteLADMCOLPlugin' else args[0].ladmcol
        context = args[1]

        for db_source in context.get_db_sources():
            db = inst.get_db_connector_from_source(db_source=db_source)
            db.test_connection()

        if not db.valuation_model_exists():
            widget = inst.iface.messageBar().createMessage("Asistente LADM-COL",
                                                           QCoreApplication.translate("AsistenteLADMCOLPlugin",
                                                                                      "Check your {} database connection. The '{} {}' model is required for this functionality, but could not be found in your current database. Click the button to go to Settings.").format(
                                                               Tr.tr_db_source(db_source),
                                                               LADMColModelRegistry().model(LADMNames.VALUATION_MODEL_KEY).alias(),
                                                               LADMColModelRegistry().model(LADMNames.VALUATION_MODEL_KEY).supported_version()))
            button = QPushButton(widget)
            button.setText(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Settings"))

            settings_context = SettingsContext(db_source)
            settings_context.required_models = [LADMNames.VALUATION_MODEL_KEY]
            settings_context.tab_pages_list = [SETTINGS_CONNECTION_TAB_INDEX]
            settings_context.title = QCoreApplication.translate("SettingsDialog", "{} Connection Settings").format(Tr.tr_db_source(db_source))
            settings_context.tip = QCoreApplication.translate("SettingsDialog", "Set a DB connection with the '{}' model.").format(
                LADMColModelRegistry().model(LADMNames.SURVEY_MODEL_KEY).alias())
            button.pressed.connect(partial(inst.show_settings_clear_message_bar, settings_context))

            widget.layout().addWidget(button)
            inst.iface.messageBar().pushWidget(widget, Qgis.Warning, 15)
            inst.logger.warning(__name__, QCoreApplication.translate("AsistenteLADMCOLPlugin",
                "A dialog/tool couldn't be opened/executed, connection to DB was not valid."))
            return

        func_to_decorate(*args, **kwargs)

    return decorated_function


# TODO: Unify all model required decorators into one with model_key as argument
def cadastral_cartography_model_required(func_to_decorate):
    """Requires list of sources. Example: [COLLECTED_DB_SOURCE, SUPPLIES_DB_SOURCE]"""

    @wraps(func_to_decorate)
    def decorated_function(*args, **kwargs):
        inst = args[0] if type(args[0]).__name__ == 'AsistenteLADMCOLPlugin' else args[0].ladmcol
        context = args[1]

        for db_source in context.get_db_sources():
            db = inst.conn_manager.get_db_connector_from_source(db_source=db_source)
            db.test_connection()
            if not db.cadastral_cartography_model_exists():
                widget = inst.iface.messageBar().createMessage("Asistente LADM-COL",
                                                               QCoreApplication.translate("AsistenteLADMCOLPlugin",
                                                                                          "Check your {} database connection. The '{} {}' model is required for this functionality, but could not be found in your current database. Click the button to go to Settings.").format(
                                                                   Tr.tr_db_source(db_source),
                                                                   LADMColModelRegistry().model(
                                                                       LADMNames.CADASTRAL_CARTOGRAPHY_MODEL_KEY).alias(),
                                                                   LADMColModelRegistry().model(
                                                                       LADMNames.CADASTRAL_CARTOGRAPHY_MODEL_KEY).alias()
                                                               ))
                button = QPushButton(widget)
                button.setText(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Settings"))

                settings_context = SettingsContext(db_source)
                settings_context.required_models = [LADMNames.CADASTRAL_CARTOGRAPHY_MODEL_KEY]
                settings_context.tab_pages_list = [SETTINGS_CONNECTION_TAB_INDEX]
                settings_context.title = QCoreApplication.translate("SettingsDialog", "{} Connection Settings").format(
                    Tr.tr_db_source(db_source))
                settings_context.tip = QCoreApplication.translate("SettingsDialog",
                                                                  "Set a DB connection with the '{}' model.").format(
                    LADMColModelRegistry().model(LADMNames.CADASTRAL_CARTOGRAPHY_MODEL_KEY).alias())
                button.pressed.connect(partial(inst.show_settings_clear_message_bar, settings_context))

                widget.layout().addWidget(button)
                inst.iface.messageBar().pushWidget(widget, Qgis.Warning, 15)
                inst.logger.warning(__name__, QCoreApplication.translate("AsistenteLADMCOLPlugin",
                                                                         "A dialog/tool couldn't be opened/executed, connection to DB was not valid."))
                return

        func_to_decorate(*args, **kwargs)

    return decorated_function


def map_swipe_tool_required(func_to_decorate):
    @wraps(func_to_decorate)
    def decorated_function(*args, **kwargs):
        inst = args[0] if type(args[0]).__name__ == 'AsistenteLADMCOLPlugin' else args[0].ladmcol
        # Check if Map Swipe Tool is installed and active, disable access if not
        if inst.mst_plugin.check_if_dependency_is_valid():
            func_to_decorate(*args, **kwargs)
        else:
            if MAP_SWIPE_TOOL_REQUIRED_VERSION_URL:
                # If we depend on a specific version of Map Swipe Tool (only on that one)
                # and it is not the latest version, show a download link
                msg = QCoreApplication.translate("AsistenteLADMCOLPlugin",
                                                 "The plugin 'MapSwipe Tool' version {} is required, but couldn't be found. Click the button to install it.").format(
                                                    MAP_SWIPE_TOOL_MIN_REQUIRED_VERSION)

                widget = inst.iface.messageBar().createMessage("Asistente LADM-COL", msg)
                button = QPushButton(widget)
                button.setText(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Install plugin"))
                button.pressed.connect(inst.mst_plugin.install)
                widget.layout().addWidget(button)
                inst.iface.messageBar().pushWidget(widget, Qgis.Warning, 20)
            else:  # Shouldn't be necessary because QGIS handles official plugin dependencies
                msg = QCoreApplication.translate("AsistenteLADMCOLPlugin", "The plugin 'MapSwipe Tool' version {} {}is required, but couldn't be found. Click the button to show the Plugin Manager.").format(MAP_SWIPE_TOOL_MIN_REQUIRED_VERSION, '' if MAP_SWIPE_TOOL_EXACT_REQUIRED_VERSION else '(or higher) ')

                widget = inst.iface.messageBar().createMessage("Asistente LADM-COL", msg)
                button = QPushButton(widget)
                button.setText(QCoreApplication.translate("AsistenteLADMCOLPlugin", "Plugin Manager"))
                button.pressed.connect(inst.show_plugin_manager)
                widget.layout().addWidget(button)
                inst.iface.messageBar().pushWidget(widget, Qgis.Warning, 15)

            inst.logger.warning(__name__,  QCoreApplication.translate("AsistenteLADMCOLPlugin",
                "A dialog/tool couldn't be opened/executed, MapSwipe Tool not found."))

    return decorated_function


def invisible_layers_and_groups_required(func_to_decorate):
    @wraps(func_to_decorate)
    def decorated_function(*args, **kwargs):
        inst = args[0] if type(args[0]).__name__ == 'AsistenteLADMCOLPlugin' else args[0].ladmcol

        # Check if Invisible Layers and Groups is installed and active, install it if necessary
        if not inst.ilg_plugin.check_if_dependency_is_valid():
            loop = QEventLoop()  # Do the installation synchronously
            inst.ilg_plugin.download_dependency_completed.connect(loop.exit)
            inst.ilg_plugin.install()
            inst.logger.info(__name__, "Installing dependency ({} {})...".format(INVISIBLE_LAYERS_AND_GROUPS_PLUGIN_NAME,
                                                                                 INVISIBLE_LAYERS_AND_GROUPS_MIN_REQUIRED_VERSION))
            loop.exec()

        func_to_decorate(*args, **kwargs)

    return decorated_function


def validate_if_wizard_is_open(func_to_decorate):
    @wraps(func_to_decorate)
    def decorated_function(*args, **kwargs):
        inst = args[0] if type(args[0]).__name__ == 'AsistenteLADMCOLPlugin' else args[0].ladmcol
        if inst.is_wizard_open:
            inst.show_message_with_close_wizard_button(QCoreApplication.translate("AsistenteLADMCOLPlugin",
                                                         "There is a wizard open, you need to close it before continuing with another tool."),
                                                       QCoreApplication.translate("AsistenteLADMCOLPlugin",
                                                                                  "Close the open wizard"),
                                                       Qgis.Info)
        else:
             func_to_decorate(*args, **kwargs)

    return decorated_function


def validate_if_layers_in_editing_mode_with_changes(func_to_decorate):
    @wraps(func_to_decorate)
    def decorated_function(*args, **kwargs):
        inst = args[0] if type(args[0]).__name__ == 'AsistenteLADMCOLPlugin' else args[0].ladmcol
        layers_modified = inst.app.core.get_ladm_layers_in_edit_mode_with_edit_buffer_is_modified(inst.get_db_connection())
        layers_names = [layer.name() for layer in layers_modified]
        if layers_modified:
            inst.app.gui.show_message(QCoreApplication.translate("AsistenteLADMCOLPlugin",
                                                         "The action could not be executed because {} layer(s) is/are in editing session. Please finish editing session before trying to execute the action again.").format(', '.join(layers_names)),
                              Qgis.Info)
        else:
            func_to_decorate(*args, **kwargs)

    return decorated_function


def update_context_to_current_role(func_to_decorate):
    """
    Requires list of sources. Example: [COLLECTED_DB_SOURCE, SUPPLIES_DB_SOURCE].

    We suggest you to call this decorator at an early stage (the farther you can from the function signature), so that
    other decorators can use the updated context for their own validations.
    """

    @wraps(func_to_decorate)
    def decorated_function(*args, **kwargs):
        inst = args[0] if type(args[0]).__name__ == 'AsistenteLADMCOLPlugin' else args[0].ladmcol
        context = args[1]

        # TaskContext has prevalence, it is the more specific functionality
        # we have in this plugin, so we don't update its context
        if not isinstance(context, TaskContext):
            role_key = inst.role_registry.get_active_role()
            role_db_source = inst.role_registry.get_role_db_source(role_key)
            if role_db_source:
                inst.logger.debug(__name__, "Updating context for role '{}' to '{}'.".format(role_key, role_db_source))
                # Now, create a copy of context, update the copy and assign it as new parameter (hint: args is a tuple)
                new_context = deepcopy(context)
                new_context.set_db_sources([role_db_source])
                largs = list(args)
                largs[1] = new_context
                args = tuple(largs)

        func_to_decorate(*args, **kwargs)

    return decorated_function


def with_override_cursor(func_to_decorate):
    @wraps(func_to_decorate)
    def decorated_function(*args, **kwargs):

        with OverrideCursor(Qt.WaitCursor):
            return func_to_decorate(*args, **kwargs)

    return decorated_function


def qgis_gui_only(func_to_decorate):

    @wraps(func_to_decorate)
    def decorated_function(*args, **kwargs):
        """
        Avoid executing the decorated function if we are not in GUI mode.

        To be used on functions that are to be run only in QGIS GUI.

        Note: inst should be plugin's instance or at least have access to app member.
        """
        inst = args[0] if type(args[0]).__name__ == 'AsistenteLADMCOLPlugin' else args[0].ladmcol

        if inst.app.settings.with_gui:
            func_to_decorate(*args, **kwargs)

    return decorated_function
