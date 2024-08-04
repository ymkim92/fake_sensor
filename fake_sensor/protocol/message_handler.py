"""message handler"""

import struct
from typing import Any, Callable

from .message import Message


class MessageHandler:
    """Message handler"""

    def __init__(
        self, message_packer: Callable[[Any], bytes], message_unpacker: Callable[[Any], Message]
    ):
        self.message_packer = message_packer
        self.message_unpacker = message_unpacker

    def send_message(self, message: Message) -> bytes:
        return self.message_packer(message)

    def receive_message(self, data: bytes) -> Message:
        return self.message_unpacker(data)


# Example usage
if __name__ == "__main__":
    # Create a message
    version_response = Message(type_=0x01, value=struct.pack(">BBB8s", 1, 0, 1, b"12345678"))

    # Pack the message
    packed_message = version_response.pack()
    print(f"Packed message: {packed_message.hex()}")

    # Unpack the message
    unpacked_message = Message.unpack(packed_message)
    print(f"Unpacked message type: {unpacked_message.type}")
    print(f"Unpacked message value: {unpacked_message.value.hex()}")
