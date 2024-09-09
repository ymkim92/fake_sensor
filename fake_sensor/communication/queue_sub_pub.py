"""queue"""

from queue import Empty, Full, Queue

from .interface_communication import ICommunication


class QueueSubPub(ICommunication):
    def __init__(self, queue_size):
        self.queue = Queue(maxsize=queue_size)
        self.queue_size = queue_size

    def connect(self) -> bool:
        return True

    def disconnect(self) -> bool:
        return True

    def send_data(self, data: bytes) -> bool:
        self.queue.put_nowait(data)

    def receive_data(self) -> bytes:
        return self.queue.get_nowait()
