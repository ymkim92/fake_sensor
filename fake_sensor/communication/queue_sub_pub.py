"""queue"""

from queue import Queue
from typing import Any, Optional

from .interface_communication import ICommunication


class QueueSubPub(ICommunication):
    def __init__(self, queue_size: int):
        self.queue: Queue[Any] = Queue(maxsize=queue_size)
        self.queue_size = queue_size

    def connect(self) -> bool:
        return True

    def disconnect(self) -> bool:
        return True

    def send_data(self, data: bytes) -> bool:
        if self.queue.full():
            return False
        self.queue.put_nowait(data)
        return True

    def receive_data(self) -> Optional[bytes]:
        if self.queue.empty():
            return None
        return bytes(self.queue.get_nowait())
