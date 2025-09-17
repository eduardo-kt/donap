# tests/test_persistencia.py
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from src.persistencia import (
    salvar_json,
    carregar_json,
    salvar_donatario,
    carregar_donatarios,
)


class TestPersistencia(unittest.TestCase):
    def test_salvar_e_carregar_generico(self):

        dados = [{"x": 1}]
        salvar_json("teste.json", dados)
        resultado = carregar_json("teste.json")
        self.assertEqual(dados, resultado)

    def test_salvar_e_carregar_donatario(self):

        with TemporaryDirectory() as tmpdir:
            arquivo = Path(tmpdir) / "donatarios.json"

            # Inicializa o arquivo vazio
            salvar_json(arquivo.name, [])
            self.assertEqual(carregar_json(arquivo.name), [])

            # Salva um donatário
            donatario = {
                "nome": "Teste",
                "data_nascimento": "01/01/2000",
                "cpf": "12345678900",
            }
            # Redefine funções temporariamente para usar o arquivo temporário
            from src import persistencia

            persistencia.ARQ_DONATARIOS = arquivo.name
            salvar_donatario(donatario)

            # Verifica se o donatário foi adicionado
            donatarios = carregar_donatarios()
            self.assertIn(donatario, donatarios)

    def test_carregar_donatarios_arquivo_vazio(self):

        with TemporaryDirectory() as tmpdir:
            arquivo = Path(tmpdir) / "donatarios.json"
            arquivo.touch()  # cria o arquivo vazio

            from src import persistencia

            persistencia.ARQ_DONATARIOS = arquivo.name

            donatarios = carregar_donatarios()
            self.assertEqual(donatarios, [])  # deve retornar lista vazia


if __name__ == "__main__":
    unittest.main()
