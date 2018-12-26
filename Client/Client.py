import socket
import threading
import time

HOST = "192.168.56.1"
class Client:

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__connect__()

    def send_message(self):
        self.sock.send(bytes(input(), 'utf-8'))

    def __connect__(self):
        # host = socket.gethostbyname(socket.gethostname())
        host = HOST
        port = 0
        self.server = (host, 9090)
        self.sock.bind((host, port))
        self.sock.setblocking(False)
        self.sock.sendto(b"user connected", self.server)
        self.sock.close()

Client()