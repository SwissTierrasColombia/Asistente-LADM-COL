from qgis.PyQt.QtCore import (QObject,
                              QCoreApplication)

from asistente_ladm_col.config.general_config import (SUPPLIES_DB_SOURCE,
                                                      COLLECTED_DB_SOURCE)
from asistente_ladm_col.config.gui.common_keys import ACTION_RUN_ETL_SUPPLIES
from asistente_ladm_col.config.ladm_names import LADMNames
from asistente_ladm_col.config.enums import (EnumSTStepType,
                                             EnumUserLevel)
from asistente_ladm_col.config.transitional_system_config import TransitionalSystemConfig
from asistente_ladm_col.lib.context import TaskContext
from asistente_ladm_col.utils.singleton import SingletonQObject

SLOT_NAME = "SLOT_NAME"
SLOT_CONTEXT = "SLOT_CONTEXT"
SLOT_PARAMS = "SLOT_PARAMS"
STEP_NUMBER = "STEP_NUMBER"
STEP_NAME = "STEP_NAME"
STEP_TYPE = "STEP_TYPE"
STEP_DESCRIPTION = "STEP_DESCRIPTION"
STEP_ACTION = "STEP_ACTION"
STEP_CUSTOM_ACTION_SLOT = "STEP_CUSTOM_ACTION_SLOT"
STEP_OPTIONAL = "STEP_OPTIONAL"


