"""message RX parser"""

from typing import Any, Callable

from fake_sensor.protocol.message import Message

from .interface_rx_parser import IRxParser, ParserState


class MessageRxParser(IRxParser):
    """Message RX parser"""

    def __init__(
        self,
        message_decoder: Callable[[Any], Message],
    ):
        self.message_decoder = message_decoder

    def receive_data(self) -> bytes:
        """recv"""

    def get_state(self) -> ParserState:
        """get state"""
