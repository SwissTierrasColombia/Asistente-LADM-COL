from abc import ABC, abstractmethod
from qgis.PyQt.QtWidgets import QWizard


class SignalDisconnectable(ABC):
    @abstractmethod
    def disconnect_signals(self):
        pass


class SignalDisconnectableMetaWiz(type(SignalDisconnectable), type(QWizard)):
    pass
