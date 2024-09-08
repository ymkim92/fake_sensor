"""version test"""

import time

import pytest

from fake_sensor.communication.zeromq_sub_pub import ZeroMqSubPub

COMMUNICATION_TOPIC = b"sensor"
COMMUNICATION_PORT = "tcp://127.0.0.1:5555"
SUB_QUEUE_SIZE = 2
PUB_QUEUE_SIZE = 2


@pytest.fixture(name="zeromq_sub_pub_fixture")
def zeromq_sub_pub() -> ZeroMqSubPub:
    return ZeroMqSubPub(COMMUNICATION_TOPIC, COMMUNICATION_PORT, SUB_QUEUE_SIZE, PUB_QUEUE_SIZE)


def test_zeromq_sub_pub(zeromq_sub_pub_fixture: ZeroMqSubPub) -> None:
    zero_mq = zeromq_sub_pub_fixture
    zero_mq.connect()

    # Why this is necessary?
    time.sleep(0.1)

    assert zero_mq.send_data(b"0123")
    assert zero_mq.send_data(b"012a")
    assert zero_mq.send_data(b"012b")
    time.sleep(0.1)
    assert zero_mq.receive_data() == b"0123"
    # assert zero_mq.receive_data() == b"012a"
    # assert zero_mq.receive_data() is None
    zero_mq.disconnect()
