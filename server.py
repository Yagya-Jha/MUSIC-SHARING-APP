import socket
from threading import Thread
import os
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

SERVER = None
PORT = 8050
IP_ADDRESS = '127.0.0.1'
BUFFER_SIZE = 4096
clients = {}

is_dir_exists = os.path.isdir('shared_files')
print(is_dir_exists)
if(not is_dir_exists):
    os.makedirs('shared_files')

def handleClient(client,client_name):
    pass

def acceptConnections():
    global SERVER
    global clients

    while True:
        client, addr = SERVER.accept()

        client_name = client.recv(4096).decode().lower()
        clients[client_name] = {
            "client" : client,
            "address": addr,
            "connected_with":"",
            "file_name":"",
            "file_size":4096
        }

        print(f"Connection established with {client_name} : {addr}")

        thread = Thread(target = handleClient, args = {client,client_name})
        thread.start()

def ftp():
    global IP_ADDRESS

    authorizer = DummyAuthorizer()
    authorizer.add_user("lftpd","lftpd",".",perm="elradfmw")

    handler = FTPHandler
    handler.authorizer = authorizer

    ftp_server = FTPServer((IP_ADDRESS,21),handler)
    ftp_server.serve_forever()

def setup():
    print("\n\t\t\t\t\t\t MUSIC SENDER\n")

    global SERVER
    global PORT
    global IP_ADDRESS

    SERVER = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS,PORT))
    SERVER.listen(100)

    print("\t\t\t\tSERVER IS WAITING FOR INCOMING CONNECTIONS....")

    acceptConnections()

thread = Thread(target=setup)
thread.start()

ftp_thread = Thread(target=ftp)               #receiving multiple messages
ftp_thread.start()
