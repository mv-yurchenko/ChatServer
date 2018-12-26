import socket
import threading


class Server:
    """
    TODO
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self):
        self.sock.bind(("0.0.0.0", 10000))
        self.sock.listen(1)
        self.connections = list()

    def handler(self, conn, a):
        while True:
            data = conn.recv(4096)
            for connection in self.connections:
                connection.send(data)
            if not data:
                break

    def run(self):
        while True:
            conn, adr = self.sock.accept()
            conn_thread = threading.Thread(target=self.handler, args=(conn, adr))
            conn_thread.daemon = True
            conn_thread.start()
            self.connections.append(conn)
            print(self.connections)
