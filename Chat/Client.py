import socket
import threading

print("------Cliente--------")
#nickname = input("Choose a nickname: ")
nickname = input("Escolha seu nome de usuario: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP_address = input("Forneça o IP da maquina: ")
Port = int(input("Forneça a porta da maquina: "))

client.connect((IP_address, Port))


def receive():
    """
    Funcao responsavel por receber as mensagens  servidor.

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
    Funcao responsavel por enviar a mensagem do cliente para o servidor.
    """
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))

receive_thread = threading.Thread(target=receive) # Cria uma thread para receber as mensagens enviadas do servidor
receive_thread.start()

write_thread = threading.Thread(target=write) # Cria uma thread para enviar mensagens do cliente para o servidor
write_thread.start()

