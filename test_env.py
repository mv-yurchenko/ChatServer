from Client.Client import Client

login = input("Input login: ")
a = Client(login)
fl = True
while fl:
    msg = input()
    if msg == "exit":
        fl = False
    a.send_message(msg)
a.close_client()