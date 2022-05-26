import socket
import threading
import sys
import time

print("------Cliente--------")
#nickname = input("Choose a nickname: ")
nickname = sys.argv[2] 
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hosthead = sys.argv[1] 
client.connect((hosthead, 8000))#Head
clients = []
max = float(-1)
port = 0
def receive(client):
    """
    Funcao responsavel por receber as mensagens  servidor.

    """
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            print(message)
        except:
            print("An error occured!")
            client.close()
            getPing()
            break

def getPing():
    hosts = []
    portas = []
    client.send("ping".encode('ascii'))
    message = client.recv(19).decode('ascii')
    print(message)
    while message != "fim":
        message = message.split()
        hosts.append(message[0])
        portas.append(message[1])
        message = client.recv(19).decode('ascii')
    i = 0
    bestPing = -1
    for host in hosts:
        serveraux = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serveraux.connect((host,int(portas[i])))
        start = time.time()
        serveraux.send("t".encode('ascii'))
        message = serveraux.recv(5)
        #ping = time.time()-start
        ping = sys.argv[3]
        if bestPing == -1:
            bestServer = serveraux
            bestPing = ping
        if bestPing > ping:
            bestServer = serveraux
            bestPing = ping
        i += 1
    print(bestPing)
    if bestPing == -1:
        return
    receive(bestServer)
def connectHead():
    """ Conecta com o server de entrada e executa as funções para achar o client com melhor ping """
    port = server.getsockname()
    print(port)
    while port[1] == 0:
        port = server.getsockname()
    message = host + " " + nickname + " " + str(port[1])
    client.send(message.encode('ascii'))# envia ip nick e porta
    getPing()
    return 1

def messagerecv(server):
    """ 
    Trata os clientes conectados com esse usuario
    Printa ou redireciona as mensagens recebidas 
    """
    global max
    while True:
        try:
            message = server.recv(1).decode('ascii')
            if message == "r":
                message = server.recv(1024).decode('ascii')
            else: 
                if message == "t":
                    server.send("teste".encode('ascii'))
            #else: if mensagem verifica ip destino esse ou repassa
        except Exception as e:
            print(message)
            print("Usuario desconectou")
            break

def write(clientServer):
    """
    Função responsavel por enviar a mensagem do cliente para o servidor.
    """
    while True:
        message = f'{nickname}: {input("")}'
        try:
            for client in clients:
                #print(socket.getsockname(client))
                client.send("r".encode('ascii'))
                client.send(message.encode('ascii'))
        except:
            print("nao foi possivel enviar a mensagem")
            break

hostname = socket.gethostname()
host = socket.gethostbyname(hostname)
server.bind((host, 0))
server.listen()
connectHeadThread = threading.Thread(target=connectHead)
connectHeadThread.start()
port = server.getsockname()
while True:
    clientServer, addressServer = server.accept()
    print("conectado")
    clients.append(clientServer)
    messagerecvThread = threading.Thread(target=messagerecv, args=(clientServer,))
    messagerecvThread.start()
    write_thread = threading.Thread(target=write, args=(client,)) # Cria uma thread para enviar mensagens do cliente para o servidor
    write_thread.start()


