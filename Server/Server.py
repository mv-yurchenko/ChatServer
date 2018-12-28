import socket
import threading
import time

# Сервер соединяет n пользователей и ретранслирует сообщение одного пользователя всем остальным


class Server:
    """
    TODO
    """

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__initialize_server__()
        self.stop_signal = False
        self.clients = dict()

    def __initialize_server__(self):
        host = socket.gethostbyname(socket.gethostname())
        port = 9090
        self.sock.bind((host, port))

        print("Server started")
        print(self.__get_current_time__())
        print("Server host: ", host)
        print("Server port: ", port)
        self.__print_separate_line__()

    def main_loop(self):
        while not self.stop_signal:
            # Используем try для предотвращения остановки цикла в случае непредвиденных вылетов пользователей
            try:
                data, address = self.sock.recvfrom(4096)
                if address not in self.clients.values():
                    self.__new_user_connected__(address, data)

                # If it's not new user
                else:
                    msg_type, receiver_id, msg_text = self.__process_msg__(str(data))
                    print(msg_type)
                    # Message for all server
                    if msg_type == "all":
                        for client in self.clients.values():
                            print(type(client) == type(address))
                            if client != address:
                                print(client)
                                self.sock.sendto(msg_text.encode("utf-8"), client)

                    # Message for specific ID (User or char_room)
                    # Chat room coming soon

                    if msg_type == "private":
                        pass
                print(self.clients.values())

            except Exception as e:
                print(e)

    def __new_user_connected__(self, new_user_address, username):
        self.clients[username] = new_user_address
        print("New user connected")
        print("IP: ", new_user_address[0])
        print("PORT: ", new_user_address[1])
        self.__print_separate_line__()

    @staticmethod
    def __process_msg__(msg):
        msg_data = msg.split("::")
        msg_type = msg_data[1]
        msg_text = msg_data[3]
        if msg_type == "all":
            return msg_type, None, msg_text

        if msg_type == "private":
            return msg_type, msg_data[2], msg_text

    @staticmethod
    def __print_separate_line__():
        print("\n--------------------------------------------------\n")

    @staticmethod
    def __get_current_time__():
        return time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())


server = Server()
server.main_loop()