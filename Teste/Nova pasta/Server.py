from email import message
from ipaddress import ip_address
import threading
import socket
import sys

from matplotlib.pyplot import hist

"""
    Modulo responsavel por criar e controlar o Servidor
"""
print("-------SERVER--------")
host = sys.argv[1] 
port = int(sys.argv[2])
print("IP: "+ host +":" + str(port))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
port += 1000
clients = []    # Lista reponsavel por salver os clientes conectados
nicknames = []  # Lista responsavel por salver os nomes dos clientes 
historico = []

Port_to = "0000"
print("------- Conectar em outro Server --------")
#IP_address = input("Forneça o IP da maquina (Digite '0' caso não queria se conectar a outra servidor:")
IP_address = sys.argv[3]
if(ip_address != "0"):
    Port_to = int(sys.argv[4])
print(IP_address +":" + str(Port_to) )
Port_to += 1000



def sendToAnotherServer(message):
    """
    Função responsavel por mandar mensagens para outro servidor.

    Args: 
        message: str   Mensagem que deseja enviar para o servidor

    """
    serverAux2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        serverAux2.connect((IP_address, Port_to))
        serverAux2.send(message)
    except:
        print("Nao foi possivel enviar a mensagem para o outro servidor")
    
    serverAux2.close()

def broadcast(message):
    """
    Função responsavel por mandar mensagens para todos os clientes conectados.

    Args: 
        message: str    Mensagem que deseja enviar para todos os clientes.

    """
    print('enviado -> '+ message.decode('ascii'))
    mensagemAux = message.decode('ascii')
    sendToAnotherServer(mensagemAux.encode('ascii'))

    for client in clients:
        client.send(message)


def handle(client):
    """
    Função responsavel por controlar o objeto cliente. 
    
    Geralmente está função será atribuida a uma Thread.

    Args:
        client: objeto cliente - Objeto criado pelo modulo Client.py.

    Raises: 
        Caso o objeto não for encontrado ele será desalocado da nossa lista de clientes.

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
    Funcao responsavel por adicionar novos clientes ao servidor.
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

def handleServer(clientServer):
    """
    Funcao responsavel por controlar a comunicacao com outro servidor

    Args:
        clientServer: Objeto relacionado a o servidor conectado
        
    Raises: 
        Caso o objeto não for encontrado ele será desalocado o servidor

    """
    while True:
        try:
            message = clientServer.recv(1024).decode('ascii')
            if len(message) != 0:
                if message in historico:
                    #print("Mensagem já enviada")
                    historico.remove(message)
                else:
                    historico.append(message)
                    broadcast(message.encode('ascii'))
        except:
            print("Erro ocorreu no servidor")
            clientServer.close()
            break


def receiveServer():
    """
    Funcao responsavel receber mensagens de outro servidor
        
    Raises: 
        Caso o objeto não for encontrado ele será desalocado

    """
    serverAux = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Servidor de Recebimento -> " + host + ":" + str(port))
    serverAux.bind((host, port))
    serverAux.listen()
    while True:
        clientServer, addressServer = serverAux.accept()
        #print(f'Server conectado com o ip {str(addressServer)}')
        thead = threading.Thread(target=handleServer, args=(clientServer,))
        thead.start()
    
        

print('Server está escutando...')

receive_thread = threading.Thread(target=receiveServer) # Cria uma thread para receber as mensagens enviadas do servidor
receive_thread.start()

receive()