"""status field"""


class Status:

    # TO get the number of status, it should start with "STATUS_"
    # DO NOT create an empty bit. Use reserved bit
    STATUS_DATA1_READY = 1 << 0
    STATUS_DATA2_READY = 1 << 1
    STATUS_RESERVED1 = 1 << 2
    STATUS_OVERRUN_ERROR = 1 << 3

    _constant_map = {
        STATUS_DATA1_READY: "DATA1_READY",
        STATUS_DATA2_READY: "DATA2_READY",
        STATUS_RESERVED1: "RESERVED1",
        STATUS_OVERRUN_ERROR: "OVERRUN_ERROR",
    }

    def __init__(self, value: int = 0):
        self.value = value & ((1 << Status.count_constants()) - 1)

    def clear(self) -> None:
        self.value = 0

    def take(self) -> int:
        tmp = self.value
        self.clear()
        return tmp

    def set(self, bit_shift: int) -> None:
        self.value |= 1 << bit_shift

    def to_value(self) -> int:
        return self.value

    @classmethod
    def from_value(cls, value: int) -> "Status":
        return cls(value)

    def __repr__(self) -> str:
        """
        Return a string representation of the status register,
        showing which constants are set.

        :return: A string showing the status register value and constants set.
        """
        set_constants = [name for bit, name in Status._constant_map.items() if self.value & bit]
        set_constants_str = ", ".join(set_constants) if set_constants else "None"
        return f"Status(value={self.value:08b}, constants={{ {set_constants_str} }})"

    @classmethod
    def count_constants(cls) -> int:
        """
        Count the number of constant attributes in the Status class.

        :return: The number of constant attributes.
        """
        constants = [attr for attr in dir(cls) if attr.isupper() and attr.startswith("STATUS_")]
        return len(constants)
