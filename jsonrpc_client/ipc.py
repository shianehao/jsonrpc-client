import logging
import os
import socket


__author__ = "Roger Huang"
__copyright__ = "Copyright 2024, The JSONRPC Client Project"
__license__ = "Proprietary"
__version__ = "2.0.1"
__maintainer__ = "Roger Huang"
__email__ = "rogerhuang7@gmail.com"
__status__ = "Package"


logger = logging.getLogger('Tcp')

class TcpIpc:
    def __init__(self, server_ip: str, port: int, *args, **kwargs):
        self.server_ip = server_ip
        self.port = port
        self.stop = False
        self.socket = None

    def run(self, event_callback:callable):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.server_ip, self.port))

        while self.stop is False:
            payload = self.socket.recv(2048)
            event_callback(payload)

        self.socket.close()
        return "Done."
    
    def close(self):
        self.stop = True

        