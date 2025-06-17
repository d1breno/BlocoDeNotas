import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import sys

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

caminho_arquivo = sys.argv[1] if len(sys.argv) > 1 else None
fixo_no_topo = True

janela = ctk.CTk()
janela.title("Editor de Nota")
janela.geometry("700x500")
janela.attributes("-topmost", True)
janela.resizable(True, True)

# === Funções ===
def alternar_topo():
    global fixo_no_topo
    fixo_no_topo = not fixo_no_topo
    janela.attributes("-topmost", fixo_no_topo)
    btn_fixar.configure(text="✅ Fixado" if fixo_no_topo else "📌 Fixar")

def salvar():
    global caminho_arquivo
    if not caminho_arquivo:
        caminho_arquivo = filedialog.asksaveasfilename(
            initialdir="notas",
            defaultextension=".txt",
            filetypes=[("Arquivos de Texto", "*.txt")]
        )
    if caminho_arquivo:
        try:
            with open(caminho_arquivo, "w", encoding="utf-8") as f:
                f.write(texto.get("1.0", "end"))
        except Exception as e:
            messagebox.showerror("Erro ao Salvar", str(e))

def backup_automatico():
    try:
        if caminho_arquivo:
            with open(caminho_arquivo, "w", encoding="utf-8") as f:
                f.write(texto.get("1.0", "end"))
        else:
            os.makedirs("notas", exist_ok=True)
            with open("notas/_backup_temp.txt", "w", encoding="utf-8") as f:
                f.write(texto.get("1.0", "end"))
    except:
        pass
    janela.after(10000, backup_automatico)

def atualizar_fonte(event=None):
    largura = janela.winfo_width()
    tamanho_base = max(14, min(32, int(largura / 40)))
    texto.configure(font=("Arial", tamanho_base))

def adicionar_imagem():
    caminho = filedialog.askopenfilename(
        title="Selecionar Imagem",
        filetypes=[("Imagens", "*.png *.jpg *.jpeg *.gif *.bmp")]
    )
    if caminho:
        try:
            imagem = Image.open(caminho)
            imagem.thumbnail((300, 300))
            imagem_tk = ImageTk.PhotoImage(imagem)

            if not hasattr(texto, "imagens"):
                texto.imagens = []
            texto.imagens.append(imagem_tk)

            texto.image_create("insert", image=imagem_tk)
            texto.insert("insert", "\n")
        except Exception as e:
            messagebox.showerror("Erro ao inserir imagem", str(e))

# === Área de Texto com Tkinter ===
frame_texto = ctk.CTkFrame(janela)
frame_texto.pack(fill="both", expand=True, padx=10, pady=(50, 10))

texto = tk.Text(frame_texto, font=("Arial", 14), wrap="word", undo=True, bg="#1e1e1e", fg="white", insertbackground="white")
texto.pack(fill="both", expand=True)
atualizar_fonte()

# Carrega arquivo, se existir
if caminho_arquivo and os.path.exists(caminho_arquivo):
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        texto.insert("1.0", f.read())

janela.bind("<Configure>", atualizar_fonte)

# === Menu Superior ===
menu = ctk.CTkFrame(janela, height=40)
menu.place(relx=0, rely=0, relwidth=1)

btn_salvar = ctk.CTkButton(menu, text="💾 Salvar", command=salvar, width=100)
btn_salvar.pack(side="left", padx=10, pady=5)

btn_fixar = ctk.CTkButton(menu, text="✅ Fixado", command=alternar_topo, width=100)
btn_fixar.pack(side="left", padx=5, pady=5)

btn_imagem = ctk.CTkButton(menu, text="🖼️ Imagem", command=adicionar_imagem, width=100)
btn_imagem.pack(side="left", padx=5, pady=5)

# === Backup ===
backup_automatico()
janela.mainloop()
