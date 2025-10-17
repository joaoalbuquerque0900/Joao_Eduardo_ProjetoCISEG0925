import socket
import threading
import time
import re
import logging

logging.basicConfig(
    level=logging.INFO, # Nível mínimo para exibir mensagens
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("server.log"), # Para escrever num ficheiro
        logging.StreamHandler()            # Para escrever na consola
    ]
)

clients={}
clients_lock=threading.Lock()

host="127.0.0.1"
port=12345

email_padrao=r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"    # padroes
tlmv_padrao=r"\b(?:(?:\+351|00351)?[\s.-]?)?(?:2\d{8}|9[1236]\d{7}|\d{9})\b"
ip_padrao=r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"
data_nascimento_padrao=r"\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b"
iban_padrao=r"\bPT50\s?\d{4}\s?\d{4}\s?\d{11}\s?\d{2}\b"
nif_padrao=r"\b\d{9}\b"
nic_padrao=r"\b\d{8}\s?\d{1}[A-Z]{2}\d\b"
codigo_postal_padrao=r"\b\d{4}[-]\d{3}\b"
cartao_padrao=r"\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|6(?:011|5[0-9]{2})[0-9]{12}|3[47][0-9]{13})\b"
nome_completo_padrao=r"[A-Z][a-z]+(?:\s[A-Z][a-z]+){1,}"

lista_padroes=[
    email_padrao,tlmv_padrao,ip_padrao,data_nascimento_padrao,
    iban_padrao,nif_padrao,nic_padrao,codigo_postal_padrao,
    cartao_padrao,nome_completo_padrao
    ] #padroes

def dados_pessoais(texto): #funcao para detetar padroes

    for padrao in lista_padroes:

        if re.search(padrao, texto):
            
            return True
        
    return False

def mensagem_broadcast(mensagem_compl, socket_envio): #garantir que as mensagens sao enviadas para todos os clients na lista client

    with clients_lock:

        for clientsocket in list(clients.keys()):
            
            if clientsocket!=socket_envio:
                
                try:

                    clientsocket.send(mensagem_compl.encode('utf-8'))

                except:

                    pass


def gerir_client(clientsocket, clientaddress):

    logging.info(f"Nova Conexão: {clientaddress}")
    username=""

    try:
        username = clientsocket.recv(1024).decode('utf-8')
        if not username:
            logging.warning(f"Conexão fechada pelo cliente {clientaddress} antes de enviar o nome de usuário.")
            clientsocket.close()
            return
            
        with clients_lock:
            clients[clientsocket]={'username':username, 'strikes':0}  #associar o nome de user ao socket do client

        logging.info(f"Usuário {username} conectado de {clientaddress}")

        mensagem_entrada=f"{username} entrou no chat."
        mensagem_broadcast(mensagem_entrada, clientsocket) #notificar os outros users que

        while True:

            mensagem=clientsocket.recv(1024).decode('utf-8')

            if not mensagem or mensagem.lower()=="exit": #definir os criterios para sair do chat: mensagem vazia ou comando exit

                logging.info(f"Desconectado {clientaddress}")
                break

            logging.info(f"{clientaddress[0]}:{clientaddress[1]} - {username}: Enviou: {mensagem}") #identificacao do client pelo ip (clientaddress[0]) e pela porta (clientaddress[1])
            
            if dados_pessoais(mensagem):
                logging.warning(f"Mensagem bloqueada de {username} por conter dados pessoais.")

                with clients_lock: #sistema de strikes

                    clients[clientsocket]['strikes']+=1
                    strikes_atuais=clients[clientsocket]['strikes']
                
                if strikes_atuais>=3:
                    aviso_final="TERCEIRO STRIKE. Foi desconectado por ter atringido os 3 strikes por partilhar dados sensiveis"
                    clientsocket.send(aviso_final.encode('utf-8'))
                    logging.warning(f"Utilizador '{username}' desconectado por atingir o terceiro strike")
                    break
                else:
                    aviso=f"MENSAGEM BLOQUEADA. Voce tem {strikes_atuais} strike(s). Ao terceiro, sera desconectado."
                    clientsocket.send(aviso.encode('utf-8'))

            else:

                mensagem_enviar=f"{username}: {mensagem}"
                mensagem_broadcast(mensagem_enviar, clientsocket) #utilizacao da funcao mensagem broadcast que garante que todos os users recebem a mensagem
                
    except ConnectionResetError:

        logging.warning(f"Conexao perdida com {clientaddress}")

    except Exception as e:
        logging.error(f"Ocorreu um erro com {clientaddress}: {e}")


    finally:
        with clients_lock: # verifica so o username ainda esta na lista clients antes de remover
            if clientsocket in clients:
                
                del clients[clientsocket]
        
        if username:
                
                mensagem_saida=f"{username} saiu do chat."
                logging.info(mensagem_saida)
                mensagem_broadcast(mensagem_saida, clientsocket)

        clientsocket.close()
        logging.info(f"Conexao fechada: {clientaddress} | Usuário: {username}")

def iniciar_server():

    serversocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        serversocket.bind((host,port)) # colocar em escuta

        serversocket.listen(5) # estabelecer o limite de conexoes
        logging.info(f"Servidor em escuta")

        while True:

            clientsocket, clientaddress=serversocket.accept()
            
            with clients_lock: #garantir que a lista clients e acedida de forma segura

                clients[clientsocket]=""
                

            logging.info(f"Conexao aceite: {clientaddress}")
            thread=threading.Thread(target=gerir_client, args=(clientsocket, clientaddress))
            thread.start() #iniciar uma thread para o client
    
    except KeyboardInterrupt:
        logging.info("Servidor a fechar...")
    
    except Exception as e:

        logging.info(f"Ocorreu um erro no servidor: {e}")

    finally:

        with clients_lock:
            for clientsocket in clients:
                clientsocket.close()
            
        serversocket.close()
        logging.info("Servidor fechado")


if __name__ == "__main__":

    iniciar_server()
