from qgis.PyQt.QtCore import QObject
from .enum_action_type import EnumActionType


class DbAdmin(QObject):

    def __init__(self):
        self._mode = None

    def get_id(self):
        raise Exception('unimplemented method')

    def get_name(self):
        raise Exception('unimplemented method')

    def get_config_panel(self):
        raise Exception('unimplemented method')

    def get_model_baker_tool_name(self):
        raise Exception('unimplemented method')

    def get_db_connector(self, parameters):
        raise Exception('unimplemented method')

    def get_schema_import_configuration(self, params):
        raise Exception('unimplemented method')

    def get_import_configuration(self, params):
        raise Exception('unimplemented method')

    def get_export_configuration(self, params):
        raise Exception('unimplemented method')
