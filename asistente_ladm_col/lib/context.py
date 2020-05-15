from PyQt5.QtCore import (QObject,
                          QCoreApplication)

from asistente_ladm_col.config.enums import EnumDbActionType
from asistente_ladm_col.config.general_config import (COLLECTED_DB_SOURCE,
                                                      SUPPLIES_DB_SOURCE,
                                                      SETTINGS_CONNECTION_TAB_INDEX)


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


class SettingsContext(Context):
    """
    Store parameters that together represent a context for running the Settings dialog
    """
    def __init__(self, db_source=COLLECTED_DB_SOURCE):
        Context.__init__(self, [db_source] if db_source else [COLLECTED_DB_SOURCE])

        self.db_source = db_source
        self.action_type = EnumDbActionType.CONFIG
        self.blocking_mode = True  # Allow to save configurations even if DB connection is invalid
        self.required_models = list()
        self.title = QCoreApplication.translate("SettingsDialog", "Settings")
        self.tip = QCoreApplication.translate("SettingsDialog", "")

        # Only show connection tab for supplies
        self.tab_pages_list = [SETTINGS_CONNECTION_TAB_INDEX] if db_source == SUPPLIES_DB_SOURCE else list()

    @property
    def db_source(self):
        return self.get_db_sources()[0]

    @db_source.setter
    def db_source(self, db_source):
        self.__db_source = db_source

    @property
    def action_type(self):
        return self.__action_type

    @action_type.setter
    def action_type(self, action_type):
        self.__action_type = action_type

    @property
    def blocking_mode(self):
        return self.__blocking_mode

    @blocking_mode.setter
    def blocking_mode(self, block):
        self.__blocking_mode = block

    @property
    def tab_pages_list(self):
        return self.__tab_pages_list

    @tab_pages_list.setter
    def tab_pages_list(self, tab_pages_list):
        self.__tab_pages_list = tab_pages_list

    @property
    def required_models(self):
        return self.__required_models

    @required_models.setter
    def required_models(self, models):
        self.__required_models = models

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, title):
        self.__title = title

    @property
    def tip(self):
        return self.__tip

    @tip.setter
    def tip(self, tip):
        self.__tip = tip


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