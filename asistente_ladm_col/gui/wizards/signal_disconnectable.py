from abc import ABC, abstractmethod

from qgis.PyQt.QtWidgets import (QWizard,
                                 QWizardPage)


class SignalDisconnectable(ABC):
    @abstractmethod
    def disconnect_signals(self):
        pass


class SignalDisconnectableMetaWiz(type(SignalDisconnectable), type(QWizard)):
    pass


class SignalDisconnectableMetaWizPage(type(SignalDisconnectable), type(QWizardPage)):
    pass
