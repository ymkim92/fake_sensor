"""interface for RX parser"""

from abc import ABC, abstractmethod
from enum import Enum


class ParserState(Enum):
    READY = 0
    HEADER_SYNC = 1
    HEADER_TYPE = 2
    HEADER_LENGTH = 3
    READING_DATA_CRC = 4
    COMPLETE_MESSAGE = 5


# pylint: disable=too-few-public-methods
class IRxParser(ABC):
    @abstractmethod
    def receive_message(self) -> bytes:
        pass

    @abstractmethod
    def get_state(self) -> ParserState:
        pass
