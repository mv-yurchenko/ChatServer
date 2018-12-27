import socket
import threading
import time

HOST = "192.168.56.1"


class Client:

    def __init__(self, username):
        self.username = username
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__connect__()
        self.__calculate_key__()
        print(self.key)

    def send_message(self):
        self.sock.sendto(bytes(input(), 'utf-8'), self.server)

    def receiving(self):
        pass

    def __connect__(self):
        # host = socket.gethostbyname(socket.gethostname())
        host = HOST
        port = 0
        self.server = (host, 9090)
        self.sock.bind((host, port))
        self.sock.setblocking(False)
        self.sock.sendto(b"user connected", self.server)

    def __calculate_key__(self): 
        sum = 0 
        mult = 1
        for char in self.username: 
            sum += ord(char)
            mult *= ord(char)
        self.key = int((sum + mult) / 2)


a = Client('user')
while 1:
    a.send_message()
