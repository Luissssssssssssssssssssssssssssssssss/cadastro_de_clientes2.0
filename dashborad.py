import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

ARQUIVO_CLIENTES = "clientes.json"

modo_escuro = False
cores = {
    "bg": "#f0f0f0",
    "fg": "#000000",
    "btn_bg": "#dcdcdc",
    "btn_fg": "#000000"
}

def aplicar_tema(janela, widgets):
    janela.configure(bg=cores["bg"])
    for w in widgets:
        if isinstance(w, tk.Button):
            w.configure(bg=cores["btn_bg"], fg=cores["btn_fg"], activebackground=cores["bg"])
        else:
            w.configure(bg=cores["bg"], fg=cores["fg"])

def alternar_tema(janela, widgets):
    global modo_escuro
    modo_escuro = not modo_escuro
    if modo_escuro:
        cores["bg"] = "#1e1e1e"
        cores["fg"] = "#ffffff"
        cores["btn_bg"] = "#333333"
        cores["btn_fg"] = "#ffffff"
    else:
        cores["bg"] = "#f0f0f0"
        cores["fg"] = "#000000"
        cores["btn_bg"] = "#dcdcdc"
        cores["btn_fg"] = "#000000"
    aplicar_tema(janela, widgets)

def gerar_novo_id(clientes):
    return max((c["id"] for c in clientes), default=0) + 1

def salvar_cliente(nome, cpf, email, telefone, nascimento, endereco, janela):
    if not all([nome.strip(), cpf.strip(), email.strip(), telefone.strip(), nascimento.strip(), endereco.strip()]):
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos!")
        return
    clientes = []
    if os.path.exists(ARQUIVO_CLIENTES):
        try:
            with open(ARQUIVO_CLIENTES, "r", encoding="utf-8") as f:
                clientes = json.load(f)
        except json.JSONDecodeError:
            clientes = []

    novo_id = gerar_novo_id(clientes)
    cliente = {
        "id": novo_id,
        "nome": nome.strip(),
        "cpf": cpf.strip(),
        "email": email.strip(),
        "telefone": telefone.strip(),
        "nascimento": nascimento.strip(),
        "endereco": endereco.strip()
    }
    clientes.append(cliente)
    with open(ARQUIVO_CLIENTES, "w", encoding="utf-8") as f:
        json.dump(clientes, f, indent=4, ensure_ascii=False)
    messagebox.showinfo("Sucesso", "Cliente salvo com sucesso!")
    janela.destroy()
    abrir_dashboard()

def abrir_cadastro(master=None):
    janela = tk.Toplevel(master)
    janela.title("Cadastro de Cliente")
    janela.geometry("400x380")
    janela.resizable(False, False)

    labels = ["Nome", "CPF", "E-mail", "Telefone", "Nascimento (dd/mm/aaaa)", "Endereço"]
    entries = []

    for i, texto in enumerate(labels):
        label = tk.Label(janela, text=texto + ":")
        label.place(x=20, y=20 + i * 40)
        entry = tk.Entry(janela, width=30)
        entry.place(x=180, y=20 + i * 40)
        entries.append(entry)

    btn_salvar = tk.Button(janela, text="Salvar", command=lambda: salvar_cliente(
        entries[0].get(), entries[1].get(), entries[2].get(),
        entries[3].get(), entries[4].get(), entries[5].get(), janela
    ))
    btn_salvar.place(x=140, y=280)

    btn_tema = tk.Button(janela, text="Alternar Tema", command=lambda: alternar_tema(janela, widgets))
    btn_tema.place(x=130, y=320)

    widgets = entries + [btn_salvar, btn_tema]
    aplicar_tema(janela, widgets)

