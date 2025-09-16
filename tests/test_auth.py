import unittest
from src.auth import registrar_usuario, autenticar
from src.persistencia import salvar_json


class TestAuth(unittest.TestCase):
    def setUp(self):
        # zera usuários antes de cada teste
        salvar_json("usuarios.json", [])

    def test_registrar_e_autenticar(self):
        registrar_usuario("teste", "123")
        self.assertTrue(autenticar("teste", "123"))

    def test_usuario_inexistente(self):
        self.assertFalse(autenticar("nao_existe", "senha"))


if __name__ == "__main__":
    unittest.main()
