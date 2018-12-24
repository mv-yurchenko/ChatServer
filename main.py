from Server.Server import Server
import sys


if len(sys.argv) > 1:
    pass

else:
    server = Server()
    server.run()