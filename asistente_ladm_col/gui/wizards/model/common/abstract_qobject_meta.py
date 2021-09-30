from abc import ABCMeta

from qgis.PyQt.QtCore import QObject


class AbstractQObjectMeta(ABCMeta, type(QObject)):
    pass
