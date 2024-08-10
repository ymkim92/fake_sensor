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
    assert Status.count_names() == 4


@pytest.mark.parametrize(
    "status_input,expected_value,expected_repr",
    [
        (0, 0, "Status(value=0x00, names=None)"),
        (1, 1, "Status(value=0x01, names=DATA1_READY)"),
        (2, 2, "Status(value=0x02, names=DATA2_READY)"),
        (4, 4, "Status(value=0x04, names=RESERVED1)"),
        (8, 8, "Status(value=0x08, names=OVERRUN_ERROR)"),
        (0xF, 0xF, "Status(value=0x0f, names=DATA1_READY,DATA2_READY,RESERVED1,OVERRUN_ERROR)"),
    ],
)
def test_status_repr(status_input, expected_value, expected_repr) -> None:
    status = Status(status_input)
    assert status.to_value() == expected_value
    assert repr(status) == expected_repr


def test_status_set() -> None:
    
