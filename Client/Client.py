import socket
import threading


class Client:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, adress):
        self.sock.connect((adress, 10000))

        client_thread = threading.Thread(target=self.send_message())
        client_thread.daemon = True
        client_thread.start()
        while True:
            data = self.sock.recv(4096)
            if not data:
                break
            print(data)

    def send_message(self):
        self.sock.send(bytes(input(), 'utf-8'))
