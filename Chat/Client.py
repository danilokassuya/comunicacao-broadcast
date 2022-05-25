import socket
import threading
import sys

print("------Cliente--------")
#nickname = input("Choose a nickname: ")
nickname = "algo"
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hosthead = sys.argv[1] 
client.connect((hosthead, 8000))
max = -1
def receive():
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
            break
    
def write():
    """
    Funcao responsavel por enviar a mensagem do cliente para o servidor.
    """
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))

def getPing(client,host):
    hosts = []
    portas = []
    message = client.recv(1024)
    while message != "fim":
        hosts.append(message)
        message = client.recv(1024)
        portas.append(message)
        message = client.recv(1024)
    i = 0
    for host in host:
        serveraux = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serveraux.connect(host,portas[i])
        i += 1
    serveraux.send("teste".encode('fim'))

def connectHead(host):
    client.send(host.encode('ascii'))# envia IP
    client.send(nickname.encode('ascii'))# envia nick do client
    getPing(client,host)
    porta = client.recv(1024).decode('ascii')
    return 1
def waitConnect(server):
    port = server.getsockname()
    clientServer, addressServer = server.accept()
    messagerecv = threading.Thread(target=messagerecv, args=(clientServer,))
    messagerecv.start()

def messagerecv(server):
    ping = -1
    while True:
        try:
            message = server.recv(1024).decode('ascii')
            print(message)
            if message == "ping":
                message = server.recv(1024).decode('ascii')
                ping = int(message)
                checkping = threading.Thread(target=checkping, args=(ping,server))
                checkping.start()
            else: 
                if message == "teste":
                    server.send("teste".encode('ascii'))
            #else: if mensagem verifica ip destino esse ou repassa
        except:
            print("Erro ocorrido")
            break
def checkping(ping,server):
    while True:
        if ping > max:
            server.close()
            break

waitConnect = threading.Thread(target=waitConnect, args=(server,))
waitConnect.start()
hostname = server.gethostname()
host = server.gethostbyname(hostname)
connectHead(host)

