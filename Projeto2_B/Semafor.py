
from genericpath import getsize
from imp import acquire_lock
import threading
import sys
import socket
import time
import traceback

host = sys.argv[1] 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servers = []
porta = []
nicks = []
memoria = []
head = ""
nova = 0
semaforo = 0

def init_sem(server):
    while True:
        print("novo client")
        global semaforo
        message = server.recv(1024).decode('ascii')
        while True:
            if semaforo == 0:
                semaforo = 1
                if message == "consumir":
                    consome()
                    semaforo = 0
                    break
                else:
                    produz()   
                    semaforo = 0
                    break
def produz():
    print("Produz")
    memoria.append(1)
    print(memoria)
def consome():
    print("Consume")
    memoria.pop()
    print(memoria)
server.bind((host, 8005))
server.listen()
while True:
    clientServer, addressServer = server.accept()
    receive_thread = threading.Thread(target=init_sem, args=(clientServer,))
    receive_thread.start()