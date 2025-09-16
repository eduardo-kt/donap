import json
from pathlib import Path


def load_json(arquivo):
    path = Path("data") / arquivo
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(arquivo, dados):
    path = Path("data") / arquivo
    with open(path, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)
