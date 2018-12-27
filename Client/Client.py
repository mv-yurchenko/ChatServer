import socket
import threading
import time

HOST = "192.168.56.1"
# HOST = "127.0.1.1"


class Client:

    def __init__(self, username):
        self.username = username
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__connect__()
        self.__calculate_key__()
        self.stop_receiving = False
        self.rT = threading.Thread(target=self.receiving)
        self.rT.start()

    def close_client(self):
        self.stop_receiving = True
        self.rT.join()
        self.sock.close()

    def send_message(self, msg):
        encrypted_msg = self.encrypt_msg(msg)
        msg = self.__compile_msg__(encrypted_msg)
        self.sock.sendto(bytes(msg, 'utf-8'), self.server)

    def receiving(self):
        while not self.stop_receiving:
            try:
                while True:
                    data, addr = self.sock.recvfrom(4096)
                    decrypted_msg = self.decrypt_msg(data)
                    time.sleep(0.2)
                    print(decrypted_msg)

            except Exception as _:
                pass

    def decrypt_msg(self, data):
        decrypted_msg = ""
        k = False
        for char in data.decode("utf-8"):
            if char == ":":
                k = True
                decrypted_msg += char
            elif k == False or char == " ":
                decrypted_msg += char
            else:
                decrypted_msg += chr(ord(char) ^ self.key)
        return decrypted_msg

    def encrypt_msg(self, msg):
        encrypted_msg = str()
        for i in msg:
            encrypted_msg += chr(ord(i) ^ self.key)
        return encrypted_msg

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
        self.key = int((sum + mult) / 2) //110000

    def __compile_msg__(self, encrypted_msg):
        msg = str()
        msg += self.username
        msg += "::" + encrypted_msg
        return msg


a = Client('user')
msg = input()
a.send_message(msg)
a.close_client()