"""interface for RX handler"""

from abc import ABC, abstractmethod


# pylint: disable=too-few-public-methods
class IRxHandler(ABC):
    @abstractmethod
    def receive_message(self) -> bytes:
        pass
