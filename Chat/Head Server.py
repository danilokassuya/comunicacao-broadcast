import socket
import threading
import sys

print("------Server Principal--------")
host = sys.argv[1] 
port = int(sys.argv[2])
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
disponivel = []
servers = []
porta = []
servers.append(host)
disponivel.append("sim")
porta.append(port)

def receive(server):
    """
    Funcao responsavel por receber as mensagens  servidor.

    """
    try:
        message = server.recv(1024).decode('ascii')
        servers.append(message)
        disponivel.append("sim")
        port += 1
        porta.append(port)
        i = 0
        for ser in servers:
            if(disponivel[i] == "sim"):
                server.send(ser.encode('ascii'))
                server.send(porta[i].encode('ascii'))
                i = i +1
        server.close()
    except:
        print("An error occured!")
        server.close()
        break

server.bind((host, port))
server.listen()
clientServer, addressServer = server.accept()
receive(clientServer)