"""ZeroMQ sub/pub"""

import time
from typing import Any, Dict, Optional

import zmq
from zmq.utils.monitor import recv_monitor_message

from .interface_communication import ICommunication

TOPIC_SEPARATOR = b" "


class ZeroMqSubPub(ICommunication):
    def __init__(self, topic: bytes, port: str, sub_queue_size: int, pub_queue_size: int):
        self.communication_topic = topic
        self.communication_port = port
        self.sub_queue_size = sub_queue_size
        self.pub_queue_size = pub_queue_size

        self.sub_socket: Optional[zmq.Socket] = None
        self.pub_socket: Optional[zmq.Socket] = None

    def connect(self) -> bool:
        try:
            context = zmq.Context()

            # Create and bind the PUB socket
            self.pub_socket = context.socket(zmq.PUB)
            self.pub_socket.bind(self.communication_port)
            self.pub_socket.setsockopt(zmq.SNDHWM, self.pub_queue_size)

            # Create and connect the SUB socket
            self.sub_socket = context.socket(zmq.SUB)
            self.sub_socket.connect(self.communication_port)
            self.sub_socket.setsockopt(zmq.SUBSCRIBE, self.communication_topic)
            self.sub_socket.setsockopt(zmq.RCVHWM, self.sub_queue_size)

            self.event_connected_monitor()
            return True

        except zmq.ZMQError as e:
            print(f"ZMQError occurred: {e}")
            return False
        except Exception as e:
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

    # def event_connected_monitor(self) -> None:
    #     if not self.pub_socket:
    #         return
    #     monitor = self.pub_socket.get_monitor_socket()
    #     if not monitor:
    #         return
    #     while monitor.poll():
    #         evt: Dict[str, Any] = {}
    #         mon_evt = recv_monitor_message(monitor)
    #         evt.update(mon_evt)
    #         print(f"Event: {evt}")
    #         if evt["event"] == zmq.EVENT_CONNECTED:
    #             print("subscriber is connected!")
    #             break

    #     monitor.close()

    def event_connected_monitor(self, timeout=5000) -> None:
        if not self.pub_socket:
            return

        monitor = self.pub_socket.get_monitor_socket(zmq.EVENT_ALL)
        if not monitor:
            return

        poller = zmq.Poller()
        poller.register(monitor, zmq.POLLIN)

        start_time = time.time()
        while time.time() - start_time < timeout / 1000:  # Timeout in seconds
            socks = dict(poller.poll(timeout))
            if monitor in socks and socks[monitor] == zmq.POLLIN:
                evt = recv_monitor_message(monitor)
                print(f"Event: {evt}")
                if evt["event"] == zmq.EVENT_CONNECTED:
                    print("Subscriber is connected!")
                    break

        monitor.close()
