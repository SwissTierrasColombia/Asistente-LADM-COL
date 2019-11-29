try:
    from qgis.PyQt.QtCore import pyqtWrapperType
except ImportError:
    from sip import wrappertype as pyqtWrapperType


class SingletonQObject(pyqtWrapperType, type):
    """
    Singleton that is also a QObject, so we can emit SIGNALS and all that stuff :P

    From: https://forum.qt.io/topic/88531/singleton-in-python-with-qobject/2
    """
    def __init__(cls, name, bases, dict):
        super().__init__(name, bases, dict)
        cls.instance=None

    def __call__(cls,*args,**kw):
        if cls.instance is None:
            cls.instance=super().__call__(*args, **kw)
        return cls.instance


class Singleton(type):
    """
    Single Singleton :)

    From: https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python#6798042
    """
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]