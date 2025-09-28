import socket
import threading
import time
import re

clients=[]
host="127.0.0.1"
port=12345

email_padrao=r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"    # padroes
tlmv_padrao=r"\b(?:(?:\+351|00351)?[\s.-]?)?(?:2\d{8}|9[1236]\d{7}|\d{9})\b"
ip_padrao=r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"
data_nascimento_padrao=r"\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b"
iban_padrao=r"PT50\s?00\d{2}\s?\d{4}\s?\d{4}\s?\d{4}\s?\d{3}\s?\d{1}"
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

    for clientsocket in clients:
        
        if clientsocket!=socket_envio:
            
            try:

                clientsocket.send(mensagem_compl.encode('utf-8'))

            except:

                clientsocket.close() #se a mensagem nao for enviada o socket do client fecha e o client e removido da lista de clients.
                if clientsocket in clients:
                    clients.remove(clientsocket)

def gerir_client(clientsocket, clientaddress):

    print(f"Nova Conexão: {clientaddress}")

    try:
        while True:

            mensagem=clientsocket.recv(1024).decode('utf-8') #buffer de 1024 para receber mensagem enviada pelo client

            if not mensagem or mensagem.lower()=="exit": #definir os criterios para sair do chat: mensagem vazia ou comando exit

                print(f"Desconectado {clientaddress}")
                break

            print(f"{clientaddress[0]}:{clientaddress[1]} Enviou: {mensagem}") #identificacao do client pelo ip (clientaddress[0]) e pela porta (clientaddress[1])

            mensagem_enviar=f"{clientaddress[0]} {mensagem}" #preparacao da mensagem para broadcast: com identificacao por ip e texto da mensagem definida pelo client
            
            if dados_pessoais(mensagem):

                clientsocket.send("Mensagem bloqueada. Atencao nao partilhe dados sensiveis".encode('utf-8'))

            else:

                mensagem_broadcast(mensagem_enviar, clientsocket) #utilizacao da funcao mensagem broadcast que garante que todos os users recebem a mensagem
     
    except:
        pass

    if clientsocket in clients: #apenas executado quando um dos criterios de saida é cumprido. fecha o socket do client e remove da lista de clients

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




