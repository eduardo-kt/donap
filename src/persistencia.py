import json
from pathlib import Path


def carregar_json(arquivo):
    path = Path("data") / arquivo
    if not path.exists():
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # arquivo vazio ou inválido → começa com lista vazia
        return []


def salvar_json(arquivo, dados):
    path = Path("data") / arquivo
    path.parent.mkdir(parents=True, exist_ok=True)  # pasta data existir
    with open(path, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


# -------- Funções específicas --------
ARQ_DONATARIOS = "donatarios.json"
ARQ_DOACOES = "doacoes.json"


# --- Donatários ---
def carregar_donatarios():
    return carregar_json(ARQ_DONATARIOS)


def salvar_donatario(donatario):
    donatarios = carregar_donatarios()
    donatarios.append(donatario)
    salvar_json(ARQ_DONATARIOS, donatarios)


# --- Doações ---
def carregar_doacoes():
    return carregar_json(ARQ_DOACOES)


def salvar_doacao(doacao):
    doacoes = carregar_doacoes()
    doacoes.append(doacao)
    salvar_json(ARQ_DOACOES, doacoes)
