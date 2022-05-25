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
servers.append(host)
disponivel.append("sim")
nova = 0
def receive(server):
    """
    Funcao responsavel por receber as mensagens  servidor.

    """
    while True:
        try:
            nova = 1
            message = server.recv(1024).decode('ascii')
            servers.append(message)
            disponivel.append("sim")
            message = server.recv(1024).decode('ascii')
            nicks.append(message)
            print("aqui")
            porta.append(port)
            i = 0
            for ser in servers:
                if(disponivel[i] == "sim"):
                    server.send(ser.encode('ascii'))
                    server.send(porta[i].encode('ascii'))
                    i = i +1
            nova = 1
        except socket.timeout:
            print("Alguma mensagem foi perdida")
            server.close()
            break
        except:
            print("An error occured!")
            server.close()
            break
server.bind((host, 8000))
server.listen()
server.settimeout(5)
print("Ip e porta do server principal")
print(server.getsockname())
port = server.getsockname()
while True:
    clientServer, addressServer = server.accept()
    receive_thread = threading.Thread(target=receive, args=(clientServer,))
    receive_thread.start()