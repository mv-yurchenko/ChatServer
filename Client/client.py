#!/usr/bin/env python3

import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORTS = [i for i in range(65432, 66000)]         # The port used by the server
print(PORTS)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    for PORT in PORTS:
        try:
            s.connect((HOST, PORT))
            s.sendall(b'Hello, world')
            data = s.recv(1024)
        except Exception as _:
            pass
print('Received', repr(data))