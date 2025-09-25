import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from src.auth import autenticar, registrar_usuario
from src.persistencia import (
    salvar_donatario,
    carregar_donatarios,
    salvar_doacao,
    carregar_doacoes,
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

    resultados_text = tk.Text(consulta_win, width=50, height=10)
    resultados_text.pack()

    def consultar():
        chave = entry_chave.get().strip()
        resultados_text.delete("1.0", tk.END)

        if not chave:
            resultados_text.insert(
                tk.END,
                "Digite um nome ou CPF para consultar!\n",
            )
            return

        encontrados = buscar_donatarios(chave)

        if encontrados:
            for d in encontrados:
                resultados_text.insert(
                    tk.END,
                    (
                        f"Nome: {d['nome']}, ",
                        f"Data Nasc.: {d['data_nascimento']}, ",
                        f"CPF: {d['cpf']}\n",
                    ),
                )
        else:
            resultados_text.insert(tk.END, "Nenhum donatário encontrado.\n")

    tk.Button(consulta_win, text="Consultar", command=consultar).pack()
    tk.Button(consulta_win, text="Fechar", command=consulta_win.destroy).pack()


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

    # Campos de filtro
    tk.Label(consulta_win, text="Tipo de item:").pack()
    tipos = ["", "Camiseta", "Calça", "Casaco", "Saia", "Vestido", "Outro"]
    cb_tipo = ttk.Combobox(consulta_win, values=tipos, state="readonly")
    cb_tipo.current(0)
    cb_tipo.pack()

    tk.Label(consulta_win, text="Cor do item:").pack()
    cores = [
        "",
        "Branco",
        "Preto",
        "Azul",
        "Vermelho",
        "Verde",
        "Amarelo",
        "Outro",
    ]
    cb_cor = ttk.Combobox(consulta_win, values=cores, state="readonly")
    cb_cor.current(0)
    cb_cor.pack()

    tk.Label(consulta_win, text="Tamanho:").pack()
    tamanhos = ["", "PP", "P", "M", "G", "GG", "Outro"]
    cb_tamanho = ttk.Combobox(consulta_win, values=tamanhos, state="readonly")
    cb_tamanho.current(0)
    cb_tamanho.pack()

    resultados_text = tk.Text(consulta_win, width=60, height=15)
    resultados_text.pack()

    def consultar():
        tipo = cb_tipo.get()
        cor = cb_cor.get()
        tamanho = cb_tamanho.get()

        resultados_text.delete("1.0", tk.END)
        doacoes = carregar_doacoes()

        # Filtragem flexível
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
