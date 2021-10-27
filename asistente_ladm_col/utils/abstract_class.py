from abc import ABCMeta

try:
    from qgis.PyQt.QtCore import pyqtWrapperType
except ImportError:
    from sip import wrappertype as pyqtWrapperType


class AbstractQObjectMeta(pyqtWrapperType, ABCMeta):
    """Abstract class implementing QObject"""
    pass
