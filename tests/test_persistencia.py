import unittest
from src.persistencia import salvar_json, carregar_json


class TestPersistencia(unittest.TestCase):
    def test_salvar_e_carregar(self):
        dados = [{"x": 1}]
        salvar_json("teste.json", dados)
        resultado = carregar_json("teste.json")
        self.assertEqual(dados, resultado)


if __name__ == "__main__":
    unittest.main()
