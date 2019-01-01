import socket
import threading
import time
from Cryptography.Cryptography import Cryptography

HOST = "192.168.56.1"
# HOST = "127.0.1.1"

TEST_CRYPTO_KEY = "Rh0xMeKP2lzezFWiNMUMV1KavMsQ4s_jjycIfZdVF6k="


class Client:

    def __init__(self, username, is_private=False, companion_login=None):
        # Client main functions initialization
        self.username = username
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__connect__()
        self.cryptography = Cryptography(TEST_CRYPTO_KEY.encode("utf-8"))
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
        encrypted_msg = self.cryptography.encrypt_string(msg)
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
                    decrypted_msg = self.__decrypt_msg__(msg_text.encode("utf-8"))
                    time.sleep(0.2)
                    print(decrypted_msg)
                    self.messages_history.append(decrypted_msg)
            except Exception as _:
                pass

    def __decrypt_msg__(self, encrypted_msg):
        return self.cryptography.decrypt_string(encrypted_msg)

    def __connect__(self):
        """Функция, инициализирующая подключенеи к серверу"""
        host = HOST
        port = 0
        self.server = (host, 9090)
        self.sock.bind((host, port))
        self.sock.setblocking(False)
        self.sock.sendto(self.username.encode("utf-8"), self.server)

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