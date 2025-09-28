import socket
import threading
import time

clients=[]
host="127.0.0.1"
port=12345

def gerir_client(clientsocket, clientaddress):

    print(f"Nova Conexão: {clientaddress}")

    try:
        while True:

            mensagem=clientsocket.recv(1024).decode('utf-8')

            if not mensagem or mensagem.lower()=="exit":

                print(f"Desconectado {clientaddress}")
                break

            print(f"{clientaddress[0]}:{clientaddress[1]} Enviou: {mensagem}")

            clientsocket.send("Mensagem enviada".encode('utf-8'))
        
    except:
        pass

    if clientsocket in clients:

        clients.remove(clientsocket)

    clientsocket.close()
    
def iniciar_server():

    serversocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    serversocket.bind((host,port)) # colocar em escuta

    serversocket.listen(5) # estabelecer o limite de conexoes
    print(f"Servidor em escuta")

    while True:

        try:

            clientsocket, clientaddress=serversocket.accept()
            print(f"Conexao aceite: {clientaddress}")

            clients.append(clientsocket)

            thread=threading.Thread(target=gerir_client, args=(clientsocket, clientaddress))
            thread.start() #iniciar uma thread para o client

        except:
            print("Ocorreu um erro.")
            break

    time.sleep(5)

    serversocket.close()


if __name__ == "__main__":
    iniciar_server()




