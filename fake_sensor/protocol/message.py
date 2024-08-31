"""message"""

import struct
from enum import Enum

import crcmod.predefined  # type: ignore

# CRC16 Modbus
crc16 = crcmod.predefined.mkPredefinedCrcFun("modbus")


MESSAGE_HEADER_LEN = 3
MESSAGE_CRC_LEN = 2
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


class MessageSizeMismatched(ValueError):
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

    # "Message" is a forward reference
    @staticmethod
    def decode(message: bytes) -> "Message":
        """Decode bytes into a Message instance"""
        if len(message) < MIN_MESSAGE_LENGTH:
            raise MessageErrorSize(f"Data too short to be a valid message: {len(message)}")
        if len(message) > MAX_MESSAGE_LENGTH:
            raise MessageErrorSize(f"Data too long to be a valid message: {len(message)}")

        sync, type_, data_len = struct.unpack(">BBB", message[:MESSAGE_HEADER_LEN])
        if sync != Message.SYNC_BYTE:
            raise MessageInvalidSync("Invalid sync byte")
        if len(message) != data_len + MESSAGE_HEADER_LEN + MESSAGE_CRC_LEN:
            expected_data_size = len(message) - MESSAGE_HEADER_LEN - MESSAGE_CRC_LEN
            raise MessageSizeMismatched(
                f"Expected data size {expected_data_size}, received data size {data_len}"
            )

        start_index = MESSAGE_HEADER_LEN
        end_index = MESSAGE_HEADER_LEN + data_len
        _header = message[:start_index]
        _data = message[start_index:end_index]

        start_index = MESSAGE_HEADER_LEN + data_len
        end_index = MESSAGE_HEADER_LEN + data_len + MESSAGE_CRC_LEN
        crc_received = struct.unpack(">H", message[start_index:end_index])[0]
        crc_calculated = crc16(_header + _data)

        if crc_received != crc_calculated:
            raise MessageErrorCrc("CRC mismatch")

        return Message(MessageType(type_), _data)
