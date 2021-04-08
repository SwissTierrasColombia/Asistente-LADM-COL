from abc import ABC, abstractmethod


class SignalDisconnectable(ABC):
    @abstractmethod
    def disconnect_signals(self):
        pass
