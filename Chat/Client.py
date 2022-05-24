import socket
import threading
import sys

print("------Cliente--------")
#nickname = input("Choose a nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = sys.argv[1] 
hosthead = sys.argv[2] 
ping = -1
client.connect((hosthead, 8000))


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
    i = 0
    while i < 10:
        client.send("teste".encode('ascii'))
        i += 1
    client.send("teste".encode('fim'))

def connectHead():
    client.send(host.encode('ascii'))
    i = 0
    host = client.recv(1024).decode('ascii')
    getPing(client,host)
    porta = client.recv(1024).decode('ascii')
    return 1
connectHead()

