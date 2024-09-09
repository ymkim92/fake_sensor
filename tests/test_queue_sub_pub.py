"""version test"""

import time

import pytest

from fake_sensor.communication.queue_sub_pub import QueueSubPub

QUEUE_SIZE = 2


@pytest.fixture(name="queue_sub_pub_fixture")
def queue_sub_pub() -> QueueSubPub:
    return QueueSubPub(QUEUE_SIZE)


def test_queue_sub_pub(queue_sub_pub_fixture: QueueSubPub) -> None:
    mq = queue_sub_pub_fixture
    mq.connect()

    assert mq.send_data(b"0123")
    assert mq.send_data(b"012a")
    assert mq.send_data(b"012b") is False

    assert mq.receive_data() == b"0123"
    assert mq.receive_data() == b"012a"
    assert mq.receive_data() is None
    mq.disconnect()
