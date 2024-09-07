"""fake sensor command line interface"""

import time

from fake_sensor.communication.zeromq_sub_pub import ZeroMqSubPub

COMMUNICATION_TOPIC = b"sensor"
COMMUNICATION_PORT = "tcp://127.0.0.1:5555"


def main():
    zero_mq = ZeroMqSubPub(COMMUNICATION_TOPIC, COMMUNICATION_PORT)
    zero_mq.connect()

    time.sleep(0.1)
    zero_mq.send_data(b"0123")
    time.sleep(0.1)
    zero_mq.send_data(b"012a")
    time.sleep(0.1)
    zero_mq.send_data(b"012b")
    time.sleep(0.1)
    print(zero_mq.receive_data())
    print(zero_mq.receive_data())
    print(zero_mq.receive_data())
    zero_mq.disconnect()


if __name__ == "__main__":
    main()
