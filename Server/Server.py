import socket
import threading
import time

# Сервер соединяет n пользователей и ретранслирует сообщение одного пользователя всем остальным
#   TODO : Удаление отключенных пользователей из рассылки (проверка на активность?)


class Server:

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__initialize_server__()
        self.stop_signal = False
        self.clients = dict()

    def __initialize_server__(self):
        self.host = socket.gethostbyname(socket.gethostname())
        port = 9090
        self.sock.bind((self.host, port))

        print("Server started")
        print(self.__get_current_time__())
        print("Server host: ", self.host)
        print("Server port: ", port)
        self.__print_separate_line__()

    def main_loop(self):
        while not self.stop_signal:
            # Используем try для предотвращения остановки цикла в случае непредвиденных вылетов пользователей
            try:
                data, address = self.sock.recvfrom(4096)
                if address not in self.clients.values():
                    self.__new_user_connected__(address, data)
                    self.sock.sendto(str(self.clients), address)

                # If it's not new user
                else:
                    sender, msg_type, receiver_id, msg_text = self.__process_msg__(data.decode("utf-8"))
                    self.__print_info_about_msg__(sender, msg_type, receiver_id, msg_text)

                    # Message for all server
                    if msg_type == "all":
                        self.__send_msg_type_all__(sender, msg_text, address)

                    # Message for specific ID (User or char_room)
                    # Chat room coming soon
                    if msg_type == "private":
                        pass

            except Exception as e:
                print(e)

    def __send_msg_type_all__(self, sender, msg_text, address):
        # Variable to catch disconnected clients
        disconnected_client = None
        try:
            for client in self.clients.values():
                # If sending data will be successful, client won't be disconnected
                disconnected_client = client
                msg = sender + "::" + msg_text
                if client != address:
                    self.sock.sendto(msg.encode("utf-8"), client)

        except Exception as e:
            # Disconnect client if sending failed
            self.clients = {key: val for key, val in self.clients.items() if val != client}

    def __send_msg_type_private(self, sender, msg_text, receiver):
        pass

    def __print_info_about_msg__(self, *msg_info):
        sender, msg_type, receiver_id, msg_text = msg_info
        print("New message")
        print("Sender: ", sender)
        print("Message type: ", msg_type)
        print("Encrypted message text: ", msg_text)
        print("Receiver id: ", receiver_id)
        self.__print_separate_line__()

    def __new_user_connected__(self, new_user_address, username : bytes):
        self.clients[username] = new_user_address
        print("New user connected")
        print("Username: ", username.decode("utf-8"))
        print("IP: ", new_user_address[0])
        print("PORT: ", new_user_address[1])
        self.__print_separate_line__()

    @staticmethod
    def __process_msg__(msg):
        msg_data = msg.split("::")
        sender = msg_data[0]
        msg_type = msg_data[1]
        msg_text = msg_data[3]
        if msg_type == "all":
            return sender, msg_type, None, msg_text

        if msg_type == "private":
            return sender, msg_type, msg_data[2], msg_text

    @staticmethod
    def __print_separate_line__():
        print("\n--------------------------------------------------\n")

    @staticmethod
    def __get_current_time__():
        return time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())

    def get_host(self):
        return self.host


server = Server()
server.main_loop()