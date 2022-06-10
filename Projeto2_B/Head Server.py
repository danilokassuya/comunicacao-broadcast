from genericpath import getsize
from imp import acquire_lock
import threading
import sys
import socket
import time
import traceback

print("------Server Principal--------")
host = sys.argv[1] 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servers = []
porta = []
nicks = []
head = ""
nova = 0

def receive(server):
    """
    Funcao responsavel por receber as mensagens  servidor.

    """
    message = server.recv(1024).decode('ascii')
    message = message.split()
    servers.append(message[0])
    nicks.append(message[1])
    nick = message[1]
    porta.append(message[2])
    global head
    while True:
        try:
            message = server.recv(1).decode('ascii')
            print(nick+" "+message)
            while message != "p":
                message = server.recv(1).decode('ascii')
            server.send("p".encode('ascii'))
            i = len(nicks)
            i -= 1
            if i == 0:
                head = nicks[0]
            server.send(str(i).encode('ascii'))
            message = server.recv(1).decode('ascii')
            i = 0
            for ser in servers:
                if head == nick:
                    print("Novo head "+head)
                    server.send("head".encode('ascii'))
                    server.send(" ".encode('ascii'))
                    break
                if nicks[i] != nick:
                    print(nicks[i])
                    server.send(nicks[i].encode('ascii'))
                    server.send(" ".encode('ascii'))
                    server.send(porta[i].encode('ascii'))
                    server.send(" ".encode('ascii'))
                    server.send(ser.encode('ascii'))
                    server.send(" ".encode('ascii'))
                i += 1
        except Exception as e:
            print(nick+" desconectou")
            i = nicks.index(nick)
            del porta[i]
            del servers[i]
            nicks.remove(nick)
            head = nicks[0]
            server.close()
            break
server.bind((host, 8000))
server.listen()
print("Ip e porta do server principal")
print(server.getsockname())
port = server.getsockname()
while True:
    clientServer, addressServer = server.accept()
    receive_thread = threading.Thread(target=receive, args=(clientServer,))
    receive_thread.start()