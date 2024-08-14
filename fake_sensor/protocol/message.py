"""message"""

import struct
from enum import Enum

import crcmod.predefined  # type: ignore

# CRC16 Modbus
crc16 = crcmod.predefined.mkPredefinedCrcFun("modbus")

MIN_MESSAGE_LENGTH = 5
MAX_MESSAGE_LENGTH = 32


class MessageType(Enum):
    VERSION = 1
    SERIAL_NUMBER = 2
    STATUS = 3
    RESET = 0x10
    DATA1_FREQUENCY_CONFIGURATION = 0x11
    DATA2_FREQUENCY_CONFIGURATION = 0x12
    DATA = 0x80


class MessageErrorSize(ValueError):
    pass


class MessageErrorCrc(ValueError):
    pass


class MessageInvalidSync(ValueError):
    pass


class Message:
    """message"""

    SYNC_BYTE = 0xA3

    def __init__(self, type_: MessageType, data: bytes = b""):
        self.sync = self.SYNC_BYTE
        self.type = type_
        self.data_len = len(data)
        self.data = data
        self.crc = crc16(struct.pack(">BBB", self.sync, self.type.value, self.data_len) + self.data)

    def encode(self) -> bytes:
        """Encode the message into bytes"""
        return (
            struct.pack(">BBB", self.sync, self.type.value, self.data_len)
            + self.data
            + self.crc.to_bytes(2, "big")
        )

    @staticmethod
    def decode(message: bytes) -> "Message":
        """Decode bytes into a Message instance"""
        if len(message) < MIN_MESSAGE_LENGTH:
            raise MessageErrorSize(f"Data too short to be a valid message: {len(message)}")
        if len(message) > MAX_MESSAGE_LENGTH:
            raise MessageErrorSize(f"Data too long to be a valid message: {len(message)}")

        sync, type_, len_ = struct.unpack(">BBB", message[:3])
        if sync != Message.SYNC_BYTE:
            raise MessageInvalidSync("Invalid sync byte")

        start_index = 3
        end_index = 3 + len_
        _header = message[:start_index]
        _data = message[start_index:end_index]
        start_index = 3 + len_
        end_index = 5 + len_
        crc_received = struct.unpack(">H", message[start_index:end_index])[0]
        crc_calculated = crc16(_header + _data)

        if crc_received != crc_calculated:
            raise MessageErrorCrc("CRC mismatch")

        return Message(MessageType(type_), _data)
