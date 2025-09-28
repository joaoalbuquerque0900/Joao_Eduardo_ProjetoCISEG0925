import socket
import time

target_port=12345
target_host="127.0.0.1"


clientsocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True:

    try:

        clientsocket.connect((target_host, target_port))
        
        print("Conectado ao servidor. Enviar mensagem...")

        mensagem_enviar=input("Mensagem: ")

        clientsocket.send(mensagem_enviar.encode('utf-8'))
        print(f"Enviado: {mensagem_enviar}")

        resposta=clientsocket.recv(1024).decode('utf-8')
        print(f"Recebido: {resposta}")

        

    except:

        print("Erro: servidor inativo ou erro de comunicação")
        break

    finally:

        clientsocket.close()
        print("Conexao fechada")
        break
