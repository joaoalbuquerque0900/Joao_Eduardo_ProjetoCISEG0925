import socket
import time
import threading

def receber_mensagens(clientsocket):

    while True:
        try:
            mensagem=clientsocket.recv(1024).decode('utf-8')
            if mensagem:
                print(f"\nMensagem recebida: {mensagem}\n")
            else:
                print("Conexão fechada pelo servidor.")
                break
        except OSError:

            break

        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            break
        
    clientsocket.close()

def iniciar_cliente():

    target_port=12345
    target_host="127.0.0.1"


    clientsocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

 
    try:

        clientsocket.connect((target_host, target_port))
        
        print("Conectado ao servidor. Para sair digite exit. Enviar mensagem...")

        thread_receber=threading.Thread(target=receber_mensagens, args=(clientsocket,))
        thread_receber.start()

        while True:

            mensagem_enviar=input("Mensagem: ")

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
