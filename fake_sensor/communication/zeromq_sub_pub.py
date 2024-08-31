"""ZeroMQ sub/pub"""

import zmq

from .interface_communication import ICommunication

TOPIC_SEPARATOR = b" "


class ZeroMqSubPub(ICommunication):
    def __init__(self, topic: bytes, port: str):
        self.communication_topic = topic
        self.communication_port = port

        self.sub_socket = None
        self.pub_socket = None

    def connect(self) -> bool:
        try:
            context = zmq.Context()

            # Create and bind the PUB socket
            self.pub_socket = context.socket(zmq.PUB)
            self.pub_socket.bind(self.communication_port)

            # Create and connect the SUB socket
            self.sub_socket = context.socket(zmq.SUB)
            self.sub_socket.connect(self.communication_port)
            self.sub_socket.setsockopt(zmq.SUBSCRIBE, self.communication_topic)

            return True

        except zmq.ZMQError as e:
            logging.error(f"ZMQError occurred: {e}")
            return False
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            return False

    def disconnect(self) -> bool:
        if self.pub_socket:
            self.pub_socket.close()

        if self.sub_socket:
            self.sub_socket.close()

        return True

    def send_data(self, data: bytes) -> bool:
        message = self.communication_topic + TOPIC_SEPARATOR + data
        bytes_sent = self.pub_socket.send(message)
        return bytes_sent == len(message)

    def receive_data(self) -> bytes:
        message = self.sub_socket.recv()
        topic, data = message.split(TOPIC_SEPARATOR)
        assert topic == self.communication_topic
        return data
