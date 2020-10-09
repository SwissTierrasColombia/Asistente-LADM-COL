from copy import deepcopy

from qgis.PyQt.QtCore import (QObject,
                              QCoreApplication)

from asistente_ladm_col.config.enums import EnumDbActionType
from asistente_ladm_col.config.general_config import (COLLECTED_DB_SOURCE,
                                                      SUPPLIES_DB_SOURCE,
                                                      SETTINGS_CONNECTION_TAB_INDEX,
                                                      SETTINGS_MODELS_TAB_INDEX)


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

    def __deepcopy__(self, memo={}):
        # Borrowed from https://stackoverflow.com/a/15774013/1073148
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result


class SettingsContext(Context):
    """
    Store parameters that together represent a context for running the Settings dialog
    """
    def __init__(self, db_source=COLLECTED_DB_SOURCE):
        Context.__init__(self, [db_source] if db_source else [COLLECTED_DB_SOURCE])

        self.action_type = EnumDbActionType.CONFIG
        self.blocking_mode = True  # Allow to save configurations even if DB connection is invalid
        self.required_models = list()
        self.title = QCoreApplication.translate("SettingsDialog", "Settings")
        self.tip = QCoreApplication.translate("SettingsDialog", "")
        self.tab_pages_list = list()

    @property
    def db_source(self):
        return self.get_db_sources()[0]

    @db_source.setter
    def db_source(self, db_source):
        self.set_db_sources([db_source])

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
        # Only show connection tab for supplies
        return [SETTINGS_CONNECTION_TAB_INDEX] if self.db_source == SUPPLIES_DB_SOURCE else self.__tab_pages_list

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
    # To run this tests, add the required vars to PYTHONPATH, like this:
    # export PYTHONPATH=/docs/dev/qgis/QGIS/build_master/output/python/:/docs/dev/qgis/QGIS/tests/src/python:/docs/dev/qgis/QGIS/build_master/output/python/plugins:/docs/dev/Asistente-LADM_COL/
    print("Starting tests...")

    # Contexts
    c = Context()
    c.set_db_sources(["c"])
    assert(c.get_db_sources() == ["c"])
    c1 = deepcopy(c)
    assert(c1 is not c)
    c1.set_db_sources(["c1"])
    assert(c.get_db_sources() == ["c"])
    assert(c1.get_db_sources() == ["c1"])

    c = Context(["c"])
    c1 = deepcopy(c)
    assert(c1 is not c)
    assert(c1.get_db_sources() == ["c"])  # Check that member variables are copied well
    c1.set_db_sources(["c1"])
    assert(c.get_db_sources() == ["c"])
    assert(c1.get_db_sources() == ["c1"])

    # Setting Contexts
    s = SettingsContext(COLLECTED_DB_SOURCE)
    s.tab_pages_list = [SETTINGS_CONNECTION_TAB_INDEX, SETTINGS_MODELS_TAB_INDEX]
    assert(s.tab_pages_list == [SETTINGS_CONNECTION_TAB_INDEX, SETTINGS_MODELS_TAB_INDEX])
    s.db_source = SUPPLIES_DB_SOURCE
    assert(s.db_source == SUPPLIES_DB_SOURCE)
    assert(s.tab_pages_list == [SETTINGS_CONNECTION_TAB_INDEX])

    s = SettingsContext(SUPPLIES_DB_SOURCE)
    assert (s.tab_pages_list == [SETTINGS_CONNECTION_TAB_INDEX])
    s.title = "My Settings"
    s1 = deepcopy(s)
    assert(s1 is not s)
    assert(s1.title == "My Settings")
    assert(s1.db_source == SUPPLIES_DB_SOURCE)
    s1.db_source = COLLECTED_DB_SOURCE
    assert(s.db_source == SUPPLIES_DB_SOURCE)
    assert(s1.db_source == COLLECTED_DB_SOURCE)
    assert(s1.tab_pages_list == list())

    # Task Contexts
    t = TaskContext()
    t.set_db_sources(["d"])
    assert(t.get_db_sources() == ["d"])
    t.set_slot_on_result("S")
    assert(t.get_slot_on_result() == "S")
    t2 = TaskContext([SUPPLIES_DB_SOURCE])
    assert(t2.get_db_sources()[0] == SUPPLIES_DB_SOURCE)

    t = TaskContext(["c"])
    t.set_slot_on_result("S")
    t1 = deepcopy(t)
    assert (t1 is not t)
    assert (t1.get_db_sources() == ["c"])  # Check that member variables are copied well
    assert (t1.get_slot_on_result() == "S")  # Check that member variables are copied well
    t1.set_db_sources(["c1"])
    assert (t.get_db_sources() == ["c"])
    assert (t1.get_db_sources() == ["c1"])

    print("Done!")