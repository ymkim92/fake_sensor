"""ZeroMQ RX handler"""

from fake_sensor.interface.interface_rx_handler import IRxHandler
from fake_sensor.interface.interface_rx_parser import IRxParser


# pylint: disable=too-few-public-methods
class MessageRxHandler(IRxHandler):
    """ZeroMQ RX handler"""

    def __init__(self, message_parser: IRxParser, message_subscriber: IRxHandler):
        self.message_parser = message_parser
        self.message_subscriber = message_subscriber

    def receive_message(self) -> bytes:
        """receive message by subscriber"""
        message = self.message_subscriber.receive_message()
        return self.message_parser(message)
