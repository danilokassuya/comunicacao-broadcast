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
client.connect((hosthead, 8000))
max = float(-1)
port = 0
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

def getPing(host):
    hosts = []
    portas = []
    client.send("ping".encode('ascii'))
    message = client.recv(1024).decode('ascii')
    while message != "fim":
        message = message.split()
        hosts.append(message[0])
        portas.append(message[1])
        message = client.recv(68).decode('ascii')
    i = 0
    for host in hosts:
        serveraux = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serveraux.connect((host,int(portas[i])))
        start = time.time()
        serveraux.send("t".encode('ascii'))
        message = serveraux.recv(1024)
        ping = sys.argv[3]
        #ping = time.time()-start
        i += 1
        time.sleep(10)
def connectHead(host):
    """ Conecta com o server de entrada e executa as funções para achar o client com melhor ping """
    port = server.getsockname()
    print(port)
    while port[1] == 0:
        port = server.getsockname()
    message = host + " " + nickname + " " + str(port[1])
    client.send(message.encode('ascii'))# envia ip nick e porta
    getPing(host)
    print("saiu do getPing")
    #return 1

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
                print(message)
            else: 
                if message == "t":
                    server.send("teste".encode('ascii'))
            #else: if mensagem verifica ip destino esse ou repassa
        except Exception as e:
            print("Usuario desconectou")
            break

def write(server):
    """
    Função responsavel por enviar a mensagem do cliente para o servidor.
    """
    while True:
        message = f'{nickname}: {input("")}'
        try:
            server.send("r".encode('ascii'))
            server.send(message.encode('ascii'))
        except:
            print("nao foi possivel enviar a mensagem")
            break

hostname = socket.gethostname()
host = socket.gethostbyname(hostname)
server.bind((host, 0))
server.listen()
connectHeadThread = threading.Thread(target=connectHead, args=(host,))
connectHeadThread.start()
print("teste aqui")
port = server.getsockname()
print("teste aqui 2")
while True:
    print("teste aqui 2")
    clientServer, addressServer = server.accept()
    print("teste aqui 3")
    messagerecvThread = threading.Thread(target=messagerecv, args=(clientServer,))
    write_thread = threading.Thread(target=write, args=(clientServer,)) # Cria uma thread para enviar mensagens do cliente para o servidor
    write_thread.start()
    print("teste aqui 3")
    messagerecvThread.start()


