"""ZeroMQ RX handler"""

from typing import Any, Callable

from .interface_rx_handler import IRxHandler
from .interface_rx_parser import IRxParser


# pylint: disable=too-few-public-methods
class ZeroMqRxHandler(IRxHandler):
    """ZeroMQ RX handler"""

    def __init__(self, message_parser: IRxParser, zmq_subscribe: XXX):
        self.message_parser = message_parser

    def receive_message(self) -> bytes:
        """receive message by zmq subscribe"""
        # zmq subscribe
        # return self.message_parser(message)
