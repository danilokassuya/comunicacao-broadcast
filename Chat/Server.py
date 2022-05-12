import threading
import socket
import  sys

print("------Host--------")
IP = sys.argv[1]
PORTA = int(sys.argv[2])

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORTA))


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORTA))
server.listen()

clients = []    # Lista reponsavel por salver os clientes conectados
nicknames = []  # Lista responsavel por salver os nomes dos clientes 



def broadcast(message):
    """
    Função responsavel por mandar mensagens para todos os clientes conectados.

    Args: message : str
        Mensagem que deseja enviar para todos os clientes.

    """
    for client in clients:
        client.send(message)


def handle(client):
    """
    Função responsavel por controlar o objeto cliente. 
        - Geralmente está função será atribuida a uma Thread.

    Args: client : objeto cliente
        Objeto criado pelo modulo Client.py.

    Except: Caso o objeto não for encontrado ele será desalocado da nossa lista de clientes.

    """
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} saiu do chat!'.encode('ascii'))
            nicknames.remove(nickname)
            break

def receive():
    """
    Função responsavel por adicionar novos clientes ao servidor.
        - Irá receber novas solicitações de clientes e adicionar cada novo cliente a uma Thread.
    """
    while True:
        client, address = server.accept()
        print(f'Conectou com o ip {str(address)}')
        
        client.send('NICK'.encode('ascii')) 
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nome do cliente é {nickname}')
        broadcast(f'{nickname} entrou no chat'.encode('ascii'))
        client.send('Conectou-se ao server'.encode('ascii'))

        thead = threading.Thread(target=handle, args=(client,))
        thead.start()

print('Server está escutando...')
receive()