from re import M
import socket
import threading
import subprocess
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
    
    maximo = int('-1')
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
                pass
            else:
                if message == 'fim':
                    print(destino)
                    client.send(destino.encode('ascii'))
                    print("teste")
                else:
                    print("test23")
                    ping = subprocess.getoutput("ping "+message).split('M‚dia = ')
                    teste = ping[1].split('ms')
                    laten = int(teste[0])
                    if maximo == -1:
                        maximo = laten
                        destino = message
                    if laten < maximo:
                        maximo = laten
                        destino = message
                    print(laten)
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

#write_thread = threading.Thread(target=write) # Cria uma thread para enviar mensagens do cliente para o servidor
#write_thread.start()
