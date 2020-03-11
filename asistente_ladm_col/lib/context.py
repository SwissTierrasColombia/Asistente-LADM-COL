from PyQt5.QtCore import QObject

from asistente_ladm_col.config.general_config import (COLLECTED_DB_SOURCE,
                                                      SUPPLIES_DB_SOURCE)


class Context(QObject):
    """
    Store parameters that together represent a context for running a tool
    """
    def __init__(self, db_sources=[COLLECTED_DB_SOURCE]):
        QObject.__init__(self)
        self._db_sources = db_sources

    def get_db_sources(self):
        return self._db_sources

    def set_db_sources(self, db_sources):
        self._db_sources = db_sources


class TaskContext(Context):
    """
    Store parameters that together represent a task context for running a tool
    """
    def __init__(self, db_sources=[COLLECTED_DB_SOURCE]):
        Context.__init__(self, db_sources)

        # A slot that will react upon getting the result of an actions slot. Mainly used to check a step checkbox.
        self._slot_on_result = None

    def get_slot_on_result(self):
        return self._slot_on_result

    def set_slot_on_result(self, slot):
        self._slot_on_result = slot


if __name__== "__main__":
    a = Context()
    a.set_db_source("c")
    assert(a.get_db_source() == "c")
    t = TaskContext()
    t.set_db_source("d")
    assert(t.get_db_source() == "d")
    t.set_slot_on_result("S")
    assert(t.get_slot_on_result() == "S")
    t2 = TaskContext([SUPPLIES_DB_SOURCE])
    assert(t2.get_db_sources()[0] == SUPPLIES_DB_SOURCE)