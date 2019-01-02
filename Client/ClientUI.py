from Client.Client import Client
import time

VERSION = "1.1"


class ClientUI:

    def __init__(self, username: str):
        self.client_obj = Client(username)

    def print_header(self):
        print("ChatClient v" + VERSION)
        print("IP: " + self.client_obj.get_host())
        print(time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime()))
    