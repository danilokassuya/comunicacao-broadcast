import socket
import threading
import sys

print("------Cliente--------")
#nickname = input("Choose a nickname: ")
nickname = input("Escolha seu nome de usuario: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((sys.argv[1], 5000))
server.listen()

IP_address = sys.argv[1]
Port = int(sys.argv[2])

client.connect((IP_address, Port))

connectedTo = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def changeClientConnect(ip, porta):
    try:
        connectedTo.connect((ip, porta))
    except:
        connectedTo.close()
        connectedTo.connect((ip, porta))

def receive():
    """
    Função responsavel por receber as mensagens  servidor.
    """
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
                pass
            if message == "<IP>":
                message = client.recv(1024).decode('ascii')
                message = message.split(":")            
                changeClientConnect(message[0], int(message[1]))
            if message == "<MSG>":
                connectedTo
            else:
                print(message)
        except:
            print("An error occured!")
            client.close()
            break
    
def write():
    """
    Função responsavel por enviar a mensagem do cliente para o servidor.
    """
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))

receive_thread = threading.Thread(target=receive) # Cria uma thread para receber as mensagens enviadas do servidor
receive_thread.start()

write_thread = threading.Thread(target=write) # Cria uma thread para enviar mensagens do cliente para o servidor
write_thread.start()

