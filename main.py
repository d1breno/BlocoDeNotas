import os
import customtkinter as ctk
import subprocess
from tkinter import messagebox

CAMINHO_NOTAS = "notas"
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Cria a pasta de notas
if not os.path.exists(CAMINHO_NOTAS):
    os.makedirs(CAMINHO_NOTAS)

def abrir_editor(caminho_arquivo=None):
    if caminho_arquivo:
        subprocess.Popen(["python", "editor.py", caminho_arquivo])
    else:
        subprocess.Popen(["python", "editor.py"])

def deletar_nota(nome_arquivo):
    confirmacao = messagebox.askyesno("Confirmar Exclusão", f"Deseja excluir '{nome_arquivo}'?")
    if confirmacao:
        os.remove(os.path.join(CAMINHO_NOTAS, nome_arquivo))
        atualizar_lista()

def atualizar_lista():
    for widget in frame_notas.winfo_children():
        widget.destroy()

    arquivos = os.listdir(CAMINHO_NOTAS)
    for nome in arquivos:
        caminho = os.path.join(CAMINHO_NOTAS, nome)
        if os.path.isfile(caminho):
            item = ctk.CTkFrame(frame_notas)
            item.pack(fill="x", pady=2, padx=10)

            botao = ctk.CTkButton(item, text=nome, anchor="w", command=lambda c=caminho: abrir_editor(c))
            botao.pack(side="left", expand=True, fill="x", padx=5, pady=5)

            btn_del = ctk.CTkButton(item, text="🗑️", width=30, command=lambda n=nome: deletar_nota(n))
            btn_del.pack(side="right", padx=5)

# Janela principal
janela = ctk.CTk()
janela.title("Gerenciador de Notas")
janela.configure(fg_color="#1E1E1E")
janela.geometry("400x500")

# Botões
btn_nova = ctk.CTkButton(janela, text="+ Nova Nota", command=lambda: abrir_editor())
btn_nova.pack(pady=10)

btn_atualizar = ctk.CTkButton(janela, text="🔄 Atualizar Lista", command=atualizar_lista)
btn_atualizar.pack(pady=5)

# Lista de notas
frame_notas = ctk.CTkScrollableFrame(janela)
frame_notas.pack(expand=True, fill="both", padx=10, pady=10)

# Carrega lista
atualizar_lista()
janela.mainloop()
