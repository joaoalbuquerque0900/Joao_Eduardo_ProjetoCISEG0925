import socket
import time

target_port=12345
target_host="127.0.0.1"


clientsocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

clientsocket.connect((target_host, target_port))

print("Conectado ao servidor")

time.sleep(10)

clientsocket.close()