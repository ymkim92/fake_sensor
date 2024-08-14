"""status field"""

from enum import Enum


class StatusType(Enum):

    # DO NOT create an empty bit. Use reserved bit
    DATA1_READY = 0
    DATA2_READY = 1
    RESERVED1 = 2
    OVERRUN_ERROR = 3


class Status:

    def __init__(self, value: int = 0):
        self.value = value & ((1 << len(StatusType)) - 1)

    def clear(self) -> None:
        self.value = 0

    def take(self) -> int:
        tmp = self.value
        self.clear()
        return tmp

    def set(self, bit_shift: StatusType) -> None:
        self.value |= 1 << bit_shift.value
        return True

    def to_value(self) -> int:
        return self.value

    @classmethod
    def from_value(cls, value: int) -> "Status":
        return cls(value)

    def __repr__(self) -> str:
        """
        Return a string representation of the status register,
        showing which names are set.

        :return: A string showing the status register value and names set.
        """
        set_names = [status.name for status in StatusType if self.value & (1 << status.value)]
        set_names_str = ",".join(set_names) if set_names else "None"
        return f"Status(value=0x{self.value:02x}, names={set_names_str})"