class TaskStepsConfig(QObject, metaclass=SingletonQObject):
    def __init__(self):
        QObject.__init__(self)

        self._slot_caller = None

        self._st_config = TransitionalSystemConfig()

    def set_slot_caller(self, slot_caller):
        self._slot_caller = slot_caller

    def get_steps_config(self, task):
        """
        Gets the configuration of the steps of a task. Each step has its own configuration and is linked either to an
        existing action call from the plugin or to a custom action call (i.e., passing custom parameters) from the
        plugin.

        :param task: STTask object
        :return: List of steps data. Each step data is a dict, which has these mandatory keys:
                    STEP_NUMBER,
                    STEP_NAME,
                    STEP_TYPE,
                    either STEP_ACTION or STEP_CUSTOM_ACTION_SLOT (a dict with SLOT_NAME and SLOT_PARAMS keys, and
                    optionally SLOT_CONTEXT key)
                and these optional keys:
                    STEP_DESCRIPTION
        """
        task_type = task.get_type()
        task_data = task.get_data()

        steps_config = []
        if task_type == self._st_config.TASK_GENERATE_CADASTRAL_SUPPLIES:
            steps_config = [
                {STEP_NUMBER: 1,
                 STEP_NAME: QCoreApplication.translate("TaskStepsConfig", "Create supplies structure in DB"),
                 STEP_TYPE: EnumSTStepType.SCHEMA_IMPORT,
                 STEP_DESCRIPTION: QCoreApplication.translate("TaskStepsConfig",
                                                              "Choose a DB connection to create there the Supplies model structure."),
                 STEP_CUSTOM_ACTION_SLOT: {
                     SLOT_NAME: self._slot_caller.show_dlg_import_schema,
                     SLOT_CONTEXT: TaskContext([SUPPLIES_DB_SOURCE]),
                     SLOT_PARAMS: {'link_to_import_data': False,
                                   'selected_models': [LADMNames.SUPPLIES_MODEL_KEY]}}
                 },
                {STEP_NUMBER: 2,
                 STEP_NAME: QCoreApplication.translate("TaskStepsConfig", "Run supplies ETL"),
                 STEP_TYPE: EnumSTStepType.RUN_ETL_COBOL,
                 STEP_DESCRIPTION: QCoreApplication.translate("TaskStepsConfig",
                                                              "Migrate SNC or Cobol data to the LADM-COL (supplies model)."),
                 STEP_CUSTOM_ACTION_SLOT: {
                     SLOT_NAME: self._slot_caller.show_wiz_supplies_etl,
                     SLOT_CONTEXT: TaskContext([SUPPLIES_DB_SOURCE]),
                     SLOT_PARAMS: {}}
                 },
                {STEP_NUMBER: 3,
                 STEP_NAME: QCoreApplication.translate("TaskStepsConfig", "Generate XTF"),
                 STEP_TYPE: EnumSTStepType.EXPORT_DATA,
                 STEP_DESCRIPTION: QCoreApplication.translate("TaskStepsConfig", "Export the data from the DB to a transfer file (.xtf)."),
                 STEP_CUSTOM_ACTION_SLOT: {
                     SLOT_NAME: self._slot_caller.show_dlg_export_data,
                     SLOT_CONTEXT: TaskContext([SUPPLIES_DB_SOURCE]),
                     SLOT_PARAMS: {}}
                 },
                {STEP_NUMBER: 4,
                 STEP_OPTIONAL: True,
                 STEP_NAME: QCoreApplication.translate("TaskStepsConfig", "Generate report (COBOL)"),
                 STEP_TYPE: EnumSTStepType.RUN_OMISSIONS_COMMISSIONS_REPORT_COBOL,
                 STEP_DESCRIPTION: QCoreApplication.translate("TaskStepsConfig",
                                                              "Generate omissions and commissions report (COBOL)."),
                 STEP_CUSTOM_ACTION_SLOT: {
                     SLOT_NAME: self._slot_caller.show_missing_cobol_supplies_dialog,
                     SLOT_CONTEXT: TaskContext([SUPPLIES_DB_SOURCE]),
                     SLOT_PARAMS: {}}
                 },
                {STEP_NUMBER: 5,
                 STEP_OPTIONAL: True,
                 STEP_NAME: QCoreApplication.translate("TaskStepsConfig", "Generate report (SNC)"),
                 STEP_TYPE: EnumSTStepType.RUN_OMISSIONS_COMMISSIONS_REPORT_SNC,
                 STEP_DESCRIPTION: QCoreApplication.translate("TaskStepsConfig",
                                                              "Generate omissions and commissions report (SNC)."),
                 STEP_CUSTOM_ACTION_SLOT: {
                     SLOT_NAME: self._slot_caller.show_missing_snc_supplies_dialog,
                     SLOT_CONTEXT: TaskContext([SUPPLIES_DB_SOURCE]),
                     SLOT_PARAMS: {}}
                 },
                {STEP_NUMBER: 6,
                 STEP_NAME: QCoreApplication.translate("TaskStepsConfig", "Upload XTF (and optionally, report files)"),
                 STEP_TYPE: EnumSTStepType.UPLOAD_FILE,
                 STEP_DESCRIPTION: QCoreApplication.translate("TaskStepsConfig", "Upload the XTF file (and optionally, report files) to the Transitional System."),
                 STEP_CUSTOM_ACTION_SLOT: {
                     SLOT_NAME: self._slot_caller.show_dlg_st_upload_file,
                     SLOT_CONTEXT: TaskContext([SUPPLIES_DB_SOURCE]),
                     SLOT_PARAMS: {
                         'request_id': task_data['request']['requestId'] if 'request' in task_data else None,
                         'other_params' : {'typeSupplyId': task_data['request'][
                             'typeSupplyId'] if 'request' in task_data else None},
                         'task_type': task_type}}
                 }]
        elif task_type == self._st_config.TASK_INTEGRATE_SUPPLIES:
            steps_config = [
                {STEP_NUMBER: 1,
                 STEP_NAME: QCoreApplication.translate("TaskStepsConfig", "Connect to remote DB"),
                 STEP_TYPE: EnumSTStepType.CONNECT_TO_DB,
                 STEP_DESCRIPTION: QCoreApplication.translate("TaskStepsConfig",
                                                              "Establish and test the connection to a remote DB, which will be used to integrate data in an assisted manner."),
                 STEP_CUSTOM_ACTION_SLOT: {
                     SLOT_NAME: self._slot_caller.open_encrypted_db_connection,
                     SLOT_PARAMS: {'db_engine': 'pg',
                                   'conn_dict': task_data['connection'] if 'connection' in task_data else {},
                                   'user_level': EnumUserLevel.CONNECT}},
                },
                {STEP_NUMBER: 2,
                 STEP_NAME: QCoreApplication.translate("TaskStepsConfig",
                                                       "Explore data from Cadastre and Land Registry"),
                 STEP_TYPE: EnumSTStepType.CONNECT_TO_DB,
                 STEP_DESCRIPTION: QCoreApplication.translate("TaskStepsConfig", "Load parcel data from cadastre and registry into QGIS."),
                 STEP_CUSTOM_ACTION_SLOT: {
                     SLOT_NAME: self._slot_caller.task_step_explore_data_cadastre_registry,
                     SLOT_PARAMS: {'db_engine': 'pg',
                                   'conn_dict': task_data['connection'] if 'connection' in task_data else {},
                                   'user_level': EnumUserLevel.CONNECT}},
                 },
                {STEP_NUMBER: 3,
                 STEP_NAME: QCoreApplication.translate("TaskStepsConfig", "Start assisted integration"),
                 STEP_TYPE: EnumSTStepType.CONNECT_TO_DB,
                 STEP_ACTION: ACTION_RUN_ETL_SUPPLIES,  # TODO: functionality to integrate in assisted manner
                 STEP_DESCRIPTION: "Not implemented yet."
                 }]
        elif task_type == self._st_config.TASK_VALIDATE_QUALITY_RULES:
            steps_config = [
                {STEP_NUMBER: 1,
                 STEP_NAME: QCoreApplication.translate("TaskStepsConfig", "Create cadastral survey structure in DB"),
                 STEP_TYPE: EnumSTStepType.SCHEMA_IMPORT,
                 STEP_DESCRIPTION: QCoreApplication.translate("TaskStepsConfig",
                                                              "Choose a DB connection to create there the Cadastral Survey model structure."),
                 STEP_CUSTOM_ACTION_SLOT: {
                     SLOT_NAME: self._slot_caller.show_dlg_import_schema,
                     SLOT_CONTEXT: TaskContext([COLLECTED_DB_SOURCE]),
                     SLOT_PARAMS: {'link_to_import_data': False,
                                   'selected_models': [LADMNames.SURVEY_MODEL_KEY]}}
                 },
                {STEP_NUMBER: 2,
                 STEP_NAME: QCoreApplication.translate("TaskStepsConfig", "Import XTF data"),
                 STEP_TYPE: EnumSTStepType.IMPORT_DATA,
                 STEP_DESCRIPTION: QCoreApplication.translate("TaskStepsConfig",
                                                              "Import the assigned XTF data."),
                 STEP_CUSTOM_ACTION_SLOT: {
                     SLOT_NAME: self._slot_caller.show_dlg_import_data,
                     SLOT_CONTEXT: TaskContext([COLLECTED_DB_SOURCE]),
                     SLOT_PARAMS: {}}
                 },
                {STEP_NUMBER: 3,
                 STEP_NAME: QCoreApplication.translate("TaskStepsConfig", "Validate Quality Rules"),
                 STEP_TYPE: EnumSTStepType.VALIDATE_QUALITY_RULES,
                 STEP_DESCRIPTION: QCoreApplication.translate("TaskStepsConfig", "Validate Quality Rules on the assigned data."),
                 STEP_CUSTOM_ACTION_SLOT: {
                     SLOT_NAME: self._slot_caller.show_dlg_quality,
                     SLOT_CONTEXT: TaskContext([COLLECTED_DB_SOURCE]),
                     SLOT_PARAMS: {}}
                 },
                {STEP_NUMBER: 4,
                 STEP_NAME: QCoreApplication.translate("TaskStepsConfig", "Upload validation report files"),
                 STEP_TYPE: EnumSTStepType.UPLOAD_FILE,
                 STEP_DESCRIPTION: QCoreApplication.translate("TaskStepsConfig", "Upload the report (PDF) file and optionally, a GeoPackage to the Transitional System."),
                 STEP_CUSTOM_ACTION_SLOT: {
                     SLOT_NAME: self._slot_caller.show_dlg_st_upload_file,
                     SLOT_CONTEXT: TaskContext([COLLECTED_DB_SOURCE]),
                     SLOT_PARAMS: {
                         'request_id': task_data['request']['requestId'] if 'request' in task_data else None,
                         'other_params': {'typeSupplyId': task_data['request'][
                             'typeSupplyId'] if 'request' in task_data else None},
                         'task_type': task_type}}
                 }]

        return steps_config

