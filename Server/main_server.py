import socket

HOST = '127.0.1.1'  # Standard loopback interface address (localhost)
PORTS = [ i for i in range(60000, 65535)]        # Port to listen on (non-privileged ports are > 1023)
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
        data.split("/")
        print(data)            
        try:
            conn.sendall(str(data).encode())
        except Exception as e:
            print(e)