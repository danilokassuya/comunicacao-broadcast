import threading
import sys
import socket

print("------Server Principal--------")
host = sys.argv[1] 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
disponivel = []
servers = []
porta = []
nicks = []
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
    while True:
        try:
            message = server.recv(1024).decode('ascii')
            if message == "ping":
                i = 0
                for ser in servers:
                    if(nicks[i] != nick):
                        ipPorta = ser + " " + porta[i]
                        print(sys.getsizeof(ipPorta))
                        server.send(ipPorta.encode('ascii'))
                        i = i + 1
            server.send("fim".encode('ascii'))
        except socket.timeout:
            print("Alguma mensagem foi perdida")
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