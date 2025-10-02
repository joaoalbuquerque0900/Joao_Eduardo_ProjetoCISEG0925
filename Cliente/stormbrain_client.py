import socket
import time
import threading

def receber_mensagens(clientsocket): #funcao para receber mensagens do servidor

    while True:
        try:
            mensagem=clientsocket.recv(1024).decode('utf-8')
            if mensagem:
                print(f"\n- {mensagem}\n")
            else:
                print("Conexão fechada pelo servidor.")
                break
        except OSError:

            break

        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            break
        
    clientsocket.close()

def iniciar_cliente(): #funcao para iniciar o cliente e conectar ao servidor

    target_port=12345
    target_host="127.0.0.1"


    clientsocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

 
    try:

        clientsocket.connect((target_host, target_port))

        username=input("Digite seu nome de utilizador: ")
        clientsocket.send(username.encode('utf-8'))
        
        print("Conectado ao servidor. Para sair digite exit. Enviar mensagem...")

        thread_receber=threading.Thread(target=receber_mensagens, args=(clientsocket,)) #thread para receber mensagens do servidor
        thread_receber.start()

        while True:

            mensagem_enviar=input("> ")

            if mensagem_enviar.lower()=="exit":
                
                break

            clientsocket.send(mensagem_enviar.encode('utf-8'))
    
    except ConnectionRefusedError:

        print("Erro: servidor inativo ou recusa de conexao")
            
    except Exception as e:
            
            print(f"Ocorreu um erro: {e}")

            print("Erro: servidor inativo ou erro de comunicação")
            
    finally:

        clientsocket.close()
        print("Conexao fechada")

if __name__=="__main__":

    iniciar_cliente()
