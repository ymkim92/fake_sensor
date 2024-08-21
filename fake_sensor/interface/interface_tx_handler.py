"""interface for TX handler"""

from abc import ABC, abstractmethod


# pylint: disable=too-few-public-methods
class ITxHandler(ABC):
    @abstractmethod
    def send_message(self, message: bytes) -> bool:
        pass
