from qgis.PyQt.QtCore import (QObject,pyqtSignal)
from qgis.core import (Qgis)


class DbConfigPanel(QObject):

    notify_message_requested = pyqtSignal(str, Qgis.MessageLevel)

    def __init__(self):
        super(DbConfigPanel, self).__init__()
        self._mode = None
        self.params_changed = False

    def read_connection_parameters(self):
        """
        Convenient function to read connection parameters and apply default
        values if needed.
        """
        raise Exception('unimplemented method')

    def write_connection_parameters(self, dict_conn):
        raise Exception('unimplemented method')

    def get_keys_connection_parameters(self):
        raise Exception('unimplemented method')

    def _set_params_changed(self):
        self.params_changed = True

    def set_action(self, action):
        pass