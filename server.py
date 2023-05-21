import threading
import socket
import time

clientes = []

def main():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind(('localhost', 10101))
        server.listen(2)
        print("Servidor conectado")
    except:
        return print('\nNão foi possível iniciar o servidor.\n')
    
    while True:

        cliente, addr = server.accept()
        clientes.append(cliente)

        thread = threading.Thread(target=messagesTreatement, args=[cliente])
        thread.start()

def messagesTreatement(cliente):

    while True:
        try:
            msg = cliente.recv(2048)
            broadcast(msg, cliente)
        except:
            deleteClient(cliente)
            break

def broadcast(msg, cliente):

    for clienteItem in clientes:
        if clienteItem != cliente:
            try:
                clienteItem.send(msg)
            except:
                deleteClient(clienteItem)

def deleteClient(cliente):

    clientes.remove(cliente)

main()