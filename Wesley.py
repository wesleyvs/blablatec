# -*- coding: utf-8 -*-
"""
@author: Wesley & Maria
"""

#Servidor TCP
import socket
import threading
import time
from datetime import datetime
import rsa

# Endereco IP do Servidor
HOST = ''
# Endereco IP do client
servidorCliente= '127.0.0.1'
# Porta IP do Servidor
PORT = 5002
# Porta IP do client
PORT1 = 5001
#Chave publica do server 2
chavePublica='./Server 2/chavePub.txt'
#Chave privada do server 1
chavePrivada='./Server 1/chavePri.txt'

tcp1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

orig = (HOST, PORT)
dest = (servidorCliente, PORT1)

def listening():
    print("Iniciando conexao")
    tcp1.bind(orig)
    tcp1.listen(1)
    while True:
        con, cliente = tcp1.accept()
        while True:
            msg = con.recv(1024)
            if not msg: break
            
            #Carregar o arquivo da chave
            arq = open(chavePrivada,'rb')
            txt = arq.read()
            arq.close()
            #Decodificar para o formato expoente e modulo
            pri = rsa.PrivateKey.load_pkcs1(txt, format='PEM')
            #Decifrar a mensagem
            msg = rsa.decrypt(msg,pri)
            
            print("\n")
            print("Maria ", end="")
            print("(", datetime.now().strftime('%d/%m/%Y - %H:%M'),")", end="")
            print(": ")
            print(">", msg.decode('utf-8'))
            print("\n")
        print ('Finalizando conexao do cliente', cliente)
        con.close()

def sending():
    tcp2.connect(dest)
    print ('Conexão Estabelecida')
    print("\n")
    print("\n\n --------========== BLABLATEC ==========-------- \n\n")
    while True:
        msg = ''
        msg = input().encode('utf-8')
        #Carregar o arquivo da chave
        arq = open(chavePublica,'rb')
        txt = arq.read()
        arq.close()
        #Decodificar para o formato expoente e modulo
        pub = rsa.PublicKey.load_pkcs1(txt, format='PEM')
        #Cifrar a mensagem
        msgc = rsa.encrypt(msg,pub)
        tcp2.send(msgc)
        if msg == '\x18': break
    tcp2.close()

#Thread de conexao
threading.Thread(target=listening).start()
time.sleep(5)
threading.Thread(target=sending).start()


