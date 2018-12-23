import socket

HOST = ''  # Standard loopback interface address (localhost)
PORTS = [ i for i in range(65433, 66000)]        # Port to listen on (non-privileged ports are > 1023)

for PORT in PORTS:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    print(PORT)
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)