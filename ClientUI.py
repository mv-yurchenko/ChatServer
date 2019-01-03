from Client.Client import Client
import time
import os
import platform


VERSION = "1.1"


class ClientUI:

    def __init__(self):
        self.print_header(first_print=True)
        self.username = input("Input username: ")
        self.mode = None
        self.companion = None
        self.input_client_mode()
        self.client_obj = Client(self.username, is_private=self.mode == "private", companion_login=self.companion)

    def print_header(self, first_print = False):
        print("ChatClient v" + VERSION)
        if not first_print:
            # В первый раз порта нет, так как клиент еще не инициализирован
            print("IP: " + self.client_obj.get_host())
        print(time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime()))

    def input_client_mode(self):
        is_public = bool(input("Is public (1 or 0) : "))
        if not is_public:
            self.mode = "private"
            self.companion = str(input("Input companion login"))
        else:
            self.mode = "public"

    def main_print_loop(self):
        exit = False
        while not exit:
            self.__clear_screen__()
            self.print_header()
            print(self.client_obj.get_messages_list())
            time.sleep(2)

    @staticmethod
    def __clear_screen__():
        if platform.system() == "Windows":
            os.system("cls")
        if platform.system() == "Linux":
            os.system("clear")


a = ClientUI()
a.main_print_loop()
