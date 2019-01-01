from Client.Client import Client


class ClientUI:

    def __init__(self, username: str):
        self.client_obj = Client(username)
