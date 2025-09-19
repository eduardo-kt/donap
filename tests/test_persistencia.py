# tests/test_persistencia.py
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from src import persistencia
from src.main import buscar_donatarios


class TestPersistencia(unittest.TestCase):
    def test_salvar_e_carregar_generico(self):
        """Testa salvar e carregar JSON genérico."""
        with TemporaryDirectory() as tmpdir:
            arquivo = Path(tmpdir) / "teste.json"
            dados = [{"x": 1}]
            persistencia.salvar_json(arquivo, dados)
            resultado = persistencia.carregar_json(arquivo)
            self.assertEqual(dados, resultado)

    def test_salvar_e_carregar_donatario(self):
        """Testa salvar e carregar um donatário usando arquivo temporário."""
        with TemporaryDirectory() as tmpdir:
            arquivo = Path(tmpdir) / "donatarios.json"

            # inicializa arquivo vazio
            persistencia.salvar_json(arquivo, [])
            self.assertEqual(persistencia.carregar_json(arquivo), [])

            # redefine ARQ_DONATARIOS para usar o arquivo temporário
            persistencia.ARQ_DONATARIOS = arquivo

            donatario = {
                "nome": "Teste",
                "data_nascimento": "01/01/2000",
                "cpf": "12345678900",
            }
            persistencia.salvar_donatario(donatario)

            # verifica se foi salvo corretamente
            donatarios = persistencia.carregar_donatarios()
            self.assertIn(donatario, donatarios)

    def test_carregar_donatarios_arquivo_vazio(self):
        """Testa comportamento com arquivo JSON vazio."""
        with TemporaryDirectory() as tmpdir:
            arquivo = Path(tmpdir) / "donatarios.json"
            arquivo.touch()  # cria arquivo vazio

            persistencia.ARQ_DONATARIOS = arquivo

            donatarios = persistencia.carregar_donatarios()
            self.assertEqual(donatarios, [])

    def test_buscar_donatarios(self):

        with TemporaryDirectory() as tmpdir:
            arquivo = Path(tmpdir) / "donatarios.json"

            # dados de teste
            donatarios = [
                {
                    "nome": "João Silva",
                    "data_nascimento": "1990-01-01",
                    "cpf": "123",
                },
                {
                    "nome": "Maria Souza",
                    "data_nascimento": "1995-05-05",
                    "cpf": "456",
                },
            ]

            # salva no arquivo temporário
            persistencia.salvar_json(arquivo, donatarios)
            persistencia.ARQ_DONATARIOS = arquivo

            # busca por nome parcial
            resultados = buscar_donatarios("joão")
            self.assertEqual(len(resultados), 1)
            self.assertEqual(resultados[0]["cpf"], "123")

            # busca por CPF
            resultados = buscar_donatarios("456")
            self.assertEqual(len(resultados), 1)
            self.assertEqual(resultados[0]["nome"], "Maria Souza")

            # busca sem resultados
            resultados = buscar_donatarios("Pedro")
            self.assertEqual(len(resultados), 0)


if __name__ == "__main__":
    unittest.main()
