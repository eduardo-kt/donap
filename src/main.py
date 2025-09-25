import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from src.auth import autenticar, registrar_usuario
from src.persistencia import (
    salvar_donatario,
    salvar_doacao,
    salvar_donatario_doacoes,
    carregar_donatarios,
    carregar_doacoes,
    carregar_donatario_doacoes,
)


# ==========================
# Funções de Lógica
# ==========================
def buscar_donatarios(chave: str):
    """
    Busca donatários pelo nome ou CPF.
    Retorna uma lista de dicionários com os donatários encontrados.
    """
    donatarios = carregar_donatarios()
    encontrados = [
        d
        for d in donatarios
        if (chave.lower() in d["nome"].lower() or chave == d["cpf"])
    ]
    return encontrados


def testar_login(usuario, senha):
    return autenticar(usuario, senha)


# ==========================
# Interface Gráfica
# ==========================
def tela_consulta_donatario():
    consulta_win = tk.Toplevel()
    consulta_win.title("Consulta Donatário")

    tk.Label(consulta_win, text="Nome ou CPF:").pack()
    entry_chave = tk.Entry(consulta_win)
    entry_chave.pack()

    # Listbox ou Treeview para exibir resultados
    tree = ttk.Treeview(
        consulta_win, columns=("Nome", "CPF"), show="headings", height=10
    )
    tree.heading("Nome", text="Nome")
    tree.heading("CPF", text="CPF")
    tree.pack()

    def consultar():
        chave = entry_chave.get().strip()
        for i in tree.get_children():
            tree.delete(i)

        if not chave:
            messagebox.showwarning(
                "Aviso",
                "Digite um nome ou CPF para consultar!",
            )
            return

        encontrados = buscar_donatarios(chave)
        if encontrados:
            for d in encontrados:
                tree.insert("", tk.END, values=(d["nome"], d["cpf"]))
        else:
            messagebox.showinfo("Resultado", "Nenhum donatário encontrado.")

    def abrir_detalhes(event):
        selecionado = tree.selection()
        if not selecionado:
            return
        item = tree.item(selecionado[0])
        nome, cpf = item["values"]
        tela_detalhes_donatario(cpf, nome)

    tree.bind("<Double-1>", abrir_detalhes)

    tk.Button(consulta_win, text="Consultar", command=consultar).pack()
    tk.Button(consulta_win, text="Fechar", command=consulta_win.destroy).pack()


