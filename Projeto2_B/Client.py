import socket
import threading
import sys
import time
import traceback

print("------Cliente--------")
nickname = input("Choose a nickname: ")
head = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
semaforo = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hosthead = sys.argv[1] 
head.connect((hosthead, 8000))#Head
semaforo.connect((hosthead, 8005))
clients = []
max = float(-1)
port = 0
def prodcons():
    while True:
        message = input()
        if message == "consumir":
            semaforo.send(message.encode('ascii'))
        else :
            if message == "produzir":
                semaforo.send(message.encode('ascii'))
def connectBest(ip,porta):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, int(porta)))
    client.send("a".encode('ascii'))
    ProdConsThread = threading.Thread(target=prodcons)
    ProdConsThread.start()
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            print(message)
            for cli in clients:
                cli.send(message.encode('ascii'))
        except Exception as e:
            print("Desconectado com o node Server")
            break

def getBest():#Retorna o melhor no para o client se conectar
    while True:
        try:
            head.send("p".encode('ascii'))
            i = head.recv(1).decode('ascii')
            while i != "p":
                i = head.recv(1).decode('ascii')
            i = head.recv(100).decode('ascii')
            i = int(i)
            head.send("p".encode('ascii'))
            nick = ""
            bestping = -1
            while i > 0:
                nick = ""
                while True:
                    message = head.recv(1).decode('ascii')
                    if message == " ":
                        break
                    nick = nick + message
                if nick == "head":
                    break
                porta = ""
                while True:
                    message = head.recv(1).decode('ascii')
                    if message == " ":
                        break
                    porta = porta + message
                ip = ""
                while True:
                    message = head.recv(1).decode('ascii')
                    if message == " ":
                        break
                    ip = ip + message
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((ip, int(porta)))
                start = time.time()
                client.send("p".encode('ascii'))
                message = client.recv(1).decode('ascii')
                ping = time.time() - start
                if bestping == -1:
                    bestping = ping
                    bestnick = nick
                    bestip = ip
                    bestporta = porta
                else:
                    if ping < bestping:
                        bestping = ping
                        bestnick = nick
                        bestip = ip
                        bestporta = porta
                client.close()
                i -= 1
                print("aqui2")
            if nick == "" or nick == "head":
                print("Head")
                Message()
            else:
                print(bestnick)
                connectBest(bestip,bestporta)
        except Exception as e:
            print(traceback.format_exc())
            print(e)
            print("Procurando novo host")
def Header():
    while True:
        try:
            message = host + " " + nickname + " " + str(port[1])
            head.send(message.encode('ascii'))# envia ip nick e porta
            getBest()
        except Exception as e:
            print(e)
            print("Um ocorreu conec????o perdida com o Head")
            break
def Message():
    while True:
        try:
            message = input()
            if message == "consumir":
                semaforo.send(message.encode('ascii'))
            else :
                if message == "produzir":
                    semaforo.send(message.encode('ascii'))
            for cli in clients:
                cli.send(message.encode('ascii'))
        except Exception as e:
            print(e)
            print("Conex??o perdida com algum host")
            break

hostname = socket.gethostname()
host = socket.gethostbyname(hostname)
server.bind((host, 0))
server.listen()
port = server.getsockname()
print(port)
connectHeadThread = threading.Thread(target=Header)
connectHeadThread.start()
while True:
    clientServer, addressServer = server.accept()
    message = clientServer.recv(1).decode('ascii')
    clientServer.send(message.encode('ascii'))
    if message == "a":
        clients.append(clientServer)
