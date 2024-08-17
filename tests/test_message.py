"""test message"""

import struct

import crcmod.predefined
import pytest

from fake_sensor.protocol.message import (
    Message,
    MessageErrorCrc,
    MessageErrorSize,
    MessageInvalidSync,
    MessageSizeMismatched,
    MessageType,
)

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


def test_decode_invalid_sync_byte():
    type_ = MessageType.DATA
    data = b"testdata"
    message = Message(type_, data)
    encoded_message = message.encode()
    invalid_encoded_message = b"\xFF" + encoded_message[1:]

    with pytest.raises(MessageInvalidSync, match="Invalid sync byte"):
        Message.decode(invalid_encoded_message)


def test_decode_invalid_crc():
    type_ = MessageType.DATA
    data = b"testdata"
    message = Message(type_, data)
    encoded_message = message.encode()
    invalid_encoded_message = encoded_message[:-1] + bytes([encoded_message[-1] ^ 1])

    with pytest.raises(MessageErrorCrc, match="CRC mismatch"):
        Message.decode(invalid_encoded_message)


def test_decode_short_message():
    short_message = b"\xA3\x01\x08"

    with pytest.raises(MessageErrorSize, match="Data too short to be a valid message"):
        Message.decode(short_message)


def test_decode_long_message():
    long_message = b"\xA3\x01\x08" + bytes(30)

    with pytest.raises(MessageErrorSize, match="Data too long to be a valid message"):
        Message.decode(long_message)


def test_decode_message_size_mismatched():
    type_ = MessageType.DATA
    data = b"testdata"
    message = Message(type_, data)
    message.data_len += 1
    encoded_message = message.encode()

    with pytest.raises(
        MessageSizeMismatched,
        match=f"Expected data size {len(data)}, received data size {len(data) + 1}",
    ):
        Message.decode(encoded_message)
