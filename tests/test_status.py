"""version test"""

import pytest

from fake_sensor.protocol.field_status import Status


def test_status_initialization() -> None:
    status = Status()
    assert status.to_value() == 0
    status = Status(0xF)
    assert status.to_value() == 0xF
    status = Status(0x1F)
    assert status.to_value() == 0xF


def test_number_of_status() -> None:
    assert Status.count_constants() == 4


def test_status_repr() -> None:
    status = Status()
    assert status.to_value() == 0
