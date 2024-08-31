"""interface for communication"""

from abc import ABC, abstractmethod


# pylint: disable=too-few-public-methods
class ICommunication(ABC):
    @abstractmethod
    def connect(self) -> bool:
        pass

    @abstractmethod
    def disconnect(self) -> bool:
        pass

    @abstractmethod
    def send_data(self, data: bytes) -> bool:
        pass

    @abstractmethod
    def receive_data(self) -> bytes:
        pass
