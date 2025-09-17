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
    with open(path, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)
