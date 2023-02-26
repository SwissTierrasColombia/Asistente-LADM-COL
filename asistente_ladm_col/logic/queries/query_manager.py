import inspect
import os
import sys

from asistente_ladm_col.utils.singleton import Singleton


class QueryManager(metaclass=Singleton):

    def __init__(self):
        self._are_queries_loaded = False
        self._query_classes = dict()
        self._load_classes()

    def get_query(self, name, db):
        real_name = db.engine.capitalize() + name

        return self._query_classes[real_name]

    def _load_classes(self):
        the_dir = os.path.dirname(os.path.realpath(__file__)) + '/dynamic_queries'
        sys.path.insert(1, the_dir)
        all_files = os.listdir(the_dir)

        for file in all_files:
            if file.endswith(".py"):

                module_name = file.replace(".py", "")

                module = __import__(module_name)

                for item in inspect.getmembers(module, inspect.isclass):
                    self._query_classes[item[0]] = item[1]

        print(self._query_classes)
