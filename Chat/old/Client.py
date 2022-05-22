from re import M
import socket
import threading
import subprocess
import sys
from traceback import print_tb



client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORTA))
#hostname = socket.gethostname()
#nickname = socket.gethostbyname(hostname)

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

def help():
    print("---------------------------- HELP ----------------------------")
    print("/listar\n\tComando responsavel por listar todos os aparelhos conectados na rede.\n\tExemplo: /listar\n")
    print("/enviar <id> <mensagem>\n\tComando responsavel por enviar uma mensagem para um outro computador.\n\t\t- <id>:  Id do computador destino.\n\t\t- <mensagem>: Mensagem a ser enviada\n\tExemplo: /enviar 1 Teste de mensagem.")


def write():
    """
    Função responsavel por enviar a mensagem do cliente para o servidor.
    """
    while True:
        menssagem = f'{input("Comando: ")}'
        if "/help" in menssagem:
            help()
        client.send(menssagem.encode('ascii'))
print("Digite /help para ver todos os comandos")

receive_thread = threading.Thread(target=receive) # Cria uma thread para receber as mensagens enviadas do servidor
receive_thread.start()

write_thread = threading.Thread(target=write) # Cria uma thread para enviar mensagens do cliente para o servidor
write_thread.start()
