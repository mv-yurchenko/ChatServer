import socket
import threading
from tkinter import messagebox
from tkinter import *
import time
from Cryptography.Cryptography import Cryptography

HOST = "192.168.0.13"
# HOST = "127.0.1.1"


TEST_CRYPTO_KEY = "Rh0xMeKP2lzezFWiNMUMV1KavMsQ4s_jjycIfZdVF6k="


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

        # По дефолту все сообщения паблик
        self.msg_receiver = "all"
        self.companion_login = "no"

        # Режим Private Talk (1 на 1)
        # TODO: Private
        self.is_private_talk = is_private
        if self.is_private_talk:
            self.msg_receiver = "private"
            self.companion_login = companion_login

        # GUI initialization
        self.gui_initialize()

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
        print("Thread started")
        while not self.stop_receiving:
            try:
                while True:
                    # Get data and address from received message
                    data, addr = self.sock.recvfrom(4096)
                    msg_time = self.__get_current_time__()

                    # Split and decrypt data
                    sender, msg_text = data.decode("utf-8").split("::")
                    decrypted_msg = self.__decrypt_msg__(msg_text.encode("utf-8"))

                    # TODO : Output function
                    self.messages_output.insert(END, self.format_message_for_output(sender, decrypted_msg))

                    # Add message to messages history
                    self.messages_history.append((msg_time, sender, decrypted_msg))

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

    def gui_initialize(self):

        # Initialize Client window
        self.window = Tk()
        self.window.title("ChatClient")
        self.window.geometry("800x600")

        # Definition of blocks size
        send_message_line_height = 25
        text_windows_width = 560
        second_column_start = 580
        second_column_width = 200

        # Window elements initialization

        self.message_input = Text(self.window)
        self.message_input.place(x=10, y=570, width=text_windows_width,
                                 height=send_message_line_height)

        self.send_message_button = Button(self.window, text="Send message", command=self.send_message_button_clicked)
        self.send_message_button.place(x=second_column_start, y=570,
                                       width=second_column_width, height=send_message_line_height)

        self.messages_output = Text(self.window)
        self.messages_output.place(x=10, y=10,
                                   width=text_windows_width, height=550)

        self.login_input = Text(self.window)
        self.login_input.place(x=second_column_start, y=10,
                               width=second_column_width, height=send_message_line_height)

        self.accept_login_button = Button(self.window, text="Accept Login", relief=GROOVE,
                                          command=self.accept_login_button_clicked)
        self.accept_login_button.place(x=second_column_start, y=50,
                                       width=second_column_width, height=send_message_line_height)

        self.window.mainloop()

    def accept_login_button_clicked(self):

        user_login = self.login_input.get("1.0", END)

        if not self.__is_login_input_empty__():
            print(user_login)
            self.messages_output.insert(END, "Welcome to Chat")
        else:
            messagebox.showerror("No login", "Input Login!")

    def __is_login_input_empty__(self) -> bool:
        return self.login_input.compare("end-1c", "==", "1.0")

    def send_message_button_clicked(self):
        self.send_message(self.message_input.get("1.0", END))
        # Clear message string after sending message
        self.message_input.delete("1.0", END)

    def format_message_for_output(self, sender: str, decrypted_msg: str) -> str:
        return self.__get_current_time__() + " : " + sender + " : " + decrypted_msg + "\n"


def main():
    a = Client("user")


if __name__ == '__main__':
    main()

