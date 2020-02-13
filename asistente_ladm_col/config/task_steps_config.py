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

    def _get_config(self, task_type, task_data):
        steps_config = {}
        if task_type == TASK_GENERATE_CADASTRAL_SUPPLIES:
            steps_config = {
               1: {STEP_NAME: QCoreApplication.translate("TaskStepsConfig", "Create supplies structure in DB"),
                   STEP_ACTION: None,
                   STEP_TYPE: STStepTypeEnum.SCHEMA_IMPORT,
                   STEP_DESCRIPTION: "",
                   STEP_CUSTOM_ACTION_SLOT: {
                       SLOT_NAME: self._slot_caller.show_dlg_import_schema,
                       SLOT_PARAMS: {'db_source': SUPPLIES_DB_SOURCE,
                                     'selected_models': [LADMNames.SUPPORTED_SUPPLIES_MODEL]}}
                   },
               2: {STEP_NAME: QCoreApplication.translate("TaskStepsConfig", "Run supplies ETL"),
                   STEP_TYPE: STStepTypeEnum.RUN_ETL_COBOL,
                   STEP_ACTION: ACTION_RUN_ETL_COBOL,
                   STEP_DESCRIPTION: ""
                   },
               3: {STEP_NAME: QCoreApplication.translate("TaskStepsConfig", "Generate XTF"),
                   STEP_TYPE: STStepTypeEnum.EXPORT_DATA,
                   STEP_ACTION: ACTION_EXPORT_DATA_SUPPLIES,
                   STEP_DESCRIPTION: ""
                   },
               4: {STEP_NAME: QCoreApplication.translate("TaskStepsConfig", "Upload XTF"),
                   STEP_TYPE: STStepTypeEnum.UPLOAD_FILE,
                   STEP_ACTION: None,
                   STEP_DESCRIPTION: "Upload an XTF file to the Transition System.",
                   STEP_CUSTOM_ACTION_SLOT: {
                       SLOT_NAME: self._slot_caller.show_dlg_st_upload_file,
                       SLOT_PARAMS: {
                           'request_id': task_data['request']['requestId'] if 'request' in task_data else None,
                           'supply_type': task_data['request']['typeSupplyId'] if 'request' in task_data else None}}
                   }
           }
        elif task_type == TASK_INTEGRATE_SUPPLIES:
            steps_config = {
                1: {STEP_NAME: QCoreApplication.translate("TaskStepsConfig", "Connect to remote DB"),
                    STEP_TYPE: STStepTypeEnum.CONNECT_TO_DB,
                    STEP_ACTION: None,
                    STEP_DESCRIPTION: "",
                    STEP_CUSTOM_ACTION_SLOT: {
                        SLOT_NAME: self._slot_caller.open_encrypted_db_connection,
                        SLOT_PARAMS: {'db_engine': 'pg',
                                      'conn_dict': task_data['connection'] if 'connection' in task_data else {},
                                      'user_level': EnumUserLevel.CONNECT}
                    },
                    },
                2: {STEP_NAME: QCoreApplication.translate("TaskStepsConfig",
                                                          "Explore data from Cadastre and Land Registry"),
                    STEP_TYPE: STStepTypeEnum.CONNECT_TO_DB,
                    STEP_ACTION: None,
                    STEP_DESCRIPTION: "",
                    STEP_CUSTOM_ACTION_SLOT: {
                        SLOT_NAME: self._slot_caller.task_step_explore_data_cadastre_registry,
                        SLOT_PARAMS: {'db_engine': 'pg',
                                      'conn_dict': task_data['connection'] if 'connection' in task_data else {},
                                      'user_level': EnumUserLevel.CONNECT}
                    },
                    },
                3: {STEP_NAME: QCoreApplication.translate("TaskStepsConfig", "Start assisted integration"),
                    STEP_TYPE: STStepTypeEnum.CONNECT_TO_DB,
                    STEP_ACTION: ACTION_EXPORT_DATA_SUPPLIES,
                    STEP_DESCRIPTION: ""
                    }
            }

        return steps_config

    def get_steps_data(self, task):
        steps_data = list()
        steps_config = self._get_config(task.get_type(), task.get_data())  # TODO, adjust the config to make it ready to return
        if steps_config:
            for id, data in steps_config.items():
                step_data = dict()
                step_data[STEP_NUMBER] = id
                step_data[STEP_NAME] = data[STEP_NAME]
                step_data[STEP_TYPE] = data[STEP_TYPE]
                step_data[STEP_ACTION] = data[STEP_ACTION]
                step_data[STEP_DESCRIPTION] = data[STEP_DESCRIPTION]
                if STEP_CUSTOM_ACTION_SLOT in data:
                    step_data[STEP_CUSTOM_ACTION_SLOT] = data[STEP_CUSTOM_ACTION_SLOT]
                steps_data.append(step_data)

        return steps_data

