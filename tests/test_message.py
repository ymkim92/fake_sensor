import struct

import crcmod.predefined
import pytest

from fake_sensor.protocol.message import Message, MessageType

# CRC16 Modbus function
crc16 = crcmod.predefined.mkPredefinedCrcFun("modbus")


def test_message_encode():
    type_ = MessageType.SERIAL_NUMBER
    data = b"testdata"
    message = Message(type_, data)

    # Manually calculate the expected packed message
    message_without_crc = struct.pack(">BBB", Message.SYNC_BYTE, type_.value, len(data)) + data
    print(message_without_crc)
    expected_crc = crc16(message_without_crc)
    expected_encoded_message = message_without_crc + expected_crc.to_bytes(2, "big")

    assert message.encode() == expected_encoded_message


def test_message_decode():
    type_ = MessageType.DATA
    data = b"testdata"

    original_message = Message(type_, data)
    packed_message = original_message.encode()

    unpacked_message = Message.decode(packed_message)

    assert unpacked_message.sync == original_message.sync
    assert unpacked_message.type == original_message.type
    assert unpacked_message.data_len == original_message.data_len
    assert unpacked_message.data == original_message.data
    assert unpacked_message.crc == original_message.crc


# def test_unpack_invalid_sync_byte():
#     # Create a valid message and then modify the sync byte
#     type_ = MessageType.DATA
#     data = b"testdata"
#     message = Message(type_, data)
#     packed_message = message.pack()
#     invalid_packed_message = b"\xFF" + packed_message[1:]  # Change sync byte to invalid value

#     # Expect ValueError due to invalid sync byte
#     with pytest.raises(ValueError, match="Invalid sync byte"):
#         Message.unpack(invalid_packed_message)


# def test_unpack_invalid_crc():
#     # Create a valid message and then modify the CRC
#     type_ = 0x01
#     data = b"testdata"
#     message = Message(type_, data)
#     packed_message = message.pack()
#     invalid_packed_message = packed_message[:-2] + b"\x00\x00"  # Change CRC to an invalid value

#     # Expect ValueError due to CRC mismatch
#     with pytest.raises(ValueError, match="CRC mismatch"):
#         Message.unpack(invalid_packed_message)


# def test_unpack_short_message():
#     # Create a short message that's not valid
#     short_message = b"\xA3\x01\x08"

#     # Expect ValueError due to data too short
#     with pytest.raises(ValueError, match="Data too short to be a valid message"):
#         Message.unpack(short_message)
