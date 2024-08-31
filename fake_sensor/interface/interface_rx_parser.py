"""interface for RX parser"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional


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
    def receive_message(self, data: bytes) -> Optional[bytes]:
        """returns message when it collects a valid message
        input data can be a part of message
        """
        pass

    @abstractmethod
    def get_state(self) -> ParserState:
        pass
