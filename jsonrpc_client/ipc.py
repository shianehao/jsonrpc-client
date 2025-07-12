import logging
import os
import socket


__author__ = "Roger Huang"
__copyright__ = "Copyright 2025, The JSONRPC Client Project"
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

    def run(self, event_callback:callable) -> str:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((self.server_ip, self.port))
        except Exception as e:
            print(f'TCP: {e}')
            self.socket = None
            return

        while self.stop is False:
            try:
                payload = self.socket.recv(4096)
            except ConnectionAbortedError as e:
                logger.error(f"Connection aborted: {e}")
                break

            if payload:
                for x in payload.decode().split('\n'):
                    event_callback(x)
            else:
                break

        self.socket = None
        return "Done."

    def close(self) -> None:
        if self.socket:
            self.socket.shutdown(0)
        self.socket.close()
        self.stop = True

    def write(self, payload: str) -> None:
        if self.socket:
            msg = payload.encode()
            totalsent = 0
            while totalsent < len(msg):
                sent = self.socket.send(msg[totalsent:])
                if sent == 0:
                    raise RuntimeError("Socket connection broken")
                totalsent += sent

