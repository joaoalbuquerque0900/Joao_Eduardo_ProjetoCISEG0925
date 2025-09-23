import socket
import threading
import time

host="127.0.0.1"
port=12345

serversocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serversocket.bind((host,port)) # colocar em escuta

serversocket.listen(5) # estabelecer o limite de conexoes
print(f"Servidor em escuta")

clientsocket, clientaddress=serversocket.accept()
print(f"Conexao aceite: {clientaddress}")

time.sleep(5)

clientsocket.close()
serversocket.close()



