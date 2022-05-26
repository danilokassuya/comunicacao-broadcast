import threading
import socket
import sys

"""
    Modulo responsavel por criar e controlar o Servidor
"""
print("-------SERVER--------")
host = sys.argv[1] 
port = int(sys.argv[2])
print("IP: "+ host +":" + int(port))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
port += 1000

clients = []    # Lista reponsavel por salver os clientes conectados
nicknames = []  # Lista responsavel por salver os nomes dos clientes 
historico = []
listaIps = []

def multicast(message):
    """
    Função responsavel por mandar mensagens para todos os clientes conectados.

    Args: message : str
        Mensagem que deseja enviar para todos os clientes.

    """
    print('enviado -> '+ message.decode('ascii'))
    mensagemAux = message.decode('ascii')
    
    for client in clients:
        client.send(message)

def resend():
    for i in len(clients):
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
            multicast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            multicast(f'{nickname} saiu do chat!'.encode('ascii'))
            nicknames.remove(nickname)
            ipAux = listaIps(index)
            listaIps.remove(ipAux)
            resend()
            break

def receive():
    """
    Função responsavel por adicionar novos clientes ao servidor.
        - Irá receber novas solicitações de clientes e adicionar cada novo cliente a uma Thread.
    """
    while True:
        client, address = server.accept()
        print(f'Entrou na rede com o ip {str(address)}')
        
        client.send('NICK'.encode('ascii'))
        
        nickname = client.recv(1024).decode('ascii')
        listaIps.append(address)
        nicknames.append(nickname)
        clients.append(client)
        
        print(f'Nome do cliente é {nickname}')
        #broadcast(f'{nickname} entrou no chat'.encode('ascii'))
        client.send('Conectou-se ao server'.encode('ascii'))

        thead = threading.Thread(target=handle, args=(client,))
        thead.start()





print('Server está escutando...')

receive()