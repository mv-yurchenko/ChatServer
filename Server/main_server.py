import socket
from signal import signal, SIGPIPE, SIG_DFL
from time import sleep
signal(SIGPIPE, SIG_DFL)

HOST = '127.0.1.1'  # Standard loopback interface address (localhost)
PORTS = [i for i in range(60000, 65535)]        # Port to listen on (non-privileged ports are > 1023)
LIST_OF_LOGINS = list()
for PORT in PORTS:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    print(PORT)
    with conn:
        print('Connected by', addr)
        data = str(conn.recv(1024))
        data = data.split("/")
        user_login = data[0][2:]
        if user_login not in LIST_OF_LOGINS:
            LIST_OF_LOGINS.append(user_login)
        else:
            try:
                msg = str("Welcome back " + user_login).encode()
                print(msg)
                s.sendall(msg)
            except Exception as e:
                print(e)
        print(user_login)
        # try:
        #     conn.sendall(str(data).encode())
        # except Exception as e:
        #     print(e)
        # finally:
        #     print(LIST_OF_LOGINS)
    s.close()
