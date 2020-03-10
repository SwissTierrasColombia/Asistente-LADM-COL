from PyQt5.QtCore import QObject

from asistente_ladm_col.config.general_config import COLLECTED_DB_SOURCE


class Context(QObject):
    """
    Store parameters that together represent a context for running a tool
    """
    def __init__(self):
        QObject.__init__(self)
        self._db_sources = [COLLECTED_DB_SOURCE]

    def get_db_sources(self):
        return self._db_sources

    def set_db_sources(self, db_sources):
        self._db_sources = db_sources


class TaskContext(Context):
    """
    Store parameters that together represent a task context for running a tool
    """
    def __init__(self):
        Context.__init__(self)
        self._slot_on_result = None

    def get_slot_on_result(self):
        return self._slot_on_result

    def set_slot_on_result(self, slot):
        self._slot_on_result = slot


if __name__== "__main__":
    a = Context()
    a.set_db_source("c")
    print(a.get_db_source())
    t = TaskContext()
    t.set_db_source("d")
    print(t.get_db_source())
    t.set_slot_on_result("S")
    print(t.get_slot_on_result())