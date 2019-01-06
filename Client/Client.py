import socket
import tkinter as tk
import threading
import time
from Cryptography.Cryptography import Cryptography
from queue import Queue

HOST = "192.168.0.13"
# HOST = "127.0.1.1"


TEST_CRYPTO_KEY = "Rh0xMeKP2lzezFWiNMUMV1KavMsQ4s_jjycIfZdVF6k="


# TODO:Fix global host


class Client:

    def __init__(self, username, is_private=False, companion_login=None, host=HOST):
        # Client main functions initialization
        self.username = username
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__connect__()
        self.cryptography = Cryptography(TEST_CRYPTO_KEY.encode("utf-8"))
        self.stop_receiving = False
        self.receiving_thread = threading.Thread(target=self.receiving)
        self.receiving_thread.start()
        self.messages_history = list()
        self.host = host
        self.GUI_connector = Queue()

        self.top = tk.Tk()
        self.tex = tk.Text(master=self.top)
        self.tex.pack(side=tk.RIGHT)
        self.top.mainloop()

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
        self.receiving_thread.join()
        self.sock.close()
        return 0

    def send_message(self, msg: str):
        """Шифрование сообщения и отправка на сервер """
        if not isinstance(msg, str):
            raise TypeError("")
        encrypted_msg = self.cryptography.encrypt_string(msg)
        msg = self.__compile_msg__(encrypted_msg)
        self.sock.sendto(msg, self.server)
        return 0

    def receiving(self):
        """Функиця непрерывного получения данных с сервера в отдельном потоке"""
        while not self.stop_receiving:
            try:
                while True:
                    data, addr = self.sock.recvfrom(4096)
                    msg_time = self.__get_current_time__()
                    sender, msg_text = data.decode("utf-8").split("::")
                    print(sender)
                    decrypted_msg = self.__decrypt_msg__(msg_text.encode("utf-8"))
                    time.sleep(0.2)
                    print(decrypted_msg)
                    self.tex.insert(tk.END, decrypted_msg)
                    # Add time for output
                    self.messages_history.append((msg_time, sender, decrypted_msg))
                    self.GUI_connector.put(self.messages_history)
            except Exception as _:
                pass

    def __decrypt_msg__(self, encrypted_msg):
        return self.cryptography.decrypt_string(encrypted_msg)

    def __connect__(self):
        """Функция, инициализирующая подключенеи к серверу"""
        port = 0
        self.server = (HOST, 9090)
        self.sock.bind((HOST, port))
        self.sock.setblocking(False)
        self.sock.sendto(self.username.encode("utf-8"), self.server)

    def __compile_msg__(self, encrypted_msg) -> bytes:
        """Составление строки для отправки на сервер"""
        msg = str()
        msg += self.username
        msg += "::" + self.msg_receiver
        # print(self.companion_login)
        msg += "::" + self.companion_login
        msg += "::" + encrypted_msg
        return msg.encode("utf-8")

    def get_host(self):
        return self.host

    def get_messages_data(self) -> list:
        return self.messages_history

    @staticmethod
    def __get_current_time__() -> str:
        return time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())

    def get_gui_connector(self):
        return self.GUI_connector