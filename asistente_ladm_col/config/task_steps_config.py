from qgis.PyQt.QtCore import (QObject,
                              QCoreApplication)

from asistente_ladm_col.config.general_config import SUPPLIES_DB_SOURCE
from asistente_ladm_col.config.gui.common_keys import (ACTION_SCHEMA_IMPORT_SUPPLIES,
                                                       ACTION_RUN_ETL_COBOL,
                                                       ACTION_EXPORT_DATA_SUPPLIES,
                                                       ACTION_ST_UPLOAD_XTF)
from asistente_ladm_col.config.mapping_config import LADMNames
from asistente_ladm_col.config.enums import (STStepTypeEnum,
                                             EnumUserLevel)
from asistente_ladm_col.utils.singleton import SingletonQObject

TASK_INTEGRATE_SUPPLIES = 1
TASK_GENERATE_CADASTRAL_SUPPLIES = 2
SLOT_NAME = "SLOT_NAME"
SLOT_PARAMS = "SLOT_PARAMS"
STEP_NUMBER = "STEP_NUMBER"
STEP_NAME = "STEP_NAME"
STEP_TYPE = "STEP_TYPE"
STEP_DESCRIPTION = "STEP_DESCRIPTION"
STEP_ACTION = "STEP_ACTION"
STEP_CUSTOM_ACTION_SLOT = "STEP_CUSTOM_ACTION_SLOT"


class TaskStepsConfig(QObject, metaclass=SingletonQObject):
    def __init__(self):
        QObject.__init__(self)

        self._slot_caller = None

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
                    either STEP_ACTION or STEP_CUSTOM_ACTION_SLOT (a dict with SLOT_NAME and SLOT_PARAMS keys)
                and these optional keys:
                    STEP_DESCRIPTION
        """
        task_type = task.get_type()
        task_data = task.get_data()

        steps_config = []
        if task_type == TASK_GENERATE_CADASTRAL_SUPPLIES:
            steps_config = [
                {STEP_NUMBER: 1,
                 STEP_NAME: QCoreApplication.translate("TaskStepsConfig", "Create supplies structure in DB"),
                 STEP_TYPE: STStepTypeEnum.SCHEMA_IMPORT,
                 STEP_DESCRIPTION: QCoreApplication.translate("TaskStepsConfig",
                                                              "Choose a DB connection to create there the Supplies model structure."),
                 STEP_CUSTOM_ACTION_SLOT: {
                     SLOT_NAME: self._slot_caller.show_dlg_import_schema,
                     SLOT_PARAMS: {'db_source': SUPPLIES_DB_SOURCE,
                                   'selected_models': [LADMNames.SUPPORTED_SUPPLIES_MODEL]}}
                 },
                {STEP_NUMBER: 2,
                 STEP_NAME: QCoreApplication.translate("TaskStepsConfig", "Run supplies ETL"),
                 STEP_TYPE: STStepTypeEnum.RUN_ETL_COBOL,
                 STEP_ACTION: ACTION_RUN_ETL_COBOL,
                 STEP_DESCRIPTION: QCoreApplication.translate("TaskStepsConfig",
                                                              "Migrate Cobol data (.lis files) and its corresponding GBD to the LADM-COL (supplies model).")
                 },
                {STEP_NUMBER: 3,
                 STEP_NAME: QCoreApplication.translate("TaskStepsConfig", "Generate XTF"),
                 STEP_TYPE: STStepTypeEnum.EXPORT_DATA,
                 STEP_ACTION: ACTION_EXPORT_DATA_SUPPLIES,
                 STEP_DESCRIPTION: QCoreApplication.translate("TaskStepsConfig", "Export the data from the DB to a transfer file (.xtf).")
                 },
                {STEP_NUMBER: 4,
                 STEP_NAME: QCoreApplication.translate("TaskStepsConfig", "Upload XTF"),
                 STEP_TYPE: STStepTypeEnum.UPLOAD_FILE,
                 STEP_DESCRIPTION: QCoreApplication.translate("TaskStepsConfig", "Upload the XTF file to the Transition System."),
                 STEP_CUSTOM_ACTION_SLOT: {
                     SLOT_NAME: self._slot_caller.show_dlg_st_upload_file,
                     SLOT_PARAMS: {
                         'request_id': task_data['request']['requestId'] if 'request' in task_data else None,
                         'supply_type': task_data['request'][
                             'typeSupplyId'] if 'request' in task_data else None}}
                 }]
        elif task_type == TASK_INTEGRATE_SUPPLIES:
            steps_config = [
                {STEP_NUMBER: 1,
                 STEP_NAME: QCoreApplication.translate("TaskStepsConfig", "Connect to remote DB"),
                 STEP_TYPE: STStepTypeEnum.CONNECT_TO_DB,
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
                 STEP_TYPE: STStepTypeEnum.CONNECT_TO_DB,
                 STEP_DESCRIPTION: QCoreApplication.translate("TaskStepsConfig", "Load parcel data from cadastre and registry into QGIS."),
                 STEP_CUSTOM_ACTION_SLOT: {
                     SLOT_NAME: self._slot_caller.task_step_explore_data_cadastre_registry,
                     SLOT_PARAMS: {'db_engine': 'pg',
                                   'conn_dict': task_data['connection'] if 'connection' in task_data else {},
                                   'user_level': EnumUserLevel.CONNECT}},
                 },
                {STEP_NUMBER: 3,
                 STEP_NAME: QCoreApplication.translate("TaskStepsConfig", "Start assisted integration"),
                 STEP_TYPE: STStepTypeEnum.CONNECT_TO_DB,
                 STEP_ACTION: ACTION_EXPORT_DATA_SUPPLIES,  # TODO: functionality to integrate in assisted manner
                 STEP_DESCRIPTION: "Not implemented yet."
                }]

        return steps_config

