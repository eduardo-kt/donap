# tests/test_main.py
import unittest
from src.main import testar_login
from src.auth import registrar_usuario


class TestMainLogic(unittest.TestCase):

    def test_login_valido(self):
        registrar_usuario("user1", "1234")
        self.assertTrue(testar_login("user1", "1234"))

    def test_login_invalido(self):
        self.assertFalse(testar_login("user2", "senha_errada"))