def tela_detalhes_donatario(cpf, nome):
    detalhes_win = tk.Toplevel()
    detalhes_win.title(f"Detalhes de {nome}")

    doacoes = carregar_doacoes()
    doacoes_por_donatario = carregar_donatario_doacoes()
    recebidas = doacoes_por_donatario.get(cpf, [])

    # Função para obter doações disponíveis
    def atualizar_disponiveis():
        todas_recebidas = [
            d for doacoes in doacoes_por_donatario.values() for d in doacoes
        ]
        return [d for d in doacoes if d not in todas_recebidas]

    disponiveis = atualizar_disponiveis()

    # ----------------- Filtros -----------------
    filtro_frame = tk.Frame(detalhes_win)
    filtro_frame.grid(row=0, column=0, columnspan=2, pady=5)

    tk.Label(filtro_frame, text="Tipo:").grid(row=0, column=0)
    tipos = sorted({d["tipo"] for d in doacoes}) + [""]
    cb_tipo = ttk.Combobox(filtro_frame, values=tipos, state="readonly")
    cb_tipo.set("")
    cb_tipo.grid(row=0, column=1)

    tk.Label(filtro_frame, text="Cor:").grid(row=0, column=2)
    cores = sorted({d["cor"] for d in doacoes}) + [""]
    cb_cor = ttk.Combobox(filtro_frame, values=cores, state="readonly")
    cb_cor.set("")
    cb_cor.grid(row=0, column=3)

    tk.Label(filtro_frame, text="Tamanho:").grid(row=0, column=4)
    tamanhos = sorted({d["tamanho"] for d in doacoes}) + [""]
    cb_tamanho = ttk.Combobox(filtro_frame, values=tamanhos, state="readonly")
    cb_tamanho.set("")
    cb_tamanho.grid(row=0, column=5)

    # ----------------- Treeviews -----------------
    tk.Label(detalhes_win, text="Doações Recebidas").grid(row=1, column=0)
    tk.Label(detalhes_win, text="Doações Disponíveis").grid(row=1, column=1)

    tree_recebidas = ttk.Treeview(
        detalhes_win,
        columns=("Tipo", "Cor", "Tamanho"),
        show="headings",
        height=10,
    )
    for c in ("Tipo", "Cor", "Tamanho"):
        tree_recebidas.heading(c, text=c)
    tree_recebidas.grid(row=2, column=0, padx=5)

    tree_disponiveis = ttk.Treeview(
        detalhes_win,
        columns=("Tipo", "Cor", "Tamanho"),
        show="headings",
        height=10,
    )
    for c in ("Tipo", "Cor", "Tamanho"):
        tree_disponiveis.heading(c, text=c)
    tree_disponiveis.grid(row=2, column=1, padx=5)

    # ----------------- Atualização das listas -----------------
    def atualizar_listas():
        # Aplica filtros
        tipo_f = cb_tipo.get()
        cor_f = cb_cor.get()
        tam_f = cb_tamanho.get()

        tree_recebidas.delete(*tree_recebidas.get_children())
        for d in recebidas:
            if (
                (not tipo_f or d["tipo"] == tipo_f)
                and (not cor_f or d["cor"] == cor_f)
                and (not tam_f or d["tamanho"] == tam_f)
            ):
                tree_recebidas.insert(
                    "", tk.END, values=(d["tipo"], d["cor"], d["tamanho"])
                )

        tree_disponiveis.delete(*tree_disponiveis.get_children())
        for d in disponiveis:
            if (
                (not tipo_f or d["tipo"] == tipo_f)
                and (not cor_f or d["cor"] == cor_f)
                and (not tam_f or d["tamanho"] == tam_f)
            ):
                tree_disponiveis.insert(
                    "", tk.END, values=(d["tipo"], d["cor"], d["tamanho"])
                )

    # Bind para atualizar ao mudar filtro
    cb_tipo.bind("<<ComboboxSelected>>", lambda e: atualizar_listas())
    cb_cor.bind("<<ComboboxSelected>>", lambda e: atualizar_listas())
    cb_tamanho.bind("<<ComboboxSelected>>", lambda e: atualizar_listas())

    # ----------------- Função adicionar doação -----------------
    def adicionar_doacao():
        sel = tree_disponiveis.selection()
        if not sel:
            return
        item = tree_disponiveis.item(sel[0])
        d = {
            "tipo": item["values"][0],
            "cor": item["values"][1],
            "tamanho": item["values"][2],
        }
        recebidas.append(d)
        disponiveis.remove(d)
        salvar_donatario_doacoes(cpf, recebidas)
        atualizar_listas()

    tk.Button(
        detalhes_win,
        text="Adicionar Doação",
        command=adicionar_doacao,
    ).grid(row=3, column=1, pady=5)

    atualizar_listas()  # inicializa


def tela_cadastro_donatario():
    cadastro_win = tk.Toplevel()
    cadastro_win.title("Cadastro de Donatário")

    tk.Label(cadastro_win, text="Nome:").pack()
    entry_nome = tk.Entry(cadastro_win)
    entry_nome.pack()

    tk.Label(cadastro_win, text="Data de Nascimento:").pack()
    entry_data = tk.Entry(cadastro_win)
    entry_data.pack()

    tk.Label(cadastro_win, text="CPF:").pack()
    entry_cpf = tk.Entry(cadastro_win)
    entry_cpf.pack()

    def salvar():
        nome = entry_nome.get()
        data = entry_data.get()
        cpf = entry_cpf.get()

        if not all([nome, data, cpf]):
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return

        donatario = {"nome": nome, "data_nascimento": data, "cpf": cpf}
        salvar_donatario(donatario)

        messagebox.showinfo(
            "Cadastro",
            f"Donatário {nome} cadastrado com sucesso!",
        )
        cadastro_win.destroy()

    tk.Button(cadastro_win, text="Salvar", command=salvar).pack()
    tk.Button(
        cadastro_win,
        text="Cancelar",
        command=cadastro_win.destroy,
    ).pack()


