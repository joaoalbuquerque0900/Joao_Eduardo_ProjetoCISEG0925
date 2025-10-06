# cliente_tkinter_funcoes_pt.py

import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import simpledialog
import queue

def iniciar_cliente():
    
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    fila_mensagens = queue.Queue()

    root = tk.Tk()
    root.title("Chat Stormbrain")

    area_chat = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled')
    area_chat.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    caixa_mensagem = tk.Entry(root, width=50)
    caixa_mensagem.pack(padx=10, pady=5, side=tk.LEFT, fill=tk.X, expand=True)
    
    botao_enviar = tk.Button(root, text="Enviar")
    botao_enviar.pack(padx=10, pady=5, side=tk.RIGHT)

    def exibir_mensagem(mensagem):

        area_chat.config(state='normal')
        area_chat.insert(tk.END, mensagem + "\n")
        area_chat.config(state='disabled')
        area_chat.yview(tk.END)

    def receber_mensagens():

        while True:
            try:
                mensagem_recebida = clientsocket.recv(1024).decode('utf-8')
                if mensagem_recebida:
                    fila_mensagens.put(mensagem_recebida)
                else:
                    fila_mensagens.put("Conexão perdida com o servidor.")
                    break
            except:
                fila_mensagens.put("Erro na conexão.")
                break

    def processar_fila():

        try:
            while not fila_mensagens.empty():
                mensagem = fila_mensagens.get_nowait()
                exibir_mensagem(mensagem)
        finally:
            root.after(100, processar_fila)

    def enviar_mensagem(event=None):

        mensagem_para_enviar = caixa_mensagem.get()

        if mensagem_para_enviar:

            exibir_mensagem(f"{username}: {mensagem_para_enviar}")
            
            clientsocket.send(mensagem_para_enviar.encode('utf-8'))

            caixa_mensagem.delete(0, tk.END)
            
            if mensagem_para_enviar.lower() == 'exit':
                fechar_janela()

    def fechar_janela():

        try:
            clientsocket.send("exit".encode('utf-8'))
        except:
            pass
        root.destroy()

    botao_enviar.config(command=enviar_mensagem)
    caixa_mensagem.bind("<Return>", enviar_mensagem)
    root.protocol("WM_DELETE_WINDOW", fechar_janela)

    try:
        target_host = "127.0.0.1"
        target_port = 12345
        clientsocket.connect((target_host, target_port))

        username = simpledialog.askstring("Nome de Utilizador", "Digite o seu nome:", parent=root)
        if username:
            clientsocket.send(username.encode('utf-8'))
            root.title(f"Chat Stormbrain - {username}")
        else:
            root.destroy()
            return

        thread_receber = threading.Thread(target=receber_mensagens, daemon=True)
        thread_receber.start()

        root.after(100, processar_fila)

        root.mainloop()

    except ConnectionRefusedError:
        exibir_mensagem("Erro: Nao foi possivel conectar ao servidor.")
        botao_enviar.config(state='disabled')
        root.mainloop()
    except Exception as e:
        exibir_mensagem(f"Ocorreu um erro: {e}")
        root.mainloop()


if __name__ == "__main__":
    iniciar_cliente()