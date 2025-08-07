
    else:
  tro, text="Nascimento (dd/mm/aaaa):")
    entry_nascimento = tk.Entry(cadastro, width=30)

    label_endereco = tk.Label(cadastro, text="Endereço:")

    entry_telefone.place(x=180, y=140)

    label_nascimento.place(x=20, y=180)
    entry_nascimento.place(x=180, y=180)

    label_endereco.place(x=20, y=220)
    entry_endereco.place(x=180, y=220)

    botao_salvar.place(x=160, y=270)
    botao_tema.place(x=145, y=310)

    widgets = [
        label_nome, entry_nome, label_cpf, entry_cpf,
        label_email, entry_email, label_telefone, entry_telefone,
        label_nascimento, entry_nascimento, label_endereco, entry_endereco,
        botao_salvar, botao_tema
    ]

    aplicar_tema(cadastro, widgets)
    return cadastro

