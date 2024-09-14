"""ZeroMQ sub/pub"""

import time
from typing import Optional

import zmq

from .interface_communication import ICommunication

TOPIC_SEPARATOR = b" "
ZEROMQ_CONNECTION_TIME = 0.001


class ZeroMqSubPub(ICommunication):
    def __init__(self, topic: bytes, port: str, sub_queue_size: int, pub_queue_size: int):
        self.communication_topic = topic
        self.communication_port = port
        self.sub_queue_size = sub_queue_size
        self.pub_queue_size = pub_queue_size

        self.context = zmq.Context()

        self.pub_socket = self.context.socket(zmq.PUB)
        self.pub_socket.bind(self.communication_port)
        self.pub_socket.setsockopt(zmq.SNDHWM, self.pub_queue_size)

        self.sub_socket: Optional[zmq.Socket] = None

    def connect(self) -> bool:
        try:
            # Create and connect the SUB socket
            self.sub_socket = self.context.socket(zmq.SUB)
            self.sub_socket.connect(self.communication_port)
            self.sub_socket.setsockopt(zmq.SUBSCRIBE, self.communication_topic)
            self.sub_socket.setsockopt(zmq.RCVHWM, self.sub_queue_size)

            # ZeroMQ does not offer a built-in, direct way to check
            # if a PUB/SUB connection is fully established between sockets.
            # This is because ZeroMQ is designed to be asynchronous,
            # and its PUB/SUB pattern doesn't guarantee message delivery
            # if the subscriber isn't yet connected.
            time.sleep(0.001)

            return True

        except zmq.ZMQError as e:
            print(f"ZMQError occurred: {e}")
            return False
        except Exception as e:  # pylint: disable=broad-exception-caught
            print(f"An unexpected error occurred: {e}")
            return False

    def disconnect(self) -> bool:
        if self.pub_socket:
            self.pub_socket.close()

        if self.sub_socket:
            self.sub_socket.close()

        return True

    def send_data(self, data: bytes) -> bool:
        if not self.pub_socket:
            return False
        message = self.communication_topic + TOPIC_SEPARATOR + data
        try:
            self.pub_socket.send(message)
        except zmq.ZMQError as e:
            print(f"Failed to send data: {e}")
            return False

        return True

    def receive_data(self) -> Optional[bytes]:
        if not self.sub_socket:
            return None
        try:
            message = self.sub_socket.recv(zmq.NOBLOCK)
        except zmq.error.Again:
            # no data available
            return None
        except zmq.ZMQError as e:
            print(f"Receive failed: {e}")
            return None

        topic, data = message.split(TOPIC_SEPARATOR)
        assert topic == self.communication_topic
        return data

    # Context Manager Methods
    def __enter__(self):
        """Handle setup when entering the context."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Handle cleanup when exiting the context."""
        self.disconnect()
