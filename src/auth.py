from persistencia import load_json, save_json


def registrar_usuario(username, senha):
    usuarios = load_json("usuarios.json")
    if any(u["username"] == username for u in usuarios):
        raise ValueError("Usuário já existe")
    usuarios.append({"username": username, "senha": senha})
    save_json("usuarios.json", usuarios)


def autenticar(username, senha):
    usuarios = load_json("usuarios.json")
    return any(u["username"] == username and u["senha"] == senha for u in usuarios)
