import socket
import threading
import time

HOST = "192.168.56.1"
# HOST = "127.0.1.1"

# TODO : Username отправить на сервер, а там его обработать


class Client:

    def __init__(self, username, is_private=False, companion_login=None):
        # Client main functions initialization
        self.username = username
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__connect__()
        self.encrypt_key = self.__calculate_key__(username)
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
                    sender, msg_text = data.decode("utf-8").split("::")
                    print(sender)
                    decrypted_msg = self.decrypt_msg(msg_text, sender)
                    time.sleep(0.2)
                    print(decrypted_msg)
                    self.messages_history.append(decrypted_msg)
            except Exception as _:
                pass

    def decrypt_msg(self, msg, sender):
        """Расшифровка сообщения"""
        decrypt_key = self.__calculate_key__(sender)
        decrypted_msg = ""
        for char in msg:
            decrypted_msg += chr(ord(char) ^ decrypt_key)
        return decrypted_msg

    def encrypt_msg(self, msg):
        """Шифровка сообщения"""
        encrypted_msg = str()
        for i in msg:
            encrypted_msg += chr(ord(i) ^ self.encrypt_key)
        return encrypted_msg

    def __connect__(self):
        """Функция, инициализирующая подключенеи к серверу"""
        host = HOST
        port = 0
        self.server = (host, 9090)
        self.sock.bind((host, port))
        self.sock.setblocking(False)
        self.sock.sendto(self.username.encode("utf-8"), self.server)

    @staticmethod
    def __calculate_key__(username):
        """Вычисление ключа шифрования по логину"""
        sum = 0
        mult = 1
        for char in username:
            sum += ord(char)
            mult *= ord(char)
        key = int((sum + mult) / 2) //110000
        return key

    def __compile_msg__(self, encrypted_msg):
        """Составление строки для отправки на сервер"""
        msg = str()
        msg += self.username
        msg += "::" + self.msg_receiver
        # print(self.companion_login)
        msg += "::" + self.companion_login
        msg += "::" + encrypted_msg
        return msg


login = input("Input login: ")
a = Client(login)
fl = True
while fl:
    msg = input()
    if msg == "exit":
        fl = False
    a.send_message(msg)
a.close_client()