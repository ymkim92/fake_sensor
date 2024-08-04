"""message"""

import struct

import crcmod.predefined  # type: ignore

# CRC16 Modbus
crc16 = crcmod.predefined.mkPredefinedCrcFun("modbus")


class Message:
    """message"""

    SYNC_BYTE = 0xA3

    def __init__(self, type_: int, value: bytes = b""):
        self.sync = self.SYNC_BYTE
        self.type = type_
        self.data_len = len(value)
        self.value = value
        self.crc = crc16(struct.pack(">BBB", self.sync, self.type, self.data_len) + self.value)

    def pack(self) -> bytes:
        """Pack the message into bytes"""
        return (
            struct.pack(">BBB", self.sync, self.type, self.data_len)
            + self.value
            + struct.pack(">H", self.crc)
        )

    @staticmethod
    def unpack(data: bytes) -> "Message":
        """Unpack bytes into a Message instance"""
        if len(data) < 5:
            raise ValueError("Data too short to be a valid message")

        sync, type_, len_ = struct.unpack(">BBB", data[:3])
        if sync != Message.SYNC_BYTE:
            raise ValueError("Invalid sync byte")

        start_index = 3
        end_index = 3 + len_
        value = data[start_index:end_index]
        start_index = 3 + len_
        end_index = 5 + len_
        crc_received = struct.unpack(">H", data[start_index:end_index])[0]
        crc_calculated = crc16(struct.pack(">BBB", sync, type_, len_) + value)

        if crc_received != crc_calculated:
            raise ValueError("CRC mismatch")

        return Message(type_, value)
