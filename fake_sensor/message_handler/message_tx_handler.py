"""message TX handler"""

from typing import Any, Callable

from fake_sensor.interface.interface_tx_handler import ITxHandler


# pylint: disable=too-few-public-methods
class MessageTxHandler(ITxHandler):
    """Message TX handler"""

    def __init__(
        self,
        message_transmitter: Callable[[Any], bool],
    ):
        self.message_transmitter = message_transmitter

    def send_message(self, message: bytes) -> bool:
        return self.message_transmitter(message)
