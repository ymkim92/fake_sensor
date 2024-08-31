"""fake sensor command line interface"""

from fake_sensor.communication.zeromq_sub_pub import ZeroMqSubPub

COMMUNICATION_TOPIC = b"sensor"
COMMUNICATION_PORT = "tcp://127.0.0.1:5555"


def main():
    ZeroMqSubPub(COMMUNICATION_TOPIC, COMMUNICATION_PORT)


if __name__ == "__main__":
    main()