def editar_cliente_por_id(cliente_id, master=None):
    with open(ARQUIVO_CLIENTES, "r", encoding="utf-8") as f:
        clientes = json.load(f)

    cliente = next((c for c in clientes if c["id"] == cliente_id), None)
    if not cliente:
        messagebox.showerror("Erro", "Cliente não encontrado.")
        return

    janela = tk.Toplevel(master)
    janela.title("Editar Cliente")
    janela.geometry("400x380")
    janela.resizable(False, False)

    campos = {}
    labels = ["Nome", "CPF", "E-mail", "Telefone", "Nascimento", "Endereço"]
    keys = ["nome", "cpf", "email", "telefone", "nascimento", "endereco"]

    for i, (label_text, key) in enumerate(zip(labels, keys)):
        tk.Label(janela, text=label_text + ":").place(x=20, y=20 + i * 40)
        entry = tk.Entry(janela, width=30)
        entry.insert(0, cliente[key])
        entry.place(x=180, y=20 + i * 40)
        campos[key] = entry

    def salvar_edicao():
        for campo, entry in campos.items():
            cliente[campo] = entry.get().strip()
        for i, c in enumerate(clientes):
            if c["id"] == cliente_id:
                clientes[i] = cliente
                break
        with open(ARQUIVO_CLIENTES, "w", encoding="utf-8") as f:
            json.dump(clientes, f, indent=4, ensure_ascii=False)
        messagebox.showinfo("Sucesso", "Cliente editado com sucesso!")
        janela.destroy()
        abrir_dashboard()

    btn_salvar = tk.Button(janela, text="Salvar Alterações", command=salvar_edicao)
    btn_salvar.place(x=130, y=280)

    btn_tema = tk.Button(janela, text="Alternar Tema", command=lambda: alternar_tema(janela, list(campos.values()) + [btn_salvar, btn_tema]))
    btn_tema.place(x=130, y=320)

    aplicar_tema(janela, list(campos.values()) + [btn_salvar, btn_tema])

def excluir_cliente(cliente_id, janela_dashboard, tree):
    resposta = messagebox.askyesno("Confirmação", f"Deseja realmente excluir o cliente ID {cliente_id}?")
    if not resposta:
        return

    with open(ARQUIVO_CLIENTES, "r", encoding="utf-8") as f:
        clientes = json.load(f)

    clientes = [c for c in clientes if c["id"] != cliente_id]

    with open(ARQUIVO_CLIENTES, "w", encoding="utf-8") as f:
        json.dump(clientes, f, indent=4, ensure_ascii=False)

    messagebox.showinfo("Sucesso", f"Cliente ID {cliente_id} excluído.")
    abrir_dashboard()
    janela_dashboard.destroy()

def abrir_dashboard(usuario):
    janela = tk.Tk()
    janela.title("Dashboard de Clientes")
    janela.geometry("750x400")
    janela.resizable(False, False)

    tk.Label(janela, text=f"Bem-vindo, {usuario}!", font=("Arial", 14)).place(x=20, y=10)

    tree = ttk.Treeview(janela, columns=("ID", "Nome", "CPF", "Email", "Telefone"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Nome", text="Nome")
    tree.heading("CPF", text="CPF")
    tree.heading("Email", text="Email")
    tree.heading("Telefone", text="Telefone")
    tree.column("ID", width=40)
    tree.column("Nome", width=160)
    tree.column("CPF", width=100)
    tree.column("Email", width=160)
    tree.column("Telefone", width=100)
    tree.place(x=20, y=50, width=700, height=250)

    def carregar_clientes():
        tree.delete(*tree.get_children())
        if os.path.exists(ARQUIVO_CLIENTES):
            try:
                with open(ARQUIVO_CLIENTES, "r", encoding="utf-8") as f:
                    clientes = json.load(f)
                    for c in clientes:
                        tree.insert("", "end", values=(c["id"], c["nome"], c["cpf"], c["email"], c["telefone"]))
            except json.JSONDecodeError:
                pass

    def editar_selecionado():
        selecionado = tree.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um cliente para editar.")
            return
        cliente_id = tree.item(selecionado)["values"][0]
        editar_cliente_por_id(cliente_id, janela)

    def excluir_selecionado():
        selecionado = tree.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um cliente para excluir.")
            return
        cliente_id = tree.item(selecionado)["values"][0]
        excluir_cliente(cliente_id, janela, tree)

    btn_novo = tk.Button(janela, text="Novo Cliente", width=15, command=lambda: abrir_cadastro(janela))
    btn_editar = tk.Button(janela, text="Editar", width=15, command=editar_selecionado)
    btn_excluir = tk.Button(janela, text="Excluir", width=15, command=excluir_selecionado)
    btn_tema = tk.Button(janela, text="Alternar Tema", width=15, command=lambda: alternar_tema(janela, [btn_novo, btn_editar, btn_excluir, btn_tema]))

    btn_novo.place(x=80, y=300)
    btn_editar.place(x=280, y=300)
    btn_excluir.place(x=480, y=300)
    btn_tema.place(x=280, y=340)

    widgets = [btn_novo, btn_editar, btn_excluir, btn_tema]
    aplicar_tema(janela, widgets)
    carregar_clientes()
    janela.mainloop()