def tela_cadastro_doacao():
    doacao_win = tk.Toplevel()
    doacao_win.title("Cadastro de Doação")

    def criar_combobox(titulo, opcoes):
        tk.Label(doacao_win, text=titulo).pack()
        cb = ttk.Combobox(doacao_win, values=opcoes, state="readonly")
        cb.pack()

        def checar_outro(event):
            if cb.get() == "Outro":
                novo_valor = simpledialog.askstring(
                    "Outro", f"Digite o valor para {titulo.lower()}:"
                )
                if novo_valor:
                    if novo_valor not in cb["values"]:
                        cb["values"] = list(cb["values"]) + [novo_valor]
                    cb.set(novo_valor)
                else:
                    cb.set("")  # limpa se nada for digitado

        cb.bind("<<ComboboxSelected>>", checar_outro)
        return cb

    # Tipo de item
    tipos = ["Camiseta", "Calça", "Casaco", "Saia", "Vestido", "Outro"]
    cb_tipo = criar_combobox("Tipo de item", tipos)

    # Cor
    cores = [
        "Branco",
        "Preto",
        "Azul",
        "Vermelho",
        "Verde",
        "Amarelo",
        "Outro",
    ]
    cb_cor = criar_combobox("Cor do item", cores)

    # Tamanho
    tamanhos = ["PP", "P", "M", "G", "GG", "Outro"]
    cb_tamanho = criar_combobox("Tamanho", tamanhos)

    def salvar():
        tipo = cb_tipo.get()
        cor = cb_cor.get()
        tamanho = cb_tamanho.get()

        if not all([tipo, cor, tamanho]):
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return

        doacao = {"tipo": tipo, "cor": cor, "tamanho": tamanho}
        salvar_doacao(doacao)
        messagebox.showinfo("Cadastro", "Doação cadastrada com sucesso!")
        doacao_win.destroy()

    tk.Button(doacao_win, text="Salvar", command=salvar).pack()
    tk.Button(doacao_win, text="Cancelar", command=doacao_win.destroy).pack()


def tela_consulta_doacao():
    consulta_win = tk.Toplevel()
    consulta_win.title("Consulta de Doações")

    # Carrega todas as doações
    doacoes = carregar_doacoes()

    # Função para extrair valores únicos de um campo
    def valores_unicos(campo):
        return sorted({d[campo] for d in doacoes}) + ["Outro"]

    # Combobox Tipo
    tk.Label(consulta_win, text="Tipo de item:").pack()
    cb_tipo = ttk.Combobox(
        consulta_win, values=valores_unicos("tipo"), state="readonly"
    )
    cb_tipo.pack()

    # Combobox Cor
    tk.Label(consulta_win, text="Cor do item:").pack()
    cb_cor = ttk.Combobox(
        consulta_win,
        values=valores_unicos("cor"),
        state="readonly",
    )
    cb_cor.pack()

    # Combobox Tamanho
    tk.Label(consulta_win, text="Tamanho:").pack()
    cb_tamanho = ttk.Combobox(
        consulta_win, values=valores_unicos("tamanho"), state="readonly"
    )
    cb_tamanho.pack()

    resultados_text = tk.Text(consulta_win, width=60, height=15)
    resultados_text.pack()

    def consultar():
        tipo = cb_tipo.get()
        cor = cb_cor.get()
        tamanho = cb_tamanho.get()

        resultados_text.delete("1.0", tk.END)

        encontrados = [
            d
            for d in doacoes
            if (not tipo or d["tipo"] == tipo)
            and (not cor or d["cor"] == cor)
            and (not tamanho or d["tamanho"] == tamanho)
        ]

        if encontrados:
            for i, d in enumerate(encontrados, start=1):
                resultados_text.insert(
                    tk.END,
                    (
                        f"{i}. Tipo: {d['tipo']}, ",
                        f"Cor: {d['cor']}, Tamanho: {d['tamanho']}\n",
                    ),
                )
        else:
            resultados_text.insert(tk.END, "Nenhuma doação encontrada.\n")

    tk.Button(consulta_win, text="Consultar", command=consultar).pack()
    tk.Button(consulta_win, text="Fechar", command=consulta_win.destroy).pack()


def tela_menu():
    root = tk.Tk()
    root.title("Menu Principal")

    tk.Label(root, text="Bem-vindo! Escolha uma opção:").pack()

    tk.Button(
        root,
        text="Cadastrar Donatário",
        command=tela_cadastro_donatario,
    ).pack()
    tk.Button(
        root,
        text="Cadastrar Doação",
        command=tela_cadastro_doacao,
    ).pack()
    tk.Button(
        root,
        text="Consultar Donatário",
        command=tela_consulta_donatario,
    ).pack()
    tk.Button(
        root,
        text="Consultar Doações",
        command=tela_consulta_doacao,
    ).pack()
    tk.Button(root, text="Sair", command=root.destroy).pack()

    root.mainloop()


def tela_login():
    def tentar_login():
        if autenticar(entry_user.get(), entry_pass.get()):
            messagebox.showinfo("Sucesso", "Login realizado!")
            root.destroy()
            tela_menu()
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos")

    root = tk.Tk()
    root.title("Login")

    tk.Label(root, text="Usuário").pack()
    entry_user = tk.Entry(root)
    entry_user.pack()

    tk.Label(root, text="Senha").pack()
    entry_pass = tk.Entry(root, show="*")
    entry_pass.pack()

    tk.Button(root, text="Entrar", command=tentar_login).pack()
    tk.Button(
        root,
        text="Registrar",
        command=lambda: registrar_usuario(entry_user.get(), entry_pass.get()),
    ).pack()

    root.mainloop()


if __name__ == "__main__":
    tela_login()
