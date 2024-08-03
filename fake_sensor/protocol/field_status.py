"""status field"""


class Status:

    DATA1_READY = 1 << 0
    DATA2_READY = 1 << 1
    OVERRUN_ERROR = 1 << 2

    def __init__(self, value: int = 0):
        self.value = value

    def clear(self):
        self.value = 0

    def take(self) -> int:
        tmp = self.value
        self.clear()
        return tmp

    def set(self, bit):
        self.value |= bit

    def to_value(self):
        return self.value

    @classmethod
    def from_value(cls, value):
        return cls(value)

    def __repr__(self):
        return f"status(value={self.value:08b})"
