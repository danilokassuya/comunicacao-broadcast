import threading
import socket
import  sys

print("------Host--------")
IP = sys.argv[1]
PORTA = int(sys.argv[2])

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORTA))
server.listen()

clients = []    # Lista reponsavel por salver os clientes conectados
nicknames = []  # Lista responsavel por salver os nomes dos clientes 
listaConec = []


def sendMessage(nick, message):
    """
    Função responsavel por mandar mensagens para todos os clientes com um nome especifico.

    Args: message : str
        nick : str
        Mensagem que deseja enviar para todos os clientes.

    """
    position = nicknames.index(nick.capitalize())
    clients[position].send(message.encode('ascii'))
    

def sendAllClientsConnected(nick):
    """
    Função responsavel por listar todos os clientes conectados

    Args: message : str
        nick : str
        Mensagem que deseja enviar para todos os clientes.

    """
    mensagem = ""
    i = 0
    for nickname in nicknames:
        mensagem += f"{i} - {nickname}\n"
        print(mensagem)
        i += 1
    sendMessage(nick, mensagem)


def sendToComputer(sender, comando):
    comando = comando.split

    if(len(comando) < 3):
        return
    
    receiver = comando[1].capitalize()
    try:
        receiver = int(receiver)
    except:
        sendMessage(sender, "ERRO nos Parametros no comando /enviar.")
        return


    if receiver > len(nicknames):
        sendMessage(sender, "ERRO id não existe.")
        return
    
    mensagem = ' '.join(comando[2:])
    mensagem = sender + ": " + mensagem
    print("Debug | " + mensagem)
    nickname = nicknames[receiver]
    sendMessage(nickname, mensagem)
    sendMessage(sender, "Mensagem enviado com sucesso.")
    
    

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
            messagem = client.recv(1024).decode('ascii')
            print(f"Server recebeu {messagem}")
            index = clients.index(client)
            nickname = nicknames[index]
            if messagem == "/listar":
                sendAllClientsConnected(nickname)
            if "/enviar" in messagem: # /enviar <idDoComputador> <Mensagem>
                sendToComputer(nickname, messagem)
            #broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            #listaConec.append(listaConec[index]) 
            #broadcast(f'{nickname} saiu do chat!'.encode('ascii')) # apenas para teste
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
        nicknames.append(nickname.capitalize())
        clients.append(client)

        print(f'Nome do cliente é {nickname}')
        broadcast(f'{nickname} entrou no chat'.encode('ascii'))

        thead = threading.Thread(target=handle, args=(client,))
        thead.start()

print('Server está escutando...')
receive()