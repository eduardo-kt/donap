import tkinter as tk
from tkinter import messagebox
from src.auth import autenticar, registrar_usuario


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


def tela_menu():
    root = tk.Tk()
    root.title("Menu Principal")

    tk.Label(root, text="Bem-vindo! Escolha uma opção:").pack()

    tk.Button(
        root, text="Cadastrar Donatário", command=lambda: print("Cadastrar...")
    ).pack()
    tk.Button(
        root, text="Cadastrar Donativo", command=lambda: print("Cadastrar...")
    ).pack()
    tk.Button(
        root, text="Consultar Donatário", command=lambda: print("Consultar...")
    ).pack()
    tk.Button(root, text="Sair", command=root.destroy).pack()

    root.mainloop()


def testar_login(usuario, senha):
    return autenticar(usuario, senha)


if __name__ == "__main__":
    tela_login()
