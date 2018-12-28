import socket
import threading
import time

# HOST = "192.168.56.1"
HOST = "127.0.1.1"


class Client:

    def __init__(self, username, is_private=False, companion_login=None):
        # Client main functions initialization
        self.username = username
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__connect__()
        self.__calculate_key__()
        self.stop_receiving = False
        self.rT = threading.Thread(target=self.receiving)
        self.rT.start()
        self.messages_history = list()

        # По дефолту все сообщения паблик
        self.msg_receiver = "all"
        self.companion_login = "no"

        # Режим Private Talk (1 на 1)
        self.is_private_talk = is_private
        if self.is_private_talk:
            self.msg_receiver = "private"
            self.companion_login = companion_login

    def close_client(self):
        """Закрывает сокет и останавливает поток"""
        self.stop_receiving = True
        self.rT.join()
        self.sock.close()

    def send_message(self, msg):
        """Шифрование сообщения и отправка на сервер """
        encrypted_msg = self.encrypt_msg(msg)
        msg = self.__compile_msg__(encrypted_msg)
        self.sock.sendto(bytes(msg, 'utf-8'), self.server)

    def receiving(self):
        """Функиця непрерывного получения данных с сервера в отдельном потоке"""
        while not self.stop_receiving:
            try:
                while True:
                    data, addr = self.sock.recvfrom(4096)
                    decrypted_msg = self.decrypt_msg(data)
                    time.sleep(0.2)
                    print(decrypted_msg)
                    self.messages_history.append(decrypted_msg)
            except Exception as _:
                pass

    def decrypt_msg(self, data):
        """Расшифровка сообщения"""
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
        """Шифровка сообщения"""
        encrypted_msg = str()
        for i in msg:
            encrypted_msg += chr(ord(i) ^ self.key)
        return encrypted_msg

    def __connect__(self):
        """Функция, инициализирующая подключенеи к серверу"""
        host = HOST
        port = 0
        self.server = (host, 9090)
        self.sock.bind((host, port))
        self.sock.setblocking(False)
        self.sock.sendto(self.username.encode("utf-8"), self.server)

    def __calculate_key__(self):
        """Вычисление ключа шифрования по логину"""
        sum = 0
        mult = 1
        for char in self.username:
            sum += ord(char)
            mult *= ord(char)
        self.key = int((sum + mult) / 2) //110000

    def __compile_msg__(self, encrypted_msg):
        """Составление строки для отправки на сервер"""
        msg = str()
        msg += self.username
        msg += "::" + self.msg_receiver
        print(self.companion_login)
        msg += "::" + self.companion_login
        msg += "::" + encrypted_msg
        return msg


login = input("Input login: ")
a = Client(login)
msg = input()
a.send_message(msg)
a.close_client()