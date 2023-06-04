import threading
import socket
from cryptography.fernet import Fernet
import pickle

chave = Fernet.generate_key() #GERA UMA CHAVE RANDÔMICA
f = Fernet(chave) 
# filehandler = open('chave.key', 'wb')
# pickle.dump(f, filehandler)
# filehandler.close()

file = open('chave.key', 'rb')
chave_lida = pickle.load(file)
file.close()

print("Objeto: "+str(chave_lida))

def main():
    
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        cliente.connect(('localhost', 10101))
        print("Cliente conectado")
    except:
        return print('\nNão foi possível conectar-se ao servidor.\n')
    
    username = input("Usuário: ")
    print("\nConectado.")

    thread1 = threading.Thread(target=reciveMessages, args=[cliente])
    thread2 = threading.Thread(target=sendMessages, args=[cliente, username])

    thread1.start()
    thread2.start()

def reciveMessages(cliente):

    while True:
        try:
            msg = cliente.recv(4096)
            mensdec = chave_lida.decrypt(msg)
            print(mensdec)
        except Exception as e:
            print("Exception Receive: "+str(e))
            print('\nNão foi possível manter-se conectado.\n')
            print('Pressione <ENTER> para continuar.')
            cliente.close()
            break

def sendMessages(cliente, username):
    while True:
        try:
            msg = input('\n')
            mens = chave_lida.encrypt(bytes(msg, 'utf-8'))
            print("\nMensagem criptografada: "+str(mens))
            cliente.send(mens)
        except Exception as e:
            print("Exception Send: "+str(e))
            return

main()
