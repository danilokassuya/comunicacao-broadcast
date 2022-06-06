from genericpath import getsize
import threading
import sys
import socket

print("------Server Principal--------")
host = sys.argv[1] 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servers = []
porta = []
nicks = []
nova = 0

def receive(server):
    """
    Funcao responsavel por receber as mensagens  servidor.

    """
    message = server.recv(1024).decode('ascii')
    print(message)
    message = message.split()
    servers.append(message[0])
    nicks.append(message[1])
    nick = message[1]
    porta.append(message[2])
    while True:
        try:
            message = server.recv(1024).decode('ascii')
            i = len(nicks)
            i -= 1
            print(i)
            server.send(str(i).encode('ascii'))
            print(i)
            i = 0
            for ser in servers:
                if nicks[i] != nick:
                    server.send(nicks[i].encode('ascii'))
                    server.send(" ".encode('ascii'))
                    server.send(porta[i].encode('ascii'))
                    server.send(" ".encode('ascii'))
                    server.send(ser.encode('ascii'))
                    server.send(" ".encode('ascii'))
                else:
                    server.send(" ".encode('ascii'))
                    server.send(" ".encode('ascii'))
                    server.send(" ".encode('ascii'))
                i += 1
        except:
            print(nick+" desconectou")
            i = nicks.index(nick)
            del porta[i]
            del servers[i]
            print(i)
            nicks.remove(nick)
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