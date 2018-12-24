from Server.Server import Server
import sys
from Client.Client import Client

if len(sys.argv) > 1:
    client = Client(sys.argv[1])

else:
    server = Server()
    server.run()