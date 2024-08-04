"""status field"""


class Status:

    DATA1_READY = 1 << 0
    DATA2_READY = 1 << 1
    OVERRUN_ERROR = 1 << 2

    def __init__(self, value: int = 0):
        self.value = value

    def clear(self) -> None:
        self.value = 0

    def take(self) -> int:
        tmp = self.value
        self.clear()
        return tmp

    def set(self, bit: int) -> None:
        self.value |= bit

    def to_value(self) -> int:
        return self.value

    @classmethod
    def from_value(cls, value: int) -> "Status":
        return cls(value)

    def __repr__(self) -> str:
        return f"status(value={self.value:08b})"
