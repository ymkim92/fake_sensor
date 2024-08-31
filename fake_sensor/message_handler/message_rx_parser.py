"""message RX parser"""

from enum import Enum, auto
from typing import Optional

from fake_sensor.interface.interface_rx_parser import IRxParser, ParserState


class Event(Enum):
    RECEIVING_VALID_BYTE = auto()
    RECEIVED_END_OF_MESSAGE = auto()
    RECEIVE_ = auto()
    RECEIVE_DATA_CRC = auto()
    RECEIVE_ = auto()



class Action(Enum):
    PRINT_STATUS = auto()
    LOCK = auto()
    UNLOCK = auto()


class MessageRxParser(IRxParser):
    """Message RX parser"""

    def __init__(self):
        self.stored_data = bytearray()

    def receive_data(self, data: bytes) -> Optional[bytes]:
        """recv"""
        for byte in data:


    def get_state(self) -> ParserState:
        """get state"""
