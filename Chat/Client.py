import socket
import threading
import os
import sys

print("------Cliente--------")
IP = sys.argv[1]
PORTA = int(sys.argv[2])

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORTA))
hostname = socket.gethostname()
nickname = socket.gethostbyname(hostname)

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

