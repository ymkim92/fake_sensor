"""queue"""

from queue import Empty, Full, Queue

from .interface_communication import ICommunication


class QueueSubPub(ICommunication):
    def __init__(self):
        self.queue = None

    def connect(self) -> bool:
        self.queue = Queue()
        return True

    def disconnect(self) -> bool:
        return True

    def send_data(self, data: bytes) -> bool:
        self.queue.put_nowait(data)

    def receive_data(self) -> bytes:
        return self.queue.get_nowait()
