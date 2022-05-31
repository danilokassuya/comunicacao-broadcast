import socket
import threading
import sys
import time

print("------Cliente--------")
nickname = input("Choose a nickname: ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hosthead = sys.argv[1] 
client.connect((hosthead, 8000))#Head
clients = []
max = float(-1)
port = 0

def connectBest():
    while True:
        try:
            except:

def getBest():#Retorna o melhor no para o client se conectar
    client.send("p".encode('ascii'))
    nick = ""
    while True:
        message = client.recv(1).decode('ascii')
        if message == " ":
            break
        nick = nick + message
    porta = ""
    while True:
        message = client.recv(1).decode('ascii')
        if message == " ":
            break
        porta = porta + message
    ip = ""
    while True:
        message = client.recv(1).decode('ascii')
        if message == " ":
            break
        ip = ip + message
    if nick == "":
        print("Head")
    else:
        connectBest()

def Header():
    port = client.getsockname()
    message = host + " " + nickname + " " + str(port[1])
    print(message)
    client.send(message.encode('ascii'))# envia ip nick e porta
    while True:
        try:
            getBest()
        except:
            print("Um ocorreu conecção perdida com o Head")
            break


hostname = socket.gethostname()
host = socket.gethostbyname(hostname)
server.bind((host, 0))
server.listen()
port = server.getsockname()
connectHeadThread = threading.Thread(target=Header)
connectHeadThread.start()
while True:
    clientServer, addressServer = server.accept()
    clients.append(clientServer)
    messagerecvThread = threading.Thread(target=Header, args=(clientServer,))
    messagerecvThread.start()
