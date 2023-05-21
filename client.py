import threading
import socket

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
            msg = cliente.recv(2048).decode('utf-8')
            print(msg+'\n')
        except:
            print('\nNão foi possível manter-se conectado.\n')
            print('Pressione <ENTER> para continuar.')
            cliente.close()
            break

def sendMessages(cliente, username):
    while True:
        try:
            msg = input('\n')
            cliente.send(f'<{username}> <{msg}>'.encode('utf-8'))
        except:
            return

main()