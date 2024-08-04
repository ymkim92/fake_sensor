"""message"""

import struct

import crcmod.predefined

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

        value = data[3:3 + len_]
        crc_received = struct.unpack(">H", data[3 + len_:5 + len_])[0]
        crc_calculated = crc16(struct.pack(">BBB", sync, type_, len_) + value)

        if crc_received != crc_calculated:
            raise ValueError("CRC mismatch")

        return Message(type_, value)


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
