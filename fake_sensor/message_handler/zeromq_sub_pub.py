"""ZeroMQ sub/pub"""

from .interface_communication import ICommunication

class ZeroMqSubPub(ICommunication):
    def __init__(self):
        