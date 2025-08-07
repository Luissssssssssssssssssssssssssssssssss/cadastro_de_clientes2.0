import login
import tkinter as tk
from tkinter import messagebox
from dashboard import abrir_dashboard


# tela-de-cadastro
# ----- Dados em Memória RAM -----
usuarios = {
    "admin": "1234",
    "user": "senha",
    "LLucio": "321",
}

# Variáveis globais para widgets e tema
janela_login = None
entry_usuario = None
entry_senha = None
modo_escuro = False
widgets = []

# Cores padrão (modo claro)
cores = {
    "bg": "#f0f0f0",
    "fg": "#000000",
    "btn_bg": "#dcdcdc",
    "btn_fg": "#000000"
}

def aplicar_tema():
    janela_login.configure(bg=cores["bg"])
    for widget in widgets:
        if isinstance(widget, tk.Button):
            widget.configure(bg=cores["btn_bg"], fg=cores["btn_fg"],
                             activebackground=cores["bg"], activeforeground=cores["btn_fg"])
        else:
            widget.configure(bg=cores["bg"], fg=cores["fg"])

def alternar_tema():
    global modo_escuro
    modo_escuro = not modo_escuro

    if modo_escuro:
        cores["bg"] = "#1e1e1e"
        cores["fg"] = "#ffffff"
        cores["btn_bg"] = "#444444"
        cores["btn_fg"] = "#ffffff"
    else:
        cores["bg"] = "#f0f0f0"
        cores["fg"] = "#000000"
        cores["btn_bg"] = "#dcdcdc"
        cores["btn_fg"] = "#000000"

    aplicar_tema()

def autenticar():
    usuario = entry_usuario.get()
    senha = entry_senha.get()

    if usuario in usuarios and usuarios[usuario] == senha:
        janela_login.destroy()  # Fecha a tela de login
        abrir_dashboard(usuario)
    else:
        messagebox.showerror("Erro", "Usuário ou senha incorretos!")

def tela_login():
    global janela_login, entry_usuario, entry_senha, widgets

    janela_login = tk.Tk()
    janela_login.title("Login")
    janela_login.geometry("300x230")
    janela_login.resizable(False, False)

    # Widgets
    label_usuario = tk.Label(janela_login, text="Usuário:")
    entry_usuario = tk.Entry(janela_login)
    label_senha = tk.Label(janela_login, text="Senha:")
    entry_senha = tk.Entry(janela_login, show="*")
    botao_entrar = tk.Button(janela_login, text="Entrar", command=autenticar)
    botao_tema = tk.Button(janela_login, text="Alternar Tema", command=alternar_tema)

    # Posicionamento
    label_usuario.place(x=30, y=30)
    entry_usuario.place(x=100, y=30)
    label_senha.place(x=30, y=70)
    entry_senha.place(x=100, y=70)
    botao_entrar.place(x=120, y=110)
    botao_tema.place(x=100, y=160)

    # Lista de widgets para aplicar tema
    widgets = [label_usuario, entry_usuario, label_senha, entry_senha, botao_entrar, botao_tema]

    aplicar_tema()
    janela_login.mainloop()

if __name__ == "__main__":
    login.tela_login()
